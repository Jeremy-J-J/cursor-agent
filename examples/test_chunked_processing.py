#!/usr/bin/env python3
"""
Test script for the chunked processing example.
"""

import asyncio
import os
import sys

# Add the project root to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from examples.advanced_chunked_processing_example import ChunkedProcessor, LARGE_DOCUMENT
from cursor_agent_tools import OpenAIAgent

def test_chunking():
    """Test that the document is properly chunked."""
    print("Testing chunking functionality...")
    
    # Create a simple agent for testing
    agent = OpenAIAgent(
        api_key="dummy-key",
        model="gpt-4-turbo",
        temperature=0.0
    )
    
    # Create processor
    processor = ChunkedProcessor(agent, chunk_size=500)
    
    # Split document
    chunks = processor._split_text_into_chunks(LARGE_DOCUMENT)
    
    print(f"Original document: {len(LARGE_DOCUMENT)} characters")
    print(f"Number of chunks: {len(chunks)}")
    
    # Verify all chunks are within size limits
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {len(chunk)} characters")
        assert len(chunk) <= 500, f"Chunk {i+1} exceeds size limit"
    
    print("✓ All chunks are within size limits")
    return True

def test_result_aggregation():
    """Test that results are properly aggregated."""
    print("\nTesting result aggregation...")
    
    # Mock results to test aggregation
    mock_results = [
        {
            "chunk_index": 0,
            "topics": ["topic1", "topic2"],
            "findings": ["finding1"],
            "recommendations": ["recommendation1"],
            "technical_details": ["detail1"]
        },
        {
            "chunk_index": 1,
            "topics": ["topic2", "topic3"],
            "findings": ["finding2", "finding3"],
            "recommendations": ["recommendation2"],
            "technical_details": ["detail2", "detail3"]
        }
    ]
    
    # Create a simple processor to test aggregation
    agent = OpenAIAgent(
        api_key="dummy-key",
        model="gpt-4-turbo",
        temperature=0.0
    )
    
    processor = ChunkedProcessor(agent, chunk_size=500)
    aggregated = processor._aggregate_results(mock_results)
    
    # Check that aggregation works correctly
    assert len(aggregated["topics"]) == 3  # topic1, topic2, topic3
    assert len(aggregated["findings"]) == 3  # finding1, finding2, finding3
    assert len(aggregated["recommendations"]) == 2  # recommendation1, recommendation2
    assert len(aggregated["technical_details"]) == 3  # detail1, detail2, detail3
    
    print("✓ Results properly aggregated")
    return True

async def main():
    """Run all tests."""
    print("Running chunked processing tests...\n")
    
    try:
        test_chunking()
        test_result_aggregation()
        print("\n✓ All tests passed!")
        return True
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)