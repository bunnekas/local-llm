"""Streamlit UI for local-llm."""

from __future__ import annotations

import os
from typing import List

import httpx
import streamlit as st


API_URL = os.environ.get("LOCAL_LLM_API_URL", "http://localhost:8000")


def fetch_health() -> dict | None:
    try:
        resp = httpx.get(f"{API_URL}/health", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def ask_api(question: str, chat_history: List[str]) -> str:
    payload = {"question": question, "chat_history": chat_history}
    resp = httpx.post(f"{API_URL}/query", json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data.get("answer", "")


def main() -> None:
    st.set_page_config(page_title="local-llm", layout="wide")

    health = fetch_health()

    with st.sidebar:
        st.markdown("### local-llm")
        st.caption("FIR / RWTH dissertation assistant")
        st.markdown("---")
        st.markdown("**Backend**")
        st.code(API_URL, language="text")
        if health:
            st.markdown("**Status**")
            st.markdown(
                f"- LLM: `{health.get('llm_provider', 'unknown')}`\n"
                f"- Collection: `{health.get('qdrant_collection', 'n/a')}`\n"
                f"- Embeddings: `{health.get('embedding_model', 'n/a')}`"
            )
        else:
            st.markdown("**Status**: Backend nicht erreichbar")

        st.markdown("---")
        st.markdown(
            "Stelle Fragen zu Inhalt, Zielsetzung und Ergebnissen der "
            "Dissertationen. Die Antworten basieren ausschließlich auf den "
            "indexierten PDF-Dokumenten."
        )

    st.title("LocalLLM – FIR Dissertationen")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # list[str]

    question = st.chat_input("Stelle eine Frage zu den Dissertationen...")
    if question:
        with st.chat_message("user"):
            st.write(question)
        try:
            answer = ask_api(question, st.session_state.chat_history)
        except Exception as e:  # noqa: BLE001
            answer = f"Fehler bei der Anfrage: {e}"
        st.session_state.chat_history.append(question)
        with st.chat_message("assistant"):
            st.write(answer)

    # render previous history
    if st.session_state.chat_history:
        st.markdown("### Verlauf")
        for idx in range(0, len(st.session_state.chat_history), 2):
            user = st.session_state.chat_history[idx]
            ai = (
                st.session_state.chat_history[idx + 1]
                if idx + 1 < len(st.session_state.chat_history)
                else ""
            )
            with st.chat_message("user"):
                st.write(user)
            if ai:
                with st.chat_message("assistant"):
                    st.write(ai)


if __name__ == "__main__":
    main()

