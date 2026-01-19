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

def xsd_to_json_schema_page(request):
    """Render the XSD to JSON Schema converter page"""
    return render(request, 'xsd-to-json-schema.html')

def json_to_jsonl_page(request):
    """Render the JSON to JSONL converter page"""
    return render(request, 'json-to-jsonl.html')


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

def dummy_json_api_page(request):
    """Render the Dummy JSON API documentation page"""
    return render(request, 'dummy-json-api.html')


def dummy_json_api_playground_page(request):
    """Render the Dummy JSON API interactive playground (noindex)"""
    return render(request, 'dummy-json-api-playground.html')


def json_tools_page(request):
    """Render the JSON Tools pillar page"""
    return render(request, 'json-tools.html')


@api_view(['GET'])
def dummy_json_users_api(request):
    """Generate random fake user data"""
    import random
    
    count = min(int(request.GET.get('count', 5)), 100)
    
    first_names = ['Emma', 'James', 'Sarah', 'Michael', 'Emily', 'David', 'Olivia', 'Daniel', 'Sophia', 'William', 'Ava', 'Alexander', 'Isabella', 'Matthew', 'Mia', 'Ethan', 'Charlotte', 'Andrew', 'Amelia', 'Joseph']
    last_names = ['Wilson', 'Rodriguez', 'Kim', 'Johnson', 'Chen', 'Smith', 'Brown', 'Davis', 'Garcia', 'Miller', 'Martinez', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Moore']
    companies = ['TechStart Inc', 'DataFlow Systems', 'CloudNine Labs', 'ByteWave', 'NexGen Solutions', 'Quantum Dynamics', 'SkyPeak Tech', 'BlueShift AI', 'InnovateCo', 'FuturePath']
    statuses = ['active', 'active', 'active', 'inactive', 'pending']
    
    users = []
    for i in range(count):
        first = random.choice(first_names)
        last = random.choice(last_names)
        user_id = i + 1
        users.append({
            'id': user_id,
            'name': f'{first} {last}',
            'email': f'{first.lower()}.{last.lower()}@example.com',
            'phone': f'+1-555-{random.randint(1000, 9999)}',
            'company': random.choice(companies),
            'status': random.choice(statuses),
            'avatar': f'https://i.pravatar.cc/150?u={user_id}'
        })
    
    # Track request
    from .models import DummyJsonApiLog
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    DummyJsonApiLog.log_request('users', ip, request.META.get('HTTP_USER_AGENT'))
    
    return Response({'success': True, 'count': count, 'data': users})


@api_view(['GET'])
def dummy_json_products_api(request):
    """Generate random fake product data"""
    import random
    
    count = min(int(request.GET.get('count', 10)), 100)
    
    products_list = [
        ('Wireless Headphones', 'Electronics'), ('Smart Watch', 'Electronics'), ('Bluetooth Speaker', 'Electronics'),
        ('Ergonomic Chair', 'Furniture'), ('Standing Desk', 'Furniture'), ('LED Desk Lamp', 'Furniture'),
        ('Running Shoes', 'Sports'), ('Yoga Mat', 'Sports'), ('Dumbbell Set', 'Sports'),
        ('Coffee Maker', 'Kitchen'), ('Air Fryer', 'Kitchen'), ('Blender Pro', 'Kitchen'),
        ('Laptop Backpack', 'Accessories'), ('Leather Wallet', 'Accessories'), ('Sunglasses', 'Accessories')
    ]
    
    products = []
    for i in range(count):
        name, category = random.choice(products_list)
        product_id = i + 1
        products.append({
            'id': product_id,
            'name': f'{name} {random.choice(["Pro", "Plus", "Max", "Lite", "X", ""])}',
            'price': round(random.uniform(19.99, 499.99), 2),
            'category': category,
            'inStock': random.choice([True, True, True, False]),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'image': f'https://picsum.photos/seed/product{product_id}/300/300'
        })
    
    # Track request
    from .models import DummyJsonApiLog
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    DummyJsonApiLog.log_request('products', ip, request.META.get('HTTP_USER_AGENT'))
    
    return Response({'success': True, 'count': count, 'data': products})


@api_view(['GET'])
def dummy_json_posts_api(request):
    """Generate random fake blog post data"""
    import random
    from datetime import datetime, timedelta
    
    count = min(int(request.GET.get('count', 5)), 100)
    
    titles = ['Getting Started with React', 'Python Best Practices', 'Introduction to Machine Learning', 
              'Docker for Beginners', 'REST API Design Patterns', 'Building Microservices', 
              'JavaScript ES6 Features', 'Cloud Architecture Basics', 'Database Optimization Tips',
              'Security Best Practices', 'CI/CD Pipeline Setup', 'Testing Strategies']
    authors = ['John Developer', 'Jane Coder', 'Alex Engineer', 'Sam Architect', 'Chris DevOps']
    
    posts = []
    for i in range(count):
        date = datetime.now() - timedelta(days=random.randint(1, 365))
        post_id = i + 1
        author_id = random.randint(1, 50)
        posts.append({
            'id': post_id,
            'title': random.choice(titles),
            'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            'author': random.choice(authors),
            'authorAvatar': f'https://i.pravatar.cc/100?u=author{author_id}',
            'date': date.strftime('%Y-%m-%d'),
            'views': random.randint(100, 10000),
            'thumbnail': f'https://picsum.photos/seed/post{post_id}/400/200'
        })
    
    # Track request
    from .models import DummyJsonApiLog
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    DummyJsonApiLog.log_request('posts', ip, request.META.get('HTTP_USER_AGENT'))
    
    return Response({'success': True, 'count': count, 'data': posts})


@api_view(['GET'])
def dummy_json_comments_api(request):
    """Generate random fake comment data"""
    import random
    
    count = min(int(request.GET.get('count', 5)), 100)
    
    names = ['Alice Johnson', 'Bob Smith', 'Carol Williams', 'David Brown', 'Eva Martinez', 'Frank Lee', 'Grace Kim', 'Henry Davis']
    
    comments = []
    for i in range(count):
        name = random.choice(names)
        commenter_id = random.randint(1, 100)
        comments.append({
            'id': i + 1,
            'name': name,
            'email': f'{name.split()[0].lower()}@example.com',
            'avatar': f'https://i.pravatar.cc/80?u=commenter{commenter_id}',
            'body': random.choice([
                'Great article! Very informative and well written.',
                'Thanks for sharing this, it really helped me understand the topic.',
                'I have a question about the third point you mentioned.',
                'This is exactly what I was looking for. Bookmarked!',
                'Could you elaborate more on the implementation details?'
            ]),
            'postId': random.randint(1, 100)
        })
    
    # Track request
    from .models import DummyJsonApiLog
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    DummyJsonApiLog.log_request('comments', ip, request.META.get('HTTP_USER_AGENT'))
    
    return Response({'success': True, 'count': count, 'data': comments})


@api_view(['GET'])
def dummy_json_todos_api(request):
    """Generate random fake todo data"""
    import random
    from datetime import datetime, timedelta
    
    count = min(int(request.GET.get('count', 5)), 100)
    
    tasks = [
        'Complete project documentation', 'Review pull request', 'Fix login bug',
        'Update dependencies', 'Write unit tests', 'Refactor authentication module',
        'Design new dashboard', 'Implement search feature', 'Optimize database queries',
        'Deploy to staging', 'Code review', 'Team meeting', 'Update README'
    ]
    priorities = ['low', 'medium', 'medium', 'high', 'critical']
    
    todos = []
    for i in range(count):
        due = datetime.now() + timedelta(days=random.randint(1, 30))
        todos.append({
            'id': i + 1,
            'title': random.choice(tasks),
            'completed': random.choice([True, False, False]),
            'priority': random.choice(priorities),
            'dueDate': due.strftime('%Y-%m-%d')
        })
    
    # Track request
    from .models import DummyJsonApiLog
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    DummyJsonApiLog.log_request('todos', ip, request.META.get('HTTP_USER_AGENT'))
    
    return Response({'success': True, 'count': count, 'data': todos})


@api_view(['GET'])
def dummy_json_companies_api(request):
    """Generate random fake company data"""
    import random
    
    count = min(int(request.GET.get('count', 5)), 100)
    
    company_names = ['TechCorp', 'DataVerse', 'CloudNine', 'ByteWorks', 'NexGen', 'SkyPeak', 'BlueShift', 'InnovateCo', 'FuturePath', 'QuantumLeap']
    industries = ['Technology', 'Finance', 'Healthcare', 'E-commerce', 'Manufacturing', 'Consulting', 'Education']
    suffixes = ['Inc', 'LLC', 'Corp', 'Group', 'Solutions', 'Labs', 'Systems']
    
    companies = []
    for i in range(count):
        company_id = i + 1
        company_name = random.choice(company_names)
        companies.append({
            'id': company_id,
            'name': f'{company_name} {random.choice(suffixes)}',
            'industry': random.choice(industries),
            'employees': random.randint(10, 10000),
            'revenue': f'${random.randint(1, 500)}M',
            'founded': random.randint(1990, 2023),
            'logo': f'https://ui-avatars.com/api/?name={company_name}&size=128&background=random'
        })
    
    # Track request
    from .models import DummyJsonApiLog
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    DummyJsonApiLog.log_request('companies', ip, request.META.get('HTTP_USER_AGENT'))
    
    return Response({'success': True, 'count': count, 'data': companies})


def json_generator_page(request):
    """Render the JSON Generator & Streaming Tool page"""
    return render(request, 'json-generator.html')


def json_formatter_online_page(request):
    """Render the JSON Formatter Online SEO landing page"""
    return render(request, 'json-formatter-online.html')


def json_formatter_page(request):
    """Render the JSON Formatter SEO authority page"""
    return render(request, 'json-formatter.html')


def string_json_to_json_page(request):
    """Render the String JSON to JSON converter page"""
    return render(request, 'string-json-to-json.html')


def json_to_string_page(request):
    """Render the JSON to String (stringify) converter page"""
    return render(request, 'json-to-string.html')


def json_path_tester_page(request):
    """Render the JSON Path Tester tool page"""
    return render(request, 'json-path-tester.html')


def robots_txt(request):
    """Serve robots.txt file"""
    return render(request, 'robots.txt', content_type='text/plain')


def llms_txt(request):
    """Serve llms.txt file for LLM crawlers"""
    return render(request, 'llms.txt', content_type='text/plain')


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
    
    # Get previous and next posts for navigation
    previous_post = BlogPost.objects.filter(
        published=True,
        published_at__lt=post.published_at
    ).order_by('-published_at').first()
    
    next_post = BlogPost.objects.filter(
        published=True,
        published_at__gt=post.published_at
    ).order_by('published_at').first()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'previous_post': previous_post,
        'next_post': next_post,
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


@api_view(['GET'])
def blog_api(request):
    """
    API endpoint to get published blog posts for AJAX lazy loading.
    Returns JSON with blog post data.
    
    Query params:
        - limit: Number of posts to return (default: 10, max: 50)
        - category: Filter by category slug
    """
    try:
        limit = min(int(request.GET.get('limit', 10)), 50)
        category_slug = request.GET.get('category', None)

        # order by views descending
        posts = BlogPost.objects.filter(published=True).order_by('-views')
        
        if category_slug:
            posts = posts.filter(category__slug=category_slug)
        
        posts = posts[:limit]
        
        posts_data = []
        for post in posts:
            posts_data.append({
                'title': post.title,
                'slug': post.slug,
                'excerpt': post.excerpt[:150] + '...' if len(post.excerpt) > 150 else post.excerpt,
                'url': f'/blog/{post.slug}/',
                'category': post.category.name if post.category else '',
                'published_at': post.published_at.strftime('%b %d, %Y') if post.published_at else '',
                'reading_time': post.reading_time,
                'views': post.views,
                'tags': post.get_tags_list()[:3],  # First 3 tags
            })
        
        return Response({
            'success': True,
            'posts': posts_data,
            'count': len(posts_data)
        })
    
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


def json_to_code_page(request):
    """Render the JSON to Code Converter page"""
    return render(request, 'json-to-code.html')


def swagger_viewer_page(request):
    """Render the Swagger/OpenAPI Viewer page"""
    return render(request, 'swagger-viewer.html')


def openapi_builder_page(request):
    """Render the OpenAPI Builder/Editor page"""
    return render(request, 'openapi-builder.html')


def redoc_viewer_page(request):
    """Render the ReDoc Viewer page"""
    return render(request, 'redoc-viewer.html')


def parquet_viewer_page(request):
    """Render the Parquet Viewer page"""
    return render(request, 'parquet-viewer.html')


def comma_separator_page(request):
    """Render the Comma Separator/Delimiter tool page"""
    return render(request, 'comma-separator.html')


def json_fixer_page(request):
    """Render the JSON Fixer tool page"""
    return render(request, 'json-fixer.html')



def lorem_ipsum_page(request):
    """Render the Lorem Ipsum Generator page"""
    return render(request, 'lorem-ipsum.html')


def resume_builder(request):
    """Render the Resume Builder page"""
    return render(request, 'resume-builder.html')


# ====================
# Calculator Pages
# ====================

def calculator_page(request):
    """Render the Simple Calculator page with Basic/Scientific modes"""
    return render(request, 'calculator.html')


def percentage_calculator_page(request):
    """Render the Percentage Calculator page"""
    return render(request, 'percentage-calculator.html')


def age_calculator_page(request):
    """Render the Age Calculator page"""
    return render(request, 'age-calculator.html')


def date_calculator_page(request):
    """Render the Date Calculator page"""
    return render(request, 'date-calculator.html')


def loan_calculator_page(request):
    """Render the Loan/EMI Calculator page"""
    return render(request, 'loan-calculator.html')


def mortgage_calculator_page(request):
    """Render the Mortgage Calculator page"""
    return render(request, 'mortgage-calculator.html')


def car_payment_calculator_page(request):
    """Render the Car Payment Calculator page"""
    return render(request, 'car-payment-calculator.html')


def sip_calculator_page(request):
    """Render the SIP Calculator page"""
    return render(request, 'sip-calculator.html')


def compound_interest_calculator_page(request):
    """Render the Compound Interest Calculator page"""
    return render(request, 'compound-interest-calculator.html')


def salary_calculator_page(request):
    """Render the Salary Calculator page"""
    return render(request, 'salary-calculator.html')


def bmi_calculator_page(request):
    """Render the BMI Calculator page"""
    return render(request, 'bmi-calculator.html')


def calorie_calculator_page(request):
    """Render the Calorie Calculator page"""
    return render(request, 'calorie-calculator.html')


def time_calculator_page(request):
    """Render the Time Calculator page"""
    return render(request, 'time-calculator.html')


def gpa_calculator_page(request):
    """Render the GPA Calculator page"""
    return render(request, 'gpa-calculator.html')


def unit_converter_page(request):
    """Render the Unit Converter page"""
    return render(request, 'unit-converter.html')


def discount_calculator_page(request):
    """Render the Discount Calculator page"""
    return render(request, 'discount-calculator.html')


def tip_calculator_page(request):
    """Render the Tip Calculator page"""
    return render(request, 'tip-calculator.html')


def currency_calculator_page(request):
    """Render the Currency Converter page"""
    return render(request, 'currency-calculator.html')


def concrete_calculator_page(request):
    """Render the Concrete Calculator page"""
    return render(request, 'concrete-calculator.html')


def graphing_calculator_page(request):
    """Render the Graphing Calculator page"""
    return render(request, 'graphing-calculator.html')


# ====================
# Legal Pages
# ====================

def terms_page(request):
    """Render the Terms of Service page"""
    return render(request, 'terms.html')


def code_of_conduct_page(request):
    """Render the Code of Conduct page"""
    return render(request, 'code-of-conduct.html')


# ====================
# Security Tools
# ====================

def password_generator_page(request):
    """Render the Password Generator page"""
    return render(request, 'password-generator.html')


def url_encoder_page(request):
    """Render the URL Encoder/Decoder page"""
    return render(request, 'url-encoder.html')


def typing_test_page(request):
    """Render the Typing Speed Test page"""
    return render(request, 'typing-test.html')


# ====================
# Careers Pages
# ====================

def careers_page(request):
    """List all active job postings"""
    from .models import JobPosting
    
    jobs = JobPosting.objects.filter(is_active=True)
    
    # Filter by department
    department = request.GET.get('department')
    if department:
        jobs = jobs.filter(department=department)
    
    # Filter by employment type
    employment_type = request.GET.get('type')
    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)
    
    # Get unique departments and employment types for filters
    departments = JobPosting.DEPARTMENT_CHOICES
    employment_types = JobPosting.EMPLOYMENT_TYPE_CHOICES
    
    context = {
        'jobs': jobs,
        'departments': departments,
        'employment_types': employment_types,
        'current_department': department,
        'current_type': employment_type,
        'total_jobs': jobs.count(),
    }
    
    return render(request, 'careers.html', context)


