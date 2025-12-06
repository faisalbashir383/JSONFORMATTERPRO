from django.contrib import admin
from .models import BlogCategory, BlogPost, SiteSettings, VisitorLog, PageView, ContactMessage


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


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'country', 'city', 'device_type', 'browser', 'visit_count', 'first_visit', 'last_visit', 'is_bot']
    list_filter = ['is_bot', 'is_mobile', 'device_type', 'country_code', 'first_visit']
    search_fields = ['ip_address', 'country', 'city', 'browser', 'os']
    readonly_fields = ['ip_address', 'session_key', 'country', 'country_code', 'city', 'region', 
                       'latitude', 'longitude', 'user_agent', 'browser', 'browser_version',
                       'device_type', 'os', 'os_version', 'referrer', 'landing_page',
                       'first_visit', 'last_visit', 'visit_count', 'total_page_views', 'is_bot', 'is_mobile']
    date_hierarchy = 'first_visit'
    
    def has_add_permission(self, request):
        # Don't allow manual addition
        return False


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip_address', 'country_code', 'device_type', 'timestamp']
    list_filter = ['timestamp', 'country_code', 'device_type', 'method']
    search_fields = ['url', 'page_title', 'ip_address']
    readonly_fields = ['visitor', 'url', 'page_title', 'method', 'ip_address', 'user_agent',
                       'referrer', 'timestamp', 'load_time', 'session_key', 'country_code', 'device_type']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        # Don't allow manual addition
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for Contact Messages"""
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read', 'is_replied']
    list_filter = ['subject', 'is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'ip_address', 'user_agent']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied', 'replied_at', 'notes')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = 'Mark selected messages as unread'
