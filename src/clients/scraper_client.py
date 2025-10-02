from firecrawl import FirecrawlApp
from typing import Optional, Dict

class ScraperClient:
    """Simple wrapper for Firecrawl API."""
    
    def __init__(self, api_key: str):
        self.client = FirecrawlApp(api_key=api_key)
    
    def scrape_url(self, url: str) -> Optional[str]:
        """Scrape content from URL and return cleaned text."""
        try:
            print(f"[Scraping] Fetching content from: {url}")
            
            result = self.client.scrape(
                url, 
                formats=[{
                    "type": "markdown",
                    "prompt": "Extract the main article content, excluding navigation, ads, and footers."
                }],
                only_main_content=True,
                timeout=120000
            )
            
            if result and 'markdown' in result:
                content = result['markdown']
                return self._clean_content(content)
            return None
            
        except Exception as e:
            print(f"[ERROR] Scraping Error: {e}")
            return None
    
    def _clean_content(self, content: str) -> str:
        """Clean and process scraped content."""
        lines = content.split('\n')
        cleaned_lines = []
        article_started = False
        
        # Patterns to skip (only at start, before article begins)
        skip_at_start = ['Skip to content', 'Home', 'News', 'Sport', 'Business', 
                         'Watch Live', 'Newsletters', 'Innovation', 'Culture']
        
        # Patterns to stop at (footer content)
        stop_patterns = ['Related Links', 'More on this story', 'Share', 'Save',
                        'You can follow', 'BBC', 'Facebook', 'Twitter', 'Instagram']
        
        for line in lines:
            stripped = line.strip()
            
            # Once we hit a heading with # or substantial text, article has started
            if not article_started:
                if stripped.startswith('#') or len(stripped) > 50:
                    article_started = True
            
            # If article hasn't started, skip navigation
            if not article_started and any(pattern in stripped for pattern in skip_at_start):
                continue
            
            # Stop if we hit footer/related content
            if article_started and any(pattern in stripped for pattern in stop_patterns):
                break
            
            # Skip image markdown and links
            if stripped.startswith('![') or stripped.startswith('[**') or stripped == '* * *':
                continue
            
            # Keep the line if it has content
            if stripped:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines).strip()
        
        # Limit content to avoid token overflow
        if len(content) > 2500:
            content = content[:2500] + "...\n\n[Content truncated for brevity]"
        
        return content if content else None