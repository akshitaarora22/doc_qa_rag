"""
Main RAG system orchestrator that coordinates all components.
"""

from typing import List, Dict, Tuple
from pathlib import Path
import os

from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_interface import LLMInterface


class RAGSystem:
    """
    Complete RAG system for document-grounded question answering.
    
    Architecture:
    1. Document Processing: Extract and chunk documents
    2. Embedding: Create vector embeddings for chunks
    3. Vector Store: Store embeddings in ChromaDB
    4. Retrieval: Find relevant chunks for queries
    5. Generation: Generate grounded answers using LLM
    """
    
    def __init__(self, 
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 top_k: int = 3,
                 max_documents: int = 3):
        """
        Initialize RAG system.
        
        Args:
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks
            top_k: Number of chunks to retrieve per query
            max_documents: Maximum number of documents allowed
        """
        self.max_documents = max_documents
        self.top_k = top_k
        
        # Initialize components
        self.doc_processor = DocumentProcessor(chunk_size, chunk_overlap)
        self.vector_store = VectorStore()
        self.llm = LLMInterface()
        
        # Track loaded documents
        self.loaded_documents = []
        self.total_chunks = 0
    
    def load_documents(self, file_paths: List[str]) -> Dict[str, any]:
        """
        Load and process documents into the system.
        
        Args:
            file_paths: List of paths to document files
            
        Returns:
            Dictionary with processing statistics
        """
        if len(file_paths) > self.max_documents:
            raise ValueError(f"Maximum {self.max_documents} documents allowed")
        
        # Clear existing data
        self.vector_store.clear()
        self.loaded_documents = []
        self.total_chunks = 0
        
        all_chunks = []
        stats = {
            'documents_processed': 0,
            'total_chunks': 0,
            'documents': []
        }
        
        # Process each document
        for file_path in file_paths:
            file_path = str(Path(file_path).resolve())
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Extract and chunk document
            chunks = self.doc_processor.process_document(file_path)
            all_chunks.extend(chunks)
            
            doc_info = {
                'name': Path(file_path).name,
                'path': file_path,
                'chunks': len(chunks)
            }
            self.loaded_documents.append(doc_info)
            stats['documents'].append(doc_info)
            stats['documents_processed'] += 1
            stats['total_chunks'] += len(chunks)
        
        # Create embeddings in batch
        texts = [chunk['text'] for chunk in all_chunks]
        embeddings = self.llm.create_embeddings_batch(texts)
        
        # Store in vector database
        self.vector_store.add_chunks(all_chunks, embeddings)
        self.total_chunks = len(all_chunks)
        
        return stats
    
    def query(self, question: str) -> Dict[str, any]:
        """
        Answer a question using RAG pipeline.
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer and source citations
        """
        if self.total_chunks == 0:
            raise ValueError("No documents loaded. Please load documents first.")
        
        # 1. Embed the query
        query_embedding = self.llm.create_embedding(question)
        
        # 2. Retrieve relevant chunks
        search_results = self.vector_store.search(query_embedding, self.top_k)
        
        # 3. Format retrieved chunks
        retrieved_chunks = []
        for i in range(len(search_results['documents'])):
            retrieved_chunks.append({
                'text': search_results['documents'][i],
                'metadata': search_results['metadatas'][i],
                'distance': search_results['distances'][i]
            })
        
        # 4. Generate answer
        answer = self.llm.generate_answer(question, retrieved_chunks)
        
        # 5. Format response with citations
        return {
            'question': question,
            'answer': answer,
            'sources': self._format_sources(retrieved_chunks)
        }
    
    def _format_sources(self, chunks: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Format source citations from retrieved chunks."""
        sources = []
        for i, chunk in enumerate(chunks, 1):
            sources.append({
                'source_number': i,
                'document_name': chunk['metadata']['document_name'],
                'chunk_id': chunk['metadata']['chunk_id'],
                'similarity_score': 1 - chunk['distance'],  # Convert distance to similarity
                'text_snippet': chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text']
            })
        return sources
    
    def get_system_info(self) -> Dict[str, any]:
        """Get information about loaded documents and system state."""
        return {
            'documents_loaded': len(self.loaded_documents),
            'total_chunks': self.total_chunks,
            'documents': self.loaded_documents,
            'chunk_size': self.doc_processor.chunk_size,
            'chunk_overlap': self.doc_processor.chunk_overlap,
            'top_k': self.top_k
        }
