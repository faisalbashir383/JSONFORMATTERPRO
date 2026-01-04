from django.contrib import admin
from .models import BlogCategory, BlogPost, SiteSettings, VisitorLog, PageView, ContactMessage, Redirect, DummyJsonApiLog


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
        ('Author Details', {
            'fields': ('author_name', 'author_profile_url')
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
    list_display = ['ip_address', 'referrer', 'landing_page', 'country', 'city', 'device_type', 'browser', 'visit_count', 'first_visit', 'last_visit', 'is_bot']
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


# ====================
# Typing Speed Test Admin
# ====================

from .models import TypingScore


@admin.register(TypingScore)
class TypingScoreAdmin(admin.ModelAdmin):
    list_display = ['username', 'wpm', 'accuracy', 'level', 'duration', 'created_at', 'is_verified']
    list_filter = ['level', 'is_verified', 'created_at']
    search_fields = ['username', 'ip_address', 'session_key']
    list_editable = ['is_verified']
    ordering = ['-wpm', '-accuracy']
    date_hierarchy = 'created_at'
    readonly_fields = ['session_key', 'ip_address', 'created_at']
    
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'session_key', 'ip_address')
        }),
        ('Score', {
            'fields': ('wpm', 'accuracy', 'level', 'duration')
        }),
        ('Details', {
            'fields': ('total_characters', 'correct_characters', 'errors'),
            'classes': ('collapse',)
        }),
        ('Admin', {
            'fields': ('is_verified', 'created_at'),
        }),
    )
    
    actions = ['verify_scores', 'unverify_scores']
    
    def verify_scores(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} score(s) verified.')
    verify_scores.short_description = 'Mark selected as verified'
    
    def unverify_scores(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} score(s) marked as suspicious.')
    unverify_scores.short_description = 'Mark selected as suspicious'


# ====================
# Job Postings Admin
# ====================

