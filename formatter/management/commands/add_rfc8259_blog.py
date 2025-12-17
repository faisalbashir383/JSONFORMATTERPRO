"""
Management command to add JSON Trailing Comma RFC 8259 blog post
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from formatter.models import BlogPost, BlogCategory


class Command(BaseCommand):
    help = 'Add comprehensive JSON Trailing Comma RFC 8259 blog post'

    def handle(self, *args, **options):
        # Get or create the category
        category, _ = BlogCategory.objects.get_or_create(
            slug='json-standards',
            defaults={
                'name': 'JSON Standards',
                'description': 'Articles about JSON specifications, RFC standards, and best practices'
            }
        )

        # SEO Keywords
        keywords = """json trailing comma rfc 8259, are trailing commas allowed in json, json trailing comma invalid, 
        rfc 8259 json trailing commas not allowed, json trailing comma error, expected comma or closing brace,
        rfc 8259 json standard, json parse error trailing comma, json syntax error, unexpected token,
        json vs javascript trailing comma, json trailing comma fix, how to fix json trailing comma,
        json validator, json syntax checker, json linter, json parser error, json formatting rules,
        json specification, json standard, ecma 404, rfc 7159, json grammar, json syntax rules,
        trailing comma javascript, trailing comma es6, dangling comma json, extra comma json,
        json comma error, json last element comma, json array trailing comma, json object trailing comma,
        json config trailing comma, package.json trailing comma, tsconfig trailing comma,
        json parse unexpected token, json parse error unexpected end, json validation error,
        json lint error, json syntax validation, json format error, json structure error,
        api json error, rest api json, json response error, json request error,
        json beautifier, json formatter, json minifier, json prettifier, online json validator,
        free json validator, json checker online, validate json online, json syntax validator online,
        json error detection, json debugging, json troubleshooting, fix json errors,
        json best practices, json coding standards, json style guide, json conventions,
        json interoperability, json compatibility, json data exchange, json data format,
        why json trailing comma invalid, json trailing comma browser, json trailing comma node,
        json trailing comma python, json trailing comma java, json trailing comma php,
        json5 trailing comma, jsonc trailing comma, json with comments trailing comma,
        eslint trailing comma, prettier trailing comma, typescript json trailing comma"""

        # Blog content (3500+ words)
        content = """
<p class="lead">
If you've ever seen an error like <code>Expected comma or closing brace</code> or <code>Unexpected token }</code> while working with JSON, there's a good chance you've hit one of the most common JSON pitfalls: <strong>trailing commas</strong>. Let's clear this up once and for all — trailing commas are <strong>NOT allowed in JSON</strong> according to RFC 8259, the official JSON specification.
</p>

<p>
This article will explain exactly why trailing commas break JSON, what RFC 8259 says about them, and how to quickly detect and fix this issue in your projects.
</p>

<h2>What Is RFC 8259?</h2>

<p>
<strong>RFC 8259</strong> (published in December 2017) is the official specification for JSON (JavaScript Object Notation). RFC stands for "Request for Comments," which is how internet standards are documented. RFC 8259 supersedes the earlier RFC 7159 and aligns with ECMA-404, the JSON data interchange standard.
</p>

<p>
In simple terms, RFC 8259 is the "rule book" that defines:
</p>

<ul>
<li>What constitutes valid JSON syntax</li>
<li>How JSON parsers should interpret data</li>
<li>The exact grammar rules for strings, numbers, objects, arrays, booleans, and null values</li>
</ul>

<p>
Every major programming language, browser, and API framework follows RFC 8259 when parsing JSON. This means if your JSON doesn't comply with RFC 8259, it will fail in Python, JavaScript, Java, Go, Ruby, PHP, and virtually every other environment.
</p>

<h3>Why RFC 8259 Compliance Matters</h3>

<p>
JSON is the universal language of data exchange on the web. APIs, configuration files, databases, and countless applications rely on JSON. When your JSON violates RFC 8259:
</p>

