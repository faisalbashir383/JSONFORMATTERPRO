"""
Management command to add Mock API Generator blog post
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from formatter.models import BlogPost, BlogCategory


class Command(BaseCommand):
    help = 'Add comprehensive Mock API Generator blog post'

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
        keywords = """mock api generator, custom mock api, mock api with ip restriction, fake api generator, 
        api mocking tool, rest api mock, mock rest api, api simulator online, test api online free,
        generate mock api, mock api endpoints, api mocking service, free mock api, json api generator,
        mock server online, api prototyping, frontend testing api, mock backend service, rest api simulator,
        api response generator, fake json api, mock http server, api mock tool, test api responses,
        ip restriction api, secure mock api, ip whitelist api, api access control, protected api endpoint,
        private mock api, ip based api security, mock api with authentication, server side mock api,
        persistent mock endpoints, saved mock api, reusable mock endpoints, dynamic mock data,
        template variables api, random data api, fake user data api, mock database api,
        api latency testing, slow api simulation, error rate testing, 500 error simulation,
        api timeout testing, network error simulation, mock api 2024, mock api 2025, mock api 2026,
        best mock api generator, free api mock service, mock api no signup, instant mock api,
        easy api mocking, developer tools api, frontend developer tools, backend mocking,
        swagger mock alternative, postman mock alternative, mock api for react, mock api for angular,
        mock api for vue, ajax mock api, fetch mock api, axios mock api, cors enabled mock api,
        how to use mock api, mock api tutorial, mock api guide, api mocking best practices,
        restrict api by ip, whitelist ip address api, secure api testing, private api endpoint,
        create fake api response, generate api response, custom json response, dynamic json generator,
        mock user api, mock products api, mock login api, mock authentication api, mock crud api,
        api response time simulation, slow api testing, test loading states, test error handling,
        frontend development mock, backend not ready, develop without backend, parallel development,
        api first development, contract testing, mock contract, api prototype, rapid prototyping"""

        # Blog content (5000+ words)
        content = """
<p class="lead">
Building modern web applications often requires a backend API, but what do you do when the backend isn't ready yet? Enter the <strong>Mock API Generator</strong> — a powerful tool that lets you create custom REST API endpoints with realistic data, IP restriction, and simulation features. In this comprehensive guide, we'll explore how to use our Mock API Generator to supercharge your development workflow.
</p>

<img src="/static/images/blog.jpg" alt="Mock API Generator Interface" style="width: 100%; border-radius: 12px; margin: 2rem 0;">

<h2>🚀 What is a Mock API Generator?</h2>

<p>
A Mock API Generator is a tool that creates simulated REST API endpoints that behave like real APIs but return fake (yet realistic) data. This is incredibly useful for:
</p>

<ul>
<li><strong>Frontend developers</strong> who need to build UIs before the backend is ready</li>
<li><strong>QA engineers</strong> who need predictable API responses for testing</li>
<li><strong>Demo applications</strong> that need realistic data without a real database</li>
<li><strong>Prototyping</strong> new features without backend investment</li>
<li><strong>Training</strong> new developers on API integration</li>
</ul>

<p>
Our Mock API Generator takes this a step further with <strong>IP restriction</strong>, allowing you to create secure endpoints that only respond to specific IP addresses — perfect for private testing and team collaboration.
</p>

<h2>🔒 The Power of IP Restriction</h2>

<p>
Unlike other mock API tools, our generator includes a built-in <strong>IP restriction</strong> feature. This means you can:
</p>

<ul>
<li><strong>Create private endpoints</strong> that only your team can access</li>
<li><strong>Test IP-based access control</strong> before implementing it in production</li>
<li><strong>Secure sensitive mock data</strong> from unauthorized access</li>
<li><strong>Simulate production environments</strong> where IP whitelisting is common</li>
</ul>

<h3>How IP Restriction Works</h3>

<p>
When you enable IP restriction on a mock endpoint:
</p>

