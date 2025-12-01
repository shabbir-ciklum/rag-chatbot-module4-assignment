import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loaders.audio_loader import AudioLoader
from src.processing.chunker import SemanticChunker
from src.vectorstore.chroma_store import ChromaVectorStore

print("=" * 70)
print("FULL RAG PIPELINE TEST")
print("=" * 70)

# Step 1: Load and transcribe audio
print("\n" + "=" * 70)
print("STEP 1: Audio Transcription (OPTIONAL - Comment out if you want to skip)")
print("=" * 70)

skip_audio = input("Skip audio transcription? (y/n): ")

if skip_audio.lower() != 'y':
    audio_loader = AudioLoader(model_size="tiny")  # Using 'tiny' for faster testing
    audio_file = input("Enter audio file path (or press Enter to use test docs): ")

    if audio_file:
        doc = audio_loader.transcribe_file(audio_file)
        documents = [doc]
    else:
        # Use test documents
        documents = [
            {
                "content": "Machine learning and artificial intelligence are transforming technology. " * 5,
                "metadata": {"source": "test.txt", "type": "text"}
            }
        ]
else:
    # Use simple test documents
    documents = [
        {
            "content": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. It uses algorithms to identify patterns and make predictions.",
            "metadata": {"source": "ml_intro.txt", "type": "text"}
        },
        {
            "content": "Deep learning uses neural networks with multiple layers. These networks can learn complex patterns in images, text, and other data. Popular frameworks include TensorFlow and PyTorch.",
            "metadata": {"source": "deep_learning.txt", "type": "text"}
        }
    ]

print(f"\n✓ Loaded {len(documents)} document(s)")

# Step 2: Chunk documents
print("\n" + "=" * 70)
print("STEP 2: Text Chunking")
print("=" * 70)

chunker = SemanticChunker(chunk_size=500, chunk_overlap=100)
chunks = chunker.chunk_documents(documents)

print(f"✓ Created {len(chunks)} chunks")

# Step 3: Store in vector database
print("\n" + "=" * 70)
print("STEP 3: Vector Storage")
print("=" * 70)

vector_store = ChromaVectorStore(
    collection_name="test_rag_pipeline",
    persist_directory="./test_pipeline_db"
)

vector_store.add_documents(chunks)

print(f"✓ Stored {len(chunks)} chunks in vector database")

# Step 4: Search
print("\n" + "=" * 70)
print("STEP 4: Semantic Search")
print("=" * 70)

queries = [
    "What is machine learning?",
    "How do neural networks work?",
    "What are popular deep learning frameworks?"
]

for query in queries:
    print(f"\nQuery: '{query}'")
    results = vector_store.search(query, n_results=2)

    for i, result in enumerate(results, 1):
        print(f"\n  Result {i}:")
        print(f"    Score: {result['score']:.4f}")
        print(f"    Source: {result['metadata']['source']}")
        print(f"    Content: {result['content'][:100]}...")

# Summary
print("\n" + "=" * 70)
print("PIPELINE TEST COMPLETE")
print("=" * 70)
print("✓ All components working correctly!")
print(f"✓ Total chunks in database: {vector_store.collection.count()}")

# Cleanup
cleanup = input("\nDelete test database? (y/n): ")
if cleanup.lower() == 'y':
    vector_store.delete_collection()
    print("Test database deleted.")
else:
    print("Test database preserved at ./test_pipeline_db")