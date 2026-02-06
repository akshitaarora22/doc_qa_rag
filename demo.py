"""
Demo script showing example run of the RAG system.
This script demonstrates the system without requiring API keys by showing expected behavior.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


def print_separator(char="=", length=80):
    print("\n" + char*length + "\n")


def demo_document_processing():
    """Demonstrate document processing phase."""
    print("RAG SYSTEM DEMONSTRATION")
    print_separator()
    
    print("STEP 1: DOCUMENT PROCESSING")
    print("-" * 80)
    print("\nDocuments to process:")
    print("  1. doc1_climate_change.txt")
    print("  2. doc2_artificial_intelligence.txt")
    print("  3. doc3_renewable_energy.txt")
    
    print("\nProcessing documents...")
    print("  ✓ Extracting text from documents")
    print("  ✓ Chunking text (size: 1000 chars, overlap: 200 chars)")
    print("  ✓ Generating embeddings")
    print("  ✓ Storing in vector database")
    
    print("\n✅ Successfully processed 3 documents into 14 chunks")
    print("\nDocument details:")
    print("  • doc1_climate_change.txt: 4 chunks")
    print("  • doc2_artificial_intelligence.txt: 5 chunks")
    print("  • doc3_renewable_energy.txt: 5 chunks")


def demo_question_1():
    """Demonstrate first question with answer found."""
    print_separator()
    print("EXAMPLE 1: SPECIFIC QUESTION WITH CLEAR ANSWER")
    print("-" * 80)
    
    question = "What are the main applications of AI in healthcare according to the documents?"
    print(f"\nQuestion: {question}")
    
    print("\nSearching documents...")
    print("  ✓ Embedding query")
    print("  ✓ Retrieving top 3 relevant chunks")
    print("  ✓ Generating answer")
    
    print("\n" + "─"*80)
    print("ANSWER:")
    print("─"*80)
    answer = """According to the documents, the main applications of AI in healthcare include:

1. Disease diagnosis - AI systems assist doctors in diagnosing various conditions
2. Drug discovery - AI helps in the development of new medications  
3. Personalized treatment planning - AI enables customized treatment approaches for patients
4. Medical imaging analysis - AI-powered systems can detect anomalies in X-rays, MRIs, and CT scans with high accuracy, sometimes matching or exceeding human radiologists

These applications demonstrate how AI is transforming healthcare by improving diagnostic accuracy and enabling more personalized care."""
    print(answer)
    
    print("\n" + "─"*80)
    print("SOURCES & CITATIONS:")
    print("─"*80)
    
    sources = [
        {
            'num': 1,
            'doc': 'doc2_artificial_intelligence.txt',
            'chunk': 1,
            'similarity': 87.34,
            'text': 'Current applications of AI span numerous industries. In healthcare, AI systems assist in disease diagnosis, drug discovery, and personalized treatment planning. Medical imaging analysis powered by AI can detect anomalies in X-rays, MRIs, and CT scans with high accuracy...'
        },
        {
            'num': 2,
            'doc': 'doc2_artificial_intelligence.txt',
            'chunk': 0,
            'similarity': 82.15,
            'text': 'Machine learning, a subset of AI, enables systems to learn and improve from experience without being explicitly programmed. Deep learning, a further specialized area, uses neural networks with multiple layers to process complex patterns in data...'
        },
        {
            'num': 3,
            'doc': 'doc2_artificial_intelligence.txt',
            'chunk': 2,
            'similarity': 76.89,
            'text': 'The financial sector utilizes AI for fraud detection, algorithmic trading, credit scoring, and customer service through chatbots. AI algorithms can analyze vast amounts of transaction data in real-time to identify suspicious patterns...'
        }
    ]
    
    for source in sources:
        print(f"\nSource {source['num']}: {source['doc']} (Chunk {source['chunk']})")
        print(f"Similarity: {source['similarity']:.2f}%")
        print(f"Text: {source['text']}")


def demo_question_2():
    """Demonstrate question requiring synthesis across documents."""
    print_separator()
    print("EXAMPLE 2: MULTI-DOCUMENT SYNTHESIS")
    print("-" * 80)
    
    question = "How do renewable energy and climate change mitigation relate?"
    print(f"\nQuestion: {question}")
    
    print("\nSearching documents...")
    print("  ✓ Embedding query")
    print("  ✓ Retrieving relevant chunks from multiple documents")
    print("  ✓ Synthesizing answer")
    
    print("\n" + "─"*80)
    print("ANSWER:")
    print("─"*80)
    answer = """Renewable energy is a crucial strategy for climate change mitigation. According to the documents, climate change mitigation efforts focus on reducing greenhouse gas emissions through various strategies, including transitioning to renewable energy sources such as solar and wind power.

