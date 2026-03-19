#!/usr/bin/env python3
"""
Simple Usage Example for Chunking System

This example demonstrates the basic usage of ContextWindowChunker 
and ChunkedProcessor classes with clear explanations.
"""

from context_window_chunker import ContextWindowChunker
from chunked_processor import ChunkedProcessor


def basic_chunking_example():
    """Demonstrate basic chunking functionality"""
    
    print("=== Basic Chunking Example ===")
    
    # Create sample large text
    large_text = "This is a sample text that will be chunked. " * 10000
    
    # Initialize chunker
    chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)
    
    # Chunk the content
    chunks = chunker.chunk_content(large_text)
    
    # Show results
    print(f"Original text size: {len(large_text)} characters")
    print(f"Number of chunks created: {len(chunks)}")
    
    # Get statistics
    stats = chunker.get_chunk_statistics(chunks)
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Average tokens per chunk: {stats['avg_tokens_per_chunk']:.2f}")
    
    return chunks


def json_chunking_example():
    """Demonstrate JSON chunking functionality"""
    
    print("\n=== JSON Chunking Example ===")
    
    # Create sample large JSON data
    large_json = {
        "items": [
            {"id": i, "name": f"Item {i}", "description": f"Description for item {i}"} 
            for i in range(1000)
        ]
    }
    
    # Initialize chunker
    chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)
    
    # Process JSON data
    chunks = chunker.process_large_json(large_json)
    
    # Show results
    print(f"Number of JSON chunks created: {len(chunks)}")
    
    # Get statistics
    stats = chunker.get_chunk_statistics(chunks)
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Average tokens per chunk: {stats['avg_tokens_per_chunk']:.2f}")
    
    return chunks


def file_processing_example():
    """Demonstrate file processing with ChunkedProcessor"""
    
    print("\n=== File Processing Example ===")
    
    # Create a sample file for demonstration
    sample_content = "Sample file content for processing. " * 5000
    
    # Save to temporary file
    temp_file = "temp_sample_file.txt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    # Initialize processor
    processor = ChunkedProcessor(max_tokens=200000, overlap=1000)
    
    def simple_processor(chunk_data):
        """Simple processing function"""
        return {
            "chunk_id": chunk_data['chunk_id'],
            "token_count": chunk_data['token_count'],
            "processed": True
        }
    
    # Process the file
    results = processor.process_large_file(
        file_path=temp_file,
        process_function=simple_processor
    )
    
    print(f"Processed {len(results)} chunks successfully")
    
    # Clean up
    import os
    os.remove(temp_file)
    
    return results


def main():
    """Run all examples"""
    
    print("Chunking System - Simple Usage Examples")
    print("=" * 50)
    
    # Run basic examples
    basic_chunks = basic_chunking_example()
    json_chunks = json_chunking_example()
    
    # Run file processing example
    file_results = file_processing_example()
    
    print("\n" + "=" * 50)
    print("All examples completed successfully!")
    print(f"Basic chunks created: {len(basic_chunks)}")
    print(f"JSON chunks created: {len(json_chunks)}")
    print(f"File processing results: {len(file_results)}")


if __name__ == "__main__":
    main()