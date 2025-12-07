"""
Context processors for global template variables
"""

from .models import SiteSettings


def site_settings(request):
    """Make site settings available in all templates"""
    try:
        settings = SiteSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            settings = SiteSettings.objects.create()
    except:
        # Fallback if table doesn't exist yet
        settings = None
    
    return {
        'site_settings': settings,
        'SITE_URL': settings.base_url if settings else 'https://jsonformatterspro.com',
        'SITE_NAME': settings.site_name if settings else 'JSON Formatters Pro',
    }
