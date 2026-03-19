# Chunking Integration Examples

This directory contains comprehensive examples demonstrating how to integrate the ContextWindowChunker and ChunkedProcessor into various workflows.

## Examples Included

1. **JSON Processing Patterns** - Demonstrates handling large JSON datasets
2. **Large Document Processing** - Shows how to process extensive text documents
3. **Conversation History Analysis** - Example for processing conversation logs
4. **API Response Handling** - How to manage large API responses
5. **Log File Processing** - Processing extensive log files efficiently

## Usage Instructions

Each example file can be run independently to demonstrate different integration patterns:

```bash
# Run JSON processing example
python examples/chunking/json_processing_example.py

# Run large document example  
python examples/chunking/large_document_example.py

# Run conversation history example
python examples/chunking/conversation_history_example.py
```

## Integration Patterns

### Pattern 1: JSON Data Processing
```python
from context_window_chunker import ContextWindowChunker

# Process large JSON data while preserving structure
chunker = ContextWindowChunker(max_tokens=200000)
chunks = chunker.process_large_json(large_json_data)
```

### Pattern 2: File Processing with ChunkedProcessor
```python
from chunked_processor import ChunkedProcessor

# Process large files efficiently
processor = ChunkedProcessor(max_tokens=200000)
results = processor.process_large_file(
    file_path="large_file.txt",
    process_function=my_processing_function
)
```

### Pattern 3: Custom Processing Logic
```python
from context_window_chunker import ContextWindowChunker

def custom_processor(chunk_data):
    # Your custom processing logic here
    return processed_content

chunker = ContextWindowChunker(max_tokens=200000)
chunks = chunker.chunk_content(large_content)
processed_results = [custom_processor(chunk) for chunk in chunks]
```