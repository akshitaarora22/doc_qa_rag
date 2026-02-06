# Quick Start Guide

Get the RAG system running in 5 minutes.

## Prerequisites

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Setup Steps

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Run the Application

**Option A: Web UI (Recommended)**
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

**Option B: Command Line**
```bash
python cli.py examples/doc1_climate_change.txt examples/doc2_artificial_intelligence.txt
```

## First Query

Once running, try these example questions:

1. "What are the main applications of AI in healthcare?"
2. "How do renewable energy and climate change mitigation relate?"
3. "What is quantum computing?" (Should return "I do not know")

## Troubleshooting

**Import errors?**
```bash
pip install --upgrade -r requirements.txt
```

**API key not working?**
- Verify key is valid at https://platform.openai.com/api-keys
- Check .env file format (no quotes around key)
- Restart the application

**ChromaDB errors?**
```bash
rm -rf chroma_db/  # Clear database and restart
```

## What's Next?

- Read full [README.md](README.md) for detailed documentation
- Customize chunking parameters in the UI
- Upload your own documents (TXT or PDF)
- Experiment with different questions

## Demo Mode

To see example output without API calls:
```bash
python demo.py
```
