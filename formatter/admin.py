from django.contrib import admin
from .models import BlogCategory, BlogPost, SiteSettings, VisitorLog, PageView, ContactMessage, Redirect


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
    search_fields = ['ip_address', 'country', 'city', 'browser', 'os', 'referrer']
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
    search_fields = ['url', 'page_title', 'ip_address', 'referrer']
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


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    """Admin interface for managing URL redirects"""
    list_display = ['old_path', 'new_path', 'redirect_type', 'is_active', 'hit_count', 'created_at', 'updated_at']
    list_filter = ['redirect_type', 'is_active', 'created_at']
    search_fields = ['old_path', 'new_path', 'notes']
    list_editable = ['is_active']
    ordering = ['-created_at']
    readonly_fields = ['hit_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Redirect Configuration', {
            'fields': ('old_path', 'new_path', 'redirect_type', 'is_active')
        }),
        ('Statistics', {
            'fields': ('hit_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['enable_redirects', 'disable_redirects', 'reset_hit_counts']
    
    def enable_redirects(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} redirect(s) enabled.')
    enable_redirects.short_description = 'Enable selected redirects'
    
    def disable_redirects(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} redirect(s) disabled.')
    disable_redirects.short_description = 'Disable selected redirects'
    
    def reset_hit_counts(self, request, queryset):
        updated = queryset.update(hit_count=0)
        self.message_user(request, f'Hit counts reset for {updated} redirect(s).')
    reset_hit_counts.short_description = 'Reset hit counts to zero'


# ====================
# Tutorial System Admin
# ====================

from .models import ProgrammingLanguage, TutorialCategory, Tutorial, CodeExample, MCQQuestion, MCQOption


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'slug', 'syntax_highlight', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'slug', 'order', 'get_tutorials_count']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    def get_tutorials_count(self, obj):
        return obj.get_tutorials_count()
    get_tutorials_count.short_description = 'Published Tutorials'


class CodeExampleInline(admin.TabularInline):
    model = CodeExample
    extra = 1
    fields = ['language', 'title', 'code', 'output', 'explanation', 'order']
    ordering = ['order']


class MCQOptionInline(admin.TabularInline):
    model = MCQOption
    extra = 4
    fields = ['option_text', 'is_correct', 'order']
    ordering = ['order']


class MCQQuestionInline(admin.StackedInline):
    model = MCQQuestion
    extra = 1
    fields = ['question', 'explanation', 'order']
    ordering = ['order']
    show_change_link = True


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'order', 'views', 'updated_at']
    list_filter = ['category', 'is_published', 'created_at']
    list_editable = ['is_published', 'order']
    search_fields = ['title', 'description', 'content', 'meta_keywords']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Use {{CODE_EXAMPLE_1}}, {{CODE_EXAMPLE_2}} etc. as placeholders for code examples'
        }),
        ('SEO (50+ keywords required)', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'description': 'Add at least 50 comma-separated keywords for SEO optimization'
        }),
        ('Publishing', {
            'fields': ('is_published', 'order')
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [CodeExampleInline, MCQQuestionInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(CodeExample)
class CodeExampleAdmin(admin.ModelAdmin):
    list_display = ['title', 'tutorial', 'language', 'order']
    list_filter = ['language', 'tutorial__category']
    search_fields = ['title', 'code', 'explanation']
    ordering = ['tutorial', 'order']
    
    fieldsets = (
        ('Relationship', {
            'fields': ('tutorial', 'language', 'order')
        }),
        ('Code', {
            'fields': ('title', 'code', 'output', 'explanation')
        }),
    )


@admin.register(MCQQuestion)
class MCQQuestionAdmin(admin.ModelAdmin):
    list_display = ['short_question', 'tutorial', 'order', 'options_count']
    list_filter = ['tutorial__category', 'tutorial']
    search_fields = ['question', 'explanation']
    ordering = ['tutorial', 'order']
    inlines = [MCQOptionInline]
    
    def short_question(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    short_question.short_description = 'Question'
    
    def options_count(self, obj):
        return obj.options.count()
    options_count.short_description = 'Options'


@admin.register(MCQOption)
class MCQOptionAdmin(admin.ModelAdmin):
    list_display = ['short_option', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__tutorial']
    search_fields = ['option_text']
    list_editable = ['is_correct', 'order']
    
    def short_option(self, obj):
        return obj.option_text[:40] + '...' if len(obj.option_text) > 40 else obj.option_text
    short_option.short_description = 'Option'


