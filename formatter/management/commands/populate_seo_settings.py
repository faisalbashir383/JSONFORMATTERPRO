"""
Django management command to populate or update SiteSettings with SEO keywords
"""

from django.core.management.base import BaseCommand
from formatter.models import SiteSettings


class Command(BaseCommand):
    help = 'Populate or update SiteSettings with SEO keywords from competitor research'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Updating SiteSettings with SEO keywords...'))
        
        # Get or create SiteSettings instance (only one should exist)
        site_settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'JSON Formatter Pro',
                'base_url': 'https://jsonformatterpro.com',
                'site_description': 'Free online JSON formatter, validator, minifier, and converter tool',
                'primary_keywords': 'json formatter, json validator, json beautifier, json minifier, json parser, json editor, json viewer, jsonlint, json lint, online json formatter, free json formatter, format json online, validate json, beautify json, json pretty print, json syntax checker, json error checker, online json validator, json tree view, json converter, json to xml, json to csv, json to yaml, api formatter, rest api json formatter, json file formatter, json linter, best json formatter 2024',
                'secondary_keywords': 'minify json, compact json, json debugging, json online editor, json beautifier online, json viewer online, json formatter tool, json validator online free, json escape online, json unescape, json tester, json formatter and validator, json compare, json diff, json schema validator, javascript object notation formatter, json data interchange format, format json file, validate json syntax, json readability tool, client side json formatter, secure json formatter, json formatter no signup, json explorer, json tree viewer, json graph view, json visualization, api response formatter, json file viewer, json file upload, drag and drop json, download json, large json files, json copy clipboard, json error detection, json corrector, json error finder, how to format json, how to validate json online, how to minify json, how to fix json syntax errors, how to convert json to xml, how to convert json to csv, json data formatter, json api formatter, json pretty printer, fix json errors, json syntax validation'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created new SiteSettings with SEO keywords'))
        else:
            # Update existing instance with new keywords
            site_settings.primary_keywords = 'json formatter, json validator, json beautifier, json minifier, json parser, json editor, json viewer, jsonlint, json lint, online json formatter, free json formatter, format json online, validate json, beautify json, json pretty print, json syntax checker, json error checker, online json validator, json tree view, json converter, json to xml, json to csv, json to yaml, api formatter, rest api json formatter, json file formatter, json linter, best json formatter 2024'
            site_settings.secondary_keywords = 'minify json, compact json, json debugging, json online editor, json beautifier online, json viewer online, json formatter tool, json validator online free, json escape online, json unescape, json tester, json formatter and validator, json compare, json diff, json schema validator, javascript object notation formatter, json data interchange format, format json file, validate json syntax, json readability tool, client side json formatter, secure json formatter, json formatter no signup, json explorer, json tree viewer, json graph view, json visualization, api response formatter, json file viewer, json file upload, drag and drop json, download json, large json files, json copy clipboard, json error detection, json corrector, json error finder, how to format json, how to validate json online, how to minify json, how to fix json syntax errors, how to convert json to xml, how to convert json to csv, json data formatter, json api formatter, json pretty printer, fix json errors, json syntax validation'
            site_settings.save()
            self.stdout.write(self.style.SUCCESS('✓ Updated existing SiteSettings with new SEO keywords'))
        
        # Display summary
        self.stdout.write('\n' + self.style.WARNING('=== SEO Keywords Summary ==='))
        self.stdout.write(f'Total primary keywords: {len(site_settings.primary_keywords.split(","))}')
        self.stdout.write(f'Total secondary keywords: {len(site_settings.secondary_keywords.split(","))}')
        self.stdout.write(f'Total keywords: {len(site_settings.get_all_keywords().split(","))}')
        self.stdout.write('\n' + self.style.SUCCESS('✓ SEO keywords populated successfully!'))
