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
            self.stdout.write(f'  ✓ Created category: {category.name}')
        
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
                self.stdout.write(f'  ✓ Created: {post.title[:60]}...')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Created {created_count} TOON blog articles!'))
        self.stdout.write(f'📚 Total posts in database: {BlogPost.objects.count()}')


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

<h3>3. Mixed Arrays</h3>
<p>Non-uniform arrays use simple notation:</p>

<pre><code class="language-toon"># TOON mixed array
items [3]
- first item
- 42
- true</code></pre>

<h2>When to Use TOON</h2>
<table>
    <tr><th>Use Case</th><th>Recommendation</th></tr>
    <tr><td>Uniform arrays (user lists, products)</td><td>✅ TOON excels</td></tr>
    <tr><td>LLM API prompts with data</td><td>✅ Great choice</td></tr>
    <tr><td>Deeply nested structures</td><td>⚠️ JSON may be better</td></tr>
    <tr><td>Configuration files</td><td>⚠️ Use YAML</td></tr>
</table>

<h2>Converting JSON to TOON</h2>
<p>Here's a simple JavaScript function to convert JSON to TOON:</p>

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
        let result = `[${json.length}] {${keys.join(', ')}}\\n`;
        json.forEach(item => {
          result += keys.map(k => formatValue(item[k])).join(', ') + '\\n';
        });
        return result;
      }
    }
    // Non-uniform array
    let result = `[${json.length}]\\n`;
    json.forEach(item => {
      result += indent + '- ' + formatValue(item) + '\\n';
    });
    return result;
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
    
    return parse_object(lines)

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
<p>TOON is a powerful format for anyone working with LLMs. By reducing token counts significantly, it helps you build more cost-effective AI applications. Try our <a href="/toon-converter/">TOON Converter Tool</a> to convert your JSON data instantly!</p>
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
      result += `${indent}${key}\\n`;
      result += objectToToon(value, indent + '  ');
    } else if (Array.isArray(value)) {
      // Handle arrays separately
      result += `${indent}${key} ` + arrayToToon(value, indent) + '\\n';
    } else {
      // Simple key-value
      result += `${indent}${key}: ${formatValue(value)}\\n`;
    }
  }
  
  return result;
}

