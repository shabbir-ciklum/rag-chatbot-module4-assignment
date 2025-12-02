# src/llm_providers/groq_provider.py

import os
from typing import Optional

class GroqProvider:
    """
    Groq LLM Provider using Groq Cloud API.
    Requires: pip install groq
    """

    def __init__(self, model: str = "llama-3.1-8b-instant", api_key: Optional[str] = None):
      """
      Args:
        model: Groq model name
        api_key: Groq API key (or set GROQ_API_KEY env var)
      """
      try:
        from groq import Groq
      except ImportError:
        raise ImportError(
          "Groq package not installed. Install with: pip install groq"
        )

      self.model = model
      self.api_key = api_key or os.getenv("GROQ_API_KEY")

      if not self.api_key:
        raise ValueError(
          "Groq API key required. Set GROQ_API_KEY environment variable "
          "or pass api_key parameter."
        )

      self.client = Groq(api_key=self.api_key)
      print(f"✓ Groq provider initialized with model: {model}")

    def generate(self, query: str, context: str) -> str:
      """Generate response using Groq API."""
      prompt = f"""You are a helpful AI assistant. Answer the question based on the provided context.

      Context:
      {context}

      Question: {query}

      Answer:"""

      try:
        response = self.client.chat.completions.create(
          model=self.model,
          messages=[{"role": "user", "content": prompt}],
          temperature=0.7,
          max_tokens=1024
        )
        return response.choices[0].message.content
      except Exception as e:
        return f"Error generating response: {str(e)}"