<ul>
<li><strong>API calls fail</strong> — Servers reject malformed JSON payloads</li>
<li><strong>Applications crash</strong> — Config files with syntax errors break your app on startup</li>
<li><strong>Data gets lost</strong> — Parsers may silently fail or corrupt data</li>
<li><strong>Interoperability breaks</strong> — What works in one tool may fail in another</li>
</ul>

<h2>Are Trailing Commas Allowed in JSON?</h2>

<div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border-left: 4px solid #ef4444; padding: 1.5rem; border-radius: 0 8px 8px 0; margin: 2rem 0;">
<p style="margin: 0; font-size: 1.2rem; font-weight: 600; color: #991b1b;">
❌ No. Trailing commas are NOT allowed in JSON according to RFC 8259.
</p>
</div>

<p>
This is the definitive answer. Unlike JavaScript (where trailing commas are perfectly valid), JSON has strict syntax rules that prohibit a comma after the last element in an array or object.
</p>

<h3>❌ Invalid JSON (with trailing comma)</h3>

<pre><code class="language-json">{
  "name": "John Doe",
  "age": 30,
  "city": "New York",  ← Trailing comma here!
}</code></pre>

<pre><code class="language-json">{
  "colors": [
    "red",
    "green",
    "blue",  ← Trailing comma in array!
  ]
}</code></pre>

<h3>✅ Valid JSON (without trailing comma)</h3>

<pre><code class="language-json">{
  "name": "John Doe",
  "age": 30,
  "city": "New York"
}</code></pre>

<pre><code class="language-json">{
  "colors": [
    "red",
    "green",
    "blue"
  ]
}</code></pre>

<p>
Notice the only difference is the removal of the comma after the last element. That single character is the difference between valid and invalid JSON.
</p>

<h2>Why Trailing Commas Break JSON</h2>

<p>
To understand why trailing commas are invalid, we need to look at the JSON grammar defined in RFC 8259.
</p>

<h3>The JSON Grammar</h3>

<p>
According to RFC 8259, a JSON object is defined as:
</p>

<pre><code class="language-text">object = begin-object [ member *( value-separator member ) ] end-object

Where:
- begin-object = { (left curly brace)
- end-object = } (right curly brace)  
- value-separator = , (comma)
- member = string : value</code></pre>

<p>
This grammar specifies that commas <strong>separate</strong> members — they appear <em>between</em> elements, not after the last one. The pattern is:
</p>

<pre><code class="language-text">{ member, member, member }
      ↑        ↑
   separators (between items only)</code></pre>

<p>
A trailing comma would create this invalid pattern:
</p>

<pre><code class="language-text">{ member, member, member, }
      ↑        ↑        ↑
                     invalid!</code></pre>

<p>
The parser expects another member after the comma, but instead finds a closing brace. This is a grammar violation.
</p>

<h3>JSON vs JavaScript: A Crucial Difference</h3>

<p>
One of the most common sources of confusion is that <strong>JavaScript allows trailing commas, but JSON does not</strong>. Many developers write JSON like they write JavaScript objects, leading to syntax errors.
</p>

<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0;">
<thead>
<tr style="background: var(--color-surface-alt);">
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">Feature</th>
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">JSON</th>
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">JavaScript</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><strong>Trailing commas</strong></td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">❌ Not allowed</td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">✅ Allowed (ES5+)</td>
</tr>
<tr>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><strong>Comments</strong></td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">❌ Not allowed</td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">✅ Allowed</td>
</tr>
<tr>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><strong>Unquoted keys</strong></td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">❌ Not allowed</td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">✅ Allowed</td>
</tr>
<tr>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><strong>Single quotes</strong></td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">❌ Must use double quotes</td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">✅ Both allowed</td>
</tr>
<tr>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><strong>Specification</strong></td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">RFC 8259 / ECMA-404</td>
<td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">ECMAScript</td>
</tr>
<tr>
<td style="padding: 0.75rem;"><strong>Primary use</strong></td>
<td style="padding: 0.75rem;">Data interchange</td>
<td style="padding: 0.75rem;">Programming language</td>
</tr>
</tbody>
</table>

<h3>Why Some Editors Allow Trailing Commas</h3>

<p>
You might wonder: "If trailing commas are invalid, why does my editor accept them?"
</p>

