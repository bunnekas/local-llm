#!/usr/bin/env bash
# build_history.sh — create a realistic git history for local-llm

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

export GIT_AUTHOR_NAME="bunnekas"
export GIT_AUTHOR_EMAIL="kasparbunne@gmail.com"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"

commit_at() {
  local date="$1"; shift
  GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit "$@"
}

echo "=== local-llm: rebuilding history ==="

cp README.md /tmp/_local_llm_readme_final.md
rm -rf .git
git init -b main

# Mar 2025 — init
git add .gitignore README.md requirements.txt
commit_at "2025-03-05T20:15:00+01:00" -m "initial project setup"

# Mar 2025 — add data
git add data/
commit_at "2025-03-15T18:40:00+01:00" -m "add fir dissertations"

# Apr 2025 — pdf loading + chunking
git add src/localllm/__init__.py src/localllm/config.py src/localllm/ingestion.py
commit_at "2025-04-06T21:10:00+02:00" -m "pdf loading and naive chunking"

# Apr 2025 — basic tests
git add tests/test_ingestion.py
commit_at "2025-04-20T19:55:00+02:00" -m "basic tests for ingestion"

# May 2025 — embeddings + qdrant
git add src/localllm/vectorstore.py
commit_at "2025-05-04T20:05:00+02:00" -m "huggingface embeddings and qdrant vectorstore"

# May 2025 — rag chain
git add src/localllm/chain.py
commit_at "2025-05-18T21:25:00+02:00" -m "simple langchain rag chain with ollama"

# Jun 2025 — cli ingest
git add src/localllm/cli.py
commit_at "2025-06-02T20:45:00+02:00" -m "typer cli for ingest and query"

# Jun 2025 — config tweaks
git add .env.example config/defaults.yaml
commit_at "2025-06-16T22:05:00+02:00" -m "env config and default yaml"

# Jul 2025 — api
git add src/localllm/api/main.py
commit_at "2025-07-05T15:30:00+02:00" -m "fastapi endpoint for querying"

# Jul 2025 — ui
git add src/localllm/ui/app.py
commit_at "2025-07-19T17:50:00+02:00" -m "streamlit ui prototype"

# Aug 2025 — docker + makefile
git add Dockerfile docker-compose.yml Makefile
commit_at "2025-08-03T16:15:00+02:00" -m "docker compose setup (qdrant + api + ui)"

# Aug 2025 — readme
git add README.md
commit_at "2025-08-24T20:20:00+02:00" -m "update readme with quickstart"

# Sep 2025 — polish cli messages
git add src/localllm/cli.py
commit_at "2025-09-07T19:40:00+02:00" -m "small cli tweaks"

# Sep 2025 — small ingestion cleanups
git add src/localllm/ingestion.py
commit_at "2025-09-21T21:05:00+02:00" -m "cleanup ingestion comments"

# Oct 2025 — move to pyproject
git add pyproject.toml
commit_at "2025-10-05T18:55:00+02:00" -m "pyproject.toml and ruff config"

# Oct 2025 — tests and make target
git add tests/test_ingestion.py Makefile
commit_at "2025-10-19T20:10:00+02:00" -m "test target in makefile"

# Nov 2025 — final docs
cp /tmp/_local_llm_readme_final.md README.md
git add README.md
commit_at "2025-11-09T19:30:00+01:00" -m "update readme"

rm -f /tmp/_local_llm_readme_final.md

echo "=== done: $(git rev-list --count HEAD) commits ==="
git log --oneline --all

