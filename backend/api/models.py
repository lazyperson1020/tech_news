from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    h_index = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    credentials = models.CharField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    profile_picture = models.FileField(upload_to='profiles/', blank=True, null=True)  # Use FileField instead of ImageField
    is_author = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        ordering = ['-created_at']

class Article(models.Model):
    SOURCE_CHOICES = [
        ('newsapi', 'NewsAPI'),
        ('tavily', 'Tavily'),
        ('user', 'User Generated'),
    ]
    
    CATEGORY_CHOICES = [
        ('ai_ml', 'AI/ML'),
        ('blockchain', 'Blockchain'),
        ('web_dev', 'Web Development'),
        ('app_dev', 'App Development'),
        ('cybersecurity', 'Cybersecurity'),
        ('cloud', 'Cloud Computing'),
        ('general', 'General Tech'),
    ]
    
    title = models.CharField(max_length=500)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='newsapi')
    source_url = models.URLField(max_length=1000, blank=True, null=True)
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_approved = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.article.title}"

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    categories = models.JSONField(default=list)
    notification_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"

    class Meta:
        verbose_name_plural = "User Preferences"

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role}: {self.content[:50]}"
