# main.py

import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

from src.data_loaders.pdf_loader import PDFLoader
from src.data_loaders.audio_loader import AudioLoader
from src.processing.chunker import SemanticChunker
from src.vectorstore.chroma_store import ChromaVectorStore
from src.retrieval.retriever import RAGRetriever
from src.chatbot import RAGChatbot
from src.llm_providers import get_llm_provider

load_dotenv()

def build_knowledge_base():
    """Load and process all data sources."""
    all_documents = []
    
    # Load PDFs
    pdf_dir = Path("data/pdfs")
    if pdf_dir.exists():
        for pdf_file in pdf_dir.glob("*.pdf"):
            print(f"\nProcessing PDF: {pdf_file.name}")
            loader = PDFLoader(str(pdf_file))
            docs = loader.load()
            all_documents.extend(docs)
    
    # Transcribe audio
    audio_dir = Path("data/audio")
    if audio_dir.exists() and list(audio_dir.glob("*")):
        audio_loader = AudioLoader(model_size="base")
        audio_docs = audio_loader.load_directory(str(audio_dir))
        all_documents.extend(audio_docs)
    
    print(f"\nTotal documents loaded: {len(all_documents)}")
    return all_documents

def main():
    parser = argparse.ArgumentParser(description="RAG Chatbot")
    parser.add_argument(
        "--provider", 
        choices=["ollama", "groq", "gemini"],
        default="ollama",
        help="LLM provider to use (default: ollama)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model name (provider-specific)"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild the vector database"
    )
    args = parser.parse_args()
    
    # Create directories
    Path("data/pdfs").mkdir(parents=True, exist_ok=True)
    Path("data/audio").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    print("="*60)
    print(f"RAG Chatbot - Using {args.provider.upper()}")
    print("="*60)
    
    # Initialize vector store
    vector_store = ChromaVectorStore(
        collection_name="genai_databases_kb",
        embedding_model="all-MiniLM-L6-v2"
    )
    
    # Rebuild if requested or if empty
    if args.rebuild or vector_store.collection.count() == 0:
        print("\n[1/3] Loading documents...")
        documents = build_knowledge_base()
        
        if not documents:
            print("\n⚠ No documents found!")
            print("  → Add PDFs to: data/pdfs/")
            print("  → Add audio to: data/audio/")
            return
        
        print("\n[2/3] Chunking documents...")
        chunker = SemanticChunker(chunk_size=500, chunk_overlap=100)
        chunks = chunker.chunk_documents(documents)
        
        print("\n[3/3] Building vector database...")
        vector_store.add_documents(chunks)
    else:
        print(f"\n✓ Using existing database with {vector_store.collection.count()} chunks")
    
    # Initialize LLM provider
    print(f"\nInitializing {args.provider} provider...")
    llm = get_llm_provider(args.provider, args.model)
    
    # Create retriever and chatbot
    retriever = RAGRetriever(vector_store=vector_store, llm_provider=llm)
    chatbot = RAGChatbot(retriever, log_file="logs/test_results.log")
    
    # Run test questions
    print("\n" + "="*60)
    print("Running Test Questions")
    print("="*60)
    
    test_questions = [
        "What are top threats in Agentic AI based solutions to look out for?",
        "Summarise the top controls outlined in CIS benchmark guide v8.1.2?",
        "What is new with Q business from latest AWS Summit London 2025 ?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'─'*50}")
        print(f"Question {i}: {question}")
        print('─'*50)
        
        result = chatbot.get_full_response(question)
        print(f"\nAnswer:\n{result['answer']}")
        
        if result.get("sources"):
            print("\nSources:")
            for source in result["sources"][:3]:
                print(f"  • {source['source']} (Page {source['page']}, Score: {source['score']:.3f})")
    
    # Interactive mode
    print("\n" + "="*60)
    chatbot.interactive_mode()

if __name__ == "__main__":
    main()