The documents explain that renewable energy offers multiple benefits for addressing climate change. The transition to renewable energy reduces greenhouse gas emissions, which are the primary cause of recent climate change. Renewable sources like solar, wind, hydroelectric, and geothermal energy do not emit carbon dioxide during operation, unlike fossil fuel combustion.

The cost decline in renewable energy has made this transition more feasible. Solar photovoltaic costs have fallen by over 80% since 2010, and wind power costs have decreased by approximately 50% during the same period. This makes renewable energy increasingly competitive with fossil fuels.

The documents also note that beyond emission reduction, renewable energy enhances energy security by reducing dependence on imported fossil fuels and creates jobs in manufacturing, installation, and maintenance sectors."""
    print(answer)
    
    print("\n" + "─"*80)
    print("SOURCES & CITATIONS:")
    print("─"*80)
    
    sources = [
        {
            'num': 1,
            'doc': 'doc1_climate_change.txt',
            'chunk': 2,
            'similarity': 89.12,
            'text': 'Mitigation efforts focus on reducing greenhouse gas emissions through various strategies. These include transitioning to renewable energy sources such as solar and wind power, improving energy efficiency in buildings and transportation...'
        },
        {
            'num': 2,
            'doc': 'doc3_renewable_energy.txt',
            'chunk': 4,
            'similarity': 85.67,
            'text': 'The transition to renewable energy offers multiple benefits beyond reducing greenhouse gas emissions. It enhances energy security by reducing dependence on imported fossil fuels. Renewable energy projects create jobs in manufacturing, installation, and maintenance...'
        },
        {
            'num': 3,
            'doc': 'doc3_renewable_energy.txt',
            'chunk': 2,
            'similarity': 81.23,
            'text': 'The cost of renewable energy has declined dramatically over the past decade. Solar photovoltaic costs have fallen by over 80% since 2010, making solar power cost-competitive with fossil fuels in many regions...'
        }
    ]
    
    for source in sources:
        print(f"\nSource {source['num']}: {source['doc']} (Chunk {source['chunk']})")
        print(f"Similarity: {source['similarity']:.2f}%")
        print(f"Text: {source['text']}")


def demo_question_3():
    """Demonstrate question with no answer in documents."""
    print_separator()
    print("EXAMPLE 3: QUESTION NOT ANSWERABLE FROM DOCUMENTS")
    print("-" * 80)
    
    question = "What is the current population of Tokyo?"
    print(f"\nQuestion: {question}")
    
    print("\nSearching documents...")
    print("  ✓ Embedding query")
    print("  ✓ Retrieving top 3 chunks")
    print("  ✓ Generating answer")
    
    print("\n" + "─"*80)
    print("ANSWER:")
    print("─"*80)
    print("I do not know based on the provided documents.")
    
    print("\n(No sources displayed as the answer is not found in the documents)")


def demo_system_info():
    """Show system configuration and architecture."""
    print_separator()
    print("SYSTEM INFORMATION")
    print("-" * 80)
    
    print("\nConfiguration:")
    print("  • Chunk size: 1000 characters")
    print("  • Chunk overlap: 200 characters")
    print("  • Top K retrieval: 3 chunks")
    print("  • Embedding model: text-embedding-3-small (OpenAI)")
    print("  • LLM model: gpt-4-turbo-preview (OpenAI)")
    print("  • Vector database: ChromaDB")
    print("  • Similarity metric: Cosine distance")
    
    print("\nArchitecture:")
    print("  1. Document Processor: Text extraction and chunking")
    print("  2. Embedding Generator: Create vector representations")
    print("  3. Vector Store: Index and search embeddings")
    print("  4. LLM Interface: Generate grounded answers")
    
    print("\nKey Features:")
    print("  ✓ Strict grounding in document content")
    print("  ✓ Source attribution with document and chunk references")
    print("  ✓ Similarity scores for transparency")
    print("  ✓ 'I do not know' responses when appropriate")
    print("  ✓ Support for TXT and PDF documents")


def main():
    """Run complete demonstration."""
    demo_document_processing()
    demo_question_1()
    demo_question_2()
    demo_question_3()
    demo_system_info()
    
    print_separator()
    print("DEMONSTRATION COMPLETE")
    print("\nThis demonstration shows the expected behavior of the RAG system.")
    print("To run the actual system with real API calls:")
    print("  1. Set up your OpenAI API key in .env file")
    print("  2. Run: streamlit run app.py (for web UI)")
    print("  3. Or run: python cli.py examples/*.txt (for CLI)")
    print_separator()


if __name__ == "__main__":
    main()
