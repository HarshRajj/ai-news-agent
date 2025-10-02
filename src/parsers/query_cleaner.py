import re

class QueryCleaner:
    """Handles query cleaning and processing."""
    
    def clean_query_from_dates(self, query: str) -> str:
        """Remove date-related terms from query for cleaner search."""
        # Remove common date patterns
        date_patterns = [
            r'\b(?:today|yesterday|this week|last week|this month|last month)\b',
            r'\b\d+\s+days?\s+ago\b',
            r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
            r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # MM-DD-YYYY
            r'\b(?:on|from|in|during)\s+',  # Prepositions
            r'\b(?:news|articles?)\s+(?:from|on|in)\b',
        ]
        
        clean_query = query
        for pattern in date_patterns:
            clean_query = re.sub(pattern, '', clean_query, flags=re.IGNORECASE)
        
        # Clean up extra spaces and common words
        clean_query = re.sub(r'\s+', ' ', clean_query).strip()
        clean_query = re.sub(r'^(?:what|show|get|find|search)\s+', '', clean_query, flags=re.IGNORECASE)
        
        return clean_query if clean_query else "general news"