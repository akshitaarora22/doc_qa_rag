"""
Document processing module for RAG system.
Handles text extraction, chunking, and metadata management.
"""

import re
from typing import List, Dict, Tuple
from pathlib import Path
import pypdf


class DocumentProcessor:
    """Processes documents for RAG pipeline."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize document processor.
        
        Args:
            chunk_size: Target size for each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from document file.
        
        Args:
            file_path: Path to document file (.txt or .pdf)
            
        Returns:
            Extracted text content
        """
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_path.suffix.lower() == '.pdf':
            return self._extract_pdf_text(file_path)
        
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF file."""
        text = []
        with open(file_path, 'rb') as f:
            pdf_reader = pypdf.PdfReader(f)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)
    
    def chunk_text(self, text: str, doc_name: str) -> List[Dict[str, any]]:
        """
        Split text into overlapping chunks with metadata.
        
        Args:
            text: Input text to chunk
            doc_name: Name of the source document
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        # Clean and normalize text
        text = self._normalize_text(text)
        
        # Split into sentences for better chunk boundaries
        sentences = self._split_into_sentences(text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        chunk_id = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence exceeds chunk_size and we have content
            if current_length + sentence_length > self.chunk_size and current_chunk:
                # Create chunk from current sentences
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        'document_name': doc_name,
                        'chunk_id': chunk_id,
                        'char_count': len(chunk_text)
                    }
                })
                chunk_id += 1
                
                # Start new chunk with overlap
                overlap_text = chunk_text[-self.chunk_overlap:] if len(chunk_text) > self.chunk_overlap else chunk_text
                overlap_sentences = self._split_into_sentences(overlap_text)
                current_chunk = overlap_sentences
                current_length = sum(len(s) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add final chunk if any content remains
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'metadata': {
                    'document_name': doc_name,
                    'chunk_id': chunk_id,
                    'char_count': len(chunk_text)
                }
            })
        
        return chunks
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text by removing extra whitespace."""
        # Replace multiple spaces/newlines with single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using basic sentence boundaries."""
        # Simple sentence splitter (could be enhanced with NLTK/spaCy)
        sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
        sentences = sentence_endings.split(text)
        return [s.strip() for s in sentences if s.strip()]
    
    def process_document(self, file_path: str) -> List[Dict[str, any]]:
        """
        Complete document processing pipeline.
        
        Args:
            file_path: Path to document file
            
        Returns:
            List of chunks with metadata
        """
        doc_name = Path(file_path).name
        text = self.extract_text(file_path)
        chunks = self.chunk_text(text, doc_name)
        return chunks
