"""
Management command to populate additional DevOps tutorials
"""

from django.core.management.base import BaseCommand
from formatter.models import (
    ProgrammingLanguage, TutorialCategory, Tutorial, 
    CodeExample, MCQQuestion, MCQOption
)


class Command(BaseCommand):
    help = 'Populate additional DevOps tutorials with comprehensive content'

    def handle(self, *args, **options):
        self.stdout.write('Creating additional DevOps tutorials...')
        
        # Get existing category and languages
        devops_category = TutorialCategory.objects.get(slug='devops-basics')
        languages = {lang.slug: lang for lang in ProgrammingLanguage.objects.all()}
        
        # Tutorial 2: Docker Fundamentals
        self.create_docker_tutorial(devops_category, languages)
        
        # Tutorial 3: Kubernetes Basics
        self.create_kubernetes_tutorial(devops_category, languages)
        
        # Tutorial 4: Git & Version Control
        self.create_git_tutorial(devops_category, languages)
        
        # Tutorial 5: CI/CD Pipelines
        self.create_cicd_tutorial(devops_category, languages)
        
        self.stdout.write(self.style.SUCCESS('\n✅ All DevOps tutorials created successfully!'))

    def create_docker_tutorial(self, category, languages):
        """Create Docker Fundamentals tutorial"""
        content = """
<h2>What is Docker?</h2>
<p>
    Docker is an open-source platform that automates the deployment, scaling, and management of applications 
    using containerization technology. Containers allow developers to package an application with all its 
    dependencies into a standardized unit for software development.
</p>

<p>
    Unlike virtual machines, containers share the host system's kernel, making them lightweight and fast. 
    This means you can run many more containers on a given hardware combination than virtual machines.
</p>

<h2>Docker Architecture</h2>
<p>Docker uses a client-server architecture with the following key components:</p>
<ul>
    <li><strong>Docker Daemon</strong> - The background service running on the host that manages building, running, and distributing Docker containers</li>
    <li><strong>Docker Client</strong> - The command-line tool that allows users to interact with the Docker daemon</li>
    <li><strong>Docker Registry</strong> - A storage and distribution system for Docker images (Docker Hub is the default public registry)</li>
    <li><strong>Docker Images</strong> - Read-only templates used to create containers</li>
    <li><strong>Docker Containers</strong> - Running instances of Docker images</li>
</ul>

<h2>Key Docker Concepts</h2>

<h3>Images vs Containers</h3>
<p>
    A Docker image is like a blueprint or template - it contains everything needed to run an application 
    (code, runtime, libraries, environment variables, config files). A container is a running instance 
    of an image. You can run multiple containers from the same image.
</p>

<h3>Dockerfile</h3>
<p>
    A Dockerfile is a text document containing instructions to build a Docker image. Each instruction 
    creates a layer in the image, making it efficient to rebuild images when only specific parts change.
</p>

<h3>Docker Compose</h3>
<p>
    Docker Compose is a tool for defining and running multi-container Docker applications. 
    With Compose, you use a YAML file to configure your application's services, networks, and volumes.
</p>

<h2>Benefits of Docker</h2>
<ul>
    <li>🚀 <strong>Consistency</strong> - Same environment from development to production</li>
    <li>⚡ <strong>Speed</strong> - Containers start in seconds, not minutes</li>
    <li>📦 <strong>Portability</strong> - Run anywhere Docker is installed</li>
    <li>🔧 <strong>Isolation</strong> - Each container is isolated from others</li>
    <li>💰 <strong>Efficiency</strong> - Better resource utilization than VMs</li>
    <li>🔄 <strong>Scalability</strong> - Easy horizontal scaling</li>
</ul>

<h2>Docker Best Practices</h2>
<ul>
    <li>Use official base images when possible</li>
    <li>Keep images small by using multi-stage builds</li>
    <li>Don't run processes as root inside containers</li>
    <li>Use .dockerignore to exclude unnecessary files</li>
    <li>Tag images with meaningful version numbers</li>
    <li>Scan images for security vulnerabilities</li>
</ul>
"""

        keywords = """docker tutorial, docker basics, learn docker, docker for beginners, what is docker, docker explained, docker fundamentals, docker containers, docker images, dockerfile tutorial, docker compose tutorial, containerization, container technology, docker architecture, docker daemon, docker client, docker registry, docker hub, docker commands, docker run, docker build, docker pull, docker push, docker volumes, docker networking, docker best practices, docker security, multi-stage builds, docker optimization, microservices docker, docker development, docker production, docker deployment, container orchestration, docker swarm, docker vs kubernetes, docker vs VM, virtualization vs containerization, devops docker, CI/CD docker, docker pipeline, docker automation"""

        tutorial, created = Tutorial.objects.update_or_create(
            slug='docker-fundamentals',
            defaults={
                'title': 'Docker Fundamentals',
                'category': category,
                'description': 'Master Docker containerization from basics to advanced concepts. Learn to build, run, and manage containers for your applications.',
                'content': content,
                'meta_title': 'Docker Tutorial - Complete Guide for Beginners 2024',
                'meta_description': 'Learn Docker from scratch with our comprehensive tutorial. Understand containers, images, Dockerfiles, and Docker Compose with practical examples.',
                'meta_keywords': keywords,
                'order': 2,
                'is_published': True,
            }
        )
        self.stdout.write(f"  Tutorial {'Created' if created else 'Updated'}: {tutorial.title}")
        
        # Docker code examples
        examples = [
            {
                'order': 1,
                'language': 'bash',
                'title': 'Essential Docker Commands',
                'code': '''# Pull an image from Docker Hub
docker pull nginx:latest

# List all images
docker images

# Run a container
docker run -d -p 8080:80 --name my-nginx nginx:latest

# List running containers
docker ps

# Stop a container
docker stop my-nginx

# Remove a container
docker rm my-nginx

# Remove an image
docker rmi nginx:latest''',
                'output': '''latest: Pulling from library/nginx
Digest: sha256:abc123...
Status: Downloaded newer image for nginx:latest

REPOSITORY   TAG       IMAGE ID       SIZE
nginx        latest    605c77e624dd   141MB

CONTAINER ID   IMAGE   COMMAND   NAMES
a1b2c3d4e5f6   nginx   ...       my-nginx''',
                'explanation': 'These are the fundamental Docker commands you will use daily. Practice these to become comfortable with Docker workflow.'
            },
            {
                'order': 2,
                'language': 'yaml',
                'title': 'Dockerfile for Python Application',
                'code': '''# Use an official Python runtime as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]''',
                'output': '''Step 1/8 : FROM python:3.11-slim
 ---> abc123
Step 2/8 : ENV PYTHONDONTWRITEBYTECODE=1
 ---> Using cache
...
Successfully built def456
Successfully tagged myapp:latest''',
                'explanation': 'This Dockerfile creates a production-ready Python container. It uses a slim base image for smaller size and follows best practices like setting environment variables.'
            },
        ]
        
        for ex in examples:
            lang = languages.get(ex['language'])
            if lang:
                CodeExample.objects.update_or_create(
                    tutorial=tutorial, order=ex['order'],
                    defaults={'language': lang, 'title': ex['title'], 
                             'code': ex['code'], 'output': ex['output'],
                             'explanation': ex['explanation']}
                )

        # Docker MCQs
        mcqs = [
            {
                'question': 'What is the main difference between a Docker container and a virtual machine?',
                'explanation': 'Containers share the host OS kernel making them lightweight, while VMs include their own complete OS making them heavier.',
                'order': 1,
                'options': [
                    {'text': 'Containers are slower than VMs', 'is_correct': False, 'order': 1},
                    {'text': 'Containers share the host OS kernel while VMs have their own OS', 'is_correct': True, 'order': 2},
                    {'text': 'VMs are more portable than containers', 'is_correct': False, 'order': 3},
                    {'text': 'There is no difference', 'is_correct': False, 'order': 4},
                ]
            },
            {
                'question': 'What file is used to define how to build a Docker image?',
                'explanation': 'A Dockerfile contains instructions for building a Docker image, including base image, commands, and configuration.',
                'order': 2,
                'options': [
                    {'text': 'docker-compose.yml', 'is_correct': False, 'order': 1},
                    {'text': 'Dockerfile', 'is_correct': True, 'order': 2},
                    {'text': 'container.json', 'is_correct': False, 'order': 3},
                    {'text': 'image.yaml', 'is_correct': False, 'order': 4},
                ]
            },
        ]
        
        for mcq in mcqs:
            question, _ = MCQQuestion.objects.update_or_create(
                tutorial=tutorial, order=mcq['order'],
                defaults={'question': mcq['question'], 'explanation': mcq['explanation']}
            )
            for opt in mcq['options']:
                MCQOption.objects.update_or_create(
                    question=question, order=opt['order'],
                    defaults={'option_text': opt['text'], 'is_correct': opt['is_correct']}
                )

    def create_kubernetes_tutorial(self, category, languages):
        """Create Kubernetes Basics tutorial"""
        content = """
<h2>What is Kubernetes?</h2>
<p>
    Kubernetes (often abbreviated as K8s) is an open-source container orchestration platform designed 
    to automate the deployment, scaling, and management of containerized applications. Originally 
    developed by Google, it is now maintained by the Cloud Native Computing Foundation (CNCF).
</p>

<p>
    Kubernetes provides a framework to run distributed systems resiliently. It takes care of scaling 
    and failover for your application, provides deployment patterns, and more.
</p>

<h2>Why Use Kubernetes?</h2>
<ul>
    <li><strong>Service Discovery & Load Balancing</strong> - Kubernetes can expose containers using DNS or IP addresses and load balance traffic</li>
    <li><strong>Storage Orchestration</strong> - Automatically mount storage systems of your choice</li>
    <li><strong>Automated Rollouts & Rollbacks</strong> - Deploy changes gradually and rollback if something goes wrong</li>
    <li><strong>Self-Healing</strong> - Restarts failed containers, replaces and reschedules containers</li>
    <li><strong>Secret & Configuration Management</strong> - Deploy and update secrets and configuration without rebuilding images</li>
</ul>

<h2>Kubernetes Architecture</h2>

<h3>Control Plane Components</h3>
<ul>
    <li><strong>kube-apiserver</strong> - The API server that exposes the Kubernetes API</li>
    <li><strong>etcd</strong> - Consistent and highly-available key-value store for cluster data</li>
    <li><strong>kube-scheduler</strong> - Watches for newly created Pods and selects nodes for them to run on</li>
    <li><strong>kube-controller-manager</strong> - Runs controller processes</li>
</ul>

<h3>Node Components</h3>
<ul>
    <li><strong>kubelet</strong> - An agent that runs on each node, ensuring containers are running in a Pod</li>
    <li><strong>kube-proxy</strong> - Network proxy that maintains network rules on nodes</li>
    <li><strong>Container Runtime</strong> - Software responsible for running containers (Docker, containerd, CRI-O)</li>
</ul>

<h2>Key Kubernetes Objects</h2>
<ul>
    <li>🔷 <strong>Pod</strong> - Smallest deployable unit, contains one or more containers</li>
    <li>🔷 <strong>Deployment</strong> - Manages Pod replicas and updates</li>
    <li>🔷 <strong>Service</strong> - Exposes Pods to network traffic</li>
    <li>🔷 <strong>ConfigMap</strong> - Stores configuration data as key-value pairs</li>
    <li>🔷 <strong>Secret</strong> - Stores sensitive data like passwords and tokens</li>
    <li>🔷 <strong>Namespace</strong> - Virtual clusters for resource isolation</li>
</ul>
"""

        keywords = """kubernetes tutorial, k8s tutorial, learn kubernetes, kubernetes basics, kubernetes for beginners, what is kubernetes, kubernetes explained, container orchestration, kubernetes architecture, kubernetes pods, kubernetes deployments, kubernetes services, kubernetes nodes, kubectl commands, kubernetes cluster, kubernetes vs docker, kubernetes container, kubernetes scaling, kubernetes load balancing, kubernetes networking, kubernetes volumes, kubernetes secrets, kubernetes configmaps, kubernetes namespaces, kubernetes helm, kubernetes operators, kubernetes ingress, kubernetes monitoring, kubernetes logging, kubernetes security, kubernetes best practices, kubernetes production, kubernetes cloud, AKS tutorial, EKS tutorial, GKE tutorial, kubernetes devops"""

        tutorial, created = Tutorial.objects.update_or_create(
            slug='kubernetes-basics',
            defaults={
                'title': 'Kubernetes Basics',
                'category': category,
                'description': 'Learn Kubernetes container orchestration from the ground up. Understand pods, deployments, services, and how to manage containerized applications at scale.',
                'content': content,
                'meta_title': 'Kubernetes Tutorial - Learn K8s from Scratch 2024',
                'meta_description': 'Master Kubernetes (K8s) with our beginner-friendly tutorial. Learn about pods, deployments, services, and container orchestration with practical examples.',
                'meta_keywords': keywords,
                'order': 3,
                'is_published': True,
            }
        )
        self.stdout.write(f"  Tutorial {'Created' if created else 'Updated'}: {tutorial.title}")

        # Kubernetes code examples
        examples = [
            {
                'order': 1,
                'language': 'bash',
                'title': 'Essential kubectl Commands',
                'code': '''# Get cluster info
kubectl cluster-info

# List all nodes
kubectl get nodes

# List all pods in default namespace
kubectl get pods

# List all pods in all namespaces
kubectl get pods --all-namespaces

# Describe a pod
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>

# Execute command in a pod
kubectl exec -it <pod-name> -- /bin/bash

# Apply a configuration
kubectl apply -f deployment.yaml

# Delete resources
kubectl delete -f deployment.yaml''',
                'output': '''Kubernetes control plane is running at https://127.0.0.1:6443

NAME           STATUS   ROLES    AGE   VERSION
node-1         Ready    master   10d   v1.28.0
node-2         Ready    worker   10d   v1.28.0

NAME                     READY   STATUS    RESTARTS   AGE
nginx-7c658794b9-abc12   1/1     Running   0          5m''',
                'explanation': 'These kubectl commands are essential for managing Kubernetes clusters. Practice these to become proficient in K8s operations.'
            },
            {
                'order': 2,
                'language': 'yaml',
                'title': 'Kubernetes Deployment Manifest',
                'code': '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
          requests:
            memory: "64Mi"
            cpu: "250m"''',
                'output': '''deployment.apps/nginx-deployment created

NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           1m''',
                'explanation': 'This Deployment creates 3 replicas of nginx with resource limits. Kubernetes will ensure these pods are always running.'
            },
        ]
        
        for ex in examples:
            lang = languages.get(ex['language'])
            if lang:
                CodeExample.objects.update_or_create(
                    tutorial=tutorial, order=ex['order'],
                    defaults={'language': lang, 'title': ex['title'], 
                             'code': ex['code'], 'output': ex['output'],
                             'explanation': ex['explanation']}
                )

        # Kubernetes MCQs
        mcqs = [
            {
                'question': 'What is the smallest deployable unit in Kubernetes?',
                'explanation': 'A Pod is the smallest deployable unit in Kubernetes. It can contain one or more containers that share storage and network resources.',
                'order': 1,
                'options': [
                    {'text': 'Container', 'is_correct': False, 'order': 1},
                    {'text': 'Node', 'is_correct': False, 'order': 2},
                    {'text': 'Pod', 'is_correct': True, 'order': 3},
                    {'text': 'Deployment', 'is_correct': False, 'order': 4},
                ]
            },
            {
                'question': 'What Kubernetes object is used to expose pods to network traffic?',
                'explanation': 'A Service in Kubernetes is used to expose pods to network traffic, providing stable networking and load balancing.',
                'order': 2,
                'options': [
                    {'text': 'Ingress', 'is_correct': False, 'order': 1},
                    {'text': 'Service', 'is_correct': True, 'order': 2},
                    {'text': 'ConfigMap', 'is_correct': False, 'order': 3},
                    {'text': 'Volume', 'is_correct': False, 'order': 4},
                ]
            },
        ]
        
        for mcq in mcqs:
            question, _ = MCQQuestion.objects.update_or_create(
                tutorial=tutorial, order=mcq['order'],
                defaults={'question': mcq['question'], 'explanation': mcq['explanation']}
            )
            for opt in mcq['options']:
                MCQOption.objects.update_or_create(
                    question=question, order=opt['order'],
                    defaults={'option_text': opt['text'], 'is_correct': opt['is_correct']}
                )

    def create_git_tutorial(self, category, languages):
        """Create Git & Version Control tutorial"""
        content = """
<h2>What is Git?</h2>
<p>
    Git is a distributed version control system that tracks changes in source code during software development. 
    Created by Linus Torvalds in 2005, Git is designed for coordinating work among programmers, but it can 
    be used to track changes in any set of files.
</p>

<h2>Why Use Version Control?</h2>
<ul>
    <li>📜 <strong>History</strong> - Track every change made to your codebase</li>
    <li>👥 <strong>Collaboration</strong> - Multiple developers can work on the same project</li>
    <li>🔄 <strong>Branching</strong> - Work on features in isolation without affecting main code</li>
    <li>⏪ <strong>Revert</strong> - Easily undo changes and go back to previous versions</li>
    <li>🔍 <strong>Blame</strong> - See who made what changes and when</li>
</ul>

<h2>Git Workflow</h2>

<h3>The Three States</h3>
<p>Git has three main states that your files can reside in:</p>
<ol>
    <li><strong>Modified</strong> - You have changed the file but not committed it</li>
    <li><strong>Staged</strong> - You have marked a modified file to go into your next commit</li>
    <li><strong>Committed</strong> - The data is safely stored in your local database</li>
</ol>

<h3>Branching Strategy</h3>
<p>Common branching strategies include:</p>
<ul>
    <li><strong>Git Flow</strong> - Feature branches, develop, and main branches</li>
    <li><strong>GitHub Flow</strong> - Simple feature branch workflow</li>
    <li><strong>Trunk-Based Development</strong> - Short-lived branches merged frequently</li>
</ul>

<h2>Git Best Practices</h2>
<ul>
    <li>Write clear, descriptive commit messages</li>
    <li>Commit often with small, focused changes</li>
    <li>Use branches for new features and bug fixes</li>
    <li>Pull frequently to stay up to date</li>
    <li>Review code before merging (Pull Requests)</li>
    <li>Never commit sensitive data (use .gitignore)</li>
</ul>
"""

        keywords = """git tutorial, git basics, learn git, git for beginners, version control, git commands, git workflow, git branching, git merge, git rebase, git commit, git push, git pull, git clone, git checkout, git branch, github tutorial, gitlab tutorial, bitbucket, git flow, github flow, trunk based development, pull request tutorial, code review, git best practices, git collaboration, distributed version control, git history, git log, git diff, git stash, git reset, git revert, gitignore, git remote, git fetch, merge conflicts, git cherry-pick, devops git"""

        tutorial, created = Tutorial.objects.update_or_create(
            slug='git-version-control',
            defaults={
                'title': 'Git & Version Control',
                'category': category,
                'description': 'Master Git version control system. Learn essential commands, branching strategies, and collaboration workflows used in modern development.',
                'content': content,
                'meta_title': 'Git Tutorial - Complete Version Control Guide 2024',
                'meta_description': 'Learn Git from basics to advanced. Master version control, branching, merging, and collaboration workflows with practical examples and best practices.',
                'meta_keywords': keywords,
                'order': 4,
                'is_published': True,
            }
        )
        self.stdout.write(f"  Tutorial {'Created' if created else 'Updated'}: {tutorial.title}")

        # Git code examples
        examples = [
            {
                'order': 1,
                'language': 'bash',
                'title': 'Essential Git Commands',
                'code': '''# Initialize a new repository
git init

# Clone a repository
git clone https://github.com/user/repo.git

# Check status
git status

# Add files to staging
git add .
git add filename.txt

# Commit changes
git commit -m "Add new feature"

# Push to remote
git push origin main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline -10''',
                'output': '''Initialized empty Git repository in /project/.git/

Cloning into 'repo'...
remote: Counting objects: 100%, done.

On branch main
Changes to be committed:
  new file:   feature.py

[main abc1234] Add new feature
 1 file changed, 50 insertions(+)

a1b2c3d Add authentication
e4f5g6h Fix login bug
i7j8k9l Initial commit''',
                'explanation': 'These are the fundamental Git commands used in daily development. Master these to work efficiently with version control.'
            },
            {
                'order': 2,
                'language': 'bash',
                'title': 'Git Branching & Merging',
                'code': '''# Create and switch to a new branch
git checkout -b feature/user-auth

# Or with newer Git syntax
git switch -c feature/user-auth

# List all branches
git branch -a

# Switch to existing branch
git checkout main
git switch main

# Merge feature branch into main
git checkout main
git merge feature/user-auth

# Delete branch after merge
git branch -d feature/user-auth

# Rebase instead of merge
git checkout feature/user-auth
git rebase main''',
                'output': '''Switched to a new branch 'feature/user-auth'

* feature/user-auth
  main
  remotes/origin/main

Switched to branch 'main'

Merge made by 'recursive' strategy.
 auth.py | 100 ++++++++++++++++++
 1 file changed, 100 insertions(+)

Deleted branch feature/user-auth''',
                'explanation': 'Branching allows you to work on features in isolation. Merge or rebase to integrate changes back into the main branch.'
            },
        ]
        
        for ex in examples:
            lang = languages.get(ex['language'])
            if lang:
                CodeExample.objects.update_or_create(
                    tutorial=tutorial, order=ex['order'],
                    defaults={'language': lang, 'title': ex['title'], 
                             'code': ex['code'], 'output': ex['output'],
                             'explanation': ex['explanation']}
                )

    def create_cicd_tutorial(self, category, languages):
        """Create CI/CD Pipelines tutorial"""
        content = """
<h2>What is CI/CD?</h2>
<p>
    CI/CD stands for Continuous Integration and Continuous Delivery/Deployment. It is a set of practices 
    that enable development teams to deliver code changes more frequently and reliably. CI/CD is one 
    of the cornerstone practices of DevOps.
</p>

<h2>Continuous Integration (CI)</h2>
<p>
    Continuous Integration is the practice of merging all developers' working copies to a shared mainline 
    several times a day. Each integration triggers an automated build and test process to detect 
    integration errors as quickly as possible.
</p>
<ul>
    <li>Developers commit code frequently (at least daily)</li>
    <li>Each commit triggers an automated build</li>
    <li>Automated tests run on every build</li>
    <li>Bugs are detected and fixed quickly</li>
</ul>

<h2>Continuous Delivery vs Continuous Deployment</h2>

<h3>Continuous Delivery (CD)</h3>
<p>
    Continuous Delivery ensures that code is always in a deployable state. Every change that passes 
    all stages of the production pipeline is ready to be released to customers. However, the final 
    deployment to production is a manual decision.
</p>

<h3>Continuous Deployment</h3>
<p>
    Continuous Deployment goes one step further - every change that passes all stages 
    of the production pipeline is automatically released to customers. There is no human intervention.
</p>

<h2>CI/CD Pipeline Stages</h2>
<ol>
    <li>📥 <strong>Source</strong> - Code commit triggers the pipeline</li>
    <li>🔨 <strong>Build</strong> - Compile code, create artifacts</li>
    <li>🧪 <strong>Test</strong> - Run unit, integration, and e2e tests</li>
    <li>📊 <strong>Analysis</strong> - Code quality, security scans</li>
    <li>📦 <strong>Package</strong> - Create deployable artifacts (Docker images)</li>
    <li>🚀 <strong>Deploy</strong> - Deploy to staging/production</li>
    <li>👁️ <strong>Monitor</strong> - Track application health</li>
</ol>

<h2>Popular CI/CD Tools</h2>
<ul>
    <li><strong>Jenkins</strong> - Open-source automation server</li>
    <li><strong>GitHub Actions</strong> - Native CI/CD for GitHub</li>
    <li><strong>GitLab CI/CD</strong> - Built into GitLab</li>
    <li><strong>CircleCI</strong> - Cloud-native CI/CD</li>
    <li><strong>Travis CI</strong> - Hosted CI service</li>
    <li><strong>Azure DevOps</strong> - Microsoft's CI/CD platform</li>
    <li><strong>AWS CodePipeline</strong> - AWS native CI/CD</li>
</ul>

<h2>CI/CD Best Practices</h2>
<ul>
    <li>Keep pipelines fast (under 10 minutes if possible)</li>
    <li>Run tests in parallel</li>
    <li>Fail fast - stop pipeline on first failure</li>
    <li>Use feature flags for gradual rollouts</li>
    <li>Implement proper monitoring and alerting</li>
    <li>Practice infrastructure as code for environments</li>
</ul>
"""

        keywords = """CI/CD tutorial, continuous integration, continuous delivery, continuous deployment, CI/CD pipeline, devops pipeline, jenkins pipeline, github actions tutorial, gitlab ci tutorial, build automation, test automation, deployment automation, CI/CD best practices, pipeline stages, automated testing, code quality, security scanning, artifact management, docker ci/cd, kubernetes ci/cd, infrastructure as code, gitops, feature flags, blue green deployment, canary deployment, rolling deployment, pipeline optimization, devops automation, release management, deployment strategies"""

        tutorial, created = Tutorial.objects.update_or_create(
            slug='cicd-pipelines',
            defaults={
                'title': 'CI/CD Pipelines',
                'category': category,
                'description': 'Learn to build robust CI/CD pipelines for automated testing and deployment. Master popular tools like Jenkins, GitHub Actions, and GitLab CI.',
                'content': content,
                'meta_title': 'CI/CD Pipeline Tutorial - Complete Guide 2024',
                'meta_description': 'Master CI/CD pipelines with our comprehensive tutorial. Learn continuous integration, delivery, and deployment with practical examples using popular tools.',
                'meta_keywords': keywords,
                'order': 5,
                'is_published': True,
            }
        )
        self.stdout.write(f"  Tutorial {'Created' if created else 'Updated'}: {tutorial.title}")

        # CI/CD code examples
        examples = [
            {
                'order': 1,
                'language': 'yaml',
                'title': 'GitHub Actions CI/CD Workflow',
                'code': '''name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v --cov=src
      
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: |
          docker tag myapp:${{ github.sha }} registry/myapp:latest
          docker push registry/myapp:latest

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: kubectl apply -f k8s/''',
                'output': '''✓ test (2m 15s)
  ✓ Set up Python
  ✓ Install dependencies
  ✓ Run tests - 45 passed

✓ build (1m 30s)
  ✓ Build Docker image
  ✓ Push to registry

✓ deploy (45s)
  ✓ Deploy to production

Pipeline completed successfully!''',
                'explanation': 'This GitHub Actions workflow demonstrates a complete CI/CD pipeline with test, build, and deploy stages. The deploy stage only runs on the main branch.'
            },
        ]
        
        for ex in examples:
            lang = languages.get(ex['language'])
            if lang:
                CodeExample.objects.update_or_create(
                    tutorial=tutorial, order=ex['order'],
                    defaults={'language': lang, 'title': ex['title'], 
                             'code': ex['code'], 'output': ex['output'],
                             'explanation': ex['explanation']}
                )

        # CI/CD MCQs
        mcqs = [
            {
                'question': 'What is the main difference between Continuous Delivery and Continuous Deployment?',
                'explanation': 'Continuous Delivery requires manual approval for production deployment, while Continuous Deployment automatically deploys every change that passes all tests.',
                'order': 1,
                'options': [
                    {'text': 'They are the same thing', 'is_correct': False, 'order': 1},
                    {'text': 'Continuous Delivery includes testing, Continuous Deployment does not', 'is_correct': False, 'order': 2},
                    {'text': 'Continuous Deployment automatically releases to production, Continuous Delivery requires manual approval', 'is_correct': True, 'order': 3},
                    {'text': 'Continuous Delivery is faster than Continuous Deployment', 'is_correct': False, 'order': 4},
                ]
            },
        ]
        
        for mcq in mcqs:
            question, _ = MCQQuestion.objects.update_or_create(
                tutorial=tutorial, order=mcq['order'],
                defaults={'question': mcq['question'], 'explanation': mcq['explanation']}
            )
            for opt in mcq['options']:
                MCQOption.objects.update_or_create(
                    question=question, order=opt['order'],
                    defaults={'option_text': opt['text'], 'is_correct': opt['is_correct']}
                )
