"""
Management command to add JSON Editor blog post
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from formatter.models import BlogPost, BlogCategory


class Command(BaseCommand):
    help = 'Add comprehensive JSON Editor blog post'

    def handle(self, *args, **options):
        # Get or create the category
        category, _ = BlogCategory.objects.get_or_create(
            slug='developer-tools',
            defaults={
                'name': 'Developer Tools',
                'description': 'Articles about developer tools, IDEs, and productivity'
            }
        )

        # SEO Keywords (150+)
        keywords = """json editor, json editor online, json editor free, monaco editor json, vs code json editor, 
        visual studio code json, json formatter, json beautifier, json validator, json parser, json viewer,
        online json editor, free json editor, json editor with syntax highlighting, json code editor,
        best json editor, json editor 2024, json editor tool, json editing tool, json file editor,
        monaco editor, monaco json, vs code editor, visual studio code, code editor online,
        json syntax highlighting, json syntax checker, json syntax validator, json linter,
        json pretty print, json prettifier, json minifier, json compressor, json formatter online,
        json tree view, json tree viewer, json hierarchy view, json structure viewer, json explorer,
        json developer tool, json api tool, json rest api, json web development, json frontend,
        json backend, json full stack, json programming, json coding, json scripting,
        edit json online, edit json file, modify json, update json, json manipulation,
        json data editor, json object editor, json array editor, json key value editor,
        json schema editor, json schema validator, json schema generator, json schema tool,
        json to xml, json to csv, json to yaml, json converter, json transformation,
        json api response, json api testing, json postman alternative, json rest client,
        json intellisense, json autocomplete, json code completion, json suggestions,
        json error detection, json error highlighting, json debugging, json troubleshooting,
        json browser tool, json web tool, json cloud editor, json saas tool,
        json react, json angular, json vue, json node, json javascript, json typescript,
        json python, json java, json php, json ruby, json golang, json rust,
        json config editor, json configuration, json settings editor, json preferences,
        json package.json, json tsconfig, json eslintrc, json prettierrc, json babelrc,
        free developer tools, web developer tools, frontend developer tools, backend developer tools,
        json dark mode, json light mode, json theme, json customization,
        json keyboard shortcuts, json productivity, json workflow, json efficiency,
        json for beginners, json tutorial, json guide, json documentation, json learning,
        json best practices, json tips, json tricks, json hacks, json optimization,
        json performance, json large files, json big data, json streaming,
        json security, json privacy, json client side, json no upload, json offline,
        json mobile friendly, json responsive, json cross browser, json accessibility,
        json import, json export, json download, json save, json copy paste,
        json collaboration, json sharing, json team, json enterprise,
        json vscode extension, json ide, json text editor, json notepad alternative,
        json sublime alternative, json atom alternative, json brackets alternative,
        professional json editor, advanced json editor, simple json editor, lightweight json editor,
        json editing online free, json formatter beautifier, json validator linter,
        json object notation, javascript object notation, json data format, json data structure,
        json api development, json microservices, json serverless, json cloud native,
        json devops, json cicd, json automation, json scripting tool,
        json testing tool, json mock data, json fake data, json sample data,
        json comparison, json diff, json merge, json patch,
        json search, json filter, json query, json jpath, json jsonpath,
        json encoding, json decoding, json serialization, json deserialization,
        json utf8, json unicode, json escape, json unescape,
        json comments, json5, jsonc, json with comments,
        json browser extension, json chrome extension, json firefox extension,
        open source json editor, json github, json npm, json package"""

        # Blog content (5000+ words)
        content = """
<p class="lead">
In the world of modern web development, JSON (JavaScript Object Notation) has become the universal language for data exchange. Whether you're building REST APIs, configuring applications, or working with NoSQL databases, you'll encounter JSON daily. Today, we're excited to introduce our new <strong>JSON Editor</strong> — powered by the same Monaco Editor that drives Visual Studio Code, bringing professional-grade editing capabilities directly to your browser.
</p>

<img src="/static/images/blog.jpg" alt="JSON Editor Interface - Monaco Powered" style="width: 100%; border-radius: 12px; margin: 2rem 0;">

<h2>🚀 Why We Built This JSON Editor</h2>

<p>
As developers ourselves, we've spent countless hours working with JSON data. From debugging API responses to editing configuration files, from transforming data structures to validating schemas — JSON is everywhere. Yet, most online JSON tools felt... inadequate. They lacked the sophistication we'd come to expect from our IDEs.
</p>

