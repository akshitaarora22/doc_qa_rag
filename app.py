"""
Streamlit web interface for RAG system.
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from rag_system import RAGSystem

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []

# Title and description
st.title("📚 RAG Document Question Answering System")
st.markdown("""
Upload up to 3 documents and ask questions that will be answered based strictly on the provided content.
Supports text files (.txt) and PDFs (.pdf).
""")

# Sidebar for document upload
with st.sidebar:
    st.header("📁 Document Upload")
    
    uploaded_files = st.file_uploader(
        "Upload documents (max 3)",
        type=['txt', 'pdf'],
        accept_multiple_files=True,
        help="Upload up to 3 text or PDF documents"
    )
    
    # Configuration options
    st.subheader("⚙️ Configuration")
    chunk_size = st.slider("Chunk Size", 500, 2000, 1000, 100)
    chunk_overlap = st.slider("Chunk Overlap", 50, 500, 200, 50)
    top_k = st.slider("Top K Results", 1, 5, 3, 1)
    
    # Process documents button
    if st.button("🔄 Process Documents", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one document")
        elif len(uploaded_files) > 3:
            st.error("Maximum 3 documents allowed")
        else:
            with st.spinner("Processing documents..."):
                try:
                    # Save uploaded files temporarily
                    temp_dir = Path("temp_uploads")
                    temp_dir.mkdir(exist_ok=True)
                    
                    file_paths = []
                    for uploaded_file in uploaded_files:
                        file_path = temp_dir / uploaded_file.name
                        with open(file_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        file_paths.append(str(file_path))
                    
                    # Initialize and load documents
                    st.session_state.rag_system = RAGSystem(
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap,
                        top_k=top_k
                    )
                    stats = st.session_state.rag_system.load_documents(file_paths)
                    st.session_state.documents_loaded = True
                    st.session_state.qa_history = []
                    
                    st.success(f"✅ Processed {stats['documents_processed']} documents into {stats['total_chunks']} chunks")
                    
                    # Show document details
                    st.subheader("📄 Loaded Documents")
                    for doc in stats['documents']:
                        st.text(f"• {doc['name']}: {doc['chunks']} chunks")
                    
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")
                    st.session_state.documents_loaded = False
    
    # System info
    if st.session_state.documents_loaded and st.session_state.rag_system:
        st.divider()
        info = st.session_state.rag_system.get_system_info()
        st.subheader("📊 System Info")
        st.metric("Documents Loaded", info['documents_loaded'])
        st.metric("Total Chunks", info['total_chunks'])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Ask Questions")
    
    if not st.session_state.documents_loaded:
        st.info("👈 Please upload and process documents first")
    else:
        # Question input
        question = st.text_input(
            "Enter your question:",
            placeholder="What information can you find in the documents?",
            key="question_input"
        )
        
        col_btn1, col_btn2 = st.columns([1, 5])
        with col_btn1:
            ask_button = st.button("🔍 Ask", type="primary")
        
        if ask_button and question:
            with st.spinner("Searching documents and generating answer..."):
                try:
                    result = st.session_state.rag_system.query(question)
                    st.session_state.qa_history.insert(0, result)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Display current answer
        if st.session_state.qa_history:
            latest = st.session_state.qa_history[0]
            
            st.subheader("📝 Answer")
            
            # Check if answer indicates no information found
            if "do not know" in latest['answer'].lower():
                st.warning(latest['answer'])
            else:
                st.write(latest['answer'])
                
                # Show sources
                st.subheader("📚 Sources & Citations")
                for source in latest['sources']:
                    with st.expander(
                        f"Source {source['source_number']}: {source['document_name']} "
                        f"(Chunk {source['chunk_id']}) - "
                        f"Similarity: {source['similarity_score']:.2%}"
                    ):
                        st.text(source['text_snippet'])

with col2:
    st.header("📜 History")
    
    if st.session_state.qa_history:
        for i, qa in enumerate(st.session_state.qa_history):
            with st.expander(f"Q: {qa['question'][:50]}...", expanded=(i == 0)):
                st.markdown(f"**Question:** {qa['question']}")
                st.markdown(f"**Answer:** {qa['answer'][:200]}...")
    else:
        st.info("No questions asked yet")

# Footer
st.divider()
st.caption("RAG System powered by OpenAI embeddings and GPT-4 | ChromaDB vector store")
