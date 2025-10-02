from typing import List, Dict, Optional
import datetime

class ResponseFormatter:
    """Handles all response formatting for display."""
    
    def format_articles(self, articles: List[Dict], query: str = "") -> str:
        """Format articles for display in a clean, readable way."""
        if not articles:
            return "❌ No articles found for this query. Try a different search term or broader date range."
        
        # Check if articles are older than expected (fallback was used)
        today = datetime.date.today()
        recent_threshold = today - datetime.timedelta(days=2)
        older_articles = any(
            datetime.datetime.fromisoformat(article.get('publishedAt', '').replace('Z', '+00:00')).date() < recent_threshold 
            for article in articles if article.get('publishedAt')
        )
        
        result = "🔍 Here are the latest headlines:\n"
        result += "=" * 50 + "\n\n"
        
        # Add fallback notice if needed
        if older_articles and any(word in query.lower() for word in ['today', 'latest', 'recent', 'current']):
            result += "💡 Note: No very recent articles found. Showing results from the past week/month.\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            description = article.get('description', 'No description available')
            source = article.get('source', {}).get('name', 'Unknown')
            published = article.get('publishedAt', 'Unknown')
            
            # Clean up the published date
            if published != 'Unknown':
                published = published.replace('T', ' at ').replace('Z', ' UTC')
            
            result += f"📰 {i}. {title}\n"
            result += f"   🔗 Source: {source} | 📅 {published}\n"
            result += f"   📋 {description}\n"
            result += "-" * 50 + "\n\n"
        
        result += "💡 Type 'details [number]' to read the full article content.\n"
        result += "   Example: 'details 1' for the first article"
        
        return result
    
    def format_article_detail(self, article: Dict, scraped_content: Optional[str] = None) -> str:
        """Format single article with full details in a readable way."""
        title = article.get('title', 'No title')
        source = article.get('source', {}).get('name', 'Unknown')
        author = article.get('author', 'Unknown')
        published = article.get('publishedAt', 'Unknown')
        
        # Clean up the published date
        if published != 'Unknown':
            published = published.replace('T', ' at ').replace('Z', ' UTC')
        
        url = article.get('url', '')
        description = article.get('description', '')
        
        # Create a clean, readable format
        result = "=" * 60 + "\n"
        result += f"📰 {title}\n"
        result += "=" * 60 + "\n\n"
        
        result += f"🔗 Source: {source}\n"
        if author and author != 'Unknown':
            result += f"✍️  Author: {author}\n"
        result += f"📅 Published: {published}\n"
        result += f"🌐 URL: {url}\n\n"
        
        # Add description if available
        if description:
            result += "📋 Summary:\n"
            result += f"{description}\n\n"
        
        # Handle content - prioritize scraped content
        if scraped_content and scraped_content.strip() and not scraped_content.startswith("Could not extract"):
            result += "📖 Full Article Content:\n"
            result += "-" * 40 + "\n"
            result += scraped_content + "\n"
        else:
            # Use fallback content with better formatting
            result += "📝 Available Article Details:\n"
            result += "-" * 40 + "\n"
            
            if description:
                result += description + "\n\n"
            
            # Add any additional content from the API
            api_content = article.get('content', '')
            if api_content and api_content != description:
                result += api_content + "\n\n"
            
            result += "💡 Note: Full article content extraction was unsuccessful.\n"
            result += "   Please visit the URL above to read the complete article.\n"
        
        result += "\n" + "=" * 60
        return result
    
    def get_fallback_content(self, article: Dict) -> str:
        """Return well-formatted article details when scraping fails."""
        if not article:
            return "❌ No article data available for fallback content."
        
        # Extract available information from the article
        description = article.get('description', '').strip()
        content = article.get('content', '').strip()
        
        fallback_text = ""
        
        if description:
            fallback_text += f"{description}\n\n"
        
        if content and content != description and len(content) > len(description):
            # Sometimes content has more info than description
            fallback_text += f"Additional Details:\n{content}\n\n"
        
        if not fallback_text:
            fallback_text = "📄 Limited article information available from the news source.\n\n"
        
        fallback_text += "⚠️  Note: Unable to extract full article content.\n"
        fallback_text += "   This may be due to website restrictions or paywall.\n"
        fallback_text += "   Visit the URL above to read the complete article."
        
        return fallback_text