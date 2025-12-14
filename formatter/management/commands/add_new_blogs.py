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
<p>Kubernetes (K8s) is the industry-standard container orchestration platform. This guide covers everything you need to get started with Kubernetes, from basic concepts to advanced deployment strategies.</p>

<h2>What is Kubernetes?</h2>
<p>Kubernetes is an open-source container orchestration platform originally developed by Google and now maintained by the Cloud Native Computing Foundation (CNCF). It automates the deployment, scaling, and management of containerized applications. The name Kubernetes originates from Greek, meaning helmsman or pilot. K8s is a common abbreviation derived by counting the eight letters between K and s.</p>

<p>Kubernetes provides a framework to run distributed systems resiliently. It takes care of scaling requirements, failover, deployment patterns, and more. Whether you are running a simple web application or a complex microservices architecture, Kubernetes provides the tools you need to manage your workloads effectively.</p>

<h2>Why Use Kubernetes?</h2>
<p>Container technology revolutionized how we package and deploy applications. However, managing containers at scale presents significant challenges. Kubernetes solves these challenges by providing:</p>

<ul>
    <li><strong>Service Discovery and Load Balancing</strong> - Kubernetes can expose containers using DNS names or IP addresses. When traffic is high, Kubernetes load balances and distributes network traffic.</li>
    <li><strong>Storage Orchestration</strong> - Automatically mount storage systems including local storage, cloud providers, and network storage.</li>
    <li><strong>Automated Rollouts and Rollbacks</strong> - Describe the desired state and Kubernetes changes the actual state at a controlled rate.</li>
    <li><strong>Automatic Bin Packing</strong> - Place containers based on resource requirements while maximizing utilization.</li>
    <li><strong>Self-Healing</strong> - Restart failed containers, replace and reschedule containers when nodes die.</li>
    <li><strong>Secret and Configuration Management</strong> - Store and manage sensitive information without rebuilding images.</li>
</ul>

<h2>Kubernetes Architecture</h2>
<p>A Kubernetes cluster consists of a control plane and worker nodes. Understanding this architecture is essential for troubleshooting and optimization.</p>

<h3>Control Plane Components</h3>

<h4>kube-apiserver</h4>
<p>The API server exposes the Kubernetes API. All communication in the cluster goes through the API server. It validates and processes requests, then updates etcd.</p>

<h4>etcd</h4>
<p>A consistent and highly-available key-value store used as Kubernetes' backing store for all cluster data. Always back up etcd in production.</p>

<h4>kube-scheduler</h4>
<p>Watches for newly created Pods with no assigned node and selects a node for them to run on based on resource requirements, constraints, and policies.</p>

<h4>kube-controller-manager</h4>
<p>Runs controller processes including Node Controller, Replication Controller, Endpoints Controller, and Service Account Controller.</p>

<h3>Worker Node Components</h3>

<h4>kubelet</h4>
<p>An agent that runs on each node ensuring containers are running in a Pod. It receives PodSpecs and ensures containers described are running and healthy.</p>

<h4>kube-proxy</h4>
<p>A network proxy that runs on each node maintaining network rules for Pod communication inside and outside the cluster.</p>

<h4>Container Runtime</h4>
<p>Software responsible for running containers. Kubernetes supports containerd, CRI-O, and other Container Runtime Interface implementations.</p>

<h2>Core Kubernetes Concepts</h2>

<h3>1. Pods - The Smallest Deployable Unit</h3>
<p>A Pod is the smallest deployable unit in Kubernetes. It represents a single instance of a running process and can contain one or more containers that share storage and network resources.</p>

<pre><code class="language-yaml">
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
  labels:
    app: my-app
    environment: production
    tier: frontend
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
      env:
        - name: LOG_LEVEL
          value: "info"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: app-config
</code></pre>

<pre><code class="language-bash">
# Create pod
kubectl apply -f pod.yaml

# View pods
kubectl get pods
kubectl get pods -o wide

# Describe pod details
kubectl describe pod my-app-pod

