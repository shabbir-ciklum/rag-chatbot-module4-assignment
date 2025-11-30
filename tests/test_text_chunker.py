import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.processing.chunker import SemanticChunker

# Create test document
test_doc = {
  "content": "Artificial intelligence has revolutionized technology. Machine learning enables computers to learn from data. Deep learning uses neural networks for complex tasks. " * 10,
  "metadata": {"source": "test.txt", "type": "text"}
}

# Initialize chunker
chunker = SemanticChunker(chunk_size=500, chunk_overlap=100)

# Chunk the document
chunks = chunker.chunk_documents([test_doc])

# Show results
print(f"\n{'='*60}")
print(f"CHUNKING TEST RESULTS")
print(f"{'='*60}")
print(f"Original length: {len(test_doc['content'])} characters")
print(f"Total chunks: {len(chunks)}")
print(f"\nFirst chunk:")
print(f"Content: {chunks[0]['content'][:200]}...")
print(f"Metadata: {chunks[0]['metadata']}")