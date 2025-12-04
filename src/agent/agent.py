"""
AI Agent Orchestrator
Main agent that coordinates reasoning, tool calling, and self-reflection.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .tools import AgentTools
from .reasoner import AgentReasoner
from .evaluator import AgentEvaluator


class AIAgent:
    """
    Main AI Agent that orchestrates autonomous reasoning, tool calling, and self-reflection.
    """
    
    def __init__(self, 
                 rag_retriever,
                 llm_provider,
                 project_root: str = "."):
        """
        Initialize the AI Agent.
        
        Args:
            rag_retriever: RAG retriever instance for information retrieval
            llm_provider: LLM provider for generation
            project_root: Root directory of the project
        """
        self.rag_retriever = rag_retriever
        self.llm_provider = llm_provider
        self.project_root = project_root
        
        # Initialize components
        self.tools = AgentTools(project_root)
        self.reasoner = AgentReasoner(llm_provider)
        self.evaluator = AgentEvaluator()
        
        # Interaction history
        self.interaction_history = []
        
    def process_query(self, query: str, use_reflection: bool = True) -> Dict[str, Any]:
        """
        Process a query with full agentic capabilities.
        
        Args:
            query: User's question or request
            use_reflection: Whether to perform self-reflection
            
        Returns:
            Dictionary with response and metadata
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "reasoning": None,
            "retrieval_results": [],
            "tool_results": {},
            "response": "",
            "reflection": None,
            "evaluation": None
        }
        
        print(f"\n{'='*70}")
        print(f"🤖 Agent Processing Query")
        print(f"{'='*70}")
        print(f"Query: {query}\n")
        
        # Step 1: Reason about the query
        print("💭 Step 1: Reasoning...")
        retrieved_docs = self.rag_retriever.retrieve(query)
        context = {"retrieved_docs": retrieved_docs}
        
        reasoning = self.reasoner.reason_about_query(query, context)
        interaction["reasoning"] = reasoning
        
        print(f"   → Query type: {reasoning['query_type']}")
        print(f"   → Required tools: {reasoning['required_tools']}")
        print(f"   → Confidence: {reasoning['confidence']:.2f}")
        
        # Step 2: Execute RAG retrieval
        print("\n📚 Step 2: Retrieving relevant information...")
        interaction["retrieval_results"] = retrieved_docs
        
        if retrieved_docs:
            print(f"   → Retrieved {len(retrieved_docs)} documents")
            print(f"   → Top relevance score: {retrieved_docs[0].get('score', 0):.3f}")
        else:
            print("   → No documents retrieved")
        
        # Step 3: Execute required tools
        print("\n🔧 Step 3: Executing tools...")
        tool_results = self._execute_tools(reasoning["required_tools"])
        interaction["tool_results"] = tool_results
        
        if tool_results:
            print(f"   → Executed {len(tool_results)} tools successfully")
            for tool_name in tool_results:
                print(f"      • {tool_name}")
        else:
            print("   → No tools executed")
        
        # Step 4: Generate response
        print("\n✍️  Step 4: Generating response...")
        response = self._generate_response(
            query=query,
            retrieved_context=retrieved_docs,
            tool_results=tool_results,
            reasoning=reasoning
        )
        interaction["response"] = response
        print(f"   → Response generated ({len(response)} chars)")
        
        # Step 5: Self-reflection (if enabled)
        if use_reflection:
            print("\n🪞 Step 5: Performing self-reflection...")
            reflection = self.reasoner.reflect_on_response(
                query=query,
                response=response,
                retrieved_context=retrieved_docs,
                tool_results=tool_results
            )
            interaction["reflection"] = reflection
            
            print(f"   → Quality score: {reflection['quality_score']:.2f}")
            if reflection["strengths"]:
                print(f"   → Strengths: {', '.join(reflection['strengths'][:2])}")
            if reflection["weaknesses"]:
                print(f"   → Areas to improve: {', '.join(reflection['weaknesses'][:2])}")
            
            # Regenerate if quality is too low
            if reflection["should_regenerate"]:
                print("\n   ⚠️  Quality below threshold - regenerating...")
                response = self._regenerate_response(query, retrieved_docs, tool_results)
                interaction["response"] = response
        
        # Step 6: Evaluate performance
        print("\n📊 Step 6: Evaluating performance...")
        evaluation = self.evaluator.evaluate_overall_performance(
            query=query,
            response=response,
            reasoning=reasoning,
            retrieval_results=retrieved_docs,
            tool_results=tool_results
        )
        interaction["evaluation"] = evaluation
        
        print(f"   → Overall score: {evaluation['overall_score']:.2f}")
        
        # Store interaction
        self.interaction_history.append(interaction)
        
        print(f"\n{'='*70}\n")
        
        return interaction
    
    def _execute_tools(self, tool_names: List[str]) -> Dict[str, Any]:
        """
        Execute the specified tools.
        
        Args:
            tool_names: List of tool names to execute
            
        Returns:
            Dictionary mapping tool names to their results
        """
        results = {}
        available_tools = {tool["name"]: tool["function"] for tool in self.tools.get_tools()}
        
        for tool_name in tool_names:
            if tool_name == "rag_search":
                # Skip - already handled by retrieval
                continue
                
            if tool_name in available_tools:
                try:
                    result = available_tools[tool_name]()
                    results[tool_name] = result
                except Exception as e:
                    results[tool_name] = {"error": str(e)}
        
        return results
    
    def _generate_response(self,
                          query: str,
                          retrieved_context: List[Dict],
                          tool_results: Dict[str, Any],
                          reasoning: Dict[str, Any]) -> str:
        """
        Generate a response using LLM with context and tool results.
        
        Args:
            query: User query
            retrieved_context: Retrieved documents
            tool_results: Results from tool executions
            reasoning: Reasoning analysis
            
        Returns:
            Generated response string
        """
        # Build comprehensive prompt
        prompt = self._build_generation_prompt(query, retrieved_context, tool_results, reasoning)
        
        try:
            # LLM providers expect (query, context) parameters
            # Pass the full prompt as query with empty context
            response = self.llm_provider.generate(
                query=prompt,
                context=""
            )
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _build_generation_prompt(self,
                                query: str,
                                retrieved_context: List[Dict],
                                tool_results: Dict[str, Any],
                                reasoning: Dict[str, Any]) -> str:
        """Build comprehensive prompt for response generation."""
        prompt = f"You are an AI assistant with reasoning and tool-using capabilities.\n\n"
        prompt += f"USER QUERY: {query}\n\n"
        
        # Add reasoning context
        prompt += f"REASONING ANALYSIS:\n"
        prompt += f"- Query type: {reasoning['query_type']}\n"
        prompt += f"- Confidence: {reasoning['confidence']:.2f}\n"
        prompt += f"- Reasoning chain: {', '.join(reasoning['reasoning_chain'][:3])}\n\n"
        
        # Add retrieved context
        if retrieved_context:
            prompt += f"RETRIEVED CONTEXT:\n"
            for i, doc in enumerate(retrieved_context[:3], 1):
                prompt += f"{i}. {doc['content'][:200]}...\n"
            prompt += "\n"
        
        # Add tool results
        if tool_results:
            prompt += f"TOOL EXECUTION RESULTS:\n"
            for tool_name, result in tool_results.items():
                if isinstance(result, dict) and "error" not in result:
                    prompt += f"\n{tool_name.upper()}:\n"
                    prompt += f"{json.dumps(result, indent=2)[:300]}...\n"
            prompt += "\n"
        
        prompt += "Based on the above information, provide a comprehensive and accurate answer to the user's query.\n"
        prompt += "RESPONSE:"
        
        return prompt
    
    def _regenerate_response(self,
                            query: str,
                            retrieved_context: List[Dict],
                            tool_results: Dict[str, Any]) -> str:
        """Regenerate response with adjusted parameters."""
        # Try with more context
        additional_docs = self.rag_retriever.retrieve(query, k=5)
        
        reasoning = self.reasoner.reason_about_query(query, {"retrieved_docs": additional_docs})
        
        return self._generate_response(
            query=query,
            retrieved_context=additional_docs,
            tool_results=tool_results,
            reasoning=reasoning
        )
    
    def analyze_self(self) -> Dict[str, Any]:
        """
        Perform self-analysis on the agent's own codebase.
        This is the meta capability for the assignment.
        
        Returns:
            Dictionary with self-analysis results
        """
        print(f"\n{'='*70}")
        print(f"🔍 Agent Self-Analysis Mode")
        print(f"{'='*70}\n")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "code_analysis": None,
            "architecture": None,
            "stats": None,
            "linkedin_post": None
        }
        
        # Analyze own code
        print("📝 Analyzing codebase...")
        analysis["code_analysis"] = self.tools.analyze_code()
        
        # Analyze architecture
        print("🏗️  Analyzing architecture...")
        analysis["architecture"] = self.tools.analyze_architecture()
        
        # Get statistics
        print("📊 Gathering statistics...")
        analysis["stats"] = self.tools.get_project_stats()
        
        # Generate LinkedIn post
        print("✍️  Generating LinkedIn post...")
        context = {
            "code_analysis": analysis["code_analysis"],
            "stats": analysis["stats"]
        }
        analysis["linkedin_post"] = self.tools.create_linkedin_post(context)
        
        print("\n✅ Self-analysis complete!\n")
        
        return analysis
    
    def get_performance_report(self) -> Dict[str, Any]:
        """
        Get a comprehensive performance report.
        
        Returns:
            Dictionary with performance metrics and summary
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "evaluator_summary": self.evaluator.get_performance_summary(),
            "reasoner_summary": self.reasoner.get_reasoning_summary(),
            "total_interactions": len(self.interaction_history),
            "tools_available": len(self.tools.get_tools())
        }
    
    def export_full_report(self, output_dir: str = "reports") -> List[str]:
        """
        Export comprehensive reports to files.
        
        Args:
            output_dir: Directory to save reports
            
        Returns:
            List of created file paths
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        created_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export evaluation report
        eval_file = f"{output_dir}/evaluation_report_{timestamp}.json"
        self.evaluator.export_evaluation_report(eval_file)
        created_files.append(eval_file)
        
        # Export interaction history
        history_file = f"{output_dir}/interaction_history_{timestamp}.json"
        with open(history_file, 'w') as f:
            json.dump(self.interaction_history, f, indent=2)
        created_files.append(history_file)
        
        # Export performance summary
        summary_file = f"{output_dir}/performance_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(self.get_performance_report(), f, indent=2)
        created_files.append(summary_file)
        
        return created_files