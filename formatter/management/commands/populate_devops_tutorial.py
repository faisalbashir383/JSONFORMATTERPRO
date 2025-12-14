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
    DevOps represents a fundamental shift in how organizations approach software delivery, emphasizing 
    collaboration, automation, and continuous improvement.
</p>

<p>
    The term "DevOps" is a combination of "Development" and "Operations," representing the collaboration 
    between these traditionally siloed teams. DevOps emphasizes communication, collaboration, integration, 
    automation, and measurement of cooperation between software developers and other IT professionals.
    This cultural and technical movement has transformed the software industry, enabling companies to 
    deliver software faster, more reliably, and with higher quality.
</p>

<h2>The History and Evolution of DevOps</h2>

<h3>Origins of DevOps (2007-2009)</h3>
<p>
    The DevOps movement emerged from the frustration with the traditional "wall of confusion" between 
    development and operations teams. In 2007, Patrick Debois, a Belgian IT consultant, became frustrated 
    with the conflicts between developers and system administrators during a data center migration project.
    This frustration led him to seek better ways for these teams to work together.
</p>

<p>
    In 2008, Andrew Shafer proposed a session called "Agile Infrastructure" at the Agile Conference in Toronto.
    Although only Patrick Debois attended, their conversation sparked ideas that would eventually become DevOps.
    The same year, John Allspaw and Paul Hammond gave a groundbreaking presentation at Velocity Conference 
    titled "10+ Deploys Per Day: Dev and Ops Cooperation at Flickr," demonstrating that development and 
    operations teams could work together to achieve remarkable deployment frequencies.
</p>

<h3>The Birth of DevOpsDays (2009)</h3>
<p>
    In 2009, Patrick Debois organized the first DevOpsDays conference in Ghent, Belgium. This event brought 
    together developers, system administrators, and others interested in bridging the gap between development 
    and operations. The Twitter hashtag #devops was born during this conference, and the movement began to 
    gain momentum globally. DevOpsDays events now take place in cities around the world, continuing to 
    spread DevOps practices and culture.
</p>

<h3>Growth and Mainstream Adoption (2010-Present)</h3>
<p>
    Throughout the 2010s, DevOps grew from a niche movement to mainstream practice. Major technology companies 
    like Netflix, Amazon, Google, and Facebook demonstrated the power of DevOps practices by deploying 
    thousands of times per day while maintaining high reliability. Tools like Docker (2013), Kubernetes (2014), 
    and Terraform (2014) emerged to support DevOps workflows. Today, DevOps is considered essential for any 
    organization seeking to deliver software efficiently and reliably.
</p>

<h2>Key Principles of DevOps</h2>

<h3>1. Culture of Collaboration</h3>
<p>
    At its core, DevOps is about breaking down silos between teams. Traditional organizations have separate 
    development, operations, QA, and security teams that often work independently with conflicting goals.
    Developers want to ship new features quickly, while operations teams prioritize stability. DevOps 
    creates a shared responsibility model where everyone is accountable for the entire software lifecycle.
</p>

<p>
    This cultural shift requires changes in organizational structure, communication patterns, and incentives.
    Teams should be organized around products or services rather than functions. Metrics should reflect 
    end-to-end delivery success rather than individual team performance. Blameless postmortems replace 
    finger-pointing when issues occur.
</p>

<h3>2. Continuous Integration (CI)</h3>
<p>
    Continuous Integration is the practice of automatically integrating code changes from multiple contributors 
    into a single software project. Developers frequently merge their code changes into a central repository, 
    after which automated builds and tests are run. The key principles of CI include:
</p>

<ul>
    <li><strong>Frequent commits</strong> - Developers commit code at least once per day, preferably multiple times</li>
    <li><strong>Automated builds</strong> - Every commit triggers an automated build process</li>
    <li><strong>Automated testing</strong> - Unit tests, integration tests, and other automated tests run on every build</li>
    <li><strong>Fast feedback</strong> - Developers receive immediate notification if their changes break the build</li>
    <li><strong>Trunk-based development</strong> - Teams work on short-lived branches or directly on the main branch</li>
</ul>

<p>
    CI reduces integration problems by detecting conflicts early when they are easier to fix. It provides 
    a safety net that gives developers confidence to refactor code and experiment with new approaches.
    The automated test suite serves as living documentation of expected system behavior.
</p>

