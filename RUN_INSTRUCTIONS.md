# 🎯 EXACT COMMANDS TO RUN YOUR CHATBOT

## ✅ Fixed: The "externally-managed-environment" Error

**Problem:** You were using system Python (3.14) instead of the virtual environment Python (3.11).

**Solution:** Always activate `venv311` OR use the helper script `run.sh`.

---

## 🚀 OPTION 1: Using Helper Script (Easiest)

I've created a helper script that automatically activates the virtual environment for you.

### First Time Setup (one command)

```bash
chmod +x run.sh
```

### Run the Chatbot

```bash
# Full agent mode (RECOMMENDED for demo)
./run.sh --provider ollama --agent-mode --rebuild

# Basic RAG mode
./run.sh --provider ollama --rebuild

# Self-analysis (generates LinkedIn post)
./run.sh --provider ollama --agent-mode --self-analyze

# Use existing database (faster, no rebuild)
./run.sh --provider ollama --agent-mode
```

---

## 🚀 OPTION 2: Manual Activation

If you prefer to activate manually:

```bash
# Step 1: Activate virtual environment
source venv311/bin/activate

# Step 2: Verify (should show Python 3.11.x)
python --version

# Step 3: Run chatbot
python main.py --provider ollama --agent-mode --rebuild
```

---

## 📝 What I Fixed

1. **Updated `requirements.txt`** - Removed invalid `ast-parser` package (ast is built-in)
2. **Installed all dependencies** in `venv311` - All packages now working
3. **Created `run.sh` helper script** - Automatically handles venv activation
4. **Updated README.md** - Added clear venv activation instructions
5. **Created QUICKSTART.md** - Comprehensive guide with examples

---

## ✅ Verification

Everything is ready to go! Test with:

```bash
# Verify packages are installed
venv311/bin/python -c "import langchain; import chromadb; import groq; print('✅ Ready!')"
```

Expected output: `✅ Ready!`

---

## 🎬 For Your Demo Video - EXACT SEQUENCE

### Terminal 1: Start Ollama

```bash
ollama serve
```

Leave this running.

### Terminal 2: Run Chatbot

```bash
cd /Users/shha/Documents/Module4Assignment/rag-chatbot-module4-assignment

# Show what data you have
echo "PDFs:"
ls data/pdfs/
echo ""
echo "Audio files:"
ls data/audio/

# Run with full agent mode
./run.sh --provider ollama --agent-mode --rebuild
```

This will:
1. Load your PDFs and audio files
2. Chunk documents
3. Build vector database
4. Run 3 test questions automatically
5. Show reasoning, self-reflection, evaluation for each
6. Enter interactive mode

### In Interactive Mode

```
You: /agent What are the main security controls?

[Shows full agent workflow]

You: /analyze

[Analyzes the codebase]

You: /report

[Shows performance metrics]

You: quit
```

### Generate LinkedIn Post

```bash
./run.sh --provider ollama --agent-mode --self-analyze

# View the generated post
cat linkedin_post.txt
```

---

## 🎯 Summary Commands

```bash
# START HERE - Full demo
./run.sh --provider ollama --agent-mode --rebuild

# If you already built database once
./run.sh --provider ollama --agent-mode

# Generate LinkedIn post
./run.sh --provider ollama --agent-mode --self-analyze
```

---

## 🆘 If You Get Errors

### "externally-managed-environment"
**Fix:** Use `./run.sh` or activate venv: `source venv311/bin/activate`

### "No module named 'src.chatbot_updated'"
**Fix:** Already fixed! The import now correctly uses `src.chatbot`

### "TypeError: 'set' object is not subscriptable"
**Fix:** Already fixed! Updated evaluator.py to properly handle set objects

### "Ollama connection failed"
**Fix:** Run `ollama serve` in another terminal, then `ollama pull llama2`

### "No documents found"
**Fix:** Check `data/pdfs/` and `data/audio/` have files

### "Module not found" or import errors
**Fix:** `source venv311/bin/activate && pip install -r requirements.txt`

### ChromaDB error
**Fix:** `rm -rf chroma_db/ && ./run.sh --provider ollama --rebuild`

---

## ✨ You're All Set!

The error is fixed. Just run:

```bash
./run.sh --provider ollama --agent-mode --rebuild
```

This will showcase all your agent features perfectly for the demo! 🚀
