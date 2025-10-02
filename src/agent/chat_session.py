class ChatSession:
    def __init__(self, max_history=6):
        self.messages = []
        self.max_history = max_history
        self.last_articles = []
    
    def add_message(self, role, content):
        """Add a message to conversation history."""
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_messages(self):
        """Get all messages for LLM context."""
        return self.messages
    
    def store_articles(self, articles):
        """Store fetched articles for reference."""
        self.last_articles = articles
    
    def get_article(self, index):
        """Get article by index."""
        if 0 <= index < len(self.last_articles):
            return self.last_articles[index]
        return None