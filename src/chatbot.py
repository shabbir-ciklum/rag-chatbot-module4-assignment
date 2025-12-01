from typing import List, Dict
import logging
from datetime import datetime

class RAGChatbot:
    """
    Main chatbot interface combining all components.
    Supports conversation history and logging.
    """
    
    def __init__(self, retriever, log_file: str = "logs/chat_history.log"):
        self.retriever = retriever
        self.chat_history: List[Dict] = []
        
        # Setup logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def chat(self, user_message: str) -> str:
        """
        Process a user message and return response.
        Maintains conversation history.
        """
        # Log the question
        self.logger.info(f"USER: {user_message}")
        
        # Get response from RAG pipeline
        result = self.retriever.query(user_message)
        answer = result["answer"]
        
        # Update chat history
        self.chat_history.append({"role": "user", "content": user_message})
        self.chat_history.append({"role": "assistant", "content": answer})
        
        # Log the answer
        self.logger.info(f"ASSISTANT: {answer}")
        
        # Log sources used
        if result.get("sources"):
            sources_log = ", ".join([
                f"{s['source']}(p.{s['page']})" 
                for s in result["sources"]
            ])
            self.logger.info(f"SOURCES: {sources_log}")
        
        return answer
    
    def get_full_response(self, user_message: str) -> Dict:
        """Get response with sources and metadata."""
        self.logger.info(f"USER: {user_message}")
        
        result = self.retriever.query(user_message, return_sources=True)
        
        self.chat_history.append({"role": "user", "content": user_message})
        self.chat_history.append({"role": "assistant", "content": result["answer"]})
        
        self.logger.info(f"ASSISTANT: {result['answer']}")
        
        return result
    
    def reset_history(self):
        """Clear conversation history."""
        self.chat_history = []
        self.logger.info("--- CONVERSATION RESET ---")
    
    def interactive_mode(self):
        """Run chatbot in interactive terminal mode."""
        print("\n" + "="*50)
        print("RAG Chatbot - Type 'quit' to exit, 'reset' to clear history")
        print("="*50 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break
                    
                if user_input.lower() == 'reset':
                    self.reset_history()
                    print("Conversation history cleared.\n")
                    continue
                
                response = self.chat(user_input)
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break