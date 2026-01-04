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
    title = models.TextField(max_length=400)
    slug = models.SlugField(unique=True, max_length=250)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    excerpt = models.TextField(help_text="Brief summary for SEO and listing pages")
    content = models.TextField(help_text="Use <pre><code class='language-python'>your code</code></pre> for code blocks")
    tags = models.TextField(help_text="Comma-separated tags", blank=True)
    
    # SEO fields
    meta_description = models.TextField(help_text="SEO meta description")
    meta_keywords = models.TextField(help_text="SEO keywords, comma-separated")
    
    # Timestamps
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Stats
    views = models.IntegerField(default=0)
    
    # Reading time (auto-calculated)
    reading_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    
    # Author Details
    author_name = models.CharField(max_length=100, default="JSON Formatters Pro", help_text="Name of the article author")
    author_profile_url = models.URLField(blank=True, help_text="Link to author's profile (e.g., dev.to, github, twitter)")
    
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


# ====================
# Tutorial System Models
# ====================

class ProgrammingLanguage(models.Model):
    """Supported programming languages for tutorials"""
    name = models.CharField(max_length=50, help_text="Language name (e.g., Python, JavaScript)")
    slug = models.SlugField(unique=True, max_length=50)
    icon = models.CharField(max_length=50, default="💻", help_text="Emoji or icon class for the language")
    syntax_highlight = models.CharField(
        max_length=20, 
        default="python",
        help_text="Prism.js language identifier for syntax highlighting"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower = first)")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Programming Language"
        verbose_name_plural = "Programming Languages"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TutorialCategory(models.Model):
    """Categories for organizing tutorials (e.g., Basics, Control Flow, Functions)"""
    name = models.CharField(max_length=100, help_text="Category name")
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, help_text="Brief description of this category")
    icon = models.CharField(max_length=50, default="📂", help_text="Emoji or icon for the category")
    order = models.IntegerField(default=0, help_text="Display order (lower = first)")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Tutorial Category"
        verbose_name_plural = "Tutorial Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_tutorials_count(self):
        """Get count of published tutorials in this category"""
        return self.tutorials.filter(is_published=True).count()


class Tutorial(models.Model):
    """Individual tutorial/topic with content, code examples, and quizzes"""
    title = models.CharField(max_length=200, help_text="Tutorial title")
    slug = models.SlugField(unique=True, max_length=250)
    category = models.ForeignKey(
        TutorialCategory, 
        on_delete=models.CASCADE, 
        related_name='tutorials'
    )
    description = models.TextField(help_text="Brief description of what this tutorial covers")
    content = models.TextField(
        help_text="Rich HTML content. Use {{CODE_EXAMPLE_1}}, {{CODE_EXAMPLE_2}} etc. as placeholders for code examples"
    )
    
    # SEO Fields (50+ keywords each)
    meta_title = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="SEO title (leave blank to use tutorial title)"
    )
    meta_description = models.TextField(
        blank=True,
        help_text="SEO meta description (150-160 characters recommended)"
    )
    meta_keywords = models.TextField(
        help_text="50+ comma-separated SEO keywords for this tutorial"
    )
    
    # Publishing
    order = models.IntegerField(default=0, help_text="Display order within category (lower = first)")
    is_published = models.BooleanField(default=False)
    
    # Stats
    views = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category__order', 'order', 'title']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published']),
            models.Index(fields=['category', 'order']),
        ]
        verbose_name = "Tutorial"
        verbose_name_plural = "Tutorials"
    
    def __str__(self):
        return f"{self.category.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tutorial_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_code_examples_for_language(self, language):
        """Get code examples for a specific programming language"""
        return self.code_examples.filter(language=language).order_by('order')
    
    def get_next_tutorial(self):
        """Get the next tutorial in the same category"""
        return Tutorial.objects.filter(
            category=self.category,
            is_published=True,
            order__gt=self.order
        ).first()
    
    def get_previous_tutorial(self):
        """Get the previous tutorial in the same category"""
        return Tutorial.objects.filter(
            category=self.category,
            is_published=True,
            order__lt=self.order
        ).order_by('-order').first()


