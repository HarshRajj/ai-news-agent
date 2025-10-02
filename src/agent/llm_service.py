from typing import List, Dict
from config import CEREBRAS_API_KEY, SYSTEM_PROMPT
from clients import LLMClient

class LLMService:
    """Service for LLM interactions."""
    
    def __init__(self):
        self.llm_client = LLMClient(CEREBRAS_API_KEY)
    
    def get_response(self, messages: List[Dict]) -> str:
        """Get response from LLM."""
        return self.llm_client.get_response(messages, SYSTEM_PROMPT)