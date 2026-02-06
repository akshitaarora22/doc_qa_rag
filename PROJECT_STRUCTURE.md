# Project Structure

Complete overview of the RAG system file organization.

## Directory Tree

```
rag_system/
├── src/                          # Core system modules
│   ├── __init__.py              # Package initialization
│   ├── document_processor.py    # Text extraction and chunking
│   ├── vector_store.py          # ChromaDB interface
│   ├── llm_interface.py         # OpenAI API wrapper
│   └── rag_system.py            # Main orchestrator
│
├── examples/                     # Example documents
│   ├── doc1_climate_change.txt
│   ├── doc2_artificial_intelligence.txt
│   └── doc3_renewable_energy.txt
│
├── app.py                       # Streamlit web interface
├── cli.py                       # Command-line interface
├── demo.py                      # Demonstration script
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
│
├── README.md                    # Full documentation
├── QUICKSTART.md                # Quick setup guide
└── PROJECT_STRUCTURE.md         # This file
```

## File Descriptions

### Core Modules (`src/`)

#### `document_processor.py` (145 lines)
**Purpose**: Document text extraction and intelligent chunking

**Key Classes**:
- `DocumentProcessor`: Main processing class

**Key Methods**:
- `extract_text(file_path)`: Extract text from TXT/PDF
- `chunk_text(text, doc_name)`: Split text into overlapping chunks
- `process_document(file_path)`: Complete processing pipeline

**Features**:
- Sentence-aware chunking
- Configurable chunk size and overlap
- Metadata preservation (doc name, chunk ID)

#### `vector_store.py` (73 lines)
**Purpose**: Vector database management using ChromaDB

**Key Classes**:
- `VectorStore`: ChromaDB interface

**Key Methods**:
- `add_chunks(chunks, embeddings)`: Store embeddings with metadata
- `search(query_embedding, top_k)`: Similarity search
- `clear()`: Reset collection
- `count()`: Get total chunks

**Features**:
- Cosine similarity search
- Metadata filtering
- Persistent storage

#### `llm_interface.py` (109 lines)
**Purpose**: OpenAI API interactions for embeddings and completions

**Key Classes**:
- `LLMInterface`: OpenAI wrapper

**Key Methods**:
- `create_embedding(text)`: Single embedding
- `create_embeddings_batch(texts)`: Batch embeddings
- `generate_answer(query, chunks)`: Generate grounded answer

**Features**:
- Batch processing for efficiency
- Temperature 0 for deterministic outputs
- System prompts for grounding

#### `rag_system.py` (159 lines)
**Purpose**: Main orchestrator coordinating all components

**Key Classes**:
- `RAGSystem`: Complete RAG pipeline

**Key Methods**:
- `load_documents(file_paths)`: Process and index documents
- `query(question)`: Answer questions with citations
- `get_system_info()`: System state information

**Features**:
- End-to-end pipeline management
- Error handling and validation
- Statistics and monitoring

### User Interfaces

#### `app.py` (206 lines)
**Purpose**: Streamlit web interface

**Features**:
- Document upload with drag-and-drop
- Real-time processing feedback
- Interactive Q&A interface
- Citation display with expandable sources
- Configuration controls
- Question history

**Pages**:
- Document upload sidebar
- Main Q&A area
- History panel
- System information

#### `cli.py` (101 lines)
**Purpose**: Command-line interface

**Features**:
- Argument parsing for documents and config
- Interactive Q&A loop
- Formatted output with source citations
- Clean exit handling

**Usage**:
```bash
python cli.py doc1.txt doc2.txt --chunk-size 1000 --top-k 3
```

#### `demo.py` (313 lines)
**Purpose**: Demonstration script showing expected behavior

**Features**:
- Simulates complete workflow
- Shows example questions and answers
- Displays source citations
- Requires no API key

**Sections**:
1. Document processing
2. Simple question (healthcare AI)
3. Multi-document synthesis (energy & climate)
4. No answer available (Tokyo population)
5. System information

