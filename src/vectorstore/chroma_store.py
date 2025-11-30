
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import hashlib

class ChromaVectorStore:
    """
    Vector database wrapper using ChromaDB with sentence-transformers.
    Handles embedding generation and similarity search.
    """
    
    def __init__(
        self,
        collection_name: str = "rag_knowledge_base",
        embedding_model: str = "all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db"
    ):
        """
        Args:
            collection_name: Name for the ChromaDB collection
            embedding_model: Sentence-transformer model name
            persist_directory: Where to store the database
        """
        # Initialize embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedder = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedder.get_sentence_embedding_dimension()
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
        
        print(f"ChromaDB initialized. Collection has {self.collection.count()} documents")
    
    def _generate_id(self, content: str, metadata: Dict) -> str:
        """Generate deterministic ID for deduplication."""
        unique_str = f"{content}_{metadata.get('source', '')}_{metadata.get('chunk_index', 0)}"
        return hashlib.md5(unique_str.encode()).hexdigest()
    
    def add_documents(self, documents: List[Dict]) -> None:
        """
        Embed and store documents in ChromaDB.
        
        Args:
            documents: List of dicts with 'content' and 'metadata' keys
        """
        if not documents:
            return
        
        # Extract content for embedding
        contents = [doc["content"] for doc in documents]
        
        # Generate embeddings in batch
        print(f"Generating embeddings for {len(contents)} chunks...")
        embeddings = self.embedder.encode(
            contents,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Prepare for ChromaDB
        ids = [self._generate_id(doc["content"], doc["metadata"]) for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        # Add to collection (ChromaDB handles duplicates by ID)
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=contents,
            metadatas=metadatas
        )
        
        print(f"Added {len(documents)} documents. Total: {self.collection.count()}")
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar documents.
        
        Args:
            query: Search query text
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of matching documents with scores
        """
        # Embed the query
        query_embedding = self.embedder.encode(query).tolist()
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        documents = []
        for i in range(len(results["documents"][0])):
            documents.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": 1 - results["distances"][0][i]  # Convert distance to similarity
            })
        
        return documents
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.client.delete_collection(self.collection.name)
        print(f"Deleted collection: {self.collection.name}")