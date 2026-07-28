"""CC-00 RAGPipeline wrapped as a LangChain tool, with ACL identity closure-bound.

Closes ASGF L4 "ACL filtering applied" (Required) using CC-00's own
`acl_filter` — the control the LangChain ecosystem assessment found the
framework does not provide out of the box (research-report.md, Finding 10).

Closes Finding 14 (Addendum, 2026-07-26): `RAGPipeline.query(user_role=...)`
takes the role as a plain argument, and the naive LangChain wrapping exposes it
as a `@tool` parameter — which a model can set to `"admin"`, since tool
parameters are model-chosen. `make_corpus_search` binds `user_role` in a
closure at construction time instead, from a value the caller controls, not
the model. There is no parameter through which a model can express the
escalation.

VERIFIED 2026-07-27: tests/test_rag_tool.py builds a real `RAGPipeline` with a
small in-memory corpus (`acl_roles=["public"]` and `acl_roles=["staff"]`
documents) and asserts a `"public"`-role tool genuinely cannot retrieve the
staff-only document, and that the tool signature has no way to ask for it.
"""

from __future__ import annotations

from typing import Any

from langchain_core.tools import tool

from .cc00_path import RAGPipeline


def make_corpus_search(pipeline: RAGPipeline, user_role: str):
    """Bind `user_role` at construction time — never expose it as a tool arg.

    Args:
        pipeline: A configured RAGPipeline (chunker/embedder/vector_store already
            wired; embedder and vector_store may be None for BM25-only retrieval).
        user_role: The authenticated caller's role. Bound in the closure below;
            the returned tool's signature has no `user_role` parameter, so a
            model has no way to request a different one.
    """

    @tool
    def search_corpus(query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search the application corpus. Returns only documents you may see.

        Args:
            query: Natural-language query.
            top_k: Maximum results, capped at 10.
        """
        context = pipeline.query(query, user_role=user_role)
        capped = min(max(top_k, 1), 10)
        return [
            {
                "content": chunk.text,
                "source": chunk.metadata.get("doc_id", "unknown"),
                "score": score,
            }
            for chunk, score in zip(context.chunks[:capped], context.scores[:capped])
        ]

    return search_corpus
