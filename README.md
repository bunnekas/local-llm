# local-llm

LocalLLM is a small knowledge assistant for FIR / RWTH dissertations.
It uses Qdrant for vector search and a pluggable LLM provider (Ollama or OpenAI)
and exposes both a Streamlit UI and a small FastAPI backend.

## Features

- **PDF ingestion**  
  Reads local FIR dissertations (PDF) from `data/` and splits them into overlapping chunks.

- **Embeddings + Qdrant**  
  Uses a SentenceTransformers model and stores vectors + metadata in a Qdrant collection.

- **LangChain RAG**  
  Simple RAG chain on top of Qdrant and a chat model (Ollama or OpenAI).

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
- `LOCAL_LLM_LLM_PROVIDER` – LLM provider: `ollama` (default) or `openai`
- `LOCAL_LLM_OLLAMA_MODEL` – Ollama chat model name (default `mistral`)
- `LOCAL_LLM_OLLAMA_BASE_URL` – Ollama base URL (default `http://localhost:11434`)
- `LOCAL_LLM_OPENAI_BASE_URL` – OpenAI(-compatible) base URL (default `https://api.openai.com/v1`)
- `LOCAL_LLM_OPENAI_API_KEY` – API key for OpenAI(-compatible) API
- `LOCAL_LLM_OPENAI_MODEL` – OpenAI(-compatible) model name (default `gpt-4o-mini`)

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

## Running with OpenAI (no Ollama / Docker needed)

If you are on a machine without Docker or Ollama, you can run the assistant
against a small OpenAI model (or any OpenAI-compatible HTTP API).

1. Install the package (ideally in a virtualenv):

```bash
pip install -e .
```

2. Create a `.env` file (or export env vars) with at least:

```bash
LOCAL_LLM_LLM_PROVIDER=openai
LOCAL_LLM_OPENAI_API_KEY=sk-...
# optional overrides:
# LOCAL_LLM_OPENAI_MODEL=gpt-4o-mini
# LOCAL_LLM_OPENAI_BASE_URL=https://api.openai.com/v1
```

3. Ingest the PDFs into Qdrant (this only uses embeddings, no LLM calls):

```bash
local-llm ingest
```

4. Ask a question on the command line using the OpenAI provider:

```bash
local-llm query "Worum geht es in der Dissertation von Spiss?"
```

5. Or run the API and UI locally (two terminals):

```bash
# terminal 1
local-llm serve-api

# terminal 2
LOCAL_LLM_LLM_PROVIDER=openai local-llm serve-ui
```

The Streamlit UI talks to the FastAPI backend, which in turn calls the selected
LLM provider (Ollama or OpenAI) and Qdrant for retrieval.

