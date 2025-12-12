"""
Management command to add new blog posts about JSON tools, programming, AI/ML, DevOps
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from formatter.models import BlogCategory, BlogPost


class Command(BaseCommand):
    help = 'Add new blog posts about JSON tools, programming, AI/ML, MLOps, DevOps'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding new blog posts...\n')
        
        # Ensure categories exist
        categories_data = [
            {'name': 'Web Development', 'description': 'Web technologies and frameworks'},
            {'name': 'DevOps', 'description': 'CI/CD, Docker, Kubernetes, and deployment'},
            {'name': 'AI & Machine Learning', 'description': 'AI, ML, and Deep Learning'},
            {'name': 'Python', 'description': 'Python programming tutorials'},
            {'name': 'Cloud Computing', 'description': 'AWS, Azure, GCP, and cloud architecture'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = BlogCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat
        
        all_posts = NEW_BLOG_POSTS
        
        created_count = 0
        for i, post_data in enumerate(all_posts, 1):
            category = categories.get(post_data['category'])
            if not category:
                self.stdout.write(f'  ⚠ Category not found: {post_data["category"]}')
                continue
            
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
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Created {created_count} new blog posts!'))
        self.stdout.write(f'📚 Total posts in database: {BlogPost.objects.count()}')


NEW_BLOG_POSTS = [
    # ===== JSON TOOLS POST =====
    {
        'category': 'Web Development',
        'title': '10 Best JSON Formatter Online Tools for Developers in 2025',
        'excerpt': 'Discover the top 10 JSON formatter tools that every developer needs. Compare features, performance, and find the perfect tool for formatting, validating, and beautifying JSON.',
        'content': '''
<p>JSON (JavaScript Object Notation) has become the universal language for data exchange in modern web development. Whether you're debugging API responses, configuring applications, or managing data pipelines, having a reliable JSON formatter is essential. In this comprehensive guide, we'll explore the 10 best JSON formatter tools available in 2025.</p>

<h2>Why You Need a Good JSON Formatter</h2>
<p>Raw JSON data is often minified or poorly formatted, making it nearly impossible to read. A good JSON formatter helps you:</p>
<ul>
    <li>Beautify and indent JSON for readability</li>
    <li>Validate JSON syntax and catch errors</li>
    <li>Minify JSON for production use</li>
    <li>Convert JSON to other formats</li>
    <li>Visualize complex nested structures</li>
</ul>

<h2>1. JSON Formatters Pro (jsonformatterspro.com)</h2>
<p>Our top pick for 2025! JSON Formatters Pro offers a comprehensive suite of JSON tools including:</p>
<pre><code class="language-json">
{
  "features": [
    "Beautiful syntax highlighting",
    "Real-time validation",
    "Tree view visualization",
    "JSON to YAML/XML conversion",
    "Schema validation",
    "Diff comparison"
  ],
  "pricing": "Free",
  "rating": 5.0
}
</code></pre>

<h3>Key Features:</h3>
<ul>
    <li><strong>JSON Formatter & Beautifier</strong> - Clean indentation with customizable spaces</li>
    <li><strong>JSON Validator</strong> - Instant error detection with line numbers</li>
    <li><strong>JSON to YAML Converter</strong> - Seamless format conversion</li>
    <li><strong>JSON Tree Viewer</strong> - Interactive collapsible tree view</li>
    <li><strong>JSON Diff</strong> - Compare two JSON documents side-by-side</li>
</ul>

<h2>2. JSONLint</h2>
<p>A classic JSON validator that's been trusted by developers for years. Simple interface, focuses purely on validation.</p>

<h2>3. JSON Editor Online</h2>
<p>Offers both code and tree views, making it easy to navigate complex JSON structures.</p>

<h2>4. Code Beautify JSON</h2>
<p>Part of a larger suite of code formatting tools. Good for quick formatting needs.</p>

<h2>5. JSON Viewer Chrome Extension</h2>
<p>Perfect for viewing JSON directly in your browser when testing APIs.</p>

<pre><code class="language-javascript">
// Example: Fetching and formatting JSON
const response = await fetch('https://api.example.com/data');
const data = await response.json();
console.log(JSON.stringify(data, null, 2)); // Formatted output
</code></pre>

<h2>6. Postman</h2>
<p>While primarily an API testing tool, Postman's built-in JSON formatter is excellent for API development.</p>

<h2>7. VS Code with JSON Extensions</h2>
<p>If you prefer your IDE, VS Code offers excellent JSON support with extensions like "Prettier" and "JSON Tools".</p>

<h2>8. jq (Command Line)</h2>
<p>For terminal enthusiasts, jq is a powerful JSON processor:</p>
<pre><code class="language-bash">
# Pretty print JSON
cat data.json | jq '.'

# Extract specific fields
cat data.json | jq '.users[].name'

# Filter data
cat data.json | jq '.items | map(select(.price > 100))'
</code></pre>

<h2>9. JSON Crack</h2>
<p>Visualizes JSON as interactive graphs - great for understanding complex data relationships.</p>

<h2>10. JSON Formatter by Curious Concept</h2>
<p>Fast, reliable, and handles large JSON files efficiently.</p>

<h2>Comparison Table</h2>
<table border="1" style="width:100%; border-collapse: collapse;">
    <tr>
        <th>Tool</th>
        <th>Validation</th>
        <th>Tree View</th>
        <th>Conversion</th>
        <th>Free</th>
    </tr>
    <tr>
        <td>JSON Formatters Pro</td>
        <td>✅</td>
        <td>✅</td>
        <td>✅</td>
        <td>✅</td>
    </tr>
    <tr>
        <td>JSONLint</td>
        <td>✅</td>
        <td>❌</td>
        <td>❌</td>
        <td>✅</td>
    </tr>
    <tr>
        <td>JSON Editor Online</td>
        <td>✅</td>
        <td>✅</td>
        <td>❌</td>
        <td>✅</td>
    </tr>
</table>

<h2>Tips for Working with JSON</h2>
<pre><code class="language-python">
import json

# Pretty print in Python
data = {"name": "John", "age": 30}
formatted = json.dumps(data, indent=4, sort_keys=True)
print(formatted)

# Validate JSON
try:
    json.loads(json_string)
    print("Valid JSON!")
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
</code></pre>

<h2>Conclusion</h2>
<p>For most developers, JSON Formatters Pro offers the best combination of features, speed, and ease of use. It's free, requires no installation, and handles all your JSON processing needs. Try it today at <a href="https://jsonformatterspro.com">jsonformatterspro.com</a>!</p>
        ''',
        'tags': 'json formatter, json tools, json beautifier, json validator, developer tools, json online',
        'meta_description': 'Discover the 10 best JSON formatter online tools for developers in 2025. Compare features, validation, and find your perfect JSON beautifier.',
        'meta_keywords': 'json formatter, best json formatter, json beautifier, json validator online, json tools 2025, format json online'
    },

    # ===== MLOps POST =====
    {
        'category': 'AI & Machine Learning',
        'title': 'MLOps Best Practices: Building Production-Ready ML Pipelines',
        'excerpt': 'Learn MLOps fundamentals including model versioning, CI/CD for ML, monitoring, and deployment strategies. Complete guide with code examples.',
        'content': '''
<p>MLOps (Machine Learning Operations) bridges the gap between ML development and production deployment. This guide covers essential practices for building robust ML systems.</p>

<h2>What is MLOps?</h2>
<p>MLOps applies DevOps principles to machine learning, focusing on:</p>
<ul>
    <li>Reproducible ML pipelines</li>
    <li>Model versioning and registry</li>
    <li>Automated testing and validation</li>
    <li>Continuous training and deployment</li>
    <li>Model monitoring and governance</li>
</ul>

<h2>1. ML Pipeline Architecture</h2>
<pre><code class="language-python">
# Example MLOps pipeline with Kubeflow
from kfp import dsl
from kfp.components import create_component_from_func

@dsl.component
def preprocess_data(input_path: str, output_path: str):
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    
    df = pd.read_csv(input_path)
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    df_scaled.to_csv(output_path, index=False)

@dsl.component
def train_model(data_path: str, model_path: str):
    import joblib
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd
    
    df = pd.read_csv(data_path)
    X, y = df.drop('target', axis=1), df['target']
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    
    joblib.dump(model, model_path)

@dsl.pipeline(name='ml-training-pipeline')
def ml_pipeline():
    preprocess_task = preprocess_data(input_path='raw_data.csv', 
                                       output_path='processed_data.csv')
    train_task = train_model(data_path=preprocess_task.outputs['output_path'],
                             model_path='model.pkl')
</code></pre>

<h2>2. Model Versioning with MLflow</h2>
<pre><code class="language-python">
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Start MLflow run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    # Log metrics
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(model, "random_forest_model")
    
    print(f"Model logged with accuracy: {accuracy:.4f}")
</code></pre>

<h2>3. CI/CD for Machine Learning</h2>
<pre><code class="language-yaml">
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly retraining

jobs:
  train-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run data validation
        run: python scripts/validate_data.py
      
      - name: Train model
        run: python scripts/train.py
      
      - name: Run model tests
        run: pytest tests/test_model.py
      
      - name: Deploy to staging
        if: success()
        run: python scripts/deploy.py --env staging
</code></pre>

<h2>4. Model Monitoring</h2>
<pre><code class="language-python">
from evidently import ColumnMapping
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab, ModelPerformanceTab

def monitor_model(reference_data, production_data, predictions):
    column_mapping = ColumnMapping()
    column_mapping.target = 'target'
    column_mapping.prediction = 'prediction'
    
    dashboard = Dashboard(tabs=[
        DataDriftTab(),
        ModelPerformanceTab()
    ])
    
    dashboard.calculate(reference_data, production_data, column_mapping)
    dashboard.save("monitoring_report.html")
    
    # Alert on significant drift
    drift_score = calculate_drift_score(reference_data, production_data)
    if drift_score > 0.3:
        send_alert("Data drift detected! Score: {:.2f}".format(drift_score))
</code></pre>

<h2>5. Feature Store with Feast</h2>
<pre><code class="language-python">
from feast import FeatureStore, Entity, Feature, FeatureView
from feast.types import Float64, Int64

# Define entity
customer = Entity(
    name="customer_id",
    join_key="customer_id",
    description="Customer identifier"
)

# Define feature view
customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    features=[
        Feature(name="total_purchases", dtype=Float64),
        Feature(name="avg_order_value", dtype=Float64),
        Feature(name="days_since_last_order", dtype=Int64),
    ],
    online=True,
    source=customer_data_source,
)

# Get features for inference
store = FeatureStore(repo_path="feature_repo/")
features = store.get_online_features(
    features=["customer_features:total_purchases", 
              "customer_features:avg_order_value"],
    entity_rows=[{"customer_id": 12345}]
)
</code></pre>

<h2>MLOps Tools Landscape</h2>
<table border="1" style="width:100%; border-collapse: collapse;">
    <tr>
        <th>Category</th>
        <th>Tools</th>
    </tr>
    <tr><td>Experiment Tracking</td><td>MLflow, Weights & Biases, Neptune</td></tr>
    <tr><td>Pipeline Orchestration</td><td>Kubeflow, Airflow, Prefect, Dagster</td></tr>
    <tr><td>Feature Store</td><td>Feast, Tecton, Hopsworks</td></tr>
    <tr><td>Model Serving</td><td>TensorFlow Serving, Seldon, BentoML</td></tr>
    <tr><td>Monitoring</td><td>Evidently, Arize, WhyLabs</td></tr>
</table>

<p>Implementing MLOps practices ensures your ML models are reliable, reproducible, and production-ready!</p>
        ''',
        'tags': 'mlops, machine learning, devops, ml pipeline, model deployment, mlflow',
        'meta_description': 'Learn MLOps best practices for building production ML pipelines. Model versioning, CI/CD, monitoring with code examples.',
        'meta_keywords': 'mlops, machine learning operations, ml pipeline, model deployment, mlflow, kubeflow'
    },

    # ===== DevOps Kubernetes POST =====
    {
        'category': 'DevOps',
        'title': 'Kubernetes for Beginners: Complete Guide to Container Orchestration',
        'excerpt': 'Master Kubernetes fundamentals including Pods, Deployments, Services, and ConfigMaps. Learn to deploy and manage containerized applications.',
        'content': '''
<p>Kubernetes (K8s) is the industry-standard container orchestration platform. This guide covers everything you need to get started with Kubernetes.</p>

<h2>Core Kubernetes Concepts</h2>

<h3>1. Pods - The Smallest Deployable Unit</h3>
<pre><code class="language-yaml">
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
  labels:
    app: my-app
spec:
  containers:
    - name: my-app
      image: nginx:latest
      ports:
        - containerPort: 80
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
        requests:
          memory: "64Mi"
          cpu: "250m"
</code></pre>

<pre><code class="language-bash">
# Create pod
kubectl apply -f pod.yaml

# View pods
kubectl get pods

# Describe pod details
kubectl describe pod my-app-pod

# View logs
kubectl logs my-app-pod
</code></pre>

<h3>2. Deployments - Managing Replicas</h3>
<pre><code class="language-yaml">
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:v1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
</code></pre>

<h3>3. Services - Exposing Applications</h3>
<pre><code class="language-yaml">
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer  # or ClusterIP, NodePort
</code></pre>

<h3>4. ConfigMaps and Secrets</h3>
<pre><code class="language-yaml">
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
  LOG_LEVEL: info
  MAX_CONNECTIONS: "100"

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  password: cGFzc3dvcmQxMjM=  # base64 encoded
  url: cG9zdGdyZXM6Ly9sb2NhbGhvc3Q6NTQzMg==
</code></pre>

<h3>5. Ingress - External Access</h3>
<pre><code class="language-yaml">
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-service
                port:
                  number: 80
</code></pre>

<h2>Essential kubectl Commands</h2>
<pre><code class="language-bash">
# Cluster info
kubectl cluster-info
kubectl get nodes

# Deployments
kubectl get deployments
kubectl rollout status deployment/my-app
kubectl rollout history deployment/my-app
kubectl rollout undo deployment/my-app

# Scaling
kubectl scale deployment my-app --replicas=5

# Debugging
kubectl exec -it pod-name -- /bin/sh
kubectl port-forward pod-name 8080:80
kubectl top pods
kubectl top nodes

# Apply configurations
kubectl apply -f kubernetes/
kubectl delete -f kubernetes/
</code></pre>

<h2>Helm Charts for Package Management</h2>
<pre><code class="language-bash">
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install application
helm install my-release bitnami/postgresql

# Create your own chart
helm create my-chart
helm package my-chart
helm install my-release ./my-chart
</code></pre>

<p>Kubernetes mastery opens doors to cloud-native development. Start with these fundamentals and gradually explore advanced topics!</p>
        ''',
        'tags': 'kubernetes, k8s, devops, container orchestration, docker, cloud native',
        'meta_description': 'Complete Kubernetes guide for beginners. Learn Pods, Deployments, Services, and kubectl commands with examples.',
        'meta_keywords': 'kubernetes tutorial, k8s beginners, kubernetes pods, kubernetes deployment, container orchestration'
    },

    # ===== AI LLM Fine-tuning POST =====
    {
        'category': 'AI & Machine Learning',
        'title': 'Fine-Tuning Large Language Models: A Practical Guide with Code',
        'excerpt': 'Learn to fine-tune LLMs like GPT, LLaMA, and Mistral for your specific use cases. Covers LoRA, QLoRA, and full fine-tuning techniques.',
        'content': '''
<p>Fine-tuning allows you to customize large language models for specific tasks, improving performance while reducing computational costs. This guide covers practical techniques with working code.</p>

<h2>Why Fine-Tune LLMs?</h2>
<ul>
    <li>Customize model behavior for specific domains</li>
    <li>Improve performance on specialized tasks</li>
    <li>Reduce inference costs with smaller, focused models</li>
    <li>Add company-specific knowledge and terminology</li>
</ul>

<h2>1. Setting Up the Environment</h2>
<pre><code class="language-bash">
# Install required packages
pip install torch transformers datasets peft accelerate bitsandbytes

# For QLoRA (4-bit quantization)
pip install -U bitsandbytes
</code></pre>

<h2>2. Preparing Your Dataset</h2>
<pre><code class="language-python">
from datasets import Dataset
import json

# Prepare instruction-following dataset
training_data = [
    {
        "instruction": "Summarize the following text:",
        "input": "The quick brown fox jumps over the lazy dog...",
        "output": "A fox jumps over a dog."
    },
    {
        "instruction": "Translate to French:",
        "input": "Hello, how are you?",
        "output": "Bonjour, comment allez-vous?"
    }
]

def format_prompt(example):
    return {
        "text": f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
    }

dataset = Dataset.from_list(training_data)
dataset = dataset.map(format_prompt)
</code></pre>

<h2>3. LoRA Fine-Tuning (Efficient)</h2>
<pre><code class="language-python">
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# Load base model
model_name = "meta-llama/Llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# LoRA configuration
lora_config = LoraConfig(
    r=16,                    # Rank
    lora_alpha=32,           # Alpha for scaling
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    optim="adamw_torch"
)

# Train
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer,
    dataset_text_field="text",
    max_seq_length=512
)

trainer.train()
model.save_pretrained("./fine-tuned-model")
</code></pre>

<h2>4. QLoRA (4-bit Quantized Fine-Tuning)</h2>
<pre><code class="language-python">
from transformers import BitsAndBytesConfig

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# Load 4-bit quantized model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

# Prepare for k-bit training
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

# Train as before...
</code></pre>

<h2>5. Inference with Fine-Tuned Model</h2>
<pre><code class="language-python">
from peft import PeftModel

# Load fine-tuned model
base_model = AutoModelForCausalLM.from_pretrained(model_name)
model = PeftModel.from_pretrained(base_model, "./fine-tuned-model")
model = model.merge_and_unload()  # Merge LoRA weights

# Generate
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

response = generate_response("Summarize the benefits of exercise:")
print(response)
</code></pre>

<h2>Fine-Tuning Comparison</h2>
<table border="1" style="width:100%; border-collapse: collapse;">
    <tr><th>Method</th><th>VRAM Required</th><th>Training Time</th><th>Quality</th></tr>
    <tr><td>Full Fine-Tuning</td><td>80GB+</td><td>Long</td><td>Best</td></tr>
    <tr><td>LoRA</td><td>16-24GB</td><td>Medium</td><td>Very Good</td></tr>
    <tr><td>QLoRA (4-bit)</td><td>8-12GB</td><td>Medium</td><td>Good</td></tr>
</table>

<p>Start with QLoRA for experimentation, then scale up as needed for production!</p>
        ''',
        'tags': 'llm, fine-tuning, lora, qlora, gpt, machine learning, transformers',
        'meta_description': 'Learn to fine-tune LLMs with LoRA and QLoRA. Practical guide with code for GPT, LLaMA, and Mistral fine-tuning.',
        'meta_keywords': 'llm fine-tuning, lora fine-tuning, qlora, llama fine-tune, gpt customization'
    },

    # ===== CI/CD Pipeline POST =====
    {
        'category': 'DevOps',
        'title': 'Building Modern CI/CD Pipelines with GitHub Actions',
        'excerpt': 'Create robust CI/CD pipelines using GitHub Actions. Learn workflows, testing, deployment, and best practices with real-world examples.',
        'content': '''
<p>GitHub Actions provides powerful automation for CI/CD pipelines directly in your repository. This guide covers practical workflows for modern development.</p>

<h2>Basic CI Workflow</h2>
<pre><code class="language-yaml">
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Cache pip packages
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-report=html
      
      - name: Upload coverage report
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
</code></pre>

<h2>Docker Build and Push</h2>
<pre><code class="language-yaml">
# .github/workflows/docker.yml
name: Docker Build

on:
  push:
    tags: ['v*']

jobs:
  build-push:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: username/my-app
          tags: |
            type=semver,pattern={{version}}
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
</code></pre>

<h2>Complete CD Pipeline with Kubernetes</h2>
<pre><code class="language-yaml">
# .github/workflows/cd.yml
name: Deploy to Production

on:
  release:
    types: [published]

env:
  CLUSTER_NAME: production-cluster
  NAMESPACE: my-app

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name $CLUSTER_NAME
      
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/my-app \
            my-app=username/my-app:${{ github.event.release.tag_name }} \
            -n $NAMESPACE
          
          kubectl rollout status deployment/my-app -n $NAMESPACE
      
      - name: Run smoke tests
        run: |
          ./scripts/smoke-tests.sh
      
      - name: Notify on Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#deployments'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
</code></pre>

<h2>Reusable Workflows</h2>
<pre><code class="language-yaml">
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
    secrets:
      api-key:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: pytest
        env:
          API_KEY: ${{ secrets.api-key }}

# Usage in another workflow:
# jobs:
#   call-tests:
#     uses: ./.github/workflows/reusable-test.yml
#     with:
#       python-version: '3.11'
#     secrets:
#       api-key: ${{ secrets.API_KEY }}
</code></pre>

<h2>Security Scanning</h2>
<pre><code class="language-yaml">
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
      
      - name: Run CodeQL analysis
        uses: github/codeql-action/analyze@v2
</code></pre>

<p>Well-designed CI/CD pipelines save time and improve code quality. Start simple and iterate!</p>
        ''',
        'tags': 'cicd, github actions, devops, automation, deployment, kubernetes',
        'meta_description': 'Build robust CI/CD pipelines with GitHub Actions. Complete guide with testing, Docker, Kubernetes deployment examples.',
        'meta_keywords': 'github actions, ci cd pipeline, devops automation, github workflow, continuous deployment'
    },

    # ===== Python FastAPI POST =====
    {
        'category': 'Python',
        'title': 'Building REST APIs with FastAPI: Complete Tutorial',
        'excerpt': 'Learn to build high-performance REST APIs with Python FastAPI. Covers routing, validation, authentication, database integration, and deployment.',
        'content': '''
<p>FastAPI is a modern, high-performance Python web framework for building APIs. It offers automatic validation, documentation, and async support out of the box.</p>

<h2>Getting Started</h2>
<pre><code class="language-bash">
pip install fastapi uvicorn sqlalchemy pydantic
</code></pre>

<h2>Basic API Structure</h2>
<pre><code class="language-python">
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="My API",
    description="A sample FastAPI application",
    version="1.0.0"
)

# Pydantic models for validation
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    
class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# In-memory database
items_db = {}
item_counter = 0

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    global item_counter
    item_counter += 1
    new_item = Item(
        id=item_counter,
        created_at=datetime.now(),
        **item.dict()
    )
    items_db[item_counter] = new_item
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = Item(
        id=item_id,
        created_at=items_db[item_id].created_at,
        **item.dict()
    )
    items_db[item_id] = updated
    return updated

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted"}
</code></pre>

<h2>Database Integration with SQLAlchemy</h2>
<pre><code class="language-python">
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemModel(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
</code></pre>

<h2>Authentication with JWT</h2>
<pre><code class="language-python">
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Validate user credentials
    token = create_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {user['sub']}!"}
</code></pre>

<h2>Run the Server</h2>
<pre><code class="language-bash">
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
</code></pre>

<p>FastAPI auto-generates OpenAPI docs at /docs. It's production-ready out of the box!</p>
        ''',
        'tags': 'fastapi, python, rest api, web development, backend',
        'meta_description': 'Complete FastAPI tutorial for building REST APIs with Python. Covers routing, validation, authentication, and database integration.',
        'meta_keywords': 'fastapi tutorial, python rest api, fastapi authentication, python backend'
    },

    # ===== Terraform IaC POST =====
    {
        'category': 'DevOps',
        'title': 'Infrastructure as Code with Terraform: AWS Complete Guide',
        'excerpt': 'Master Terraform for AWS infrastructure automation. Learn modules, state management, and production-ready IaC patterns.',
        'content': '''
<p>Terraform enables you to define cloud infrastructure as code, ensuring consistency and repeatability across environments.</p>

<h2>Basic AWS Infrastructure</h2>
<pre><code class="language-hcl">
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  default = "us-east-1"
}

variable "environment" {
  default = "production"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

# Subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.environment}-public-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "${var.environment}-private-${count.index + 1}"
  }
}
</code></pre>

<h2>EC2 with Auto Scaling</h2>
<pre><code class="language-hcl">
# ec2.tf
resource "aws_launch_template" "app" {
  name_prefix   = "${var.environment}-app"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = "t3.medium"
  
  vpc_security_group_ids = [aws_security_group.app.id]
  
  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    docker run -d -p 80:8080 my-app:latest
  EOF
  )
  
  iam_instance_profile {
    name = aws_iam_instance_profile.app.name
  }
  
  tags = {
    Environment = var.environment
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "${var.environment}-app-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  desired_capacity    = 2
  min_size            = 1
  max_size            = 10
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  target_group_arns = [aws_lb_target_group.app.arn]
  
  tag {
    key                 = "Name"
    value               = "${var.environment}-app"
    propagate_at_launch = true
  }
}

# Auto Scaling Policy
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  autoscaling_group_name = aws_autoscaling_group.app.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = 1
  cooldown               = 300
}
</code></pre>

<h2>RDS Database</h2>
<pre><code class="language-hcl">
# rds.tf
resource "aws_db_instance" "main" {
  identifier           = "${var.environment}-db"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = "db.t3.medium"
  allocated_storage    = 20
  max_allocated_storage = 100
  
  db_name  = "myapp"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"
  
  multi_az               = true
  deletion_protection    = true
  skip_final_snapshot    = false
  
  tags = {
    Environment = var.environment
  }
}
</code></pre>

<h2>Modules for Reusability</h2>
<pre><code class="language-hcl">
# modules/vpc/main.tf
variable "cidr_block" {}
variable "environment" {}

resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  tags = { Name = "${var.environment}-vpc" }
}

output "vpc_id" {
  value = aws_vpc.this.id
}

# Usage in main.tf
module "vpc" {
  source      = "./modules/vpc"
  cidr_block  = "10.0.0.0/16"
  environment = "production"
}
</code></pre>

<h2>Terraform Commands</h2>
<pre><code class="language-bash">
# Initialize
terraform init

# Plan changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Destroy infrastructure
terraform destroy

# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Import existing resources
terraform import aws_instance.example i-1234567890abcdef0
</code></pre>

<p>Terraform makes infrastructure reproducible and version-controlled. Start with modules for maintainability!</p>
        ''',
        'tags': 'terraform, infrastructure as code, aws, devops, cloud, iac',
        'meta_description': 'Complete Terraform AWS tutorial. Learn infrastructure as code with VPC, EC2, RDS, and module patterns.',
        'meta_keywords': 'terraform tutorial, aws terraform, infrastructure as code, terraform modules, iac'
    },

    # ===== RAG Systems POST =====
    {
        'category': 'AI & Machine Learning',
        'title': 'Building RAG Systems: Retrieval-Augmented Generation with LangChain',
        'excerpt': 'Learn to build RAG applications that combine LLMs with your own data. Covers vector databases, embeddings, and LangChain implementation.',
        'content': '''
<p>Retrieval-Augmented Generation (RAG) enhances LLMs by retrieving relevant context from your documents before generating responses. This guide shows how to build production-ready RAG systems.</p>

<h2>RAG Architecture Overview</h2>
<ol>
    <li>Load and split documents</li>
    <li>Generate embeddings</li>
    <li>Store in vector database</li>
    <li>Retrieve relevant chunks</li>
    <li>Generate response with context</li>
</ol>

<h2>Setting Up</h2>
<pre><code class="language-bash">
pip install langchain langchain-openai chromadb tiktoken pypdf
</code></pre>

<h2>Document Loading and Splitting</h2>
<pre><code class="language-python">
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load PDFs
loader = DirectoryLoader(
    "./documents/",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks from {len(documents)} documents")
</code></pre>

<h2>Creating Embeddings and Vector Store</h2>
<pre><code class="language-python">
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# For persistence
vectorstore.persist()

# Load existing vectorstore
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
</code></pre>

<h2>Building the RAG Chain</h2>
<pre><code class="language-python">
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Custom prompt template
template = """Use the following context to answer the question.
If you don't know the answer, say you don't know.

