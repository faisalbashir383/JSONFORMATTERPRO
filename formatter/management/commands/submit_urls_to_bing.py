"""
Django management command to extract all URLs from sitemap and submit to Bing Webmaster API.

Usage:
    python manage.py submit_urls_to_bing                    # List all URLs
    python manage.py submit_urls_to_bing --submit           # Submit to Bing
    python manage.py submit_urls_to_bing --export urls.txt  # Export to file
"""

import requests
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.conf import settings
from formatter.models import BlogPost, Tutorial, JobPosting
from formatter.sitemaps import StaticViewSitemap


class Command(BaseCommand):
    help = 'Extract all URLs from sitemap and optionally submit to Bing Webmaster API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--submit',
            action='store_true',
            help='Actually submit URLs to Bing API',
        )
        parser.add_argument(
            '--api-key',
            type=str,
            help='Bing Webmaster API key (or set BING_API_KEY env variable)',
        )
        parser.add_argument(
            '--export',
            type=str,
            help='Export URLs to a text file',
        )

    def get_all_urls(self):
        """Extract all URLs from Django sitemaps"""
        SITE_URL = getattr(settings, 'SITE_URL', 'https://jsonformatterspro.com')
        all_urls = []

        # 1. Static pages from sitemap
        static_sitemap = StaticViewSitemap()
        for item in static_sitemap.items():
            try:
                url = SITE_URL + reverse(item)
                all_urls.append(url)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not resolve URL for: {item}'))

        # 2. Blog posts
        for post in BlogPost.objects.filter(published=True):
            url = SITE_URL + post.get_absolute_url()
            all_urls.append(url)

        # 3. Tutorials
        for tutorial in Tutorial.objects.filter(is_published=True):
            url = SITE_URL + tutorial.get_absolute_url()
            all_urls.append(url)

        # 4. Job postings
        for job in JobPosting.objects.filter(is_active=True):
            url = SITE_URL + job.get_absolute_url()
            all_urls.append(url)

        return all_urls

    def submit_to_bing(self, urls, api_key):
        """Submit URLs to Bing Webmaster API in batches of 500"""
        import os
        
        api_key = api_key or os.getenv('BING_API_KEY')
        if not api_key:
            self.stdout.write(self.style.ERROR(
                'Bing API key not provided. Use --api-key or set BING_API_KEY env variable.'
            ))
            return False

        SITE_URL = getattr(settings, 'SITE_URL', 'https://jsonformatterspro.com')
        endpoint = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey={api_key}"
        headers = {"Content-Type": "application/json; charset=utf-8"}

        batch_size = 500
        total_submitted = 0

        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            payload = {
                "siteUrl": SITE_URL,
                "urlList": batch
            }

            try:
                response = requests.post(endpoint, json=payload, headers=headers)
                if response.status_code == 200:
                    total_submitted += len(batch)
                    self.stdout.write(self.style.SUCCESS(
                        f'✅ Batch {i // batch_size + 1}: Submitted {len(batch)} URLs'
                    ))
                else:
                    self.stdout.write(self.style.ERROR(
                        f'❌ Batch {i // batch_size + 1}: Error - {response.text}'
                    ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Request failed: {str(e)}'))

        return total_submitted

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('📥 Extracting URLs from Django sitemaps...'))
        
        urls = self.get_all_urls()
        
        self.stdout.write(self.style.SUCCESS(f'\n📋 Total URLs found: {len(urls)}'))
        
        # Show breakdown
        static_count = len(StaticViewSitemap().items())
        blog_count = BlogPost.objects.filter(published=True).count()
        tutorial_count = Tutorial.objects.filter(is_published=True).count()
        job_count = JobPosting.objects.filter(is_active=True).count()
        
        self.stdout.write(f'   - Static pages: {static_count}')
        self.stdout.write(f'   - Blog posts: {blog_count}')
        self.stdout.write(f'   - Tutorials: {tutorial_count}')
        self.stdout.write(f'   - Job postings: {job_count}')
        
        # Export to file if requested
        if options['export']:
            with open(options['export'], 'w') as f:
                for url in urls:
                    f.write(url + '\n')
            self.stdout.write(self.style.SUCCESS(f'\n✅ Exported {len(urls)} URLs to {options["export"]}'))
        
        # Show sample URLs
        self.stdout.write('\n📝 Sample URLs:')
        for url in urls[:5]:
            self.stdout.write(f'   {url}')
        self.stdout.write('   ...')
        
        # Submit to Bing if requested
        if options['submit']:
            self.stdout.write(self.style.HTTP_INFO('\n📤 Submitting to Bing Webmaster API...'))
            submitted = self.submit_to_bing(urls, options.get('api_key'))
            if submitted:
                self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully submitted {submitted} URLs to Bing!'))
        else:
            self.stdout.write(self.style.WARNING(
                '\n💡 To submit to Bing, run:\n'
                '   python manage.py submit_urls_to_bing --submit --api-key YOUR_BING_API_KEY'
            ))
