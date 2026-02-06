# RAG Document Question Answering System

A production-quality Retrieval Augmented Generation (RAG) system that enables users to upload documents and ask questions answered strictly based on the provided content.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Example Run](#example-run)
- [Design Choices](#design-choices)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

## ✨ Features

- **Document Processing**: Upload up to 3 documents (TXT or PDF)
- **Intelligent Chunking**: Text segmentation with configurable overlap
- **Vector Embeddings**: OpenAI embeddings for semantic search
- **Vector Database**: ChromaDB for efficient similarity search
- **Grounded Answers**: Responses strictly based on document content
- **Source Citations**: Full traceability with document name and chunk ID
- **Multiple Interfaces**: Streamlit web UI and CLI

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                       RAG System                             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Document   │  │    Vector    │  │     LLM      │     │
│  │  Processor   │→ │    Store     │→ │  Interface   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                 ↓                  ↓              │
│    Text/PDF          ChromaDB            OpenAI            │
│    Chunking          Embeddings           GPT-4            │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Document Upload**: User uploads text or PDF files (max 3, ~20 pages each)
2. **Text Extraction**: Extract text content from documents
3. **Chunking**: Split text into overlapping chunks (default: 1000 chars, 200 overlap)
4. **Embedding**: Generate vector embeddings using OpenAI's `text-embedding-3-small`
5. **Storage**: Store embeddings in ChromaDB with metadata (doc name, chunk ID)
6. **Query**: User asks a question
7. **Retrieval**: Embed query and find top-K similar chunks using cosine similarity
8. **Generation**: GPT-4 generates answer grounded in retrieved context
9. **Response**: Display answer with source citations

### Key Components

#### 1. Document Processor (`src/document_processor.py`)
- Extracts text from TXT and PDF files
- Implements sentence-aware chunking with overlap
- Maintains metadata (document name, chunk ID)

#### 2. Vector Store (`src/vector_store.py`)
- Manages ChromaDB collection
- Stores embeddings with metadata
- Performs similarity search using cosine distance

#### 3. LLM Interface (`src/llm_interface.py`)
- Handles OpenAI API interactions
- Creates embeddings (batch and single)
- Generates grounded answers with system prompts

#### 4. RAG System (`src/rag_system.py`)
- Orchestrates all components
- Manages document loading pipeline
- Handles query processing and response formatting

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone or download the repository**
```bash
cd rag_system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Your `.env` file should contain:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 📖 Usage

### Streamlit Web UI (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Steps:**
1. Upload documents using the sidebar (max 3)
2. Configure chunking parameters if desired
3. Click "Process Documents"
4. Enter questions in the main area
5. View answers with source citations

### Command Line Interface

```bash
python cli.py examples/doc1_climate_change.txt examples/doc2_artificial_intelligence.txt
```

**Options:**
- `--chunk-size`: Chunk size in characters (default: 1000)
- `--chunk-overlap`: Overlap in characters (default: 200)
- `--top-k`: Number of chunks to retrieve (default: 3)

**Example:**
```bash
python cli.py examples/*.txt --chunk-size 800 --top-k 5
```

## 📊 Example Run

### Documents Used

1. **doc1_climate_change.txt**: Overview of climate change, causes, and solutions
2. **doc2_artificial_intelligence.txt**: AI applications and ethical considerations
3. **doc3_renewable_energy.txt**: Renewable energy technologies and adoption

### Processing Output

```
Initializing RAG system...

Loading 3 document(s)...

✅ Successfully processed 3 documents
   Total chunks: 14

Document details:
  • doc1_climate_change.txt: 4 chunks
  • doc2_artificial_intelligence.txt: 5 chunks
  • doc3_renewable_energy.txt: 5 chunks

================================================================================

RAG System Ready! Ask questions about your documents.
Type 'quit' or 'exit' to end the session.

================================================================================
```

### Example Question 1: Document-Grounded Answer

**Question:** What are the main applications of AI in healthcare according to the documents?

**Answer:**
```
According to the documents, the main applications of AI in healthcare include:

1. Disease diagnosis - AI systems assist doctors in diagnosing various conditions
2. Drug discovery - AI helps in the development of new medications
3. Personalized treatment planning - AI enables customized treatment approaches for patients
4. Medical imaging analysis - AI-powered systems can detect anomalies in X-rays, MRIs, and CT scans with high accuracy, sometimes matching or exceeding human radiologists

These applications demonstrate how AI is transforming healthcare by improving diagnostic accuracy and enabling more personalized care.
```

**Sources & Citations:**
```
Source 1: doc2_artificial_intelligence.txt (Chunk 1)
Similarity: 87.34%
Text: Current applications of AI span numerous industries. In healthcare, AI systems assist in disease diagnosis, drug discovery, and personalized treatment planning. Medical imaging analysis powered by AI can detect anomalies in X-rays...

Source 2: doc2_artificial_intelligence.txt (Chunk 0)
Similarity: 82.15%
Text: Machine learning, a subset of AI, enables systems to learn and improve from experience without being explicitly programmed. Deep learning, a further specialized area, uses neural networks with multiple layers...

Source 3: doc2_artificial_intelligence.txt (Chunk 2)
Similarity: 76.89%
Text: The financial sector utilizes AI for fraud detection, algorithmic trading, credit scoring, and customer service through chatbots. AI algorithms can analyze vast amounts of transaction data in real-time...
```

### Example Question 2: Multi-Document Synthesis

**Question:** How do renewable energy and climate change mitigation relate?

**Answer:**
```
Renewable energy is a crucial strategy for climate change mitigation. According to the documents, climate change mitigation efforts focus on reducing greenhouse gas emissions through various strategies, including transitioning to renewable energy sources such as solar and wind power.

The documents explain that renewable energy offers multiple benefits for addressing climate change. The transition to renewable energy reduces greenhouse gas emissions, which are the primary cause of recent climate change. Renewable sources like solar, wind, hydroelectric, and geothermal energy do not emit carbon dioxide during operation, unlike fossil fuel combustion.

The cost decline in renewable energy has made this transition more feasible. Solar photovoltaic costs have fallen by over 80% since 2010, and wind power costs have decreased by approximately 50% during the same period. This makes renewable energy increasingly competitive with fossil fuels.

The documents also note that beyond emission reduction, renewable energy enhances energy security by reducing dependence on imported fossil fuels and creates jobs in manufacturing, installation, and maintenance sectors.
```

**Sources & Citations:**
```
Source 1: doc1_climate_change.txt (Chunk 2)
Similarity: 89.12%
Text: Mitigation efforts focus on reducing greenhouse gas emissions through various strategies. These include transitioning to renewable energy sources such as solar and wind power, improving energy efficiency...

Source 2: doc3_renewable_energy.txt (Chunk 4)
Similarity: 85.67%
Text: The transition to renewable energy offers multiple benefits beyond reducing greenhouse gas emissions. It enhances energy security by reducing dependence on imported fossil fuels. Renewable energy projects create jobs...

Source 3: doc3_renewable_energy.txt (Chunk 2)
Similarity: 81.23%
Text: The cost of renewable energy has declined dramatically over the past decade. Solar photovoltaic costs have fallen by over 80% since 2010, making solar power cost-competitive with fossil fuels...
```

### Example Question 3: No Answer Available

**Question:** What is the current population of Tokyo?

**Answer:**
```
I do not know based on the provided documents.
```

*No sources displayed as the answer is not found in the documents.*

## 🎯 Design Choices

### 1. Chunking Strategy
- **Sentence-based chunking**: Preserves semantic coherence
- **Configurable overlap**: Default 200 characters to maintain context across boundaries
- **Size optimization**: 1000 characters balances context window and retrieval precision

### 2. Embedding Model
- **OpenAI text-embedding-3-small**: Good balance of performance and cost
- **Batch processing**: Efficient embedding generation for multiple chunks
- **Dimension**: 1536-dimensional vectors for high-quality semantic representation

### 3. Vector Database
- **ChromaDB**: Lightweight, easy to set up, excellent for prototypes
- **Cosine similarity**: Standard for semantic search with normalized embeddings
- **In-memory with persistence**: Fast queries with data durability

### 4. LLM Selection
- **GPT-4 Turbo**: High-quality answer generation with strong instruction following
- **Temperature 0**: Deterministic outputs for consistent, factual responses
- **System prompts**: Explicit instructions to ground answers in context only

### 5. Retrieval
- **Top-K = 3**: Provides sufficient context without overwhelming the prompt
- **Similarity scoring**: Returned to user for transparency
- **Metadata preservation**: Document name and chunk ID tracked throughout

## ⚠️ Limitations

### Current Limitations

1. **Document Size**: Maximum 3 documents, approximately 20 pages each
   - Large documents may require significant processing time
   - Memory constraints for very long documents

2. **PDF Processing**: Basic text extraction
   - May struggle with complex layouts, tables, or images
   - OCR not included for scanned PDFs

3. **Chunking**: Simple sentence-based approach
   - May split logical sections awkwardly
   - No semantic understanding of document structure

4. **Context Window**: Fixed chunk size
   - May miss relevant information split across distant chunks
   - No dynamic chunk merging based on query

5. **API Dependencies**: Requires OpenAI API access
   - Costs incurred per query
   - Network dependency and latency

6. **Single Language**: Optimized for English
   - May work with other languages but not tested extensively

7. **No Caching**: Repeated queries generate new API calls
   - Could be optimized with semantic caching

## 🚀 Future Improvements

### Short Term

1. **Enhanced PDF Processing**
   - Table extraction and preservation
   - Image OCR with layout analysis
   - Support for more document formats (DOCX, HTML)

2. **Improved Chunking**
   - Semantic chunking using embeddings
   - Recursive splitting strategies
   - Document structure awareness (headers, sections)

3. **Query Optimization**
   - Query expansion and reformulation
   - Multi-query retrieval
   - Semantic caching for repeated questions

4. **Better Citations**
   - Highlight exact text used in answer
   - Page numbers and line references
   - Confidence scores for each citation

### Medium Term

1. **Advanced Retrieval**
   - Hybrid search (keyword + semantic)
   - Re-ranking with cross-encoder
   - Contextual compression of retrieved chunks

2. **Multi-Modal Support**
   - Image understanding and Q&A
   - Chart and graph interpretation
   - Video transcription and analysis

3. **Evaluation Framework**
   - Automated testing suite
   - Answer quality metrics (faithfulness, relevance)
   - Retrieval accuracy benchmarks

4. **User Experience**
   - Document preview and navigation
   - Interactive citation exploration
   - Follow-up question suggestions

### Long Term

1. **Agentic Capabilities**
   - Multi-step reasoning
   - Tool use for calculations
   - Query planning and decomposition

2. **Enterprise Features**
   - User authentication and permissions
   - Document versioning
   - Audit logs and compliance

3. **Scalability**
   - Distributed vector store
   - API rate limiting and queuing
   - Horizontal scaling architecture

4. **Alternative Backends**
   - Support for open-source LLMs
   - Local embedding models
   - Multiple vector database options

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Web UI)
- **Backend**: Python 3.8+
- **LLM**: OpenAI GPT-4 Turbo
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector DB**: ChromaDB
- **PDF Processing**: pypdf
- **Environment**: python-dotenv

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. For production use, consider the limitations and future improvements outlined above.

## 📧 Support

For issues or questions, please refer to the documentation in this README.
