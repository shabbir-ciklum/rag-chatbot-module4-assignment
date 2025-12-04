"""
Agent Tools Module
Provides actionable tools for the AI agent to use during reasoning.
"""

import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class AgentTools:
    """Collection of tools the agent can use."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools with descriptions."""
        return [
            {
                "name": "analyze_code",
                "description": "Analyze code files in the repository to understand structure, patterns, and functionality",
                "function": self.analyze_code
            },
            {
                "name": "generate_documentation",
                "description": "Generate documentation summaries for the project",
                "function": self.generate_documentation
            },
            {
                "name": "create_linkedin_post",
                "description": "Create a professional LinkedIn post about the project",
                "function": self.create_linkedin_post
            },
            {
                "name": "analyze_architecture",
                "description": "Analyze the overall architecture and design patterns of the project",
                "function": self.analyze_architecture
            },
            {
                "name": "get_project_stats",
                "description": "Get statistics about the project (files, lines of code, etc.)",
                "function": self.get_project_stats
            }
        ]
    
    def analyze_code(self, file_path: str = None) -> Dict[str, Any]:
        """
        Analyze Python code files to extract structure and patterns.
        
        Args:
            file_path: Specific file to analyze, or None to analyze all Python files
            
        Returns:
            Dictionary with code analysis results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": [],
            "total_classes": 0,
            "total_functions": 0,
            "key_components": []
        }
        
        if file_path:
            files_to_analyze = [Path(file_path)]
        else:
            # Analyze all Python files in src/
            src_dir = self.project_root / "src"
            files_to_analyze = list(src_dir.rglob("*.py"))
        
        for py_file in files_to_analyze:
            if py_file.name.startswith("__"):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    
                file_info = {
                    "file": str(py_file.relative_to(self.project_root)),
                    "classes": [],
                    "functions": []
                }
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        file_info["classes"].append({
                            "name": node.name,
                            "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                        })
                        results["total_classes"] += 1
                    elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                        file_info["functions"].append(node.name)
                        results["total_functions"] += 1
                
                results["files_analyzed"].append(file_info)
                
            except Exception as e:
                print(f"Error analyzing {py_file}: {e}")
                
        # Extract key components
        for file_info in results["files_analyzed"]:
            for cls in file_info["classes"]:
                results["key_components"].append({
                    "type": "class",
                    "name": cls["name"],
                    "file": file_info["file"],
                    "methods_count": len(cls["methods"])
                })
        
        return results
    
    def generate_documentation(self, section: str = "overview") -> Dict[str, str]:
        """
        Generate documentation for different sections of the project.
        
        Args:
            section: Which section to document (overview, architecture, usage)
            
        Returns:
            Dictionary with documentation content
        """
        docs = {
            "section": section,
            "timestamp": datetime.now().isoformat()
        }
        
        if section == "overview":
            stats = self.get_project_stats()
            docs["content"] = f"""
# RAG Chatbot - AI Agentic System

## Overview
This project is an advanced RAG (Retrieval-Augmented Generation) chatbot enhanced with agentic capabilities.
It combines multiple data sources with autonomous reasoning and tool-calling abilities.

## Key Statistics
- Total Files: {stats['total_files']}
- Lines of Code: {stats['total_lines']}
- Python Modules: {stats['python_files']}

## Core Capabilities
1. Multi-format data ingestion (PDF, Audio)
2. Semantic chunking and vector storage
3. Autonomous reasoning and self-reflection
4. Tool-based actions
5. Multi-LLM support (Ollama, Groq, Gemini)
"""
        
        elif section == "architecture":
            code_analysis = self.analyze_code()
            docs["content"] = f"""
# Architecture

## Components
- Total Classes: {code_analysis['total_classes']}
- Total Functions: {code_analysis['total_functions']}

## Key Modules
"""
            for component in code_analysis['key_components'][:5]:
                docs["content"] += f"\n- {component['name']} ({component['type']}): {component['file']}"
        
        elif section == "usage":
            docs["content"] = """
# Usage Guide

## Running the Agent
```bash
python main.py --provider ollama --rebuild
```

## Available Providers
- ollama: Local LLM (default)
- groq: Groq Cloud API
- gemini: Google Gemini API