def job_detail(request, slug):
    """Display individual job posting and handle application submissions"""
    from .models import JobPosting, JobApplication
    from django.contrib import messages
    
    job = get_object_or_404(JobPosting, slug=slug, is_active=True)
    
    # Handle form submission
    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        cover_letter = request.POST.get('cover_letter', '').strip()
        resume_url = request.POST.get('resume_url', '').strip()
        portfolio_url = request.POST.get('portfolio_url', '').strip()
        linkedin_url = request.POST.get('linkedin_url', '').strip()
        years_of_experience = request.POST.get('years_of_experience', 0)
        current_company = request.POST.get('current_company', '').strip()
        current_role = request.POST.get('current_role', '').strip()
        
        # Validate required fields
        errors = []
        if not full_name:
            errors.append('Full name is required.')
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email:
            errors.append('Please enter a valid email address.')
        if not resume_url:
            errors.append('Resume/CV link is required.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Get client IP
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip_address = x_forwarded_for.split(',')[0].strip()
                else:
                    ip_address = request.META.get('REMOTE_ADDR')
                
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                
                # Parse years of experience
                try:
                    years_exp = int(years_of_experience)
                except (ValueError, TypeError):
                    years_exp = 0
                
                # Create application
                JobApplication.objects.create(
                    job=job,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    cover_letter=cover_letter,
                    resume_url=resume_url,
                    portfolio_url=portfolio_url,
                    linkedin_url=linkedin_url,
                    years_of_experience=years_exp,
                    current_company=current_company,
                    current_role=current_role,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                
                messages.success(request, 'Thank you for applying! We\'ve received your application and will get back to you soon.')
                
                # Redirect to prevent form resubmission
                from django.shortcuts import redirect
                return redirect('job_detail', slug=slug)
                
            except Exception as e:
                messages.error(request, f'An error occurred while submitting your application. Please try again.')
    
    # Get related jobs in same department
    related_jobs = JobPosting.objects.filter(
        is_active=True,
        department=job.department
    ).exclude(id=job.id)[:3]
    
    context = {
        'job': job,
        'related_jobs': related_jobs,
    }
    
    return render(request, 'job-detail.html', context)


# ====================
# Typing Test API
# ====================

@api_view(['POST'])
def submit_typing_score(request):
    """
    Submit a typing test score to the leaderboard.
    Enforces ONE entry per user per level (High Score logic).
    """
    from .models import TypingScore
    from django.utils import timezone
    
    try:
        username = request.data.get('username', 'Anonymous').strip()[:50]
        wpm = int(request.data.get('wpm', 0))
        accuracy = float(request.data.get('accuracy', 0))
        level = request.data.get('level', 'medium')
        duration = int(request.data.get('duration', 60))
        total_chars = int(request.data.get('total_characters', 0))
        correct_chars = int(request.data.get('correct_characters', 0))
        errors = int(request.data.get('errors', 0))
        
        # Basic validation
        if wpm < 0 or wpm > 3000: # Increased limit for testing, though 300 is realistic max
            return Response({'success': False, 'error': 'Invalid WPM'}, status=400)
        
        if accuracy < 0 or accuracy > 100:
            return Response({'success': False, 'error': 'Invalid accuracy'}, status=400)
        
        # Get session key for tracking (primary user ID mechanism usually, but we use username for 'Public' unique)
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        # Get IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        
        # Check for existing score for this User + Level
        existing_score = TypingScore.objects.filter(username=username, level=level).first()
        
        score_id = None
        is_new_high_score = False
        
        if existing_score:
            if wpm > existing_score.wpm:
                # NEW HIGH SCORE: Update existing record
                existing_score.wpm = wpm
                existing_score.accuracy = accuracy
                existing_score.duration = duration
                existing_score.total_characters = total_chars
                existing_score.correct_characters = correct_chars
                existing_score.errors = errors
                existing_score.ip_address = ip
                existing_score.session_key = session_key
                existing_score.created_at = timezone.now() # Manually update timestamp to now
                existing_score.save()
                
                score = existing_score
                is_new_high_score = True
                message = f'New High Score! You ranked #{TypingScore.get_rank(wpm, level)} in {level} mode.'
            else:
                # LOWER or EQUAL SCORE: Keep old record
                score = existing_score
                message = f'Score recorded, but your personal best of {existing_score.wpm} WPM remains!'
        else:
            # CREATE NEW RECORD
            score = TypingScore.objects.create(
                username=username or 'Anonymous',
                session_key=session_key,
                ip_address=ip,
                wpm=wpm,
                accuracy=accuracy,
                level=level,
                duration=duration,
                total_characters=total_chars,
                correct_characters=correct_chars,
                errors=errors
            )
            is_new_high_score = True
            message = f'Score saved! You ranked #{TypingScore.get_rank(wpm, level)} in {level} mode.'
        
        # Get ranks
        rank = TypingScore.get_rank(score.wpm, level)
        global_rank = TypingScore.get_rank(score.wpm)
        
        return Response({
            'success': True,
            'score_id': score.id,
            'rank': rank,
            'global_rank': global_rank,
            'message': message,
            'is_high_score': is_new_high_score
        })
        
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)


@api_view(['GET'])
def get_typing_leaderboard(request):
    """
    Get the global typing leaderboard with filters.
    Query params:
        - level: filter by difficulty level (easy, medium, hard, etc.)
        - period: 'all' (default), 'daily', 'weekly'
        - duration: filter by test duration in seconds (15, 30, 60, 120, etc.)
        - limit: max results per page (default 20, max 100)
        - page: page number for pagination (default 1)
    """
    from .models import TypingScore
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        level = request.GET.get('level', 'all')
        period = request.GET.get('period', 'all')
        duration = request.GET.get('duration', None)
        limit = min(int(request.GET.get('limit', 20)), 100)
        page = max(int(request.GET.get('page', 1)), 1)
        
        # Base query
        queryset = TypingScore.objects.filter(is_verified=True)
        
        # Filter by level/difficulty
        if level and level != 'all':
            queryset = queryset.filter(level=level)
        
        # Filter by time period
        now = timezone.now()
        if period == 'daily':
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = queryset.filter(created_at__gte=start_of_day)
        elif period == 'weekly':
            start_of_week = now - timedelta(days=now.weekday())
            start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
            queryset = queryset.filter(created_at__gte=start_of_week)
        
        # Filter by test duration
        if duration:
            try:
                duration_int = int(duration)
                queryset = queryset.filter(duration=duration_int)
            except ValueError:
                pass
        
        # Get total count before pagination
        total_count = queryset.count()
        total_pages = max(1, (total_count + limit - 1) // limit)
        
        # Order by WPM (descending), then accuracy (descending)
        queryset = queryset.order_by('-wpm', '-accuracy')
        
        # Pagination
        offset = (page - 1) * limit
        scores = queryset[offset:offset + limit]
        
        leaderboard = [{
            'rank': offset + i + 1,
            'username': score.username,
            'wpm': score.wpm,
            'accuracy': float(score.accuracy),
            'level': score.level,
            'duration': score.duration,
            'date': score.created_at.strftime('%Y-%m-%d')
        } for i, score in enumerate(scores)]
        
        # Get requester's best score if they have session
        session_key = request.session.session_key
        user_best = None
        user_rank = None
        
        if session_key:
            # Build filter for user's best in same conditions
            user_query = TypingScore.objects.filter(session_key=session_key, is_verified=True)
            if level and level != 'all':
                user_query = user_query.filter(level=level)
            if duration:
                try:
                    user_query = user_query.filter(duration=int(duration))
                except ValueError:
                    pass
            
            best_score = user_query.order_by('-wpm').first()
            if best_score:
                user_best = {
                    'wpm': best_score.wpm,
                    'accuracy': float(best_score.accuracy),
                    'level': best_score.level,
                    'duration': best_score.duration
                }
                # Calculate rank
                user_rank = queryset.filter(wpm__gt=best_score.wpm).count() + 1
        
        return Response({
            'success': True,
            'leaderboard': leaderboard,
            'user_best': user_best,
            'user_rank': user_rank,
            'total_scores': total_count,
            'page': page,
            'total_pages': total_pages,
            'limit': limit,
            'filters': {
                'level': level,
                'period': period,
                'duration': duration
            }
        })
        
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)


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
    Perform comprehensive DNS lookup for a domain.
    Returns A, AAAA, MX, TXT, NS, SOA, CNAME records with geolocation info.
    """
    import requests as http_requests
    import dns.resolver
    import dns.rdatatype
    
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
        
        # Create resolver with timeout
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 10
        
        # A records (IPv4)
        try:
            a_records = resolver.resolve(domain, 'A')
            result['records']['A'] = [str(rdata) for rdata in a_records]
        except:
            result['records']['A'] = []
        
        # AAAA records (IPv6)
        try:
            aaaa_records = resolver.resolve(domain, 'AAAA')
            result['records']['AAAA'] = [str(rdata) for rdata in aaaa_records]
        except:
            result['records']['AAAA'] = []
        
        # MX records (Mail servers)
        try:
            mx_records = resolver.resolve(domain, 'MX')
            result['records']['MX'] = [
                {'priority': rdata.preference, 'host': str(rdata.exchange).rstrip('.')}
                for rdata in mx_records
            ]
        except:
            result['records']['MX'] = []
        
        # TXT records
        try:
            txt_records = resolver.resolve(domain, 'TXT')
            result['records']['TXT'] = [str(rdata).strip('"') for rdata in txt_records]
        except:
            result['records']['TXT'] = []
        
        # NS records (Name servers)
        try:
            ns_records = resolver.resolve(domain, 'NS')
            result['records']['NS'] = [str(rdata).rstrip('.') for rdata in ns_records]
        except:
            result['records']['NS'] = []
        
        # SOA record (Start of Authority)
        try:
            soa_records = resolver.resolve(domain, 'SOA')
            for rdata in soa_records:
                result['records']['SOA'] = {
                    'mname': str(rdata.mname).rstrip('.'),
                    'rname': str(rdata.rname).rstrip('.'),
                    'serial': rdata.serial,
                    'refresh': rdata.refresh,
                    'retry': rdata.retry,
                    'expire': rdata.expire,
                    'minimum': rdata.minimum
                }
                break
        except:
            result['records']['SOA'] = None
        
        # CNAME record
        try:
            cname_records = resolver.resolve(domain, 'CNAME')
            result['records']['CNAME'] = [str(rdata.target).rstrip('.') for rdata in cname_records]
        except:
            result['records']['CNAME'] = []
        
        # PTR record (Reverse DNS for first A record)
        if result['records']['A']:
            try:
                first_ip = result['records']['A'][0]
                # Create reverse IP for PTR lookup
                parts = first_ip.split('.')
                reverse_ip = '.'.join(reversed(parts)) + '.in-addr.arpa'
                ptr_records = resolver.resolve(reverse_ip, 'PTR')
                result['records']['PTR'] = [str(rdata).rstrip('.') for rdata in ptr_records]
            except:
                result['records']['PTR'] = []
        else:
            result['records']['PTR'] = []
        
        # Get geolocation for each IP (limit to first 3)
        all_ips = result['records']['A'][:3]
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
                result['ipDetails'].append({
                    'ip': ip,
                    'error': 'Could not fetch location'
                })
        
        # Log the DNS lookup request
        from formatter.models import NetworkLookupLog
        try:
            NetworkLookupLog.log_dns_lookup(
                domain=domain,
                requester_ip=get_client_ip(request),
                response_data=result,
                success=True,
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        except:
            pass  # Don't fail the request if logging fails
        
        return Response(result)
        
    except Exception as e:
        # Log failed DNS lookup
        from formatter.models import NetworkLookupLog
        try:
            NetworkLookupLog.log_dns_lookup(
                domain=request.data.get('domain', ''),
                requester_ip=get_client_ip(request),
                success=False,
                error=str(e),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        except:
            pass
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


def toon_converter_page(request):
    """Render the JSON to TOON Converter tool page"""
    return render(request, 'toon-converter.html')


def domain_age_page(request):
    """Render the Domain Age Checker page"""
    return render(request, 'domain-age-checker.html')


def whois_lookup_page(request):
    """Render the WHOIS Lookup page"""
    return render(request, 'whois-lookup.html')


def domain_expiry_checker_page(request):
    """Render the Domain Expiry Checker page"""
    return render(request, 'domain-expiry-checker.html')


def whois_api_page(request):
    """Render the WHOIS API documentation page"""
    return render(request, 'whois-api.html')


def domain_age_result_page(request, domain):
    """
    Dynamic domain age result page for SEO.
    Uses cached WHOIS data for SSR (Answer-First) when available.
    New domains show loading spinner, subsequent visits have full SSR.
    Index/noindex controlled via ApprovedDomain model in admin.
    """
    from .models import ApprovedDomain, DomainPageVisit
    from datetime import datetime
    import json
    
    # Helper to format ISO date to "Month Day, Year"
    def format_date_human(iso_date_str):
        if not iso_date_str:
            return None
        try:
            # Handle both datetime and date-only strings
            date_str = iso_date_str[:10]  # YYYY-MM-DD
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime('%B %d, %Y')  # e.g., "August 08, 1996"
        except:
            return iso_date_str[:10]
    
    # Clean domain
    domain = domain.lower().strip()
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'^www\.', '', domain)
    domain = domain.split('/')[0]
    domain = domain.split('?')[0]
    
    # Validate domain format (basic check)
    if not domain or '.' not in domain or len(domain) < 4:
        from django.http import Http404
        raise Http404(f"Invalid domain: '{domain}'")
    
    # Get client IP for visit tracking
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0].strip()
    else:
        ip_address = request.META.get('REMOTE_ADDR', '')
    
    # Record visit
    visit_record = None
    try:
        visit_record = DomainPageVisit.record_visit(domain, ip_address)
        visit_count = visit_record.visit_count
        unique_visitors = visit_record.unique_visitors
    except:
        visit_count = 0
        unique_visitors = 0
    
    # ---------------------------------------------------------
    # Try to get cached WHOIS data for SSR (Answer-First)
    # ---------------------------------------------------------
    whois_data = None
    if visit_record and visit_record.last_cached_data:
        try:
            whois_data = json.loads(visit_record.last_cached_data)
            # Add human-readable date formats
            whois_data['createdDateHuman'] = format_date_human(whois_data.get('createdDate'))
            whois_data['updatedDateHuman'] = format_date_human(whois_data.get('updatedDate'))
            whois_data['expiryDateHuman'] = format_date_human(whois_data.get('expiryDate'))
        except json.JSONDecodeError:
            pass
    
    # Check if domain is approved and indexable
    try:
        approved = ApprovedDomain.objects.get(domain=domain)
        is_indexable = approved.is_indexable
        custom_title = approved.meta_title
        custom_description = approved.meta_description
    except ApprovedDomain.DoesNotExist:
        # Auto-index if we have cached data, otherwise noindex
        is_indexable = True if whois_data else False
        custom_title = ''
        custom_description = ''
    
    # Check if admin values use old format (should be regenerated)
    old_format_markers = [
        "Domain Registration Date & Age |",
        "Domain Age Checker",
        "Check ",
        "using our free",
    ]
    
    # Force regeneration if old format detected
    if custom_title and any(marker in custom_title for marker in old_format_markers):
        custom_title = ''
    if custom_description and any(marker in custom_description for marker in old_format_markers):
        custom_description = ''
    
    # Generate SEO-optimized title (always use new format unless admin has custom non-default value)
    if custom_title:
        meta_title = custom_title
    else:
        meta_title = f"{domain} domain Registration Date (WHOIS) – Exact Age"
    
    # Generate SEO-optimized description with real data
    if custom_description:
        meta_description = custom_description
    else:
        if whois_data and whois_data.get('createdDateHuman'):
            age_years = whois_data.get('age', {}).get('years', 0)
            meta_description = f"{domain} was registered on {whois_data['createdDateHuman']} and is {age_years} years old. View official WHOIS registration details, registrar, and expiry date."
        else:
            meta_description = f"{domain} domain registration date and age verified from official WHOIS records maintained by ICANN-accredited registries."
    
    # Last updated timestamp for freshness signals
    try:
        if visit_record and visit_record.cache_updated_at:
            last_updated = visit_record.cache_updated_at
        else:
            last_updated = datetime.now()
    except:
        last_updated = datetime.now()
    
    context = {
        'domain': domain,
        'is_indexable': is_indexable,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'visit_count': visit_count,
        'unique_visitors': unique_visitors,
        'last_updated': last_updated,
        'whois_data': whois_data,  # None if no cache, dict if cached
    }
    
    return render(request, 'domain-age-result.html', context)


@api_view(['POST'])
def domain_age_api(request):
    """
    Check domain age and WHOIS information.
    Returns registration dates, registrar, nameservers, and calculated age.
    Results are cached for 24 hours for performance.
    """
    try:
        import whois
        from datetime import datetime
        from django.core.cache import cache
        import json
        
        domain = request.data.get('domain', '').strip()
        
        if not domain:
            return Response({'error': 'Domain is required'}, status=400)
        
        # Clean domain (remove protocol and path)
        domain = re.sub(r'^https?://', '', domain)
        domain = re.sub(r'^www\.', '', domain)
        domain = domain.split('/')[0]
        domain = domain.split('?')[0]
        domain = domain.lower()
        
        # Check cache first (24 hour cache)
        cache_key = f"whois_data_{domain}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)
        
        try:
            w = whois.whois(domain)
        except Exception as e:
            return Response({'error': f'Unable to fetch WHOIS data: {str(e)}'}, status=400)
        
        if not w or not w.domain_name:
            return Response({'error': 'Domain not found or WHOIS data unavailable'}, status=404)
        
        # Handle dates that might be lists
        def get_first_date(date_value):
            if isinstance(date_value, list):
                return date_value[0] if date_value else None
            return date_value
        
        created_date = get_first_date(w.creation_date)
        updated_date = get_first_date(w.updated_date)
        expiry_date = get_first_date(w.expiration_date)
        
        # Calculate age
        age = {'years': 0, 'months': 0, 'days': 0}
        if created_date:
            now = datetime.now()
            if hasattr(created_date, 'tzinfo') and created_date.tzinfo:
                created_date = created_date.replace(tzinfo=None)
            
            delta = now - created_date
            total_days = delta.days
            
            age['years'] = total_days // 365
            remaining_days = total_days % 365
            age['months'] = remaining_days // 30
            age['days'] = remaining_days % 30
        
        # Calculate days until expiry
        days_until_expiry = None
        if expiry_date:
            if hasattr(expiry_date, 'tzinfo') and expiry_date.tzinfo:
                expiry_date_clean = expiry_date.replace(tzinfo=None)
            else:
                expiry_date_clean = expiry_date
            days_until_expiry = (expiry_date_clean - datetime.now()).days
        
        # Handle registrar (might be a list)
        registrar = w.registrar
        if isinstance(registrar, list):
            registrar = registrar[0] if registrar else None
        
        # Handle nameservers
        name_servers = w.name_servers
        if name_servers:
            if isinstance(name_servers, str):
                name_servers = [name_servers]
            name_servers = list(set([ns.lower() for ns in name_servers if ns]))
        else:
            name_servers = []
        
        # Handle status
        status = w.status
        if status:
            if isinstance(status, str):
                status = [status]
        else:
            status = []
        
        # Handle DNSSEC
        dnssec = getattr(w, 'dnssec', None)
        if dnssec:
            if isinstance(dnssec, list):
                dnssec = dnssec[0] if dnssec else 'Unsigned'
        else:
            dnssec = 'Unsigned'
        
        result = {
            'domain': domain,
            'createdDate': created_date.isoformat() if created_date else None,
            'updatedDate': updated_date.isoformat() if updated_date else None,
            'expiryDate': expiry_date.isoformat() if expiry_date else None,
            'age': age,
            'daysUntilExpiry': days_until_expiry,
            'registrar': registrar,
            'nameServers': name_servers,
            'status': status,
            'dnssec': dnssec,
        }
        
        # Cache for 24 hours (86400 seconds)
        cache.set(cache_key, result, 86400)
        
        # Also store in database for persistence
        try:
            from .models import DomainPageVisit
            visit_record, _ = DomainPageVisit.objects.get_or_create(domain=domain)
            visit_record.last_cached_data = json.dumps(result)
            visit_record.cache_updated_at = datetime.now()
            visit_record.save(update_fields=['last_cached_data', 'cache_updated_at'])
        except:
            pass  # Don't fail request if caching fails
        
        # Auto-create ApprovedDomain for indexing (only if WHOIS lookup was successful)
        try:
            from .models import ApprovedDomain
            
            # Format date for meta description
            reg_date_human = None
            if created_date:
                reg_date_human = created_date.strftime('%B %d, %Y')  # e.g., "August 08, 1996"
            
            age_years = age.get('years', 0)
            
            # Generate meta fields with real data
            if reg_date_human:
                auto_title = f"{domain} domain Registration Date (WHOIS) – Exact Age"
                auto_description = f"{domain} was registered on {reg_date_human} and is {age_years} years old. View official WHOIS registration details, registrar, and expiry date."
            else:
                auto_title = f"{domain} domain Registration Date (WHOIS) – Exact Age"
                auto_description = f"{domain} domain registration date and age verified from official WHOIS records maintained by ICANN-accredited registries."
            
            approved, created = ApprovedDomain.objects.get_or_create(
                domain=domain,
                defaults={
                    "is_indexable": True,
                    "meta_title": auto_title,
                    "meta_description": auto_description,
                    "notes": "Auto-approved: capturing domain registration date searches."
                }
            )
        except:
            pass  # Don't fail request if approval fails
        
        return Response(result)
        
    except ImportError:
        return Response({'error': 'WHOIS library not installed. Please install python-whois.'}, status=500)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def top_domains_api(request):
    """
    Get top visited domain age pages.
    Used to display popular domains slider on main page.
    """
    try:
        from .models import DomainPageVisit
        import json
        
        limit = int(request.GET.get('limit', 10))
        limit = min(limit, 50)  # Cap at 50
        
        top_domains = DomainPageVisit.objects.order_by('-visit_count')[:limit]
        
        results = []
        for visit in top_domains:
            data = {
                'domain': visit.domain,
                'visitCount': visit.visit_count,
                'uniqueVisitors': visit.unique_visitors,
            }
            
            # Include cached WHOIS data if available
            if visit.last_cached_data:
                try:
                    cached = json.loads(visit.last_cached_data)
                    data['age'] = cached.get('age')
                    data['registrar'] = cached.get('registrar')
                except:
                    pass
            
            results.append(data)
        
        return Response({
            'success': True,
            'domains': results,
            'total': len(results)
        })
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)


# ====================
# Tutorial Views
# ====================

from .models import ProgrammingLanguage, TutorialCategory, Tutorial


def tutorials_list(request):
    """List all tutorials grouped by category with language selection"""
    # Get all active languages
    languages = ProgrammingLanguage.objects.filter(is_active=True)
    
    # Get selected language from query param or default to first
    selected_lang_slug = request.GET.get('lang')
    selected_language = None
    if selected_lang_slug:
        selected_language = languages.filter(slug=selected_lang_slug).first()
    if not selected_language and languages.exists():
        selected_language = languages.first()
    
    # Get all categories with their published tutorials
    categories = TutorialCategory.objects.prefetch_related(
        'tutorials'
    ).filter(
        tutorials__is_published=True
    ).distinct().order_by('order')
    
    context = {
        'languages': languages,
        'selected_language': selected_language,
        'categories': categories,
    }
    
    return render(request, 'tutorials-list.html', context)


def tutorial_detail(request, slug):
    """Display a single tutorial with code examples and MCQs"""
    tutorial = get_object_or_404(Tutorial, slug=slug, is_published=True)
    
    # Get all active languages
    languages = ProgrammingLanguage.objects.filter(is_active=True)
    
    # Get selected language from query param or default to first
    selected_lang_slug = request.GET.get('lang')
    selected_language = None
    if selected_lang_slug:
        selected_language = languages.filter(slug=selected_lang_slug).first()
    if not selected_language and languages.exists():
        selected_language = languages.first()
    
    # Get all code examples for this tutorial (show all, don't filter by language)
    code_examples = tutorial.code_examples.all().order_by('order')
    
    # Get MCQ questions with their options
    mcq_questions = tutorial.mcq_questions.prefetch_related('options').order_by('order')
    
    # Get all tutorials in the same category for sidebar navigation
    category_tutorials = Tutorial.objects.filter(
        category=tutorial.category,
        is_published=True
    ).order_by('order')
    
    # Increment views
    tutorial.increment_views()
    
    # Get next and previous tutorials
    next_tutorial = tutorial.get_next_tutorial()
    prev_tutorial = tutorial.get_previous_tutorial()
    
    context = {
        'tutorial': tutorial,
        'languages': languages,
        'selected_language': selected_language,
        'code_examples': code_examples,
        'mcq_questions': mcq_questions,
        'category_tutorials': category_tutorials,
        'next_tutorial': next_tutorial,
        'prev_tutorial': prev_tutorial,
    }
    
    return render(request, 'tutorial-detail.html', context)


# ====================
# Mock API Endpoints
# ====================

import time
import random
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import MockEndpoint


def get_client_ip(request):
    """Get the real client IP from request headers"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = (
            request.META.get('HTTP_X_REAL_IP') or
            request.META.get('HTTP_CF_CONNECTING_IP') or
            request.META.get('REMOTE_ADDR')
        )
    return ip


