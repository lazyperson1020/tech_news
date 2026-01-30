import requests
from django.conf import settings
from openai import OpenAI

class NewsService:
    def __init__(self):
        self.news_api_key = settings.NEWS_API_KEY
        self.tavily_api_key = settings.TAVILY_API_KEY
    
    def fetch_news(self, category='technology', limit=20):
        # Use only Tavily for better quality news
        articles = []
        
        if self.tavily_api_key:
            articles.extend(self._fetch_from_tavily(category, limit))
        
        return articles[:limit]
    
    def _fetch_from_newsapi(self, category, limit):
        url = 'https://newsapi.org/v2/everything'
        
        category_keywords = {
            'ai_ml': 'artificial intelligence OR machine learning',
            'blockchain': 'blockchain OR cryptocurrency',
            'web_dev': 'web development OR javascript OR react',
            'app_dev': 'mobile app development OR iOS OR Android',
            'cybersecurity': 'cybersecurity OR hacking OR data breach',
            'cloud': 'cloud computing OR AWS OR Azure',
            'general': 'technology OR tech news'
        }
        
        query = category_keywords.get(category, 'technology')
        
        params = {
            'q': query,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': limit,
            'apiKey': self.news_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get('articles', []):
                if item.get('title') and item.get('description'):
                    articles.append({
                        'title': item['title'],
                        'content': item.get('description', '') + '\n\n' + item.get('content', ''),
                        'source': 'newsapi',
                        'source_url': item.get('url', ''),
                        'image_url': item.get('urlToImage', ''),
                        'category': category
                    })
            
            return articles
        except Exception as e:
            print(f"NewsAPI error: {e}")
            return []
    
    def _fetch_from_tavily(self, category, limit):
        if not self.tavily_api_key:
            return []
        
        url = 'https://api.tavily.com/search'
        
        category_queries = {
            'ai_ml': 'latest artificial intelligence machine learning news',
            'blockchain': 'latest blockchain cryptocurrency news',
            'web_dev': 'latest web development technology news',
            'app_dev': 'latest mobile app development news',
            'cybersecurity': 'latest cybersecurity news',
            'cloud': 'latest cloud computing news',
            'general': 'latest technology news'
        }
        
        query = category_queries.get(category, 'latest technology news')
        
        payload = {
            'api_key': self.tavily_api_key,
            'query': query,
            'search_depth': 'basic',
            'max_results': limit
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get('results', []):
                articles.append({
                    'title': item.get('title', ''),
                    'content': item.get('content', ''),
                    'source': 'tavily',
                    'source_url': item.get('url', ''),
                    'image_url': item.get('image_url', ''),
                    'category': category
                })
            
            return articles
        except Exception as e:
            print(f"Tavily error: {e}")
            return []

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    def summarize_article(self, content, max_words=150):
        if not self.client:
            return None
        
        try:
            response = self.client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {
                        'role': 'system',
                        'content': f'Summarize the following article in {max_words} words or less. Be concise and capture the main points.'
                    },
                    {
                        'role': 'user',
                        'content': content
                    }
                ],
                max_tokens=max_words // 4 + 100,
                temperature=0.5
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
            return None
    
    def chat(self, messages):
        """
        Send a message to the LLM and get a response.
        messages: list of dicts with 'role' and 'content' keys
        """
        if not self.client:
            return None
        
        try:
            response = self.client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI chat error: {e}")
            return None