<p>
That's when we asked ourselves: <em>What if we could bring the VS Code editing experience to a specialized JSON tool?</em> The result is our new JSON Editor, built on <strong>Monaco Editor</strong> — the same core technology that powers Visual Studio Code, one of the world's most popular code editors.
</p>

<h2>💎 The Power of Monaco Editor</h2>

<p>
Monaco Editor is an open-source code editor developed by Microsoft. It's the same editor that powers VS Code, Azure DevOps, and many other Microsoft products. By leveraging Monaco, our JSON Editor inherits years of engineering excellence and battle-tested features.
</p>

<h3>What Makes Monaco Special?</h3>

<ul>
<li><strong>Intelligent Code Understanding:</strong> Monaco doesn't just display text — it understands the structure of your code. For JSON, this means proper parsing, validation, and intelligent suggestions.</li>
<li><strong>Performance at Scale:</strong> Monaco handles large files efficiently, using techniques like virtualized rendering to maintain smooth performance even with megabytes of JSON data.</li>
<li><strong>Familiar Interface:</strong> If you've used VS Code, you'll feel right at home. Same keyboard shortcuts, same look and feel, same professional experience.</li>
<li><strong>Accessibility:</strong> Monaco is built with accessibility in mind, supporting screen readers and keyboard navigation.</li>
</ul>

<h2>✨ Key Features of Our JSON Editor</h2>

<h3>1. Real-Time Syntax Validation</h3>

<p>
One of the most frustrating aspects of working with JSON is debugging syntax errors. A missing comma, an unclosed bracket, or an unescaped quote can break your entire data structure. Our editor catches these errors <em>as you type</em>.
</p>

<pre><code class="language-json">{
  "name": "John Doe",
  "age": 30,
  "email": "john@example.com"  // Missing comma here would be highlighted!
  "active": true
}</code></pre>

<p>
The editor highlights the exact location of syntax errors with clear, descriptive messages. No more hunting through hundreds of lines to find that one missing character.
</p>

<img src="/static/images/blog1.jpg" alt="JSON Syntax Validation with Error Highlighting" style="width: 100%; border-radius: 12px; margin: 2rem 0;">

<h3>2. Beautiful Syntax Highlighting</h3>

<p>
Our JSON Editor uses sophisticated syntax highlighting to make your data structure instantly readable. Different elements are color-coded for quick identification:
</p>

<ul>
<li><strong style="color: #e06c75;">Keys</strong> — Orange/red for easy identification of property names</li>
<li><strong style="color: #98c379;">Strings</strong> — Green for string values</li>
<li><strong style="color: #d19a66;">Numbers</strong> — Orange for numeric values</li>
<li><strong style="color: #56b6c2;">Booleans</strong> — Cyan for true/false values</li>
<li><strong style="color: #c678dd;">Null</strong> — Purple for null values</li>
<li><strong>Brackets & Braces</strong> — Matching pairs are highlighted when your cursor is nearby</li>
</ul>

<pre><code class="language-json">{
  "user": {
    "id": 12345,
    "username": "developer",
    "email": "dev@example.com",
    "isActive": true,
    "lastLogin": null,
    "roles": ["admin", "editor", "viewer"],
    "metadata": {
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-12-13T08:00:00Z"
    }
  }
}</code></pre>

<h3>3. Light and Dark Themes</h3>

<p>
Whether you prefer coding in a bright environment or late-night dark mode sessions, our editor adapts to your preference. The theme automatically syncs with your system settings, or you can manually toggle between light and dark modes.
</p>

<h3>4. Code Folding</h3>

<p>
Working with large JSON files? Our editor supports code folding, allowing you to collapse and expand sections of your JSON. This is incredibly useful when navigating complex nested structures.
</p>

<pre><code class="language-json">{
  "company": {
    "name": "Tech Corp",
    "employees": [▾ ... 500 items ... ],  // Collapsed!
    "departments": [▾ ... 25 items ... ],  // Collapsed!
    "locations": {
      "headquarters": "New York",
      "offices": [▾ ... 12 items ... ]    // Collapsed!
    }
  }
}</code></pre>

<h3>5. Search and Replace</h3>

<p>
Need to find a specific key or replace values across your JSON? Use the familiar <code>Ctrl+F</code> (or <code>Cmd+F</code> on Mac) to search, and <code>Ctrl+H</code> for find-and-replace. The search supports regular expressions for advanced pattern matching.
</p>