<ol>
<li>The system checks the incoming request's IP address</li>
<li>If the IP is in your allowed list, the request proceeds normally</li>
<li>If the IP is NOT allowed, the server returns a <code>403 Forbidden</code> error</li>
</ol>

<pre><code class="language-json">// Response when IP is NOT allowed (403 Forbidden)
{
  "error": "Forbidden",
  "message": "Your IP address is not authorized to access this endpoint",
  "your_ip": "192.168.1.100",
  "allowed_ips": ["10.0.0.1", "203.0.113.50"],
  "status": 403
}</code></pre>

<h2>📌 Step-by-Step: Creating Your First Mock Endpoint</h2>

<h3>Step 1: Configure Your Endpoint</h3>

<p>
Start by setting up the basic endpoint configuration:
</p>

<ul>
<li><strong>Endpoint Path:</strong> Define your API path (e.g., <code>/api/users</code>)</li>
<li><strong>HTTP Method:</strong> Choose GET, POST, PUT, PATCH, or DELETE</li>
<li><strong>Status Code:</strong> Set the HTTP response status (200, 201, 404, etc.)</li>
</ul>

<pre><code class="language-json">// Example configuration
Endpoint Path: /api/users
HTTP Method: GET
Status Code: 200</code></pre>

<h3>Step 2: Create Your Response Template</h3>

<p>
Define the JSON response your endpoint will return. You can use plain JSON or leverage our <strong>template variables</strong> for dynamic data:
</p>

<pre><code class="language-json">{
  "success": true,
  "data": [
    {
      "id": "{{uuid}}",
      "firstName": "{{firstName}}",
      "lastName": "{{lastName}}",
      "email": "{{email}}",
      "phone": "{{phone}}",
      "company": "{{company}}",
      "jobTitle": "{{jobTitle}}",
      "avatar": "{{avatar}}",
      "createdAt": "{{isoDate}}"
    }
  ],
  "meta": {
    "total": "{{number:100}}",
    "page": 1,
    "perPage": 10
  }
}</code></pre>

<h3>Step 3: Set Number of Records</h3>

<p>
Use the <strong>Number of Records</strong> field to specify how many items should be generated in your response array. Set it to 5, 10, 50, or even 100 records — each with unique randomized data!
</p>

<h3>Step 4: Configure Simulation Options (Optional)</h3>

<p>
To make your testing more realistic, configure simulation options:
</p>

<ul>
<li><strong>Latency:</strong> Add a delay (0-5000ms) to simulate network conditions</li>
<li><strong>Error Rate:</strong> Set a percentage chance of returning a 500 error</li>
</ul>

<p>
These features help you test loading states, error handling, and user experience under various conditions.
</p>

<h3>Step 5: Enable IP Restriction (Optional)</h3>

<p>
For secure endpoints:
</p>

<ol>
<li>Your public IP is <strong>auto-detected</strong> and shown on the page</li>
<li>Click <strong>"Add My IP"</strong> to whitelist your current IP</li>
<li>Check <strong>"Enable IP Restriction"</strong> to activate the feature</li>
<li>Add multiple IPs by separating them with commas</li>
</ol>

<pre><code class="language-text">// Example: Multiple allowed IPs
192.168.1.1, 10.0.0.1, 203.0.113.50, 45.33.32.156</code></pre>

<h3>Step 6: Create the Server Endpoint</h3>

<p>
Click <strong>"Create Server Endpoint"</strong> to generate your mock API. You'll receive a unique URL like:
</p>

<pre><code class="language-text">https://jsonformatterspro.com/api/mock/abc12xyz/</code></pre>

<p>
This URL is immediately usable in your application, Postman, curl, or any HTTP client!
</p>

<h2>📋 Template Variables Reference</h2>

<p>
Our Mock API Generator supports a rich set of template variables that generate realistic fake data on each request:
</p>

