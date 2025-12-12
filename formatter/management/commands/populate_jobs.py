"""
Management command to populate sample job postings
"""

from django.core.management.base import BaseCommand
from formatter.models import JobPosting


class Command(BaseCommand):
    help = 'Populate sample job postings for the careers page'

    def handle(self, *args, **options):
        jobs_data = [
            {
                'title': 'Technical Content Writer',
                'slug': 'technical-content-writer',
                'department': 'marketing',
                'location': 'Delhi, India (Remote Friendly)',
                'employment_type': 'full-time',
                'description': '''
                    <p>We're looking for a skilled Technical Content Writer to join our team and help create compelling, 
                    developer-focused content for JSON Formatters Pro. You'll be responsible for writing documentation, 
                    tutorials, blog posts, and educational content that helps developers understand and use our tools effectively.</p>
                    
                    <p>As a Technical Content Writer, you'll work closely with our engineering and product teams to 
                    translate complex technical concepts into clear, engaging content that resonates with our developer audience.</p>
                ''',
                'requirements': '''
                    <ul>
                        <li>3+ years of experience in technical writing or developer documentation</li>
                        <li>Strong understanding of web development concepts (HTML, CSS, JavaScript, APIs)</li>
                        <li>Experience with JSON, REST APIs, and developer tools</li>
                        <li>Excellent written English with attention to grammar and clarity</li>
                        <li>Ability to explain complex technical concepts in simple terms</li>
                        <li>Familiarity with SEO best practices for technical content</li>
                        <li>Experience with markdown, Git, and documentation platforms</li>
                        <li>Portfolio of published technical writing samples</li>
                    </ul>
                ''',
                'responsibilities': '''
                    <ul>
                        <li>Write and maintain comprehensive documentation for all JSON Formatters Pro tools</li>
                        <li>Create in-depth tutorials and how-to guides for developers</li>
                        <li>Produce engaging blog posts on JSON, APIs, and web development topics</li>
                        <li>Collaborate with engineers to document new features and updates</li>
                        <li>Optimize content for SEO to improve organic search visibility</li>
                        <li>Research and stay current with industry trends and best practices</li>
                        <li>Review and edit content from other team members</li>
                        <li>Maintain a consistent voice and style across all content</li>
                    </ul>
                ''',
                'benefits': '''
                    <ul>
                        <li>Competitive salary with performance bonuses</li>
                        <li>Flexible remote work options</li>
                        <li>Health insurance for you and your family</li>
                        <li>Annual learning budget for courses and conferences</li>
                        <li>Latest equipment and tools</li>
                        <li>Paid time off and holidays</li>
                    </ul>
                ''',
                'meta_keywords': 'technical content writer jobs, technical writer delhi, content writer developer tools, documentation writer, API documentation jobs, tech blog writer, developer content creator, remote technical writer, JSON documentation, web development writer, SEO content writer, technical copywriter, software documentation, developer advocate, technical marketing writer',
                'is_active': True,
                'is_featured': True,
                'apply_email': 'careers@jsonformatterspro.com',
            },
            {
                'title': 'SEO Specialist',
                'slug': 'seo-specialist',
                'department': 'marketing',
                'location': 'Delhi, India (Remote Friendly)',
                'employment_type': 'full-time',
                'description': '''
                    <p>We're seeking an experienced SEO Specialist to drive organic growth for JSON Formatters Pro. 
                    You'll be responsible for developing and executing SEO strategies that increase our visibility 
                    in search engines and attract millions of developers to our platform.</p>
                    
                    <p>This is an exciting opportunity to work on a high-traffic developer tools website with 
                    significant potential for growth. You'll have the autonomy to implement strategies and 
                    see the direct impact of your work.</p>
                ''',
                'requirements': '''
                    <ul>
                        <li>4+ years of experience in SEO, preferably for tech/developer products</li>
                        <li>Proven track record of improving organic rankings and traffic</li>
                        <li>Deep understanding of technical SEO (site structure, schema markup, Core Web Vitals)</li>
                        <li>Experience with SEO tools (Google Search Console, Ahrefs, SEMrush, Screaming Frog)</li>
                        <li>Strong analytical skills and proficiency with Google Analytics 4</li>
                        <li>Understanding of web development basics (HTML, CSS, JavaScript)</li>
                        <li>Experience with keyword research and content strategy</li>
                        <li>Knowledge of link building strategies and outreach</li>
                    </ul>
                ''',
                'responsibilities': '''
                    <ul>
                        <li>Develop and execute comprehensive SEO strategies for organic growth</li>
                        <li>Conduct keyword research and competitive analysis</li>
                        <li>Optimize on-page elements including meta tags, headers, and content</li>
                        <li>Implement technical SEO improvements (structured data, sitemaps, page speed)</li>
                        <li>Monitor and analyze SEO performance metrics and rankings</li>
                        <li>Build high-quality backlinks through outreach and partnerships</li>
                        <li>Collaborate with content team on SEO-optimized content creation</li>
                        <li>Stay updated with Google algorithm changes and SEO best practices</li>
                        <li>Report on SEO KPIs and provide actionable insights</li>
                    </ul>
                ''',
                'benefits': '''
                    <ul>
                        <li>Competitive salary with performance bonuses</li>
                        <li>Flexible remote work options</li>
                        <li>Health insurance for you and your family</li>
                        <li>Annual learning budget for SEO tools and courses</li>
                        <li>Latest equipment and tools</li>
                        <li>Paid time off and holidays</li>
                    </ul>
                ''',
                'meta_keywords': 'SEO specialist jobs delhi, search engine optimization jobs, SEO manager india, digital marketing SEO, organic growth specialist, technical SEO expert, SEO analyst jobs, remote SEO jobs, developer tools SEO, SaaS SEO specialist, link building specialist, keyword research analyst, Google ranking expert, SEO strategist, search marketing jobs',
                'is_active': True,
                'is_featured': False,
                'apply_email': 'careers@jsonformatterspro.com',
            },
        ]

        created_count = 0
        for job_data in jobs_data:
            job, created = JobPosting.objects.update_or_create(
                slug=job_data['slug'],
                defaults=job_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created job: {job.title}'))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Updated job: {job.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully processed {len(jobs_data)} job postings ({created_count} new)'))
