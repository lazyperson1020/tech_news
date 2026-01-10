from django.db import models
from django.utils.text import slugify
from users.models import User

class Category(models.Model):
    """Technology domains/categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Article(models.Model):
    """Main article model for both news and user-generated content"""
    
    SOURCE_CHOICES = [
        ('news_api', 'News API'),
        ('tavily', 'Tavily'),
        ('user_generated', 'User Generated'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=550, unique=True, blank=True)
    content = models.TextField()
    summary = models.TextField(blank=True, help_text="AI-generated summary")
    excerpt = models.TextField(max_length=500, blank=True)
    
    # Author and Source
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='user_generated')
    source_name = models.CharField(max_length=200, blank=True, help_text="Original source name")
    source_url = models.URLField(blank=True, help_text="Original article URL")
    
    # Media
    featured_image = models.URLField(blank=True)
    featured_image_caption = models.CharField(max_length=300, blank=True)
    
    # Categorization
    categories = models.ManyToManyField(Category, related_name='articles')
    tags = models.JSONField(default=list)
    
    # Status and Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)
    
    # Engagement Metrics
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    bookmarks_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['slug']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Bookmark(models.Model):
    """User bookmarks for articles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarked_by')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bookmarks'
        unique_together = ('user', 'article')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.article.title}"


class Comment(models.Model):
    """Comments on articles"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField(max_length=2000)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"