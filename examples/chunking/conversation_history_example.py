#!/usr/bin/env python3
"""
Conversation History Processing Example for Chunking System

This example demonstrates how to integrate the ContextWindowChunker 
and ChunkedProcessor for handling large conversation history files 
that exceed token context window limits.
"""

import json
from context_window_chunker import ContextWindowChunker
from chunked_processor import ChunkedProcessor


def create_sample_conversation_history():
    """Create a sample conversation history for testing"""
    
    # Create a large conversation history
    conversations = []
    
    for i in range(50):  # 50 conversations to make it large
        conversation = {
            "conversation_id": f"conv_{i}",
            "participants": ["user", "assistant"],
            "messages": [
                {
                    "role": "user" if j % 2 == 0 else "assistant",
                    "content": f"This is message {j} in conversation {i}. The content is quite detailed and extensive. It contains multiple sentences that describe various topics and ideas. This is a sample conversation history that would normally exceed token limits when processed as a whole.",
                    "timestamp": f"2025-01-{i:02d}T{j:02d}:00:00Z"
                }
                for j in range(20)  # 20 messages per conversation
            ],
            "metadata": {
                "created_at": f"2025-01-{i:02d}T00:00:00Z",
                "topic": f"Topic {i}",
                "duration": "30 minutes"
            }
        }
        conversations.append(conversation)
    
    return {"conversations": conversations}


def process_conversation_history():
    """Process a large conversation history using ContextWindowChunker"""
    
    # Create sample conversation history
    conversation_history = create_sample_conversation_history()
    
    print("Processing conversation history...")
    print(f"Total conversations: {len(conversation_history['conversations'])}")
    
    # Initialize the chunker
    chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)
    
    # Process the conversation history
    chunks = chunker.process_large_json(conversation_history)
    
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
            "type": chunk.get('type', 'json')
        }
        processed_chunks.append(processed_chunk)
        print(f"Processed conversation chunk {i+1}: {chunk['token_count']} tokens")
    
    return processed_chunks


def process_conversation_with_chunked_processor():
    """Demonstrate using ChunkedProcessor for conversation history processing"""
    
    # Create sample conversation history
    conversation_history = create_sample_conversation_history()
    
    # Save to a temporary file for demonstration
    temp_file = "temp_conversation_history.json"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(conversation_history, f, indent=2)
    
    print("\nUsing ChunkedProcessor for conversation history processing...")
    
    # Initialize the processor
    processor = ChunkedProcessor(max_tokens=200000, overlap=1000)
    
    def process_conversation_chunk(chunk_data):
        """Custom processing function for conversation chunks"""
        # Parse the JSON content
        chunk_content = json.loads(chunk_data['content'])
        
        # Process the chunk (example: count conversations)
        conversation_count = len(chunk_content.get('conversations', []))
        
        return {
            "chunk_id": chunk_data['chunk_id'],
            "conversation_count": conversation_count,
            "token_count": chunk_data['token_count'],
            "processed": True
        }
    
    # Process the large conversation file
    results = processor.process_large_file(
        file_path=temp_file,
        process_function=process_conversation_chunk
    )
    
    print(f"Processed {len(results)} conversation chunks successfully")
    
    # Clean up
    import os
    os.remove(temp_file)
    
    return results


def analyze_conversation_chunks():
    """Analyze the chunks created from conversation history"""
    
    # Create sample conversation history
    conversation_history = create_sample_conversation_history()
    
    print("\nAnalyzing conversation chunks...")
    
    # Initialize the chunker
    chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)
    
    # Process the conversation history
    chunks = chunker.process_large_json(conversation_history)
    
    # Analyze each chunk
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"  Token count: {chunk['token_count']}")
        print(f"  Chunk size: {chunk['chunk_size']} characters")
        print(f"  Strategy: {chunk['strategy']}")
        print(f"  Needs processing: {chunk['needs_processing']}")
        
        # Show first part of content
        content_preview = chunk['content'][:100] + "..." if len(chunk['content']) > 100 else chunk['content']
        print(f"  Content preview: {content_preview}")


if __name__ == "__main__":
    # Run conversation history processing example
    conv_results = process_conversation_history()
    
    # Run ChunkedProcessor example
    try:
        processor_results = process_conversation_with_chunked_processor()
    except Exception as e:
        print(f"ChunkedProcessor example skipped due to: {e}")
    
    # Analyze chunks
    analyze_conversation_chunks()
    
    print("\nConversation History Processing Example Complete!")