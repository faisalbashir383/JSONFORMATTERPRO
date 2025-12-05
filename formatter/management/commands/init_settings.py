"""
Management command to initialize site settings
"""

from django.core.management.base import BaseCommand
from formatter.models import SiteSettings


class Command(BaseCommand):
    help = 'Initialize site settings with enhanced SEO'

    def handle(self, *args, **kwargs):
        if SiteSettings.objects.exists():
            self.stdout.write(self.style.WARNING('Site settings already exist. Updating...'))
            settings = SiteSettings.objects.first()
        else:
            settings = SiteSettings()
        
        # Update with comprehensive SEO keywords
        settings.primary_keywords = "json formatter, json validator, json minifier, json beautifier, json parser, json editor, jsonlint, json viewer, json lint, json pretty print, online json formatter, free json formatter"
        
        settings.secondary_keywords = "format json online, validate json, minify json, json to xml, json to csv, json converter, base64 encoder, base64 decoder, online json tool, json syntax checker, compact json, json escape, json unescape, json tester, json checker, json decode, json encode, rest api json, json api, json compare, json diff, json merge, json spli t, json xpath, json query, json path, json schema validator, json schema, json formatter online free, free json validator, json syntax error, json parse error, beautify json, compress json, json tree view, json editor online, json formatter google, format json file"
        
        settings.save()
        
        self.stdout.write(self.style.SUCCESS('✅ Site settings initialized successfully!'))
        self.stdout.write(f'  Primary keywords: {len(settings.primary_keywords.split(","))} keywords')
        self.stdout.write(f'  Secondary keywords: {len(settings.secondary_keywords.split(","))} keywords')
        self.stdout.write(f'  Total: {len(settings.get_all_keywords().split(","))} keywords')
