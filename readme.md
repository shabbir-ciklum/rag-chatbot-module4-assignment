# AI-Agentic RAG Chatbot

> An advanced Retrieval-Augmented Generation (RAG) chatbot enhanced with autonomous reasoning, tool-calling capabilities, and self-reflection mechanisms. Built for the Ciklum AI Academy Engineering Track.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

##  Features

### Core Capabilities
- **Multi-Format Data Ingestion**: Process PDFs and audio files (via Whisper)
- **Autonomous Reasoning**: Agent reasons about queries before responding
- **Self-Reflection**: Critiques own responses and regenerates if quality is low
- **Tool Calling**: Can analyze code, generate documentation, create LinkedIn posts
- **Performance Evaluation**: Comprehensive metrics tracking
- **Multi-LLM Support**: Works with Ollama (local), Groq, or Google Gemini
- **Meta-Capability**: Can analyze its own codebase

### Agent Tools
1. **Code Analyzer**: AST-based analysis of Python codebase
2. **Documentation Generator**: Auto-generates project docs
3. **LinkedIn Post Creator**: Creates professional social media posts
4. **Architecture Analyzer**: Analyzes system design patterns
5. **Stats Collector**: Gathers project statistics

##  Architecture

See [architecture.mmd](architecture.mmd) for detailed system architecture diagram.

```
User Query → AI Agent → Reasoner → Tools/RAG → LLM → Self-Reflection → Evaluation → Response
```

##  Prerequisites

- Python 3.9+
- pip
- (Optional) Ollama installed locally
- (Optional) Groq API key
- (Optional) Google Gemini API key

##  Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd rag-chatbot-module4-assignment
```

### 2. Activate Virtual Environment

**IMPORTANT:** Always activate the virtual environment before running the project:

```bash
source venv311/bin/activate
```

You should see `(venv311)` in your terminal prompt.

### 3. Install Dependencies (if needed)

Dependencies are already installed. If you need to reinstall:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Optional: If using Groq
GROQ_API_KEY=your_groq_api_key_here

# Optional: If using Google Gemini
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Prepare Data

```bash
# Add PDF files
mkdir -p data/pdfs
# Copy your PDF files to data/pdfs/

# Add audio files (optional)
mkdir -p data/audio
# Copy audio files to data/audio/
```

##  Usage

### Quick Start with Helper Script

The easiest way to run the chatbot:

```bash
# Basic RAG mode
./run.sh --provider ollama --rebuild

# Full agent mode (RECOMMENDED)
./run.sh --provider ollama --agent-mode --rebuild

# Self-analysis mode
./run.sh --provider ollama --agent-mode --self-analyze
```

### Manual Usage (with venv activation)

```bash
# 1. Activate virtual environment
source venv311/bin/activate

# 2. Run the chatbot
python main.py --provider ollama --agent-mode --rebuild
```

### Basic Usage (RAG Mode)

```bash
./run.sh --provider ollama --rebuild
# OR
python main.py --provider ollama --rebuild
```

### Agent Mode (Full Capabilities) ⭐ RECOMMENDED

```bash
./run.sh --provider ollama --agent-mode --rebuild
# OR
python main.py --provider ollama --agent-mode --rebuild
```

### Self-Analysis Mode

Generate a LinkedIn post about the project:

```bash
./run.sh --provider ollama --agent-mode --self-analyze
# OR
python main.py --provider ollama --agent-mode --self-analyze
```

### Command-Line Options

```
--provider        : LLM provider (ollama, groq, gemini) [default: ollama]
--model          : Specific model name (optional)
--rebuild        : Rebuild vector database from scratch
--agent-mode     : Enable full agent capabilities
--self-analyze   : Run self-analysis and generate LinkedIn post
```

##  Interactive Commands

When in interactive mode, use these commands:

- **Regular query**: Just type your question
- `/agent <query>`: Use full agent capabilities with reasoning
- `/analyze`: Perform self-analysis of codebase
- `/report`: Get performance metrics report
- `/linkedin`: Generate LinkedIn post
- `exit` or `quit`: Exit the program

### Example Session

```
You: /agent What are the key components of this system?

Using full agent capabilities...

 Step 1: Reasoning...
   → Query type: information
   → Required tools: ['analyze_code', 'analyze_architecture']
   → Confidence: 0.80

 Step 2: Retrieving relevant information...
   → Retrieved 3 documents
   → Top relevance score: 0.892

 Step 3: Executing tools...
   → Executed 2 tools successfully
      • analyze_code
      • analyze_architecture

 Step 4: Generating response...
   → Response generated (450 chars)

 Step 5: Performing self-reflection...
   → Quality score: 0.85
   → Strengths: Response addresses query keywords, Used 3 context documents

 Step 6: Evaluating performance...
   → Overall score: 0.82