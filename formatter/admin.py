from django.contrib import admin
from .models import BlogCategory, BlogPost, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'base_url', 'site_description')
        }),
        ('SEO Keywords', {
            'fields': ('primary_keywords', 'secondary_keywords'),
            'description': 'Enter keywords separated by commas'
        }),
        ('Social Media', {
            'fields': ('og_image', 'twitter_handle')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id', 'google_search_console'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'published_at', 'views', 'reading_time']
    list_filter = ['published', 'category', 'published_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content')
        }),
        ('Meta & Tags', {
            'fields': ('tags', 'meta_description', 'meta_keywords')
        }),
        ('Publishing', {
            'fields': ('published', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views', 'reading_time'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['views', 'reading_time']
    
    def save_model(self, request, obj, form, change):
        """Auto-save with reading time calculation"""
        super().save_model(request, obj, form, change)
