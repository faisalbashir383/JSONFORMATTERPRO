"""
Management command to populate DevOps tutorial data
"""

from django.core.management.base import BaseCommand
from formatter.models import (
    ProgrammingLanguage, TutorialCategory, Tutorial, 
    CodeExample, MCQQuestion, MCQOption
)


class Command(BaseCommand):
    help = 'Populate DevOps Basics tutorial with content, code examples, and MCQ questions'

    def handle(self, *args, **options):
        self.stdout.write('Creating DevOps tutorial content...')
        
        # Create Programming Languages
        languages_data = [
            {'name': 'Bash', 'slug': 'bash', 'icon': '💻', 'syntax_highlight': 'bash', 'order': 1},
            {'name': 'Python', 'slug': 'python', 'icon': '🐍', 'syntax_highlight': 'python', 'order': 2},
            {'name': 'YAML', 'slug': 'yaml', 'icon': '📄', 'syntax_highlight': 'yaml', 'order': 3},
            {'name': 'Docker', 'slug': 'docker', 'icon': '🐳', 'syntax_highlight': 'docker', 'order': 4},
            {'name': 'JavaScript', 'slug': 'javascript', 'icon': '🟨', 'syntax_highlight': 'javascript', 'order': 5},
        ]
        
        languages = {}
        for lang_data in languages_data:
            lang, created = ProgrammingLanguage.objects.get_or_create(
                slug=lang_data['slug'],
                defaults=lang_data
            )
            languages[lang_data['slug']] = lang
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'  {status}: {lang.name}')
        
        # Create Tutorial Category
        devops_category, created = TutorialCategory.objects.get_or_create(
            slug='devops-basics',
            defaults={
                'name': 'DevOps Fundamentals',
                'description': 'Learn the core concepts of DevOps including CI/CD, containerization, infrastructure as code, and more.',
                'icon': '🚀',
                'order': 1
            }
        )
        self.stdout.write(f"  Category {'Created' if created else 'Already exists'}: {devops_category.name}")
        
        # Create Tutorial: Introduction to DevOps
        tutorial_content = """
<h2>What is DevOps?</h2>
<p>
    DevOps is a set of practices, tools, and cultural philosophies that automate and integrate the processes 
    between software development and IT operations teams. The goal is to shorten the systems development 
    lifecycle while delivering features, fixes, and updates frequently in close alignment with business objectives.
</p>

<p>
    The term "DevOps" is a combination of "Development" and "Operations," representing the collaboration 
    between these traditionally siloed teams. DevOps emphasizes communication, collaboration, integration, 
    automation, and measurement of cooperation between software developers and other IT professionals.
</p>

<h2>Key Principles of DevOps</h2>

<h3>1. Continuous Integration (CI)</h3>
<p>
    Continuous Integration is the practice of automatically integrating code changes from multiple contributors 
    into a single software project. Developers frequently merge their code changes into a central repository, 
    after which automated builds and tests are run.
</p>

<h3>2. Continuous Delivery/Deployment (CD)</h3>
<p>
    Continuous Delivery ensures that code can be rapidly and safely deployed to production by delivering 
    every change to a production-like environment through rigorous automated testing. Continuous Deployment 
    takes this a step further by automatically releasing every change that passes all stages of your production pipeline.
</p>

<h3>3. Infrastructure as Code (IaC)</h3>
<p>
    Infrastructure as Code is the managing and provisioning of infrastructure through code instead of through 
    manual processes. With IaC, configuration files are created that contain your infrastructure specifications, 
    which makes it easier to edit and distribute configurations.
</p>

<h2>DevOps Tools Ecosystem</h2>

<h3>Version Control</h3>
<ul>
    <li><strong>Git</strong> - Distributed version control system</li>
    <li><strong>GitHub/GitLab/Bitbucket</strong> - Git hosting platforms</li>
</ul>

<h3>CI/CD Tools</h3>
<ul>
    <li><strong>Jenkins</strong> - Open-source automation server</li>
    <li><strong>GitHub Actions</strong> - CI/CD built into GitHub</li>
    <li><strong>GitLab CI</strong> - Integrated CI/CD with GitLab</li>
    <li><strong>CircleCI</strong> - Cloud-based CI/CD platform</li>
</ul>

<h3>Containerization</h3>
<ul>
    <li><strong>Docker</strong> - Container platform</li>
    <li><strong>Kubernetes</strong> - Container orchestration</li>
    <li><strong>Podman</strong> - Daemonless container engine</li>
</ul>

<h3>Configuration Management</h3>
<ul>
    <li><strong>Ansible</strong> - Agentless automation</li>
    <li><strong>Terraform</strong> - Infrastructure as Code</li>
    <li><strong>Puppet/Chef</strong> - Configuration management</li>
</ul>

<h2>The DevOps Lifecycle</h2>
<p>
    The DevOps lifecycle consists of eight phases representing the processes, capabilities, and tools needed 
    for development (on the left side of the loop) and operations (on the right side of the loop). 
    Throughout each phase, teams collaborate and communicate to maintain alignment, velocity, and quality.
</p>

<ol>
    <li><strong>Plan</strong> - Define requirements and track work</li>
    <li><strong>Code</strong> - Write and review code</li>
    <li><strong>Build</strong> - Compile and create artifacts</li>
    <li><strong>Test</strong> - Automated testing</li>
    <li><strong>Release</strong> - Prepare for deployment</li>
    <li><strong>Deploy</strong> - Push to production</li>
    <li><strong>Operate</strong> - Manage infrastructure</li>
    <li><strong>Monitor</strong> - Track performance and issues</li>
</ol>

<h2>Benefits of DevOps</h2>
<ul>
    <li>🚀 <strong>Faster Time to Market</strong> - Rapid delivery of features</li>
    <li>🔄 <strong>Continuous Improvement</strong> - Regular feedback loops</li>
    <li>🛡️ <strong>Increased Reliability</strong> - Automated testing reduces errors</li>
    <li>📈 <strong>Scalability</strong> - Infrastructure that grows with demand</li>
    <li>👥 <strong>Better Collaboration</strong> - Breaking down silos</li>
    <li>💰 <strong>Cost Efficiency</strong> - Automation reduces manual work</li>
</ul>
"""

        tutorial_keywords = """devops tutorial, devops basics, learn devops, devops for beginners, what is devops, devops explained, devops fundamentals, devops concepts, devops principles, CI/CD tutorial, continuous integration, continuous deployment, continuous delivery, infrastructure as code, IaC tutorial, devops tools, jenkins tutorial, docker devops, kubernetes basics, ansible tutorial, terraform basics, git devops, version control devops, devops automation, devops pipeline, devops lifecycle, devops practices, devops methodology, devops culture, agile devops, devops workflow, cloud devops, AWS devops, azure devops, GCP devops, devops engineer, devops skills, devops certification, devops roadmap, devops career, site reliability engineering, SRE basics, deployment automation, release management, configuration management, container orchestration, microservices devops, monorepo devops, gitops, devsecops, shift left testing, blue green deployment, canary deployment, rolling deployment, feature flags, devops monitoring, observability, logging devops, metrics devops, alerting devops"""

        tutorial, created = Tutorial.objects.update_or_create(
            slug='introduction-to-devops',
            defaults={
                'title': 'Introduction to DevOps',
                'category': devops_category,
                'description': 'Learn the fundamentals of DevOps including CI/CD, Infrastructure as Code, containerization, and the DevOps lifecycle. Perfect for beginners starting their DevOps journey.',
                'content': tutorial_content,
                'meta_title': 'Introduction to DevOps - Complete Beginner Guide 2024',
                'meta_description': 'Master DevOps fundamentals with our comprehensive tutorial. Learn CI/CD, Docker, Kubernetes, Terraform, and more. Free step-by-step guide with code examples.',
                'meta_keywords': tutorial_keywords,
                'order': 1,
                'is_published': True,
            }
        )
        self.stdout.write(f"  Tutorial {'Created' if created else 'Updated'}: {tutorial.title}")
        
        # Create Code Examples
        code_examples_data = [
            # Example 1: Basic CI Pipeline (Bash)
            {
                'order': 1,
                'language': 'bash',
                'title': 'Basic CI Script - Running Tests',
                'code': '''#!/bin/bash
# Simple CI script to run tests

echo "🔍 Installing dependencies..."
pip install -r requirements.txt

echo "🧪 Running unit tests..."
python -m pytest tests/ -v

echo "📊 Running code coverage..."
python -m pytest --cov=src tests/

echo "✅ All tests passed!"''',
                'output': '''🔍 Installing dependencies...
Successfully installed all packages
🧪 Running unit tests...
tests/test_api.py::test_health_check PASSED
tests/test_api.py::test_user_create PASSED
tests/test_api.py::test_user_login PASSED
📊 Running code coverage...
Coverage: 85%
✅ All tests passed!''',
                'explanation': 'This basic CI script demonstrates automating the test process. It installs dependencies, runs unit tests with pytest, and generates a coverage report.'
            },
            # Example 2: GitHub Actions YAML
            {
                'order': 2,
                'language': 'yaml',
                'title': 'GitHub Actions CI/CD Pipeline',
                'code': '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src
    
    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .
    
    - name: Deploy to staging
      if: github.ref == 'refs/heads/develop'
      run: |
        echo "Deploying to staging..."''',
                'output': '''✓ Workflow triggered on push to main
✓ Checkout completed
✓ Python 3.11 set up
✓ Dependencies installed
✓ All tests passed (12/12)
✓ Docker image built: myapp:abc123
✓ Workflow completed successfully''',
                'explanation': 'This GitHub Actions workflow demonstrates a complete CI/CD pipeline. It triggers on pushes and PRs, sets up the environment, runs tests, builds a Docker image, and conditionally deploys to staging.'
            },
            # Example 3: Terraform IaC
            {
                'order': 3,
                'language': 'yaml',
                'title': 'Terraform Infrastructure as Code',
                'code': '''# main.tf - AWS EC2 Instance Configuration

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name        = "WebServer"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
  
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              EOF
}

output "public_ip" {
  value = aws_instance.web_server.public_ip
}''',
                'output': '''Terraform will perform the following actions:

  # aws_instance.web_server will be created
  + resource "aws_instance" "web_server" {
      + ami           = "ami-0c55b159cbfafe1f0"
      + instance_type = "t2.micro"
      + public_ip     = (known after apply)
      + tags          = {
          + "Environment" = "Production"
          + "ManagedBy"   = "Terraform"
          + "Name"        = "WebServer"
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.''',
                'explanation': 'This Terraform configuration demonstrates Infrastructure as Code. It defines an AWS EC2 instance with specific settings, tags, and a startup script to install Apache web server.'
            },
            # Example 4: Docker Compose
            {
                'order': 4,
                'language': 'yaml',
                'title': 'Docker Compose for Multi-Container Apps',
                'code': '''version: '3.8'

services:
  web:
    build: ./app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    restart: always

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_PASSWORD=secret

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

volumes:
  postgres_data:''',
                'output': '''Creating network "myapp_default"
Creating volume "myapp_postgres_data"
Creating myapp_db_1    ... done
Creating myapp_cache_1 ... done
Creating myapp_web_1   ... done
Creating myapp_nginx_1 ... done

All containers are up and running!
Web app available at: http://localhost:80''',
                'explanation': 'This Docker Compose file defines a complete multi-container application with a web service, PostgreSQL database, Redis cache, and Nginx reverse proxy. It demonstrates container orchestration and service dependencies.'
            },
        ]
        
        for example_data in code_examples_data:
            lang = languages.get(example_data['language'])
            if lang:
                example, created = CodeExample.objects.get_or_create(
                    tutorial=tutorial,
                    language=lang,
                    order=example_data['order'],
                    defaults={
                        'title': example_data['title'],
                        'code': example_data['code'],
                        'output': example_data['output'],
                        'explanation': example_data['explanation'],
                    }
                )
                self.stdout.write(f"    Code Example {'Created' if created else 'Already exists'}: {example.title}")
        
        # Create MCQ Questions
        mcq_data = [
            {
                'question': 'What does DevOps stand for?',
                'explanation': 'DevOps is a combination of "Development" and "Operations", representing the collaboration between development and IT operations teams.',
                'order': 1,
                'options': [
                    {'text': 'Developer Operations', 'is_correct': False, 'order': 1},
                    {'text': 'Development and Operations', 'is_correct': True, 'order': 2},
                    {'text': 'Device Operations', 'is_correct': False, 'order': 3},
                    {'text': 'Deploy Operations', 'is_correct': False, 'order': 4},
                ]
            },
            {
                'question': 'What is Continuous Integration (CI)?',
                'explanation': 'Continuous Integration is the practice of automatically integrating code changes from multiple contributors into a single software project, with automated builds and tests.',
                'order': 2,
                'options': [
                    {'text': 'Manually merging code once a week', 'is_correct': False, 'order': 1},
                    {'text': 'Automatically integrating code changes with automated testing', 'is_correct': True, 'order': 2},
                    {'text': 'Writing code continuously without breaks', 'is_correct': False, 'order': 3},
                    {'text': 'Integrating third-party services', 'is_correct': False, 'order': 4},
                ]
            },
            {
                'question': 'Which tool is commonly used for container orchestration?',
                'explanation': 'Kubernetes is the most widely used container orchestration platform, managing containerized applications across multiple hosts.',
                'order': 3,
                'options': [
                    {'text': 'Jenkins', 'is_correct': False, 'order': 1},
                    {'text': 'Git', 'is_correct': False, 'order': 2},
                    {'text': 'Kubernetes', 'is_correct': True, 'order': 3},
                    {'text': 'Ansible', 'is_correct': False, 'order': 4},
                ]
            },
            {
                'question': 'What is Infrastructure as Code (IaC)?',
                'explanation': 'Infrastructure as Code is managing and provisioning infrastructure through code and configuration files rather than manual processes.',
                'order': 4,
                'options': [
                    {'text': 'Writing code for software applications', 'is_correct': False, 'order': 1},
                    {'text': 'Managing infrastructure through code and configuration files', 'is_correct': True, 'order': 2},
                    {'text': 'Building physical data centers', 'is_correct': False, 'order': 3},
                    {'text': 'Writing documentation for infrastructure', 'is_correct': False, 'order': 4},
                ]
            },
            {
                'question': 'Which of the following is NOT a DevOps principle?',
                'explanation': 'Working in isolation contradicts DevOps principles, which emphasize collaboration and breaking down silos between teams.',
                'order': 5,
                'options': [
                    {'text': 'Continuous Integration', 'is_correct': False, 'order': 1},
                    {'text': 'Automation', 'is_correct': False, 'order': 2},
                    {'text': 'Working in isolation', 'is_correct': True, 'order': 3},
                    {'text': 'Continuous Monitoring', 'is_correct': False, 'order': 4},
                ]
            },
        ]
        
        for mcq in mcq_data:
            question, created = MCQQuestion.objects.get_or_create(
                tutorial=tutorial,
                order=mcq['order'],
                defaults={
                    'question': mcq['question'],
                    'explanation': mcq['explanation'],
                }
            )
            self.stdout.write(f"    MCQ {'Created' if created else 'Already exists'}: Q{mcq['order']}")
            
            for opt in mcq['options']:
                option, opt_created = MCQOption.objects.get_or_create(
                    question=question,
                    order=opt['order'],
                    defaults={
                        'option_text': opt['text'],
                        'is_correct': opt['is_correct'],
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('\n✅ DevOps tutorial content created successfully!'))
        self.stdout.write(f'   Visit /tutorials/{tutorial.slug}/ to view the tutorial')
