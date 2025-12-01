# test_rag.py

import logging
from datetime import datetime

def run_tests():
    """Run comprehensive tests and generate log output."""
    
    # Setup test logging
    log_file = f"logs/test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s | %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.info("="*60)
    logger.info("RAG CHATBOT TEST RESULTS")
    logger.info("="*60)
    
    # Initialize components (simplified for testing)
    from main import build_knowledge_base
    from src.processing.chunker import SemanticChunker
    from src.vectorstore.chroma_store import ChromaVectorStore
    from src.retrieval.retriever import RAGRetriever
    
    # Build pipeline
    documents = build_knowledge_base()
    chunker = SemanticChunker()
    chunks = chunker.chunk_documents(documents)
    
    vector_store = ChromaVectorStore()
    vector_store.add_documents(chunks)
    
    retriever = RAGRetriever(vector_store=vector_store)
    
    # Test questions
    test_cases = [
        {
            "question": "What are the production 'Do's' for RAG?",
            "expected_topics": ["production", "RAG", "best practices"]
        },
        {
            "question": "What is the difference between standard retrieval and the ColPali approach?",
            "expected_topics": ["ColPali", "retrieval", "vision"]
        },
        {
            "question": "Why is hybrid search better than vector-only search?",
            "expected_topics": ["hybrid", "BM25", "vector", "keyword"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        logger.info(f"\n{'='*40}")
        logger.info(f"TEST {i}")
        logger.info(f"{'='*40}")
        logger.info(f"QUESTION: {test['question']}")
        
        result = retriever.query(test["question"])
        
        logger.info(f"\nANSWER:\n{result['answer']}")
        logger.info(f"\nSOURCES RETRIEVED: {len(result.get('sources', []))}")
        
        for j, source in enumerate(result.get("sources", [])[:3], 1):
            logger.info(f"  Source {j}: {source['source']} (Score: {source['score']:.3f})")
    
    logger.info("\n" + "="*60)
    logger.info("TESTS COMPLETED")
    logger.info("="*60)
    
    print(f"Test results saved to: {log_file}")
    return log_file

if __name__ == "__main__":
    run_tests()