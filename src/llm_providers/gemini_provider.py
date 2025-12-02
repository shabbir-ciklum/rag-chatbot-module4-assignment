# src/llm_providers/gemini_provider.py

import os
from typing import Optional

class GeminiProvider:
  """
  Google Gemini LLM Provider.
  Requires: pip install google-generativeai
  """

  def __init__(self, model: str = "gemini-1.5-flash", api_key: Optional[str] = None):
    """
    Args:
      model: Gemini model name
      api_key: Google API key (or set GEMINI_API_KEY env var)
    """
    try:
        import google.generativeai as genai
    except ImportError:
      raise ImportError(
        "Google Generative AI package not installed. "
        "Install with: pip install google-generativeai"
      )

    self.model_name = model
    self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    if not self.api_key:
      raise ValueError(
        "Gemini API key required. Set GEMINI_API_KEY environment variable "
        "or pass api_key parameter."
      )

    genai.configure(api_key=self.api_key)
    self.model = genai.GenerativeModel(model)
    print(f"✓ Gemini provider initialized with model: {model}")

  def generate(self, query: str, context: str) -> str:
    """Generate response using Gemini API."""
    prompt = f"""You are a helpful AI assistant. Answer the question based on the provided context.

    Context:
    {context}

    Question: {query}

    Answer:"""

    try:
      response = self.model.generate_content(prompt)
      return response.text
    except Exception as e:
      return f"Error generating response: {str(e)}"