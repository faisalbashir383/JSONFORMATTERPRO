"""
Sitemaps for JSON Formatter Pro
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return [
            'index',
            'base64_page',
            'blog_list',
            'about_page',
            'contact_page',
            'privacy_page',
            'json_to_yaml_page',
            'csv_to_json_page',
            'json_diff_page',
            'json_schema_page',
            'json_tree_page',
            'dummy_json_page',
            # API & Network Tools
            'http_headers_page',
            'ip_info_page',
            'dns_lookup_page',
            'ssl_checker_page',
            'cors_checker_page',
            # Code Tools
            'cron_builder_page',
            'markdown_preview_page',
            'sql_formatter_page',
            'qr_generator_page',
            'mock_api_generator_page',
            'push_notification_tester_page',
            'api_response_tester_page',
            'image_to_base64_page',
            'json_editor_page',
            'regex_tester_page',
            'json_visualizer_page',
            # SEO & Web Tools
            'lorem_ipsum_page',
        ]
    
    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return BlogPost.objects.filter(published=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()
