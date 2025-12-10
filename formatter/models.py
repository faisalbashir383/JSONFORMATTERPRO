"""
Blog models for JSON Formatter Pro
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


class SiteSettings(models.Model):
    """Global site settings - Only one instance should exist"""
    site_name = models.CharField(max_length=100, default="JSON Formatter Pro")
    base_url = models.URLField(max_length=200, default="https://jsonformatterpro.com", help_text="Base URL without trailing slash")
    site_description = models.TextField(default="Free online JSON formatter, validator, minifier, and converter tool")
    
    # SEO Keywords
    primary_keywords = models.TextField(
        default="json formatter, json validator, json beautifier, json minifier, json parser, json editor, json viewer, jsonlint, json lint, online json formatter, free json formatter, format json online, validate json, beautify json, json pretty print, json syntax checker, json error checker, online json validator, json tree view, json converter, json to xml, json to csv, json to yaml, api formatter, rest api json formatter, json file formatter, json linter, best json formatter 2024",
        help_text="Comma-separated primary keywords"
    )
    secondary_keywords = models.TextField(
        default="minify json, compact json, json debugging, json online editor, json beautifier online, json viewer online, json formatter tool, json validator online free, json escape online, json unescape, json tester, json formatter and validator, json compare, json diff, json schema validator, javascript object notation formatter, json data interchange format, format json file, validate json syntax, json readability tool, client side json formatter, secure json formatter, json formatter no signup, json explorer, json tree viewer, json graph view, json visualization, api response formatter, json file viewer, json file upload, drag and drop json, download json, large json files, json copy clipboard, json error detection, json corrector, json error finder, how to format json, how to validate json online, how to minify json, how to fix json syntax errors, how to convert json to xml, how to convert json to csv, json data formatter, json api formatter, json pretty printer, fix json errors, json syntax validation",
        help_text="Comma-separated secondary keywords"
    )
    
    # Social Media
    og_image = models.URLField(max_length=500, blank=True, help_text="Open Graph image URL")
    twitter_handle = models.CharField(max_length=50, blank=True, help_text="Twitter handle without @")
    
    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True, help_text="GA4 Measurement ID")
    google_search_console = models.TextField(blank=True, help_text="Google Search Console verification code")
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one SiteSettings instance can exist")
        return super().save(*args, **kwargs)
    
    def get_all_keywords(self):
        """Get all keywords as a comma-separated string"""
        return f"{self.primary_keywords}, {self.secondary_keywords}"


class BlogCategory(models.Model):
    """Category for organizing blog posts"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Blog post model with SEO fields"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    excerpt = models.TextField(max_length=300, help_text="Brief summary for SEO and listing pages")
    content = models.TextField(help_text="Use <pre><code class='language-python'>your code</code></pre> for code blocks")
    tags = models.CharField(max_length=200, help_text="Comma-separated tags", blank=True)
    
    # SEO fields
    meta_description = models.CharField(max_length=160, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=500, help_text="SEO keywords, comma-separated")
    
    # Timestamps
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Stats
    views = models.IntegerField(default=0)
    
    # Reading time (auto-calculated)
    reading_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    
    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['published']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.published and not self.published_at:
            self.published_at = timezone.now()
        # Calculate reading time (average 200 words per minute)
        word_count = len(self.content.split())
        self.reading_time = max(1, word_count // 200)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_related_posts(self, limit=3):
        """Get related posts from the same category"""
        return BlogPost.objects.filter(
            category=self.category,
            published=True
        ).exclude(id=self.id)[:limit]


class VisitorLog(models.Model):
    """Track unique visitors with IP, location, and device information"""
    # Visitor Identification
    ip_address = models.GenericIPAddressField(help_text="Visitor's IP address")
    session_key = models.CharField(max_length=40, blank=True, null=True, help_text="Session identifier")
    
    # Geolocation Data
    country = models.CharField(max_length=100, blank=True, null=True, help_text="Country name")
    country_code = models.CharField(max_length=2, blank=True, null=True, help_text="2-letter country code")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City name")
    region = models.CharField(max_length=100, blank=True, null=True, help_text="State/Region")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Device & Browser Information
    user_agent = models.TextField(blank=True, null=True, help_text="Full user agent string")
    browser = models.CharField(max_length=100, blank=True, null=True, help_text="Browser name")
    browser_version = models.CharField(max_length=50, blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True, help_text="Desktop/Mobile/Tablet")
    os = models.CharField(max_length=100, blank=True, null=True, help_text="Operating system")
    os_version = models.CharField(max_length=50, blank=True, null=True)
    
    # Referral Information
    referrer = models.URLField(max_length=500, blank=True, null=True, help_text="Referring URL")
    landing_page = models.CharField(max_length=500, blank=True, null=True, help_text="First page visited")
    
    # Visit Tracking
    first_visit = models.DateTimeField(auto_now_add=True, help_text="First time visitor arrived")
    last_visit = models.DateTimeField(auto_now=True, help_text="Most recent visit")
    visit_count = models.IntegerField(default=1, help_text="Number of visits by this user")
    total_page_views = models.IntegerField(default=0, help_text="Total pages viewed")
    
    # Flags
    is_bot = models.BooleanField(default=False, help_text="Detected as bot/crawler")
    is_mobile = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-last_visit']
        indexes = [
            models.Index(fields=['-last_visit']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['country_code']),
        ]
        verbose_name = "Visitor Log"
        verbose_name_plural = "Visitor Logs"
    
    def __str__(self):
        return f"{self.ip_address} - {self.country or 'Unknown'} ({self.first_visit.strftime('%Y-%m-%d')})"
    
    def increment_visit(self):
        """Increment visit count and update last visit time"""
        self.visit_count += 1
        self.save(update_fields=['visit_count', 'last_visit'])


class PageView(models.Model):
    """Track individual page views with detailed analytics"""
    visitor = models.ForeignKey(VisitorLog, on_delete=models.CASCADE, related_name='page_views', null=True, blank=True)
    
    # Page Information
    url = models.CharField(max_length=500, help_text="Page URL / path")
    page_title = models.CharField(max_length=200, blank=True, null=True)
    method = models.CharField(max_length=10, default='GET', help_text="HTTP method")
    
    # Request Details
    ip_address = models.GenericIPAddressField(help_text="IP address (denormalized for quick queries)")
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(max_length=500, blank=True, null=True)
    
    # Timing
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When page was viewed")
    load_time = models.IntegerField(blank=True, null=True, help_text="Page load time in milliseconds")
    
    # Session
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    # Analytics
    country_code = models.CharField(max_length=2, blank=True, null=True, help_text="Denormalized country code")
    device_type = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['url']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['country_code']),
        ]
        verbose_name = "Page View"
        verbose_name_plural = "Page Views"
    
    def __str__(self):
        return f"{self.url} - {self.ip_address} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"


