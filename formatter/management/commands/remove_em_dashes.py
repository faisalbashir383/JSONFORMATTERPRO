"""
Management command to remove em dashes from all blog posts and tutorials
"""

from django.core.management.base import BaseCommand
from formatter.models import BlogPost, Tutorial


class Command(BaseCommand):
    help = 'Remove em dashes (—) from all blog post and tutorial content'

    def handle(self, *args, **options):
        self.stdout.write('Scanning blog posts for em dashes (—)...\n')
        
        updated_count = 0
        total_posts = BlogPost.objects.count()
        
        for post in BlogPost.objects.all():
            changed = False
            
            # Check and replace in title
            if '—' in post.title:
                post.title = post.title.replace('—', '')
                changed = True
            
            # Check and replace in content
            if '—' in post.content:
                post.content = post.content.replace('—', '')
                changed = True
            
            # Check and replace in excerpt
            if '—' in post.excerpt:
                post.excerpt = post.excerpt.replace('—', '')
                changed = True
            
            # Check and replace in meta_description
            if '—' in post.meta_description:
                post.meta_description = post.meta_description.replace('—', '')
                changed = True
            
            # Check and replace in meta_keywords
            if '—' in post.meta_keywords:
                post.meta_keywords = post.meta_keywords.replace('—', '')
                changed = True
            
            # Check and replace in tags
            if '—' in post.tags:
                post.tags = post.tags.replace('—', '')
                changed = True
            
            if changed:
                post.save()
                updated_count += 1
                self.stdout.write(f'  ✓ Updated blog: {post.title[:60]}...')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Updated {updated_count} out of {total_posts} blog posts'))
        
        # Now process tutorials
        self.stdout.write('\nScanning tutorials for em dashes (—)...\n')
        
        tutorial_updated = 0
        total_tutorials = Tutorial.objects.count()
        
        for tutorial in Tutorial.objects.all():
            changed = False
            
            # Check and replace in title
            if '—' in tutorial.title:
                tutorial.title = tutorial.title.replace('—', '')
                changed = True
            
            # Check and replace in content
            if '—' in tutorial.content:
                tutorial.content = tutorial.content.replace('—', '')
                changed = True
            
            # Check and replace in description
            if '—' in tutorial.description:
                tutorial.description = tutorial.description.replace('—', '')
                changed = True
            
            # Check and replace in meta_title
            if tutorial.meta_title and '—' in tutorial.meta_title:
                tutorial.meta_title = tutorial.meta_title.replace('—', '')
                changed = True
            
            # Check and replace in meta_description
            if tutorial.meta_description and '—' in tutorial.meta_description:
                tutorial.meta_description = tutorial.meta_description.replace('—', '')
                changed = True
            
            # Check and replace in meta_keywords
            if '—' in tutorial.meta_keywords:
                tutorial.meta_keywords = tutorial.meta_keywords.replace('—', '')
                changed = True
            
            if changed:
                tutorial.save()
                tutorial_updated += 1
                self.stdout.write(f'  ✓ Updated tutorial: {tutorial.title[:60]}...')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Updated {tutorial_updated} out of {total_tutorials} tutorials'))