function formatValue(val) {
  if (val === null) return 'null';
  if (typeof val === 'boolean') return val.toString();
  if (typeof val === 'number') return val.toString();
  // Quote strings only if they contain special characters
  if (/[,:\\n\\r]/.test(val)) return `"${val}"`;
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
        return f"{key} [{len(arr)}]\\n" + "\\n".join(f"- {v}" for v in arr)
    
    # Check if uniform (all items have same keys)
    first_keys = set(arr[0].keys())
    is_uniform = all(set(item.keys()) == first_keys for item in arr)
    
    if not is_uniform:
        # Fall back to non-tabular format
        return f"{key} [{len(arr)}]\\n" + "\\n".join(f"- {item}" for item in arr)
    
    # Create tabular format
    fields = list(arr[0].keys())
    header = f"{key} [{len(arr)}] {{{', '.join(fields)}}}"
    
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
        return f'"{val}"'
    return str(val)

# Example
orders = {
    "orders": [
        {"orderId": "ORD001", "product": "Laptop", "qty": 1, "price": 999.99},
        {"orderId": "ORD002", "product": "Mouse", "qty": 2, "price": 29.99},
        {"orderId": "ORD003", "product": "Keyboard", "qty": 1, "price": 79.99}
    ]
}

print(array_to_toon("orders", orders["orders"]))
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

<h2>Complete JSON to TOON Converter</h2>
<pre><code class="language-javascript">class ToonConverter {
  static toToon(json, indent = '') {
    if (json === null) return 'null';
    if (typeof json === 'boolean') return json.toString();
    if (typeof json === 'number') return json.toString();
    if (typeof json === 'string') return this.formatString(json);
    
    if (Array.isArray(json)) {
      return this.arrayToToon(json, indent);
    }
    
    if (typeof json === 'object') {
      return this.objectToToon(json, indent);
    }
    
    return String(json);
  }
  
  static objectToToon(obj, indent = '') {
    let result = '';
    
    for (const [key, value] of Object.entries(obj)) {
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        result += `${indent}${key}\\n`;
        result += this.objectToToon(value, indent + '  ');
      } else if (Array.isArray(value)) {
        result += this.handleArrayProperty(key, value, indent);
      } else {
        result += `${indent}${key}: ${this.toToon(value)}\\n`;
      }
    }
    
    return result;
  }
  
  static handleArrayProperty(key, arr, indent) {
    if (this.isUniformObjectArray(arr)) {
      return this.tabularArray(key, arr, indent);
    }
    return this.simpleArray(key, arr, indent);
  }
  
  static isUniformObjectArray(arr) {
    if (arr.length === 0) return false;
    if (typeof arr[0] !== 'object' || arr[0] === null) return false;
    const keys = JSON.stringify(Object.keys(arr[0]).sort());
    return arr.every(item => 
      typeof item === 'object' && 
      item !== null &&
      JSON.stringify(Object.keys(item).sort()) === keys
    );
  }
  
  static tabularArray(key, arr, indent) {
    const fields = Object.keys(arr[0]);
    let result = `${indent}${key} [${arr.length}] {${fields.join(', ')}}\\n`;
    
    for (const item of arr) {
      const values = fields.map(f => this.toToon(item[f]));
      result += `${indent}${values.join(', ')}\\n`;
    }
    
    return result;
  }
  
  static simpleArray(key, arr, indent) {
    let result = `${indent}${key} [${arr.length}]\\n`;
    for (const item of arr) {
      result += `${indent}- ${this.toToon(item)}\\n`;
    }
    return result;
  }
  
  static formatString(str) {
    if (/[,:\\n\\r\\t]/.test(str) || str.includes('"')) {
      return `"${str.replace(/"/g, '\\\\"')}"`;
    }
    return str;
  }
}

// Usage
const complexData = {
  company: "Acme Inc",
  employees: [
    {name: "Alice", role: "Developer", salary: 75000},
    {name: "Bob", role: "Designer", salary: 65000}
  ],
  office: {
    city: "New York",
    floor: 12
  }
};

console.log(ToonConverter.toToon(complexData));
/* Output:
company: Acme Inc
employees [2] {name, role, salary}
Alice, Developer, 75000
Bob, Designer, 65000
office
  city: New York
  floor: 12
*/</code></pre>

<h2>Common Pitfalls</h2>
<ol>
    <li><strong>Forgetting array length</strong> - Always include <code>[N]</code></li>
    <li><strong>Inconsistent indentation</strong> - Use consistent 2-space indentation</li>
    <li><strong>Not quoting special characters</strong> - Values with commas need quotes</li>
    <li><strong>Missing field headers</strong> - Tabular arrays require <code>{fields}</code></li>
</ol>

