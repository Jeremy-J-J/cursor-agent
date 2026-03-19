#!/usr/bin/env python3
"""
Example demonstrating chunked processing of large text inputs using the agent framework.
This shows how to break down large documents into manageable chunks, process each chunk
through the agent's tool calling system, and aggregate the results while maintaining
context awareness.
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from cursor_agent_tools import OpenAIAgent
from cursor_agent_tools.tools import register_default_tools
from cursor_agent_tools.base import AgentResponse

# Sample large document to process
LARGE_DOCUMENT = """
# Technical Report: AI System Performance Analysis

## Executive Summary

The implementation of the AI system has shown significant improvements in processing efficiency and accuracy. This report outlines the key findings from the performance analysis conducted over the past quarter.

## System Architecture Overview

The system architecture consists of three main components:
1. Data ingestion layer
2. Processing engine
3. Output generation module

Each component plays a crucial role in the overall performance of the system.

## Performance Metrics

### Processing Speed
The system processes 10,000 documents per hour with an average response time of 2.3 seconds per document.

### Accuracy Rate
The accuracy rate for document classification is 94.7%, with a false positive rate of 2.1%.

### Resource Utilization
CPU utilization averages 65% during peak hours, with memory usage at 42% of total capacity.

## Detailed Analysis

### Data Ingestion Layer
The data ingestion layer handles incoming documents from multiple sources including:
- Web APIs
- Database connections
- File uploads
- Real-time streaming

This layer is designed to handle up to 500 concurrent connections with minimal latency.

### Processing Engine
The processing engine performs the core analysis tasks:
- Natural language processing
- Pattern recognition
- Data validation
- Quality assurance checks

The engine uses advanced algorithms to ensure consistent performance across all document types.

### Output Generation Module
The output generation module formats results for various stakeholders:
- Technical reports
- Executive summaries
- Data visualizations
- API responses

## Challenges Encountered

### Scalability Issues
During the initial deployment, we encountered scalability challenges with the database connection pool. This was resolved by implementing connection pooling and optimizing query performance.

### Memory Management
The system required significant memory optimization to handle large documents. We implemented streaming processing to reduce memory footprint.

### Latency Concerns
Initial latency was higher than expected due to inefficient data processing pipelines. This was addressed through algorithm optimization and parallel processing improvements.

## Recommendations

### Immediate Actions
1. Implement automated scaling for the processing engine
2. Add additional monitoring for resource utilization
3. Optimize database queries for better performance

### Long-term Improvements
1. Integrate machine learning models for predictive scaling
2. Develop advanced caching mechanisms
3. Implement distributed processing for very large documents

## Conclusion

The AI system has demonstrated strong performance capabilities and is ready for production deployment. Continued monitoring and optimization will ensure sustained performance improvements.

## Appendices

### Appendix A: Technical Specifications
- Supported file formats: PDF, DOCX, TXT, CSV
- Maximum document size: 100MB
- Processing time per document: 1-5 seconds
- Supported languages: English, Spanish, French, German

### Appendix B: Performance Benchmarks
- Throughput: 10,000 documents/hour
- Accuracy: 94.7%
- Availability: 99.9%
- Response time: < 3 seconds

### Appendix C: Future Enhancements
- Multi-language support expansion
- Real-time processing capabilities
- Enhanced analytics dashboard
- Integration with third-party services

## References

1. Smith, J. (2023). "Advanced AI Processing Techniques". Journal of Artificial Intelligence, 45(3), 123-145.
2. Johnson, A. (2023). "Scalable System Design". Systems Engineering Review, 22(2), 67-89.
3. Brown, M. (2023). "Performance Optimization Strategies". Computing Performance Journal, 18(4), 201-220.

## Acknowledgments

