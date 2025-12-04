# main.py - Updated with Agent Integration

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

# Import agent components
from src.agent.agent import AIAgent

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
    parser = argparse.ArgumentParser(description="AI-Agentic RAG Chatbot")
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
    parser.add_argument(
        "--agent-mode",
        action="store_true",
        help="Enable full agent capabilities (recommended)"
    )
    parser.add_argument(
        "--self-analyze",
        action="store_true",
        help="Run self-analysis and generate LinkedIn post"
    )
    args = parser.parse_args()
    
    # Create directories
    Path("data/pdfs").mkdir(parents=True, exist_ok=True)
    Path("data/audio").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    print("="*70)
    print(f"🤖 AI-Agentic RAG Chatbot - Using {args.provider.upper()}")
    if args.agent_mode:
        print("✨ Agent Mode: ENABLED")
    print("="*70)
    
    # Initialize vector store
    vector_store = ChromaVectorStore(
        collection_name="genai_databases_kb",
        embedding_model="all-MiniLM-L6-v2"
    )
    
    # Rebuild if requested or if empty
    if args.rebuild or vector_store.collection.count() == 0:
        print("\n[1/4] Loading documents...")
        documents = build_knowledge_base()
        
        if not documents:
            print("\n⚠ No documents found!")
            print("  → Add PDFs to: data/pdfs/")
            print("  → Add audio to: data/audio/")
            return
        
        print("\n[2/4] Chunking documents...")
        chunker = SemanticChunker(chunk_size=500, chunk_overlap=100)
        chunks = chunker.chunk_documents(documents)
        
        print("\n[3/4] Building vector database...")
        vector_store.add_documents(chunks)
    else:
        print(f"\n✓ Using existing database with {vector_store.collection.count()} chunks")
    
    # Initialize LLM provider
    print(f"\n[4/4] Initializing {args.provider} provider...")
    llm = get_llm_provider(args.provider, args.model)
    
    # Create retriever
    retriever = RAGRetriever(vector_store=vector_store, llm_provider=llm)
    
    # Create agent if enabled
    agent = None
    if args.agent_mode or args.self_analyze:
        print("\n🚀 Initializing AI Agent...")
        agent = AIAgent(
            rag_retriever=retriever,
            llm_provider=llm,
            project_root="."
        )
        print("   ✓ Agent tools loaded")
        print("   ✓ Reasoner initialized")
        print("   ✓ Evaluator initialized")
    
    # Create chatbot
    chatbot = RAGChatbot(retriever, log_file="logs/agent_results.log", agent=agent)
    
    # Handle self-analysis mode
    if args.self_analyze:
        print("\n" + "="*70)
        print("🔍 Self-Analysis Mode")
        print("="*70)
        
        analysis = agent.analyze_self()
        
        # Display results
        print("\n📊 Project Statistics:")
        stats = analysis["stats"]
        print(f"   Total Files: {stats['total_files']}")
        print(f"   Python Files: {stats['python_files']}")
        print(f"   Total Lines: {stats['total_lines']:,}")
        print(f"   Test Files: {stats['test_files']}")
        
        print("\n🏗️  Architecture Analysis:")
        arch = analysis["architecture"]
        print(f"   Type: {arch['architecture_type']}")
        print(f"   Layers: {len(arch['layers'])}")
        for layer, info in arch["layers"].items():
            print(f"      • {layer}: {info['purpose']}")
        
        print("\n💻 Code Analysis:")
        code = analysis["code_analysis"]
        print(f"   Total Classes: {code['total_classes']}")
        print(f"   Total Functions: {code['total_functions']}")
        print(f"   Files Analyzed: {len(code['files_analyzed'])}")
        
        print("\n✍️  Generated LinkedIn Post:")
        print("="*70)
        print(analysis["linkedin_post"])
        print("="*70)
        
        # Save post to file
        post_file = "linkedin_post.txt"
        with open(post_file, 'w') as f:
            f.write(analysis["linkedin_post"])
        print(f"\n💾 LinkedIn post saved to: {post_file}")
        
        # Save full analysis
        import json
        analysis_file = "reports/self_analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"💾 Full analysis saved to: {analysis_file}")
        
        return
    
    # Run test questions
    print("\n" + "="*70)
    print("Running Test Questions")
    print("="*70)
    
    test_questions = [
        "What are top threats in Agentic AI based solutions to look out for?",
        "Summarise the top controls outlined in CIS benchmark guide v8.1.2?",
        "What is new with Q business from latest AWS Summit London 2025 ?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'─'*50}")
        print(f"Question {i}: {question}")
        print('─'*50)
        
        # Use agent mode if enabled
        result = chatbot.get_full_response(question, use_agent=args.agent_mode)
        print(f"\nAnswer:\n{result['answer']}")
        
        if result.get("sources"):
            print("\nSources:")
            for source in result["sources"][:3]:
                # Handle both agent format (with metadata) and regular RAG format
                if "metadata" in source:
                    # Agent format: extract from metadata
                    source_name = source["metadata"].get("source", "Unknown")
                    page = source["metadata"].get("page", "N/A")
                else:
                    # Regular RAG format: already at top level
                    source_name = source.get("source", "Unknown")
                    page = source.get("page", "N/A")

                score = source.get("score", 0)
                print(f"  • {source_name} (Page {page}, Score: {score:.3f})")
        
        if args.agent_mode and result.get("evaluation"):
            eval_data = result["evaluation"]
            print(f"\n📊 Evaluation: Overall Score = {eval_data['overall_score']:.2f}")
    
    # Interactive mode
    print("\n" + "="*70)
    chatbot.interactive_mode()
    
    # Final performance report if agent was used
    if agent:
        print("\n" + "="*70)
        print("📈 Final Performance Report")
        print("="*70)
        
        report = agent.get_performance_report()
        summary = report["evaluator_summary"]
        
        print(f"\nTotal Interactions: {report['total_interactions']}")
        print(f"Total Evaluations: {summary['total_evaluations']}")
        
        if summary.get("average_scores"):
            print("\nAverage Performance Scores:")
            for metric, score in summary["average_scores"].items():
                print(f"   {metric}: {score:.2f}")
        
        # Export reports
        print("\n💾 Exporting detailed reports...")
        files = agent.export_full_report()
        for file in files:
            print(f"   ✓ {file}")

if __name__ == "__main__":
    main()