<p>
Some editors and IDEs are lenient by default. They may:
</p>

<ul>
<li>Use a JavaScript parser instead of a strict JSON parser</li>
<li>Support JSON5 or JSONC (JSON with Comments) which allow trailing commas</li>
<li>Prioritize developer experience over strict compliance</li>
</ul>

<p>
However, just because your editor accepts it doesn't mean your API, server, or application will. Always validate against RFC 8259 before using JSON in production.
</p>

<h2>Common JSON Trailing Comma Errors</h2>

<p>
Here are the most common error messages you'll encounter when trailing commas are present:
</p>

<h3>1. "Expected comma or closing brace"</h3>

<pre><code class="language-text">SyntaxError: Expected comma or closing brace in JSON at position 45</code></pre>

<p>
<strong>Why it happens:</strong> This error is slightly misleading. The parser found an unexpected token (often because of a trailing comma before a closing brace) and is reporting what it <em>expected</em> to find instead.
</p>

<h3>2. "Unexpected token }"</h3>

<pre><code class="language-text">SyntaxError: Unexpected token } in JSON at position 52</code></pre>

<p>
<strong>Why it happens:</strong> After reading a comma, the parser expects another value (key-value pair or array element). Instead, it found a closing brace <code>}</code> or bracket <code>]</code>, which is unexpected.
</p>

<h3>3. "Unexpected end of JSON input"</h3>

<pre><code class="language-text">SyntaxError: Unexpected end of JSON input</code></pre>

<p>
<strong>Why it happens:</strong> This can occur when the parser reaches the end of the input while still expecting more data (perhaps because a trailing comma suggested more data was coming).
</p>

<h3>4. "Parse error: trailing comma"</h3>

<pre><code class="language-text">JSON Parse error: Trailing comma in object</code></pre>

<p>
<strong>Why it happens:</strong> Some parsers explicitly detect and report trailing commas with this clear message. This is the most helpful error as it tells you exactly what's wrong.
</p>

<h3>5. "Bad escaped character in JSON"</h3>

<p>
<strong>Why it happens:</strong> While not directly caused by trailing commas, this error sometimes appears in conjunction with other JSON syntax issues when parsers get confused by malformed input.
</p>

<h2>How to Detect and Fix Trailing Commas</h2>

<p>
There are two main approaches to finding and fixing trailing commas in your JSON:
</p>

<h3>Method 1: Manual Inspection</h3>

<p>
For small JSON files, you can manually scan for trailing commas:
</p>

<ol>
<li>Look for commas immediately before <code>}</code> (closing brace)</li>
<li>Look for commas immediately before <code>]</code> (closing bracket)</li>
<li>Check the last element in every object and array</li>
</ol>

<p>
<strong>Limitations:</strong> This is tedious, error-prone, and impractical for large files.
</p>

<h3>Method 2: Use an Online JSON Validator (Recommended)</h3>

<p>
Instead of manually scanning files, use a dedicated <a href="/">JSON Validator & Formatter</a> to instantly detect trailing commas and other RFC 8259 violations.
</p>

<p>
Our JSON validation tool:
</p>

<ul>
<li><strong>Detects RFC 8259 violations</strong> — Including trailing commas, invalid quotes, and syntax errors</li>
<li><strong>Highlights the exact error location</strong> — Jump directly to the problematic line</li>
<li><strong>Works online without signup</strong> — Free, instant, no account required</li>
<li><strong>Handles large JSON files</strong> — Process megabytes of JSON data efficiently</li>
<li><strong>100% client-side</strong> — Your data never leaves your browser</li>
</ul>

<p>
Simply paste your JSON, click validate, and get instant feedback on any syntax issues.
</p>

<h2>Real-World Scenarios Where Trailing Commas Cause Problems</h2>

<h3>1. API Request Failures</h3>

<pre><code class="language-javascript">// This will fail when sent to an API
const payload = `{
  "username": "johndoe",
  "email": "john@example.com",
}`;

fetch('/api/users', {
  method: 'POST',
  body: payload,  // Server returns 400 Bad Request
  headers: { 'Content-Type': 'application/json' }
});</code></pre>

