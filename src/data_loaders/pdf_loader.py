"""
PDF Loader - Extracts text from PDF files.
Uses PyMuPDF as primary, pdfplumber as fallback.
"""

import fitz
import pdfplumber
from pathlib import Path
import re


class PDFLoader:
  def __init__(self, pdf_path: str):
    self.pdf_path = Path(pdf_path)
    if not self.pdf_path.exists():
      raise FileNotFoundError(f"PDF not found: {pdf_path}")

  def _clean_text(self, text: str) -> str:
    """Clean up common PDF extraction artifacts."""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove standalone page numbers
    text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
    return text.strip()

  def load(self):
    """Extract text from PDF, returns list of documents."""
    documents = []
        
    with fitz.open(self.pdf_path) as doc:
      for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        text = self._clean_text(text)
          
        if text.strip():
          documents.append({
            "content": text,
            "metadata": {
              "source": self.pdf_path.name,
              "page": page_num,
              "type": "pdf"
            }
          })
    
    print(f"  ✓ Extracted {len(documents)} pages from {self.pdf_path.name}")
    return documents