# View logs
kubectl logs my-app-pod
kubectl logs my-app-pod -f  # Follow logs

# Execute command in pod
kubectl exec -it my-app-pod -- /bin/bash

# Delete pod
kubectl delete pod my-app-pod
</code></pre>

<h3>2. Deployments - Managing Replicas</h3>
<p>Deployments provide declarative updates for Pods and ReplicaSets. They manage the lifecycle of your application, ensuring the specified number of replicas are running at all times.</p>

<pre><code class="language-yaml">
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
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
          resources:
            requests:
              memory: "128Mi"
              cpu: "250m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            successThreshold: 1
</code></pre>

<pre><code class="language-bash">
# Apply deployment
kubectl apply -f deployment.yaml

# View deployments
kubectl get deployments
kubectl get deploy

# Watch rollout status
kubectl rollout status deployment/my-app-deployment

# View rollout history
kubectl rollout history deployment/my-app-deployment

# Scale deployment
kubectl scale deployment my-app-deployment --replicas=5

# Update image
kubectl set image deployment/my-app-deployment my-app=my-app:v2.0.0

# Rollback to previous version
kubectl rollout undo deployment/my-app-deployment

# Rollback to specific revision
kubectl rollout undo deployment/my-app-deployment --to-revision=2
</code></pre>

<h3>3. Services - Exposing Applications</h3>
<p>A Service provides a stable network endpoint for accessing a set of Pods. Services enable load balancing and service discovery.</p>

<h4>Service Types</h4>
<ul>
    <li><strong>ClusterIP</strong> (default) - Internal cluster IP, only accessible within the cluster</li>
    <li><strong>NodePort</strong> - Exposes service on each node's IP at a static port</li>
    <li><strong>LoadBalancer</strong> - Exposes service using cloud provider's load balancer</li>
    <li><strong>ExternalName</strong> - Maps service to a DNS name</li>
</ul>

<pre><code class="language-yaml">
# ClusterIP Service
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
  type: ClusterIP

---
# NodePort Service
apiVersion: v1
kind: Service
metadata:
  name: my-app-nodeport
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
      nodePort: 30080
  type: NodePort

---
# LoadBalancer Service
apiVersion: v1
kind: Service
metadata:
  name: my-app-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
</code></pre>

<h3>4. ConfigMaps and Secrets</h3>
<p>ConfigMaps store non-confidential configuration data. Secrets store sensitive data like passwords and API keys.</p>

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
  database.properties: |
    host=db.example.com
    port=5432
    pool_size=10

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

---
# Using ConfigMap and Secret in a Pod
apiVersion: v1
kind: Pod
metadata:
  name: app-with-config
spec:
  containers:
    - name: app
      image: my-app:latest
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: db-secret
      volumeMounts:
        - name: config-volume
          mountPath: /etc/app-config
  volumes:
    - name: config-volume
      configMap:
        name: app-config
</code></pre>

<pre><code class="language-bash">
# Create ConfigMap from literal values
kubectl create configmap app-config --from-literal=APP_ENV=production

# Create ConfigMap from file
kubectl create configmap app-config --from-file=config.properties

# Create Secret
kubectl create secret generic db-secret --from-literal=password=secret123

# View ConfigMaps and Secrets
kubectl get configmaps
kubectl get secrets
kubectl describe secret db-secret
</code></pre>

<h3>5. Namespaces</h3>
<p>Namespaces provide a way to divide cluster resources between multiple users or teams. They provide scope for names and can have resource quotas.</p>

<pre><code class="language-yaml">
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production

---
# ResourceQuota for namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"
</code></pre>

<pre><code class="language-bash">
# Create namespace
kubectl create namespace production

# List namespaces
kubectl get namespaces

# Set default namespace
kubectl config set-context --current --namespace=production

# Deploy to specific namespace
kubectl apply -f deployment.yaml -n production

# View resources in namespace
kubectl get all -n production
</code></pre>

<h3>6. Ingress - External Access</h3>
<p>Ingress manages external HTTP/HTTPS access to services. It provides load balancing, SSL termination, and name-based virtual hosting.</p>

