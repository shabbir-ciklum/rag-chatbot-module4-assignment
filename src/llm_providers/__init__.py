# src/llm_providers/__init__.py

from typing import Literal

def get_llm_provider(
    provider: Literal["ollama", "groq", "gemini"] = "ollama",
    model: str = None
):
    """
    Factory function to get the appropriate LLM provider.
    
    Args:
        provider: Which provider to use
        model: Optional model override
    
    Returns:
        LLM provider instance
    """
    
    if provider == "ollama":
        from .ollama_provider import OllamaProvider
        return OllamaProvider(model=model or "llama3.2:3b")
    
    elif provider == "groq":
        from .groq_provider import GroqProvider
        return GroqProvider(model=model or "llama-3.1-8b-instant")
    
    elif provider == "gemini":
        from .gemini_provider import GeminiProvider
        return GeminiProvider(model=model or "gemini-1.5-flash")
    
    else:
        raise ValueError(f"Unknown provider: {provider}")