class CodeExample(models.Model):
    """Multi-language code examples for tutorials"""
    tutorial = models.ForeignKey(
        Tutorial, 
        on_delete=models.CASCADE, 
        related_name='code_examples'
    )
    language = models.ForeignKey(
        ProgrammingLanguage, 
        on_delete=models.CASCADE,
        related_name='code_examples'
    )
    title = models.CharField(max_length=200, help_text="Title for this code example")
    code = models.TextField(help_text="The actual code snippet")
    output = models.TextField(blank=True, help_text="Expected output when code is run")
    explanation = models.TextField(blank=True, help_text="Explanation of what this code does")
    order = models.IntegerField(default=0, help_text="Order of this example within the tutorial")
    
    class Meta:
        ordering = ['order']
        unique_together = ['tutorial', 'language', 'order']
        verbose_name = "Code Example"
        verbose_name_plural = "Code Examples"
    
    def __str__(self):
        return f"{self.tutorial.title} - {self.language.name} - {self.title}"


class MCQQuestion(models.Model):
    """Multiple Choice Questions for tutorial quizzes"""
    tutorial = models.ForeignKey(
        Tutorial, 
        on_delete=models.CASCADE, 
        related_name='mcq_questions'
    )
    question = models.TextField(help_text="The question text")
    explanation = models.TextField(
        blank=True, 
        help_text="Explanation shown after answering (regardless of correct/incorrect)"
    )
    order = models.IntegerField(default=0, help_text="Order of this question in the quiz")
    
    class Meta:
        ordering = ['order']
        verbose_name = "MCQ Question"
        verbose_name_plural = "MCQ Questions"
    
    def __str__(self):
        return f"{self.tutorial.title} - Q{self.order}: {self.question[:50]}..."
    
    def get_correct_option(self):
        """Get the correct answer option"""
        return self.options.filter(is_correct=True).first()


class MCQOption(models.Model):
    """Answer options for MCQ questions"""
    question = models.ForeignKey(
        MCQQuestion, 
        on_delete=models.CASCADE, 
        related_name='options'
    )
    option_text = models.CharField(max_length=500, help_text="The answer option text")
    is_correct = models.BooleanField(default=False, help_text="Is this the correct answer?")
    order = models.IntegerField(default=0, help_text="Display order of this option")
    
    class Meta:
        ordering = ['order']
        verbose_name = "MCQ Option"
        verbose_name_plural = "MCQ Options"
    
    def __str__(self):
        correct = "✓" if self.is_correct else "✗"
        return f"{correct} {self.option_text[:50]}..."


# ====================
# Typing Speed Test
# ====================