<pre><code class="language-yaml">
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - myapp.example.com
        - api.example.com
      secretName: app-tls-secret
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
    - host: api.example.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: api-v1-service
                port:
                  number: 80
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: api-v2-service
                port:
                  number: 80
</code></pre>

<h2>Persistent Storage</h2>
<p>Kubernetes provides persistent storage through PersistentVolumes (PV) and PersistentVolumeClaims (PVC).</p>

<pre><code class="language-yaml">
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard

---
# Pod using PVC
apiVersion: v1
kind: Pod
metadata:
  name: app-with-storage
spec:
  containers:
    - name: app
      image: my-app:latest
      volumeMounts:
        - name: data-volume
          mountPath: /data
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: app-data-pvc
</code></pre>

<h2>Essential kubectl Commands</h2>
<pre><code class="language-bash">
# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl get nodes -o wide

# Viewing resources
kubectl get all
kubectl get pods,svc,deploy
kubectl get pods -w  # Watch for changes

# Debugging
kubectl describe pod pod-name
kubectl logs pod-name
kubectl logs pod-name -c container-name
kubectl logs pod-name --previous

# Executing commands
kubectl exec -it pod-name -- /bin/sh
kubectl exec pod-name -- cat /etc/config

# Port forwarding
kubectl port-forward pod-name 8080:80
kubectl port-forward svc/service-name 8080:80

# Resource usage
kubectl top pods
kubectl top nodes

# Labels and selectors
kubectl get pods -l app=my-app
kubectl get pods -l environment=production,tier=frontend

# Apply and delete
kubectl apply -f kubernetes/
kubectl delete -f kubernetes/
kubectl delete pod pod-name --grace-period=0 --force
</code></pre>

<h2>Helm Charts for Package Management</h2>
<p>Helm is the package manager for Kubernetes. It helps you define, install, and upgrade complex Kubernetes applications.</p>

<pre><code class="language-bash">
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search for charts
helm search repo nginx

# Install application
helm install my-nginx bitnami/nginx

# Install with custom values
helm install my-release bitnami/postgresql --set auth.postgresPassword=secret

# List releases
helm list

# Upgrade release
helm upgrade my-release bitnami/postgresql

# Rollback
helm rollback my-release 1

# Uninstall
helm uninstall my-release

# Create your own chart
helm create my-chart
</code></pre>

<h2>Best Practices</h2>

<h3>Resource Management</h3>
<ul>
    <li>Always set resource requests and limits</li>
    <li>Use horizontal pod autoscaling (HPA)</li>
    <li>Implement pod disruption budgets</li>
</ul>

<h3>Security</h3>
<ul>
    <li>Use RBAC for access control</li>
    <li>Run containers as non-root</li>
    <li>Scan images for vulnerabilities</li>
    <li>Use network policies</li>
</ul>

<h3>Reliability</h3>
<ul>
    <li>Define liveness and readiness probes</li>
    <li>Use multiple replicas</li>
    <li>Spread pods across nodes with anti-affinity</li>
</ul>

<h2>Troubleshooting</h2>
<pre><code class="language-bash">
# Pod not starting
kubectl describe pod pod-name
kubectl get events --sort-by=.metadata.creationTimestamp

# Application errors
kubectl logs pod-name
kubectl logs pod-name --previous

# Network issues
kubectl get endpoints service-name
kubectl run debug --rm -it --image=alpine -- wget -qO- http://service-name

# Resource issues
kubectl top pods
kubectl describe node node-name
</code></pre>

<p>Kubernetes mastery opens doors to cloud-native development. Start with these fundamentals and gradually explore advanced topics like operators, custom resources, and service mesh!</p>
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
<p>GitHub Actions provides powerful automation for CI/CD pipelines directly in your repository. This guide covers practical workflows for modern development, from basic testing to production deployments.</p>

<h2>What is CI/CD?</h2>
<p>CI/CD stands for Continuous Integration and Continuous Delivery/Deployment. These practices automate the process of integrating code changes, testing them, and deploying to production environments.</p>

