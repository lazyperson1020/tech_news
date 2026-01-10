import requests
from django.conf import settings
from datetime import datetime
from articles.models import Article, Category

class NewsAPIService:
    """Service for fetching news from NewsAPI"""
    
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"
    
    def fetch_tech_news(self, category='technology', page_size=20):
        """Fetch technology news"""
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'apiKey': self.api_key,
                'category': category,
                'language': 'en',
                'pageSize': page_size
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get('articles', []):
                article = self._process_article(item, 'news_api')
                if article:
                    articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"NewsAPI fetch error: {str(e)}")
            return []
    
    def _process_article(self, item, source):
        """Process and save article"""
        try:
            # Check if article already exists
            if Article.objects.filter(source_url=item.get('url')).exists():
                return None
            
            article = Article.objects.create(
                title=item.get('title', 'Untitled'),
                content=item.get('content') or item.get('description', ''),
                excerpt=item.get('description', '')[:500],
                source=source,
                source_name=item.get('source', {}).get('name', 'Unknown'),
                source_url=item.get('url', ''),
                featured_image=item.get('urlToImage', ''),
                status='published',
                published_at=datetime.fromisoformat(
                    item.get('publishedAt', '').replace('Z', '+00:00')
                ) if item.get('publishedAt') else datetime.now()
            )
            
            # Add default technology category
            tech_category, _ = Category.objects.get_or_create(
                name='Technology',
                defaults={'description': 'General technology news'}
            )
            article.categories.add(tech_category)
            
            return article
            
        except Exception as e:
            print(f"Error processing article: {str(e)}")
            return None


class TavilyService:
    """Service for fetching news from Tavily API"""
    
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com"
    
    def search_tech_news(self, query="technology news", max_results=10):
        """Search for technology news"""
        try:
            url = f"{self.base_url}/search"
            headers = {'Content-Type': 'application/json'}
            payload = {
                'api_key': self.api_key,
                'query': query,
                'max_results': max_results,
                'search_depth': 'basic',
                'include_answer': False
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get('results', []):
                article = self._process_article(item)
                if article:
                    articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Tavily fetch error: {str(e)}")
            return []
    
    def _process_article(self, item):
        """Process and save article from Tavily"""
        try:
            if Article.objects.filter(source_url=item.get('url')).exists():
                return None
            
            article = Article.objects.create(
                title=item.get('title', 'Untitled'),
                content=item.get('content', ''),
                excerpt=item.get('content', '')[:500],
                source='tavily',
                source_name='Tavily',
                source_url=item.get('url', ''),
                status='published',
                published_at=datetime.now()
            )
            
            tech_category, _ = Category.objects.get_or_create(
                name='Technology',
                defaults={'description': 'General technology news'}
            )
            article.categories.add(tech_category)
            
            return article
            
        except Exception as e:
            print(f"Error processing Tavily article: {str(e)}")
            return None