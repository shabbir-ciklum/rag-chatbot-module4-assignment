#!/bin/bash
# Helper script to run the RAG Chatbot with venv311

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv311/bin/activate

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"
echo "✅ Python version: $(python --version)"
echo ""

# Run the main script with all arguments passed to this script
python main.py "$@"
