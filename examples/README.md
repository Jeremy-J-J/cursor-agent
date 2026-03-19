# Chunked Processing Example

This example demonstrates how to implement chunked processing of large text inputs using the agent framework's multi-step capabilities. It shows how to:

1. Break down large documents into manageable chunks
2. Process each chunk through the agent's tool calling system
3. Aggregate the results while maintaining context awareness
4. Handle iterative processing loops
5. Manage conversation history between chunks

## Key Features

- **Chunk Management**: Automatically splits large documents into smaller, manageable pieces
- **Context Preservation**: Maintains document context across chunks for better analysis
- **Tool Integration**: Demonstrates how to use the agent's tool calling capabilities
- **Result Aggregation**: Combines results from all chunks into a comprehensive summary
- **Error Handling**: Gracefully handles processing errors in individual chunks

## How It Works

1. **Document Splitting**: The `ChunkedProcessor` splits large text into chunks based on character limits
2. **Chunk Processing**: Each chunk is processed through the agent with context awareness
3. **Tool Usage**: The agent can utilize registered tools for enhanced processing capabilities
4. **Result Aggregation**: Results from all chunks are combined into a unified output

## Running the Example

```bash
python examples/advanced_chunked_processing_example.py
```

## Key Components

### ChunkedProcessor Class
- Handles the splitting and processing of text chunks
- Manages conversation history between chunks
- Aggregates results from all processed chunks

### Main Processing Flow
1. Split large document into chunks
2. Process each chunk with context awareness
3. Collect and aggregate results
4. Save final results to file

## Use Cases

This pattern is particularly useful for:
- Processing large documents that exceed context window limitations
- Analyzing lengthy technical reports
- Handling large datasets in AI applications
- Implementing scalable text processing pipelines

## Customization

You can customize the example by:
- Adjusting `chunk_size` parameter for different chunk sizes
- Modifying the analysis prompt for different focus areas
- Adding additional tools to the agent for enhanced processing
- Implementing more sophisticated chunking strategies