<h3>Continuous Integration (CI)</h3>
<p>CI automates the process of integrating code changes from multiple contributors. Every commit triggers automated builds and tests, providing rapid feedback on code quality.</p>

<h3>Continuous Delivery (CD)</h3>
<p>CD ensures code is always in a deployable state. After passing all tests, code can be deployed to production with a manual approval step.</p>

<h3>Continuous Deployment</h3>
<p>Takes CD further by automatically deploying every change that passes all tests directly to production without manual intervention.</p>

<h2>GitHub Actions Fundamentals</h2>
<p>GitHub Actions uses YAML files stored in the .github/workflows directory. Each file defines a workflow that responds to specific events.</p>

<h3>Key Concepts</h3>
<ul>
    <li><strong>Workflow</strong> - An automated process defined in YAML</li>
    <li><strong>Event</strong> - Triggers that start a workflow (push, pull_request, schedule)</li>
    <li><strong>Job</strong> - A set of steps that execute on the same runner</li>
    <li><strong>Step</strong> - An individual task that runs commands or actions</li>
    <li><strong>Action</strong> - A reusable unit of code</li>
    <li><strong>Runner</strong> - The server that runs the workflow</li>
</ul>

<h2>Basic CI Workflow</h2>
<p>Here is a comprehensive CI workflow that tests a Python application across multiple Python versions:</p>

<pre><code class="language-yaml">
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION_DEFAULT: '3.11'

jobs:
  lint:
    name: Code Linting
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION_DEFAULT }}
      
      - name: Install linting tools
        run: pip install flake8 black isort mypy
      
      - name: Run Black
        run: black --check src/
      
      - name: Run isort
        run: isort --check-only src/
      
      - name: Run Flake8
        run: flake8 src/
      
      - name: Run MyPy
        run: mypy src/

  test:
    name: Tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    needs: lint
    
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
        os: [ubuntu-latest]
        include:
          - python-version: '3.11'
            os: macos-latest
          - python-version: '3.11'
            os: windows-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist
      
      - name: Run tests with coverage
        run: |
          pytest tests/ -v --cov=src --cov-report=xml --cov-report=html -n auto
      
      - name: Upload coverage report
        if: matrix.python-version == '3.11' && matrix.os == 'ubuntu-latest'
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          flags: unittests
          fail_ci_if_error: true

  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: test
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION_DEFAULT }}
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run integration tests
        run: pytest tests/integration/ -v
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
</code></pre>

<h2>Docker Build and Push</h2>
<p>Building and pushing Docker images is a common CI/CD task. This workflow builds multi-platform images with caching:</p>

<pre><code class="language-yaml">
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix=
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            VERSION=${{ github.ref_name }}
            COMMIT_SHA=${{ github.sha }}

  scan:
    name: Security Scan
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name != 'pull_request'
    
    steps:
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
</code></pre>

<h2>Complete CD Pipeline with Kubernetes</h2>
<p>This workflow deploys to Kubernetes using environments for staging and production:</p>

<pre><code class="language-yaml">
# .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    name: Build Image
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.version }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build and push image
        # ... (same as docker build workflow)

  deploy-staging:
    name: Deploy to Staging
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name staging-cluster
      
      - name: Deploy with Helm
        run: |
          helm upgrade --install my-app ./helm/my-app \
            --namespace staging \
            --set image.tag=${{ needs.build.outputs.image-tag }} \
            --set environment=staging \
            --wait --timeout 10m
      
      - name: Verify deployment
        run: |
          kubectl rollout status deployment/my-app -n staging
          kubectl get pods -n staging -l app=my-app
      
      - name: Run smoke tests
        run: |
          sleep 30
          curl -f https://staging.example.com/health

  deploy-production:
    name: Deploy to Production
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    environment:
      name: production
      url: https://example.com
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name production-cluster
      
      - name: Deploy with Helm
        run: |
          helm upgrade --install my-app ./helm/my-app \
            --namespace production \
            --set image.tag=${{ needs.build.outputs.image-tag }} \
            --set environment=production \
            --set replicas=3 \
            --wait --timeout 15m
      
      - name: Verify deployment
        run: kubectl rollout status deployment/my-app -n production
      
      - name: Notify on Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#deployments'
          fields: repo,message,commit,author,action,workflow
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
</code></pre>