<h3>3. Continuous Delivery and Deployment (CD)</h3>
<p>
    Continuous Delivery ensures that code can be rapidly and safely deployed to production by delivering 
    every change to a production-like environment through rigorous automated testing. The code is always 
    in a deployable state, and the decision to release is a business decision, not a technical one.
</p>

<p>
    Continuous Deployment takes this a step further by automatically releasing every change that passes 
    all stages of your production pipeline. There is no human intervention required. This approach requires 
    extremely robust automated testing and monitoring to catch issues before they impact users.
</p>

<p>
    Key practices for CD include:
</p>

<ul>
    <li><strong>Deployment pipelines</strong> - Automated workflows that build, test, and deploy code</li>
    <li><strong>Environment parity</strong> - Development, staging, and production environments are as similar as possible</li>
    <li><strong>Feature flags</strong> - Decouple deployment from release by toggling features on/off</li>
    <li><strong>Blue-green deployments</strong> - Maintain two identical production environments for zero-downtime releases</li>
    <li><strong>Canary releases</strong> - Gradually roll out changes to a subset of users before full deployment</li>
</ul>

<h3>4. Infrastructure as Code (IaC)</h3>
<p>
    Infrastructure as Code is the managing and provisioning of infrastructure through code instead of through 
    manual processes. With IaC, configuration files are created that contain your infrastructure specifications, 
    which makes it easier to edit and distribute configurations. It also ensures that the same environment 
    is provisioned every time.
</p>

<p>
    IaC brings software development practices to infrastructure management:
</p>

<ul>
    <li><strong>Version control</strong> - Infrastructure code is stored in Git alongside application code</li>
    <li><strong>Code review</strong> - Infrastructure changes go through the same review process as code changes</li>
    <li><strong>Testing</strong> - Infrastructure can be tested before deployment using tools like Terratest</li>
    <li><strong>Reusability</strong> - Modules and templates enable consistent infrastructure across environments</li>
    <li><strong>Documentation</strong> - The code itself serves as documentation of the infrastructure</li>
</ul>

<h3>5. Monitoring and Observability</h3>
<p>
    DevOps emphasizes comprehensive monitoring and observability to understand system behavior in production.
    Monitoring involves collecting metrics, logs, and traces to detect and diagnose issues. Observability 
    goes further by enabling teams to ask arbitrary questions about system state without having to anticipate 
    those questions in advance.
</p>

<p>
    The three pillars of observability are:
</p>

<ul>
    <li><strong>Metrics</strong> - Numerical measurements of system behavior over time (CPU usage, request latency, error rates)</li>
    <li><strong>Logs</strong> - Timestamped records of discrete events (errors, state changes, user actions)</li>
    <li><strong>Traces</strong> - Records of requests as they flow through distributed systems</li>
</ul>

<p>
    Effective monitoring enables proactive issue detection through alerting. Teams define Service Level 
    Objectives (SLOs) and set up alerts when metrics approach thresholds. This allows issues to be addressed 
    before they impact users.
</p>

<h3>6. Automation</h3>
<p>
    Automation is fundamental to DevOps. By automating repetitive tasks, teams can focus on higher-value 
    work while reducing human error. Automation applies to every stage of the software delivery lifecycle:
</p>

<ul>
    <li><strong>Build automation</strong> - Compile, package, and create artifacts automatically</li>
    <li><strong>Test automation</strong> - Run unit, integration, and end-to-end tests automatically</li>
    <li><strong>Deployment automation</strong> - Deploy to any environment with a single command</li>
    <li><strong>Infrastructure automation</strong> - Provision and configure infrastructure automatically</li>
    <li><strong>Incident response automation</strong> - Automatically detect, diagnose, and remediate issues</li>
</ul>

<h2>DevOps Tools Ecosystem</h2>

<p>
    The DevOps ecosystem includes hundreds of tools spanning multiple categories. Understanding the major 
    tools in each category helps teams make informed decisions about their toolchain.
</p>

<h3>Version Control Systems</h3>
<ul>
    <li><strong>Git</strong> - The dominant distributed version control system, used by over 90% of developers</li>
    <li><strong>GitHub</strong> - The largest Git hosting platform with built-in CI/CD, issue tracking, and collaboration features</li>
    <li><strong>GitLab</strong> - Complete DevOps platform with built-in CI/CD, container registry, and security scanning</li>
    <li><strong>Bitbucket</strong> - Atlassian's Git hosting platform with tight Jira integration</li>
