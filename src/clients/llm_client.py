from cerebras.cloud.sdk import Cerebras
from typing import List, Dict

class LLMClient:
    """Simple wrapper for Cerebras LLM API."""
    
    def __init__(self, api_key: str):
        self.client = Cerebras(api_key=api_key)
    
    def get_response(self, messages: List[Dict], system_prompt: str) -> str:
        """Get response from LLM."""
        try:
            full_messages = [{"role": "system", "content": system_prompt}] + messages
            
            response = self.client.chat.completions.create(
                messages=full_messages,
                model="llama-4-maverick-17b-128e-instruct",
                temperature=0.2,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}"