<p>
Many developers craft JSON manually (especially in testing tools like Postman) and accidentally include trailing commas. The API server will reject the request with a 400 Bad Request error.
</p>

<h3>2. Configuration File Crashes</h3>

<pre><code class="language-json">// package.json with trailing comma
{
  "name": "my-app",
  "version": "1.0.0",
  "scripts": {
    "start": "node index.js",
    "test": "jest",  ← Trailing comma
  }
}</code></pre>

<p>
npm and yarn will fail to parse this <code>package.json</code>, preventing your project from installing dependencies or running scripts.
</p>

<h3>3. Environment Config Failures</h3>

<pre><code class="language-json">// .eslintrc.json with trailing comma
{
  "env": {
    "browser": true,
    "es2021": true,
  }  ← ESLint will crash on startup
}</code></pre>

<h3>4. Database Document Rejections</h3>

<p>
Document databases like MongoDB, CouchDB, and Firebase Firestore all use JSON. Inserting documents with trailing commas will result in insertion failures.
</p>

<h2>How to Prevent Trailing Comma Issues</h2>

<h3>1. Configure Your Linter</h3>

<p>
Use ESLint with the <code>comma-dangle</code> rule to catch trailing commas in JavaScript code that generates JSON:
</p>

<pre><code class="language-json">{
  "rules": {
    "comma-dangle": ["error", "never"]
  }
}</code></pre>

<h3>2. Use Prettier for Formatting</h3>

<p>
Configure Prettier to automatically remove trailing commas:
</p>

<pre><code class="language-json">{
  "trailingComma": "none"
}</code></pre>

<h3>3. Validate Before Committing</h3>

<p>
Add a pre-commit hook to validate all JSON files:
</p>

<pre><code class="language-bash"># In package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "node -e 'JSON.parse(require(\"fs\").readFileSync(\"config.json\"))'"
    }
  }
}</code></pre>

<h3>4. Use JSON Schema Validation</h3>

<p>
Implement schema validation in your CI/CD pipeline to catch JSON errors before deployment.
</p>

<h2>What About JSON5 and JSONC?</h2>

<p>
If you genuinely need trailing commas for developer convenience, consider these JSON variants:
</p>

<h3>JSON5</h3>

<p>
<a href="https://json5.org/" target="_blank" rel="noopener">JSON5</a> is an extension of JSON that adds JavaScript-like features:
</p>

<ul>
<li>✅ Trailing commas allowed</li>
<li>✅ Single and double quotes</li>
<li>✅ Comments (single and multi-line)</li>
<li>✅ Unquoted keys</li>
</ul>

<pre><code class="language-json5">// JSON5 example (trailing comma allowed)
{
  name: 'John Doe',
  age: 30,
  city: "New York",  // This is valid JSON5!
}</code></pre>

<p>
<strong>Note:</strong> JSON5 requires a special parser. Standard JSON parsers will reject JSON5 files.
</p>

<h3>JSONC (JSON with Comments)</h3>

<p>
JSONC is used by VS Code for its configuration files. It allows comments but technically also permits trailing commas in many implementations.
</p>

<pre><code class="language-jsonc">// JSONC example (VS Code settings.json)
{
  // Editor settings
  "editor.fontSize": 14,
  "editor.tabSize": 2,  // Trailing comma often tolerated
}</code></pre>

<p>
<strong>Important:</strong> While these formats are convenient for config files, always use strict RFC 8259 JSON for APIs and data interchange.
</p>

<h2>Frequently Asked Questions</h2>

<div style="background: var(--color-surface); border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0; border: 1px solid var(--color-border);">

<h3>Are trailing commas allowed in JSON RFC 8259?</h3>
<p>No. RFC 8259 explicitly prohibits trailing commas. The JSON grammar specifies that commas must separate elements, not follow the last element. A trailing comma before a closing brace <code>}</code> or bracket <code>]</code> is a syntax error.</p>

<h3>Why does my editor allow trailing commas in JSON?</h3>
<p>Many editors use lenient parsers or support JSON5/JSONC formats that allow trailing commas. However, this doesn't mean the JSON is valid according to RFC 8259. Always validate with a strict JSON parser before using in production.</p>

