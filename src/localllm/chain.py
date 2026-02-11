"""LangChain RAG chain wired to Ollama and Qdrant."""

from __future__ import annotations

from typing import Any, Dict

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

from .config import get_settings
from .vectorstore import get_vectorstore


def build_llm():
    settings = get_settings()
    if settings.llm_provider == "ollama":
        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
        )
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "LOCAL_LLM_OPENAI_API_KEY must be set when llm_provider is 'openai'."
            )
        return ChatOpenAI(
            model=settings.openai_model,
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
        )
    raise ValueError(f"Unsupported llm_provider: {settings.llm_provider!r}")


def build_rag_chain():
    """Return a simple conversational RAG chain (no memory persistence)."""

    llm = build_llm()
    vs = get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "Du bist ein hilfreicher Assistent für Fragen zu Dissertationen, "
                    "die am FIR e.V. an der RWTH Aachen veröffentlicht wurden. "
                    "Beantworte Fragen ausschließlich auf Basis des gegebenen Kontexts. "
                    "Wenn du keine Antwort findest, sag explizit, dass du es nicht weißt."
                ),
            ),
            MessagesPlaceholder("chat_history"),
            ("user", "{input}"),
            ("user", "Kontext:\n{context}"),
        ]
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, document_chain)


def run_rag_chain(
    question: str,
    chat_history: list[Any] | None = None,
) -> Dict[str, Any]:
    """Run the chain with a simple chat history structure."""

    chain = build_rag_chain()
    history = chat_history or []
    # history is expected to be a list of LangChain messages
    return chain.invoke({"input": question, "chat_history": history})


def append_to_history(
    chat_history: list[Any],
    user: str,
    answer: str,
) -> None:
    """Append a user / AI exchange to chat history in-place."""

    chat_history.append(HumanMessage(content=user))
    chat_history.append(AIMessage(content=answer))