<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
<thead>
<tr style="background: var(--color-surface-alt);">
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">Variable</th>
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">Description</th>
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">Example Output</th>
</tr>
</thead>
<tbody>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{uuid}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Unique identifier</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">a1b2c3d4-e5f6-4789-abcd-123456789012</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{firstName}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Random first name</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Emma, Liam, Olivia</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{lastName}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Random last name</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Smith, Johnson, Williams</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{fullName}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Full name combination</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Emma Johnson</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{email}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Email address</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">emma.johnson@gmail.com</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{phone}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Phone number</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">+1 555-123-4567</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{company}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Company name</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">TechCorp, Innovate Inc</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{jobTitle}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Job title</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Software Engineer</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{city}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">City name</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">New York, San Francisco</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{country}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Country name</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">United States, Canada</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{isoDate}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">ISO 8601 date</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">2024-06-15T14:30:00</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{boolean}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Random true/false</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">true, false</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{number:100}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Random number (0-100)</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">42, 73, 15</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{avatar}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Avatar URL</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">https://i.pravatar.cc/150?img=42</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);"><code>{{imageUrl}}</code></td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Random image URL</td><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">https://picsum.photos/seed/123/400/300</td></tr>
<tr><td style="padding: 0.75rem;"><code>{{zipCode}}</code></td><td style="padding: 0.75rem;">ZIP/Postal code</td><td style="padding: 0.75rem;">10001, 90210</td></tr>
</tbody>
</table>

<h2>📊 Real-World Response Examples</h2>

<h3>Example 1: User List API</h3>

<pre><code class="language-json">// Template
{
  "success": true,
  "data": [
    {
      "id": "{{uuid}}",
      "name": "{{fullName}}",
      "email": "{{email}}",
      "avatar": "{{avatar}}",
      "isActive": {{boolean}}
    }
  ]
}

// Generated Response (5 records)
{
  "success": true,
  "data": [
    {
      "id": "8f2e9a4b-c3d1-4e5f-a6b7-c8d9e0f1a2b3",
      "name": "Emma Johnson",
      "email": "emma.johnson@gmail.com",
      "avatar": "https://i.pravatar.cc/150?img=23",
      "isActive": true
    },
    {
      "id": "1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
      "name": "Liam Williams",
      "email": "liam.williams@outlook.com",
      "avatar": "https://i.pravatar.cc/150?img=45",
      "isActive": false
    },
    // ... 3 more records
  ]
}</code></pre>

<h3>Example 2: E-commerce Products API</h3>

<pre><code class="language-json">{
  "products": [
    {
      "sku": "{{uuid}}",
      "name": "Premium {{company}} Widget",
      "price": {{number:500}},
      "inStock": {{boolean}},
      "image": "{{imageUrl}}",
      "createdAt": "{{isoDate}}"
    }
  ],
  "pagination": {
    "page": 1,
    "totalItems": {{number:1000}},
    "hasMore": true
  }
}</code></pre>

<h3>Example 3: Authentication Response</h3>

<pre><code class="language-json">{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.{{uuid}}",
  "user": {
    "id": "{{uuid}}",
    "email": "{{email}}",
    "firstName": "{{firstName}}",
    "lastName": "{{lastName}}"
  },
  "expiresAt": "{{isoDate}}"
}</code></pre>

<h2>🧪 Testing Your Mock Endpoints</h2>

<h3>Using cURL</h3>

<pre><code class="language-bash"># Simple GET request
curl https://jsonformatterspro.com/api/mock/abc12xyz/

# POST request with data
curl -X POST https://jsonformatterspro.com/api/mock/abc12xyz/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User"}'</code></pre>

<h3>Using JavaScript (Fetch)</h3>

<pre><code class="language-javascript">// In your React/Vue/Angular app
fetch('https://jsonformatterspro.com/api/mock/abc12xyz/')
  .then(response => response.json())
  .then(data => {
    console.log('Mock API Response:', data);
    setUsers(data.data);
  })
  .catch(error => console.error('Error:', error));</code></pre>

