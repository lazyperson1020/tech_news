import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_summary(content, max_words=150):
    """
    Generate AI-powered summary using OpenAI GPT
    
    Args:
        content (str): Article content to summarize
        max_words (int): Maximum words in summary
    
    Returns:
        str: Generated summary
    """
    try:
        prompt = f"""Summarize the following technical article in approximately {max_words} words. 
        Focus on the key points, main findings, and important takeaways.
        
        Article:
        {content[:4000]}"""  # Limit content length
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical writer who creates concise, accurate summaries of technology articles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        raise Exception(f"Failed to generate summary: {str(e)}")


def generate_tags(content, max_tags=5):
    """Generate relevant tags for an article"""
    try:
        prompt = f"""Generate {max_tags} relevant tags for this technical article. 
        Return only the tags as a comma-separated list.
        
        Article excerpt:
        {content[:2000]}"""
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You generate relevant tags for technical articles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.5
        )
        
        tags_str = response.choices[0].message.content.strip()
        tags = [tag.strip() for tag in tags_str.split(',')]
        return tags[:max_tags]
        
    except Exception as e:
        return []