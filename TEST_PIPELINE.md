# RAG Pipeline Testing Guide

This guide will walk you through testing the complete RAG (Retrieval-Augmented Generation) pipeline.

## Prerequisites

1. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install Ollama** (if using ollama provider):
   ```bash
   # On macOS
   brew install ollama

   # Start ollama service
   ollama serve

   # In another terminal, pull a model
   ollama pull llama2
   # or
   ollama pull mistral
   ```

3. **Check your data**:
   ```bash
   ls data/pdfs/     # Should have PDF files
   ls data/audio/    # Should have audio files
   ```

## Test 1: Quick Component Test

Test individual components with the test scripts we created:

```bash
# Test the chunker
python tests/test_text_chunker.py

# Test the vector store
python tests/test_chroma_store.py

# Test the full pipeline (without LLM)
python tests/test_full_pipeline.py
```

## Test 2: Run Main Pipeline (No Rebuild)

If you already have data indexed, test retrieval:

```bash
python main.py
```

This will:
- Load existing vector database
- Initialize Ollama (default provider)
- Run 3 test questions
- Enter interactive mode

## Test 3: Rebuild Vector Database

To rebuild the vector database from scratch:

```bash
python main.py --rebuild
```

This will:
1. **Load documents** from `data/pdfs/` and `data/audio/`
2. **Chunk documents** using SemanticChunker
3. **Generate embeddings** using sentence-transformers
4. **Store in ChromaDB** vector database
5. **Run test questions**
6. **Interactive mode**

## Test 4: Use Different LLM Providers

### Using Ollama (default):
```bash
python main.py --provider ollama --model llama2
```

### Using Groq (requires API key):
```bash
# Set API key in .env file
echo "GROQ_API_KEY=your_key_here" >> .env

python main.py --provider groq --model llama-3.1-70b-versatile
```

### Using Gemini (requires API key):
```bash
# Set API key in .env file
echo "GEMINI_API_KEY=your_key_here" >> .env

python main.py --provider gemini --model gemini-pro
```

## Test 5: Interactive Testing

After running main.py, you'll enter interactive mode:

```
Enter your question (or 'quit' to exit): What is RAG?
```

Try these test questions:
- "What are the production 'Do's' for RAG?"
- "What is the difference between standard retrieval and the ColPali approach?"
- "Why is hybrid search better than vector-only search?"
- "Explain the key concepts from the audio file"

## Test 6: Verify Each Component

### Check Vector Database:
```python
from src.vectorstore.chroma_store import ChromaVectorStore

store = ChromaVectorStore()
print(f"Total chunks: {store.collection.count()}")

# Test search
results = store.search("What is RAG?", n_results=3)
for r in results:
    print(f"Score: {r['score']:.3f} - {r['content'][:100]}...")
```

### Check Document Loading:
```bash
python -c "
from pathlib import Path
from src.data_loaders.pdf_loader import PDFLoader

pdf_files = list(Path('data/pdfs').glob('*.pdf'))
print(f'Found {len(pdf_files)} PDFs')

if pdf_files:
    loader = PDFLoader(str(pdf_files[0]))
    docs = loader.load()
    print(f'Loaded {len(docs)} pages from {pdf_files[0].name}')
"
```

### Check Audio Transcription:
```bash
python -c "
from pathlib import Path
from src.data_loaders.audio_loader import AudioLoader

audio_files = list(Path('data/audio').glob('*'))
print(f'Found {len(audio_files)} audio files')

if audio_files:
    loader = AudioLoader(model_size='tiny')
    doc = loader.transcribe_file(str(audio_files[0]))
    print(f'Transcribed {len(doc[\"content\"])} characters')
"
```

## Expected Output

### Successful Pipeline Run:

```
============================================================
RAG Chatbot - Using OLLAMA
============================================================

✓ Using existing database with 150 chunks

Initializing ollama provider...

============================================================
Running Test Questions
============================================================

──────────────────────────────────────────────────
Question 1: What are the production 'Do's' for RAG?
──────────────────────────────────────────────────

Answer:
[Answer from LLM based on retrieved context]

Sources:
  • document.pdf (Page 5, Score: 0.872)
  • document.pdf (Page 12, Score: 0.845)
  • document.pdf (Page 3, Score: 0.823)

...

============================================================
Interactive Mode
============================================================
Enter your question (or 'quit' to exit):
```

## Troubleshooting

### Error: No documents found
- Add PDF files to `data/pdfs/`
- Add audio files to `data/audio/`
- Run with `--rebuild` flag

### Error: Ollama connection failed
```bash
# Start ollama service
ollama serve

# Pull a model
ollama pull llama2
```

### Error: Module not found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: ChromaDB initialization failed
```bash
# Delete and rebuild
rm -rf chroma_db/
python main.py --rebuild
```

## Performance Tips

1. **First run will be slow** - Downloads models, processes documents
2. **Subsequent runs are fast** - Uses cached embeddings
3. **Use smaller audio model** for faster transcription: `model_size="tiny"`
4. **Adjust chunk size** for better retrieval: Edit `chunk_size` in main.py

## Logs

Check logs for detailed information:
```bash
cat logs/test_results.log
```

## Next Steps

After successful testing:
1. Add more documents to `data/pdfs/` and `data/audio/`
2. Run `python main.py --rebuild` to reindex
3. Customize test questions in `main.py`
4. Adjust chunking parameters for better results
5. Experiment with different LLM providers