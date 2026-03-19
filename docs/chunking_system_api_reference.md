# Chunking System API Reference

This document provides comprehensive API documentation for the ContextWindowChunker and ChunkedProcessor classes, including usage examples and integration patterns.

## Overview

The chunking system provides two main components:
1. **ContextWindowChunker** - Core chunking functionality with multiple strategies
2. **ChunkedProcessor** - High-level processor that handles file loading, chunking, and processing

## ContextWindowChunker API

### Constructor

```python
ContextWindowChunker(max_tokens: int = 200000, overlap: int = 1000, 
                   chunking_strategy: str = 'tokens', min_chunk_size: int = 1000)
```

**Parameters:**
- `max_tokens` (int): Maximum tokens per chunk (default: 200000)
- `overlap` (int): Number of tokens to overlap between chunks (default: 1000)
- `chunking_strategy` (str): Strategy to use ('tokens', 'sentences', 'paragraphs')
- `min_chunk_size` (int): Minimum chunk size in characters to avoid overly small chunks

### Methods

#### `chunk_content(content: Union[str, Dict, List], preserve_structure: bool = True) -> List[Dict[str, Any]]`

Chunk content based on the specified strategy.

**Parameters:**
- `content`: Content to chunk (string, dict, or list)
- `preserve_structure`: Whether to preserve original structure

**Returns:**
List of chunk dictionaries with metadata including:
- `chunk_id`: Unique identifier for the chunk
- `content`: The actual chunk content
- `token_count`: Estimated token count
- `chunk_size`: Character length of chunk
- `strategy`: Chunking strategy used
- `overlap_tokens`: Overlap size in tokens
- `needs_processing`: Whether this chunk requires further processing

#### `process_large_json(json_data: Union[str, Dict], max_tokens: Optional[int] = None) -> List[Dict[str, Any]]`

Process large JSON data by chunking it appropriately.

**Parameters:**
- `json_data`: JSON data to process (string or dict)
- `max_tokens`: Override max_tokens parameter

**Returns:**
List of chunked JSON data with metadata

#### `merge_chunks(chunks: List[Dict[str, Any]], preserve_order: bool = True) -> str`

Merge chunks back into a single string.

**Parameters:**
- `chunks`: List of chunk dictionaries
- `preserve_order`: Whether to preserve the original order

**Returns:**
Merged content as string

#### `get_chunk_statistics(chunks: List[Dict[str, Any]]) -> Dict[str, Any]`

Get statistics about the chunked content.

**Parameters:**
- `chunks`: List of chunk dictionaries

**Returns:**
Dictionary with statistics:
- `total_chunks`: Total number of chunks
- `total_tokens`: Total token count across all chunks
- `total_size`: Total character size
- `avg_tokens_per_chunk`: Average tokens per chunk
- `max_tokens_in_chunk`: Maximum tokens in any single chunk
- `min_tokens_in_chunk`: Minimum tokens in any single chunk

## ChunkedProcessor API

### Constructor

```python
ChunkedProcessor(max_tokens: int = 200000, overlap: int = 1000, 
                chunking_strategy: str = 'tokens')
```

**Parameters:**
- `max_tokens` (int): Maximum tokens per chunk (default: 200000)
- `overlap` (int): Number of tokens to overlap between chunks (default: 1000)
- `chunking_strategy` (str): Strategy to use ('tokens', 'sentences', 'paragraphs')

### Methods

#### `load_content(file_path: str) -> str`

Load content from a file.

**Parameters:**
- `file_path`: Path to the file to load

**Returns:**
Content as string

#### `chunk_content(content: str, preserve_structure: bool = True) -> List[Dict[str, Any]]`

Chunk content using the specified strategy.

**Parameters:**
- `content`: Content to chunk
- `preserve_structure`: Whether to preserve original structure

**Returns:**
List of chunk dictionaries with metadata

#### `process_chunks(chunks: List[Dict[str, Any]], process_function: Callable[[Dict[str, Any]], Any], max_concurrent: int = 1) -> List[Any]`

Process chunks using a provided processing function.

**Parameters:**
- `chunks`: List of chunk dictionaries
- `process_function`: Function to process each chunk
- `max_concurrent`: Maximum number of concurrent processes (default: 1)

**Returns:**
List of results from processing each chunk

#### `merge_chunks(chunks: List[Dict[str, Any]], preserve_order: bool = True) -> str`

Merge chunks back into a single string.

**Parameters:**
- `chunks`: List of chunk dictionaries
- `preserve_order`: Whether to preserve the original order

**Returns:**
Merged content as string

#### `get_chunk_statistics(chunks: List[Dict[str, Any]]) -> Dict[str, Any]`

Get statistics about the chunked content.

**Parameters:**
- `chunks`: List of chunk dictionaries

**Returns:**
Dictionary with statistics

#### `process_large_file(file_path: str, process_function: Callable[[Dict[str, Any]], Any], output_dir: str = "./chunked_output") -> List[Any]`

Process a large file by chunking it appropriately.

**Parameters:**
- `file_path`: Path to the large file to process
- `process_function`: Function to process each chunk
- `output_dir`: Directory to save intermediate results

**Returns:**
List of results from processing each chunk

## Usage Examples

### Basic Usage Example

