# local-llm

LocalLLM is a small knowledge assistant for FIR / RWTH dissertations.
It runs locally, uses Qdrant for vector search and Ollama for the LLM, and exposes
both a Streamlit UI and a small FastAPI backend.

## Features

- **PDF ingestion**  
  Reads local FIR dissertations (PDF) from `data/` and splits them into overlapping chunks.

- **Embeddings + Qdrant**  
  Uses a SentenceTransformers model and stores vectors + metadata in a Qdrant collection.

- **LangChain RAG**  
  Simple RAG chain on top of Qdrant and an Ollama chat model.

- **CLI, API, UI**  
  Typer CLI, FastAPI endpoint, and a Streamlit chat interface.

## Quick start

Install (ideally in a virtualenv):

```bash
pip install -e .
```

Ingest the PDFs under `data/` into Qdrant (local server or docker-compose):

```bash
local-llm ingest
```

Ask a question on the command line:

```bash
local-llm query "Worum geht es in der Dissertation von Spiss?"
```

Or run the full stack with Docker:

```bash
docker compose up --build
```

This starts:

- Qdrant on `localhost:6333`
- FastAPI backend on `localhost:8000`
- Streamlit UI on `localhost:8501`

## Configuration

Main settings are loaded from environment variables (see `.env.example`), all prefixed
with `LOCAL_LLM_`. The most important ones:

- `LOCAL_LLM_QDRANT_URL` – Qdrant URL (default `http://localhost:6333`)
- `LOCAL_LLM_QDRANT_COLLECTION_NAME` – collection name (default `fir_dissertations`)
- `LOCAL_LLM_OLLAMA_MODEL` – chat model name (default `mistral`)
- `LOCAL_LLM_OLLAMA_BASE_URL` – Ollama base URL (default `http://localhost:11434`)

## Development

Basic workflow:

```bash
make venv
source .venv/bin/activate
make install
make test
```

The code lives under `src/localllm/` and is intentionally small and explicit. The goal
is to be easy to read and adapt for other small internal knowledge bases.

