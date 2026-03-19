# Scripts for Large File Processing

This directory contains scripts for processing large files using the chunking approach to handle token limits.

## Available Scripts

### `process_large_conversation.py`
Demonstrates how to process large conversation history files using chunking techniques.

## Usage

1. Make sure you have the required dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the conversation processing script:
   ```bash
   python process_large_conversation.py
   ```

## Features

- **Chunking**: Splits large files into smaller, manageable pieces
- **Context Preservation**: Maintains conversation flow with overlap between chunks
- **Flexible Processing**: Supports custom processing functions for each chunk
- **Merge Capability**: Combines processed chunks back into a single file

## Configuration

The chunking parameters can be adjusted in the script:
- `max_tokens`: Maximum tokens per chunk (default: 200,000)
- `overlap`: Number of tokens to overlap between chunks (default: 1,000)

## Best Practices

1. **Monitor token usage**: Keep chunks within the token limit
2. **Preserve context**: Use appropriate overlap settings
3. **Test with samples**: Verify processing logic with smaller datasets first
4. **Handle errors gracefully**: Implement proper error handling for chunk processing