#!/usr/bin/env python3
"""
Test suite for the chunking functionality to ensure it works correctly.
"""

import json
import os
import tempfile
from chunked_processor import ChunkedDataProcessor
from conversation_chunker import ConversationHistoryChunker

def test_chunked_processor_basic():
    """Test basic chunked processor functionality."""
    # Create sample data
    sample_data = []
    for i in range(1500):  # Create 1500 sample records
        record = {
            "id": i,
            "name": f"Record_{i}",
            "field_1": i * 2,
            "field_2": i * 3,
            "field_3": i * 4,
            "score_1": i % 100,
            "status": "active" if i % 2 == 0 else "inactive"
        }
        sample_data.append(record)
    
    # Create temporary files
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "sample_large_dataset.json")
        output_file = os.path.join(tmpdir, "processed_dataset.json")
        
        # Save sample data
        with open(input_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        # Test chunked processor
        processor = ChunkedDataProcessor(batch_size=100)
        processed_data = processor.process_dataset(input_file, output_file)
        
        # Verify results
        assert len(processed_data) == 1500
        assert os.path.exists(output_file)
        
        print("✅ Basic chunked processor test passed")

def test_conversation_chunker():
    """Test conversation history chunker functionality."""
    # Create sample conversation data
    sample_conversation = [
        {
            "role": "system",
            "content": "System instructions"
        },
        {
            "role": "user",
            "content": "User query 1"
        },
        {
            "role": "assistant",
            "content": "Assistant response 1"
        }
    ]
    
    # Create a larger conversation for testing
    large_conversation = sample_conversation * 1000  # Repeat to make it large
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "sample_conversation.json")
        output_dir = os.path.join(tmpdir, "chunked_conversations")
        
        # Save sample conversation
        with open(input_file, 'w') as f:
            json.dump(large_conversation, f, indent=2)
        
        # Test conversation chunker
        chunker = ConversationHistoryChunker(max_tokens=500, overlap=100)
        chunk_files = chunker.chunk_conversation_history(input_file, output_dir)
        
        # Verify results
        assert len(chunk_files) > 0
        assert os.path.exists(output_dir)
        
        print("✅ Conversation chunker test passed")

def main():
    """Run all tests."""
    print("Running chunking functionality tests...")
    
    try:
        test_chunked_processor_basic()
        test_conversation_chunker()
        print("\n🎉 All tests passed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    main()