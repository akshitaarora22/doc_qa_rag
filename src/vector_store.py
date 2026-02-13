"""
Vector store module using ChromaDB for semantic search.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict
import uuid


class VectorStore:
    """Manages vector embeddings and similarity search using ChromaDB."""
    
    def __init__(self, collection_name: str = "rag_documents", persist_directory: str = "./chroma_db"):
        """
        Initialize vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the database
        """
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
    
    def add_chunks(self, chunks: List[Dict[str, any]], embeddings: List[List[float]]):
        """
        Add document chunks with embeddings to the vector store.
        
        Args:
            chunks: List of chunk dictionaries with text and metadata
            embeddings: Corresponding embedding vectors
        """
        ids = [str(uuid.uuid4()) for _ in chunks]
        texts = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
    
    def search(self, query_embedding: List[float], top_k: int = 3) -> Dict[str, any]:
        """
        Search for similar chunks using query embedding.
        
        Args:
            query_embedding: Query vector embedding
            top_k: Number of top results to return
            
        Returns:
            Dictionary with retrieved documents, metadata, and distances
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }
    
    def clear(self):
        """Clear all documents from the collection."""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def count(self) -> int:
        """Get total number of chunks in the store."""
        return self.collection.count()