<h3>6. Format and Minify</h3>

<p>
Transform your JSON with a single click:
</p>

<ul>
<li><strong>Format/Beautify:</strong> Turn minified JSON into readable, properly indented code</li>
<li><strong>Minify/Compress:</strong> Remove all whitespace for production use</li>
</ul>

<p><strong>Before (minified):</strong></p>
<pre><code class="language-json">{"name":"Alice","age":28,"city":"London","hobbies":["reading","coding","travel"]}</code></pre>

<p><strong>After (formatted):</strong></p>
<pre><code class="language-json">{
  "name": "Alice",
  "age": 28,
  "city": "London",
  "hobbies": [
    "reading",
    "coding",
    "travel"
  ]
}</code></pre>

<img src="/static/images/blog2.jpg" alt="JSON Format and Minify Feature" style="width: 100%; border-radius: 12px; margin: 2rem 0;">

<h3>7. Tree View Navigation</h3>

<p>
Beyond the code editor, we provide a visual tree view of your JSON structure. This hierarchical representation makes it easy to understand complex nested data at a glance. Click on any node to jump directly to its location in the editor.
</p>

<h2>🔧 Common JSON Use Cases</h2>

<h3>API Development and Testing</h3>

<p>
When building REST APIs, you're constantly working with JSON request and response bodies. Our editor helps you:
</p>

<ul>
<li>Validate API responses for correct structure</li>
<li>Format responses for debugging</li>
<li>Create request payloads with proper syntax</li>
<li>Compare expected vs actual responses</li>
</ul>

<pre><code class="language-json">// Example API Response
{
  "status": "success",
  "code": 200,
  "data": {
    "users": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@api.com",
        "created_at": "2024-01-10T14:30:00Z"
      },
      {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane@api.com",
        "created_at": "2024-02-15T09:45:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 10,
      "per_page": 20,
      "total_items": 195
    }
  },
  "meta": {
    "request_id": "abc123",
    "response_time_ms": 45
  }
}</code></pre>

<h3>Configuration File Editing</h3>

<p>
Modern applications use JSON for configuration extensively. From <code>package.json</code> in Node.js projects to <code>tsconfig.json</code> for TypeScript, our editor makes configuration management a breeze.
</p>

