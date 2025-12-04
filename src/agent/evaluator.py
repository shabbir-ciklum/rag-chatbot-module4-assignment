"""
Agent Evaluator Module
Provides evaluation and measurement capabilities for the agent's performance.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict
import json
import math


class AgentEvaluator:
    """
    Evaluates the agent's performance across multiple dimensions.
    """
    
    def __init__(self):
        """Initialize the evaluator."""
        self.evaluation_history = []
        self.metrics = {
            "retrieval_accuracy": [],
            "response_relevance": [],
            "tool_selection_accuracy": [],
            "reasoning_quality": [],
            "overall_quality": []
        }
        
    def evaluate_retrieval(self, 
                          query: str, 
                          retrieved_docs: List[Dict],
                          expected_keywords: Optional[List[str]] = None) -> Dict[str, float]:
        """
        Evaluate the quality of document retrieval.
        
        Args:
            query: Original query
            retrieved_docs: Documents retrieved by RAG
            expected_keywords: Optional list of keywords that should appear
            
        Returns:
            Dictionary with retrieval metrics
        """
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "num_retrieved": len(retrieved_docs),
            "avg_score": 0.0,
            "score_variance": 0.0,
            "keyword_coverage": 0.0,
            "retrieval_score": 0.0
        }
        
        if not retrieved_docs:
            self.metrics["retrieval_accuracy"].append(0.0)
            return metrics
        
        # Calculate average retrieval score
        scores = [doc.get("score", 0.0) for doc in retrieved_docs]
        metrics["avg_score"] = sum(scores) / len(scores)
        
        # Calculate score variance (measures consistency)
        mean_score = metrics["avg_score"]
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        metrics["score_variance"] = math.sqrt(variance)
        
        # Check keyword coverage if provided
        if expected_keywords:
            found_keywords = 0
            for doc in retrieved_docs:
                content = doc.get("content", "").lower()
                for keyword in expected_keywords:
                    if keyword.lower() in content:
                        found_keywords += 1
                        break
            
            metrics["keyword_coverage"] = found_keywords / len(expected_keywords)
        else:
            # Check query keyword coverage
            query_keywords = set(query.lower().split())
            found_keywords = 0
            for doc in retrieved_docs:
                content = doc.get("content", "").lower()
                if any(kw in content for kw in query_keywords):
                    found_keywords += 1
            
            metrics["keyword_coverage"] = found_keywords / len(retrieved_docs) if retrieved_docs else 0
        
        # Overall retrieval score (weighted combination)
        metrics["retrieval_score"] = (
            metrics["avg_score"] * 0.4 +
            metrics["keyword_coverage"] * 0.4 +
            (1 - min(1.0, metrics["score_variance"])) * 0.2
        )
        
        self.metrics["retrieval_accuracy"].append(metrics["retrieval_score"])
        return metrics
    
    def evaluate_response_relevance(self, 
                                   query: str, 
                                   response: str,
                                   retrieved_context: List[Dict]) -> Dict[str, float]:
        """
        Evaluate how relevant the response is to the query.
        
        Args:
            query: Original query
            response: Generated response
            retrieved_context: Context used to generate response
            
        Returns:
            Dictionary with relevance metrics
        """
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "query_keyword_overlap": 0.0,
            "context_usage": 0.0,
            "response_length_score": 0.0,
            "relevance_score": 0.0
        }
        
        # Calculate query keyword overlap
        query_keywords = set(query.lower().split())
        response_keywords = set(response.lower().split())
        overlap = len(query_keywords & response_keywords)
        metrics["query_keyword_overlap"] = overlap / len(query_keywords) if query_keywords else 0
        
        # Estimate context usage
        if retrieved_context:
            context_text = " ".join([doc.get("content", "") for doc in retrieved_context[:3]])
            context_keywords = set(context_text.lower().split())

            # Check how many context keywords appear in response
            context_in_response = len(context_keywords & response_keywords)
            # Use min to limit context keywords to 50, or use all if less than 50
            context_keywords_count = min(50, len(context_keywords))
            metrics["context_usage"] = min(1.0, context_in_response / max(1, context_keywords_count))
        
        # Score response length (penalize too short or too long)
        ideal_length = 200  # words
        response_length = len(response.split())
        length_ratio = response_length / ideal_length
        metrics["response_length_score"] = 1.0 - abs(1.0 - length_ratio) if length_ratio < 2 else 0.3
        
        # Overall relevance score
        metrics["relevance_score"] = (
            metrics["query_keyword_overlap"] * 0.4 +
            metrics["context_usage"] * 0.4 +
            metrics["response_length_score"] * 0.2
        )
        
        self.metrics["response_relevance"].append(metrics["relevance_score"])
        return metrics
    
    def evaluate_tool_selection(self, 
                               query: str,
                               tools_selected: List[str],
                               tools_executed: List[str],
                               expected_tools: Optional[List[str]] = None) -> Dict[str, float]:
        """
        Evaluate the quality of tool selection and execution.
        
        Args:
            query: Original query
            tools_selected: Tools the agent decided to use
            tools_executed: Tools that were actually executed successfully
            expected_tools: Optional list of tools that should have been used
            
        Returns:
            Dictionary with tool selection metrics
        """
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "tools_selected": len(tools_selected),
            "tools_executed": len(tools_executed),
            "execution_rate": 0.0,
            "precision": 0.0,
            "tool_selection_score": 0.0
        }
        
        # Calculate execution rate
        if tools_selected:
            metrics["execution_rate"] = len(tools_executed) / len(tools_selected)
        else:
            metrics["execution_rate"] = 1.0 if not tools_executed else 0.0
        
        # Calculate precision if expected tools are provided
        if expected_tools:
            correct_selections = len(set(tools_selected) & set(expected_tools))
            metrics["precision"] = correct_selections / len(tools_selected) if tools_selected else 0.0
        else:
            # Without ground truth, give credit for any tool usage
            metrics["precision"] = 1.0 if tools_selected else 0.5
        
        # Overall tool selection score
        metrics["tool_selection_score"] = (
            metrics["execution_rate"] * 0.5 +
            metrics["precision"] * 0.5
        )
        
        self.metrics["tool_selection_accuracy"].append(metrics["tool_selection_score"])
        return metrics
    
    def evaluate_reasoning_quality(self, reasoning_chain: List[str]) -> Dict[str, float]:
        """
        Evaluate the quality of the agent's reasoning process.
        
        Args:
            reasoning_chain: List of reasoning steps taken
            
        Returns:
            Dictionary with reasoning quality metrics
        """
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "reasoning_steps": len(reasoning_chain),
            "avg_step_length": 0.0,
            "reasoning_depth": 0.0,
            "reasoning_score": 0.0
        }
        
        if not reasoning_chain:
            self.metrics["reasoning_quality"].append(0.0)
            return metrics
        
        # Calculate average step length
        step_lengths = [len(step) for step in reasoning_chain]
        metrics["avg_step_length"] = sum(step_lengths) / len(step_lengths)
        
        # Estimate reasoning depth (more steps = deeper reasoning)
        metrics["reasoning_depth"] = min(1.0, len(reasoning_chain) / 5.0)
        
        # Overall reasoning score
        # Good reasoning should have multiple steps but not too verbose
        optimal_steps = 4
        step_score = 1.0 - abs(len(reasoning_chain) - optimal_steps) / optimal_steps
        step_score = max(0.0, step_score)
        
        metrics["reasoning_score"] = (
            step_score * 0.6 +
            metrics["reasoning_depth"] * 0.4
        )
        
        self.metrics["reasoning_quality"].append(metrics["reasoning_score"])
        return metrics
    
    def evaluate_overall_performance(self, 
                                    query: str,
                                    response: str,
                                    reasoning: Dict[str, Any],
                                    retrieval_results: List[Dict],
                                    tool_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive evaluation of a single agent interaction.
        
        Args:
            query: User query
            response: Agent response
            reasoning: Reasoning process details
            retrieval_results: RAG retrieval results
            tool_results: Results from tool executions
            
        Returns:
            Dictionary with comprehensive evaluation
        """
        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "component_scores": {},
            "overall_score": 0.0,
            "strengths": [],
            "areas_for_improvement": []
        }
        
        # Evaluate each component
        retrieval_eval = self.evaluate_retrieval(query, retrieval_results)
        relevance_eval = self.evaluate_response_relevance(query, response, retrieval_results)
        
        tools_selected = reasoning.get("required_tools", [])
        tools_executed = list(tool_results.keys()) if tool_results else []
        tool_eval = self.evaluate_tool_selection(query, tools_selected, tools_executed)
        
        reasoning_chain = reasoning.get("reasoning_chain", [])
        reasoning_eval = self.evaluate_reasoning_quality(reasoning_chain)
        
        # Aggregate scores
        evaluation["component_scores"] = {
            "retrieval": retrieval_eval["retrieval_score"],
            "relevance": relevance_eval["relevance_score"],
            "tool_selection": tool_eval["tool_selection_score"],
            "reasoning": reasoning_eval["reasoning_score"]
        }
        
        # Calculate overall score (weighted average)
        weights = {"retrieval": 0.25, "relevance": 0.35, "tool_selection": 0.20, "reasoning": 0.20}
        evaluation["overall_score"] = sum(
            evaluation["component_scores"][key] * weights[key] 
            for key in weights
        )
        
        # Identify strengths and areas for improvement
        for component, score in evaluation["component_scores"].items():
            if score >= 0.7:
                evaluation["strengths"].append(f"Strong {component} performance ({score:.2f})")
            elif score < 0.5:
                evaluation["areas_for_improvement"].append(f"Improve {component} ({score:.2f})")
        
        # Store in history
        self.evaluation_history.append(evaluation)
        self.metrics["overall_quality"].append(evaluation["overall_score"])
        
        return evaluation
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a summary of overall agent performance.
        
        Returns:
            Dictionary with performance statistics
        """
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_evaluations": len(self.evaluation_history),
            "average_scores": {},
            "best_performance": None,
            "worst_performance": None,
            "trends": {}
        }
        
        # Calculate average scores for each metric
        for metric_name, scores in self.metrics.items():
            if scores:
                summary["average_scores"][metric_name] = sum(scores) / len(scores)
        
        # Find best and worst performances
        if self.evaluation_history:
            sorted_evals = sorted(self.evaluation_history, key=lambda x: x["overall_score"])
            summary["worst_performance"] = {
                "score": sorted_evals[0]["overall_score"],
                "query": sorted_evals[0]["query"]
            }
            summary["best_performance"] = {
                "score": sorted_evals[-1]["overall_score"],
                "query": sorted_evals[-1]["query"]
            }
        
        # Calculate trends (improving or declining)
        for metric_name, scores in self.metrics.items():
            if len(scores) >= 3:
                recent_avg = sum(scores[-3:]) / 3
                overall_avg = summary["average_scores"].get(metric_name, 0)
                
                if recent_avg > overall_avg * 1.1:
                    summary["trends"][metric_name] = "improving"
                elif recent_avg < overall_avg * 0.9:
                    summary["trends"][metric_name] = "declining"
                else:
                    summary["trends"][metric_name] = "stable"
        
        return summary
    
    def export_evaluation_report(self, filepath: str) -> None:
        """
        Export detailed evaluation report to a JSON file.
        
        Args:
            filepath: Path where to save the report
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": self.get_performance_summary(),
            "detailed_evaluations": self.evaluation_history,
            "metrics_history": self.metrics
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Evaluation report exported to: {filepath}")