from .models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'location', 'employment_type', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'department', 'employment_type', 'created_at']
    search_fields = ['title', 'description', 'requirements', 'responsibilities', 'meta_keywords']
    list_editable = ['is_active', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-is_featured', '-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'department', 'location', 'employment_type')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'responsibilities', 'benefits')
        }),
        ('Salary (Optional)', {
            'fields': ('show_salary', 'salary_min', 'salary_max', 'salary_currency'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
            'description': 'SEO fields for search engine optimization'
        }),
        ('Publishing', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Application', {
            'fields': ('apply_email', 'apply_url'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_jobs', 'deactivate_jobs', 'feature_jobs', 'unfeature_jobs']
    
    def activate_jobs(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} job(s) activated.')
    activate_jobs.short_description = 'Activate selected jobs'
    
    def deactivate_jobs(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} job(s) deactivated.')
    deactivate_jobs.short_description = 'Deactivate selected jobs'
    
    def feature_jobs(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} job(s) featured.')
    feature_jobs.short_description = 'Feature selected jobs'
    
    def unfeature_jobs(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} job(s) unfeatured.')
    unfeature_jobs.short_description = 'Unfeature selected jobs'


# ====================
# Job Applications Admin
# ====================

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'job', 'status', 'years_of_experience', 'applied_at']
    list_filter = ['status', 'job', 'applied_at', 'years_of_experience']
    search_fields = ['full_name', 'email', 'phone', 'current_company', 'current_role', 'cover_letter']
    list_editable = ['status']
    ordering = ['-applied_at']
    date_hierarchy = 'applied_at'
    readonly_fields = ['job', 'full_name', 'email', 'phone', 'cover_letter', 'resume_url', 
                       'portfolio_url', 'linkedin_url', 'years_of_experience', 'current_company',
                       'current_role', 'ip_address', 'user_agent', 'applied_at', 'updated_at']
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Application', {
            'fields': ('job', 'cover_letter', 'years_of_experience', 'current_company', 'current_role')
        }),
        ('Links', {
            'fields': ('resume_url', 'portfolio_url', 'linkedin_url')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_reviewing', 'mark_as_shortlisted', 'mark_as_rejected']
    
    def mark_as_reviewing(self, request, queryset):
        updated = queryset.update(status='reviewing')
        self.message_user(request, f'{updated} application(s) marked as under review.')
    mark_as_reviewing.short_description = 'Mark as Under Review'
    
    def mark_as_shortlisted(self, request, queryset):
        updated = queryset.update(status='shortlisted')
        self.message_user(request, f'{updated} application(s) shortlisted.')
    mark_as_shortlisted.short_description = 'Mark as Shortlisted'
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} application(s) rejected.')
    mark_as_rejected.short_description = 'Mark as Rejected'
    
    def has_add_permission(self, request):
        # Applications come from the website, not admin
        return False


from .models import MockEndpoint


@admin.register(MockEndpoint)
class MockEndpointAdmin(admin.ModelAdmin):
    list_display = ['endpoint_id', 'name', 'method', 'path', 'status_code', 'ip_restriction_enabled', 'request_count', 'created_at']
    list_filter = ['method', 'ip_restriction_enabled', 'created_at']
    search_fields = ['endpoint_id', 'name', 'path', 'allowed_ips', 'creator_ip']
    readonly_fields = ['endpoint_id', 'created_at', 'updated_at', 'request_count', 'last_accessed', 'creator_ip']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Endpoint Configuration', {
            'fields': ('endpoint_id', 'name', 'path', 'method', 'status_code')
        }),
        ('Response', {
            'fields': ('response_body', 'content_type', 'custom_headers')
        }),
        ('Simulation', {
            'fields': ('latency_ms', 'error_rate')
        }),
        ('IP Restriction', {
            'fields': ('ip_restriction_enabled', 'allowed_ips')
        }),
        ('Metadata', {
            'fields': ('creator_ip', 'request_count', 'last_accessed', 'expires_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ====================
# Domain Age SEO - Approved Domains Admin
# ====================

from .models import ApprovedDomain


@admin.register(ApprovedDomain)
class ApprovedDomainAdmin(admin.ModelAdmin):
    """Admin for managing indexable domain age result pages"""
    list_display = ['domain', 'is_indexable', 'meta_title', 'created_at', 'updated_at']
    list_filter = ['is_indexable', 'created_at']
    search_fields = ['domain', 'meta_title', 'notes']
    list_editable = ['is_indexable']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Domain', {
            'fields': ('domain', 'is_indexable')
        }),
        ('SEO Overrides (Optional)', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Leave blank to use auto-generated SEO content'
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_indexable', 'make_noindex']
    
    def make_indexable(self, request, queryset):
        updated = queryset.update(is_indexable=True)
        self.message_user(request, f'{updated} domain(s) marked as indexable.')
    make_indexable.short_description = 'Mark selected as indexable'
    
    def make_noindex(self, request, queryset):
        updated = queryset.update(is_indexable=False)
        self.message_user(request, f'{updated} domain(s) marked as noindex.')
    make_noindex.short_description = 'Mark selected as noindex'


from .models import DomainPageVisit


@admin.register(DomainPageVisit)
class DomainPageVisitAdmin(admin.ModelAdmin):
    """Admin for viewing domain page visit statistics"""
    list_display = ['domain', 'visit_count', 'unique_visitors', 'cache_updated_at', 'last_visit']
    list_filter = ['cache_updated_at', 'first_visit']
    search_fields = ['domain']
    readonly_fields = ['domain', 'visit_count', 'unique_visitors', 'first_visit', 'last_visit', 'cache_updated_at']
    ordering = ['-visit_count']
    
    fieldsets = (
        ('Domain Stats', {
            'fields': ('domain', 'visit_count', 'unique_visitors')
        }),
        ('Timestamps', {
            'fields': ('first_visit', 'last_visit', 'cache_updated_at'),
        }),
        ('Cached Data', {
            'fields': ('last_cached_data',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Records are auto-created


@admin.register(DummyJsonApiLog)
class DummyJsonApiLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'endpoint', 'request_count', 'first_request', 'last_request']
    list_filter = ['endpoint', 'first_request', 'last_request']
    search_fields = ['ip_address', 'user_agent']
    readonly_fields = ['ip_address', 'endpoint', 'user_agent', 'request_count', 'first_request', 'last_request']
    ordering = ['-request_count']
    
    def has_add_permission(self, request):
        return False
    
    def changelist_view(self, request, extra_context=None):
        from .models import DummyJsonApiLog
        stats = DummyJsonApiLog.get_stats()
        extra_context = extra_context or {}
        extra_context['api_stats'] = stats
        return super().changelist_view(request, extra_context=extra_context)
