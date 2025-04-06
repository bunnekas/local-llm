"""
localllm – lightweight local RAG assistant for FIR dissertations.

This package exposes a small, focused API around:

- configuration (`Settings`)
- ingestion (`load_pdfs`, `chunk_documents`)
- vector store (`get_vectorstore`)
- RAG chain (`build_rag_chain`)
"""

from .config import Settings  # noqa: F401

