from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
import requests as http_requests
from .models import WebhookEndpoint, CapturedRequest


def webhook_tester_page(request):
    """Render the webhook tester page."""
    return render(request, 'apiutils/webhook-tester.html')


@csrf_exempt
@require_http_methods(["POST"])
def create_endpoint(request):
    """Create a new webhook endpoint and return its URL."""
    # Get or create session key
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    # Get name from request body
    try:
        data = json.loads(request.body) if request.body else {}
        name = data.get('name', '')
    except json.JSONDecodeError:
        name = ''
    
    endpoint = WebhookEndpoint.objects.create(session_key=session_key, name=name)
    
    return JsonResponse({
        'id': str(endpoint.id),
        'name': endpoint.name,
        'url': request.build_absolute_uri(f'/hook/{endpoint.id}/'),
        'expires_at': endpoint.expires_at.isoformat(),
        'created_at': endpoint.created_at.isoformat(),
        'is_expired': False,
        'request_count': 0
    })


def list_endpoints(request):
    """List all webhook endpoints for the current session."""
    if not request.session.session_key:
        return JsonResponse({'endpoints': []})
    
    session_key = request.session.session_key
    endpoints = WebhookEndpoint.objects.filter(session_key=session_key).order_by('-created_at')
    
    return JsonResponse({
        'endpoints': [
            {
                'id': str(e.id),
                'name': e.name,
                'url': request.build_absolute_uri(f'/hook/{e.id}/'),
                'created_at': e.created_at.isoformat(),
                'expires_at': e.expires_at.isoformat(),
                'is_expired': e.is_expired,
                'request_count': e.requests.count()
            } for e in endpoints
        ]
    })



@csrf_exempt
@require_http_methods(["POST"])
def delete_endpoint(request, endpoint_id):
    """Delete a webhook endpoint."""
    endpoint = get_object_or_404(WebhookEndpoint, id=endpoint_id)
    endpoint.delete()
    return JsonResponse({'success': True})


@csrf_exempt

def capture_webhook(request, endpoint_id):
    """Capture incoming webhook requests at /hook/<uuid>/."""
    try:
        endpoint = WebhookEndpoint.objects.get(id=endpoint_id)
    except WebhookEndpoint.DoesNotExist:
        return JsonResponse({'error': 'Endpoint not found'}, status=404)
    
    if endpoint.is_expired:
        return JsonResponse({'error': 'Endpoint expired'}, status=410)
    
    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # Capture the request
    CapturedRequest.objects.create(
        endpoint=endpoint,
        method=request.method,
        headers=dict(request.headers),
        body=request.body.decode('utf-8', errors='replace'),
        content_type=request.content_type or '',
        query_params=dict(request.GET),
        ip_address=ip
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Webhook received'
    })


def get_requests(request, endpoint_id):
    """Get all captured requests for an endpoint."""
    endpoint = get_object_or_404(WebhookEndpoint, id=endpoint_id)
    
    captured = endpoint.requests.all()[:100]  # Limit to 100 most recent
    
    return JsonResponse({
        'endpoint_id': str(endpoint.id),
        'is_expired': endpoint.is_expired,
        'expires_at': endpoint.expires_at.isoformat(),
        'requests': [
            {
                'id': r.id,
                'method': r.method,
                'headers': r.headers,
                'body': r.body,
                'content_type': r.content_type,
                'query_params': r.query_params,
                'ip_address': r.ip_address,
                'received_at': r.received_at.isoformat()
            } for r in captured
        ]
    })


@csrf_exempt
@require_http_methods(["POST"])
def clear_requests(request, endpoint_id):
    """Clear all captured requests for an endpoint."""
    endpoint = get_object_or_404(WebhookEndpoint, id=endpoint_id)
    count = endpoint.requests.count()
    endpoint.requests.all().delete()
    
    return JsonResponse({
        'success': True,
        'deleted': count
    })


@csrf_exempt
@require_http_methods(["POST"])
def send_request(request):
    """Send a test request to user's webhook URL (proxy)."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    url = data.get('url')
    if not url:
        return JsonResponse({'error': 'URL is required'}, status=400)
    
    method = data.get('method', 'POST').upper()
    headers = data.get('headers', {})
    body = data.get('body', '')
    
    try:
        response = http_requests.request(
            method=method,
            url=url,
            headers=headers,
            data=body,
            timeout=30,
            allow_redirects=True
        )
        
        return JsonResponse({
            'status': response.status_code,
            'status_text': response.reason,
            'headers': dict(response.headers),
            'body': response.text,
            'time_ms': round(response.elapsed.total_seconds() * 1000, 2),
            'url': response.url
        })
    except http_requests.exceptions.Timeout:
        return JsonResponse({'error': 'Request timed out (30s limit)'}, status=504)
    except http_requests.exceptions.ConnectionError as e:
        return JsonResponse({'error': f'Connection failed: {str(e)}'}, status=502)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
