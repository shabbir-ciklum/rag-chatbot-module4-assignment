#!/bin/bash

# RAG Chatbot Setup Script
# This script sets up the Python virtual environment and installs all dependencies

set -e  # Exit on error

echo "🚀 Setting up RAG Chatbot environment..."
echo ""

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg is not installed. Installing via Homebrew..."
    brew install ffmpeg
else
    echo "✓ ffmpeg is already installed"
fi

# Determine Python version to use
# Note: Using Python 3.11 because PyTorch (required by openai-whisper) doesn't have wheels for 3.13+ yet
PYTHON_CMD="python3.11"

if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "⚠️  Python 3.11 not found, trying python3..."
    PYTHON_CMD="python3"

    # Check if the found version is compatible
    PY_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    PY_MAJOR=$(echo $PY_VERSION | cut -d. -f1)
    PY_MINOR=$(echo $PY_VERSION | cut -d. -f2)

    if [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -ge 13 ]; then
        echo "❌ Python $PY_VERSION is too new. This project requires Python 3.10-3.12"
        echo "   (PyTorch doesn't have pre-built wheels for Python 3.13+ yet)"
        echo ""
        echo "Please install Python 3.11:"
        echo "  brew install python@3.11"
        exit 1
    fi
fi

echo "✓ Using $PYTHON_CMD ($($PYTHON_CMD --version))"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To test the audio loader, run:"
echo "  python"
echo "  >>> from src.data_loaders.audio_loader import AudioLoader"
echo ""