class TypingScore(models.Model):
    """Store typing test scores for global leaderboard"""
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('html', 'HTML/CSS'),
        ('sql', 'SQL'),
    ]
    
    # User identification
    username = models.CharField(max_length=50, help_text="Display name for leaderboard")
    session_key = models.CharField(max_length=100, blank=True, null=True, help_text="Browser session identifier")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    # Score data
    wpm = models.IntegerField(help_text="Words per minute")
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, help_text="Accuracy percentage")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='medium')
    duration = models.IntegerField(help_text="Test duration in seconds")
    
    # Additional stats
    total_characters = models.IntegerField(default=0)
    correct_characters = models.IntegerField(default=0)
    errors = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Flags
    is_verified = models.BooleanField(default=True, help_text="Flag for potential cheating detection")
    
    class Meta:
        ordering = ['-wpm', '-accuracy']
        indexes = [
            models.Index(fields=['-wpm']),
            models.Index(fields=['level', '-wpm']),
            models.Index(fields=['session_key']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = "Typing Score"
        verbose_name_plural = "Typing Scores"
    
    def __str__(self):
        return f"{self.username} - {self.wpm} WPM ({self.level})"
    
    @classmethod
    def get_rank(cls, wpm, level=None):
        """Get rank for a given WPM score"""
        query = cls.objects.filter(is_verified=True)
        if level:
            query = query.filter(level=level)
        return query.filter(wpm__gt=wpm).count() + 1
    
    @classmethod
    def get_top_scores(cls, limit=20, level=None):
        """Get top scores for leaderboard"""
        query = cls.objects.filter(is_verified=True)
        if level and level != 'all':
            query = query.filter(level=level)
        return query.order_by('-wpm', '-accuracy')[:limit]
    
    @classmethod
    def get_user_best(cls, session_key, level=None):
        """Get user's best score"""
        query = cls.objects.filter(session_key=session_key)
        if level:
            query = query.filter(level=level)
        return query.order_by('-wpm').first()
    
    @classmethod
    def get_user_scores(cls, session_key, limit=10):
        """Get user's recent scores"""
        return cls.objects.filter(session_key=session_key).order_by('-created_at')[:limit]


# ====================
# Careers / Job Postings
# ====================

class JobPosting(models.Model):
    """Job posting for careers page with SEO optimization"""
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('engineering', 'Engineering'),
        ('product', 'Product'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('operations', 'Operations'),
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, help_text="Job title")
    slug = models.SlugField(unique=True, max_length=250)
    department = models.CharField(
        max_length=50, 
        choices=DEPARTMENT_CHOICES, 
        default='engineering',
        help_text="Department this role belongs to"
    )
    location = models.CharField(
        max_length=200, 
        default="Delhi, India",
        help_text="Job location (e.g., 'Delhi, India' or 'Remote')"
    )
    employment_type = models.CharField(
        max_length=20, 
        choices=EMPLOYMENT_TYPE_CHOICES, 
        default='full-time',
        help_text="Type of employment"
    )
    
    # Job Details
    description = models.TextField(
        help_text="Full job description (HTML supported)"
    )
    requirements = models.TextField(
        help_text="Skills and qualifications required (HTML supported)"
    )
    responsibilities = models.TextField(
        help_text="Key responsibilities (HTML supported)"
    )
    benefits = models.TextField(
        blank=True,
        help_text="Benefits and perks (HTML supported)"
    )
    
    # Salary Information
    salary_min = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Minimum salary (optional)"
    )
    salary_max = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Maximum salary (optional)"
    )
    salary_currency = models.CharField(
        max_length=10, 
        default="INR",
        help_text="Salary currency code"
    )
    show_salary = models.BooleanField(
        default=False,
        help_text="Display salary range on job posting"
    )
    
    # SEO Fields
    meta_title = models.CharField(
        max_length=200, 
        blank=True,
        help_text="SEO title (leave blank to use job title)"
    )
    meta_description = models.TextField(
        blank=True,
        help_text="SEO meta description (150-160 characters recommended)"
    )
    meta_keywords = models.TextField(
        blank=True,
        help_text="Comma-separated SEO keywords"
    )
    
    # Publishing
    is_active = models.BooleanField(
        default=True,
        help_text="Is this job currently open?"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this job at the top of listings"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Application
    apply_email = models.EmailField(
        blank=True,
        help_text="Email to receive applications"
    )
    apply_url = models.URLField(
        blank=True,
        help_text="External application URL"
    )
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['department']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = "Job Posting"
        verbose_name_plural = "Job Postings"
    
    def __str__(self):
        status = "✓" if self.is_active else "✗"
        return f"{status} {self.title} ({self.get_department_display()})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = f"{self.title} - Careers at JSON Formatters Pro"
        if not self.meta_description:
            self.meta_description = f"Apply for {self.title} position at JSON Formatters Pro. {self.get_employment_type_display()} role in {self.location}."
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'slug': self.slug})
    
    def get_salary_range(self):
        """Get formatted salary range if available"""
        if self.show_salary and self.salary_min:
            if self.salary_max:
                return f"{self.salary_currency} {self.salary_min:,} - {self.salary_max:,}"
            return f"{self.salary_currency} {self.salary_min:,}+"
        return None


