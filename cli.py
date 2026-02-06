"""
Command-line interface for RAG system.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import argparse

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from rag_system import RAGSystem


def print_separator():
    print("\n" + "="*80 + "\n")


def format_sources(sources):
    """Format source citations for display."""
    output = []
    for source in sources:
        output.append(
            f"\nSource {source['source_number']}: {source['document_name']} "
            f"(Chunk {source['chunk_id']})\n"
            f"Similarity: {source['similarity_score']:.2%}\n"
            f"Text: {source['text_snippet']}\n"
        )
    return "\n".join(output)


def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='RAG Document Q&A System')
    parser.add_argument('documents', nargs='+', help='Paths to documents (max 3)')
    parser.add_argument('--chunk-size', type=int, default=1000, help='Chunk size in characters')
    parser.add_argument('--chunk-overlap', type=int, default=200, help='Chunk overlap in characters')
    parser.add_argument('--top-k', type=int, default=3, help='Number of chunks to retrieve')
    
    args = parser.parse_args()
    
    # Validate number of documents
    if len(args.documents) > 3:
        print("Error: Maximum 3 documents allowed")
        sys.exit(1)
    
    # Initialize RAG system
    print("Initializing RAG system...")
    rag_system = RAGSystem(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        top_k=args.top_k
    )
    
    # Load documents
    print(f"\nLoading {len(args.documents)} document(s)...")
    try:
        stats = rag_system.load_documents(args.documents)
        print(f"\n✅ Successfully processed {stats['documents_processed']} documents")
        print(f"   Total chunks: {stats['total_chunks']}")
        print("\nDocument details:")
        for doc in stats['documents']:
            print(f"  • {doc['name']}: {doc['chunks']} chunks")
    except Exception as e:
        print(f"Error loading documents: {str(e)}")
        sys.exit(1)
    
    # Interactive Q&A loop
    print_separator()
    print("RAG System Ready! Ask questions about your documents.")
    print("Type 'quit' or 'exit' to end the session.")
    print_separator()
    
    while True:
        try:
            question = input("\nQuestion: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not question:
                continue
            
            # Query the system
            print("\nSearching documents...")
            result = rag_system.query(question)
            
            # Display answer
            print("\n" + "─"*80)
            print("ANSWER:")
            print("─"*80)
            print(result['answer'])
            
            # Display sources
            if "do not know" not in result['answer'].lower():
                print("\n" + "─"*80)
                print("SOURCES & CITATIONS:")
                print("─"*80)
                print(format_sources(result['sources']))
            
            print_separator()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
