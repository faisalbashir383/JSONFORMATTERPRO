"""
JSON Formatter API Views
This module contains API endpoints for JSON formatting, validation, minification, and conversion.
"""

import json
import csv
import io
import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


@api_view(['POST'])
def format_json(request):
    """
    Format JSON with proper indentation.
    
    Expected input: {"data": "json_string"}
    Returns: {"formatted": "formatted_json_string", "success": true}
    """
    try:
        # Get JSON data from request
        json_string = request.data.get('data', '')
        
        if not json_string:
            return Response({
                'success': False,
                'error': 'No JSON data provided. Please provide JSON data in the request body.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse and format JSON
        parsed_json = json.loads(json_string)
        formatted_json = json.dumps(parsed_json, indent=2, sort_keys=False, ensure_ascii=False)
        
        return Response({
            'success': True,
            'formatted': formatted_json
        })
    
    except json.JSONDecodeError as e:
        return Response({
            'success': False,
            'error': f'Invalid JSON: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def minify_json(request):
    """
    Minify JSON by removing all whitespace.
    
    Expected input: {"data": "json_string"}
    Returns: {"minified": "minified_json_string", "success": true}
    """
    try:
        # Get JSON data from request
        json_string = request.data.get('data', '')
        
        if not json_string:
            return Response({
                'success': False,
                'error': 'No JSON data provided. Please provide JSON data in the request body.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse and minify JSON
        parsed_json = json.loads(json_string)
        minified_json = json.dumps(parsed_json, separators=(',', ':'), ensure_ascii=False)
        
        return Response({
            'success': True,
            'minified': minified_json
        })
    
    except json.JSONDecodeError as e:
        return Response({
            'success': False,
            'error': f'Invalid JSON: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def validate_json(request):
    """
    Validate JSON structure.
    
    Expected input: {"data": "json_string"}
    Returns: {"valid": true/false, "message": "validation_message"}
    """
    try:
        # Get JSON data from request
        json_string = request.data.get('data', '')
        
        if not json_string:
            return Response({
                'success': False,
                'valid': False,
                'message': 'No JSON data provided. Please provide JSON data in the request body.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to parse JSON
        parsed_json = json.loads(json_string)
        
        return Response({
            'success': True,
            'valid': True,
            'message': '✓ Valid JSON! Your JSON is correctly structured.',
            'data': parsed_json
        })
    
    except json.JSONDecodeError as e:
        return Response({
            'success': False,
            'valid': False,
            'message': f'Invalid JSON: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'valid': False,
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def convert_to_xml(request):
    """
    Convert JSON to XML format.
    
    Expected input: {"data": "json_string"}
    Returns: {"xml": "xml_string", "success": true}
    """
    try:
        # Get JSON data from request
        json_string = request.data.get('data', '')
        
        if not json_string:
            return Response({
                'success': False,
                'error': 'No JSON data provided. Please provide JSON data in the request body.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse JSON
        parsed_json = json.loads(json_string)
        
        # Convert to XML
        xml_string = dicttoxml(parsed_json, custom_root='root', attr_type=False)
        
        # Pretty print XML
        dom = parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        # Remove empty lines and XML declaration
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        
        return Response({
            'success': True,
            'xml': pretty_xml
        })
    
    except json.JSONDecodeError as e:
        return Response({
            'success': False,
            'error': f'Invalid JSON: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def convert_to_csv(request):
    """
    Convert JSON to CSV format.
    
    Expected input: {"data": "json_string"}
    Returns: {"csv": "csv_string", "success": true}
    """
    try:
        # Get JSON data from request
        json_string = request.data.get('data', '')
        
        if not json_string:
            return Response({
                'success': False,
                'error': 'No JSON data provided. Please provide JSON data in the request body.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse JSON
        parsed_json = json.loads(json_string)
        
        # Convert to CSV
        output = io.StringIO()
        
        # Handle array of objects
        if isinstance(parsed_json, list) and len(parsed_json) > 0:
            if isinstance(parsed_json[0], dict):
                # Get all unique keys from all objects
                keys = set()
                for item in parsed_json:
                    if isinstance(item, dict):
                        keys.update(item.keys())
                keys = sorted(list(keys))
                
                writer = csv.DictWriter(output, fieldnames=keys)
                writer.writeheader()
                
                for item in parsed_json:
                    if isinstance(item, dict):
                        writer.writerow(item)
                    else:
                        # Handle non-dict items in array
                        writer.writerow({keys[0]: item})
            else:
                # Simple array
                writer = csv.writer(output)
                writer.writerow(['value'])
                for item in parsed_json:
                    writer.writerow([item])
        
        # Handle single object
        elif isinstance(parsed_json, dict):
            writer = csv.DictWriter(output, fieldnames=parsed_json.keys())
            writer.writeheader()
            writer.writerow(parsed_json)
        
        # Handle primitive values
        else:
            writer = csv.writer(output)
            writer.writerow(['value'])
            writer.writerow([parsed_json])
        
        csv_string = output.getvalue()
        
        return Response({
            'success': True,
            'csv': csv_string
        })
    
    except json.JSONDecodeError as e:
        return Response({
            'success': False,
            'error': f'Invalid JSON: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def base64_encode(request):
    """
    Encode text to Base64.
    
    Expected input: {"data": "text_to_encode"}
    Returns: {"encoded": "base64_string", "success": true}
    """
    try:
        # Get text data from request
        text_data = request.data.get('data', '')
        
        if not text_data:
            return Response({
                'success': False,
                'error': 'No data provided. Please provide text data in the request body.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Encode to Base64
        encoded_bytes = base64.b64encode(text_data.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        
        return Response({
            'success': True,
            'encoded': encoded_string
        })
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def base64_decode(request):
    """
    Decode Base64 to text.
    
    Expected input: {"data": "base64_string"}
    Returns: {"decoded": "decoded_text", "success": true}
    """
    try:
        # Get Base64 data from request
        base64_data = request.data.get('data', '')
        
        if not base64_data:
            return Response({
                'success': False,
                'error': 'No data provided. Please provide Base64 data in the request body.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove whitespace and newlines
        base64_data = base64_data.strip().replace('\n', '').replace('\r', '').replace(' ', '')
        
        # Decode from Base64
        try:
            decoded_bytes = base64.b64decode(base64_data)
            decoded_string = decoded_bytes.decode('utf-8')
            
            return Response({
                'success': True,
                'decoded': decoded_string
            })
        except Exception as decode_error:
            return Response({
                'success': False,
                'error': f'Invalid Base64 data: {str(decode_error)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ====================
# Page Views
# ====================

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, BlogCategory


def base64_page(request):
    """Render the Base64 encode/decode page"""
    return render(request, 'base64.html')


def about_page(request):
    """Render the About Us page"""
    return render(request, 'about.html')


def contact_page(request):
    """Render the Contact Us page and handle form submissions"""
    from .models import ContactMessage
    from django.contrib import messages
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        # Validate required fields
        errors = []
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email:
            errors.append('Please enter a valid email address.')
        if not subject:
            errors.append('Subject is required.')
        if not message_text:
            errors.append('Message is required.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Get client IP and user agent
                def get_client_ip(req):
                    x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0].strip()
                    else:
                        ip = req.META.get('REMOTE_ADDR')
                    return ip
                
                ip_address = get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                
                # Create contact message
                contact = ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message_text,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                
                messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
                
                # Redirect to prevent form resubmission
                from django.shortcuts import redirect
                return redirect('contact_page')
                
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}. Please try again.')
    
    return render(request, 'contact.html')


def privacy_page(request):
    """Render the Privacy Policy page"""
    return render(request, 'privacy.html')


def json_to_yaml_page(request):
    """Render the JSON to YAML converter page"""
    return render(request, 'json-to-yaml.html')


def csv_to_json_page(request):
    """Render the CSV to JSON converter page"""
    return render(request, 'csv-to-json.html')


def json_diff_page(request):
    """Render the JSON Diff comparison tool page"""
    return render(request, 'json-diff.html')


def json_schema_page(request):
    """Render the JSON Schema Validator page"""
    return render(request, 'json-schema.html')


def json_tree_page(request):
    """Render the JSON Tree Viewer page"""
    return render(request, 'json-tree.html')


def json_visualizer_page(request):
    """Render the JSON Visualizer page with graph view"""
    return render(request, 'json-visualizer.html')


def dummy_json_page(request):
    """Render the Dummy JSON Generator page"""
    return render(request, 'dummy-json.html')



def robots_txt(request):
    """Serve robots.txt file"""
    return render(request, 'robots.txt', content_type='text/plain')


# ====================
# Blog Views
# ====================

def blog_list(request):
    """List all published blog posts with pagination and filtering"""
    posts = BlogPost.objects.filter(published=True)
    total_posts = posts.count()
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Search
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = BlogCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'query': query,
        'total_posts': total_posts,
    }
    
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    """Display individual blog post"""
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    
    # Increment views
    post.increment_views()
    
    # Get related posts
    related_posts = post.get_related_posts()
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog_detail.html', context)


def blog_category(request, slug):
    """Filter blog posts by category"""
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.objects.filter(category=category, published=True)
    total_posts = BlogPost.objects.filter(published=True).count()
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    all_categories = BlogCategory.objects.all()
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'categories': all_categories,
        'current_category': slug,
        'total_posts': total_posts,
    }
    
    return render(request, 'blog_list.html', context)


# ====================
# API & Network Tools Pages
# ====================

def http_headers_page(request):
    """Render the HTTP Headers Parser page"""
    return render(request, 'http-headers.html')


def ip_info_page(request):
    """Render the IP Address Info page"""
    return render(request, 'ip-info.html')


def dns_lookup_page(request):
    """Render the DNS Lookup page"""
    return render(request, 'dns-lookup.html')


def ssl_checker_page(request):
    """Render the SSL Certificate Checker page"""
    return render(request, 'ssl-checker.html')


def cors_checker_page(request):
    """Render the CORS Checker page"""
    return render(request, 'cors-checker.html')


# ====================
# Code Tools Pages
# ====================

def cron_builder_page(request):
    """Render the Cron Builder page"""
    return render(request, 'cron-builder.html')


def markdown_preview_page(request):
    """Render the Markdown Preview page"""
    return render(request, 'markdown-preview.html')


def sql_formatter_page(request):
    """Render the SQL Formatter page"""
    return render(request, 'sql-formatter.html')


def qr_generator_page(request):
    """Render the QR Code Generator page"""
    return render(request, 'qr-generator.html')


def meta_tag_generator_page(request):
    """Render the Meta Tag Generator page"""
    return render(request, 'meta-tag-generator.html')


def mock_api_generator_page(request):
    """Render the Mock API Generator page"""
    return render(request, 'mock-api-generator.html')


def push_notification_tester_page(request):
    """Render the Push Notification Tester page"""
    return render(request, 'push-notification-tester.html')


def api_response_tester_page(request):
    """Render the API Response Tester page"""
    return render(request, 'api-response-tester.html')


def image_to_base64_page(request):
    """Render the Image to Base64 Converter page"""
    return render(request, 'image-to-base64.html')


def json_editor_page(request):
    """Render the JSON Editor page"""
    return render(request, 'json-editor.html')


def regex_tester_page(request):
    """Render the Regex Tester page"""
    return render(request, 'regex-tester.html')


def swagger_viewer_page(request):
    """Render the Swagger/OpenAPI Viewer page"""
    return render(request, 'swagger-viewer.html')


def lorem_ipsum_page(request):
    """Render the Lorem Ipsum Generator page"""
    return render(request, 'lorem-ipsum.html')


# ====================
# Custom Error Handlers
# ====================

def custom_404(request, exception):
    """
    Custom 404 error handler
    Returns SEO-friendly 404 page with noindex meta tag
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Custom 500 error handler
    Returns user-friendly 500 page
    """
    return render(request, '500.html', status=500)


@api_view(['POST'])
def generate_qr_code(request):
    """
    Generate QR code from text/URL using Python qrcode library.
    Returns base64 encoded PNG image.
    
    Expected input: {
        "content": "text or URL",
        "size": 256 (optional, default 256),
        "fg_color": "#000000" (optional),
        "bg_color": "#FFFFFF" (optional)
    }
    """
    import qrcode
    from PIL import Image
    import io
    
    try:
        content = request.data.get('content', '').strip()
        size = int(request.data.get('size', 256))
        fg_color = request.data.get('fg_color', '#000000')
        bg_color = request.data.get('bg_color', '#FFFFFF')
        
        if not content:
            return Response({
                'success': False,
                'error': 'Content is required. Please provide text or URL.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Limit size to reasonable bounds
        size = max(64, min(size, 1024))
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)
        
        # Create image with colors
        qr_img = qr.make_image(fill_color=fg_color, back_color=bg_color)
        
        # Convert to PIL Image (the make_image returns a PilImage wrapper)
        # Get the underlying PIL image
        if hasattr(qr_img, 'get_image'):
            pil_img = qr_img.get_image()
        else:
            pil_img = qr_img
        
        # Convert to RGB mode for proper PNG saving
        if pil_img.mode != 'RGB':
            pil_img = pil_img.convert('RGB')
        
        # Resize to requested size
        pil_img = pil_img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Convert to base64
        buffer = io.BytesIO()
        pil_img.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return Response({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'size': size
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': f'Failed to generate QR code: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ====================
# API Endpoints for Network Tools
# ====================

import socket
import ssl
import re
from datetime import datetime
from urllib.parse import urlparse


@api_view(['POST'])
def dns_lookup_api(request):
    """
    Perform DNS lookup for a domain.
    Returns A, AAAA records with geolocation info for each IP.
    """
    import requests as http_requests
    
    try:
        domain = request.data.get('domain', '').strip()
        
        if not domain:
            return Response({'error': 'Domain is required'}, status=400)
        
        # Clean domain (remove protocol if present)
        domain = re.sub(r'^https?://', '', domain)
        domain = domain.split('/')[0]  # Remove path
        
        result = {
            'domain': domain,
            'records': {},
            'ipDetails': []
        }
        
        # A records (IPv4)
        try:
            a_records = socket.getaddrinfo(domain, None, socket.AF_INET)
            ips = list(set([r[4][0] for r in a_records]))
            result['records']['A'] = ips
        except:
            result['records']['A'] = []
        
        # AAAA records (IPv6)
        try:
            aaaa_records = socket.getaddrinfo(domain, None, socket.AF_INET6)
            ipv6s = list(set([r[4][0] for r in aaaa_records]))
            result['records']['AAAA'] = ipv6s
        except:
            result['records']['AAAA'] = []
        
        # Get hostname
        try:
            hostname = socket.gethostbyaddr(result['records']['A'][0])[0] if result['records']['A'] else None
            result['hostname'] = hostname
        except:
            result['hostname'] = None
        
        # Get geolocation for each IP (limit to first 5)
        all_ips = result['records']['A'][:5]
        for ip in all_ips:
            try:
                geo_response = http_requests.get(
                    f'http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as',
                    timeout=5
                )
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    if geo_data.get('status') == 'success':
                        result['ipDetails'].append({
                            'ip': ip,
                            'country': geo_data.get('country', ''),
                            'countryCode': geo_data.get('countryCode', ''),
                            'region': geo_data.get('regionName', ''),
                            'city': geo_data.get('city', ''),
                            'zip': geo_data.get('zip', ''),
                            'lat': geo_data.get('lat'),
                            'lon': geo_data.get('lon'),
                            'timezone': geo_data.get('timezone', ''),
                            'isp': geo_data.get('isp', ''),
                            'org': geo_data.get('org', ''),
                            'as': geo_data.get('as', '')
                        })
            except:
                # Skip if geolocation fails for this IP
                result['ipDetails'].append({
                    'ip': ip,
                    'error': 'Could not fetch location'
                })
        
        # Get nameservers using socket
        try:
            ns_info = socket.gethostbyname_ex(domain)
            result['aliases'] = ns_info[1] if ns_info[1] else []
        except:
            result['aliases'] = []
        
        return Response(result)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def ssl_checker_api(request):
    """
    Check SSL certificate for a domain.
    Returns certificate details including expiry.
    """
    try:
        domain = request.data.get('domain', '').strip()
        
        if not domain:
            return Response({'error': 'Domain is required'}, status=400)
        
        # Clean domain
        domain = re.sub(r'^https?://', '', domain)
        domain = domain.split('/')[0]
        
        # Create SSL context
        context = ssl.create_default_context()
        
        try:
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse dates
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    
                    # Calculate days until expiry
                    days_remaining = (not_after - datetime.utcnow()).days
                    
                    # Get subject and issuer
                    subject = dict(x[0] for x in cert.get('subject', []))
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    
                    result = {
                        'domain': domain,
                        'valid': True,
                        'subject': {
                            'commonName': subject.get('commonName', ''),
                            'organization': subject.get('organizationName', ''),
                        },
                        'issuer': {
                            'commonName': issuer.get('commonName', ''),
                            'organization': issuer.get('organizationName', ''),
                        },
                        'validFrom': not_before.isoformat(),
                        'validTo': not_after.isoformat(),
                        'daysRemaining': days_remaining,
                        'expired': days_remaining < 0,
                        'serialNumber': cert.get('serialNumber', ''),
                        'version': cert.get('version', ''),
                        'subjectAltNames': [x[1] for x in cert.get('subjectAltName', [])],
                    }
                    
                    return Response(result)
                    
        except ssl.SSLError as e:
            return Response({
                'domain': domain,
                'valid': False,
                'error': f'SSL Error: {str(e)}'
            })
        except socket.timeout:
            return Response({
                'domain': domain,
                'valid': False,
                'error': 'Connection timed out'
            })
        except socket.gaierror:
            return Response({
                'domain': domain,
                'valid': False,
                'error': 'Could not resolve domain'
            })
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def cors_checker_api(request):
    """
    Check CORS headers for a URL.
    Tests with different origins to check CORS policy.
    """
    import requests
    
    try:
        url = request.data.get('url', '').strip()
        test_origin = request.data.get('origin', 'https://example.com')
        
        if not url:
            return Response({'error': 'URL is required'}, status=400)
        
        # Add protocol if missing
        if not url.startswith('http'):
            url = 'https://' + url
        
        headers = {
            'Origin': test_origin,
            'User-Agent': 'Mozilla/5.0 CORS Checker'
        }
        
        try:
            # Send preflight OPTIONS request
            options_response = requests.options(url, headers=headers, timeout=10)
            
            # Send GET request
            get_response = requests.get(url, headers=headers, timeout=10)
            
            # Extract CORS headers
            cors_headers = {
                'Access-Control-Allow-Origin': get_response.headers.get('Access-Control-Allow-Origin', ''),
                'Access-Control-Allow-Methods': get_response.headers.get('Access-Control-Allow-Methods', ''),
                'Access-Control-Allow-Headers': get_response.headers.get('Access-Control-Allow-Headers', ''),
                'Access-Control-Allow-Credentials': get_response.headers.get('Access-Control-Allow-Credentials', ''),
                'Access-Control-Expose-Headers': get_response.headers.get('Access-Control-Expose-Headers', ''),
                'Access-Control-Max-Age': get_response.headers.get('Access-Control-Max-Age', ''),
            }
            
            # Determine if CORS is enabled
            allow_origin = cors_headers['Access-Control-Allow-Origin']
            cors_enabled = bool(allow_origin)
            allows_any = allow_origin == '*'
            allows_test_origin = allow_origin == test_origin or allow_origin == '*'
            
            result = {
                'url': url,
                'testOrigin': test_origin,
                'corsEnabled': cors_enabled,
                'allowsAnyOrigin': allows_any,
                'allowsTestOrigin': allows_test_origin,
                'headers': cors_headers,
                'statusCode': get_response.status_code,
            }
            
            return Response(result)
            
        except requests.exceptions.SSLError:
            return Response({'error': 'SSL certificate verification failed'}, status=400)
        except requests.exceptions.ConnectionError:
            return Response({'error': 'Could not connect to the URL'}, status=400)
        except requests.exceptions.Timeout:
            return Response({'error': 'Request timed out'}, status=400)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)


def image_resizer_page(request):
    """Render the Image Resizer tool page"""
    return render(request, 'image-resizer.html')
