#!/usr/bin/env python3
"""
Script to demonstrate processing of large conversation history files
using the chunking approach to stay within token limits.
"""

import json
import os
from conversation_chunker import ConversationHistoryChunker

def main():
    """Main function to demonstrate large conversation processing."""
    
    # Path to the large conversation file
    input_file = "conversation_history.json"
    output_dir = "./chunked_conversations"
    
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        return
    
    # Initialize the chunker with appropriate parameters for large files
    # Using 200,000 tokens per chunk to stay within the limit
    chunker = ConversationHistoryChunker(max_tokens=200000, overlap=1000)
    
    print("Starting conversation history chunking...")
    print(f"Processing file: {input_file}")
    
    # Chunk the conversation history
    chunk_files = chunker.chunk_conversation_history(input_file, output_dir)
    
    if chunk_files:
        print(f"Successfully created {len(chunk_files)} chunks")
        
        # Process each chunk (example processing function)
        def example_processing_function(chunk_data):
            """Example processing function for demonstration."""
            content = chunk_data.get("content", [])
            user_messages = [msg for msg in content if msg.get("role") == "user"]
            assistant_messages = [msg for msg in content if msg.get("role") == "assistant"]
            
            return {
                "chunk_id": chunk_data.get("chunk_info", {}).get("chunk_id"),
                "total_messages": len(content),
                "user_messages": len(user_messages),
                "assistant_messages": len(assistant_messages)
            }
        
        # Process chunks
        results = chunker.process_conversation_chunks(
            chunk_files, 
            example_processing_function
        )
        
        print("Processing results:")
        for result in results:
            if result:
                print(f"Chunk {result['chunk_id']}: {result['total_messages']} messages")
        
        # Merge chunks back
        output_file = "merged_conversation.json"
        success = chunker.merge_conversation_chunks(chunk_files, output_file)
        
        if success:
            print(f"Successfully merged chunks to {output_file}")
        else:
            print("Failed to merge chunks")
    else:
        print("No chunks were created")

if __name__ == "__main__":
    main()