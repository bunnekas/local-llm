"""Qdrant vector store helpers using LangChain."""

from __future__ import annotations

from typing import Iterable, List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from .config import get_settings
from .ingestion import DocumentChunk


def _get_client() -> QdrantClient:
    settings = get_settings()
    # For now we always use server mode; embedded mode can be added later.
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)


def _get_embeddings() -> HuggingFaceEmbeddings:
    settings = get_settings()
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)


def get_vectorstore() -> QdrantVectorStore:
    """Return a LangChain QdrantVectorStore instance."""

    settings = get_settings()
    client = _get_client()
    embeddings = _get_embeddings()
    return QdrantVectorStore(
        client=client,
        collection_name=settings.qdrant_collection_name,
        embedding=embeddings,
    )


def ingest_chunks(chunks: Iterable[DocumentChunk]) -> int:
    """Ingest chunks into Qdrant, returning number of stored chunks."""

    vs = get_vectorstore()
    texts: List[str] = []
    metadatas: List[dict] = []

    for c in chunks:
        texts.append(c.text)
        metadatas.append({"source": c.source, "page": c.page})

    if not texts:
        return 0

    vs.add_texts(texts=texts, metadatas=metadatas)
    return len(texts)

