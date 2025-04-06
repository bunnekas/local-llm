"""PDF loading and text chunking for FIR dissertations.

This stays intentionally simple: we read PDFs with pdfplumber, extract
page text, and then apply naive character-based chunking with overlap.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import pdfplumber

from .config import get_settings


@dataclass
class DocumentChunk:
    """Single chunk of text with minimal metadata."""

    text: str
    source: str
    page: int


def load_pdfs(data_dir: Path | str | None = None) -> List[Path]:
    """Return all PDF files under data_dir."""

    settings = get_settings()
    root = Path(data_dir) if data_dir is not None else settings.data_dir
    return sorted(p for p in root.glob("*.pdf") if p.is_file())


def extract_text_from_pdf(path: Path) -> List[str]:
    """Extract raw text per page from a PDF file."""

    pages: List[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            pages.append(txt)
    return pages


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> List[str]:
    """Simple character-based chunking with overlap."""

    settings = get_settings()
    size = chunk_size or settings.chunk_size
    overlap = chunk_overlap or settings.chunk_overlap

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


def iter_chunks_from_pdfs() -> Iterable[DocumentChunk]:
    """Iterate over chunks from all PDFs in the configured data dir."""

    settings = get_settings()
    for pdf_path in load_pdfs(settings.data_dir):
        pages = extract_text_from_pdf(pdf_path)
        for page_idx, page_text in enumerate(pages, start=1):
            for chunk in chunk_text(page_text):
                yield DocumentChunk(
                    text=chunk,
                    source=pdf_path.name,
                    page=page_idx,
                )

