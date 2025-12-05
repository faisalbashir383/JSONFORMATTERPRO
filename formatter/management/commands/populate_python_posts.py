"""
Management command to populate additional Python blog posts from blog_content
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from formatter.models import BlogCategory, BlogPost


class Command(BaseCommand):
    help = 'Populate additional Python blog posts with detailed content'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating/retrieving Python category...')
        
        # Get or create Python category
        python_category, created = BlogCategory.objects.get_or_create(
            name='Python',
            defaults={'description': 'Python programming tutorials and advanced topics'}
        )
        
        if created:
            self.stdout.write('  ✓ Created Python category')
        else:
            self.stdout.write('  ✓ Python category already exists')
        
        self.stdout.write('\nPopulating detailed Python blog posts...')
        
        # Get blog posts data
        posts_data = self._get_python_posts()
        
        # Create blog posts
        created_count = 0
        for i, post_data in enumerate(posts_data, 1):
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'category': python_category,
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'],
                    'tags': post_data['tags'],
                    'meta_description': post_data['meta_description'],
                    'meta_keywords': post_data['meta_keywords'],
                    'published': True,
                    'published_at': timezone.now(),
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created post {i}/{len(posts_data)}: {post.title[:50]}...')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} new Python blog posts!'))
        self.stdout.write(f'📚 Total posts in database: {BlogPost.objects.count()}')

    def _generate_content(self, sections):
        """Generate full HTML content from sections"""
        content = ''
        for i, (heading, text) in enumerate(sections):
            if i == 0:
                content += f'<p>{text}</p>\n\n'
            else:
                content += f'<h2>{heading}</h2>\n<p>{text}</p>\n\n'
        return content

    def _get_python_posts(self):
        """Get all Python blog posts with detailed content"""
        
        python_posts = [
            {
                'title': 'Python List Comprehensions: Complete Guide with Advanced Patterns',
                'excerpt': 'Master Python list comprehensions from basics to advanced patterns including nested comprehensions, filtering, conditional logic, and performance optimization techniques.',
                'content_sections': [
                    ('Introduction', 'List comprehensions are one of Python\'s most powerful features, providing a concise way to create lists. They\'re not just syntactic sugar - they\'re often faster than traditional loops and lead to more readable, Pythonic code.'),
                    ('Basic Syntax', '''<pre><code class="language-python">
# Traditional approach
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With transformation
names = ['alice', 'bob', 'charlie']
capitalized = [name.capitalize() for name in names]
</code></pre>'''),
                    ('Filtering with Conditions', '''<pre><code class="language-python">
# Single condition
evens = [x for x in range(20) if x % 2 == 0]

# Multiple conditions
divisible_by_2_and_5 = [x for x in range(100) if x % 2 == 0 if x % 5 == 0]

# If-else in comprehension
numbers = [x if x % 2 == 0 else -x for x in range(10)]
# [0, -1, 2, -3, 4, -5, 6, -7, 8, -9]
</code></pre>'''),
                    ('Nested List Comprehensions', '''<pre><code class="language-python">
# Create a 3x3 matrix
matrix = [[i*3+j for j in range(3)] for i in range(3)]
# [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# Flatten a matrix
flattened = [num for row in matrix for num in row]

# Combine two lists
pairs = [(x, y) for x in [1, 2, 3] for y in ['a', 'b', 'c']]
</code></pre>'''),
                    ('Dictionary and Set Comprehensions', '''<pre><code class="language-python">
# Dictionary comprehension
squares_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Invert dictionary
inverted = {v: k for k, v in squares_dict.items()}

# Set comprehension (removes duplicates)
unique_chars = {char for word in ['hello', 'world'] for char in word}
</code></pre>'''),
                    ('Performance Tips', '''List comprehensions are generally faster than loops because they're optimized at the C level. However, for very large datasets, consider using generator expressions instead:

<pre><code class="language-python">
# Generator expression (memory efficient)
large_squares = (x**2 for x in range(1000000))

# Use next() to get values one at a time
print(next(large_squares))  # 0
print(next(large_squares))  # 1
</code></pre>'''),
                    ('Real-World Examples', '''<pre><code class="language-python">
# Filter and transform API data
users = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
adult_names = [user['name'] for user in users if user['age'] >= 18]

# Parse CSV data
csv_lines = ['name,age', 'Alice,30', 'Bob,25']
data = [line.split(',') for line in csv_lines[1:]]

# Process file lines
with open('data.txt') as f:
    clean_lines = [line.strip().lower() for line in f if line.strip()]
</code></pre>'''),
                ],
                'tags': 'python, list comprehension, tutorial, advanced python, performance',
                'meta_keywords': 'python list comprehension, python tutorial, list comprehension examples, python optimization'
            },
            {
                'title': 'Python Decorators Deep Dive: From Basics to Custom Implementations',
                'excerpt': 'Complete guide to Python decorators covering function decorators, class decorators, decorators with arguments, preserving metadata, and real-world use cases.',
                'content_sections': [
                    ('Understanding Decorators', 'Decorators are a powerful metaprogramming tool in Python that allow you to modify or enhance functions and classes without changing their source code. They follow the decorator pattern from design patterns.'),
                    ('Basic Function Decorator', '''<pre><code class="language-python">
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"

# Equivalent to: greet = my_decorator(greet)
result = greet("Alice")
</code></pre>'''),
                    ('Decorators with Arguments', '''<pre><code class="language-python">
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

@repeat(times=3)
def say_hello(name):
    return f"Hello, {name}!"

# Calls the function 3 times
messages = say_hello("Bob")
</code></pre>'''),
                    ('Preserving Function Metadata', '''<pre><code class="language-python">
from functools import wraps

def timer(func):
    @wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    """This is a slow function"""
    import time
    time.sleep(1)
    return "Done"

print(slow_function.__name__)  # 'slow_function'
print(slow_function.__doc__)   # 'This is a slow function'
</code></pre>'''),
                    ('Class Decorators', '''<pre><code class="language-python">
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connection = "Connected"

db1 = Database()
db2 = Database()
print(db1 is db2)  # True - same instance
</code></pre>'''),
                    ('Real-World Use Cases', '''<pre><code class="language-python">
# Authentication decorator
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            raise PermissionError("Not authenticated")
        return func(*args, **kwargs)
    return wrapper

# Caching/Memoization
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Logging
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

# Rate limiting
import time
from functools import wraps

def rate_limit(max_per_second):
    min_interval = 1.0 / max_per_second
    def decorator(func):
        last_called = [0.0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator
</code></pre>'''),
                    ('Stacking Multiple Decorators', '''<pre><code class="language-python">
@timer
@log_calls
@require_auth
def process_payment(amount):
    return f"Processed ${amount}"

# Decorators are applied from bottom to top
# Equivalent to: timer(log_calls(require_auth(process_payment)))
</code></pre>'''),
                ],
                'tags': 'python, decorators, advanced python, metaprogramming, design patterns',
                'meta_keywords': 'python decorators, function decorators, python metaprogramming, decorator pattern'
            },
        ]
        
        # Generate full posts with content
        posts = []
        for post_data in python_posts:
            posts.append({
                'title': post_data['title'],
                'excerpt': post_data['excerpt'],
                'content': self._generate_content(post_data['content_sections']),
                'tags': post_data['tags'],
                'meta_description': post_data['excerpt'],
                'meta_keywords': post_data['meta_keywords']
            })
        
        return posts
