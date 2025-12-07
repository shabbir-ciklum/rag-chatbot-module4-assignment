
import logging
from datetime import datetime
from pathlib import Path


class RAGChatbot:
    """Enhanced RAG Chatbot with Agent capabilities."""
    
    def __init__(self, retriever, log_file=None, agent=None):
        """
        Initialize the chatbot.
        
        Args:
            retriever: RAGRetriever instance
            log_file: Optional path to log file
            agent: Optional AIAgent instance for advanced capabilities
        """
        self.retriever = retriever
        self.agent = agent
        
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='%(asctime)s | %(message)s'
            )
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = None
    
    def get_full_response(self, query: str, use_agent: bool = False) -> dict:
        """
        Get a complete response with sources.
        
        Args:
            query: User question
            use_agent: Whether to use the full agent capabilities
            
        Returns:
            Dictionary with answer and sources
        """
        if use_agent and self.agent:
            # Use full agent processing
            interaction = self.agent.process_query(query, use_reflection=True)
            
            result = {
                "answer": interaction["response"],
                "sources": interaction["retrieval_results"],
                "reasoning": interaction.get("reasoning"),
                "reflection": interaction.get("reflection"),
                "evaluation": interaction.get("evaluation"),
                "tool_results": interaction.get("tool_results")
            }
        else:
            # Use basic RAG retrieval
            result = self.retriever.query(query)
        
        if self.logger:
            self.logger.info(f"Query: {query}")
            self.logger.info(f"Answer: {result['answer']}")
        
        return result
    
    def interactive_mode(self):
        """Run the chatbot in interactive mode."""
        print("\n" + "="*60)
        print("Interactive Mode (type 'exit' to quit)")
        print("Commands:")
        print("  - Type your question normally for basic RAG")
        print("  - Use '/agent <query>' for full agent capabilities")
        print("  - Use '/analyze' to make agent analyze itself")
        print("  - Use '/report' to get performance report")
        print("  - Use '/linkedin' to generate LinkedIn post")
        print("="*60)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye! 👋")
                    
                    # Export final reports if agent is available
                    if self.agent:
                        print("\nExporting performance reports...")
                        files = self.agent.export_full_report()
                        print(f"Reports saved to: {', '.join(files)}")
                    break
                
                # Handle special commands
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                    continue
                
                # Regular query
                result = self.get_full_response(user_input, use_agent=False)
                
                print(f"\nAssistant: {result['answer']}")
                
                if result.get("sources"):
                    print("\n Sources:")
                    for i, source in enumerate(result["sources"][:3], 1):
                        print(f"  {i}. {source['source']} (Page {source.get('page', 'N/A')}, Score: {source['score']:.3f})")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! ")
                break
            except Exception as e:
                print(f"\n Error: {e}")
    
    def _handle_command(self, command: str):
        """Handle special commands in interactive mode."""
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if not self.agent:
            print(" Agent capabilities not available. Please run with agent enabled.")
            return
        
        if cmd == '/agent':
            if not args:
                print(" Please provide a query after /agent")
                return
            
            print("\n Using full agent capabilities...\n")
            result = self.get_full_response(args, use_agent=True)
            
            print(f"\nAssistant: {result['answer']}")
            
            if result.get("reflection"):
                print(f"\n Reflection:")
                print(f"   Quality Score: {result['reflection']['quality_score']:.2f}")
                if result['reflection'].get('strengths'):
                    print(f"   Strengths: {', '.join(result['reflection']['strengths'])}")
            
            if result.get("evaluation"):
                print(f"\n Evaluation:")
                print(f"   Overall Score: {result['evaluation']['overall_score']:.2f}")
        
        elif cmd == '/analyze':
            print("\n Performing self-analysis...\n")
            analysis = self.agent.analyze_self()
            
            print("\n Statistics:")
            stats = analysis["stats"]
            print(f"   Total Files: {stats['total_files']}")
            print(f"   Python Files: {stats['python_files']}")
            print(f"   Total Lines: {stats['total_lines']:,}")
            
            print("\n  Architecture:")
            arch = analysis["architecture"]
            print(f"   Type: {arch['architecture_type']}")
            print(f"   Layers: {', '.join(arch['layers'].keys())}")
        
        elif cmd == '/report':
            print("\n Performance Report:\n")
            report = self.agent.get_performance_report()
            
            summary = report["evaluator_summary"]
            print(f"Total Evaluations: {summary['total_evaluations']}")
            
            if summary.get("average_scores"):
                print("\nAverage Scores:")
                for metric, score in summary["average_scores"].items():
                    print(f"   {metric}: {score:.2f}")
        
        elif cmd == '/linkedin':
            print("\n  Generating LinkedIn post...\n")
            analysis = self.agent.analyze_self()
            post = analysis["linkedin_post"]
            
            print("="*70)
            print(post)
            print("="*70)
            
            # Save to file
            output_file = "linkedin_post.txt"
            with open(output_file, 'w') as f:
                f.write(post)
            print(f"\n Post saved to: {output_file}")
        
        else:
            print(f" Unknown command: {cmd}")
            print("Available commands: /agent, /analyze, /report, /linkedin")