from typing import Optional, Dict
from config import FIRECRAWL_API_KEY
from clients import ScraperClient
from services import ResponseFormatter

class ScraperService:
    """Service for web scraping operations."""
    
    def __init__(self):
        self.scraper_client = ScraperClient(FIRECRAWL_API_KEY)
        self.formatter = ResponseFormatter()
    
    def scrape_article(self, url: str, fallback_article: Optional[Dict] = None) -> str:
        """Scrape full article content from URL with fallback."""
        # Try to scrape content
        scraped_content = self.scraper_client.scrape_url(url)
        
        if scraped_content:
            return scraped_content
        else:
            # Return fallback content if scraping fails
            print(f"[FALLBACK] Using article details instead of scraped content")
            return self.formatter.get_fallback_content(fallback_article)