"""
Utility functions for token management and chunking to handle large inputs
within token limits.
"""

import re
from typing import List, Dict, Any, Optional
from collections import deque

# Token estimation constants (approximate)
# These are rough estimates and may need adjustment based on actual tokenization
TOKENS_PER_CHAR = 0.5  # Rough estimate for English text
TOKENS_PER_WORD = 1.3  # Rough estimate for English text

def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    
    Args:
        text: The input text
        
    Returns:
        Estimated number of tokens
    """
    # Simple estimation based on characters and words
    char_tokens = len(text) * TOKENS_PER_CHAR
    word_tokens = len(text.split()) * TOKENS_PER_WORD
    # Use the higher estimate to be safe
    return max(int(char_tokens), int(word_tokens))

def split_text_by_tokens(text: str, max_tokens: int) -> List[str]:
    """
    Split text into chunks that don't exceed the token limit.
    
    Args:
        text: The text to split
        max_tokens: Maximum tokens per chunk
        
    Returns:
        List of text chunks
    """
    if estimate_tokens(text) <= max_tokens:
        return [text]
    
    # Split by sentences first
    sentences = re.split(r'[.!?]+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Add a period back to the sentence if it was removed
        if sentence.strip() and not sentence.strip().endswith('.'):
            sentence += '.'
        
        # Check if adding this sentence would exceed the limit
        if current_chunk and estimate_tokens(current_chunk + " " + sentence) > max_tokens:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
    
    # Add the last chunk if it exists
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def truncate_text_by_tokens(text: str, max_tokens: int, preserve_end: bool = False) -> str:
    """
    Truncate text to fit within token limit.
    
    Args:
        text: The text to truncate
        max_tokens: Maximum tokens allowed
        preserve_end: If True, preserve the end of the text instead of the beginning
        
    Returns:
        Truncated text
    """
    if estimate_tokens(text) <= max_tokens:
        return text
    
    # For simplicity, we'll truncate from the beginning
    # In a more sophisticated implementation, we might want to preserve context
    words = text.split()
    current_tokens = 0
    result_words = []
    
    if preserve_end:
        # Truncate from the beginning to preserve the end
        for word in reversed(words):
            word_tokens = estimate_tokens(word)
            if current_tokens + word_tokens > max_tokens:
                break
            result_words.insert(0, word)
            current_tokens += word_tokens
    else:
        # Truncate from the end to preserve the beginning
        for word in words:
            word_tokens = estimate_tokens(word)
            if current_tokens + word_tokens > max_tokens:
                break
            result_words.append(word)
            current_tokens += word_tokens
    
    return " ".join(result_words)

def chunk_conversation_history(history: List[Dict[str, Any]], max_tokens: int) -> List[Dict[str, Any]]:
    """
    Chunk conversation history to stay within token limits.
    
    Args:
        history: List of conversation messages
        max_tokens: Maximum tokens allowed for the entire history
        
    Returns:
        Chunked conversation history
    """
    # Estimate total tokens in history
    total_tokens = 0
    chunked_history = []
    
    # Process messages in reverse order to preserve recent context
    for message in reversed(history):
        message_tokens = estimate_tokens(str(message))
        
        if total_tokens + message_tokens > max_tokens:
            # If we can't add this message, we stop here
            break
            
        chunked_history.append(message)
        total_tokens += message_tokens
    
    # Reverse back to maintain chronological order
    return list(reversed(chunked_history))

def get_token_count_from_messages(messages: List[Dict[str, Any]]) -> int:
    """
    Calculate total token count from a list of messages.
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Total estimated token count
    """
    total = 0
    for message in messages:
        # Estimate tokens for role and content
        total += estimate_tokens(str(message.get('role', ''))) + estimate_tokens(str(message.get('content', '')))
        # Add tokens for tool calls if present
        if 'tool_calls' in message:
            total += estimate_tokens(str(message['tool_calls']))
    return total

def estimate_tokens_precise(text: str) -> int:
    """
    More precise token estimation using a simple tokenizer approach.
    This is a basic implementation that can be replaced with actual tokenization.
    
    Args:
        text: The input text
        
    Returns:
        Estimated number of tokens
    """
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # For basic estimation, we'll use a combination of word and character counting
    # This is a simplified approach - in production, you'd use a proper tokenizer
    words = text.split()
    if not words:
        return 0
    
    # Estimate based on word count (more accurate for most English text)
    # Each word is roughly 1.3 tokens, but we'll be conservative
    return max(len(words), int(len(text) * 0.4))