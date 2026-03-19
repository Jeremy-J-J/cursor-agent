#!/usr/bin/env python3
"""
JSON Processing Example for Chunking System

This example demonstrates how to integrate the ContextWindowChunker 
and ChunkedProcessor for handling large JSON datasets that exceed 
token context window limits.
"""

import json
from context_window_chunker import ContextWindowChunker
from chunked_processor import ChunkedProcessor


def process_large_json_dataset():
    """Process a large JSON dataset that exceeds token limits"""
    
    # Create a large JSON dataset (simulating a real-world scenario)
    large_json_data = {
        "users": [
            {
                "id": i,
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "profile": {
                    "bio": f"This is the biography of user {i}. It contains detailed information about their interests, background, and professional experience.",
                    "preferences": {
                        "theme": "dark" if i % 2 == 0 else "light",
                        "notifications": True if i % 3 == 0 else False
                    }
                },
                "activity_log": [
                    {
                        "timestamp": f"2025-01-{i:02d}T08:00:00Z",
                        "action": "login",
                        "details": f"User {i} logged in successfully"
                    }
                    for _ in range(10)
                ]
            }
            for i in range(1000)  # 1000 users to make it large enough
        ]
    }
    
    print("Processing large JSON dataset...")
    print(f"Total users: {len(large_json_data['users'])}")
    
    # Initialize the chunker
    chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)
    
    # Process the JSON data
    chunks = chunker.process_large_json(large_json_data)
    
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
            "processed": True,
            "user_count": len(json.loads(chunk['content'])['users']) if 'users' in chunk['content'] else 0
        }
        processed_chunks.append(processed_chunk)
        print(f"Processed chunk {i+1}: {chunk['token_count']} tokens")
    
    return processed_chunks


def process_json_with_chunked_processor():
    """Demonstrate using ChunkedProcessor for JSON processing"""
    
    # Create sample large JSON data
    sample_json = {
        "products": [
            {
                "id": i,
                "name": f"Product {i}",
                "description": f"Description for product {i}. This is a very detailed description that contains a lot of information about the product features, specifications, and benefits.",
                "price": round(i * 10.5, 2),
                "category": "Electronics" if i % 3 == 0 else "Clothing" if i % 3 == 1 else "Books"
            }
            for i in range(500)  # 500 products to make it large
        ]
    }
    
    print("\nUsing ChunkedProcessor for JSON processing...")
    
    # Initialize the processor
    processor = ChunkedProcessor(max_tokens=200000, overlap=1000)
    
    def process_json_chunk(chunk_data):
        """Custom processing function for JSON chunks"""
        # Parse the JSON content
        chunk_content = json.loads(chunk_data['content'])
        
        # Process the chunk (example: count products)
        product_count = len(chunk_content.get('products', []))
        
        return {
            "chunk_id": chunk_data['chunk_id'],
            "product_count": product_count,
            "token_count": chunk_data['token_count'],
            "processed": True
        }
    
    # Process the large JSON file
    results = processor.process_large_file(
        file_path="temp_large_json.json",  # This would be your actual file path
        process_function=process_json_chunk
    )
    
    print(f"Processed {len(results)} chunks successfully")
    return results


if __name__ == "__main__":
    # Run JSON processing example
    json_results = process_large_json_dataset()
    
    # Run ChunkedProcessor example (this would require a file)
    try:
        processor_results = process_json_with_chunked_processor()
    except Exception as e:
        print(f"ChunkedProcessor example skipped due to: {e}")
        print("This example requires a file to be created first")
    
    print("\nJSON Processing Example Complete!")