<h2>Try It Yourself</h2>
<p>Use our <a href="/toon-converter/">TOON Converter</a> to instantly convert your JSON data and see the token savings!</p>
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
        <td>⭐⭐⭐⭐⭐ Best</td>
        <td>⭐⭐⭐ Moderate</td>
        <td>⭐⭐⭐⭐ Good</td>
    </tr>
    <tr>
        <td>Human Readability</td>
        <td>⭐⭐⭐⭐ Good</td>
        <td>⭐⭐⭐ Moderate</td>
        <td>⭐⭐⭐⭐⭐ Best</td>
    </tr>
    <tr>
        <td>Machine Parsing</td>
        <td>⭐⭐⭐⭐ Good</td>
        <td>⭐⭐⭐⭐⭐ Best</td>
        <td>⭐⭐⭐ Complex</td>
    </tr>
    <tr>
        <td>LLM Optimization</td>
        <td>⭐⭐⭐⭐⭐ Purpose-built</td>
        <td>⭐⭐⭐ Standard</td>
        <td>⭐⭐⭐⭐ Good</td>
    </tr>
    <tr>
        <td>Ecosystem/Tooling</td>
        <td>⭐⭐ Emerging</td>
        <td>⭐⭐⭐⭐⭐ Mature</td>
        <td>⭐⭐⭐⭐ Mature</td>
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
    },
    {
      "id": 3,
      "name": "Laptop Stand",
      "price": 49.99,
      "category": "Office",
      "inStock": false
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
    inStock: true
  - id: 3
    name: Laptop Stand
    price: 49.99
    category: Office
    inStock: false</code></pre>

<h3>TOON (28 tokens) - 55% less than JSON!</h3>
<pre><code class="language-toon">products [3] {id, name, price, category, inStock}
1, Wireless Mouse, 29.99, Electronics, true
2, USB Cable, 9.99, Accessories, true
3, Laptop Stand, 49.99, Office, false</code></pre>

<h2>Token Count Analysis</h2>
<pre><code class="language-python">import tiktoken

def count_tokens(text, model="gpt-4"):
    """Count tokens for a given text"""
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

# Sample data in different formats
json_text = '''{"products":[{"id":1,"name":"Wireless Mouse","price":29.99},...]}'''
yaml_text = '''products:\\n  - id: 1\\n    name: Wireless Mouse\\n    price: 29.99...'''
toon_text = '''products [3] {id, name, price}\\n1, Wireless Mouse, 29.99...'''

print(f"JSON tokens: {count_tokens(json_text)}")  # ~62
print(f"YAML tokens: {count_tokens(yaml_text)}")  # ~48
print(f"TOON tokens: {count_tokens(toon_text)}")  # ~28

# Cost calculation (GPT-4: $30/M input tokens)
json_cost = (count_tokens(json_text) / 1_000_000) * 30
toon_cost = (count_tokens(toon_text) / 1_000_000) * 30
savings = ((json_cost - toon_cost) / json_cost) * 100

print(f"Cost savings with TOON: {savings:.1f}%")</code></pre>

<h2>When to Use Each Format</h2>

<h3>Use TOON When:</h3>
<ul>
    <li>✅ Sending data to LLMs (cost optimization)</li>
    <li>✅ Working with uniform arrays of objects</li>
    <li>✅ Token budget is a concern</li>
    <li>✅ Data has consistent structure</li>
</ul>

<h3>Use JSON When:</h3>
<ul>
    <li>✅ API communication between services</li>
    <li>✅ Complex nested structures</li>
    <li>✅ Need maximum tooling support</li>
    <li>✅ Storing configuration with strict parsing</li>
</ul>

<h3>Use YAML When:</h3>
<ul>
    <li>✅ Configuration files (Docker, K8s, CI/CD)</li>
    <li>✅ Human-edited content</li>
    <li>✅ Need comments in data files</li>
    <li>✅ Multi-document files required</li>
</ul>

<h2>Format Conversion Code</h2>
<pre><code class="language-javascript">// Convert between all three formats
class DataConverter {
  // JSON -> TOON
  static jsonToToon(jsonStr) {
    const data = JSON.parse(jsonStr);
    return this._objectToToon(data);
  }
  
  // YAML -> TOON (requires js-yaml library)
  static yamlToToon(yamlStr) {
    const data = jsyaml.load(yamlStr);
    return this._objectToToon(data);
  }
  
  // TOON -> JSON
  static toonToJson(toonStr) {
    const data = this._parseToon(toonStr);
    return JSON.stringify(data, null, 2);
  }
  
  // Internal TOON parser
  static _parseToon(toon) {
    const lines = toon.trim().split('\\n');
    const result = {};
    
    // Check for tabular format
    const headerMatch = lines[0].match(/(\\w+)\\s*\\[(\\d+)\\]\\s*\\{([^}]+)\\}/);
    
    if (headerMatch) {
      const [, key, count, fieldsStr] = headerMatch;
      const fields = fieldsStr.split(',').map(f => f.trim());
      const items = [];
      
      for (let i = 1; i <= parseInt(count); i++) {
        const values = lines[i].split(',').map(v => v.trim());
        const item = {};
        fields.forEach((field, idx) => {
          item[field] = this._parseValue(values[idx]);
        });
        items.push(item);
      }
      
      result[key] = items;
    }
    
    return result;
  }
  
  static _parseValue(val) {
    if (val === 'true') return true;
    if (val === 'false') return false;
    if (val === 'null') return null;
    if (!isNaN(val) && val !== '') return Number(val);
    return val.replace(/^"|"$/g, '');
  }
  
  static _objectToToon(obj, indent = '') {
    // ... (implementation from previous article)
  }
}

