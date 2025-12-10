"""
Script to update TOON blog articles with links to the TOON converter tool
"""

from django.core.management.base import BaseCommand
from formatter.models import BlogPost


class Command(BaseCommand):
    help = 'Update TOON blog articles with links to the converter tool'

    def handle(self, *args, **kwargs):
        self.stdout.write('Updating TOON blog articles with converter links...')
        
        # Find all TOON-related posts
        toon_posts = BlogPost.objects.filter(title__icontains='TOON')
        
        # Link HTML to add to each article
        link_section = '''

<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.08)); padding: 1.5rem; border-radius: 12px; margin: 2rem 0; border: 1px solid rgba(16, 185, 129, 0.2);">
    <h3 style="margin: 0 0 0.75rem 0; color: #059669;">🔧 Try Our Free TOON Converter</h3>
    <p style="margin: 0 0 1rem 0;">Convert your JSON to TOON format instantly and see your token savings in real-time!</p>
    <a href="/toon-converter/" style="display: inline-block; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981, #059669); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">⚡ Open TOON Converter</a>
</div>
'''
        
        updated_count = 0
        for post in toon_posts:
            # Check if link is already present
            if '/toon-converter/' not in post.content:
                # Add link section near the end (before conclusion if exists, or at end)
                if '<h2>Conclusion</h2>' in post.content:
                    post.content = post.content.replace('<h2>Conclusion</h2>', link_section + '<h2>Conclusion</h2>')
                else:
                    post.content = post.content + link_section
                
                post.save()
                updated_count += 1
                self.stdout.write(f'  ✓ Updated: {post.title[:50]}...')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Updated {updated_count} TOON blog articles with converter links!'))
