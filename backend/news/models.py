from django.db import models

class NewsSource(models.Model):
    """Configuration for external news sources"""
    name = models.CharField(max_length=100, unique=True)
    api_type = models.CharField(max_length=50, choices=[
        ('tavily', 'Tavily'),
        ('newsapi', 'NewsAPI'),
    ])
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    last_fetch = models.DateTimeField(null=True, blank=True)
    fetch_interval = models.IntegerField(default=60, help_text="Minutes between fetches")
    
    class Meta:
        db_table = 'news_sources'
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return self.name


class FetchLog(models.Model):
    """Log of news fetching operations"""
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, related_name='fetch_logs')
    status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('partial', 'Partial'),
    ])
    articles_fetched = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'fetch_logs'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.source.name} - {self.status} - {self.started_at}"