@csrf_exempt
@require_http_methods(["GET"])
def get_client_ip_api(request):
    """Return the client's public IP address"""
    client_ip = get_client_ip(request)
    return JsonResponse({
        'success': True,
        'ip': client_ip,
        'message': 'Your public IP address'
    })


@csrf_exempt
@require_http_methods(["GET"])
def ip_lookup_api(request):
    """
    Lookup IP address geolocation details.
    Server-side proxy to ip-api.com to avoid CSP issues.
    
    Query params:
        ip: IP address to lookup (optional, defaults to client IP)
    """
    import requests
    
    # Get IP to lookup - either from query param or client IP
    ip_to_lookup = request.GET.get('ip', '').strip()
    if not ip_to_lookup:
        ip_to_lookup = get_client_ip(request)
    
    # Validate IP format (basic check)
    if not ip_to_lookup:
        return JsonResponse({
            'success': False,
            'error': 'No IP address provided'
        }, status=400)
    
    try:
        # Call ip-api.com from server side
        response = requests.get(
            f'http://ip-api.com/json/{ip_to_lookup}',
            params={
                'fields': 'status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query'
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'success':
                result = {
                    'success': True,
                    'ip': data.get('query'),
                    'country': data.get('country'),
                    'countryCode': data.get('countryCode'),
                    'region': data.get('region'),
                    'regionName': data.get('regionName'),
                    'city': data.get('city'),
                    'zip': data.get('zip'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('isp'),
                    'org': data.get('org'),
                    'as': data.get('as')
                }
                
                # Log the IP lookup
                from formatter.models import NetworkLookupLog
                try:
                    NetworkLookupLog.log_ip_lookup(
                        ip_address=ip_to_lookup,
                        requester_ip=get_client_ip(request),
                        response_data=result,
                        success=True,
                        user_agent=request.META.get('HTTP_USER_AGENT')
                    )
                except:
                    pass
                
                return JsonResponse(result)
            else:
                return JsonResponse({
                    'success': False,
                    'error': data.get('message', 'Lookup failed')
                }, status=400)
        else:
            return JsonResponse({
                'success': False,
                'error': 'External API unavailable'
            }, status=502)
            
    except requests.Timeout:
        return JsonResponse({
            'success': False,
            'error': 'Request timed out'
        }, status=504)
    except Exception as e:
        # Log failed IP lookup
        from formatter.models import NetworkLookupLog
        try:
            NetworkLookupLog.log_ip_lookup(
                ip_address=ip_to_lookup,
                requester_ip=get_client_ip(request),
                success=False,
                error=str(e),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        except:
            pass
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_mock_endpoint(request):
    """
    Create a new mock API endpoint.
    
    Expected JSON body:
    {
        "path": "/api/users",
        "method": "GET",
        "status_code": 200,
        "response_body": "{...}",
        "latency_ms": 0,
        "error_rate": 0,
        "ip_restriction_enabled": false,
        "allowed_ips": "1.2.3.4,5.6.7.8",
        "name": "My Endpoint",
        "custom_headers": {}
    }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON in request body'
        }, status=400)
    
    # Validate required fields
    response_body = data.get('response_body', '')
    if not response_body:
        return JsonResponse({
            'success': False,
            'error': 'response_body is required'
        }, status=400)
    
    # Check endpoint limit (5 per IP)
    client_ip = get_client_ip(request)
    existing_count = MockEndpoint.objects.filter(creator_ip=client_ip).count()
    if existing_count >= 5:
        return JsonResponse({
            'success': False,
            'error': 'You have reached the maximum limit of 5 endpoints. Please delete an existing endpoint to create a new one.',
            'limit': 5,
            'current_count': existing_count
        }, status=400)
    
    # Create the endpoint (endpoint_id is always auto-generated)
    try:
        user_path = data.get('path', '/api/users').strip()
        # Ensure path doesn't start/end with slash for consistent URL building
        user_path = user_path.strip('/')
        
        endpoint = MockEndpoint.objects.create(
            name=data.get('name', ''),
            path=user_path,  # Store the normalized user path
            method=data.get('method', 'GET').upper(),
            status_code=int(data.get('status_code', 200)),
            response_body=response_body,
            latency_ms=int(data.get('latency_ms', 0)),
            error_rate=int(data.get('error_rate', 0)),
            record_count=int(data.get('record_count', 1)),
            ip_restriction_enabled=bool(data.get('ip_restriction_enabled', False)),
            allowed_ips=data.get('allowed_ips', ''),
            custom_headers=json.dumps(data.get('custom_headers', {})),
            creator_ip=client_ip
        )
        
        # Build the full endpoint URL using user's path
        site_url = request.build_absolute_uri('/').rstrip('/')
        endpoint_url = f"{site_url}/{user_path}/{endpoint.endpoint_id}/"
        
        return JsonResponse({
            'success': True,
            'endpoint_id': endpoint.endpoint_id,
            'endpoint_url': endpoint_url,
            'method': endpoint.method,
            'path': f"/{user_path}",
            'ip_restriction_enabled': endpoint.ip_restriction_enabled,
            'allowed_ips': endpoint.get_allowed_ips_list(),
            'created_at': endpoint.created_at.isoformat(),
            'message': 'Mock endpoint created successfully'
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def process_template_variables(template_str):
    """Process template variables like {{uuid}}, {{firstName}}, etc."""
    import secrets
    import string
    from datetime import datetime, timedelta
    
    # Fake data
    first_names = ['James', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason', 'Isabella']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    companies = ['TechCorp', 'Innovate Inc', 'Digital Dynamics', 'CloudFirst', 'DataDriven', 'NetSolutions']
    job_titles = ['Software Engineer', 'Product Manager', 'UX Designer', 'Data Scientist', 'DevOps Engineer']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'San Francisco', 'Seattle']
    countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Australia', 'Japan']
    streets = ['Main St', 'Oak Ave', 'Park Blvd', 'Maple Dr', 'Cedar Ln', 'Elm St', 'Pine Rd']
    words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliqua']
    
    def gen_uuid():
        return str(secrets.token_hex(4)) + '-' + str(secrets.token_hex(2)) + '-4' + str(secrets.token_hex(1))[1:] + '-' + str(secrets.token_hex(2)) + '-' + str(secrets.token_hex(6))
    
    def gen_email():
        fn = random.choice(first_names).lower()
        ln = random.choice(last_names).lower()
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com']
        return f"{fn}.{ln}@{random.choice(domains)}"
    
    def gen_phone():
        return f"+1 {random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"
    
    def gen_username():
        fn = random.choice(first_names).lower()
        return f"{fn}{random.randint(10,999)}"
    
    def gen_slug():
        return '-'.join(random.choices(words, k=random.randint(2,4)))
    
    def gen_paragraph():
        sentences = random.randint(3, 6)
        result = []
        for _ in range(sentences):
            sentence_words = random.randint(8, 15)
            sentence = ' '.join(random.choices(words, k=sentence_words))
            result.append(sentence.capitalize() + '.')
        return ' '.join(result)
    
    def gen_sentence():
        sentence_words = random.randint(8, 15)
        sentence = ' '.join(random.choices(words, k=sentence_words))
        return sentence.capitalize() + '.'
    
    def gen_url():
        paths = ['products', 'users', 'posts', 'articles', 'pages', 'items']
        return f"https://example.com/{random.choice(paths)}/{random.randint(1,9999)}"
    
    def gen_color():
        return f"#{secrets.token_hex(3)}"
    
    def gen_credit_card():
        return f"4{random.randint(100,999)} {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"
    
    def gen_price():
        return f"{random.randint(1, 999)}.{random.randint(0,99):02d}"
    
    def gen_ip():
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
    
    def gen_mac():
        return ':'.join([secrets.token_hex(1) for _ in range(6)])
    
    result = template_str
    result = re.sub(r'\{\{uuid\}\}', lambda m: gen_uuid(), result)
    result = re.sub(r'\{\{id\}\}', lambda m: str(random.randint(1, 99999)), result)
    result = re.sub(r'\{\{firstName\}\}', lambda m: random.choice(first_names), result)
    result = re.sub(r'\{\{lastName\}\}', lambda m: random.choice(last_names), result)
    result = re.sub(r'\{\{fullName\}\}', lambda m: f"{random.choice(first_names)} {random.choice(last_names)}", result)
    result = re.sub(r'\{\{username\}\}', lambda m: gen_username(), result)
    result = re.sub(r'\{\{email\}\}', lambda m: gen_email(), result)
    result = re.sub(r'\{\{phone\}\}', lambda m: gen_phone(), result)
    result = re.sub(r'\{\{company\}\}', lambda m: random.choice(companies), result)
    result = re.sub(r'\{\{jobTitle\}\}', lambda m: random.choice(job_titles), result)
    result = re.sub(r'\{\{street\}\}', lambda m: f"{random.randint(100,9999)} {random.choice(streets)}", result)
    result = re.sub(r'\{\{city\}\}', lambda m: random.choice(cities), result)
    result = re.sub(r'\{\{country\}\}', lambda m: random.choice(countries), result)
    result = re.sub(r'\{\{isoDate\}\}', lambda m: (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(), result)
    result = re.sub(r'\{\{date\}\}', lambda m: (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'), result)
    result = re.sub(r'\{\{datetime\}\}', lambda m: (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S'), result)
    result = re.sub(r'\{\{time\}\}', lambda m: f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}", result)
    result = re.sub(r'\{\{boolean\}\}', lambda m: str(random.choice([True, False])).lower(), result)
    # Number with range: {{number:min,max}}
    result = re.sub(r'\{\{number:(\d+),(\d+)\}\}', lambda m: str(random.randint(int(m.group(1)), int(m.group(2)))), result)
    # Number with max only: {{number:max}}
    result = re.sub(r'\{\{number:(\d+)\}\}', lambda m: str(random.randint(0, int(m.group(1)))), result)
    # Float with range: {{float:min,max}}
    result = re.sub(r'\{\{float:(\d+),(\d+)\}\}', lambda m: f"{random.uniform(float(m.group(1)), float(m.group(2))):.2f}", result)
    # Percentage
    result = re.sub(r'\{\{percentage\}\}', lambda m: str(random.randint(0, 100)), result)
    # OneOf choice: {{oneOf:option1,option2,option3}}
    result = re.sub(r'\{\{oneOf:([^}]+)\}\}', lambda m: random.choice(m.group(1).split(',')), result)
    result = re.sub(r'\{\{avatar\}\}', lambda m: f"https://i.pravatar.cc/150?img={random.randint(1,70)}", result)
    result = re.sub(r'\{\{imageUrl\}\}', lambda m: f"https://picsum.photos/seed/{random.randint(1,1000)}/400/300", result)
    result = re.sub(r'\{\{zipCode\}\}', lambda m: str(random.randint(10000, 99999)), result)
    result = re.sub(r'\{\{url\}\}', lambda m: gen_url(), result)
    result = re.sub(r'\{\{slug\}\}', lambda m: gen_slug(), result)
    result = re.sub(r'\{\{paragraph\}\}', lambda m: gen_paragraph(), result)
    result = re.sub(r'\{\{sentence\}\}', lambda m: gen_sentence(), result)
    result = re.sub(r'\{\{color\}\}', lambda m: gen_color(), result)
    result = re.sub(r'\{\{hexColor\}\}', lambda m: gen_color(), result)
    result = re.sub(r'\{\{creditCard\}\}', lambda m: gen_credit_card(), result)
    result = re.sub(r'\{\{price\}\}', lambda m: gen_price(), result)
    result = re.sub(r'\{\{ipAddress\}\}', lambda m: gen_ip(), result)
    result = re.sub(r'\{\{macAddress\}\}', lambda m: gen_mac(), result)
    # Lorem with word count: {{lorem:N}}
    result = re.sub(r'\{\{lorem:(\d+)\}\}', lambda m: ' '.join(random.choices(words, k=int(m.group(1)))), result)
    
    return result


@csrf_exempt
def serve_path_mock_endpoint(request, user_path='', endpoint_id=''):
    """
    Serve mock endpoint via path-based URL: /{user_path}/{endpoint_id}/
    Examples: /api/users/abc123/, /api/employees/xyz789/
    The endpoint_id is extracted from the URL path.
    """
    if not endpoint_id:
        return JsonResponse({
            'error': 'Missing endpoint_id in URL path',
            'message': 'URL format should be /{path}/{endpoint_id}/',
            'user_path': user_path
        }, status=400)
    
    # Convert UUID object to string for database query
    endpoint_id_str = str(endpoint_id)
    
    # Validate that the path matches the endpoint's stored path (optional check)
    try:
        endpoint = MockEndpoint.objects.get(endpoint_id=endpoint_id_str)
        # Path validation is optional - we allow any path for flexibility
    except MockEndpoint.DoesNotExist:
        return JsonResponse({
            'error': 'Endpoint not found',
            'endpoint_id': endpoint_id_str,
            'path': user_path
        }, status=404)
    
    # Delegate to the main serve_mock_endpoint function
    return serve_mock_endpoint(request, endpoint_id_str, subpath='')


@csrf_exempt
def serve_mock_endpoint(request, endpoint_id, subpath=''):
    """
    Serve the mock endpoint response.
    Handles IP restriction, latency simulation, and error rate.
    """
    # Convert UUID object to string if needed
    endpoint_id_str = str(endpoint_id)
    
    try:
        endpoint = MockEndpoint.objects.get(endpoint_id=endpoint_id_str)
    except MockEndpoint.DoesNotExist:
        return JsonResponse({
            'error': 'Not Found',
            'message': 'Mock endpoint does not exist or has been deleted',
            'status': 404
        }, status=404)
    
    # Check if expired
    if endpoint.is_expired():
        return JsonResponse({
            'error': 'Gone',
            'message': 'This mock endpoint has expired',
            'status': 410
        }, status=410)
    
    # Check IP restriction
    client_ip = get_client_ip(request)
    if not endpoint.is_ip_allowed(client_ip):
        return JsonResponse({
            'error': 'Forbidden',
            'message': 'Your IP address is not authorized to access this endpoint',
            'your_ip': client_ip,
            'allowed_ips': endpoint.get_allowed_ips_list(),
            'status': 403
        }, status=403)
    
    # Check method
    if request.method != endpoint.method:
        return JsonResponse({
            'error': 'Method Not Allowed',
            'message': f'This endpoint only accepts {endpoint.method} requests',
            'status': 405
        }, status=405)
    
    # Apply latency simulation
    if endpoint.latency_ms > 0:
        time.sleep(endpoint.latency_ms / 1000.0)
    
    # Check error rate simulation
    if endpoint.error_rate > 0 and random.randint(1, 100) <= endpoint.error_rate:
        return JsonResponse({
            'error': 'Internal Server Error',
            'message': 'Simulated server error (based on configured error rate)',
            'status': 500
        }, status=500)
    
    # Increment request count
    endpoint.increment_request_count()
    
    # Process template variables and generate N records
    try:
        record_count = max(1, endpoint.record_count)
        response_template = endpoint.response_body
        
        # Try to detect if we have a data array structure
        has_data_array = '"data"' in response_template and '[' in response_template
        
        if has_data_array:
            try:
                # Step 1: Replace template vars with placeholders to make parseable JSON
                import re
                # Find all template patterns like {{varName}} or {{varName:param}}
                template_vars = re.findall(r'\{\{[^}]+\}\}', response_template)
                temp_template = response_template
                var_map = {}
                for i, var in enumerate(template_vars):
                    placeholder = f'"__PLACEHOLDER_{i}__"'
                    var_map[placeholder] = var
                    # Replace only in non-string contexts or as string values
                    temp_template = temp_template.replace(f'"{var}"', placeholder)
                    temp_template = temp_template.replace(var, f'"__PLACEHOLDER_{i}__"')
                
                # Parse the JSON with placeholders
                parsed = json.loads(temp_template)
                
                if 'data' in parsed and isinstance(parsed['data'], list) and len(parsed['data']) > 0:
                    # Get the first item as our template - but use the ORIGINAL string template, not parsed
                    # Extract the original item template string from response_template
                    data_idx = response_template.find('"data"')
                    bracket_start = response_template.find('[', data_idx)
                    obj_start = response_template.find('{', bracket_start)
                    
                    # Find matching closing brace
                    brace_count = 1
                    pos = obj_start + 1
                    while pos < len(response_template) and brace_count > 0:
                        if response_template[pos] == '{':
                            brace_count += 1
                        elif response_template[pos] == '}':
                            brace_count -= 1
                        pos += 1
                    
                    original_item_template = response_template[obj_start:pos]
                    array_end = response_template.find(']', pos)
                    
                    # Generate N records - each with fresh random values
                    generated_items = []
                    for _ in range(record_count):
                        # Process template variables fresh for each item
                        processed_item = process_template_variables(original_item_template)
                        generated_items.append(json.loads(processed_item))
                    
                    # Build the complete response
                    before_data = response_template[:bracket_start + 1]
                    after_data = response_template[array_end:]
                    items_json = ',\n'.join(json.dumps(item) for item in generated_items)
                    processed_body = before_data + items_json + after_data
                    
                    # Process remaining template vars (like in meta)
                    processed_body = process_template_variables(processed_body)
                    response_data = json.loads(processed_body)
                else:
                    # No data array found, process normally
                    processed_body = process_template_variables(response_template)
                    response_data = json.loads(processed_body)
                    
            except Exception as e:
                # Fallback: Try a simpler approach that still generates multiple records
                import re
                try:
                    # Find the data array start position
                    data_start = response_template.find('"data"')
                    if data_start != -1:
                        # Find the opening bracket of the array
                        bracket_start = response_template.find('[', data_start)
                        if bracket_start != -1:
                            # Find the first object's opening brace
                            obj_start = response_template.find('{', bracket_start)
                            if obj_start != -1:
                                # Find the matching closing brace (handle nested braces)
                                brace_count = 1
                                pos = obj_start + 1
                                while pos < len(response_template) and brace_count > 0:
                                    if response_template[pos] == '{':
                                        brace_count += 1
                                    elif response_template[pos] == '}':
                                        brace_count -= 1
                                    pos += 1
                                obj_end = pos
                                
                                # Extract the item template
                                item_template = response_template[obj_start:obj_end]
                                
                                # Find where the data array ends
                                array_end = response_template.find(']', obj_end)
                                
                                # Generate multiple items with fresh random values each time
                                items = []
                                for _ in range(record_count):
                                    processed_item = process_template_variables(item_template)
                                    items.append(processed_item)
                                
                                # Build the new response
                                items_json = ',\n'.join(items)
                                before_data = response_template[:bracket_start + 1]
                                after_data = response_template[array_end:]
                                processed_body = before_data + items_json + after_data
                                
                                # Process any remaining template vars (like in meta section)
                                processed_body = process_template_variables(processed_body)
                                response_data = json.loads(processed_body)
                            else:
                                raise ValueError("No object found in data array")
                        else:
                            raise ValueError("No data array bracket found")
                    else:
                        # No data array, just process normally
                        processed_body = process_template_variables(response_template)
                        response_data = json.loads(processed_body)
                except Exception as e2:
                    # Final fallback
                    processed_body = process_template_variables(response_template)
                    try:
                        response_data = json.loads(processed_body)
                    except:
                        response_data = {'raw_response': processed_body, 'error': str(e)}
        else:
            # No data array structure, simple processing
            processed_body = process_template_variables(response_template)
            response_data = json.loads(processed_body)
            
    except json.JSONDecodeError:
        # Return as plain text if not valid JSON
        response_data = {'raw_response': process_template_variables(endpoint.response_body)}
    
    # Handle query parameter filtering (e.g., ?id=123, ?email=test@example.com)
    query_params = request.GET
    if query_params and isinstance(response_data, dict) and 'data' in response_data and isinstance(response_data['data'], list):
        # Check for id param first (most common use case)
        param_id = query_params.get('id')
        if param_id:
            # Find matching record by id field
            matching = None
            for item in response_data['data']:
                if isinstance(item, dict):
                    # Check various id field names
                    item_id = item.get('id') or item.get('_id') or item.get('uuid') or item.get('ID')
                    if str(item_id) == str(param_id):
                        matching = item
                        break
            
            if matching:
                response_data = {'success': True, 'data': matching}
            else:
                # Generate a new record with the specified ID
                if response_data['data']:
                    matching = response_data['data'][0].copy() if isinstance(response_data['data'][0], dict) else {}
                    matching['id'] = param_id
                    response_data = {'success': True, 'data': matching}
                else:
                    response_data = {'success': False, 'error': 'Record not found', 'id': param_id}
        else:
            # Check for other filter params
            for key, value in query_params.items():
                if key not in ['format', 'callback', '_']:  # Ignore common non-filter params
                    filtered = [item for item in response_data['data'] 
                               if isinstance(item, dict) and str(item.get(key, '')).lower() == str(value).lower()]
                    if filtered:
                        response_data['data'] = filtered
                        response_data['filtered_by'] = {key: value}
                        break
    
    response = JsonResponse(response_data, status=endpoint.status_code, safe=False)
    
    # Add custom headers
    try:
        custom_headers = json.loads(endpoint.custom_headers)
        for key, value in custom_headers.items():
            response[key] = value
    except:
        pass
    
    # Add CORS headers for accessibility
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    return response


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def delete_mock_endpoint(request, endpoint_id):
    """Delete a mock endpoint (only by creator IP)"""
    endpoint_id_str = str(endpoint_id)
    try:
        endpoint = MockEndpoint.objects.get(endpoint_id=endpoint_id_str)
    except MockEndpoint.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Endpoint not found'
        }, status=404)
    
    # Only allow deletion by creator IP
    client_ip = get_client_ip(request)
    if endpoint.creator_ip and endpoint.creator_ip != client_ip:
        return JsonResponse({
            'success': False,
            'error': 'You can only delete endpoints you created'
        }, status=403)
    
    endpoint.delete()
    return JsonResponse({
        'success': True,
        'message': 'Endpoint deleted successfully'
    })


@csrf_exempt
@require_http_methods(["POST", "PUT", "PATCH"])
def update_mock_endpoint(request, endpoint_id):
    """Update an existing mock endpoint (only by creator IP)"""
    endpoint_id_str = str(endpoint_id)
    try:
        endpoint = MockEndpoint.objects.get(endpoint_id=endpoint_id_str)
    except MockEndpoint.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Endpoint not found'
        }, status=404)
    
    # Only allow update by creator IP
    client_ip = get_client_ip(request)
    if endpoint.creator_ip and endpoint.creator_ip != client_ip:
        return JsonResponse({
            'success': False,
            'error': 'You can only edit endpoints you created'
        }, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON in request body'
        }, status=400)
    
    # Update allowed fields
    if 'name' in data:
        endpoint.name = data['name']
    if 'allowed_ips' in data:
        endpoint.allowed_ips = data['allowed_ips']
    if 'ip_restriction_enabled' in data:
        endpoint.ip_restriction_enabled = bool(data['ip_restriction_enabled'])
    if 'record_count' in data:
        endpoint.record_count = int(data['record_count'])
    if 'response_body' in data and data['response_body'].strip():
        endpoint.response_body = data['response_body']
    
    endpoint.save()
    
    site_url = request.build_absolute_uri('/').rstrip('/')
    
    return JsonResponse({
        'success': True,
        'endpoint_id': endpoint.endpoint_id,
        'endpoint_url': f"{site_url}/api/mock/{endpoint.endpoint_id}/",
        'name': endpoint.name,
        'ip_restriction_enabled': endpoint.ip_restriction_enabled,
        'allowed_ips': endpoint.get_allowed_ips_list(),
        'record_count': endpoint.record_count,
        'message': 'Endpoint updated successfully'
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_mock_endpoint_info(request, endpoint_id):
    """Get information about a mock endpoint"""
    endpoint_id_str = str(endpoint_id)
    try:
        endpoint = MockEndpoint.objects.get(endpoint_id=endpoint_id_str)
    except MockEndpoint.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Endpoint not found'
        }, status=404)
    
    site_url = request.build_absolute_uri('/').rstrip('/')
    
    return JsonResponse({
        'success': True,
        'endpoint_id': endpoint.endpoint_id,
        'endpoint_url': f"{site_url}/api/mock/{endpoint.endpoint_id}/",
        'name': endpoint.name,
        'path': endpoint.path,
        'method': endpoint.method,
        'status_code': endpoint.status_code,
        'latency_ms': endpoint.latency_ms,
        'error_rate': endpoint.error_rate,
        'ip_restriction_enabled': endpoint.ip_restriction_enabled,
        'request_count': endpoint.request_count,
        'created_at': endpoint.created_at.isoformat(),
        'last_accessed': endpoint.last_accessed.isoformat() if endpoint.last_accessed else None,
        'is_expired': endpoint.is_expired()
    })


@csrf_exempt
@require_http_methods(["GET"])
def list_my_endpoints(request):
    """List all mock endpoints created by the current user (based on IP)"""
    client_ip = get_client_ip(request)
    
    endpoints = MockEndpoint.objects.filter(creator_ip=client_ip).order_by('-created_at')[:20]
    
    site_url = request.build_absolute_uri('/').rstrip('/')
    
    endpoints_list = []
    for ep in endpoints:
        # Build path-based URL: /{path}/{endpoint_id}/
        user_path = ep.path.strip('/') if ep.path else 'api/mock'
        endpoints_list.append({
            'endpoint_id': ep.endpoint_id,
            'endpoint_url': f"{site_url}/{user_path}/{ep.endpoint_id}/",
            'name': ep.name,
            'path': f"/{user_path}",
            'method': ep.method,
            'status_code': ep.status_code,
            'record_count': ep.record_count,
            'response_body': ep.response_body,
            'ip_restriction_enabled': ep.ip_restriction_enabled,
            'allowed_ips': ep.get_allowed_ips_list(),
            'request_count': ep.request_count,
            'created_at': ep.created_at.isoformat(),
            'is_expired': ep.is_expired()
        })
    
    return JsonResponse({
        'success': True,
        'count': len(endpoints_list),
        'limit': 5,
        'remaining': max(0, 5 - len(endpoints_list)),
        'endpoints': endpoints_list,
        'your_ip': client_ip
    })

@api_view(['GET'])
def track_swagger_usage(request):
    """
    Track Swagger Viewer usage event.
    The actual tracking happens via VisitorTrackingMiddleware which logs the request.
    No JSON payload is processed or stored.
    """
    return Response({'success': True, 'tracked': True})


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def track_tool_usage(request):
    """
    Generic endpoint to track tool usage.
    Expects JSON: {"tool_name": "...", "action": "...", "metadata": {...}}
    """
    try:
        data = request.data
        tool_name = data.get('tool_name')
        action = data.get('action')
        
        if not tool_name or not action:
            return Response({'success': False, 'error': 'tool_name and action are required'}, status=400)
            
        # Get IP and User Agent
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
        if ip and ',' in ip:
            ip = ip.split(',')[0].strip()
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Resolve Geolocation (if not local)
        country = None
        city = None
        
        if ip not in ['127.0.0.1', '::1'] and not ip.startswith('192.168.'):
            try:
                import requests
                # Use a short timeout to prevent blocking
                geo_resp = requests.get(f'http://ip-api.com/json/{ip}', timeout=1.5)
                if geo_resp.status_code == 200:
                    geo_data = geo_resp.json()
                    if geo_data.get('status') == 'success':
                        country = geo_data.get('country')
                        city = geo_data.get('city')
            except:
                pass # Fail silently for geo lookup
        
        # Create Log
        from .models import ToolUsageLog
        ToolUsageLog.objects.create(
            tool_name=tool_name,
            action=action,
            ip_address=ip,
            user_agent=user_agent,
            country=country,
            city=city,
            metadata=data.get('metadata', {})
        )
        
        return Response({'success': True, 'tracked': True})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)

def xsd_to_json_schema_example_page(request):
    """Render the XSD to JSON Schema Examples page"""
    return render(request, 'xsd-to-json-schema-example.html')

def xsd_complextype_to_json_schema_page(request):
    """Render the XSD ComplexType Guide page"""
    return render(request, 'xsd-complextype-to-json-schema.html')

def json_viewer_page(request):
    """Render the JSON Viewer Online page"""
    return render(request, 'json-viewer.html')

def sqlite_viewer_page(request):
    """
    Render the SQLite Viewer page.
    """
    context = {
        'page_title': 'SQLite Viewer Online – Open & Explore SQLite .db Files Instantly',
        'meta_description': 'Open, view, and explore SQLite database files online. Upload .db, browse tables, run SQL queries, and export data to CSV or JSON. 100% client-side, private, and secure.',
    }
    return render(request, 'sqlite-viewer.html', context)


# ====================
# AI JSON Generator API
# ====================

import os
import requests as http_requests

@api_view(['POST'])
def ai_generate_json(request):
    """
    Generate JSON using OpenRouter AI based on user's natural language description.
    
    Expected input: {"prompt": "create 5 records of biscuits"}
    Returns: {"success": true, "json": "generated_json_string"}
    """
    try:
        prompt = request.data.get('prompt', '').strip()
        
        if not prompt:
            return Response({
                'success': False,
                'error': 'No prompt provided. Please describe what JSON you need.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get OpenRouter API key from environment
        api_key = os.environ.get('OPENROUTER_API_KEY')
        
        if not api_key:
            return Response({
                'success': False,
                'error': 'OpenRouter API key not configured.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # System prompt for JSON generation
        system_prompt = """You are a JSON generator. Generate ONLY valid JSON based on the user's request.

Rules:
1. Return ONLY valid JSON - no markdown, no code blocks, no explanations
2. Generate realistic, varied data for each record
3. If user asks for multiple records, return an array
4. Include appropriate fields based on the entity type
5. For names, use realistic examples (not "Name 1", "Name 2")
6. For icd codes, use realistic format (like ICD-10 codes, product SKUs, etc.)

Examples:
- "5 biscuits" → array of 5 biscuit objects with name, brand, flavor, etc.
- "100 users" → array of 100 user objects with name, email, age, etc.
- "10 countries" → array of 10 countries with name, capital, population, etc."""

        # Call OpenRouter API with Llama 3.3 70B
        response = http_requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://jsonformatterspro.com",
                "X-Title": "JSON Formatter Pro"
            },
            json={
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 8192
            },
            timeout=60
        )
        
        if response.status_code != 200:
            return Response({
                'success': False,
                'error': f'AI API error: {response.status_code}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = response.json()
        ai_text = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # Clean up response - remove markdown code blocks if present
        ai_text = ai_text.strip()
        if ai_text.startswith('```json'):
            ai_text = ai_text[7:]
        if ai_text.startswith('```'):
            ai_text = ai_text[3:]
        if ai_text.endswith('```'):
            ai_text = ai_text[:-3]
        ai_text = ai_text.strip()
        
        # Validate it's proper JSON
        try:
            parsed = json.loads(ai_text)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            
            return Response({
                'success': True,
                'json': formatted
            })
        except json.JSONDecodeError as e:
            return Response({
                'success': False,
                'error': f'AI returned invalid JSON: {str(e)}',
                'raw': ai_text[:500]  # Return first 500 chars for debugging
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except http_requests.exceptions.Timeout:
        return Response({
            'success': False,
            'error': 'AI request timed out. Please try again.'
        }, status=status.HTTP_504_GATEWAY_TIMEOUT)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
