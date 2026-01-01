"""
Sitemaps for JSON Formatter Pro
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost, Tutorial, JobPosting


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return [
            'index',
            'base64_page',
            'blog_list',
            'tutorials_list',
            'about_page',
            'contact_page',
            'privacy_page',
            'careers_page',
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
            'image_resizer_page',
            'domain_age_page',
            'resume_builder',
            # Data Format Tools
            'toon_converter_page',
            # Calculators
            'calculator_page',
            'percentage_calculator_page',
            'age_calculator_page',
            'date_calculator_page',
            'loan_calculator_page',
            'mortgage_calculator_page',
            'car_payment_calculator_page',
            'sip_calculator_page',
            'compound_interest_calculator_page',
            'salary_calculator_page',
            'bmi_calculator_page',
            'calorie_calculator_page',
            'time_calculator_page',
            'gpa_calculator_page',
            'unit_converter_page',
            'discount_calculator_page',
            'tip_calculator_page',
            'currency_calculator_page',
            'concrete_calculator_page',
            'graphing_calculator_page',
            # Legal Pages
            'terms_page',
            'code_of_conduct_page',
            # Security Tools
            'password_generator_page',
            'url_encoder_page',
            'typing_test_page',
            'json_to_jsonl_page',
            'xsd_to_json_schema_page',
            'json_to_code_page',
            'json_generator_page',
            'json_formatter_online_page',
            'json_formatter_page',
            'string_json_to_json_page'
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


class TutorialSitemap(Sitemap):
    """Sitemap for tutorials"""
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Tutorial.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class JobPostingSitemap(Sitemap):
    """Sitemap for job postings - SEO optimized for Google Jobs"""
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return JobPosting.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()
