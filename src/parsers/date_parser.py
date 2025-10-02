import datetime
import re
from typing import Tuple

class DateParser:
    """Handles date parsing from user queries."""
    
    def __init__(self):
        self.today = datetime.date.today()
    
    def parse_date_query(self, query: str) -> Tuple[datetime.date, datetime.date]:
        """Parse date-related terms from the query and return date range."""
        from_date = None
        to_date = None
        
        # Convert query to lowercase for pattern matching
        query_lower = query.lower()
        
        # Handle specific date patterns
        if 'today' in query_lower:
            from_date = to_date = self.today
        elif 'yesterday' in query_lower:
            from_date = to_date = self.today - datetime.timedelta(days=1)
        elif 'this week' in query_lower:
            days_since_monday = self.today.weekday()
            from_date = self.today - datetime.timedelta(days=days_since_monday)
            to_date = self.today
        elif 'last week' in query_lower:
            days_since_monday = self.today.weekday()
            last_monday = self.today - datetime.timedelta(days=days_since_monday + 7)
            from_date = last_monday
            to_date = last_monday + datetime.timedelta(days=6)
        elif 'this month' in query_lower:
            from_date = self.today.replace(day=1)
            to_date = self.today
        elif 'last month' in query_lower:
            # Get first day of current month, then go back one day to get last month
            first_this_month = self.today.replace(day=1)
            last_day_prev_month = first_this_month - datetime.timedelta(days=1)
            from_date = last_day_prev_month.replace(day=1)
            to_date = last_day_prev_month
        
        # Handle "X days ago" pattern
        days_ago_match = re.search(r'(\d+)\s+days?\s+ago', query_lower)
        if days_ago_match:
            days = int(days_ago_match.group(1))
            from_date = to_date = self.today - datetime.timedelta(days=days)
        
        # Handle specific date formats (YYYY-MM-DD, MM/DD/YYYY, etc.)
        if from_date is None:
            from_date, to_date = self._parse_absolute_dates(query)
        
        # Default to past week if no specific date found
        if from_date is None:
            from_date = self.today - datetime.timedelta(days=7)
            to_date = self.today
        
        return from_date, to_date
    
    def _parse_absolute_dates(self, query: str) -> Tuple[datetime.date, datetime.date]:
        """Parse absolute date formats."""
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY
            r'(\d{1,2}-\d{1,2}-\d{4})',  # MM-DD-YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, query)
            if match:
                date_str = match.group(1)
                try:
                    if '/' in date_str:
                        parsed_date = datetime.datetime.strptime(date_str, '%m/%d/%Y').date()
                    elif '-' in date_str and len(date_str.split('-')[0]) == 4:
                        parsed_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    elif '-' in date_str:
                        parsed_date = datetime.datetime.strptime(date_str, '%m-%d-%Y').date()
                    
                    return parsed_date, parsed_date
                except ValueError:
                    continue
        
        return None, None