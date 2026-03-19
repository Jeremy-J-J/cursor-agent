# Large File Processing with Chunking

## Overview

This project includes robust chunking capabilities to handle large files that exceed token limits. The system processes large datasets in smaller, manageable chunks while maintaining data integrity and relationships.

## Key Components

### 1. Chunked Data Processor (`chunked_processor.py`)
- Processes large datasets in configurable batch sizes
- Maintains original field mappings and transformations
- Preserves data structure and relationships
- Configurable batch sizes for different use cases

### 2. Advanced Chunking System (`advanced_chunking.py`)
- Provides multiple chunking strategies:
  - Token-based chunking
  - Sentence-based chunking
  - Paragraph-based chunking
- Supports overlap between chunks to maintain context
- Handles JSON data with structure preservation

### 3. Conversation History Chunker (`conversation_chunker.py`)
- Specialized for processing large conversation history files
- Maintains conversation flow and context
- Handles complex nested structures

## Usage Examples

### Basic Chunked Processing
```python
from chunked_processor import ChunkedDataProcessor

# Create processor with default batch size (1000)
processor = ChunkedDataProcessor()

# Process your dataset
processed_data = processor.process_dataset(
    input_file='large_dataset.json',
    output_file='processed_dataset.json'
)
```

### Custom Batch Size
```python
# Process with custom batch size
processor = ChunkedDataProcessor(batch_size=500)
processed_data = processor.process_dataset(
    input_file='large_dataset.json',
    output_file='processed_dataset.json'
)
```

### Conversation History Processing
```python
from conversation_chunker import ConversationHistoryChunker

# Initialize chunker for conversation history
history_chunker = ConversationHistoryChunker(max_tokens=200000, overlap=1000)

# Chunk a large conversation file
chunk_files = history_chunker.chunk_conversation_history(
    'conversation_history.json',
    './chunked_conversations'
)

# Process each chunk
results = history_chunker.process_conversation_chunks(
    chunk_files, 
    your_processing_function
)
```

## Token Limit Compliance

The default batch size of 1000 records ensures that each processing step stays within the 262,144 token limit while maintaining full functionality. For conversation history files, the system uses a maximum of 200,000 tokens per chunk with 1,000 token overlap to maintain context.

## Implementation Details

### Chunking Strategies
1. **Token-based**: Splits content based on estimated token count
2. **Sentence-based**: Preserves sentence boundaries for natural language processing
3. **Paragraph-based**: Maintains paragraph structure for document processing

### Overlap Strategy
- Maintains context between chunks by overlapping a specified number of tokens
- Ensures that information spanning chunk boundaries is preserved
- Configurable overlap size for different requirements

### Data Preservation
- Maintains all original field mappings and relationships
- Preserves data structure and nested objects
- Supports both simple and complex data structures

## Best Practices

1. **Choose appropriate batch sizes** based on your data complexity and token limits
2. **Use overlap strategically** to maintain context in sequential processing
3. **Monitor chunk statistics** to optimize processing parameters
4. **Test with sample data** before processing large datasets
5. **Implement error handling** for chunk processing failures

## Troubleshooting

### Common Issues
- **Token limit exceeded**: Reduce batch size or use smaller chunking strategies
- **Memory issues**: Process in smaller batches or use streaming approaches
- **Context loss**: Increase overlap settings for better context preservation

### Solutions
- Adjust `max_tokens` and `overlap` parameters in chunking functions
- Implement custom `transform_record` methods for specific data transformations
- Use the `process_conversation_chunks` method for parallel processing of chunks