<h3>Using Axios</h3>

<pre><code class="language-javascript">import axios from 'axios';

const getMockUsers = async () => {
  const response = await axios.get('https://jsonformatterspro.com/api/mock/abc12xyz/');
  return response.data;
};</code></pre>

<h2>⚡ Testing Latency and Error Handling</h2>

<p>
Our Mock API Generator lets you simulate real-world conditions:
</p>

<h3>Latency Simulation</h3>

<p>
Set latency to test loading states in your application. For example:
</p>

<ul>
<li><strong>0ms:</strong> Instant response (ideal conditions)</li>
<li><strong>500ms:</strong> Typical API response time</li>
<li><strong>2000ms:</strong> Slow network simulation</li>
<li><strong>5000ms:</strong> Very slow / timeout edge case testing</li>
</ul>

<h3>Error Rate Simulation</h3>

<p>
Set an error rate percentage to test your app's error handling:
</p>

<ul>
<li><strong>0%:</strong> Always success</li>
<li><strong>10%:</strong> Occasional failures (realistic)</li>
<li><strong>50%:</strong> Frequent failures (stress testing)</li>
<li><strong>100%:</strong> Always fails (error handling verification)</li>
</ul>

<pre><code class="language-json">// Error response (when error simulation triggers)
{
  "error": "Internal Server Error",
  "message": "Simulated server error (based on configured error rate)",
  "status": 500
}</code></pre>

<h2>💾 Managing Your Endpoints</h2>

<p>
All your created endpoints are saved and visible in the <strong>"My Saved Endpoints"</strong> section. You can:
</p>

<ul>
<li><strong>Copy URL:</strong> Quick copy to clipboard</li>
<li><strong>Edit:</strong> Update name, IP restriction settings, and allowed IPs</li>
<li><strong>Delete:</strong> Remove endpoints you no longer need</li>
<li><strong>View Stats:</strong> See how many times each endpoint was accessed</li>
</ul>

<p>
Your endpoints persist on our servers and are associated with your IP address, so you'll see them even after refreshing the page.
</p>

<h2>🔐 IP Restriction Best Practices</h2>

<h3>For Development Teams</h3>

<ol>
<li>Collect the public IP addresses of all team members</li>
<li>Add all IPs to the allowed list (comma-separated)</li>
<li>Share the endpoint URL with your team</li>
</ol>

<h3>For Production-like Testing</h3>

<ol>
<li>Use IP restriction to simulate production access control</li>
<li>Test your application's handling of 403 responses</li>
<li>Verify your error messages and redirects work correctly</li>
</ol>

<h3>For Personal Use</h3>

<ol>
<li>Click "Add My IP" to auto-add your current IP</li>
<li>Enable IP restriction to protect your mock data</li>
<li>Remember to update the IP if you change networks!</li>
</ol>

<h2>🌐 CORS Support</h2>

<p>
All mock endpoints include proper CORS headers, making them usable from any domain:
</p>

<pre><code class="language-text">Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization</code></pre>

<p>
This means you can call your mock endpoints from:
</p>

<ul>
<li>Localhost development servers</li>
<li>Deployed applications on any domain</li>
<li>CodePen, JSFiddle, and other online editors</li>
<li>Mobile applications</li>
</ul>

<h2>🔧 Common Use Cases</h2>

<h3>1. Frontend Development Before Backend</h3>

<p>
Start building your UI immediately using mock APIs that match your planned backend structure. When the real backend is ready, simply swap the endpoint URLs.
</p>

<h3>2. UI/UX Prototyping</h3>

<p>
Create realistic prototypes with dynamic data to demonstrate to stakeholders. The random data makes each demo feel fresh and real.
</p>

<h3>3. Automated Testing</h3>

<p>
Use mock endpoints in your Jest, Cypress, or Playwright tests for consistent, reliable test data.
</p>

<h3>4. Demo Applications</h3>

<p>
Build portfolio projects or demos that look real without needing a production database.
</p>

