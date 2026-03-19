#!/usr/bin/env python3
"""
Script to analyze the conversation history file structure and size.
"""

import json
import os
from typing import Dict, Any

def analyze_conversation_file(file_path: str) -> Dict[str, Any]:
    """
    Analyze the structure and size of a conversation history file.
    
    Args:
        file_path (str): Path to the conversation history file
        
    Returns:
        Dict[str, Any]: Analysis results
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    
    # Load the conversation
    with open(file_path, 'r', encoding='utf-8') as f:
        conversation = json.load(f)
    
    # Basic statistics
    total_messages = len(conversation)
    
    # Count message types
    message_types = {}
    for msg in conversation:
        role = msg.get('role', 'unknown')
        message_types[role] = message_types.get(role, 0) + 1
    
    # Estimate token count (rough approximation)
    total_chars = sum(len(str(msg)) for msg in conversation)
    estimated_tokens = total_chars // 4  # Rough estimate: 1 token ~ 4 characters
    
    # Analyze content length distribution
    content_lengths = [len(str(msg)) for msg in conversation]
    avg_content_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0
    
    return {
        'file_path': file_path,
        'total_messages': total_messages,
        'message_types': message_types,
        'total_characters': total_chars,
        'estimated_tokens': estimated_tokens,
        'average_message_length': avg_content_length,
        'largest_message': max(content_lengths) if content_lengths else 0,
        'smallest_message': min(content_lengths) if content_lengths else 0
    }

def main():
    """Main function to analyze conversation file."""
    
    file_path = "conversation_history.json"
    
    try:
        analysis = analyze_conversation_file(file_path)
        
        print("=== CONVERSATION FILE ANALYSIS ===")
        print(f"File: {analysis['file_path']}")
        print(f"Total Messages: {analysis['total_messages']}")
        print(f"Total Characters: {analysis['total_characters']}")
        print(f"Estimated Tokens: {analysis['estimated_tokens']}")
        print(f"Average Message Length: {analysis['average_message_length']:.2f}")
        print(f"Largest Message: {analysis['largest_message']}")
        print(f"Smallest Message: {analysis['smallest_message']}")
        
        print("\nMessage Type Distribution:")
        for msg_type, count in analysis['message_types'].items():
            print(f"  {msg_type}: {count}")
            
        print(f"\nRecommendation: This file contains {analysis['estimated_tokens']} tokens.")
        if analysis['estimated_tokens'] > 262144:
            print("⚠️  This exceeds the 262,144 token limit. Chunking is required.")
        else:
            print("✅ This file is within the token limit.")
            
    except Exception as e:
        print(f"Error analyzing conversation file: {e}")

if __name__ == "__main__":
    main()