<h2>Reusable Workflows</h2>
<p>Reusable workflows allow you to share workflow logic across repositories:</p>

<pre><code class="language-yaml">
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
      run-integration-tests:
        required: false
        type: boolean
        default: false
    secrets:
      api-key:
        required: false
    outputs:
      coverage:
        description: "Code coverage percentage"
        value: ${{ jobs.test.outputs.coverage }}

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      coverage: ${{ steps.coverage.outputs.total }}
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt pytest pytest-cov
      
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=json
      
      - name: Extract coverage
        id: coverage
        run: |
          COVERAGE=$(python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered_display'])")
          echo "total=$COVERAGE" >> $GITHUB_OUTPUT
      
      - name: Run integration tests
        if: inputs.run-integration-tests
        run: pytest tests/integration/ -v
        env:
          API_KEY: ${{ secrets.api-key }}
</code></pre>

<pre><code class="language-yaml">
# Calling the reusable workflow
name: CI
on: [push]

jobs:
  test-python-39:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: '3.9'
  
  test-python-311:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: '3.11'
      run-integration-tests: true
    secrets:
      api-key: ${{ secrets.API_KEY }}
</code></pre>

<h2>Security Scanning</h2>
<p>Automate security scanning to catch vulnerabilities early:</p>

<pre><code class="language-yaml">
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  dependency-scan:
    name: Dependency Vulnerabilities
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Dependabot alerts
        uses: dependency-check/dependency-check-action@v3
        with:
          path: '.'
          format: 'SARIF'
      
      - name: Upload results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'dependency-check-report.sarif'

  code-scan:
    name: Code Security Analysis
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3

  container-scan:
    name: Container Vulnerability Scan
    runs-on: ubuntu-latest
    needs: dependency-scan
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build image
        run: docker build -t app:test .
      
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'app:test'
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'

  secrets-scan:
    name: Secrets Detection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Detect secrets with Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
</code></pre>

<h2>Workflow Triggers</h2>
<p>GitHub Actions supports various triggers for different use cases:</p>

<pre><code class="language-yaml">
on:
  # Push events
  push:
    branches: [main, 'release/**']
    tags: ['v*']
    paths:
      - 'src/**'
      - 'tests/**'
    paths-ignore:
      - '**.md'
      - 'docs/**'
  
  # Pull request events
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]
  
  # Manual trigger
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options: [staging, production]
      debug:
        description: 'Enable debug mode'
        required: false
        type: boolean
        default: false
  
  # Schedule (cron)
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  
  # Other workflow
  workflow_call:
    inputs:
      version:
        type: string
  
  # Repository events
  release:
    types: [published]
  
  issue_comment:
    types: [created]
</code></pre>

<h2>Environment Variables and Secrets</h2>
<p>Managing configuration securely is critical:</p>

<pre><code class="language-yaml">
# Workflow-level environment variables
env:
  NODE_ENV: production
  REGISTRY: ghcr.io

jobs:
  build:
    runs-on: ubuntu-latest
    # Job-level environment variables
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
    
    steps:
      - name: Deploy
        # Step-level environment variables
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          echo "Deploying to ${{ env.NODE_ENV }}"
          ./deploy.sh
</code></pre>

<h2>Caching and Optimization</h2>
<p>Speed up workflows with caching:</p>

<pre><code class="language-yaml">
steps:
  - uses: actions/checkout@v4
  
  # Cache npm dependencies
  - name: Cache node modules
    uses: actions/cache@v4
    with:
      path: ~/.npm
      key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-
  
  # Cache pip packages
  - uses: actions/setup-python@v5
    with:
      python-version: '3.11'
      cache: 'pip'
  
  # Cache Docker layers
  - uses: docker/build-push-action@v5
    with:
      cache-from: type=gha
      cache-to: type=gha,mode=max
