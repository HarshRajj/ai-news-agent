from newsapi import NewsApiClient
from typing import List, Dict
import datetime

class NewsAPIClient:
    """Simple wrapper for NewsAPI.org."""
    
    def __init__(self, api_key: str):
        self.client = NewsApiClient(api_key=api_key)
    
    def search_articles(self, query: str, from_date: datetime.date, 
                       to_date: datetime.date, limit: int = 5) -> List[Dict]:
        """Search articles with specific date range."""
        try:
            print(f"[DEBUG] Searching for: '{query}' from {from_date} to {to_date}")
            
            response = self.client.get_everything(
                q=query,
                from_param=from_date.isoformat(),
                to=to_date.isoformat(),
                language='en',
                sort_by='publishedAt',
                page_size=limit
            )
            
            if response['status'] == 'ok' and response['articles']:
                return response['articles'][:limit]
            return []
            
        except Exception as e:
            print(f"[ERROR] NewsAPI search failed: {e}")
            return []