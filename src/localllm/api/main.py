"""FastAPI backend for local-llm."""

from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from ..chain import append_to_history, run_rag_chain
from ..config import get_settings

app = FastAPI(title="local-llm API")


class QueryRequest(BaseModel):
    question: str
    chat_history: Optional[List[str]] = None
    source: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str


@app.get("/health")
async def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "llm_provider": settings.llm_provider,
        "qdrant_url": settings.qdrant_url,
        "qdrant_collection": settings.qdrant_collection_name,
        "embedding_model": settings.embedding_model,
    }


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest) -> QueryResponse:
    history = []
    if req.chat_history:
        # simple reconstruction – we only keep alternating user / ai messages
        from langchain_core.messages import HumanMessage

        for msg in req.chat_history:
            history.append(HumanMessage(content=msg))

    result = run_rag_chain(req.question, history, source_filter=req.source)
    answer = result.get("answer") or result.get("output_text") or ""
    return QueryResponse(answer=answer)