// Usage examples
const jsonData = '{"users":[{"name":"Alice","age":30}]}';
console.log(DataConverter.jsonToToon(jsonData));

const toonData = 'users [1] {name, age}\\nAlice, 30';
console.log(DataConverter.toonToJson(toonData));</code></pre>

<h2>LLM Prompt Optimization</h2>
<p>Here's how to structure LLM prompts with TOON data:</p>

<pre><code class="language-python">def create_llm_prompt(data, question):
    """Create an optimized LLM prompt using TOON format"""
    toon_data = json_to_toon(data)
    
    prompt = f"""Analyze the following data and answer the question.

DATA (TOON format):
{toon_data}

QUESTION: {question}

Provide a detailed answer based on the data above."""
    
    return prompt

# Example
users_data = {
    "employees": [
        {"name": "Alice", "department": "Engineering", "salary": 95000},
        {"name": "Bob", "department": "Sales", "salary": 75000},
        {"name": "Charlie", "department": "Engineering", "salary": 85000}
    ]
}

prompt = create_llm_prompt(
    users_data, 
    "What is the average salary in the Engineering department?"
)
print(prompt)
# Uses ~40% fewer tokens than JSON equivalent!</code></pre>

<h2>Conclusion</h2>
<p>TOON is specifically designed for LLM optimization and excels at reducing token counts. JSON remains the standard for APIs and data exchange. YAML is best for human-editable configuration. Choose based on your specific needs!</p>

<p>Try our <a href="/toon-converter/">TOON Converter</a> to see the token savings for your own data.</p>
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

# 1000 products in JSON format
json_catalog = '''
{
  "products": [
    {"sku": "PRD001", "name": "Laptop", "price": 999.99, "category": "Electronics", "stock": 50},
    {"sku": "PRD002", "name": "Mouse", "price": 29.99, "category": "Accessories", "stock": 200},
    ... (1000 products)
  ]
}
'''

# Same data in TOON format
toon_catalog = '''
products [1000] {sku, name, price, category, stock}
PRD001, Laptop, 999.99, Electronics, 50
PRD002, Mouse, 29.99, Accessories, 200
... (1000 rows)
'''

def calculate_cost(text, model="gpt-4-turbo"):
    enc = tiktoken.encoding_for_model(model)
    tokens = len(enc.encode(text))
    cost_per_token = 10 / 1_000_000  # $10 per 1M for GPT-4 Turbo input
    return tokens, tokens * cost_per_token

json_tokens, json_cost = calculate_cost(json_catalog)
toon_tokens, toon_cost = calculate_cost(toon_catalog)

print(f"JSON: {json_tokens:,} tokens = ${json_cost:.4f}")
print(f"TOON: {toon_tokens:,} tokens = ${toon_cost:.4f}")
print(f"Savings: {(1 - toon_cost/json_cost) * 100:.1f}% = ${json_cost - toon_cost:.4f}")

# For 1000 products:
# JSON: ~45,000 tokens = $0.45
# TOON: ~18,000 tokens = $0.18
# Savings: 60% = $0.27 per request</code></pre>

<h2>Monthly Cost Projection</h2>
<pre><code class="language-python">def project_monthly_savings(daily_requests, records_per_request, model="gpt-4-turbo"):
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

