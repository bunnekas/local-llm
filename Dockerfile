FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY pyproject.toml ./
COPY src ./src

RUN pip install --upgrade pip && \
    pip install .

COPY config ./config
COPY data ./data

CMD ["local-llm", "serve-api"]