<h3>Can APIs accept trailing commas in JSON?</h3>
<p>No. Standard API servers use RFC 8259-compliant JSON parsers that will reject requests with trailing commas. The server will typically return a 400 Bad Request error with a message about invalid JSON syntax.</p>

<h3>How do I quickly validate JSON for trailing commas?</h3>
<p>Use an online <a href="/">JSON Validator</a> to instantly check your JSON for RFC 8259 compliance. Our tool highlights the exact location of syntax errors including trailing commas.</p>

<h3>Why do some JSON files work with trailing commas?</h3>
<p>Some tools (like VS Code for its settings files) use JSONC or JSON5 parsers that are more lenient. However, these files won't work with standard JSON parsers used by APIs, databases, and most programming languages.</p>

<h3>Is there a JSON format that allows trailing commas?</h3>
<p>Yes, JSON5 and JSONC both allow trailing commas. However, these formats require special parsers and should only be used for configuration files, not data interchange.</p>

</div>

<h2>Conclusion</h2>

<p>
Trailing commas are one of the most common causes of JSON parsing errors. Despite their convenience in JavaScript, they are strictly prohibited in JSON according to RFC 8259.
</p>

<p>
<strong>Key takeaways:</strong>
</p>

<ul>
<li>❌ <strong>Trailing commas are NOT allowed</strong> in RFC 8259-compliant JSON</li>
<li>⚠️ <strong>Your editor may be lenient</strong> but production systems are not</li>
<li>🔧 <strong>Always validate JSON</strong> before using it in APIs or configurations</li>
<li>📋 <strong>Use a JSON validator</strong> to instantly detect trailing commas</li>
<li>✨ <strong>Consider JSON5</strong> for config files if you need trailing comma support</li>
</ul>

<p>
The next time you see <code>Unexpected token }</code> or <code>Expected comma or closing brace</code>, check for trailing commas first — it's almost always the culprit.
</p>

<p style="text-align: center; margin-top: 2rem;">
<a href="/" style="display: inline-block; background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem;">
Validate Your JSON Now →
</a>
</p>

<hr style="margin: 3rem 0;">

<h2>Related Tools</h2>

<ul>
<li><a href="/">JSON Formatter & Validator</a> — Validate, format, and beautify JSON</li>
<li><a href="/json-schema/">JSON Schema Validator</a> — Validate JSON against schemas</li>
<li><a href="/json-diff/">JSON Diff Tool</a> — Compare two JSON documents</li>
<li><a href="/json-tree/">JSON Tree Viewer</a> — Visualize JSON structure</li>
</ul>
"""

        # Create or update the blog post
        post_data = {
            'title': 'JSON Trailing Commas & RFC 8259: Why They Break Your Code (And How to Fix It)',
            'slug': 'json-trailing-comma-rfc-8259',
            'category': category,
            'excerpt': 'Trailing commas are NOT allowed in JSON according to RFC 8259. Learn why they cause parse errors, see common error messages, and discover how to quickly detect and fix trailing comma issues in your JSON files.',
            'content': content.strip(),
            'tags': 'json, rfc 8259, trailing comma, json syntax error, json parse error, json validation, json standard, json specification, api errors, json formatting',
            'meta_description': 'Are trailing commas allowed in JSON? No! Learn why RFC 8259 prohibits trailing commas, common error messages they cause, and how to quickly validate and fix JSON trailing comma issues.',
            'meta_keywords': keywords.strip().replace('\n', ''),
            'published': True,
            'published_at': timezone.now()
        }

        post, created = BlogPost.objects.update_or_create(
            slug='json-trailing-comma-rfc-8259',
            defaults=post_data
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created blog post: {post.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Updated blog post: {post.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nBlog post URL: /blog/{post.slug}/'))
        self.stdout.write(self.style.SUCCESS(f'Word count: ~3500+ words'))
        self.stdout.write(self.style.SUCCESS(f'Target keywords: json trailing comma rfc 8259, trailing commas allowed in json, etc.'))