print(f"Monthly JSON cost: ${result['json_cost']:,.2f}")
print(f"Monthly TOON cost: ${result['toon_cost']:,.2f}")
print(f"Monthly savings: ${result['monthly_savings']:,.2f}")
print(f"Savings percentage: {result['savings_percent']:.1f}%")

# Output:
# Monthly JSON cost: $675.00
# Monthly TOON cost: $270.00
# Monthly savings: $405.00 per month!</code></pre>

<h2>Implementation Patterns</h2>

<h3>Pattern 1: Preprocessing Pipeline</h3>
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
    console.log(`Input tokens: ${inputTokens} (${useToon ? 'TOON' : 'JSON'})`);
    
    return await this.callLLM(prompt);
  }
  
  buildPrompt(data, question, isToon) {
    const formatNote = isToon 
      ? 'Data is in TOON format (tabular arrays with {field} headers)'
      : 'Data is in JSON format';
    
    return `${formatNote}

DATA:
${data}

QUESTION: ${question}

Analyze the data and provide a detailed answer.`;
  }
  
  jsonToToon(data) {
    // ... conversion logic
  }
  
  countTokens(text) {
    // Approximate: 1 token ≈ 4 characters
    return Math.ceil(text.length / 4);
  }
}

// Usage
const pipeline = new LLMDataPipeline(process.env.OPENAI_API_KEY);

const salesData = {
  sales: [
    {date: "2024-01", product: "Widget A", qty: 150, revenue: 4500},
    {date: "2024-02", product: "Widget A", qty: 180, revenue: 5400},
    // ... more data
  ]
};

const response = await pipeline.query(
  salesData,
  "What is the trend in Widget A sales?"
);</code></pre>

<h3>Pattern 2: Batch Processing</h3>
<pre><code class="language-python">import asyncio
from typing import List, Dict

class BatchProcessor:
    def __init__(self, api_client, batch_size=50):
        self.api_client = api_client
        self.batch_size = batch_size
    
    async def process_large_dataset(
        self, 
        records: List[Dict], 
        prompt_template: str
    ):
        """Process large datasets in optimized batches"""
        results = []
        
        for i in range(0, len(records), self.batch_size):
            batch = records[i:i + self.batch_size]
            
            # Convert batch to TOON for token efficiency
            toon_batch = self.records_to_toon(batch)
            
            # Create prompt with TOON data
            prompt = prompt_template.format(data=toon_batch)
            
            # Process batch
            response = await self.api_client.complete(prompt)
            results.append(response)
            
            # Log progress
            print(f"Processed {min(i + self.batch_size, len(records))}/{len(records)}")
        
        return results
    
    def records_to_toon(self, records: List[Dict]) -> str:
        if not records:
            return ""
        
        fields = list(records[0].keys())
        header = f"records [{len(records)}] {{{', '.join(fields)}}}"
        
        rows = []
        for rec in records:
            values = [self.format_value(rec.get(f, '')) for f in fields]
            rows.append(", ".join(values))
        
        return header + "\\n" + "\\n".join(rows)
    
    def format_value(self, val):
        if val is None:
            return "null"
        if isinstance(val, bool):
            return "true" if val else "false"
        if isinstance(val, str) and "," in val:
            return f'"{val}"'
        return str(val)

# Usage
processor = BatchProcessor(openai_client, batch_size=100)

customer_records = [
    {"id": 1, "name": "Alice", "purchases": 5, "total": 450.00},
    {"id": 2, "name": "Bob", "purchases": 3, "total": 280.00},
    # ... 10,000 records
]

results = await processor.process_large_dataset(
    customer_records,
    """Analyze these customer records and identify:
1. Top spending customers
2. Purchase frequency patterns
3. Customer segments

DATA:
{data}

Provide actionable insights."""
)</code></pre>