</code></pre>

<h2>Matrix Builds</h2>
<p>Test across multiple configurations:</p>

<pre><code class="language-yaml">
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python: ['3.9', '3.10', '3.11', '3.12']
        database: [postgres, mysql]
        exclude:
          - os: windows-latest
            database: mysql
        include:
          - os: ubuntu-latest
            python: '3.11'
            coverage: true
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      
      - name: Run tests
        run: pytest tests/
      
      - name: Upload coverage
        if: matrix.coverage
        uses: codecov/codecov-action@v4
</code></pre>

<h2>Best Practices</h2>

<h3>Pipeline Design</h3>
<ul>
    <li>Keep workflows fast (under 10 minutes)</li>
    <li>Use caching to speed up builds</li>
    <li>Run jobs in parallel when possible</li>
    <li>Fail fast to get quick feedback</li>
    <li>Use path filters to avoid unnecessary runs</li>
</ul>

<h3>Security</h3>
<ul>
    <li>Use secrets for sensitive data</li>
    <li>Pin action versions to specific commits</li>
    <li>Use environment protections</li>
    <li>Limit permissions with GITHUB_TOKEN</li>
    <li>Scan for vulnerabilities automatically</li>
</ul>

<h3>Maintainability</h3>
<ul>
    <li>Use reusable workflows</li>
    <li>Document workflow purpose and requirements</li>
    <li>Use descriptive names for jobs and steps</li>
    <li>Keep workflows DRY with composite actions</li>
</ul>

<h2>Troubleshooting</h2>
<pre><code class="language-yaml">
# Enable debug logging
steps:
  - name: Debug
    run: |
      echo "Event: ${{ github.event_name }}"
      echo "Ref: ${{ github.ref }}"
      echo "SHA: ${{ github.sha }}"
    env:
      ACTIONS_STEP_DEBUG: true

# Re-run with debug logging
# From UI: Re-run jobs > Enable debug logging
</code></pre>

<p>Well-designed CI/CD pipelines save time and improve code quality. Start simple and iterate based on your team's needs!</p>
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
<p>Terraform enables you to define cloud infrastructure as code, ensuring consistency and repeatability across environments. This comprehensive guide covers everything from basics to production patterns.</p>

<h2>What is Terraform?</h2>
<p>Terraform is an open-source Infrastructure as Code (IaC) tool created by HashiCorp. It allows you to define both cloud and on-premise resources in human-readable configuration files that you can version, reuse, and share.</p>

<h3>Why Use Terraform?</h3>
<ul>
    <li><strong>Declarative Configuration</strong> - Define what you want, not how to get there</li>
    <li><strong>Provider Ecosystem</strong> - Support for AWS, Azure, GCP, and hundreds of other providers</li>
    <li><strong>State Management</strong> - Tracks resource dependencies and changes</li>
    <li><strong>Plan Before Apply</strong> - Preview changes before making them</li>
    <li><strong>Reusable Modules</strong> - Create and share infrastructure components</li>
    <li><strong>Team Collaboration</strong> - Remote state and locking for team workflows</li>
</ul>

<h2>Terraform Core Concepts</h2>

<h3>Providers</h3>
<p>Providers are plugins that interact with cloud platforms and services. Each provider offers resources and data sources.</p>

<h3>Resources</h3>
<p>Resources are the most important element. Each resource block describes one or more infrastructure objects.</p>

<h3>Data Sources</h3>
<p>Data sources allow Terraform to use information defined outside of Terraform or by another configuration.</p>

<h3>State</h3>
<p>Terraform stores the state of your managed infrastructure. This state is used to map resources to configuration and track metadata.</p>

<h2>Getting Started</h2>

<pre><code class="language-bash">
# Install Terraform (macOS)
brew install terraform

# Install Terraform (Linux)
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform version
</code></pre>

<h2>Basic AWS Infrastructure</h2>
<p>Here is a complete example that creates a VPC with public and private subnets:</p>

