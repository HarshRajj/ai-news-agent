from typing import List, Dict, Optional
import datetime
from config import NEWSAPI_KEY
from parsers import DateParser, QueryCleaner
from clients import NewsAPIClient
from services import ResponseFormatter

class NewsService:
    """Main news service orchestrating all operations."""
    
    def __init__(self):
        self.news_client = NewsAPIClient(NEWSAPI_KEY)
        self.date_parser = DateParser()
        self.query_cleaner = QueryCleaner()
        self.formatter = ResponseFormatter()
    
    def fetch_headlines(self, query: str, limit: int = 5, 
                       from_date: Optional[datetime.date] = None, 
                       to_date: Optional[datetime.date] = None) -> List[Dict]:
        """Fetch news articles for a given query with progressive fallback."""
        try:
            # Parse dates from query if not provided
            if from_date is None or to_date is None:
                parsed_from, parsed_to = self.date_parser.parse_date_query(query)
                from_date = from_date or parsed_from
                to_date = to_date or parsed_to
            
            # Clean the query to remove date-related terms
            clean_query = self.query_cleaner.clean_query_from_dates(query)
            
            # First attempt: Search with original date range
            articles = self.news_client.search_articles(clean_query, from_date, to_date, limit)
            
            # If no articles found and searching for recent dates, try progressive fallback
            if not articles:
                today = datetime.date.today()
                
                # Check if we were searching for very recent dates (today or yesterday)
                if from_date >= (today - datetime.timedelta(days=2)):
                    print(f"[FALLBACK] No recent articles found. Searching past week...")
                    
                    # Fallback 1: Search past week
                    week_ago = today - datetime.timedelta(days=7)
                    articles = self.news_client.search_articles(clean_query, week_ago, today, limit)
                    
                    if articles:
                        print(f"[SUCCESS] Found {len(articles)} articles from the past week")
                    else:
                        print(f"[FALLBACK] No articles in past week. Searching past month...")
                        
                        # Fallback 2: Search past month
                        month_ago = today - datetime.timedelta(days=30)
                        articles = self.news_client.search_articles(clean_query, month_ago, today, limit)
                        
                        if articles:
                            print(f"[SUCCESS] Found {len(articles)} articles from the past month")
            
            return articles
            
        except Exception as e:
            print(f"News Service Error: {e}")
            return []
    
    def format_articles(self, articles: List[Dict], query: str = "") -> str:
        """Format articles for display."""
        return self.formatter.format_articles(articles, query)
    
    def format_article_detail(self, article: Dict, scraped_content: Optional[str] = None) -> str:
        """Format single article with full details."""
        return self.formatter.format_article_detail(article, scraped_content)