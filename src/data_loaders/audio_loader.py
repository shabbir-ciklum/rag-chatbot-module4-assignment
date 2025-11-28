"""
Audio Loader - Transcribes audio/video using Whisper.
Runs completely locally, no API needed.
"""

import whisper
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")


class AudioLoader:
  SUPPORTED_FORMATS = {'.mp3', '.mp4', '.wav', '.m4a', '.webm', '.flac', '.ogg'}

  def __init__(self, model_size: str = "base"):
    """
    model_size options: tiny, base, small, medium, large
    Larger = more accurate but slower
    """
    print(f"  Loading Whisper '{model_size}' model...")
    self.model = whisper.load_model(model_size)

  def transcribe_file(self, audio_path: str):
    """Transcribe a single audio/video file."""
    path = Path(audio_path)
    print(f"  Transcribing {path.name}... (this may take a while)")
    
    result = self.model.transcribe(str(path), language="en", verbose=False)
    
    return {
      "content": result["text"].strip(),
      "metadata": {
        "source": path.name,
        "type": "audio"
      }
    }

  def load_directory(self, directory: str):
    """Load all audio files from a directory."""
    dir_path = Path(directory)
    documents = []
    
    audio_files = [
      f for f in dir_path.iterdir()
      if f.suffix.lower() in self.SUPPORTED_FORMATS
    ]
    
    for audio_file in audio_files:
      try:
        doc = self.transcribe_file(str(audio_file))
        documents.append(doc)
        print(f"  ✓ Transcribed: {audio_file.name}")
      except Exception as e:
        print(f"  ✗ Error: {audio_file.name}: {e}")
    
    return documents