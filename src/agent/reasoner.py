"""
Agent Reasoner Module
Implements reasoning and self-reflection capabilities for the agent.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class AgentReasoner:
    """
    Handles agent reasoning, self-reflection, and decision-making.
    """
    
    def __init__(self, llm_provider=None):
        """
        Initialize the reasoner.
        
        Args:
            llm_provider: LLM provider instance for generating reflections
        """
        self.llm_provider = llm_provider
        self.reasoning_history = []
        
    def reason_about_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reason about a user query and determine the best approach.
        
        Args:
            query: User's question or request
            context: Available context (retrieved documents, etc.)
            
        Returns:
            Dictionary with reasoning results and recommended actions
        """
        reasoning = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "query_type": self._classify_query(query),
            "required_tools": [],
            "confidence": 0.0,
            "reasoning_chain": []
        }
        
        # Step 1: Classify the query
        query_type = reasoning["query_type"]
        reasoning["reasoning_chain"].append(f"Query classified as: {query_type}")
        
        # Step 2: Determine required tools
        required_tools = self._determine_required_tools(query, query_type)
        reasoning["required_tools"] = required_tools
        reasoning["reasoning_chain"].append(f"Required tools: {', '.join(required_tools)}")
        
        # Step 3: Check if we have sufficient context
        has_context = bool(context.get("retrieved_docs"))
        if has_context:
            reasoning["reasoning_chain"].append(f"Retrieved {len(context.get('retrieved_docs', []))} relevant documents")
        else:
            reasoning["reasoning_chain"].append("No context retrieved - may need tool execution")
        
        # Step 4: Estimate confidence
        reasoning["confidence"] = self._estimate_confidence(query_type, has_context, required_tools)
        reasoning["reasoning_chain"].append(f"Confidence level: {reasoning['confidence']:.2f}")
        
        # Store reasoning
        self.reasoning_history.append(reasoning)
        
        return reasoning
    
    def reflect_on_response(self, 
                          query: str, 
                          response: str, 
                          retrieved_context: List[Dict],
                          tool_results: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Reflect on the generated response and assess its quality.
        
        Args:
            query: Original user query
            response: Generated response
            retrieved_context: Documents that were retrieved
            tool_results: Results from any tools that were called
            
        Returns:
            Dictionary with reflection analysis
        """
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "quality_score": 0.0,
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "should_regenerate": False
        }
        
        # Check response completeness
        if len(response) < 50:
            reflection["weaknesses"].append("Response seems too short")
            reflection["quality_score"] -= 0.2
        else:
            reflection["strengths"].append("Response has adequate length")
            reflection["quality_score"] += 0.2
        
        # Check if response addresses the query
        query_keywords = set(query.lower().split())
        response_keywords = set(response.lower().split())
        overlap = len(query_keywords & response_keywords)
        
        if overlap >= len(query_keywords) * 0.3:
            reflection["strengths"].append("Response addresses query keywords")
            reflection["quality_score"] += 0.3
        else:
            reflection["weaknesses"].append("Response may not fully address the query")
            reflection["quality_score"] -= 0.2
        
        # Check if context was used
        if retrieved_context:
            reflection["strengths"].append(f"Used {len(retrieved_context)} context documents")
            reflection["quality_score"] += 0.2
        else:
            reflection["weaknesses"].append("No context was retrieved")
            reflection["suggestions"].append("Consider broadening search parameters")
        
        # Check if tools were used when needed
        if tool_results:
            reflection["strengths"].append(f"Successfully used {len(tool_results)} tools")
            reflection["quality_score"] += 0.3
        
        # Normalize quality score to 0-1 range
        reflection["quality_score"] = max(0.0, min(1.0, 0.5 + reflection["quality_score"]))
        
        # Decide if regeneration is needed
        if reflection["quality_score"] < 0.4:
            reflection["should_regenerate"] = True
            reflection["suggestions"].append("Consider regenerating with different parameters")
        
        return reflection
    
    def generate_reflection_prompt(self, query: str, response: str, context: str) -> str:
        """
        Generate a prompt for LLM-based self-reflection.
        
        Args:
            query: Original query
            response: Generated response
            context: Retrieved context
            
        Returns:
            Reflection prompt string
        """
        prompt = f"""You are reflecting on your own response. Analyze it critically.

QUERY: {query}

YOUR RESPONSE: {response}

CONTEXT USED: {context[:500]}...

Please reflect on:
1. Does the response fully answer the query?
2. Is the response accurate based on the context?
3. What could be improved?
4. Rate your confidence (1-10) in this response.

Provide a brief reflection (2-3 sentences) and a confidence score.
"""
        return prompt
    
    def perform_llm_reflection(self, query: str, response: str, context: str) -> Dict[str, Any]:
        """
        Use the LLM to reflect on its own response.
        
        Args:
            query: Original query
            response: Generated response  
            context: Retrieved context
            
        Returns:
            Dictionary with LLM reflection results
        """
        if not self.llm_provider:
            return {
                "reflection": "LLM reflection not available (no LLM provider)",
                "confidence": 0.5
            }
        
        reflection_prompt = self.generate_reflection_prompt(query, response, context)
        
        try:
            # LLM providers expect (query, context) parameters
            # Pass the reflection prompt as query with empty context
            llm_reflection = self.llm_provider.generate(
                query=reflection_prompt,
                context=""
            )
            
            # Parse confidence from reflection
            confidence = self._extract_confidence(llm_reflection)
            
            return {
                "reflection": llm_reflection,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "reflection": f"Reflection failed: {str(e)}",
                "confidence": 0.0
            }
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of query."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["analyze", "examine", "inspect", "review"]):
            return "analysis"
        elif any(word in query_lower for word in ["create", "generate", "make", "build"]):
            return "generation"
        elif any(word in query_lower for word in ["what", "how", "why", "explain"]):
            return "information"
        elif any(word in query_lower for word in ["summarize", "summary", "overview"]):
            return "summarization"
        else:
            return "general"
    
    def _determine_required_tools(self, query: str, query_type: str) -> List[str]:
        """Determine which tools are needed for this query."""
        tools = []
        query_lower = query.lower()
        
        if "code" in query_lower or "analyze" in query_lower:
            tools.append("analyze_code")
        
        if "document" in query_lower or "readme" in query_lower:
            tools.append("generate_documentation")
        
        if "post" in query_lower or "linkedin" in query_lower or "social" in query_lower:
            tools.append("create_linkedin_post")
        
        if "architecture" in query_lower or "design" in query_lower:
            tools.append("analyze_architecture")
        
        if "stats" in query_lower or "statistics" in query_lower or "count" in query_lower:
            tools.append("get_project_stats")
        
        # Default to RAG search if no specific tools identified
        if not tools and query_type == "information":
            tools.append("rag_search")
        
        return tools
    
    def _estimate_confidence(self, query_type: str, has_context: bool, required_tools: List[str]) -> float:
        """Estimate confidence in handling this query."""
        confidence = 0.5  # Base confidence
        
        # Boost confidence if we have context
        if has_context:
            confidence += 0.2
        
        # Boost confidence if we know which tools to use
        if required_tools:
            confidence += 0.2
        
        # Adjust based on query type complexity
        if query_type in ["information", "summarization"]:
            confidence += 0.1
        elif query_type in ["analysis", "generation"]:
            confidence += 0.0  # Neutral for complex tasks
        
        return min(1.0, confidence)
    
    def _extract_confidence(self, reflection_text: str) -> float:
        """Extract confidence score from reflection text."""
        try:
            # Look for patterns like "confidence: 8/10" or "8 out of 10"
            import re
            patterns = [
                r'confidence[:\s]+(\d+)[/\s]',
                r'(\d+)\s*[/out of]+\s*10',
                r'score[:\s]+(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, reflection_text.lower())
                if match:
                    score = int(match.group(1))
                    return score / 10.0
            
            return 0.5  # Default if no confidence found
        except:
            return 0.5
    
    def get_reasoning_summary(self) -> Dict[str, Any]:
        """Get a summary of all reasoning performed."""
        return {
            "total_queries_reasoned": len(self.reasoning_history),
            "avg_confidence": sum(r["confidence"] for r in self.reasoning_history) / len(self.reasoning_history) if self.reasoning_history else 0,
            "query_types": [r["query_type"] for r in self.reasoning_history],
            "tools_used": [tool for r in self.reasoning_history for tool in r["required_tools"]]
        }