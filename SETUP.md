# Setup Guide

This guide will help you set up the RAG Chatbot project environment.

## Prerequisites

- **Python 3.11 or 3.12** (NOT 3.13 or 3.14)
  - Python 3.13+: PyTorch doesn't have pre-built wheels yet
  - Python 3.14: numba doesn't support it
- Homebrew (for macOS)

## Quick Setup (Recommended)

Run the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
1. Install `ffmpeg` (required for audio processing)
2. Create a Python virtual environment
3. Install all required dependencies

## Manual Setup

If you prefer to set up manually:

### 1. Install ffmpeg

```bash
brew install ffmpeg
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
```

Or use your preferred Python version:
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

### Activate the Environment

Every time you work on this project, activate the virtual environment first:

```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Deactivate the Environment

When you're done working:

```bash
deactivate
```

## Testing the Setup

Test that the audio loader works:

```bash
python
```

Then in the Python REPL:
```python
from src.data_loaders.audio_loader import AudioLoader
loader = AudioLoader(model_size="base")
print("✓ Audio loader imported successfully!")
```

## Dependencies

The project uses these main packages:

- **openai-whisper** - Audio transcription (runs locally)
- **pymupdf** & **pdfplumber** - PDF processing
- **sentence-transformers** - Text embeddings
- **chromadb** - Vector database
- **ollama** - LLM integration
- **langchain-text-splitters** - Text chunking
- **python-dotenv** - Environment variables
- **tqdm** - Progress bars

## Troubleshooting

### "externally-managed-environment" Error

This means you're trying to install packages system-wide. Always use a virtual environment:

```bash
source venv/bin/activate
pip install <package>
```

### "No module named 'whisper'" Error

Make sure:
1. Virtual environment is activated (`source venv/bin/activate`)
2. Dependencies are installed (`pip install -r requirements.txt`)

### ffmpeg Not Found

Install via Homebrew:
```bash
brew install ffmpeg
```

## Notes

- The first time you use Whisper, it will download model files (~100-500MB depending on model size)
- Different Python versions require different virtual environments
- Don't commit the `venv` folder to git (it's in `.gitignore`)