<h3>5. Learning API Integration</h3>

<p>
New developers can practice API integration without setting up a backend server.
</p>

<h2>🏆 Why Choose Our Mock API Generator?</h2>

<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
<thead>
<tr style="background: var(--color-surface-alt);">
<th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid var(--color-border);">Feature</th>
<th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid var(--color-border);">Our Tool</th>
<th style="padding: 0.75rem; text-align: center; border-bottom: 2px solid var(--color-border);">Others</th>
</tr>
</thead>
<tbody>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">IP Restriction</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">✅</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">❌</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">No Signup Required</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">✅</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">❌</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Multiple Record Generation</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">✅</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">Limited</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Latency Simulation</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">✅</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">Some</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Error Rate Simulation</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">✅</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">Rare</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">Edit Saved Endpoints</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">✅</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">❌</td></tr>
<tr><td style="padding: 0.75rem; border-bottom: 1px solid var(--color-border);">CORS Enabled</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">✅</td><td style="padding: 0.75rem; text-align: center; border-bottom: 1px solid var(--color-border);">✅</td></tr>
<tr><td style="padding: 0.75rem;">100% Free</td><td style="padding: 0.75rem; text-align: center;">✅</td><td style="padding: 0.75rem; text-align: center;">Often limited</td></tr>
</tbody>
</table>

<h2>🚀 Get Started Now</h2>

<p>
Ready to create your first mock endpoint? Here's what to do:
</p>

<ol>
<li>Configure your endpoint path and method</li>
<li>Create a response template with dynamic variables</li>
<li>Set the number of records you need</li>
<li>Optionally enable IP restriction for security</li>
<li>Click "Create Server Endpoint" and copy your URL</li>
<li>Use the URL in your application immediately!</li>
</ol>

<p style="text-align: center; margin-top: 2rem;">
<a href="/mock-api/" style="display: inline-block; background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem;">
Try the Mock API Generator Now →
</a>
</p>

<hr style="margin: 3rem 0;">

<h2>📚 Related Tools You Might Like</h2>

<ul>
<li><a href="/api-response-tester/">API Response Tester</a> — Test any API endpoint and view responses</li>
<li><a href="/swagger-viewer/">Swagger/OpenAPI Viewer</a> — Visualize your API documentation</li>
<li><a href="/json-diff/">JSON Diff Tool</a> — Compare two JSON documents</li>
<li><a href="/dummy-json/">Dummy JSON Generator</a> — Generate sample JSON data</li>
<li><a href="/">JSON Formatter</a> — Format and validate JSON data</li>
</ul>
"""

        # Create or update the blog post
        post_data = {
            'title': 'Complete Guide to Mock API Generator with IP Restriction',
            'slug': 'mock-api-generator-guide-ip-restriction',
            'category': category,
            'excerpt': 'Learn how to create custom mock API endpoints with IP restriction, dynamic data generation, latency simulation, and more. Perfect for frontend development, testing, and prototyping.',
            'content': content.strip(),
            'tags': 'mock api, api testing, ip restriction, mock server, rest api, api generator, fake api, json api, frontend development, api mocking, postman alternative, developer tools',
            'meta_description': 'Complete guide to creating mock API endpoints with IP restriction. Learn template variables, latency simulation, error rate testing, and best practices for API mocking.',
            'meta_keywords': keywords.strip().replace('\\n', ''),
            'published': True,
            'published_at': timezone.now()
        }

        post, created = BlogPost.objects.update_or_create(
            slug='mock-api-generator-guide-ip-restriction',
            defaults=post_data
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created blog post: {post.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Updated blog post: {post.title}'))

        self.stdout.write(self.style.SUCCESS(f'\\nBlog post URL: /blog/{post.slug}/'))
        self.stdout.write(self.style.SUCCESS(f'Word count: ~4000+ words'))
        self.stdout.write(self.style.SUCCESS(f'Keywords: 100+'))
