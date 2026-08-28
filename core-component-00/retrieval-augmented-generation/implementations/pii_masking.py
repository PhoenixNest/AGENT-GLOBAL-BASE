"""
PII Masking — CC-00 RAG Layer 4 Reference Implementation

Regex-based detection and redaction of common PII patterns. Invoked from
RAGPipeline.ingest() between chunking and embedding, so no raw PII reaches
the embedding model call, the vector store payload, or the local BM25 index.

Pattern-based coverage (email, phone, SSN-like, credit-card-like) per the
mandatory ASGF Security Control in rag-engineering.md § Security Controls —
not a full NER-based PII system.
"""

from __future__ import annotations

import re

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_CREDIT_CARD_RE = re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b")
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_PHONE_RE = re.compile(r"\b(?:\(?\d{3}\)?[-.\s])?\d{3}[-.\s]?\d{4}\b")

# Order matters: longer/more-specific patterns (credit card, SSN) run before
# the looser phone pattern so a redacted card/SSN can't leave a digit
# fragment behind that the phone pattern then partially re-matches.
_MASKS = [
    (_EMAIL_RE, "[EMAIL_REDACTED]"),
    (_CREDIT_CARD_RE, "[CC_REDACTED]"),
    (_SSN_RE, "[SSN_REDACTED]"),
    (_PHONE_RE, "[PHONE_REDACTED]"),
]


def mask_pii(text: str) -> str:
    """
    Redact common PII patterns (email addresses, phone numbers, SSN-like
    numbers, credit-card-like numbers) from text.

    Args:
        text: Raw chunk text, prior to embedding.

    Returns:
        Text with detected PII patterns replaced by `[<KIND>_REDACTED]`
        placeholders. Text with no matching patterns is returned unchanged.
    """
    if not text:
        return text
    masked = text
    for pattern, placeholder in _MASKS:
        masked = pattern.sub(placeholder, masked)
    return masked
