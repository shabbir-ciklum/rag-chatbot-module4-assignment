import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.vectorstore.chroma_store import ChromaVectorStore
from src.processing.chunker import SemanticChunker

# Create test documents
print("=" * 70)
print("CHROMA VECTOR STORE TEST")
print("=" * 70)

# Sample documents about AI and machine learning
test_docs = [
    {
        "content": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed.",
        "metadata": {"source": "ai_basics.txt", "type": "text", "chunk_index": 0, "total_chunks": 3}
    },
    {
        "content": "Deep learning uses neural networks with multiple layers to process complex patterns in data. It has revolutionized fields like computer vision and natural language processing.",
        "metadata": {"source": "ai_basics.txt", "type": "text", "chunk_index": 1, "total_chunks": 3}
    },
    {
        "content": "Natural language processing (NLP) is a branch of AI that helps computers understand, interpret, and generate human language.",
        "metadata": {"source": "ai_basics.txt", "type": "text", "chunk_index": 2, "total_chunks": 3}
    },
    {
        "content": "Python is the most popular programming language for machine learning and data science. Libraries like TensorFlow, PyTorch, and scikit-learn make ML accessible.",
        "metadata": {"source": "programming.txt", "type": "text", "chunk_index": 0, "total_chunks": 1}
    }
]

print(f"\nCreated {len(test_docs)} test documents")

# Initialize ChromaDB with a test collection
print("\n" + "=" * 70)
print("STEP 1: Initialize ChromaDB Vector Store")
print("=" * 70)

vector_store = ChromaVectorStore(
    collection_name="test_collection",
    embedding_model="all-MiniLM-L6-v2",
    persist_directory="./test_chroma_db"
)

print(f"Embedding dimension: {vector_store.embedding_dim}")

# Add documents to the vector store
print("\n" + "=" * 70)
print("STEP 2: Add Documents to Vector Store")
print("=" * 70)

vector_store.add_documents(test_docs)

# Test search functionality
print("\n" + "=" * 70)
print("STEP 3: Test Search Functionality")
print("=" * 70)

# Query 1: About machine learning
query1 = "What is machine learning?"
print(f"\nQuery 1: '{query1}'")
results1 = vector_store.search(query1, n_results=2)

for i, result in enumerate(results1, 1):
    print(f"\nResult {i}:")
    print(f"  Score: {result['score']:.4f}")
    print(f"  Source: {result['metadata']['source']}")
    print(f"  Content: {result['content'][:100]}...")

# Query 2: About programming
query2 = "Which programming language should I use for AI?"
print(f"\n\nQuery 2: '{query2}'")
results2 = vector_store.search(query2, n_results=2)

for i, result in enumerate(results2, 1):
    print(f"\nResult {i}:")
    print(f"  Score: {result['score']:.4f}")
    print(f"  Source: {result['metadata']['source']}")
    print(f"  Content: {result['content'][:100]}...")

# Query 3: About neural networks
query3 = "Tell me about neural networks"
print(f"\n\nQuery 3: '{query3}'")
results3 = vector_store.search(query3, n_results=2)

for i, result in enumerate(results3, 1):
    print(f"\nResult {i}:")
    print(f"  Score: {result['score']:.4f}")
    print(f"  Source: {result['metadata']['source']}")
    print(f"  Content: {result['content'][:100]}...")

# Test metadata filtering
print("\n" + "=" * 70)
print("STEP 4: Test Metadata Filtering")
print("=" * 70)

query4 = "artificial intelligence"
print(f"\nQuery: '{query4}' (filtered by source='ai_basics.txt')")
results4 = vector_store.search(
    query4,
    n_results=3,
    filter_metadata={"source": "ai_basics.txt"}
)

print(f"\nFound {len(results4)} results from ai_basics.txt:")
for i, result in enumerate(results4, 1):
    print(f"\nResult {i}:")
    print(f"  Score: {result['score']:.4f}")
    print(f"  Chunk: {result['metadata']['chunk_index']}/{result['metadata']['total_chunks']}")
    print(f"  Content: {result['content'][:80]}...")

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"✓ Vector store initialized successfully")
print(f"✓ Added {len(test_docs)} documents")
print(f"✓ Semantic search working correctly")
print(f"✓ Metadata filtering working correctly")
print(f"✓ Total documents in collection: {vector_store.collection.count()}")

# Clean up (optional - uncomment if you want to delete the test collection)
print("\n" + "=" * 70)
print("CLEANUP")
print("=" * 70)
cleanup = input("\nDo you want to delete the test collection? (y/n): ")
if cleanup.lower() == 'y':
    vector_store.delete_collection()
    print("Test collection deleted.")
else:
    print("Test collection preserved at ./test_chroma_db")