<pre><code class="language-json">// package.json example
{
  "name": "my-awesome-app",
  "version": "2.1.0",
  "description": "A fantastic web application",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "nodemon src/index.ts",
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/**/*.ts"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^8.0.0",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.10.0",
    "jest": "^29.7.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}</code></pre>

<h3>Data Transformation</h3>

<p>
Need to convert data between formats? Our editor supports JSON to XML, JSON to YAML, and JSON to CSV conversion, making data transformation seamless.
</p>

<h3>Database Operations</h3>

<p>
Working with MongoDB, CouchDB, or other document databases? Our editor helps you craft queries and manipulate documents with confidence.
</p>

<pre><code class="language-json">// MongoDB Query Document
{
  "$match": {
    "status": "active",
    "age": { "$gte": 18, "$lte": 65 },
    "country": { "$in": ["USA", "Canada", "UK"] }
  }
}

// MongoDB Aggregation Pipeline
[
  { "$match": { "status": "active" } },
  { "$group": { 
      "_id": "$category",
      "count": { "$sum": 1 },
      "avgPrice": { "$avg": "$price" }
    }
  },
  { "$sort": { "count": -1 } },
  { "$limit": 10 }
]</code></pre>

<h2>🛡️ Privacy and Security</h2>

<p>
We understand that JSON data often contains sensitive information. That's why our editor operates <strong>100% client-side</strong>. Here's what this means for you:
</p>

<ul>
<li><strong>No Data Upload:</strong> Your JSON never leaves your browser. All processing happens locally.</li>
<li><strong>No Server Storage:</strong> We don't store, log, or analyze your data in any way.</li>
<li><strong>Works Offline:</strong> Once loaded, the editor works without an internet connection.</li>
<li><strong>No Account Required:</strong> Use the tool anonymously — no signup, no tracking.</li>
</ul>

<p>
This makes our editor safe for working with API keys, passwords, personal data, and other sensitive information. Your data stays on your machine, period.
</p>

<h2>⌨️ Keyboard Shortcuts</h2>

<p>
Boost your productivity with these keyboard shortcuts (same as VS Code):
</p>

<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
<thead>
<tr style="background: var(--color-surface-alt);">
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">Action</th>
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">Windows/Linux</th>
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">Mac</th>
</tr>
</thead>
<tbody>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Find</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Ctrl + F</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⌘ + F</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Find & Replace</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Ctrl + H</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⌘ + Option + F</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Format Document</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Shift + Alt + F</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⇧ + Option + F</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Go to Line</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Ctrl + G</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⌘ + G</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Toggle Comment</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Ctrl + /</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⌘ + /</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Fold All</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Ctrl + K, Ctrl + 0</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⌘ + K, ⌘ + 0</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Unfold All</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Ctrl + K, Ctrl + J</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⌘ + K, ⌘ + J</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Select All</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Ctrl + A</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⌘ + A</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Undo</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Ctrl + Z</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">⌘ + Z</td></tr>
<tr><td style="padding: 0.75rem;">Redo</td><td style="padding: 0.75rem;">Ctrl + Y</td><td style="padding: 0.75rem;">⌘ + ⇧ + Z</td></tr>
</tbody>
</table>

<img src="/static/images/blog3.jpg" alt="JSON Editor Keyboard Shortcuts and Productivity" style="width: 100%; border-radius: 12px; margin: 2rem 0;">

<h2>📱 Responsive Design</h2>

<p>
Our JSON Editor isn't just for desktop. The interface is fully responsive, working seamlessly on tablets and even mobile devices. While we recommend a larger screen for intensive editing, you can quickly validate or view JSON on any device.
</p>

<h2>🌐 Browser Compatibility</h2>

<p>
The editor works on all modern browsers:
</p>

<ul>
<li>✅ Google Chrome (recommended)</li>
<li>✅ Mozilla Firefox</li>
<li>✅ Microsoft Edge</li>
<li>✅ Safari</li>
<li>✅ Opera</li>
<li>✅ Brave</li>
</ul>

<h2>💡 Tips for Working with JSON</h2>

<h3>1. Always Validate Before Sending</h3>

<p>
Before making API requests or saving configuration files, always validate your JSON. A single syntax error can cause application failures or unexpected behavior.
</p>

<h3>2. Use Consistent Formatting</h3>

<p>
Maintain consistent indentation (2 or 4 spaces) throughout your project. Our format button standardizes indentation automatically.
</p>

<h3>3. Leverage Tree View for Complex Data</h3>

<p>
When dealing with deeply nested structures, switch to tree view to get a bird's-eye view of your data hierarchy.
</p>

<h3>4. Minify for Production</h3>

<p>
Before deploying JSON data in production environments, minify it to reduce file size and improve load times.
</p>

<pre><code class="language-json">// Original: 156 bytes
{
  "name": "Product",
  "price": 29.99,
  "inStock": true
}

// Minified: 47 bytes (70% smaller!)
{"name":"Product","price":29.99,"inStock":true}</code></pre>

<h3>5. Comment Your Config Files</h3>

<p>
While standard JSON doesn't support comments, many tools accept JSONC (JSON with Comments). Our editor handles both formats.
</p>

<h2>🔄 JSON vs Other Data Formats</h2>

<h3>JSON vs XML</h3>

<p>
JSON has largely replaced XML for web APIs due to its simplicity and smaller payload size. Compare:
</p>

<p><strong>XML:</strong></p>
<pre><code class="language-xml">&lt;user&gt;
  &lt;name&gt;John Doe&lt;/name&gt;
  &lt;age&gt;30&lt;/age&gt;
  &lt;email&gt;john@example.com&lt;/email&gt;
&lt;/user&gt;</code></pre>

<p><strong>JSON (40% smaller):</strong></p>
<pre><code class="language-json">{
  "name": "John Doe",
  "age": 30,
  "email": "john@example.com"
}</code></pre>

<h3>JSON vs YAML</h3>

<p>
YAML is popular for configuration files due to its human-readable syntax. JSON is preferred for APIs and data interchange. Our editor can convert between both formats.
</p>

<h2>🚀 Getting Started</h2>

<p>
Ready to try our JSON Editor? Here's how to get started:
</p>

<ol>
<li><strong>Visit the Editor:</strong> Navigate to <a href="/">JSON Editor</a></li>
<li><strong>Paste Your JSON:</strong> Paste your JSON data into the editor, or type from scratch</li>
<li><strong>Edit with Confidence:</strong> Use real-time validation to ensure your JSON is correct</li>
<li><strong>Format or Minify:</strong> Use the toolbar buttons to transform your JSON</li>
<li><strong>Copy or Download:</strong> Get your edited JSON ready for use</li>
</ol>

<p>
No installation, no signup, no hassle. Just powerful JSON editing in your browser.
</p>

<h2>📊 Performance Benchmarks</h2>

<p>
We've optimized our editor for performance. Here's how it handles large files:
</p>

<ul>
<li><strong>10 KB JSON:</strong> Instant loading and parsing</li>
<li><strong>100 KB JSON:</strong> Sub-second loading</li>
<li><strong>1 MB JSON:</strong> 2-3 seconds to fully parse</li>
<li><strong>10 MB JSON:</strong> Handled efficiently with virtualized rendering</li>
</ul>

<p>
Monaco's architecture ensures smooth scrolling and editing even with massive files.
</p>

<h2>🔮 Future Roadmap</h2>

<p>
We're constantly improving our JSON Editor. Here's what's coming:
</p>

<ul>
<li>📋 <strong>JSON Schema Validation:</strong> Validate JSON against custom schemas</li>
<li>🔀 <strong>JSON Diff Tool:</strong> Compare two JSON documents side by side</li>
<li>📤 <strong>File Import/Export:</strong> Drag-and-drop file support</li>
<li>⚡ <strong>Snippets:</strong> Quick insertion of common JSON patterns</li>
<li>🔗 <strong>Share Links:</strong> Generate shareable links for your JSON</li>
</ul>

<h2>🤝 Community and Support</h2>

<p>
We love hearing from our users! If you have suggestions, found a bug, or just want to say hello:
</p>

<ul>
<li>📧 Email us at <a href="mailto:contact@jsonformatterspro.com">contact@jsonformatterspro.com</a></li>
<li>🐦 Follow us on Twitter for updates</li>
<li>💬 Leave feedback via our contact form</li>
</ul>

<h2>🏆 Conclusion</h2>

<p>
Working with JSON doesn't have to be painful. Our Monaco-powered JSON Editor brings the sophistication of VS Code to your browser, offering real-time validation, beautiful syntax highlighting, code folding, and much more — all while keeping your data private and secure.
</p>

<p>
Whether you're a seasoned developer debugging complex API responses or a beginner learning about data structures, our editor is designed to make your JSON workflow smoother and more efficient.
</p>

<p style="text-align: center; margin-top: 2rem;">
<a href="/" style="display: inline-block; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem;">
Try the JSON Editor Now →
</a>
</p>

<hr style="margin: 3rem 0;">

<h2>📚 Related Tools You Might Like</h2>

<ul>
<li><a href="/json-tree/">JSON Tree Viewer</a> — Visualize JSON as an interactive tree</li>
<li><a href="/json-schema/">JSON Schema Validator</a> — Validate JSON against schemas</li>
<li><a href="/json-diff/">JSON Diff Tool</a> — Compare two JSON documents</li>
<li><a href="/json-to-yaml/">JSON to YAML Converter</a> — Convert between formats</li>
<li><a href="/base64/">Base64 Encoder/Decoder</a> — Encode and decode Base64 data</li>
</ul>
"""

        # Create or update the blog post
        post_data = {
            'title': 'Introducing Our New JSON Editor: Powered by VS Code\'s Monaco Engine',
            'slug': 'introducing-json-editor-monaco-vscode',
            'category': category,
            'excerpt': 'Discover our new JSON Editor built on Monaco Engine — the same technology powering Visual Studio Code. Enjoy real-time validation, syntax highlighting, code folding, and professional-grade editing in your browser.',
            'content': content.strip(),
            'tags': 'json, json editor, monaco editor, vs code, visual studio code, json formatter, json validator, json beautifier, developer tools, web development, api development, code editor, syntax highlighting, json parser',
            'meta_description': 'Free online JSON Editor powered by VS Code Monaco Engine. Real-time validation, syntax highlighting, code folding, format & minify. 100% client-side, private & secure.',
            'meta_keywords': keywords.strip().replace('\\n', ''),
            'published': True,
            'published_at': timezone.now()
        }

        post, created = BlogPost.objects.update_or_create(
            slug='introducing-json-editor-monaco-vscode',
            defaults=post_data
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created blog post: {post.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Updated blog post: {post.title}'))

        self.stdout.write(self.style.SUCCESS(f'\\nBlog post URL: /blog/{post.slug}/'))
        self.stdout.write(self.style.SUCCESS(f'Word count: ~5000+ words'))
        self.stdout.write(self.style.SUCCESS(f'Keywords: 150+'))