</ul>

<h3>CI/CD Tools</h3>
<ul>
    <li><strong>Jenkins</strong> - Open-source automation server with extensive plugin ecosystem</li>
    <li><strong>GitHub Actions</strong> - CI/CD built into GitHub with YAML-based workflow definitions</li>
    <li><strong>GitLab CI/CD</strong> - Integrated CI/CD with GitLab using .gitlab-ci.yml configuration</li>
    <li><strong>CircleCI</strong> - Cloud-based CI/CD platform with fast parallel test execution</li>
    <li><strong>Travis CI</strong> - Hosted CI service popular with open-source projects</li>
    <li><strong>Azure DevOps</strong> - Microsoft's complete DevOps platform with pipelines, repos, and boards</li>
    <li><strong>AWS CodePipeline</strong> - AWS native CI/CD service integrated with other AWS services</li>
    <li><strong>ArgoCD</strong> - Declarative GitOps continuous delivery tool for Kubernetes</li>
</ul>

<h3>Containerization and Orchestration</h3>
<ul>
    <li><strong>Docker</strong> - The standard container platform for building and running containers</li>
    <li><strong>Kubernetes</strong> - The dominant container orchestration platform for managing containerized applications at scale</li>
    <li><strong>Docker Swarm</strong> - Docker's native clustering and orchestration solution</li>
    <li><strong>Podman</strong> - Daemonless container engine compatible with Docker commands</li>
    <li><strong>containerd</strong> - Industry-standard container runtime used by Kubernetes</li>
    <li><strong>OpenShift</strong> - Red Hat's enterprise Kubernetes platform</li>
    <li><strong>Amazon ECS</strong> - AWS's proprietary container orchestration service</li>
    <li><strong>Amazon EKS</strong> - Managed Kubernetes service on AWS</li>
    <li><strong>Google GKE</strong> - Managed Kubernetes service on Google Cloud</li>
    <li><strong>Azure AKS</strong> - Managed Kubernetes service on Microsoft Azure</li>
</ul>

<h3>Infrastructure as Code Tools</h3>
<ul>
    <li><strong>Terraform</strong> - Cloud-agnostic infrastructure provisioning using HCL</li>
    <li><strong>Ansible</strong> - Agentless configuration management and automation</li>
    <li><strong>Puppet</strong> - Configuration management with declarative language</li>
    <li><strong>Chef</strong> - Infrastructure automation using Ruby-based DSL</li>
    <li><strong>Pulumi</strong> - Infrastructure as Code using general-purpose programming languages</li>
    <li><strong>AWS CloudFormation</strong> - AWS native infrastructure as code service</li>
    <li><strong>Azure ARM Templates</strong> - Azure native infrastructure as code</li>
    <li><strong>Google Cloud Deployment Manager</strong> - GCP native infrastructure as code</li>
</ul>

<h3>Monitoring and Observability</h3>
<ul>
    <li><strong>Prometheus</strong> - Open-source monitoring system with powerful query language</li>
    <li><strong>Grafana</strong> - Visualization platform for metrics, logs, and traces</li>
    <li><strong>Datadog</strong> - Cloud monitoring platform with APM, logs, and infrastructure monitoring</li>
    <li><strong>New Relic</strong> - Application performance monitoring and observability platform</li>
    <li><strong>Splunk</strong> - Log management and security information platform</li>
    <li><strong>ELK Stack</strong> - Elasticsearch, Logstash, and Kibana for log aggregation and analysis</li>
    <li><strong>Jaeger</strong> - Open-source distributed tracing system</li>
    <li><strong>PagerDuty</strong> - Incident management and alerting platform</li>
</ul>

<h3>Security Tools (DevSecOps)</h3>
<ul>
    <li><strong>SonarQube</strong> - Static code analysis for code quality and security</li>
    <li><strong>Snyk</strong> - Security scanning for code, containers, and infrastructure</li>
    <li><strong>Trivy</strong> - Container and infrastructure vulnerability scanner</li>
    <li><strong>OWASP ZAP</strong> - Web application security scanner</li>
    <li><strong>HashiCorp Vault</strong> - Secrets management and encryption</li>
    <li><strong>Aqua Security</strong> - Cloud native security platform</li>
</ul>