Context: {context}

Question: {question}

Answer:"""

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# Build RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)

# Query
result = qa_chain({"query": "What is the main topic of these documents?"})
print(result["result"])
print("\\nSources:")
for doc in result["source_documents"]:
    print(f"- {doc.metadata['source']}: {doc.page_content[:100]}...")
</code></pre>

<h2>Advanced: Conversational RAG</h2>
<pre><code class="language-python">
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

conversational_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True
)

# Chat
response1 = conversational_chain({"question": "What is RAG?"})
response2 = conversational_chain({"question": "How does it improve LLMs?"})
</code></pre>

<h2>Using Pinecone for Production</h2>
<pre><code class="language-python">
from langchain.vectorstores import Pinecone
import pinecone

pinecone.init(
    api_key="your-api-key",
    environment="your-environment"
)

vectorstore = Pinecone.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name="my-rag-index"
)
</code></pre>

<h2>Evaluation and Optimization</h2>
<pre><code class="language-python">
from langchain.evaluation import load_evaluator

# Evaluate relevance
evaluator = load_evaluator("relevance")

# Test retrieval quality
def evaluate_retrieval(question):
    docs = retriever.get_relevant_documents(question)
    for i, doc in enumerate(docs):
        score = evaluator.evaluate_strings(
            input=question,
            prediction=doc.page_content
        )
        print(f"Doc {i+1} relevance: {score['score']}")
</code></pre>

<p>RAG systems give LLMs access to your private data while maintaining accuracy. Experiment with chunk sizes and retrieval strategies!</p>
        ''',
        'tags': 'rag, langchain, llm, vector database, embeddings, ai',
        'meta_description': 'Build RAG systems with LangChain. Complete guide to retrieval-augmented generation with vector databases and LLMs.',
        'meta_keywords': 'rag tutorial, langchain rag, retrieval augmented generation, vector database, llm context'
    },
]
