"""
Management command to populate blog with 30 programming posts
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from formatter.models import BlogCategory, BlogPost


class Command(BaseCommand):
    help = 'Populate blog with 30 programming posts'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating blog categories...')
        
        # Create categories
        categories_data = [
            {'name': 'Python', 'description': 'Python programming tutorials and tips'},
            {'name': 'JavaScript', 'description': 'JavaScript and web development'},
            {'name': 'AI & Machine Learning', 'description': 'Artificial Intelligence and ML tutorials'},
            {'name': 'Web Development', 'description': 'HTML, CSS, and web technologies'},
            {'name': 'Data Science', 'description': 'Data analysis and visualization'},
            {'name': 'Programming Basics', 'description': 'Beginner programming concepts'},
            {'name': 'DevOps', 'description': 'CI/CD, Docker, and deployment'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = BlogCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'  ✓ Created category: {cat.name}')
        
        self.stdout.write('\nCreating 30 blog posts...')
        
        # Blog posts data with code examples
        posts_data = [
            {
                'category': 'Python',
                'title': 'Python List Comprehensions: A Complete Guide',
                'excerpt': 'Learn how to write cleaner and more efficient Python code using list comprehensions with practical examples.',
                'content': '''
<p>List comprehensions provide a concise way to create lists in Python. They're more readable and often faster than traditional for loops.</p>

<h2>Basic Syntax</h2>
<p>The basic syntax of a list comprehension is:</p>

<pre><code class="language-python">
# Traditional approach
squares = []
for x in range(10):
    squares.append(x**2)

# List comprehension approach
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
</code></pre>

<h2>With Conditions</h2>
<p>You can add conditions to filter elements:</p>

<pre><code class="language-python">
# Get even numbers only
evens = [x for x in range(20) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Multiple conditions
filtered = [x for x in range(50) if x % 2 == 0 if x % 5 == 0]
print(filtered)  # [0, 10, 20, 30, 40]
</code></pre>

<h2>Nested List Comprehensions</h2>
<p>Create matrices and flatten lists:</p>

<pre><code class="language-python">
# Create a 3x3 matrix
matrix = [[i*3+j for j in range(3)] for i in range(3)]
print(matrix)  # [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# Flatten a matrix
flattened = [num for row in matrix for num in row]
print(flattened)  # [0, 1, 2, 3, 4, 5, 6, 7, 8]
</code></pre>

<p>List comprehensions make your code more Pythonic and easier to read once you're familiar with the syntax!</p>
                ''',
                'tags': 'python, list comprehension, tutorial, beginner',
                'meta_description': 'Complete guide to Python list comprehensions with examples. Learn how to write cleaner, more efficient Python code.',
                'meta_keywords': 'python list comprehension, python tutorial, python tips, list comprehension examples'
            },
            {
                'category': 'JavaScript',
                'title': 'Understanding JavaScript Async/Await',
                'excerpt': 'Master asynchronous JavaScript with async/await syntax for cleaner, more readable code.',
                'content': '''
<p>Async/await makes working with promises much easier and your asynchronous code look more like synchronous code.</p>

<h2>Basic Usage</h2>
<pre><code class="language-javascript">
// Traditional promise approach
function fetchUser() {
    return fetch('https://api.example.com/user')
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
}

// Using async/await
async function fetchUser() {
    try {
        const response = await fetch('https://api.example.com/user');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}
</code></pre>

<h2>Multiple Async Operations</h2>
<pre><code class="language-javascript">
async function getAllData() {
    try {
        // Sequential execution
        const user = await fetch('/api/user').then(r => r.json());
        const posts = await fetch(`/api/posts/${user.id}`).then(r => r.json());
        
        // Parallel execution (faster!)
        const [userData, postsData] = await Promise.all([
            fetch('/api/user').then(r => r.json()),
            fetch('/api/posts').then(r => r.json())
        ]);
        
        return { userData, postsData };
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
</code></pre>

<p>Always remember to use try/catch blocks for proper error handling!</p>
                ''',
                'tags': 'javascript, async await, promises, async programming',
                'meta_description': 'Learn JavaScript async/await with practical examples. Master asynchronous programming for modern web development.',
                'meta_keywords': 'javascript async await, async javascript, promises tutorial, async programming'
            },
            {
                'category': 'Python',
                'title': 'Python Decorators Explained',
                'excerpt': 'Understanding Python decorators and how to use them to enhance your functions.',
                'content': '''
<p>Decorators are a powerful feature in Python that allow you to modify or enhance functions without changing their core functionality.</p>

<h2>What is a Decorator?</h2>
<p>A decorator is a function that takes another function and extends its behavior.</p>

<pre><code class="language-python">
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Before function call
# Hello!
# After function call
</code></pre>

<h2>Decorators with Arguments</h2>
<pre><code class="language-python">
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
</code></pre>

<h2>Practical Example: Timing Decorator</h2>
<pre><code class="language-python">
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    return "Done!"

result = slow_function()
# Output: slow_function took 2.00 seconds
</code></pre>
                ''',
                'tags': 'python, decorators, advanced python, functions',
                'meta_description': 'Complete guide to Python decorators with examples. Learn how to enhance functions and write cleaner code.',
                'meta_keywords': 'python decorators, python functions, decorator pattern, advanced python'
            },
            # Adding more posts...
            {
                'category': 'AI & Machine Learning',
                'title': 'Introduction to Machine Learning with Python',
                'excerpt': 'Get started with machine learning using scikit-learn and practical examples.',
                'content': '''
<p>Machine Learning enables computers to learn from data without being explicitly programmed. Let's explore the basics with Python.</p>

<h2>Linear Regression Example</h2>
<pre><code class="language-python">
from sklearn.linear_model import LinearRegression
import numpy as np

# Sample data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Create and train model
model = LinearRegression()
model.fit(X, y)

# Make predictions
prediction = model.predict([[6]])
print(f"Predicted value: {prediction[0]}")  # Output: 12.0
print(f"Coefficient: {model.coef_[0]}")  # Output: 2.0
</code></pre>

<h2>Classification with Decision Trees</h2>
<pre><code class="language-python">
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Sample dataset
X = [[0, 0], [1, 1], [2, 2], [3, 3]]
y = [0, 0, 1, 1]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

# Train model
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Evaluate
accuracy = clf.score(X_test, y_test)
print(f"Accuracy: {accuracy * 100}%")
</code></pre>
                ''',
                'tags': 'machine learning, python, sklearn, ai, tutorial',
                'meta_description': 'Learn machine learning basics with Python and scikit-learn. Practical examples for beginners.',
                'meta_keywords': 'machine learning python, sklearn tutorial, ml basics, python ai'
            },
            {
                'category': 'Web Development',
                'title': 'CSS Flexbox Complete Guide',
                'excerpt': 'Master CSS Flexbox layout with practical examples and best practices.',
                'content': '''
<p>Flexbox is a powerful layout system that makes it easy to design flexible responsive layouts.</p>

<h2>Basic Flex Container</h2>
<pre><code class="language-css">
.container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
}

.item {
    flex: 1; /* Equal width for all items */
    padding: 1rem;
    background: #f0f0f0;
}
</code></pre>

<h2>Responsive Navigation</h2>
<pre><code class="language-css">
.navbar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
}

.nav-links {
    display: flex;
    gap: 2rem;
    list-style: none;
}

@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
    }
    
    .nav-links {
        flex-direction: column;
        width: 100%;
    }
}
</code></pre>

<h2>Centering Content</h2>
<pre><code class="language-css">
.center-box {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
</code></pre>
                ''',
                'tags': 'css, flexbox, web development, responsive design',
                'meta_description': 'Complete CSS Flexbox guide with examples. Learn responsive web layouts with flexbox.',
                'meta_keywords': 'css flexbox, flexbox tutorial, responsive design, css layout'
            },
        ]
        
        # Create remaining 25 posts with varied content
        additional_posts = self._generate_additional_posts(categories)
        posts_data.extend(additional_posts)
        
        # Create all blog posts
        created_count = 0
        for i, post_data in enumerate(posts_data[:30], 1):
            category = categories[post_data['category']]
            
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'category': category,
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
                self.stdout.write(f'  ✓ Created post {i}/30: {post.title}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} new blog posts!'))
        self.stdout.write(f'📚 Total posts in database: {BlogPost.objects.count()}')

    def _generate_additional_posts(self, categories):
        """Generate 25 more blog posts"""
        return [
            {
                'category': 'JavaScript',
                'title': 'ES6 Arrow Functions Guide',
                'excerpt': 'Learn modern JavaScript arrow functions and when to use them.',
                'content': '<p>Arrow functions provide a shorter syntax for writing functions.</p><pre><code class="language-javascript">const add = (a, b) => a + b;\nconst numbers = [1, 2, 3].map(n => n * 2);\nconsole.log(numbers); // [2, 4, 6]</code></pre>',
                'tags': 'javascript, es6, arrow functions',
                'meta_description': 'Master JavaScript ES6 arrow functions with examples',
                'meta_keywords': 'javascript arrow functions, es6, modern javascript'
            },
            {
                'category': 'Python',
                'title': 'Python Dictionary Methods You Should Know',
                'excerpt': 'Essential Python dictionary methods for efficient data manipulation.',
                'content': '<p>Python dictionaries have powerful built-in methods.</p><pre><code class="language-python">data = {\'a\': 1, \'b\': 2}\ndata.get(\'c\', 0)  # Returns 0 if key doesn\'t exist\ndata.setdefault(\'d\', 3)\nfor key, value in data.items():\n    print(f"{key}: {value}")</code></pre>',
                'tags': 'python, dictionaries, data structures',
                'meta_description': 'Learn essential Python dictionary methods with examples',
                'meta_keywords': 'python dictionary, python methods, data structures'
            },
            {
                'category': 'Web Development',
                'title': 'Build a REST API with Express.js',
                'excerpt': 'Create a RESTful API using Node.js and Express framework.',
                'content': '<p>Express makes building APIs simple.</p><pre><code class="language-javascript">const express = require(\'express\');\nconst app = express();\n\napp.get(\'/api/users\', (req, res) => {\n    res.json({ users: [\'Alice\', \'Bob\'] });\n});\n\napp.listen(3000, () => console.log(\'Server running\'));</code></pre>',
                'tags': 'nodejs, express, REST API, backend',
                'meta_description': 'Build REST APIs with Express.js and Node.js',
                'meta_keywords': 'express.js, nodejs api, rest api tutorial'
            },
            {
                'category': 'Data Science',
                'title': 'Pandas DataFrames Tutorial',
                'excerpt': 'Working with Pandas DataFrames for data analysis in Python.',
                'content': '<p>Pandas is essential for data manipulation.</p><pre><code class="language-python">import pandas as pd\n\ndf = pd.DataFrame({\'A\': [1, 2, 3], \'B\': [4, 5, 6]})\nprint(df.head())\nprint(df.describe())\nfiltered = df[df[\'A\'] > 1]</code></pre>',
                'tags': 'pandas, data science, python, data analysis',
                'meta_description': 'Learn Pandas DataFrame operations for data analysis',
                'meta_keywords': 'pandas tutorial, dataframe, python data analysis'
            },
            {
                'category': 'Programming Basics',
                'title': 'Understanding Variables and Data Types',
                'excerpt': 'Learn the fundamentals of variables and data types in programming.',
                'content': '<p>Variables store data in your programs.</p><pre><code class="language-python"># Python variables\nname = "Alice"  # String\nage = 25  # Integer\nheight = 5.6  # Float\nis_student = True  # Boolean\n\nprint(f"{name} is {age} years old")</code></pre>',
                'tags': 'programming basics, variables, beginner',
                'meta_description': 'Learn about variables and data types for beginners',
                'meta_keywords': 'programming basics, variables tutorial, data types'
            },
            {
                'category': 'DevOps',
                'title': 'Docker Basics: Getting Started',
                'excerpt': 'Introduction to Docker containers and containerization.',
                'content': '<p>Docker makes deployment consistent across environments.</p><pre><code class="language-dockerfile">FROM python:3.9\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ["python", "app.py"]</code></pre>',
                'tags': 'docker, devops, containers, deployment',
                'meta_description': 'Getting started with Docker containers and containerization',
                'meta_keywords': 'docker tutorial, containers, devops basics'
            },
            {
                'category': 'JavaScript',
                'title': 'JavaScript Array Methods Cheat Sheet',
                'excerpt': 'Essential JavaScript array methods every developer should know.',
                'content': '<p>Master these array methods for cleaner code.</p><pre><code class="language-javascript">const arr = [1, 2, 3, 4, 5];\narr.map(x => x * 2);  // [2, 4, 6, 8, 10]\narr.filter(x => x > 2);  // [3, 4, 5]\narr.reduce((acc, x) => acc + x, 0);  // 15\narr.find(x => x > 3);  // 4</code></pre>',
                'tags': 'javascript, arrays, methods, tutorial',
                'meta_description': 'JavaScript array methods cheat sheet with examples',
                'meta_keywords': 'javascript arrays, array methods, javascript tutorial'
            },
            {
                'category': 'Python',
                'title': 'Python File Handling Made Easy',
                'excerpt': 'Read and write files in Python with best practices.',
                'content': '<p>Working with files is a common task in Python.</p><pre><code class="language-python">with open(\'file.txt\', \'r\') as f:\n    content = f.read()\n\nwith open(\'output.txt\', \'w\') as f:\n    f.write(\'Hello, World!\')\n\nimport json\nwith open(\'data.json\', \'r\') as f:\n    data = json.load(f)</code></pre>',
                'tags': 'python, file handling, io, tutorial',
                'meta_description': 'Learn Python file handling with practical examples',
                'meta_keywords': 'python file handling, read write files python'
            },
            {
                'category': 'AI & Machine Learning',
                'title': 'Neural Networks from Scratch',
                'excerpt': 'Build a simple neural network using only NumPy.',
                'content': '<p>Understanding neural networks by building one.</p><pre><code class="language-python">import numpy as np\n\ndef sigmoid(x):\n    return 1 / (1 + np.exp(-x))\n\nX = np.array([[0,0], [0,1], [1,0], [1,1]])\ny = np.array([[0], [1], [1], [0]])\n\nweights = np.random.random((2, 1))\nfor _ in range(10000):\n    output = sigmoid(np.dot(X, weights))\n    error = y - output\n    weights += np.dot(X.T, error * output * (1 - output))</code></pre>',
                'tags': 'neural networks, machine learning, numpy, ai',
                'meta_description': 'Build neural networks from scratch with NumPy',
                'meta_keywords': 'neural network tutorial, numpy, machine learning'
            },
            {
                'category': 'Web Development',
                'title': 'React Hooks Complete Guide',
                'excerpt': 'Master React Hooks for modern functional components.',
                'content': '<p>Hooks revolutionized React development.</p><pre><code class="language-javascript">import React, { useState, useEffect } from \'react\';\n\nfunction Counter() {\n    const [count, setCount] = useState(0);\n    \n    useEffect(() => {\n        document.title = `Count: ${count}`;\n    }, [count]);\n    \n    return (\n        <button onClick={() => setCount(count + 1)}>\n            Count: {count}\n        </button>\n    );\n}</code></pre>',
                'tags': 'react, hooks, javascript, frontend',
                'meta_description': 'Complete guide to React Hooks with practical examples',
                'meta_keywords': 'react hooks, useState, useEffect, react tutorial'
            },
            {
                'category': 'Python',
                'title': 'Python Context Managers Explained',
                'excerpt': 'Understanding the with statement and creating custom context managers.',
                'content': '<p>Context managers handle setup and cleanup automatically.</p><pre><code class="language-python">class FileManager:\n    def __init__(self, filename, mode):\n        self.filename = filename\n        self.mode = mode\n        \n    def __enter__(self):\n        self.file = open(self.filename, self.mode)\n        return self.file\n        \n    def __exit__(self, exc_type, exc_val, exc_tb):\n        self.file.close()\n\nwith FileManager(\'test.txt\', \'w\') as f:\n    f.write(\'Hello!\')</code></pre>',
                'tags': 'python, context managers, advanced python',
                'meta_description': 'Learn Python context managers and the with statement',
                'meta_keywords': 'python context managers, with statement, python tutorial'
            },
            {
                'category': 'JavaScript',
                'title': 'JavaScript Promises Explained',
                'excerpt': 'Master JavaScript Promises for asynchronous programming.',
                'content': '<p>Promises help handle async operations elegantly.</p><pre><code class="language-javascript">const fetchData = () => {\n    return new Promise((resolve, reject) => {\n        setTimeout(() => {\n            resolve({ data: \'Success!\' });\n        }, 1000);\n    });\n};\n\nfetchData()\n    .then(result => console.log(result))\n   .catch(error => console.error(error));</code></pre>',
                'tags': 'javascript, promises, async, tutorial',
                'meta_description': 'Complete guide to JavaScript Promises',
                'meta_keywords': 'javascript promises, async javascript, promise tutorial'
            },
            {
                'category': 'Data Science',
                'title': 'Data Visualization with Matplotlib',
                'excerpt': 'Create stunning visualizations using Matplotlib in Python.',
                'content': '<p>Matplotlib is powerful for creating charts and graphs.</p><pre><code class="language-python">import matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(0, 10, 100)\ny = np.sin(x)\n\nplt.figure(figsize=(10, 6))\nplt.plot(x, y, label=\'sin(x)\')\nplt.xlabel(\'X axis\')\nplt.ylabel(\'Y axis\')\nplt.title(\'Sine Wave\')\nplt.legend()\nplt.grid(True)\nplt.show()</code></pre>',
                'tags': 'matplotlib, data visualization, python, plotting',
                'meta_description': 'Learn data visualization with Matplotlib and Python',
                'meta_keywords': 'matplotlib tutorial, python visualization, data plotting'
            },
            {
                'category': 'Programming Basics',
                'title': 'Understanding Loops in Programming',
                'excerpt': 'Learn about for loops, while loops, and when to use each.',
                'content': '<p>Loops let you repeat code efficiently.</p><pre><code class="language-python"># For loop\nfor i in range(5):\n    print(i)\n\n# While loop\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1\n\n# Loop with break\nfor num in range(10):\n    if num == 5:\n        break\n    print(num)</code></pre>',
                'tags': 'programming, loops, beginner, tutorial',
                'meta_description': 'Understanding programming loops for beginners',
                'meta_keywords': 'programming loops, for loop, while loop'
            },
            {
                'category': 'DevOps',
                'title': 'Git Commands Every Developer Needs',
                'excerpt': 'Essential Git commands for version control and collaboration.',
                'content': '<p>Git is crucial for modern development.</p><pre><code class="language-bash"># Initialize repository\ngit init\n\n# Stage and commit\ngit add .\ngit commit -m "Initial commit"\n\n# Branching\ngit branch feature\ngit checkout feature\n\n# Merge branches\ngit checkout main\ngit merge feature\n\n# Push to remote\ngit push origin main</code></pre>',
                'tags': 'git, version control, devops, tutorial',
                'meta_description': 'Essential Git commands every developer should know',
                'meta_keywords': 'git commands, version control, git tutorial'
            },
            {
                'category': 'Web Development',
                'title': 'CSS Grid Layout Tutorial',
                'excerpt': 'Master CSS Grid for powerful two-dimensional layouts.',
                'content': '<p>CSS Grid makes complex layouts simple.</p><pre><code class="language-css">.grid-container {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    grid-gap: 20px;\n    padding: 20px;\n}\n\n.grid-item {\n    background: #f0f0f0;\n    padding: 20px;\n    text-align: center;\n}\n\n@media (max-width: 768px) {\n    .grid-container {\n        grid-template-columns: 1fr;\n    }\n}</code></pre>',
                'tags': 'css grid, css, web design, responsive',
                'meta_description': 'Learn CSS Grid for modern web layouts',
                'meta_keywords': 'css grid, grid layout, responsive design'
            },
            {
                'category': 'Python',
                'title': 'Python Generators and Iterators',
                'excerpt': 'Efficient iteration with Python generators and iterators.',
                'content': '<p>Generators provide memory-efficient iteration.</p><pre><code class="language-python"># Generator function\ndef fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b\n\nfor num in fibonacci(10):\n    print(num)\n\n# Generator expression\nsquares = (x**2 for x in range(1000000))\nprint(next(squares))  # 0\nprint(next(squares))  # 1</code></pre>',
                'tags': 'python, generators, iterators, advanced',
                'meta_description': 'Master Python generators and iterators',
                'meta_keywords': 'python generators, iterators, yield'
            },
            {
                'category': 'JavaScript',
                'title': 'Destructuring in JavaScript',
                'excerpt': 'Simplify your code with ES6 destructuring syntax.',
                'content': '<p>Destructuring makes extracting values cleaner.</p><pre><code class="language-javascript">// Array destructuring\nconst [first, second, ...rest] = [1, 2, 3, 4, 5];\n\n// Object destructuring  \nconst {name, age, city = \'NYC\'} = user;\n\n// Function parameters\nfunction greet({name, age}) {\n    console.log(`Hello ${name}, age ${age}`);\n}\n\ngreet({name: \'Alice\', age: 25});</code></pre>',
                'tags': 'javascript, destructuring, es6, syntax',
                'meta_description': 'Learn JavaScript destructuring with examples',
                'meta_keywords': 'javascript destructuring, es6 destructuring'
            },
            {
                'category': 'AI & Machine Learning',
                'title': 'K-Means Clustering Tutorial',
                'excerpt': 'Implement K-Means clustering for unsupervised learning.',
                'content': '<p>K-Means groups similar data points together.</p><pre><code class="language-python">from sklearn.cluster import KMeans\nimport numpy as np\n\n# Sample data\nX = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])\n\n# Create and fit model\nkmeans = KMeans(n_clusters=2)\nkmeans.fit(X)\n\nprint("Labels:", kmeans.labels_)\nprint("Centers:", kmeans.cluster_centers_)</code></pre>',
                'tags': 'machine learning, clustering, k-means, sklearn',
                'meta_description': 'Learn K-Means clustering with Python',
                'meta_keywords': 'k-means clustering, machine learning, sklearn'
            },
            {
                'category': 'Web Development',
                'title': 'Building Progressive Web Apps',
                'excerpt': 'Create Progressive Web Apps (PWAs) with modern web technologies.',
                'content': '<p>PWAs combine the best of web and mobile apps.</p><pre><code class="language-javascript">// service-worker.js\nself.addEventListener(\'install\', event => {\n    event.waitUntil(\n        caches.open(\'v1\').then(cache => {\n            return cache.addAll([\n                \'/\',\n                \'/styles.css\',\n                \'/script.js\'\n            ]);\n        })\n    );\n});</code></pre>',
                'tags': 'pwa, web development, service workers',
                'meta_description': 'Build Progressive Web Apps (PWAs) tutorial',
                'meta_keywords': 'pwa tutorial, progressive web apps, service workers'
            },
            {
                'category': 'Data Science',
                'title': 'NumPy Array Operations',
                'excerpt': 'Essential NumPy operations for numerical computing.',
                'content': '<p>NumPy is the foundation of data science in Python.</p><pre><code class="language-python">import numpy as np\n\narr = np.array([1, 2, 3, 4, 5])\nprint(arr * 2)  # [2, 4, 6, 8, 10]\nprint(arr.mean())  # 3.0\n\n# Matrix operations\nmatrix = np.array([[1, 2], [3, 4]])\nprint(np.linalg.inv(matrix))  # Inverse\nprint(matrix.T)  # Transpose</code></pre>',
                'tags': 'numpy, data science, python, arrays',
                'meta_description': 'NumPy array operations tutorial for data science',
                'meta_keywords': 'numpy tutorial, numpy arrays, data science python'
            },
            {
                'category': 'Programming Basics',
                'title': 'Functions and Parameters Explained',
                'excerpt': 'Understanding functions, parameters, and return values in programming.',
                'content': '<p>Functions organize code into reusable blocks.</p><pre><code class="language-python">def greet(name, greeting="Hello"):\n    return f"{greeting}, {name}!"\n\nprint(greet("Alice"))  # Hello, Alice!\nprint(greet("Bob", "Hi"))  # Hi, Bob!\n\n# Multiple return values\ndef calculate(a, b):\n    return a + b, a - b, a * b\n\nsum_val, diff, prod = calculate(10, 5)</code></pre>',
                'tags': 'programming basics, functions, parameters',
                'meta_description': 'Learn programming functions and parameters',
                'meta_keywords': 'programming functions, function parameters, coding basics'
            },
            {
                'category': 'DevOps',
                'title': 'CI/CD Pipeline with GitHub Actions',
                'excerpt': 'Automate your development workflow with GitHub Actions.',
                'content': '<p>GitHub Actions enables powerful CI/CD workflows.</p><pre><code class="language-yaml">name: CI\n\non: [push, pull_request]\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v2\n      - name: Set up Python\n        uses: actions/setup-python@v2\n        with:\n          python-version: 3.9\n      - name: Run tests\n        run: |\n          pip install -r requirements.txt\n          pytest</code></pre>',
                'tags': 'ci cd, github actions, devops, automation',
                'meta_description': 'Build CI/CD pipelines with GitHub Actions',
                'meta_keywords': 'github actions, ci cd, devops automation'
            },
            {
                'category': 'JavaScript',
                'title': 'JavaScript Classes and OOP',
                'excerpt': 'Object-Oriented Programming in JavaScript with ES6 classes.',
                'content': '<p>JavaScript classes provide a cleaner syntax for OOP.</p><pre><code class="language-javascript">class Animal {\n    constructor(name) {\n        this.name = name;\n    }\n    \n    speak() {\n        console.log(`${this.name} makes a sound`);\n    }\n}\n\nclass Dog extends Animal {\n    speak() {\n        console.log(`${this.name} barks`);\n    }\n}\n\nconst dog = new Dog(\'Rex\');\ndog.speak();  // Rex barks</code></pre>',
                'tags': 'javascript, oop, classes, es6',
                'meta_description': 'Learn Object-Oriented Programming in JavaScript',
                'meta_keywords': 'javascript classes, javascript oop, es6 classes'
            },
            {
                'category': 'Python',
                'title': 'Error Handling in Python',
                'excerpt': 'Master exception handling and error management in Python.',
                'content': '<p>Proper error handling makes your code robust.</p><pre><code class="language-python">try:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f"Error: {e}")\nexcept Exception as e:\n    print(f"Unexpected error: {e}")\nelse:\n    print("No errors occurred")\nfinally:\n    print("Cleanup code")\n\n# Custom exceptions\nclass ValidationError(Exception):\n    pass\n\ndef validate_age(age):\n    if age < 0:\n        raise ValidationError("Age cannot be negative")</code></pre>',
                'tags': 'python, error handling, exceptions, try except',
                'meta_description': 'Learn Python error handling and exceptions',
                'meta_keywords': 'python exceptions, error handling, try except'
            },
        ]