## Interactive Mode
The chatbot enters interactive mode after running test questions.
Type your questions and the agent will reason through them.
"""
        
        return docs
    
    def create_linkedin_post(self, context: Dict[str, Any]) -> str:
        """
        Create a professional LinkedIn post about the project.
        
        Args:
            context: Dictionary with project information from agent's analysis
            
        Returns:
            LinkedIn post text
        """
        stats = self.get_project_stats()
        
        post = f"""🤖 Excited to share my AI Agentic System built during the Ciklum AI Academy!

This project evolved from a RAG chatbot into a full autonomous agent capable of:

✅ Multi-format data processing (PDFs, Audio transcriptions)
✅ Semantic search with vector embeddings
✅ Autonomous reasoning and self-reflection
✅ Tool-based actions (code analysis, documentation generation)
✅ Multi-LLM flexibility (Ollama, Groq, Gemini)

🔧 Tech Stack: Python, LangChain, ChromaDB, Whisper, Sentence Transformers

📊 Project Stats:
• {stats['python_files']} Python modules
• {stats['total_lines']:,} lines of code
• {stats['total_files']} total files

This agent can analyze its own codebase, generate documentation, and even write this post autonomously! 

Built as part of @Ciklum AI Academy's Engineering Track - focusing on real-world AI agent development, RAG pipelines, and autonomous reasoning systems.

#AI #MachineLearning #RAG #AgenticAI #Python #CiklumAIAcademy
"""
        
        return post
    
    def analyze_architecture(self) -> Dict[str, Any]:
        """
        Analyze the overall architecture and design patterns.
        
        Returns:
            Dictionary with architecture analysis
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "architecture_type": "Modular Agent System with RAG",
            "patterns": [],
            "layers": {}
        }
        
        # Identify architectural layers
        src_dir = self.project_root / "src"
        if src_dir.exists():
            subdirs = [d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith("__")]
            
            for subdir in subdirs:
                layer_name = subdir.name
                files = list(subdir.glob("*.py"))
                analysis["layers"][layer_name] = {
                    "files": len(files),
                    "purpose": self._infer_layer_purpose(layer_name)
                }
        
        # Identify patterns
        analysis["patterns"] = [
            "Provider Pattern (LLM providers)",
            "Strategy Pattern (Chunking strategies)",
            "Repository Pattern (Vector store)",
            "Tool Pattern (Agent tools)",
            "Chain of Responsibility (Agent reasoning)"
        ]
        
        return analysis
    
    def get_project_stats(self) -> Dict[str, int]:
        """
        Get basic statistics about the project.

        Returns:
            Dictionary with project statistics
        """
        stats = {
            "total_files": 0,
            "python_files": 0,
            "total_lines": 0,
            "test_files": 0
        }

        # Directories to exclude (dependencies, caches, etc.)
        exclude_dirs = {
            'venv', 'venv311', 'env', '.venv',
            '__pycache__', '.git', '.pytest_cache',
            'node_modules', 'build', 'dist',
            'chroma_db', 'test_chroma_db', 'quick_test_db',
            'logs', 'reports', 'data', 'models',
            '.cache', '.huggingface'
        }

        for file_path in self.project_root.rglob("*"):
            # Skip if file is in an excluded directory
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue

            # Skip hidden files and directories
            if any(part.startswith(".") for part in file_path.parts):
                continue

            if file_path.is_file():
                stats["total_files"] += 1

                if file_path.suffix == ".py":
                    stats["python_files"] += 1

                    if "test" in str(file_path):
                        stats["test_files"] += 1

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            stats["total_lines"] += len(f.readlines())
                    except:
                        pass

        return stats
    
    def _infer_layer_purpose(self, layer_name: str) -> str:
        """Infer the purpose of an architectural layer from its name."""
        purposes = {
            "data_loaders": "Data ingestion and preprocessing",
            "processing": "Text processing and chunking",
            "vectorstore": "Vector database management",
            "retrieval": "Information retrieval and RAG",
            "llm_providers": "LLM provider abstraction",
            "agent": "Autonomous reasoning and tool calling"
        }
        return purposes.get(layer_name, "Custom module")


# Convenience function to get tool instance
def get_agent_tools(project_root: str = ".") -> AgentTools:
    """Get an instance of AgentTools."""
    return AgentTools(project_root)