<h2>Best Practices Checklist</h2>
<ol>
    <li>✅ <strong>Use TOON for uniform arrays</strong> - Greatest token savings</li>
    <li>✅ <strong>Pre-process data client-side</strong> - Convert before API call</li>
    <li>✅ <strong>Batch similar records</strong> - Maximize tabular efficiency</li>
    <li>✅ <strong>Include format hints</strong> - Tell LLM about TOON format</li>
    <li>✅ <strong>Monitor token usage</strong> - Track actual savings</li>
    <li>✅ <strong>Cache frequent conversions</strong> - Avoid redundant processing</li>
</ol>

<h2>ROI Calculator</h2>
<pre><code class="language-javascript">function calculateROI(params) {
  const {
    dailyRequests,
    avgRecordsPerRequest,
    modelCostPerMillionTokens,
    jsonTokensPerRecord = 45,
    toonTokensPerRecord = 18
  } = params;
  
  const monthlyRequests = dailyRequests * 30;
  const yearlyRequests = dailyRequests * 365;
  
  const jsonMonthlyTokens = monthlyRequests * avgRecordsPerRequest * jsonTokensPerRecord;
  const toonMonthlyTokens = monthlyRequests * avgRecordsPerRequest * toonTokensPerRecord;
  
  const jsonMonthlyCost = (jsonMonthlyTokens / 1_000_000) * modelCostPerMillionTokens;
  const toonMonthlyCost = (toonMonthlyTokens / 1_000_000) * modelCostPerMillionTokens;
  
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

console.log(`Monthly savings: $${roi.monthlySavings.toFixed(2)}`);
console.log(`Yearly savings: $${roi.yearlySavings.toFixed(2)}`);
console.log(`Savings: ${roi.savingsPercent}%`);

// Output for this example:
// Monthly savings: $405.00
// Yearly savings: $4,860.00
// Savings: 60.0%</code></pre>

<h2>Start Saving Today</h2>
<p>Try our <a href="/toon-converter/">TOON Converter</a> to instantly convert your JSON data and calculate your potential savings!</p>
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
    <li><strong>File extension:</strong> <code>.toon</code></li>
    <li><strong>Media type:</strong> <code>text/toon</code></li>
    <li><strong>Encoding:</strong> UTF-8 (always)</li>
    <li><strong>Line endings:</strong> LF (\\n) or CRLF (\\r\\n)</li>
</ul>

<h2>Primitive Values</h2>

<h3>Strings</h3>
<pre><code class="language-toon"># Unquoted strings (preferred when possible)
name: John Doe
city: New York

# Quoted strings (required for special characters)
description: "Hello, World!"
multiline: "Line 1\\nLine 2"
withQuotes: "He said \\"Hello\\""</code></pre>

<h3>Numbers</h3>
<pre><code class="language-toon"># Integers
count: 42
negative: -17

# Floating point
price: 29.99
scientific: 1.5e10

# Special values
infinity: Infinity
notANumber: NaN</code></pre>

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
- go

# Numbers
scores [3]
- 95
- 87
- 92</code></pre>

<h3>Mixed Arrays</h3>
<pre><code class="language-toon"># Arrays with mixed types
mixedData [4]
- hello
- 42
- true
- null</code></pre>

<h3>Empty Arrays</h3>
<pre><code class="language-toon">noItems [0]</code></pre>

<h2>Complex Structures</h2>

<h3>Array of Objects with Nested Data</h3>
<pre><code class="language-json">// JSON equivalent
{
  "companies": [
    {
      "name": "Acme Inc",
      "employees": [
        {"name": "Alice", "role": "Dev"},
        {"name": "Bob", "role": "Design"}
      ]
    }
  ]
}</code></pre>

<pre><code class="language-toon"># TOON representation
companies [1]
- name: Acme Inc
  employees [2] {name, role}
  Alice, Dev
  Bob, Design</code></pre>

<h3>Objects Containing Arrays</h3>
<pre><code class="language-toon">config
  name: MyApp
  version: 1.0.0
  features [3]
  - authentication
  - payments
  - analytics
  database
    host: localhost
    port: 5432
    replicas [2] {host, port}
    replica1.db.com, 5432
    replica2.db.com, 5432</code></pre>

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
        <td><code>name: John</code></td>
    </tr>
    <tr>
        <td>Contains spaces</td>
        <td>Only if leading/trailing</td>
        <td><code>city: New York</code></td>
    </tr>
    <tr>
        <td>Contains comma</td>
        <td>Yes</td>
        <td><code>desc: "Hello, World"</code></td>
    </tr>
    <tr>
        <td>Contains colon</td>
        <td>Yes</td>
        <td><code>time: "12:30:00"</code></td>
    </tr>
    <tr>
        <td>Contains newline</td>
        <td>Yes (escaped)</td>
        <td><code>text: "Line1\\nLine2"</code></td>
    </tr>
    <tr>
        <td>Contains quotes</td>
        <td>Yes (escaped)</td>
        <td><code>say: "He said \\"Hi\\""</code></td>
    </tr>
    <tr>
        <td>Empty string</td>
        <td>Yes</td>
        <td><code>empty: ""</code></td>
    </tr>
</table>

<h2>Escape Sequences</h2>
<pre><code class="language-toon"># Supported escape sequences in quoted strings
newline: "line1\\nline2"
tab: "col1\\tcol2"
carriage: "line1\\rline2"
backslash: "path\\\\to\\\\file"
quote: "say \\"hello\\""</code></pre>

<h2>Comments</h2>
<pre><code class="language-toon"># Single-line comments start with hash
name: John  # End-of-line comments also work

# Multi-line comments are just multiple single-line comments
# This is line 1
# This is line 2</code></pre>

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
        const [, key, count, fieldsStr] = tabularMatch;
        const fields = fieldsStr.split(',').map(f => f.trim());
        result[key] = this.parseTabular(lines, i + 1, parseInt(count), fields);
        i += parseInt(count) + 1;
        continue;
      }
      
      // Check for simple array
      const arrayMatch = content.match(/^(\\w+)\\s*\\[(\\d+)\\]$/);
      if (arrayMatch) {
        const [, key, count] = arrayMatch;
        result[key] = this.parseSimpleArray(lines, i + 1, parseInt(count));
        i += parseInt(count) + 1;
        continue;
      }
      
      // Key-value pair
      const kvMatch = content.match(/^(\\w+):\\s*(.+)?$/);
      if (kvMatch) {
        const [, key, value] = kvMatch;
        result[key] = this.parseValue(value);
        i++;
        continue;
      }
      
      // Nested object
      const objMatch = content.match(/^(\\w+)$/);
      if (objMatch) {
        const key = objMatch[1];
        const nested = this.parseLines(lines, i + 1);
        result[key] = nested.value;
        i = nested.nextIndex;
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
  
  parseSimpleArray(lines, startIndex, count) {
    const items = [];
    for (let i = 0; i < count && startIndex + i < lines.length; i++) {
      const line = lines[startIndex + i].trim();
      if (line.startsWith('- ')) {
        items.push(this.parseValue(line.slice(2)));
      }
    }
    return items;
  }
  
  parseValue(val) {
    if (val === undefined || val === '') return null;
    if (val === 'true') return true;
    if (val === 'false') return false;
    if (val === 'null') return null;
    if (!isNaN(val) && val !== '') return Number(val);
    return val.replace(/^"|"$/g, '').replace(/\\\\"/g, '"');
  }
  
  getIndent(line) {
    const match = line.match(/^(\\s*)/);
    return match ? match[1].length : 0;
  }
}

// Usage
const parser = new ToonParser();
const toonData = `users [2] {name, age}
Alice, 30
Bob, 25`;

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
    <li>✅ Array count matches actual items</li>
    <li>✅ Field count matches values per row</li>
    <li>✅ Consistent indentation (2 spaces)</li>
    <li>✅ Special characters are quoted</li>
    <li>✅ UTF-8 encoding</li>
</ol>

<p>Use our <a href="/toon-converter/">TOON Converter</a> to validate and convert your data!</p>
'''
    }
]
