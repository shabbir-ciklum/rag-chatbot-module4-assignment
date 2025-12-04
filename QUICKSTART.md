# 🚀 Quick Start Guide - AI-Agentic RAG Chatbot

## ⚡ TL;DR - Run It Now!

```bash
# Option 1: Using the helper script (easiest)
./run.sh --provider ollama --agent-mode --rebuild

# Option 2: Manual activation
source venv311/bin/activate
python main.py --provider ollama --agent-mode --rebuild
```

---

## 📝 Step-by-Step Instructions

### Step 1: Navigate to Project Directory

```bash
cd /Users/shha/Documents/Module4Assignment/rag-chatbot-module4-assignment
```

### Step 2: Choose Your Method

#### Method A: Using Helper Script (Recommended)

```bash
# Make script executable (one-time only)
chmod +x run.sh

# Run with full agent capabilities
./run.sh --provider ollama --agent-mode --rebuild
```

#### Method B: Manual Activation

```bash
# 1. Activate virtual environment
source venv311/bin/activate

# 2. Verify Python version (should be 3.11.x)
python --version

# 3. Run the chatbot
python main.py --provider ollama --agent-mode --rebuild
```

---

## 🎯 Running Different Modes

### 1. Basic RAG Mode (Simple Q&A)

```bash
./run.sh --provider ollama --rebuild
```

**What it does:**
- Loads documents (PDFs + audio)
- Builds vector database
- Answers questions using RAG
- No agent features

### 2. Agent Mode (Full Features) ⭐ RECOMMENDED

```bash
./run.sh --provider ollama --agent-mode --rebuild
```

**What it does:**
- Everything in Basic Mode, PLUS:
- 🧠 Autonomous reasoning
- 🔁 Self-reflection
- 🔧 Tool-calling
- 📊 Performance evaluation
- 📈 Detailed metrics

### 3. Self-Analysis Mode (Generate LinkedIn Post)

```bash
./run.sh --provider ollama --agent-mode --self-analyze
```

**What it does:**
- Analyzes its own codebase
- Generates project statistics
- Creates architecture analysis
- **Auto-generates LinkedIn post**
- Saves to `linkedin_post.txt`

### 4. Use Existing Database (Skip Rebuild)

```bash
./run.sh --provider ollama --agent-mode
```

**Use this when:**
- You've already built the database once
- You just want to test queries
- Faster startup (skips data loading)

---

## 🦙 Ollama Setup (Required for Local LLM)

### Install Ollama

```bash
brew install ollama
```

### Start Ollama Service

```bash
# In a separate terminal window
ollama serve
```

Keep this running in the background.

### Pull a Model

```bash
# Choose one:
ollama pull llama2           # Balanced (recommended)
ollama pull mistral          # Faster, smaller
ollama pull llama3.2         # More capable
```

### Verify Ollama is Running

```bash
curl http://localhost:11434/api/tags
```

You should see a JSON response with available models.

---

## 🧪 Testing the System

### Interactive Commands

When you run the chatbot, after test questions you'll enter interactive mode:

```
Enter your question (or 'quit' to exit):
```

**Available Commands:**

| Command | Description | Example |
|---------|-------------|---------|
| `<your question>` | Ask anything | `What is RAG?` |
| `/agent <query>` | Use full agent mode | `/agent Explain agentic AI threats` |
| `/analyze` | Analyze codebase | `/analyze` |
| `/report` | Performance report | `/report` |
| `/linkedin` | Generate LinkedIn post | `/linkedin` |
| `exit` or `quit` | Exit program | `quit` |

### Example Session

```bash
You: What are the top threats in Agentic AI?

[Answer with sources displayed]

You: /agent Summarize the CIS controls

[Agent performs reasoning, retrieval, self-reflection, evaluation]

You: /linkedin

[Generates LinkedIn post]

You: quit
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "externally-managed-environment" Error

**Problem:** You're using system Python instead of venv.

**Solution:**
```bash
# Always activate venv first!
source venv311/bin/activate

# OR use the helper script
./run.sh --provider ollama --agent-mode
```

### Issue 2: "Ollama connection failed"

**Problem:** Ollama service is not running.

**Solution:**
```bash
# In a new terminal
ollama serve

# Then in another terminal, pull a model
ollama pull llama2

# Verify it's running
curl http://localhost:11434/api/tags
```

### Issue 3: "No documents found"

**Problem:** No PDFs or audio files in data directories.

**Solution:**
```bash
# Check data directories
ls data/pdfs/
ls data/audio/

# You should have files there. If not, add your documents and run with --rebuild
```

### Issue 4: "Module not found" Error

**Problem:** Dependencies not installed or wrong Python.

**Solution:**
```bash
# Activate venv
source venv311/bin/activate

# Verify Python version
python --version  # Should be 3.11.x

