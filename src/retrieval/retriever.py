# src/retrieval/retriever.py

from typing import List, Dict

class RAGRetriever:
    """
    Provider-agnostic RAG retriever.
    Works with Ollama, Groq, or Gemini.
    """
    
    def __init__(self, vector_store, llm_provider):
        """
        Args:
            vector_store: ChromaVectorStore instance
            llm_provider: Any provider with .generate(query, context) method
        """
        self.vector_store = vector_store
        self.llm = llm_provider
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant documents for a query."""
        return self.vector_store.search(query, n_results=top_k)
    
    def format_context(self, documents: List[Dict]) -> str:
        """Format retrieved documents into a context string."""
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            source = doc["metadata"].get("source", "Unknown")
            page = doc["metadata"].get("page", "N/A")
            doc_type = doc["metadata"].get("type", "document")
            
            context_parts.append(
                f"[Source {i}: {source} (Page {page}, Type: {doc_type})]\n{doc['content']}"
            )
        
        return "\n\n---\n\n".join(context_parts)
    
    def query(
        self,
        question: str,
        top_k: int = 5,
        return_sources: bool = True
    ) -> Dict:
        """
        Full RAG pipeline: retrieve + generate.
        """
        # Step 1: Retrieve
        retrieved_docs = self.retrieve(question, top_k=top_k)
        
        if not retrieved_docs:
            return {
                "answer": "I couldn't find any relevant information in the knowledge base.",
                "sources": []
            }
        
        # Step 2: Format context
        context = self.format_context(retrieved_docs)
        
        # Step 3: Generate (works with any provider)
        answer = self.llm.generate(question, context)
        
        result = {"answer": answer}
        
        if return_sources:
            result["sources"] = [
                {
                    "content": doc["content"][:200] + "...",
                    "source": doc["metadata"].get("source"),
                    "page": doc["metadata"].get("page"),
                    "score": doc.get("score", 0)
                }
                for doc in retrieved_docs
            ]
        
        return result