We would like to thank the development team for their dedication and the stakeholders for their continued support throughout this project.
"""

class ChunkedProcessor:
    """Handles chunked processing of large text inputs using the agent framework."""
    
    def __init__(self, agent: OpenAIAgent, chunk_size: int = 1000):
        """
        Initialize the chunked processor.
        
        Args:
            agent: The agent to use for processing chunks
            chunk_size: Maximum characters per chunk (default: 1000)
        """
        self.agent = agent
        self.chunk_size = chunk_size
        self.processed_chunks = []
        self.conversation_history = []
        
    def _split_text_into_chunks(self, text: str) -> List[str]:
        """
        Split text into chunks of specified size.
        
        Args:
            text: The text to split into chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        # Simple approach: split by sentences or by character limit
        if len(text) <= self.chunk_size:
            return [text]
            
        # Split by paragraphs first for better context preservation
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If paragraph is larger than chunk size, split it
            if len(paragraph) > self.chunk_size:
                # Split paragraph into smaller chunks
                words = paragraph.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk) + len(word) + 1 <= self.chunk_size:
                        temp_chunk += (word + " ")
                    else:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = word + " "
                if temp_chunk:
                    chunks.append(temp_chunk.strip())
            else:
                # Add paragraph to current chunk if it fits
                if len(current_chunk) + len(paragraph) + 2 <= self.chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph + "\n\n"
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    async def process_chunk(self, chunk: str, chunk_index: int, total_chunks: int) -> Dict[str, Any]:
        """
        Process a single chunk through the agent.
        
        Args:
            chunk: The text chunk to process
            chunk_index: Index of this chunk in the sequence
            total_chunks: Total number of chunks
            
        Returns:
            Dictionary containing the processing results
        """
        # Create a context-aware prompt for this chunk
        context_prompt = f"""
        You are analyzing a specific section of a technical document. 
        This is chunk {chunk_index + 1} of {total_chunks} total chunks.
        
        The full document context is: {self._get_document_context()}
        
        Please analyze the following section:
        {chunk}
        
        Your task is to extract key information from this section, including:
        1. Main topics discussed
        2. Key findings or metrics mentioned
        3. Any recommendations or conclusions
        4. Important technical details
        
        Format your response as JSON with the following structure:
        {{
            "chunk_index": {chunk_index},
            "topics": ["topic1", "topic2", ...],
            "findings": ["finding1", "finding2", ...],
            "recommendations": ["recommendation1", "recommendation2", ...],
            "technical_details": ["detail1", "detail2", ...]
        }}
        """
        
        try:
            # Process the chunk with the agent
            response = await self.agent.run(context_prompt)
            
            # Extract the JSON response
            result = self._extract_json_from_response(response)
            
            # Store the result
            self.processed_chunks.append({
                "chunk_index": chunk_index,
                "chunk": chunk,
                "result": result
            })
            
            return result
            
        except Exception as e:
            print(f"Error processing chunk {chunk_index}: {e}")
            return {
                "chunk_index": chunk_index,
                "error": str(e),
                "topics": [],
                "findings": [],
                "recommendations": [],
                "technical_details": []
            }
    
    def _get_document_context(self) -> str:
        """Get a summary of the overall document context."""
        # For this example, we'll create a simple context summary
        return "Technical report analyzing AI system performance with sections on architecture, metrics, challenges, and recommendations."
    
    def _extract_json_from_response(self, response: AgentResponse) -> Dict[str, Any]:
        """
        Extract JSON from agent response.
        
        Args:
            response: The agent response
            
        Returns:
            Dictionary with extracted JSON data
        """
        # In a real implementation, this would parse the actual JSON from the response
        # For this example, we'll return a mock response
        return {
            "chunk_index": 0,
            "topics": ["system architecture", "performance metrics", "challenges"],
            "findings": ["94.7% accuracy rate", "10,000 documents/hour processing"],
            "recommendations": ["implement automated scaling", "add monitoring"],
            "technical_details": ["CPU utilization 65%", "memory usage 42%"]
        }
    
    async def process_document(self, document: str) -> Dict[str, Any]:
        """
        Process an entire document by splitting it into chunks and processing each.
        
        Args:
            document: The document text to process
            
        Returns:
            Aggregated results from all chunks
        """
        print(f"Starting processing of document with {len(document)} characters")
        
        # Split document into chunks
        chunks = self._split_text_into_chunks(document)
        print(f"Split into {len(chunks)} chunks")
        
        # Process each chunk
        tasks = []
        for i, chunk in enumerate(chunks):
            task = self.process_chunk(chunk, i, len(chunks))
            tasks.append(task)
        
        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        aggregated_results = self._aggregate_results(results)
        
        return aggregated_results
    
    def _aggregate_results(self, results: List[Any]) -> Dict[str, Any]:
        """
        Aggregate results from all chunks.
        
        Args:
            results: List of results from chunk processing
            
        Returns:
            Aggregated results dictionary
        """
        # Initialize aggregated results
        aggregated = {
            "total_chunks": len(results),
            "topics": set(),
            "findings": set(),
            "recommendations": set(),
            "technical_details": set(),
            "chunk_details": []
        }
        
        # Process each result
        for result in results:
            if isinstance(result, Exception):
                print(f"Error in processing: {result}")
                continue
                
            if isinstance(result, dict):
                # Add topics
                for topic in result.get("topics", []):
                    aggregated["topics"].add(topic)
                
                # Add findings
                for finding in result.get("findings", []):
                    aggregated["findings"].add(finding)
                
                # Add recommendations
                for recommendation in result.get("recommendations", []):
                    aggregated["recommendations"].add(recommendation)
                
                # Add technical details
                for detail in result.get("technical_details", []):
                    aggregated["technical_details"].add(detail)
                
                # Store chunk details
                aggregated["chunk_details"].append(result)
        
        # Convert sets to lists for JSON serialization
        aggregated["topics"] = list(aggregated["topics"])
        aggregated["findings"] = list(aggregated["findings"])
        aggregated["recommendations"] = list(aggregated["recommendations"])
        aggregated["technical_details"] = list(aggregated["technical_details"])
        
        return aggregated

async def main():
    """Main function to demonstrate chunked processing."""
    print("=== Chunked Processing Example ===")
    
    # Initialize the agent (using a dummy key for this example)
    # In a real scenario, you would use a valid API key
    agent = OpenAIAgent(
        api_key="dummy-key",
        model="gpt-4-turbo",
        temperature=0.0
    )
    
    # Register default tools
    register_default_tools(agent)
    
    # Create the chunked processor
    processor = ChunkedProcessor(agent, chunk_size=500)
    
    # Process the large document
    print("Processing large document...")
    results = await processor.process_document(LARGE_DOCUMENT)
    
    # Display results
    print("\n=== Processing Results ===")
    print(f"Total chunks processed: {results['total_chunks']}")
    print(f"Topics identified: {', '.join(results['topics'])}")
    print(f"Key findings: {', '.join(results['findings'])}")
    print(f"Recommendations: {', '.join(results['recommendations'])}")
    print(f"Technical details: {', '.join(results['technical_details'])}")
    
    # Show detailed chunk information
    print("\n=== Chunk Details ===")
    for chunk_detail in results['chunk_details'][:3]:  # Show first 3 chunks
        print(f"Chunk {chunk_detail['chunk_index'] + 1}:")
        print(f"  Topics: {', '.join(chunk_detail['topics'])}")
        print(f"  Findings: {', '.join(chunk_detail['findings'])}")
        print()

if __name__ == "__main__":
    asyncio.run(main())