### Example Documents

#### `doc1_climate_change.txt` (2,089 chars)
**Topics**:
- Causes and effects of climate change
- Greenhouse gas emissions
- Mitigation and adaptation strategies
- International cooperation (Paris Agreement)

#### `doc2_artificial_intelligence.txt` (2,823 chars)
**Topics**:
- AI technologies (ML, deep learning)
- Healthcare applications
- Financial sector use cases
- Ethical considerations
- Future prospects

#### `doc3_renewable_energy.txt` (3,147 chars)
**Topics**:
- Types of renewable energy
- Cost trends
- Energy storage
- Global adoption
- Corporate commitments

### Configuration Files

#### `requirements.txt`
**Dependencies**:
- streamlit==1.29.0 (Web UI)
- openai==1.6.1 (LLM & embeddings)
- chromadb==0.4.22 (Vector database)
- pypdf==3.17.4 (PDF processing)
- python-dotenv==1.0.0 (Environment variables)
- tiktoken==0.5.2 (Token counting)
- numpy==1.24.3 (Numerical operations)

#### `.env.example`
**Template for**:
- OPENAI_API_KEY
- Optional model configuration

#### `.gitignore`
**Excludes**:
- Python cache files
- Virtual environments
- API keys (.env)
- ChromaDB data
- Temporary uploads
- IDE configurations

### Documentation

#### `README.md` (608 lines)
**Comprehensive documentation including**:
- Features overview
- Architecture diagram
- Setup instructions
- Usage examples
- Example run with output
- Design choices explanation
- Current limitations
- Future improvements roadmap
- Technology stack

#### `QUICKSTART.md` (68 lines)
**Quick start guide with**:
- 5-minute setup
- Basic usage
- Example queries
- Common troubleshooting

#### `PROJECT_STRUCTURE.md` (This file)
**Project organization overview**

## Code Statistics

| Component | Lines of Code | Purpose |
|-----------|---------------|---------|
| document_processor.py | 145 | Text extraction & chunking |
| vector_store.py | 73 | Vector database interface |
| llm_interface.py | 109 | OpenAI API wrapper |
| rag_system.py | 159 | System orchestrator |
| app.py | 206 | Web interface |
| cli.py | 101 | CLI interface |
| demo.py | 313 | Demonstration |
| **Total** | **1,106** | **Core system** |

## Generated Artifacts

When running the system, these are created automatically:

### Runtime Artifacts
- `chroma_db/` - ChromaDB vector database (persisted)
- `temp_uploads/` - Temporary file storage for uploads
- `__pycache__/` - Python bytecode cache

## Design Principles

### Modularity
- Each component has single responsibility
- Clear interfaces between modules
- Easy to swap implementations

### Extensibility
- Add new document types in `document_processor.py`
- Change embedding model in `llm_interface.py`
- Replace vector store in `vector_store.py`

### Maintainability
- Comprehensive docstrings
- Type hints where helpful
- Consistent naming conventions
- Error handling throughout

### User Experience
- Multiple interfaces (web, CLI, demo)
- Clear error messages
- Progress indicators
- Rich citation display

## Testing Approach

While formal tests are not included, the system can be validated through:

1. **Demo script** (`demo.py`): Shows expected behavior
2. **Example documents**: Provides test corpus
3. **Manual testing**: Use provided example questions
4. **Edge cases**: Try questions with no answers

## Deployment Considerations

### Local Development
- Run directly with `streamlit run app.py`
- Suitable for personal use and testing

### Production Deployment
Would require:
- Environment variable management
- API rate limiting
- User authentication
- Database scaling
- Monitoring and logging
- Error tracking

## Next Steps for Development

See README.md "Future Improvements" section for:
- Enhanced PDF processing
- Improved chunking strategies
- Evaluation framework
- Multi-modal support
- Enterprise features
