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
        default="json formatter, json validator, json minifier, json beautifier, json parser",
        help_text="Comma-separated primary keywords"
    )
    secondary_keywords = models.TextField(
        default="format json online, validate json, minify json, json to xml, json to csv, base64 encoder",
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
    meta_keywords = models.CharField(max_length=200, help_text="SEO keywords, comma-separated")
    
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
