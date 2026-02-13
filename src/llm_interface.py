"""
LLM interface module for embeddings and answer generation using OpenAI.
"""

from openai import OpenAI
from typing import List, Dict
import os


class LLMInterface:
    """Handles interactions with OpenAI API for embeddings and completions."""
    
    def __init__(self, api_key: str = None, embedding_model: str = "text-embedding-3-small", 
                 llm_model: str = "gpt-4-turbo-preview"):
        """
        Initialize LLM interface.
        
        Args:
            api_key: OpenAI API key (if None, reads from environment)
            embedding_model: Model to use for embeddings
            llm_model: Model to use for text generation
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.client = OpenAI(api_key=self.api_key)
        self.embedding_model = embedding_model
        self.llm_model = llm_model
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding vector for text.
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector
        """
        response = self.client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return response.data[0].embedding
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts in batch.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        response = self.client.embeddings.create(
            input=texts,
            model=self.embedding_model
        )
        return [item.embedding for item in response.data]
    
    def generate_answer(self, query: str, context_chunks: List[Dict[str, any]], 
                       max_tokens: int = 500) -> str:
        """
        Generate answer based on query and retrieved context.
        
        Args:
            query: User question
            context_chunks: Retrieved document chunks with metadata
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated answer
        """
        # Build context from chunks
        context = self._build_context(context_chunks)
        
        # Create system prompt
        system_prompt = """You are a helpful assistant that answers questions based strictly on the provided context from documents.

Your responsibilities:
1. Answer questions using ONLY information from the provided context
2. If the answer is not in the context, respond with: "I do not know based on the provided documents."
3. Be accurate and concise
4. Do not use external knowledge or make assumptions
5. If you quote or reference specific information, be precise"""

        # Create user prompt with context
        user_prompt = f"""Context from documents:
{context}

Question: {query}

Answer:"""

        # Generate response
        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.0  # Deterministic for factual answers
        )
        
        return response.choices[0].message.content
    
    def _build_context(self, chunks: List[Dict[str, any]]) -> str:
        """Build formatted context string from chunks."""
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk['metadata']
            text = chunk['text']
            context_parts.append(
                f"[Source {i}: {metadata['document_name']}, Chunk {metadata['chunk_id']}]\n{text}"
            )
        return "\n\n".join(context_parts)