<pre><code class="language-hcl">
# versions.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
</code></pre>

<pre><code class="language-hcl">
# variables.tf
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (production, staging, development)"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name for tagging"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "db_username" {
  description = "Database administrator username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}
</code></pre>

<pre><code class="language-hcl">
# vpc.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.environment}-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.environment}-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = var.availability_zones[count.index]
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.environment}-public-${count.index + 1}"
    Tier = "Public"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index + length(var.availability_zones))
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.environment}-private-${count.index + 1}"
    Tier = "Private"
  }
}

# NAT Gateway
resource "aws_eip" "nat" {
  count  = length(var.availability_zones)
  domain = "vpc"
  
  tags = {
    Name = "${var.environment}-nat-eip-${count.index + 1}"
  }
}

resource "aws_nat_gateway" "main" {
  count         = length(var.availability_zones)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {
    Name = "${var.environment}-nat-${count.index + 1}"
  }
  
  depends_on = [aws_internet_gateway.main]
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.environment}-public-rt"
  }
}

resource "aws_route_table" "private" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
  
  tags = {
    Name = "${var.environment}-private-rt-${count.index + 1}"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}
</code></pre>

<h2>Security Groups</h2>
<pre><code class="language-hcl">
# security_groups.tf
resource "aws_security_group" "alb" {
  name        = "${var.environment}-alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.environment}-alb-sg"
  }
}

resource "aws_security_group" "app" {
  name        = "${var.environment}-app-sg"
  description = "Security group for application servers"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description     = "HTTP from ALB"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.environment}-app-sg"
  }
}

resource "aws_security_group" "db" {
  name        = "${var.environment}-db-sg"
  description = "Security group for database"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    description     = "PostgreSQL from app servers"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
  
  tags = {
    Name = "${var.environment}-db-sg"
  }
}
</code></pre>

<h2>Application Load Balancer</h2>
<pre><code class="language-hcl">
# alb.tf
resource "aws_lb" "main" {
  name               = "${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
  
  enable_deletion_protection = var.environment == "production"
  
  access_logs {
    bucket  = aws_s3_bucket.logs.id
    prefix  = "alb-logs"
    enabled = true
  }
  
  tags = {
    Name = "${var.environment}-alb"
  }
}

resource "aws_lb_target_group" "app" {
  name     = "${var.environment}-app-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }
  
  tags = {
    Name = "${var.environment}-app-tg"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"
  
  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = aws_acm_certificate.main.arn
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}
</code></pre>

<h2>EC2 with Auto Scaling</h2>
<pre><code class="language-hcl">
# ec2.tf
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_launch_template" "app" {
  name_prefix   = "${var.environment}-app-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = "t3.medium"
  
  vpc_security_group_ids = [aws_security_group.app.id]
  
  user_data = base64encode(templatefile("${path.module}/user_data.sh.tpl", {
    environment = var.environment
    db_host     = aws_db_instance.main.endpoint
  }))
  
  iam_instance_profile {
    name = aws_iam_instance_profile.app.name
  }
  
  monitoring {
    enabled = true
  }
  
  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size           = 30
      volume_type           = "gp3"
      encrypted             = true
      delete_on_termination = true
    }
  }
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.environment}-app"
    }
  }
  
  lifecycle {
    create_before_destroy = true
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
  
  target_group_arns         = [aws_lb_target_group.app.arn]
  health_check_type         = "ELB"
  health_check_grace_period = 300
  
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
    }
  }
  
  tag {
    key                 = "Name"
    value               = "${var.environment}-app"
    propagate_at_launch = true
  }
}

# Auto Scaling Policies
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "${var.environment}-scale-up"
  autoscaling_group_name = aws_autoscaling_group.app.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = 1
  cooldown               = 300
}

resource "aws_autoscaling_policy" "scale_down" {
  name                   = "${var.environment}-scale-down"
  autoscaling_group_name = aws_autoscaling_group.app.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = -1
  cooldown               = 300
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 80
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
  
  alarm_actions = [aws_autoscaling_policy.scale_up.arn]
}
</code></pre>

