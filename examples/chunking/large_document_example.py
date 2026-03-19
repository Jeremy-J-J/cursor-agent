#!/usr/bin/env python3
"""
Large Document Processing Example for Chunking System

This example demonstrates how to integrate the ContextWindowChunker 
and ChunkedProcessor for handling large text documents that exceed 
token context window limits.
"""

import os
from context_window_chunker import ContextWindowChunker
from chunked_processor import ChunkedProcessor


def create_sample_large_document():
    """Create a sample large document for testing"""
    
    # Create a large document with multiple sections
    document_parts = []
    
    for i in range(100):  # 100 sections to make it large
        section = f"""
Section {i}
==========

This is section {i} of our large document. It contains detailed information about various topics.
The content is quite extensive and would normally exceed the token context window limits.

Key points in this section:
- Point 1 about topic {i}
- Point 2 about topic {i}
- Point 3 about topic {i}

Additional details:
- More information about {i}
- Further elaboration on {i}
- Extended content for {i}

This document continues with many more sections like this one, making it very large in size.
The total character count will be well over the 262,144 token limit when converted to tokens.
"""
        document_parts.append(section)
    
    return "\n".join(document_parts)


def process_large_document():
    """Process a large document using ContextWindowChunker"""
    
    # Create sample large document
    large_document = create_sample_large_document()
    
    print("Processing large document...")
    print(f"Document size: {len(large_document)} characters")
    
    # Initialize the chunker
    chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)
    
    # Chunk the document
    chunks = chunker.chunk_content(large_document)
    
    print(f"Created {len(chunks)} chunks")
    
    # Get statistics
    stats = chunker.get_chunk_statistics(chunks)
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Average tokens per chunk: {stats['avg_tokens_per_chunk']:.2f}")
    print(f"Max tokens in chunk: {stats['max_tokens_in_chunk']}")
    print(f"Min tokens in chunk: {stats['min_tokens_in_chunk']}")
    
    # Process each chunk (simulating actual processing)
    processed_chunks = []
    for i, chunk in enumerate(chunks):
        # Simulate processing each chunk
        processed_chunk = {
            "chunk_id": chunk['chunk_id'],
            "token_count": chunk['token_count'],
            "chunk_size": chunk['chunk_size'],
            "processed": True,
            "strategy": chunk['strategy']
        }
        processed_chunks.append(processed_chunk)
        print(f"Processed chunk {i+1}: {chunk['token_count']} tokens")
    
    return processed_chunks


def process_large_document_with_chunked_processor():
    """Demonstrate using ChunkedProcessor for large document processing"""
    
    # Create sample large document
    large_document = create_sample_large_document()
    
    # Save to a temporary file for demonstration
    temp_file = "temp_large_document.txt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(large_document)
    
    print("\nUsing ChunkedProcessor for large document processing...")
    
    # Initialize the processor
    processor = ChunkedProcessor(max_tokens=200000, overlap=1000)
    
    def process_document_chunk(chunk_data):
        """Custom processing function for document chunks"""
        # Simulate document processing (e.g., extract key information)
        content = chunk_data['content']
        token_count = chunk_data['token_count']
        
        # Simple processing: count words
        word_count = len(content.split())
        
        return {
            "chunk_id": chunk_data['chunk_id'],
            "word_count": word_count,
            "token_count": token_count,
            "processed": True
        }
    
    # Process the large document file
    results = processor.process_large_file(
        file_path=temp_file,
        process_function=process_document_chunk
    )
    
    print(f"Processed {len(results)} chunks successfully")
    
    # Clean up
    os.remove(temp_file)
    
    return results


def demonstrate_different_strategies():
    """Demonstrate different chunking strategies"""
    
    # Create sample content
    sample_content = "This is a sample document with multiple sentences. " * 1000
    
    print("\nDemonstrating different chunking strategies...")
    
    strategies = ['tokens', 'sentences', 'paragraphs']
    
    for strategy in strategies:
        chunker = ContextWindowChunker(max_tokens=200000, overlap=1000, chunking_strategy=strategy)
        chunks = chunker.chunk_content(sample_content)
        
        stats = chunker.get_chunk_statistics(chunks)
        print(f"{strategy.capitalize()} strategy:")
        print(f"  Chunks created: {len(chunks)}")
        print(f"  Average tokens per chunk: {stats['avg_tokens_per_chunk']:.2f}")
        print(f"  Total tokens: {stats['total_tokens']}")
        print()


if __name__ == "__main__":
    # Run large document processing example
    doc_results = process_large_document()
    
    # Run ChunkedProcessor example
    try:
        processor_results = process_large_document_with_chunked_processor()
    except Exception as e:
        print(f"ChunkedProcessor example skipped due to: {e}")
    
    # Demonstrate different strategies
    demonstrate_different_strategies()
    
    print("\nLarge Document Processing Example Complete!")