<h2>The DevOps Lifecycle</h2>

<p>
    The DevOps lifecycle consists of eight phases representing the processes, capabilities, and tools needed 
    for development (on the left side of the loop) and operations (on the right side of the loop). 
    Throughout each phase, teams collaborate and communicate to maintain alignment, velocity, and quality.
</p>

<h3>1. Plan</h3>
<p>
    The planning phase involves defining the work to be done. Teams gather requirements, prioritize features, 
    and break down work into manageable tasks. Agile methodologies like Scrum and Kanban are commonly used 
    to manage this process. Tools like Jira, Azure Boards, or GitHub Issues help track work items and progress.
</p>

<h3>2. Code</h3>
<p>
    Developers write code following established coding standards and best practices. Version control systems 
    like Git enable collaboration and maintain code history. Code reviews ensure quality and knowledge 
    sharing across the team. IDEs and code editors provide productivity features and integrations.
</p>

<h3>3. Build</h3>
<p>
    The build phase compiles source code, runs static analysis, and creates deployable artifacts. Build 
    tools vary by language: Maven or Gradle for Java, npm for JavaScript, pip for Python. Container images 
    are built using Docker. Build caching optimizes build times.
</p>

<h3>4. Test</h3>
<p>
    Automated testing validates that code works as expected. The testing pyramid includes:
</p>

<ul>
    <li><strong>Unit tests</strong> - Test individual functions or methods in isolation</li>
    <li><strong>Integration tests</strong> - Test interactions between components</li>
    <li><strong>End-to-end tests</strong> - Test complete user workflows</li>
    <li><strong>Performance tests</strong> - Validate system performance under load</li>
    <li><strong>Security tests</strong> - Identify vulnerabilities and security issues</li>
</ul>

<h3>5. Release</h3>
<p>
    The release phase prepares code for deployment. This includes versioning artifacts, generating release 
    notes, and obtaining necessary approvals. Release management tools help coordinate complex releases 
    across multiple services.
</p>

<h3>6. Deploy</h3>
<p>
    Deployment moves code from staging to production environments. Deployment strategies minimize risk:
</p>

<ul>
    <li><strong>Rolling deployment</strong> - Gradually replace old instances with new ones</li>
    <li><strong>Blue-green deployment</strong> - Switch traffic between two identical environments</li>
    <li><strong>Canary deployment</strong> - Deploy to a small subset of users first</li>
    <li><strong>Feature flags</strong> - Deploy code but control feature visibility</li>
</ul>

<h3>7. Operate</h3>
<p>
    Operations involves managing production infrastructure and responding to issues. Site Reliability 
    Engineering (SRE) practices ensure systems meet reliability targets. Runbooks document standard 
    operating procedures. Chaos engineering proactively tests system resilience.
</p>

<h3>8. Monitor</h3>
<p>
    Continuous monitoring provides visibility into system health and performance. Dashboards display 
    key metrics. Alerts notify teams of issues. Log aggregation enables troubleshooting. User feedback 
    is collected and analyzed. Insights from monitoring inform the next planning cycle.
</p>

<h2>DevOps Best Practices</h2>

<h3>Start Small and Iterate</h3>
<p>
    DevOps transformation is a journey, not a destination. Start with small improvements and build momentum.
    Identify high-value, low-risk areas for initial automation. Celebrate early wins to build organizational 
    support. Gradually expand DevOps practices across the organization.
</p>

<h3>Measure Everything</h3>
<p>
    The DORA (DevOps Research and Assessment) metrics provide benchmarks for DevOps performance:
</p>

<ul>
    <li><strong>Deployment Frequency</strong> - How often code is deployed to production</li>
    <li><strong>Lead Time for Changes</strong> - Time from commit to production deployment</li>
    <li><strong>Mean Time to Recovery (MTTR)</strong> - Time to restore service after an incident</li>
    <li><strong>Change Failure Rate</strong> - Percentage of deployments causing failures</li>
</ul>

<h3>Embrace Failure</h3>
<p>
    Failure is inevitable in complex systems. Blameless postmortems focus on learning rather than blame.
    Chaos engineering intentionally introduces failures to build resilience. Game days simulate incident 
    response scenarios. Error budgets balance reliability with feature velocity.
</p>

