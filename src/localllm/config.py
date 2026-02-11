"""Configuration for local-llm using Pydantic settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file.

    Environment variables are prefixed with LOCAL_LLM_ by default, e.g.:
    - LOCAL_LLM_QDRANT_URL
    - LOCAL_LLM_COLLECTION_NAME
    - LOCAL_LLM_OLLAMA_MODEL
    """

    # Paths
    data_dir: Path = Field(default=Path("data"))

    # Qdrant
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_api_key: str | None = None
    qdrant_collection_name: str = Field(default="fir_dissertations")

    # Embeddings
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    embedding_batch_size: int = Field(default=32)

    # Chunking
    chunk_size: int = Field(default=900, description="Number of characters per chunk")
    chunk_overlap: int = Field(default=150, description="Overlap between chunks")

    # LLM
    llm_provider: str = Field(
        default="ollama",
        description="LLM provider to use: 'ollama' or 'openai'",
    )

    # Ollama
    ollama_model: str = Field(default="mistral")
    ollama_base_url: str = Field(default="http://localhost:11434")

    # OpenAI or OpenAI-compatible HTTP API
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the OpenAI-compatible API",
    )
    openai_api_key: str | None = Field(
        default=None,
        description="API key for the OpenAI-compatible API",
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        description="Model name for the OpenAI-compatible API",
    )

    class Config:
        env_prefix = "LOCAL_LLM_"
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()

