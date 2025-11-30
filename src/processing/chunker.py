
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

class SemanticChunker:
  """
  Intelligent text chunking with overlap for context preservation.
  Uses recursive splitting to respect natural boundaries.
  """
  
  def __init__(
    self,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    separators: List[str] = None
  ):
    """
    Args:
      chunk_size: Target size of each chunk in characters
      chunk_overlap: Overlap between chunks to preserve context
      separators: Priority list of split points
    """
    self.separators = separators or [
      "\n\n",  # Paragraph breaks
      "\n",    # Line breaks
      ". ",    # Sentences
      "? ",    # Questions
      "! ",    # Exclamations
      "; ",    # Semicolons
      ", ",    # Commas
      " ",     # Words
      ""       # Characters (last resort)
    ]
      
    self.splitter = RecursiveCharacterTextSplitter(
      chunk_size=chunk_size,
      chunk_overlap=chunk_overlap,
      separators=self.separators,
      length_function=len,
      is_separator_regex=False
    )
  
  def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
    """
    Split documents into semantic chunks while preserving metadata.
    
    Args:
      documents: List of dicts with 'content' and 'metadata' keys

    Returns:
      List of chunked documents with inherited metadata
    """
    chunked_docs = []

    for doc in documents:
      chunks = self.splitter.split_text(doc["content"])

      for i, chunk in enumerate(chunks):
        chunked_docs.append({
          "content": chunk,
          "metadata": {
            **doc["metadata"],
            "chunk_index": i,
            "total_chunks": len(chunks)
          }
        })

    print(f"Created {len(chunked_docs)} chunks from {len(documents)} documents")
    return chunked_docs


class SlidingWindowChunker:
  """
  Alternative chunker using sliding window approach.
  Good for maintaining more context at boundaries.
  """
    
  def __init__(self, window_size: int = 500, step_size: int = 250):
    self.window_size = window_size
    self.step_size = step_size
    
  def chunk_text(self, text: str) -> List[str]:
    """Create overlapping chunks using sliding window."""
    chunks = []
    start = 0
        
    while start < len(text):
      end = start + self.window_size
      chunk = text[start:end]
      
      # Try to end at a sentence boundary
      if end < len(text):
        last_period = chunk.rfind('. ')
        if last_period > self.window_size // 2:
          chunk = chunk[:last_period + 1]
      
      chunks.append(chunk.strip())
      start += self.step_size
    
    return chunks