"""Streamlit UI for local-llm."""

from __future__ import annotations

import os
from typing import List

import httpx
import streamlit as st


API_URL = os.environ.get("LOCAL_LLM_API_URL", "http://localhost:8000")


def ask_api(question: str, chat_history: List[str]) -> str:
    payload = {"question": question, "chat_history": chat_history}
    resp = httpx.post(f"{API_URL}/query", json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data.get("answer", "")


def main() -> None:
    st.set_page_config(page_title="local-llm", layout="centered")
    st.title("LocalLLM – FIR dissertations")
    st.caption(f"Backend: {API_URL}")

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
    for idx in range(0, len(st.session_state.chat_history), 2):
        user = st.session_state.chat_history[idx]
        ai = st.session_state.chat_history[idx + 1] if idx + 1 < len(st.session_state.chat_history) else ""
        with st.chat_message("user"):
            st.write(user)
        if ai:
            with st.chat_message("assistant"):
                st.write(ai)


if __name__ == "__main__":
    main()