class ContactMessage(models.Model):
    """Store contact form submissions"""
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback & Suggestions'),
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200, help_text="Sender's name")
    email = models.EmailField(help_text="Sender's email address")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, help_text="Message subject category")
    message = models.TextField(help_text="Message content")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the message was submitted")
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="Sender's IP address")
    user_agent = models.TextField(null=True, blank=True, help_text="Sender's browser user agent")
    
    # Status tracking
    is_read = models.BooleanField(default=False, help_text="Has this message been read?")
    is_replied = models.BooleanField(default=False, help_text="Has this message been replied to?")
    replied_at = models.DateTimeField(null=True, blank=True, help_text="When the reply was sent")
    notes = models.TextField(blank=True, help_text="Internal notes about this message")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['email']),
            models.Index(fields=['is_read']),
        ]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%Y-%m-%d')})"
    
    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    def mark_as_replied(self):
        """Mark message as replied"""
        self.is_replied = True
        self.replied_at = timezone.now()
        self.save(update_fields=['is_replied', 'replied_at'])


class Redirect(models.Model):
    """
    Manage URL redirects for SEO
    Supports both 301 (permanent) and 302 (temporary) redirects
    """
    REDIRECT_TYPES = [
        (301, 'Permanent (301) - SEO link juice preserved'),
        (302, 'Temporary (302) - No SEO value transfer'),
    ]
    
    old_path = models.CharField(
        max_length=500, 
        unique=True,
        help_text="Old URL path (e.g., /old-page/). Must start with /"
    )
    new_path = models.CharField(
        max_length=500,
        help_text="New URL path or full URL (e.g., /new-page/ or https://example.com/)"
    )
    redirect_type = models.IntegerField(
        choices=REDIRECT_TYPES, 
        default=301,
        help_text="301 for permanent moves (SEO-friendly), 302 for temporary redirects"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to disable this redirect without deleting it"
    )
    hit_count = models.IntegerField(
        default=0,
        help_text="Number of times this redirect has been triggered"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(
        blank=True,
        help_text="Optional notes about why this redirect exists"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['old_path']),
            models.Index(fields=['is_active']),
        ]
        verbose_name = "URL Redirect"
        verbose_name_plural = "URL Redirects"
    
    def __str__(self):
        status = "✓" if self.is_active else "✗"
        return f"{status} {self.old_path} → {self.new_path} ({self.redirect_type})"
    
    def save(self, *args, **kwargs):
        # Ensure old_path starts with /
        if self.old_path and not self.old_path.startswith('/'):
            self.old_path = '/' + self.old_path
        super().save(*args, **kwargs)
    
    def increment_hit_count(self):
        """Increment the hit counter"""
        self.hit_count += 1
        self.save(update_fields=['hit_count'])