<h2>RDS Database</h2>
<pre><code class="language-hcl">
# rds.tf
resource "aws_db_subnet_group" "main" {
  name       = "${var.environment}-db-subnet"
  subnet_ids = aws_subnet.private[*].id
  
  tags = {
    Name = "${var.environment}-db-subnet-group"
  }
}

resource "aws_db_instance" "main" {
  identifier           = "${var.environment}-db"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = "db.t3.medium"
  allocated_storage    = 20
  max_allocated_storage = 100
  storage_type         = "gp3"
  storage_encrypted    = true
  
  db_name  = "myapp"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"
  
  multi_az               = var.environment == "production"
  deletion_protection    = var.environment == "production"
  skip_final_snapshot    = var.environment != "production"
  
  performance_insights_enabled = true
  
  tags = {
    Name = "${var.environment}-db"
  }
}
</code></pre>

<h2>Terraform Modules</h2>
<p>Modules allow you to organize and reuse infrastructure code:</p>

<pre><code class="language-hcl">
# modules/vpc/variables.tf
variable "name" {
  description = "Name of the VPC"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
}

variable "availability_zones" {
  description = "List of AZs"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply"
  type        = map(string)
  default     = {}
}
</code></pre>

<pre><code class="language-hcl">
# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(var.tags, { Name = var.name })
}

# ... other resources
</code></pre>

<pre><code class="language-hcl">
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}
</code></pre>

<pre><code class="language-hcl">
# Using the module
module "vpc" {
  source = "./modules/vpc"
  
  name               = "${var.environment}-vpc"
  cidr_block         = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b"]
  
  tags = {
    Environment = var.environment
  }
}

# Using Terraform Registry modules
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
}
</code></pre>

<h2>State Management</h2>
<p>Remote state enables team collaboration and state locking:</p>

<pre><code class="language-hcl">
# Create S3 bucket for state
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-terraform-state-bucket"
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
}
</code></pre>

<h2>Terraform Commands</h2>
<pre><code class="language-bash">
# Initialize working directory
terraform init

# Upgrade providers to latest versions
terraform init -upgrade

# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Create execution plan
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Apply with auto-approve (use in CI/CD)
terraform apply -auto-approve

# Destroy infrastructure
terraform destroy

# Import existing resources
terraform import aws_instance.example i-1234567890abcdef0

# Show current state
terraform show

# List resources in state
terraform state list

# Move resource in state
terraform state mv aws_instance.old aws_instance.new

# Remove resource from state (without destroying)
terraform state rm aws_instance.example

# Output values
terraform output
terraform output -json
</code></pre>

<h2>Best Practices</h2>

<h3>Code Organization</h3>
<ul>
    <li>Use consistent file naming (main.tf, variables.tf, outputs.tf)</li>
    <li>Separate environments using workspaces or directory structure</li>
    <li>Use modules for reusable components</li>
    <li>Keep modules small and focused</li>
</ul>

<h3>State Management</h3>
<ul>
    <li>Always use remote state for team projects</li>
    <li>Enable state locking with DynamoDB</li>
    <li>Enable versioning on S3 state bucket</li>
    <li>Never commit state files to version control</li>
</ul>

<h3>Security</h3>
<ul>
    <li>Never hardcode secrets in configuration</li>
    <li>Use AWS Secrets Manager or Parameter Store</li>
    <li>Mark sensitive variables with sensitive = true</li>
    <li>Encrypt state at rest and in transit</li>
</ul>

<h2>Terraform in CI/CD</h2>
<pre><code class="language-yaml">
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0
      
      - name: Terraform Format
        run: terraform fmt -check
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Validate
        run: terraform validate
      
      - name: Terraform Plan
        run: terraform plan -out=tfplan
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve tfplan
</code></pre>

<p>Terraform makes infrastructure reproducible and version-controlled. Start with simple configurations and gradually adopt modules, workspaces, and advanced patterns as your needs grow!</p>
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
