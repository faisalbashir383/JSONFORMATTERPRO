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


def json_diff_page(request):
    """Render the JSON Diff comparison tool page"""
    return render(request, 'json-diff.html')


def json_schema_page(request):
    """Render the JSON Schema Validator page"""
    return render(request, 'json-schema.html')


def json_tree_page(request):
    """Render the JSON Tree Viewer page"""
    return render(request, 'json-tree.html')



def robots_txt(request):
    """Serve robots.txt file"""
    return render(request, 'robots.txt', content_type='text/plain')


# ====================
# Blog Views
# ====================

def blog_list(request):
    """List all published blog posts with pagination and filtering"""
    posts = BlogPost.objects.filter(published=True)
    
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
    }
    
    return render(request, 'blog_list.html', context)