<h3>Automate Security (DevSecOps)</h3>
<p>
    Security should be integrated throughout the development lifecycle, not bolted on at the end.
    Shift security left by incorporating security testing early in the pipeline. Automate security 
    scanning in CI/CD. Use infrastructure as code to enforce security policies. Implement secrets 
    management to protect sensitive data.
</p>

<h3>Document and Share Knowledge</h3>
<p>
    Documentation enables scaling knowledge across the organization. README files explain project setup.
    Architecture Decision Records (ADRs) document design decisions. Runbooks guide operational procedures.
    Internal tech talks and blog posts share lessons learned.
</p>

<h2>Benefits of DevOps</h2>

<ul>
    <li><strong>Faster Time to Market</strong> - Rapid delivery of features and updates enables competitive advantage</li>
    <li><strong>Improved Reliability</strong> - Automated testing and monitoring reduce errors and downtime</li>
    <li><strong>Better Collaboration</strong> - Shared goals and practices improve team dynamics</li>
    <li><strong>Increased Efficiency</strong> - Automation reduces manual work and accelerates delivery</li>
    <li><strong>Enhanced Customer Satisfaction</strong> - Faster response to feedback improves user experience</li>
    <li><strong>Reduced Risk</strong> - Smaller, more frequent changes are easier to troubleshoot and rollback</li>
    <li><strong>Cost Optimization</strong> - Efficient resource utilization and reduced waste lower costs</li>
    <li><strong>Innovation Culture</strong> - Teams have time and confidence to experiment and innovate</li>
</ul>

<h2>Common DevOps Challenges</h2>

<h3>Cultural Resistance</h3>
<p>
    Changing established organizational culture is difficult. Teams may resist new tools and processes.
    Leadership support is essential for driving cultural change. Training and coaching help teams adopt 
    new practices. Demonstrating early wins builds momentum for broader adoption.
</p>

<h3>Legacy Systems</h3>
<p>
    Older systems may not easily support DevOps practices. Monolithic applications are difficult to 
    deploy frequently. Legacy infrastructure may lack automation capabilities. Strangler fig pattern 
    enables gradual modernization. Containerization can help isolate legacy components.
</p>

<h3>Tool Overload</h3>
<p>
    The abundance of DevOps tools can be overwhelming. Evaluate tools based on specific requirements.
    Prefer integrated platforms over point solutions when possible. Standardize on a consistent toolchain 
    across teams. Avoid tool sprawl by periodically reviewing and consolidating.
</p>

<h3>Security Concerns</h3>
<p>
    Fast deployment cycles can introduce security risks. Automated security scanning helps maintain 
    security at speed. Security teams should be embedded in development processes. Compliance requirements 
    must be incorporated into pipelines.
</p>

<h2>Getting Started with DevOps</h2>

<h3>Step 1: Assess Current State</h3>
<p>
    Evaluate your current development and operations practices. Identify pain points and bottlenecks.
    Measure baseline metrics for deployment frequency, lead time, and failure rate. Document existing 
    processes and tools.
</p>

<h3>Step 2: Build Skills</h3>
<p>
    DevOps requires new skills across development and operations. Learn version control with Git.
    Understand containerization with Docker. Study infrastructure as code with Terraform. Practice 
    CI/CD pipelines with Jenkins or GitHub Actions.
</p>

<h3>Step 3: Start Automating</h3>
<p>
    Begin with high-value automation opportunities. Automate your build and test processes first.
    Implement basic CI pipelines. Gradually add more comprehensive testing. Document automation 
    with infrastructure as code.
</p>

<h3>Step 4: Implement Monitoring</h3>
<p>
    Establish visibility into your systems. Deploy monitoring agents and collect metrics. Set up 
    log aggregation. Create dashboards for key indicators. Configure alerts for critical thresholds.
</p>

<h3>Step 5: Iterate and Improve</h3>
<p>
    DevOps is a continuous journey. Review metrics and identify improvement opportunities. Conduct 
    retrospectives to learn from successes and failures. Expand automation coverage. Share knowledge 
    and best practices across teams.
</p>

<h2>Conclusion</h2>
<p>
    DevOps is more than just tools and automation. It represents a fundamental change in how organizations 
    approach software delivery. By breaking down silos, embracing automation, and fostering a culture of 
    continuous improvement, teams can deliver software faster, more reliably, and with higher quality.
    The journey to DevOps requires patience, commitment, and willingness to learn, but the benefits 
    make the investment worthwhile.
</p>
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
