from celery import shared_task
from .services import NewsAPIService, TavilyService
from .models import NewsSource, FetchLog
from datetime import datetime

@shared_task
def fetch_news_from_all_sources():
    """Background task to fetch news from all active sources"""
    active_sources = NewsSource.objects.filter(is_active=True)
    
    for source in active_sources:
        fetch_news_from_source.delay(source.id)


@shared_task
def fetch_news_from_source(source_id):
    """Fetch news from a specific source"""
    try:
        source = NewsSource.objects.get(id=source_id)
        log = FetchLog.objects.create(source=source, status='in_progress')
        
        articles_fetched = 0
        
        if source.api_type == 'newsapi':
            service = NewsAPIService()
            articles = service.fetch_tech_news()
            articles_fetched = len(articles)
        
        elif source.api_type == 'tavily':
            service = TavilyService()
            articles = service.search_tech_news()
            articles_fetched = len(articles)
        
        # Update log
        log.status = 'success'
        log.articles_fetched = articles_fetched
        log.completed_at = datetime.now()
        log.save()
        
        # Update source last fetch
        source.last_fetch = datetime.now()
        source.save()
        
        return articles_fetched
        
    except Exception as e:
        if 'log' in locals():
            log.status = 'failed'
            log.error_message = str(e)
            log.completed_at = datetime.now()
            log.save()
        raise


@shared_task
def generate_article_summaries():
    """Generate AI summaries for articles without summaries"""
    from articles.models import Article
    from ai_services.summarizer import generate_summary
    
    articles = Article.objects.filter(
        status='published',
        summary=''
    )[:10]  # Process 10 at a time
    
    for article in articles:
        try:
            summary = generate_summary(article.content)
            article.summary = summary
            article.save()
        except Exception as e:
            print(f"Failed to generate summary for article {article.id}: {str(e)}")