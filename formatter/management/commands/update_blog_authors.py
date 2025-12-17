from django.core.management.base import BaseCommand
from formatter.models import BlogPost

class Command(BaseCommand):
    help = 'Updates all blog posts with a specific author name and profile URL'

    def handle(self, *args, **kwargs):
        author_name = "Asif Ahmad"
        author_profile_url = "https://dev.to/devtoolkit_66accef6cc37"
        
        posts = BlogPost.objects.all()
        count = posts.count()
        
        self.stdout.write(f'Updating {count} blog posts...')
        
        # Using update() for efficient bulk update
        updated_count = posts.update(
            author_name=author_name,
            author_profile_url=author_profile_url
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} blog posts with author: {author_name}'))
