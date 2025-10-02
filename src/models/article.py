from dataclasses import dataclass
from typing import Optional

@dataclass
class Article:
    """Simple article data structure."""
    title: str
    description: str
    url: str
    source: str
    author: Optional[str]
    published_at: str
    content: Optional[str] = None
    
    @classmethod
    def from_newsapi_response(cls, article_data: dict) -> 'Article':
        """Create Article from NewsAPI response data."""
        return cls(
            title=article_data.get('title', 'No title'),
            description=article_data.get('description', 'No description'),
            url=article_data.get('url', ''),
            source=article_data.get('source', {}).get('name', 'Unknown'),
            author=article_data.get('author'),
            published_at=article_data.get('publishedAt', 'Unknown'),
            content=article_data.get('content')
        )