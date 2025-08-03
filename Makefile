default:
	@echo "available targets: venv, install, ingest, api, ui, test"

venv:
	python -m venv .venv

install:
	pip install -e .

ingest:
	local-llm ingest

api:
	local-llm serve-api

ui:
	local-llm serve-ui --api-url http://localhost:8000

test:
	pytest -v

