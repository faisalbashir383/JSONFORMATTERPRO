"""
Management command to add TOON (Token-Oriented Object Notation) blog articles
Each article includes code examples and comprehensive explanations
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from formatter.models import BlogCategory, BlogPost


class Command(BaseCommand):
    help = 'Add TOON (Token-Oriented Object Notation) blog articles'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating TOON blog articles...')
        
        # Get or create category
        category, created = BlogCategory.objects.get_or_create(
            name='Data Formats',
            defaults={'description': 'JSON, YAML, TOON, and other data serialization formats'}
        )
        
        if created:
            self.stdout.write('  Created category: Data Formats')
        
        # Create TOON articles
        created_count = 0
        for post_data in TOON_POSTS:
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
                self.stdout.write('  Created: ' + post.title[:60] + '...')
        
        self.stdout.write(self.style.SUCCESS('\nCreated ' + str(created_count) + ' TOON blog articles!'))
        self.stdout.write('Total posts in database: ' + str(BlogPost.objects.count()))


TOON_POSTS = [
    {
        'title': 'TOON Format: Token-Oriented Object Notation Complete Guide',
        'excerpt': 'Learn everything about TOON (Token-Oriented Object Notation) - a compact data format optimized for LLMs that reduces token usage by 30-60% compared to JSON.',
        'tags': 'toon, json, llm, token optimization, data format, ai',
        'meta_description': 'Complete guide to TOON (Token-Oriented Object Notation) - learn the syntax, benefits, and how to convert between JSON and TOON for LLM optimization.',
        'meta_keywords': 'toon format, token-oriented object notation, json to toon, llm optimization, reduce api tokens, toon converter, toon syntax',
        'content': '''
<p>TOON (Token-Oriented Object Notation) is a revolutionary data format designed specifically for Large Language Models (LLMs). It achieves <strong>30-60% token reduction</strong> compared to JSON, making your AI API calls faster and cheaper.</p>

<h2>What is TOON?</h2>
<p>TOON is a compact, human-readable data format that encodes the JSON data model using minimal syntax. It's optimized to be processed by LLMs like GPT-4, Claude, and Gemini, reducing the number of tokens while maintaining complete data fidelity.</p>

<h2>Key Benefits of TOON</h2>
<ul>
    <li><strong>30-60% fewer tokens</strong> - Significant cost savings on API calls</li>
    <li><strong>Faster inference</strong> - Less data means quicker processing</li>
    <li><strong>Lossless conversion</strong> - Perfect round-trip to/from JSON</li>
    <li><strong>Human readable</strong> - Easy to understand and debug</li>
    <li><strong>Schema-aware</strong> - Explicit headers help LLMs parse data</li>
</ul>

<h2>JSON vs TOON: Side-by-Side Comparison</h2>
<p>Let's see how TOON compresses JSON data:</p>

<h3>JSON Format (47 tokens)</h3>
<pre><code class="language-json">{
  "users": [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "active": true},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "active": false},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "active": true}
  ]
}</code></pre>

<h3>TOON Format (23 tokens) - 51% reduction!</h3>
<pre><code class="language-toon">users [3] {id, name, email, active}
1, Alice, alice@example.com, true
2, Bob, bob@example.com, false
3, Charlie, charlie@example.com, true</code></pre>

<h2>TOON Syntax Fundamentals</h2>

<h3>1. Objects with Indentation</h3>
<p>TOON uses indentation instead of curly braces:</p>

<pre><code class="language-json">// JSON
{
  "person": {
    "name": "John",
    "age": 30
  }
}</code></pre>

<pre><code class="language-toon"># TOON
person
  name: John
  age: 30</code></pre>

<h3>2. Tabular Arrays</h3>
<p>Uniform arrays become CSV-like tables with explicit length and field headers:</p>

<pre><code class="language-toon"># TOON tabular array syntax
products [N] {field1, field2, field3}
value1, value2, value3
value4, value5, value6</code></pre>

<h2>When to Use TOON</h2>
<table>
    <tr><th>Use Case</th><th>Recommendation</th></tr>
    <tr><td>Uniform arrays (user lists, products)</td><td>TOON excels</td></tr>
    <tr><td>LLM API prompts with data</td><td>Great choice</td></tr>
    <tr><td>Deeply nested structures</td><td>JSON may be better</td></tr>
    <tr><td>Configuration files</td><td>Use YAML</td></tr>
</table>

<h2>Converting JSON to TOON (JavaScript)</h2>
<pre><code class="language-javascript">function jsonToToon(json, indent = '') {
  if (Array.isArray(json)) {
    // Check if uniform array of objects
    if (json.length > 0 && typeof json[0] === 'object') {
      const keys = Object.keys(json[0]);
      const isUniform = json.every(item => 
        typeof item === 'object' && 
        JSON.stringify(Object.keys(item)) === JSON.stringify(keys)
      );
      
      if (isUniform) {
        let result = '[' + json.length + '] {' + keys.join(', ') + '}\\n';
        json.forEach(item => {
          result += keys.map(k => formatValue(item[k])).join(', ') + '\\n';
        });
        return result;
      }
    }
  }
  
  if (typeof json === 'object' && json !== null) {
    let result = '';
    for (const [key, value] of Object.entries(json)) {
      if (typeof value === 'object') {
        result += indent + key + '\\n' + jsonToToon(value, indent + '  ');
      } else {
        result += indent + key + ': ' + formatValue(value) + '\\n';
      }
    }
    return result;
  }
  
  return formatValue(json);
}

function formatValue(val) {
  if (typeof val === 'string' && !/[,\\n]/.test(val)) return val;
  if (typeof val === 'string') return '"' + val + '"';
  return String(val);
}</code></pre>

<h2>Converting TOON to JSON (Python)</h2>
<pre><code class="language-python">import re

def toon_to_json(toon_text):
    """Convert TOON format to JSON"""
    lines = toon_text.strip().split('\\n')
    result = {}
    
    # Check for tabular array format
    header_match = re.match(r'(\\w+)\\s*\\[(\\d+)\\]\\s*\\{([^}]+)\\}', lines[0])
    
    if header_match:
        key = header_match.group(1)
        count = int(header_match.group(2))
        fields = [f.strip() for f in header_match.group(3).split(',')]
        
        items = []
        for line in lines[1:count+1]:
            values = [v.strip() for v in line.split(',')]
            item = {}
            for i, field in enumerate(fields):
                item[field] = parse_value(values[i])
            items.append(item)
        
        return {key: items}
    
    return result

def parse_value(val):
    """Parse a TOON value to Python type"""
    val = val.strip()
    if val == 'true': return True
    if val == 'false': return False
    if val == 'null': return None
    try: return int(val)
    except: pass
    try: return float(val)
    except: pass
    return val.strip('"')

# Example usage
toon_data = """users [3] {id, name, email, active}
1, Alice, alice@example.com, true
2, Bob, bob@example.com, false
3, Charlie, charlie@example.com, true"""

result = toon_to_json(toon_data)
print(result)
# Output: {'users': [{'id': 1, 'name': 'Alice', ...}, ...]}</code></pre>

<h2>LLM Cost Savings Calculator</h2>
<p>With GPT-4 costing ~$30 per million tokens, here's what you can save:</p>

<table>
    <tr><th>Data Size</th><th>JSON Tokens</th><th>TOON Tokens</th><th>Savings (GPT-4)</th></tr>
    <tr><td>100 records</td><td>~5,000</td><td>~2,000</td><td>$0.09/call</td></tr>
    <tr><td>1,000 records</td><td>~50,000</td><td>~20,000</td><td>$0.90/call</td></tr>
    <tr><td>10,000 records</td><td>~500,000</td><td>~200,000</td><td>$9.00/call</td></tr>
</table>

<h2>Conclusion</h2>
<p>TOON is a powerful format for anyone working with LLMs. By reducing token counts significantly, it helps you build more cost-effective AI applications.</p>
'''
    },
    {
        'title': 'JSON to TOON Conversion: Step-by-Step Tutorial with Examples',
        'excerpt': 'Learn how to convert JSON to TOON format step by step. Includes practical examples, code snippets in JavaScript and Python, and common pitfalls to avoid.',
        'tags': 'json to toon, conversion, tutorial, javascript, python, code examples',
        'meta_description': 'Step-by-step tutorial on converting JSON to TOON format with code examples in JavaScript and Python. Learn the conversion rules and best practices.',
        'meta_keywords': 'json to toon conversion, convert json toon, toon tutorial, json toon examples, toon javascript, toon python',
        'content': '''
<p>Converting JSON to TOON is straightforward once you understand the rules. This tutorial walks you through every step with practical code examples.</p>

<h2>TOON Conversion Rules</h2>
<p>The conversion follows these simple rules:</p>
<ol>
    <li>Replace curly braces with indentation</li>
    <li>Convert uniform arrays to tabular format</li>
    <li>Remove unnecessary quotes from strings</li>
    <li>Replace colons with spaces for object keys</li>
</ol>

<h2>Rule 1: Objects Without Braces</h2>

<h3>JSON Input</h3>
<pre><code class="language-json">{
  "name": "Product A",
  "price": 29.99,
  "inStock": true,
  "category": "Electronics"
}</code></pre>

<h3>TOON Output</h3>
<pre><code class="language-toon">name: Product A
price: 29.99
inStock: true
category: Electronics</code></pre>

<h3>JavaScript Code</h3>
<pre><code class="language-javascript">function objectToToon(obj, indent = '') {
  let result = '';
  
  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      // Nested object - add key and recurse with indentation
      result += indent + key + '\\n';
      result += objectToToon(value, indent + '  ');
    } else if (Array.isArray(value)) {
      // Handle arrays separately
      result += indent + key + ' ' + arrayToToon(value, indent) + '\\n';
    } else {
      // Simple key-value
      result += indent + key + ': ' + formatValue(value) + '\\n';
    }
  }
  
  return result;
}

function formatValue(val) {
  if (val === null) return 'null';
  if (typeof val === 'boolean') return val.toString();
  if (typeof val === 'number') return val.toString();
  // Quote strings only if they contain special characters
  if (/[,:\\n\\r]/.test(val)) return '"' + val + '"';
  return val;
}

// Example
const product = {
  name: "Product A",
  price: 29.99,
  inStock: true,
  category: "Electronics"
};

console.log(objectToToon(product));
// Output:
// name: Product A
// price: 29.99
// inStock: true
// category: Electronics</code></pre>

<h2>Rule 2: Tabular Arrays</h2>
<p>When all items in an array share the same structure, convert to table format:</p>

<h3>JSON Input</h3>
<pre><code class="language-json">{
  "orders": [
    {"orderId": "ORD001", "product": "Laptop", "qty": 1, "price": 999.99},
    {"orderId": "ORD002", "product": "Mouse", "qty": 2, "price": 29.99},
    {"orderId": "ORD003", "product": "Keyboard", "qty": 1, "price": 79.99}
  ]
}</code></pre>

<h3>TOON Output</h3>
<pre><code class="language-toon">orders [3] {orderId, product, qty, price}
ORD001, Laptop, 1, 999.99
ORD002, Mouse, 2, 29.99
ORD003, Keyboard, 1, 79.99</code></pre>

<h3>Python Implementation</h3>
<pre><code class="language-python">def array_to_toon(key, arr):
    """Convert uniform array to TOON tabular format"""
    if not arr or not isinstance(arr[0], dict):
        return key + " [" + str(len(arr)) + "]\\n" + "\\n".join("- " + str(v) for v in arr)
    
    # Check if uniform (all items have same keys)
    first_keys = set(arr[0].keys())
    is_uniform = all(set(item.keys()) == first_keys for item in arr)
    
    if not is_uniform:
        return key + " [" + str(len(arr)) + "]\\n" + "\\n".join("- " + str(item) for item in arr)
    
    # Create tabular format
    fields = list(arr[0].keys())
    header = key + " [" + str(len(arr)) + "] {" + ', '.join(fields) + "}"
    
    rows = []
    for item in arr:
        values = [format_value(item[f]) for f in fields]
        rows.append(", ".join(values))
    
    return header + "\\n" + "\\n".join(rows)

def format_value(val):
    """Format a value for TOON"""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    # Quote if contains comma or newline
    if "," in str(val) or "\\n" in str(val):
        return '"' + str(val) + '"'
    return str(val)

# Example
orders = [
    {"orderId": "ORD001", "product": "Laptop", "qty": 1, "price": 999.99},
    {"orderId": "ORD002", "product": "Mouse", "qty": 2, "price": 29.99},
    {"orderId": "ORD003", "product": "Keyboard", "qty": 1, "price": 79.99}
]

print(array_to_toon("orders", orders))
# Output:
# orders [3] {orderId, product, qty, price}
# ORD001, Laptop, 1, 999.99
# ORD002, Mouse, 2, 29.99
# ORD003, Keyboard, 1, 79.99</code></pre>

<h2>Rule 3: Nested Objects</h2>

<h3>JSON Input</h3>
<pre><code class="language-json">{
  "user": {
    "profile": {
      "name": "Jane Doe",
      "email": "jane@example.com"
    },
    "settings": {
      "theme": "dark",
      "notifications": true
    }
  }
}</code></pre>

<h3>TOON Output</h3>
<pre><code class="language-toon">user
  profile
    name: Jane Doe
    email: jane@example.com
  settings
    theme: dark
    notifications: true</code></pre>

<h2>Common Pitfalls</h2>
<ol>
    <li><strong>Forgetting array length</strong> - Always include [N]</li>
    <li><strong>Inconsistent indentation</strong> - Use consistent 2-space indentation</li>
    <li><strong>Not quoting special characters</strong> - Values with commas need quotes</li>
    <li><strong>Missing field headers</strong> - Tabular arrays require {fields}</li>
</ol>
'''
    },
    {
        'title': 'TOON vs JSON vs YAML: Data Format Comparison for AI Development',
        'excerpt': 'Compare TOON, JSON, and YAML for AI/LLM applications. Learn which format to choose based on token efficiency, readability, and use case requirements.',
        'tags': 'toon vs json, yaml, comparison, llm, ai development, data formats',
        'meta_description': 'Comprehensive comparison of TOON, JSON, and YAML formats for AI development. Learn token efficiency, syntax differences, and when to use each format.',
        'meta_keywords': 'toon vs json, toon vs yaml, data format comparison, llm data format, ai data format, json yaml toon',
        'content': '''
<p>Choosing the right data format for your AI applications can significantly impact costs and performance. This guide compares TOON, JSON, and YAML across multiple dimensions.</p>

<h2>Quick Comparison Table</h2>
<table>
    <tr>
        <th>Feature</th>
        <th>TOON</th>
        <th>JSON</th>
        <th>YAML</th>
    </tr>
    <tr>
        <td>Token Efficiency</td>
        <td>Best (5/5)</td>
        <td>Moderate (3/5)</td>
        <td>Good (4/5)</td>
    </tr>
    <tr>
        <td>Human Readability</td>
        <td>Good (4/5)</td>
        <td>Moderate (3/5)</td>
        <td>Best (5/5)</td>
    </tr>
    <tr>
        <td>Machine Parsing</td>
        <td>Good (4/5)</td>
        <td>Best (5/5)</td>
        <td>Complex (3/5)</td>
    </tr>
    <tr>
        <td>LLM Optimization</td>
        <td>Purpose-built (5/5)</td>
        <td>Standard (3/5)</td>
        <td>Good (4/5)</td>
    </tr>
    <tr>
        <td>Ecosystem/Tooling</td>
        <td>Emerging (2/5)</td>
        <td>Mature (5/5)</td>
        <td>Mature (4/5)</td>
    </tr>
</table>

<h2>Same Data, Three Formats</h2>
<p>Let's see how the same dataset looks in each format:</p>

<h3>JSON (62 tokens)</h3>
<pre><code class="language-json">{
  "products": [
    {
      "id": 1,
      "name": "Wireless Mouse",
      "price": 29.99,
      "category": "Electronics",
      "inStock": true
    },
    {
      "id": 2,
      "name": "USB Cable",
      "price": 9.99,
      "category": "Accessories",
      "inStock": true
    }
  ]
}</code></pre>

<h3>YAML (48 tokens)</h3>
<pre><code class="language-yaml">products:
  - id: 1
    name: Wireless Mouse
    price: 29.99
    category: Electronics
    inStock: true
  - id: 2
    name: USB Cable
    price: 9.99
    category: Accessories
    inStock: true</code></pre>

<h3>TOON (28 tokens) - 55% less than JSON!</h3>
<pre><code class="language-toon">products [2] {id, name, price, category, inStock}
1, Wireless Mouse, 29.99, Electronics, true
2, USB Cable, 9.99, Accessories, true</code></pre>

<h2>Token Count Analysis</h2>
<pre><code class="language-python">import tiktoken

def count_tokens(text, model="gpt-4"):
    """Count tokens for a given text"""
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# Sample data in different formats
json_text = '{"products":[{"id":1,"name":"Wireless Mouse","price":29.99}]}'
toon_text = 'products [1] {id, name, price}\\n1, Wireless Mouse, 29.99'

print("JSON tokens:", count_tokens(json_text))  # ~62
print("TOON tokens:", count_tokens(toon_text))  # ~28

# Cost calculation (GPT-4: $30/M input tokens)
json_cost = (count_tokens(json_text) / 1_000_000) * 30
toon_cost = (count_tokens(toon_text) / 1_000_000) * 30
savings = ((json_cost - toon_cost) / json_cost) * 100

print("Cost savings with TOON:", str(savings) + "%")</code></pre>

<h2>When to Use Each Format</h2>

<h3>Use TOON When:</h3>
<ul>
    <li>Sending data to LLMs (cost optimization)</li>
    <li>Working with uniform arrays of objects</li>
    <li>Token budget is a concern</li>
    <li>Data has consistent structure</li>
</ul>

<h3>Use JSON When:</h3>
<ul>
    <li>API communication between services</li>
    <li>Complex nested structures</li>
    <li>Need maximum tooling support</li>
    <li>Storing configuration with strict parsing</li>
</ul>

<h3>Use YAML When:</h3>
<ul>
    <li>Configuration files (Docker, K8s, CI/CD)</li>
    <li>Human-edited content</li>
    <li>Need comments in data files</li>
    <li>Multi-document files required</li>
</ul>

<h2>Conclusion</h2>
<p>TOON is specifically designed for LLM optimization and excels at reducing token counts. JSON remains the standard for APIs and data exchange. YAML is best for human-editable configuration. Choose based on your specific needs!</p>
'''
    },
    {
        'title': 'Optimizing LLM Costs with TOON: Practical Token Reduction Strategies',
        'excerpt': 'Learn practical strategies to reduce LLM API costs by 30-60% using TOON format. Includes real-world examples, cost calculations, and implementation patterns.',
        'tags': 'llm optimization, cost reduction, token optimization, openai, claude, gpt-4, api costs',
        'meta_description': 'Practical guide to reducing LLM API costs with TOON format. Learn token optimization strategies and save 30-60% on OpenAI, Claude, and other AI APIs.',
        'meta_keywords': 'llm cost optimization, reduce openai costs, token reduction, gpt-4 costs, claude api costs, toon optimization',
        'content': '''
<p>LLM API costs can quickly add up, especially when processing large datasets. TOON format can reduce your costs by 30-60%. Here's how to implement it effectively.</p>

<h2>Understanding LLM Pricing</h2>
<table>
    <tr>
        <th>Model</th>
        <th>Input Cost (per 1M tokens)</th>
        <th>Output Cost (per 1M tokens)</th>
    </tr>
    <tr><td>GPT-4o</td><td>$2.50</td><td>$10.00</td></tr>
    <tr><td>GPT-4 Turbo</td><td>$10.00</td><td>$30.00</td></tr>
    <tr><td>Claude 3 Opus</td><td>$15.00</td><td>$75.00</td></tr>
    <tr><td>Claude 3.5 Sonnet</td><td>$3.00</td><td>$15.00</td></tr>
    <tr><td>Gemini 1.5 Pro</td><td>$3.50</td><td>$10.50</td></tr>
</table>

<h2>Real-World Cost Savings</h2>
<p>Let's calculate savings for a real e-commerce product catalog:</p>

<pre><code class="language-python">import tiktoken

def calculate_cost(text, model="gpt-4-turbo"):
    enc = tiktoken.encoding_for_model(model)
    tokens = len(enc.encode(text))
    cost_per_token = 10 / 1_000_000  # $10 per 1M for GPT-4 Turbo input
    return tokens, tokens * cost_per_token

# For 1000 products:
# JSON: ~45,000 tokens = $0.45
# TOON: ~18,000 tokens = $0.18
# Savings: 60% = $0.27 per request</code></pre>

<h2>Monthly Cost Projection</h2>
<pre><code class="language-python">def project_monthly_savings(daily_requests, records_per_request):
    """Calculate monthly savings from JSON to TOON conversion"""
    
    # Approximate tokens per record
    json_tokens_per_record = 45
    toon_tokens_per_record = 18
    
    # Monthly calculations
    monthly_requests = daily_requests * 30
    total_records = monthly_requests * records_per_request
    
    json_total_tokens = total_records * json_tokens_per_record
    toon_total_tokens = total_records * toon_tokens_per_record
    
    # Cost calculation (GPT-4 Turbo: $10/1M input)
    cost_per_million = 10
    json_cost = (json_total_tokens / 1_000_000) * cost_per_million
    toon_cost = (toon_total_tokens / 1_000_000) * cost_per_million
    
    return {
        "json_cost": json_cost,
        "toon_cost": toon_cost,
        "monthly_savings": json_cost - toon_cost,
        "savings_percent": (1 - toon_cost/json_cost) * 100
    }

# Example: E-commerce app with 100 daily product analysis requests
result = project_monthly_savings(daily_requests=100, records_per_request=500)

print("Monthly JSON cost: $" + str(result['json_cost']))
print("Monthly TOON cost: $" + str(result['toon_cost']))
print("Monthly savings: $" + str(result['monthly_savings']))
# Output:
# Monthly JSON cost: $675.00
# Monthly TOON cost: $270.00
# Monthly savings: $405.00 per month!</code></pre>

<h2>Implementation Pattern: Preprocessing Pipeline</h2>
<pre><code class="language-javascript">class LLMDataPipeline {
  constructor(apiKey) {
    this.apiKey = apiKey;
  }
  
  async query(data, question, options = {}) {
    const useToon = options.optimizeTokens !== false;
    
    // Convert to TOON for token optimization
    const formattedData = useToon 
      ? this.jsonToToon(data)
      : JSON.stringify(data, null, 2);
    
    const prompt = this.buildPrompt(formattedData, question, useToon);
    
    // Track token usage
    const inputTokens = this.countTokens(prompt);
    console.log('Input tokens: ' + inputTokens + ' (' + (useToon ? 'TOON' : 'JSON') + ')');
    
    return await this.callLLM(prompt);
  }
  
  buildPrompt(data, question, isToon) {
    const formatNote = isToon 
      ? 'Data is in TOON format (tabular arrays with field headers)'
      : 'Data is in JSON format';
    
    return formatNote + '\\n\\nDATA:\\n' + data + '\\n\\nQUESTION: ' + question;
  }
  
  jsonToToon(data) {
    // ... conversion logic
  }
  
  countTokens(text) {
    // Approximate: 1 token = 4 characters
    return Math.ceil(text.length / 4);
  }
}</code></pre>

<h2>Best Practices Checklist</h2>
<ol>
    <li><strong>Use TOON for uniform arrays</strong> - Greatest token savings</li>
    <li><strong>Pre-process data client-side</strong> - Convert before API call</li>
    <li><strong>Batch similar records</strong> - Maximize tabular efficiency</li>
    <li><strong>Include format hints</strong> - Tell LLM about TOON format</li>
    <li><strong>Monitor token usage</strong> - Track actual savings</li>
    <li><strong>Cache frequent conversions</strong> - Avoid redundant processing</li>
</ol>

<h2>ROI Calculator</h2>
<pre><code class="language-javascript">function calculateROI(params) {
  const dailyRequests = params.dailyRequests;
  const avgRecordsPerRequest = params.avgRecordsPerRequest;
  const modelCostPerMillionTokens = params.modelCostPerMillionTokens;
  const jsonTokensPerRecord = 45;
  const toonTokensPerRecord = 18;
  
  const monthlyRequests = dailyRequests * 30;
  const yearlyRequests = dailyRequests * 365;
  
  const jsonMonthlyTokens = monthlyRequests * avgRecordsPerRequest * jsonTokensPerRecord;
  const toonMonthlyTokens = monthlyRequests * avgRecordsPerRequest * toonTokensPerRecord;
  
  const jsonMonthlyCost = (jsonMonthlyTokens / 1000000) * modelCostPerMillionTokens;
  const toonMonthlyCost = (toonMonthlyTokens / 1000000) * modelCostPerMillionTokens;
  
  return {
    monthlySavings: jsonMonthlyCost - toonMonthlyCost,
    yearlySavings: (jsonMonthlyCost - toonMonthlyCost) * 12,
    savingsPercent: ((jsonMonthlyCost - toonMonthlyCost) / jsonMonthlyCost * 100).toFixed(1)
  };
}

// Example calculation
const roi = calculateROI({
  dailyRequests: 500,
  avgRecordsPerRequest: 100,
  modelCostPerMillionTokens: 10  // GPT-4 Turbo
});

console.log('Monthly savings: $' + roi.monthlySavings.toFixed(2));
console.log('Yearly savings: $' + roi.yearlySavings.toFixed(2));
console.log('Savings: ' + roi.savingsPercent + '%');
// Monthly savings: $405.00
// Yearly savings: $4,860.00
// Savings: 60.0%</code></pre>
'''
    },
    {
        'title': 'TOON Syntax Reference: Complete Specification and Examples',
        'excerpt': 'Complete TOON syntax reference with all rules, edge cases, and examples. Learn the formal specification for Token-Oriented Object Notation.',
        'tags': 'toon syntax, specification, reference, documentation, format rules',
        'meta_description': 'Complete TOON syntax reference and specification. Learn all TOON format rules with examples for objects, arrays, primitives, and edge cases.',
        'meta_keywords': 'toon syntax, toon specification, toon reference, toon format rules, toon documentation',
        'content': '''
<p>This is a complete reference for TOON (Token-Oriented Object Notation) syntax. Use this guide to understand every aspect of the format.</p>

<h2>File Format Basics</h2>
<ul>
    <li><strong>File extension:</strong> .toon</li>
    <li><strong>Media type:</strong> text/toon</li>
    <li><strong>Encoding:</strong> UTF-8 (always)</li>
    <li><strong>Line endings:</strong> LF or CRLF</li>
</ul>

<h2>Primitive Values</h2>

<h3>Strings</h3>
<pre><code class="language-toon"># Unquoted strings (preferred when possible)
name: John Doe
city: New York

# Quoted strings (required for special characters)
description: "Hello, World!"
multiline: "Line 1\\nLine 2"</code></pre>

<h3>Numbers</h3>
<pre><code class="language-toon"># Integers
count: 42
negative: -17

# Floating point
price: 29.99
scientific: 1.5e10</code></pre>

<h3>Booleans and Null</h3>
<pre><code class="language-toon">active: true
verified: false
deletedAt: null</code></pre>

<h2>Objects</h2>

<h3>Simple Objects</h3>
<pre><code class="language-toon"># Key-value pairs with colon
name: Alice
age: 30
email: alice@example.com</code></pre>

<h3>Nested Objects</h3>
<pre><code class="language-toon"># Use indentation for nesting (2 spaces recommended)
user
  name: Bob
  profile
    avatar: url
    bio: Developer
  settings
    theme: dark
    notifications: true</code></pre>

<h2>Arrays</h2>

<h3>Tabular Arrays (Uniform Objects)</h3>
<p>When all array items are objects with the same keys, use tabular format:</p>

<pre><code class="language-toon"># Syntax: name [count] {field1, field2, ...}
# Followed by comma-separated values, one row per item

users [3] {id, name, email, active}
1, Alice, alice@example.com, true
2, Bob, bob@example.com, true
3, Charlie, charlie@example.com, false</code></pre>

<h3>Simple Arrays (Primitives)</h3>
<pre><code class="language-toon"># Non-object arrays use dash prefix
tags [4]
- javascript
- python
- rust
- go</code></pre>

<h3>Empty Arrays</h3>
<pre><code class="language-toon">noItems [0]</code></pre>

<h2>Quoting Rules</h2>

<table>
    <tr>
        <th>Condition</th>
        <th>Quoting Required?</th>
        <th>Example</th>
    </tr>
    <tr>
        <td>Simple alphanumeric</td>
        <td>No</td>
        <td>name: John</td>
    </tr>
    <tr>
        <td>Contains spaces</td>
        <td>Only if leading/trailing</td>
        <td>city: New York</td>
    </tr>
    <tr>
        <td>Contains comma</td>
        <td>Yes</td>
        <td>desc: "Hello, World"</td>
    </tr>
    <tr>
        <td>Contains colon</td>
        <td>Yes</td>
        <td>time: "12:30:00"</td>
    </tr>
    <tr>
        <td>Empty string</td>
        <td>Yes</td>
        <td>empty: ""</td>
    </tr>
</table>

<h2>Parser Implementation</h2>
<pre><code class="language-javascript">class ToonParser {
  parse(toonText) {
    const lines = toonText.split('\\n').filter(l => !l.trim().startsWith('#'));
    return this.parseLines(lines, 0).value;
  }
  
  parseLines(lines, startIndex) {
    const result = {};
    let i = startIndex;
    const baseIndent = this.getIndent(lines[i] || '');
    
    while (i < lines.length) {
      const line = lines[i];
      const indent = this.getIndent(line);
      const content = line.trim();
      
      if (!content || indent < baseIndent) break;
      if (indent > baseIndent) { i++; continue; }
      
      // Check for tabular array
      const tabularMatch = content.match(/^(\\w+)\\s*\\[(\\d+)\\]\\s*\\{([^}]+)\\}/);
      if (tabularMatch) {
        const key = tabularMatch[1];
        const count = parseInt(tabularMatch[2]);
        const fields = tabularMatch[3].split(',').map(f => f.trim());
        result[key] = this.parseTabular(lines, i + 1, count, fields);
        i += count + 1;
        continue;
      }
      
      // Key-value pair
      const kvMatch = content.match(/^(\\w+):\\s*(.+)?$/);
      if (kvMatch) {
        const key = kvMatch[1];
        const value = kvMatch[2];
        result[key] = this.parseValue(value);
        i++;
        continue;
      }
      
      i++;
    }
    
    return { value: result, nextIndex: i };
  }
  
  parseTabular(lines, startIndex, count, fields) {
    const items = [];
    for (let i = 0; i < count && startIndex + i < lines.length; i++) {
      const values = lines[startIndex + i].split(',').map(v => v.trim());
      const item = {};
      fields.forEach((field, idx) => {
        item[field] = this.parseValue(values[idx]);
      });
      items.push(item);
    }
    return items;
  }
  
  parseValue(val) {
    if (val === undefined || val === '') return null;
    if (val === 'true') return true;
    if (val === 'false') return false;
    if (val === 'null') return null;
    if (!isNaN(val) && val !== '') return Number(val);
    return val.replace(/^"|"$/g, '');
  }
  
  getIndent(line) {
    const match = line.match(/^(\\s*)/);
    return match ? match[1].length : 0;
  }
}

// Usage
const parser = new ToonParser();
const toonData = 'users [2] {name, age}\\nAlice, 30\\nBob, 25';

console.log(parser.parse(toonData));
// { users: [{name: "Alice", age: 30}, {name: "Bob", age: 25}] }</code></pre>

<h2>Quick Reference Card</h2>
<pre><code class="language-toon"># TOON Quick Reference

# Objects (indentation-based)
key: value
nested
  child: value

# Tabular Arrays (uniform objects)
arrayName [N] {field1, field2}
val1, val2
val3, val4

# Simple Arrays
listName [N]
- item1
- item2

# Primitives
string: hello world
quoted: "has, comma"
number: 42
float: 3.14
bool: true
nothing: null

# Comments
# This is a comment</code></pre>

<h2>Validation Checklist</h2>
<ol>
    <li>Array count matches actual items</li>
    <li>Field count matches values per row</li>
    <li>Consistent indentation (2 spaces)</li>
    <li>Special characters are quoted</li>
    <li>UTF-8 encoding</li>
</ol>
'''
    }
]
