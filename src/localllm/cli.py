"""Typer CLI for local-llm."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich import print

from .chain import append_to_history, run_rag_chain
from .config import get_settings
from .ingestion import iter_chunks_from_pdfs, load_pdfs
from .vectorstore import ingest_chunks

app = typer.Typer(help="local-llm – query FIR dissertations locally.")


@app.command()
def ingest(
    data_dir: Optional[Path] = typer.Argument(
        None,
        help="Directory with PDF files (defaults to configured data_dir).",
    ),
) -> None:
    """Ingest PDFs into Qdrant."""

    settings = get_settings()
    if data_dir is not None:
        # override for this run only
        settings.data_dir = data_dir  # type: ignore[attr-defined]

    pdfs = load_pdfs(settings.data_dir)
    if not pdfs:
        print("[yellow]no pdf files found – nothing to do[/yellow]")
        raise typer.Exit(code=1)

    print(f"[green]ingesting {len(pdfs)} pdf files from {settings.data_dir}[/green]")
    count = ingest_chunks(iter_chunks_from_pdfs())
    print(f"[green]stored {count} chunks in collection '{settings.qdrant_collection_name}'[/green]")


@app.command()
def query(
    question: Optional[str] = typer.Argument(
        None,
        help="Question to ask. If omitted, starts an interactive prompt.",
    ),
) -> None:
    """Ask a question on the command line."""

    history: list = []

    def ask_once(q: str) -> None:
        result = run_rag_chain(q, history)
        answer = result.get("answer") or result.get("output_text") or ""
        append_to_history(history, q, answer)
        print("\n[bold]Answer:[/bold]")
        print(answer)

    if question:
        ask_once(question)
        return

    print("[green]interactive mode – type 'exit' to quit[/green]")
    while True:
        q = input("\n> ")
        if not q or q.lower() in {"exit", "quit"}:
            break
        ask_once(q)


@app.command("serve-api")
def serve_api() -> None:
    """Run the FastAPI server."""

    import uvicorn

    uvicorn.run("localllm.api.main:app", host="0.0.0.0", port=8000, reload=False)


@app.command("serve-ui")
def serve_ui(
    api_url: str = typer.Option(
        "http://localhost:8000",
        "--api-url",
        help="Base URL of the FastAPI backend.",
    ),
) -> None:
    """Run the Streamlit UI."""

    # Pass API URL via env var so the Streamlit app can pick it up
    import os
    import subprocess

    env = os.environ.copy()
    env["LOCAL_LLM_API_URL"] = api_url
    subprocess.run(
        ["streamlit", "run", "src/localllm/ui/app.py"],
        env=env,
        check=True,
    )


if __name__ == "__main__":
    app()

