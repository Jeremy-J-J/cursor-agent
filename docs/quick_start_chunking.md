# Quick Start Guide: Chunking System

This guide provides a fast way to get started with the chunking system.

## Prerequisites

Make sure you have Python 3.7+ installed and the required packages:

```bash
pip install -r requirements.txt
```

## Quick Usage Examples

### 1. Basic Text Chunking

```python
from context_window_chunker import ContextWindowChunker

# Create a large text
large_text = "This is sample text that will be chunked. " * 10000

# Initialize chunker
chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)

# Chunk the text
chunks = chunker.chunk_content(large_text)

print(f"Created {len(chunks)} chunks")
print(f"Average tokens per chunk: {chunker.get_chunk_statistics(chunks)['avg_tokens_per_chunk']:.2f}")
```

### 2. JSON Data Processing

```python
from context_window_chunker import ContextWindowChunker

# Create large JSON data
large_json = {
    "items": [{"id": i, "name": f"Item {i}"} for i in range(1000)]
}

# Initialize chunker
chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)

# Process JSON data
chunks = chunker.process_large_json(large_json)

print(f"Created {len(chunks)} JSON chunks")
```

### 3. File Processing

```python
from chunked_processor import ChunkedProcessor

def process_chunk(chunk_data):
    """Process each chunk"""
    return {
        "chunk_id": chunk_data['chunk_id'],
        "token_count": chunk_data['token_count'],
        "processed": True
    }

# Initialize processor
processor = ChunkedProcessor(max_tokens=200000, overlap=1000)

# Process a large file
results = processor.process_large_file(
    file_path="large_file.txt",
    process_function=process_chunk
)

print(f"Processed {len(results)} chunks")
```

## Running Examples

You can run the provided examples directly:

```bash
# Run simple usage example
python examples/chunking/simple_usage_example.py

# Run JSON processing example  
python examples/chunking/json_processing_example.py

# Run large document example
python examples/chunking/large_document_example.py

# Run conversation history example
python examples/chunking/conversation_history_example.py
```

## Key Parameters

- `max_tokens`: Maximum tokens per chunk (default: 200000)
- `overlap`: Tokens to overlap between chunks (default: 1000) 
- `chunking_strategy`: 'tokens', 'sentences', or 'paragraphs'

## Best Practices

1. **Choose appropriate strategies** based on your content type
2. **Monitor chunk sizes** to ensure they stay within limits
3. **Use overlap wisely** to maintain context without excessive redundancy
4. **Test with realistic data sizes** to validate performance

## Troubleshooting

If you encounter issues:

1. Check that your content exceeds the token limit
2. Verify that `max_tokens` is set appropriately
3. Ensure you're using the correct chunking strategy for your data type
4. Review the chunk statistics to understand the distribution

For more detailed information, refer to the [API Reference Documentation](./docs/chunking_system_api_reference.md).