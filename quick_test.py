#!/usr/bin/env python3
"""
Quick test script for the RAG pipeline.
Tests all components without requiring external LLM.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loaders.pdf_loader import PDFLoader
from src.data_loaders.audio_loader import AudioLoader
from src.processing.chunker import SemanticChunker
from src.vectorstore.chroma_store import ChromaVectorStore

def test_component(name, test_func):
    """Helper to test a component."""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print('='*70)
    try:
        test_func()
        print(f"✓ {name} - PASSED")
        return True
    except Exception as e:
        print(f"✗ {name} - FAILED: {e}")
        return False

def test_pdf_loader():
    """Test PDF loading."""
    pdf_dir = Path("data/pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print("⚠ No PDFs found in data/pdfs/")
        return

    pdf_file = pdf_files[0]
    print(f"Loading: {pdf_file.name}")

    loader = PDFLoader(str(pdf_file))
    docs = loader.load()

    print(f"✓ Loaded {len(docs)} pages")
    print(f"✓ First page preview: {docs[0]['content'][:100]}...")

def test_audio_loader():
    """Test audio transcription."""
    audio_dir = Path("data/audio")
    audio_files = [f for f in audio_dir.glob("*") if f.suffix.lower() in {'.mp3', '.mp4', '.wav', '.m4a'}]

    if not audio_files:
        print("⚠ No audio files found in data/audio/")
        return

    audio_file = audio_files[0]
    print(f"Transcribing: {audio_file.name} (using tiny model for speed)")

    loader = AudioLoader(model_size="tiny")
    doc = loader.transcribe_file(str(audio_file))

    print(f"✓ Transcribed {len(doc['content'])} characters")
    print(f"✓ Preview: {doc['content'][:100]}...")

def test_chunker():
    """Test document chunking."""
    test_doc = {
        "content": "Machine learning is a subset of AI. " * 20,
        "metadata": {"source": "test.txt", "type": "text"}
    }

    chunker = SemanticChunker(chunk_size=100, chunk_overlap=20)
    chunks = chunker.chunk_documents([test_doc])

    print(f"✓ Created {len(chunks)} chunks from 1 document")
    print(f"✓ First chunk: {chunks[0]['content'][:80]}...")

def test_vector_store():
    """Test vector storage and search."""
    # Create test documents
    test_docs = [
        {
            "content": "Machine learning is a subset of artificial intelligence.",
            "metadata": {"source": "ml.txt", "type": "text"}
        },
        {
            "content": "Python is the most popular programming language for AI.",
            "metadata": {"source": "python.txt", "type": "text"}
        }
    ]

    # Initialize vector store with test collection
    store = ChromaVectorStore(
        collection_name="quick_test",
        persist_directory="./quick_test_db"
    )

    # Add documents
    store.add_documents(test_docs)

    # Search
    results = store.search("What is machine learning?", n_results=1)

    print(f"✓ Added {len(test_docs)} documents")
    print(f"✓ Search returned {len(results)} results")
    print(f"✓ Top result score: {results[0]['score']:.3f}")
    print(f"✓ Top result: {results[0]['content'][:80]}...")

    # Cleanup
    store.delete_collection()
    print("✓ Cleaned up test database")

def test_full_pipeline():
    """Test the complete pipeline."""
    print("\nTesting complete pipeline with actual data...")

    # 1. Load documents
    all_docs = []

    pdf_dir = Path("data/pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if pdf_files:
        print(f"\nLoading {len(pdf_files)} PDF(s)...")
        for pdf_file in pdf_files[:1]:  # Just first PDF for speed
            loader = PDFLoader(str(pdf_file))
            docs = loader.load()
            all_docs.extend(docs[:5])  # Just first 5 pages
            print(f"  ✓ {pdf_file.name}: {len(docs[:5])} pages")

    if not all_docs:
        print("⚠ No documents loaded - skipping full pipeline test")
        return

    # 2. Chunk documents
    print("\nChunking documents...")
    chunker = SemanticChunker(chunk_size=500, chunk_overlap=100)
    chunks = chunker.chunk_documents(all_docs)

    # 3. Store in vector database
    print("\nStoring in vector database...")
    store = ChromaVectorStore(
        collection_name="pipeline_test",
        persist_directory="./pipeline_test_db"
    )
    store.add_documents(chunks)

    # 4. Test search
    print("\nTesting search...")
    queries = [
        "What is RAG?",
        "How does retrieval work?",
        "What are the key concepts?"
    ]

    for query in queries:
        results = store.search(query, n_results=2)
        print(f"\nQuery: '{query}'")
        print(f"  Top result score: {results[0]['score']:.3f}")
        print(f"  Content: {results[0]['content'][:100]}...")

    # Cleanup
    cleanup = input("\nDelete test database? (y/n): ")
    if cleanup.lower() == 'y':
        store.delete_collection()
        print("✓ Test database deleted")

def main():
    """Run all tests."""
    print("="*70)
    print("RAG PIPELINE QUICK TEST")
    print("="*70)

    results = []

    # Test each component
    results.append(test_component("PDF Loader", test_pdf_loader))
    results.append(test_component("Audio Loader", test_audio_loader))
    results.append(test_component("Text Chunker", test_chunker))
    results.append(test_component("Vector Store", test_vector_store))

    # Test full pipeline
    print("\n" + "="*70)
    print("Testing Full Pipeline")
    print("="*70)
    try:
        test_full_pipeline()
        results.append(True)
    except Exception as e:
        print(f"✗ Full Pipeline - FAILED: {e}")
        results.append(False)

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n✓ All tests passed! Your RAG pipeline is ready.")
        print("\nNext steps:")
        print("  1. Install Ollama: brew install ollama")
        print("  2. Start Ollama: ollama serve")
        print("  3. Pull a model: ollama pull llama2")
        print("  4. Run full pipeline: python main.py")
    else:
        print(f"\n✗ Some tests failed. Please review the errors above.")

if __name__ == "__main__":
    main()