class JobApplication(models.Model):
    """Store job applications submitted through the careers page"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    # Link to job posting
    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='applications',
        help_text="The job position applied for"
    )
    
    # Applicant Information
    full_name = models.CharField(max_length=200, help_text="Applicant's full name")
    email = models.EmailField(help_text="Applicant's email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Applicant's phone number")
    
    # Application Details
    cover_letter = models.TextField(
        blank=True,
        help_text="Cover letter or message from the applicant"
    )
    resume_url = models.URLField(
        blank=True,
        help_text="Link to resume (Google Drive, Dropbox, LinkedIn, etc.)"
    )
    portfolio_url = models.URLField(
        blank=True,
        help_text="Link to portfolio or personal website"
    )
    linkedin_url = models.URLField(
        blank=True,
        help_text="LinkedIn profile URL"
    )
    
    # Experience
    years_of_experience = models.PositiveIntegerField(
        default=0,
        help_text="Years of relevant experience"
    )
    current_company = models.CharField(
        max_length=200,
        blank=True,
        help_text="Current or most recent company"
    )
    current_role = models.CharField(
        max_length=200,
        blank=True,
        help_text="Current or most recent job title"
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Application status"
    )
    
    # Metadata
    ip_address = models.GenericIPAddressField(
        null=True, blank=True,
        help_text="Applicant's IP address"
    )
    user_agent = models.TextField(
        blank=True,
        help_text="Browser user agent"
    )
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Admin notes
    notes = models.TextField(
        blank=True,
        help_text="Internal notes about this application"
    )
    
    class Meta:
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['-applied_at']),
            models.Index(fields=['job']),
            models.Index(fields=['status']),
            models.Index(fields=['email']),
        ]
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
    
    def __str__(self):
        return f"{self.full_name} - {self.job.title} ({self.get_status_display()})"


class MockEndpoint(models.Model):
    """
    Stores user-created mock API endpoints with optional IP restriction.
    These endpoints can be accessed via /api/mock/{endpoint_id}/
    """
    
    HTTP_METHODS = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
    ]
    
    # Unique identifier for the endpoint (UUID format)
    endpoint_id = models.CharField(max_length=36, unique=True, db_index=True)
    
    # Endpoint configuration
    name = models.CharField(max_length=100, blank=True, help_text="Optional name for this endpoint")
    path = models.CharField(max_length=200, default="/api/users", help_text="API path e.g., /api/users")
    method = models.CharField(max_length=10, choices=HTTP_METHODS, default='GET')
    status_code = models.IntegerField(default=200)
    response_body = models.TextField(help_text="JSON response body (can include template variables)")
    content_type = models.CharField(max_length=100, default='application/json')
    
    # Simulation settings
    latency_ms = models.IntegerField(default=0, help_text="Response delay in milliseconds")
    error_rate = models.IntegerField(default=0, help_text="Percentage chance of returning 500 error")
    record_count = models.IntegerField(default=1, help_text="Number of records to generate in array responses")
    
    # IP Restriction
    ip_restriction_enabled = models.BooleanField(default=False, help_text="Only allow requests from specified IPs")
    allowed_ips = models.TextField(blank=True, help_text="Comma-separated list of allowed IP addresses")
    
    # Custom headers (JSON)
    custom_headers = models.TextField(blank=True, default='{}', help_text="Custom response headers as JSON")
    
    # Metadata
    creator_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Endpoint expires after this time")
    request_count = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['endpoint_id']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['expires_at']),
        ]
        verbose_name = "Mock Endpoint"
        verbose_name_plural = "Mock Endpoints"
    
    def __str__(self):
        return f"{self.method} {self.path} ({self.endpoint_id})"
    
    def save(self, *args, **kwargs):
        if not self.endpoint_id:
            self.endpoint_id = self.generate_endpoint_id()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_endpoint_id():
        """Generate a unique UUID endpoint ID"""
        import uuid
        return str(uuid.uuid4())
    
    def is_expired(self):
        """Check if the endpoint has expired"""
        if self.expires_at is None:
            return False
        return timezone.now() > self.expires_at
    
    def is_ip_allowed(self, client_ip):
        """Check if a client IP is allowed to access this endpoint"""
        if not self.ip_restriction_enabled:
            return True
        
        if not self.allowed_ips:
            return False
        
        allowed_list = [ip.strip() for ip in self.allowed_ips.split(',') if ip.strip()]
        return client_ip in allowed_list
    
    def increment_request_count(self):
        """Increment the request counter and update last_accessed"""
        self.request_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['request_count', 'last_accessed'])
    
    def get_allowed_ips_list(self):
        """Return allowed IPs as a list"""
        if not self.allowed_ips:
            return []
        return [ip.strip() for ip in self.allowed_ips.split(',') if ip.strip()]


# ====================
# Domain Age SEO - Approved Domains for Dynamic Pages
# ====================

class ApprovedDomain(models.Model):
    """
    Admin-controlled list of domains that can have indexable dynamic result pages.
    Used for /domain-age/<domain>/ URLs to capture branded search queries like
    "indianexpress.com domain registration date"
    """
    domain = models.CharField(
        max_length=255, 
        unique=True, 
        db_index=True,
        help_text="Domain name without protocol (e.g., 'indianexpress.com')"
    )
    is_indexable = models.BooleanField(
        default=False,
        help_text="If True, page will have 'index, follow'. If False, 'noindex, follow'"
    )
    meta_title = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Custom SEO title (leave blank for auto-generated)"
    )
    meta_description = models.TextField(
        blank=True,
        help_text="Custom SEO description (leave blank for auto-generated)"
    )
    notes = models.TextField(
        blank=True,
        help_text="Internal notes about this domain"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['domain']),
            models.Index(fields=['is_indexable']),
        ]
        verbose_name = "Approved Domain"
        verbose_name_plural = "Approved Domains"
    
    def __str__(self):
        status = "✓ Index" if self.is_indexable else "✗ NoIndex"
        return f"{status} - {self.domain}"
    
    def save(self, *args, **kwargs):
        # Clean domain: remove protocol and www
        if self.domain:
            import re
            self.domain = re.sub(r'^https?://', '', self.domain)
            self.domain = re.sub(r'^www\.', '', self.domain)
            self.domain = self.domain.lower().strip()
        super().save(*args, **kwargs)


class DomainPageVisit(models.Model):
    """
    Track unique visits to dynamic domain age pages.
    Used to show popular domains and visit counts.
    """
    domain = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Domain name being checked"
    )
    visit_count = models.PositiveIntegerField(
        default=0,
        help_text="Total visits to this domain's page"
    )
    unique_visitors = models.PositiveIntegerField(
        default=0,
        help_text="Unique IP addresses that visited"
    )
    last_cached_data = models.TextField(
        blank=True,
        help_text="Cached WHOIS JSON data"
    )
    cache_updated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When WHOIS data was last cached"
    )
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_count']
        indexes = [
            models.Index(fields=['domain']),
            models.Index(fields=['-visit_count']),
        ]
        verbose_name = "Domain Page Visit"
        verbose_name_plural = "Domain Page Visits"
    
    def __str__(self):
        return f"{self.domain} - {self.visit_count} visits"
    
    @classmethod
    def record_visit(cls, domain, ip_address):
        """Record a visit, incrementing counters"""
        from django.core.cache import cache
        
        # Clean domain
        import re
        domain = domain.lower().strip()
        domain = re.sub(r'^https?://', '', domain)
        domain = re.sub(r'^www\.', '', domain)
        
        # Get or create the record
        obj, created = cls.objects.get_or_create(domain=domain)
        obj.visit_count += 1
        
        # Check if this IP is unique for this domain (using cache)
        cache_key = f"domain_visit_{domain}_{ip_address}"
        if not cache.get(cache_key):
            obj.unique_visitors += 1
            cache.set(cache_key, True, 86400)  # 24 hours
        
        obj.save()
        return obj
    
    @classmethod
    def get_top_domains(cls, limit=10):
        """Get top visited domains"""
        return cls.objects.order_by('-visit_count')[:limit]


class DummyJsonApiLog(models.Model):
    """Track Dummy JSON API requests"""
    ENDPOINT_CHOICES = [
        ('users', 'Users'),
        ('products', 'Products'),
        ('posts', 'Posts'),
        ('comments', 'Comments'),
        ('todos', 'Todos'),
        ('companies', 'Companies'),
    ]
    
    endpoint = models.CharField(max_length=20, choices=ENDPOINT_CHOICES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    request_count = models.PositiveIntegerField(default=1)
    first_request = models.DateTimeField(auto_now_add=True)
    last_request = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dummy JSON API Log"
        verbose_name_plural = "Dummy JSON API Logs"
        unique_together = ['endpoint', 'ip_address']
        indexes = [
            models.Index(fields=['endpoint']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['last_request']),
        ]
    
    def __str__(self):
        return f"{self.ip_address} - {self.endpoint} ({self.request_count} requests)"
    
    @classmethod
    def log_request(cls, endpoint, ip_address, user_agent=None):
        """Log an API request, incrementing count for existing IP+endpoint combo"""
        obj, created = cls.objects.get_or_create(
            endpoint=endpoint,
            ip_address=ip_address,
            defaults={'user_agent': user_agent}
        )
        if not created:
            obj.request_count += 1
            obj.save(update_fields=['request_count', 'last_request'])
        return obj
    
    @classmethod
    def get_stats(cls):
        """Get overall API stats"""
        from django.db.models import Sum, Count
        return {
            'total_requests': cls.objects.aggregate(total=Sum('request_count'))['total'] or 0,
            'unique_ips': cls.objects.values('ip_address').distinct().count(),
            'by_endpoint': {
                e[0]: cls.objects.filter(endpoint=e[0]).aggregate(
                    total=Sum('request_count'),
                    unique_ips=Count('ip_address', distinct=True)
                ) for e in cls.ENDPOINT_CHOICES
            }
        }
