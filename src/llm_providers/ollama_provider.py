# src/llm_providers/ollama_provider.py

import ollama
from typing import List, Dict

class OllamaProvider:
    """
    Fully local LLM using Ollama.
    No API keys, no costs, runs on your machine.
    
    Setup:
        1. Install Ollama: https://ollama.ai
        2. Pull a model: ollama pull llama3.1:8b
        3. Or smaller: ollama pull phi3:mini
    """
    
    # Recommended free models (smallest to largest)
    RECOMMENDED_MODELS = {
        "phi3:mini": "2.7GB - Fast, good for basic Q&A",
        "llama3.2:3b": "2GB - Good balance of speed/quality",
        "llama3.1:8b": "4.7GB - Better quality, slower",
        "mistral:7b": "4.1GB - Great for instruction following",
        "gemma2:9b": "5.4GB - Google's open model, high quality"
    }
    
    def __init__(self, model: str = "llama3.2:3b"):
        """
        Args:
            model: Ollama model name. Run 'ollama list' to see installed models.
        """
        self.model = model
        self._ensure_model_available()
        
        self.system_prompt = """You are a helpful assistant that answers questions based on the provided context.

INSTRUCTIONS:
1. Answer the question using ONLY the information from the provided context
2. If the context doesn't contain enough information, say so clearly
3. Be concise but thorough
4. Do not make up information that isn't in the context"""
    
    def _ensure_model_available(self):
        """Check if model is available, provide helpful message if not."""
        try:
            ollama.show(self.model)
            print(f"✓ Using Ollama model: {self.model}")
        except Exception:
            print(f"Model '{self.model}' not found. Installing...")
            print(f"Run: ollama pull {self.model}")
            raise RuntimeError(f"Please install the model first: ollama pull {self.model}")
    
    def generate(
        self, 
        query: str, 
        context: str,
        temperature: float = 0.7
    ) -> str:
        """Generate response using Ollama."""
        
        prompt = f"""CONTEXT:
{context}

QUESTION: {query}

Please answer the question based on the context provided above."""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": temperature,
                "num_predict": 1000  # max tokens
            }
        )
        
        return response["message"]["content"]
    
    def stream_generate(self, query: str, context: str):
        """Stream response for better UX."""
        prompt = f"""CONTEXT:
{context}

QUESTION: {query}

Please answer based on the context above."""
        
        stream = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        for chunk in stream:
            yield chunk["message"]["content"]