```python
from context_window_chunker import ContextWindowChunker
from chunked_processor import ChunkedProcessor

# Initialize the chunker
chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)

# Sample large content
large_content = "Your very large content here..." * 1000

# Chunk the content
chunks = chunker.chunk_content(large_content)

# Print chunk statistics
stats = chunker.get_chunk_statistics(chunks)
print(f"Total chunks: {stats['total_chunks']}")
print(f"Average tokens per chunk: {stats['avg_tokens_per_chunk']}")
```

### JSON Processing Example

```python
from context_window_chunker import ContextWindowChunker

# Initialize the chunker
chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)

# Sample large JSON data
large_json = {
    "users": [
        {"id": i, "name": f"User {i}", "email": f"user{i}@example.com"} 
        for i in range(1000)
    ]
}

# Process JSON data
chunks = chunker.process_large_json(large_json)

# Print chunk information
for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']}: {chunk['token_count']} tokens")
```

### File Processing Example

```python
from chunked_processor import ChunkedProcessor

def process_chunk(chunk_data):
    """Example processing function for chunks"""
    # Your processing logic here
    return f"Processed chunk {chunk_data['chunk_id']} with {chunk_data['token_count']} tokens"

# Initialize the processor
processor = ChunkedProcessor(max_tokens=200000, overlap=1000)

# Process a large file
results = processor.process_large_file(
    file_path="large_conversation.txt",
    process_function=process_chunk
)

print(f"Processed {len(results)} chunks successfully")
```

### Integration Patterns

#### Pattern 1: Simple Text Processing

```python
from context_window_chunker import ContextWindowChunker

def simple_text_processor(text):
    """Process text in chunks"""
    chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)
    
    # Chunk the text
    chunks = chunker.chunk_content(text)
    
    # Process each chunk
    processed_chunks = []
    for chunk in chunks:
        # Your processing logic here
        processed_chunk = chunk['content'].upper()  # Example transformation
        processed_chunks.append(processed_chunk)
    
    # Merge results back
    return chunker.merge_chunks([
        {'chunk_id': i, 'content': chunk} 
        for i, chunk in enumerate(processed_chunks)
    ])

# Usage
result = simple_text_processor("Very large text content...")
```

#### Pattern 2: JSON Data Processing

```python
from context_window_chunker import ContextWindowChunker

def json_data_processor(json_data):
    """Process large JSON data in chunks"""
    chunker = ContextWindowChunker(max_tokens=200000, overlap=1000)
    
    # Process JSON data
    chunks = chunker.process_large_json(json_data)
    
    # Process each chunk
    processed_chunks = []
    for chunk in chunks:
        # Your JSON processing logic here
        processed_chunk = {
            "processed": True,
            "original_tokens": chunk['token_count'],
            "chunk_id": chunk['chunk_id']
        }
        processed_chunks.append(processed_chunk)
    
    return processed_chunks

# Usage
large_json = {"data": [{"id": i, "value": f"item_{i}"} for i in range(1000)]}
result = json_data_processor(large_json)
```

#### Pattern 3: Large Document Handling

```python
from chunked_processor import ChunkedProcessor

def large_document_handler(file_path):
    """Handle large document processing"""
    
    def document_processor(chunk_data):
        """Process individual document chunks"""
        # Example: Extract key information from each chunk
        content = chunk_data['content']
        token_count = chunk_data['token_count']
        
        # Your document processing logic here
        return {
            "chunk_id": chunk_data['chunk_id'],
            "token_count": token_count,
            "summary": f"Processed chunk with {token_count} tokens"
        }
    
    # Initialize processor
    processor = ChunkedProcessor(max_tokens=200000, overlap=1000)
    
    # Process the document
    results = processor.process_large_file(
        file_path=file_path,
        process_function=document_processor
    )
    
    return results

# Usage
results = large_document_handler("large_document.txt")
```

## Best Practices

1. **Choose the Right Strategy**: 
   - Use 'tokens' for general text processing
   - Use 'sentences' for preserving sentence boundaries
   - Use 'paragraphs' for maintaining paragraph structure

2. **Optimize Overlap**: 
   - Set overlap to 1000-2000 tokens for good context preservation
   - Adjust based on your specific use case

3. **Handle Large JSON**: 
   - Use `process_large_json()` method for JSON data to preserve structure
   - Consider splitting by top-level keys or array elements

4. **Monitor Token Usage**: 
   - Always check chunk statistics to ensure proper sizing
   - Verify that chunks stay within the 262,144 token limit

5. **Error Handling**: 
   - Implement proper error handling for file operations
   - Handle cases where content cannot be processed due to size limits

## Performance Tips

1. **Caching**: Enable caching for repeated operations to improve performance
2. **Parallel Processing**: Use `max_concurrent` parameter for parallel processing when appropriate
3. **Memory Management**: Process chunks sequentially for memory-constrained environments
4. **Chunk Size Optimization**: Adjust `max_tokens` based on your specific model's capabilities

## Common Use Cases

1. **Conversation History Processing**: Breaking down large conversation logs
2. **Document Analysis**: Processing large documents for analysis
3. **Data Migration**: Handling large datasets that exceed context limits
4. **API Response Processing**: Managing large API responses
5. **Log File Analysis**: Processing extensive log files