"""Basic tests for PDF loading and chunking."""

from pathlib import Path

from localllm.ingestion import chunk_text, load_pdfs


def test_chunk_text_basic():
    text = "a" * 1000
    chunks = chunk_text(text, chunk_size=200, chunk_overlap=50)
    # we should get several chunks and none should be empty
    assert len(chunks) > 1
    assert all(c.strip() for c in chunks)


def test_load_pdfs_uses_data_dir(tmp_path, monkeypatch):
    # create a fake pdf file
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n% dummy")

    monkeypatch.setenv("LOCAL_LLM_DATA_DIR", str(tmp_path))

    pdfs = load_pdfs(tmp_path)
    assert pdf_path in pdfs