# Reinstall dependencies if needed
pip install -r requirements.txt
```

### Issue 5: ChromaDB Error

**Problem:** Corrupted vector database.

**Solution:**
```bash
# Delete database and rebuild
rm -rf chroma_db/
./run.sh --provider ollama --rebuild
```

---

## 📊 What to Expect

### First Run (with --rebuild)

```
======================================================================
🤖 AI-Agentic RAG Chatbot - Using OLLAMA
✨ Agent Mode: ENABLED
======================================================================

[1/4] Loading documents...
Processing PDF: AI-Threats.pdf
Processing PDF: CIS_Controls_Guide_v8.1.2_0325_v2.pdf
Transcribing audio: AWS Summit London 2025...

Total documents loaded: 45

[2/4] Chunking documents...
Created 287 chunks

[3/4] Building vector database...
✓ Added 287 documents to ChromaDB

[4/4] Initializing ollama provider...

🚀 Initializing AI Agent...
   ✓ Agent tools loaded
   ✓ Reasoner initialized
   ✓ Evaluator initialized

======================================================================
Running Test Questions
======================================================================

[Test questions run automatically...]

======================================================================
Interactive Mode
======================================================================
Enter your question (or 'quit' to exit):
```

### Agent Mode Output Example

```
─────────────────────────────────────────
Question 1: What are top threats in Agentic AI?
─────────────────────────────────────────

🧠 Step 1: Reasoning...
   → Query type: information
   → Required tools: []
   → Confidence: 0.85

📚 Step 2: Retrieving relevant information...
   → Retrieved 3 documents
   → Top relevance score: 0.892

💬 Step 3: Generating response...
   → Response generated (520 chars)

🔁 Step 4: Self-Reflection...
   → Quality score: 0.87
   → Strengths: Comprehensive coverage, Used high-quality sources
   → Improvements: Could include more examples

📊 Step 5: Evaluation...
   → Retrieval accuracy: 0.89
   → Response relevance: 0.87
   → Overall score: 0.88

Answer:
[Detailed answer based on your documents...]

Sources:
  • AI-Threats.pdf (Page 5, Score: 0.892)
  • AI-Threats.pdf (Page 12, Score: 0.845)
  • AI-Threats.pdf (Page 3, Score: 0.823)
```

---

## 📈 Performance Reports

After running in agent mode, you'll get performance reports:

```
======================================================================
📈 Final Performance Report
======================================================================

Total Interactions: 5
Total Evaluations: 5

Average Performance Scores:
   retrieval_accuracy: 0.87
   response_relevance: 0.84
   tool_accuracy: 0.91
   reasoning_quality: 0.82
   overall_score: 0.86

💾 Exporting detailed reports...
   ✓ reports/evaluator_report.json
   ✓ reports/reasoner_report.json
```

Check these files for detailed analysis!

---

## 🎬 For Demo Video

### Recommended Recording Flow (5 minutes)

**Part 1: Setup (30 sec)**
```bash
cd /Users/shha/Documents/Module4Assignment/rag-chatbot-module4-assignment
ls data/pdfs/    # Show your documents
ls data/audio/   # Show audio files
```

**Part 2: Agent Mode Demo (2 min)**
```bash
./run.sh --provider ollama --agent-mode --rebuild

# Let it run through test questions
# Show reasoning steps, self-reflection, evaluation
```

**Part 3: Interactive Commands (1.5 min)**
```bash
# In interactive mode:
/agent What are the main security controls?
/analyze
/report
```

**Part 4: Self-Analysis (1 min)**
```bash
./run.sh --provider ollama --agent-mode --self-analyze

# Show generated LinkedIn post
cat linkedin_post.txt
```

---

## ✅ Quick Checklist

Before running:
- [ ] Ollama service is running (`ollama serve`)
- [ ] At least one model is pulled (`ollama pull llama2`)
- [ ] Data files exist in `data/pdfs/` and `data/audio/`
- [ ] Virtual environment activated OR using `run.sh`

---

## 💡 Pro Tips

1. **First run takes time** - Downloads models, processes documents (~5-10 min)
2. **Use `--rebuild` only once** - Then omit it for faster startups
3. **Agent mode is impressive** - Shows all features for demo
4. **Self-analysis is demo-ready** - Perfect for video showcase
5. **Check logs** - `logs/agent_results.log` has detailed execution logs

---

## 🎯 Next Steps

1. ✅ Run basic test: `./run.sh --provider ollama --rebuild`
2. ✅ Try agent mode: `./run.sh --provider ollama --agent-mode`
3. ✅ Generate LinkedIn post: `./run.sh --provider ollama --agent-mode --self-analyze`
4. ✅ Record demo video
5. ✅ Submit assignment

---

## 📞 Need Help?

If you encounter issues:
1. Check this guide's troubleshooting section
2. Verify virtual environment is activated
3. Ensure Ollama is running
4. Check `logs/agent_results.log` for errors
5. Try deleting `chroma_db/` and rebuilding

---

**You're ready to go! 🚀**

Start with: `./run.sh --provider ollama --agent-mode --rebuild`
