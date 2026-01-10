from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    is_author = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """Extended profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=1000)
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Professional Information
    h_index = models.IntegerField(default=0, help_text="H-index for research impact")
    current_company = models.CharField(max_length=200, blank=True)
    domain_expertise = models.JSONField(default=list, help_text="List of expertise domains")
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    
    # Social Links
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    
    # Preferences
    preferred_categories = models.JSONField(default=list)
    notification_enabled = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"