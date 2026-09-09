import logging
from typing import Any, Dict, List, Tuple

import ollama

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def build_grounded_prompt(question: str, context_chunks: List[Dict[str, Any]]) -> str:
    """Combine retrieved chunks + the user question into a strict grounded prompt."""
    formatted_context = ""
    for idx, chunk in enumerate(context_chunks, start=1):
        source = chunk["metadata"]["source"]
        page = chunk["metadata"]["page"]
        formatted_context += (
            f"--- CONTEXT BLOCK {idx} [Source: {source}, Page: {page}] ---\n"
            f"{chunk['text']}\n\n"
        )

    prompt = f"""You are a strict, factual Customer Support AI Assistant.
Answer the user's question using ONLY the retrieved context below.

Rules:
1. Do NOT use outside knowledge or speculate.
2. Every claim must be grounded in the context.
3. Do NOT include any inline citations, document names, source filenames, or page numbers (e.g., do not write [Source: ...] or (Source: ...)) in your answer.
4. If the context does not contain enough information, state clearly: "I cannot answer this based on the available documents."

Retrieved Context:
{formatted_context}

User Question: {question}

Grounded Answer:"""
    return prompt


class GenerationService:
    """Calls the local Ollama LLM and produces a grounded answer with citations."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = ollama.Client(host=self.settings.OLLAMA_BASE_URL)

    def check_connection(self) -> bool:
        """True when the Ollama server is reachable."""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def generate(self, question: str, context_chunks: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
        """Return (answer, sources) for a question grounded in the given chunks."""
        prompt = build_grounded_prompt(question, context_chunks)

        response = self.client.chat(
            model=self.settings.OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response["message"]["content"]

        sources = sorted({
            f"{chunk['metadata']['source']} (Pg. {chunk['metadata']['page']})"
            for chunk in context_chunks
        })
        return answer, sources