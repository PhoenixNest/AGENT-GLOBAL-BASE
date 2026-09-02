"""Pattern-based PII redaction for agent-memory's write path (R3, 2026-09-02).

Closes the gap flagged by both `.claude/rules/mcp-governance.md` (agent-memory
row: "PII scrubbing on the embed path" — an open Required-level ASE gap) and
the 2026-09-01 MCP servers enterprise assessment
(`platform/benchmarks/model-context-protocol-servers/
2026-09-01-mcp-servers-enterprise-assessment/enterprise-assessment.md`, B4/R3):
before this fix, `grep -rni "pii|redact|scrub"` returned zero hits anywhere in
this server's first-party source.

Design, following that assessment's cited external practice (S4 — "If the
source text doesn't contain PII when it's embedded, the embedding can't leak
PII even under perfect inversion"): redact-before-embed, using standard
regex patterns for the common PII classes named in the remediation item —
email addresses, phone numbers, SSN-like patterns, and credit-card-like
digit sequences. This is intentionally not a general-purpose PII/NER
scrubber (no ML model, no locale-aware phone/ID validation) — regex-based
pattern matching only, per R3's explicit "don't over-engineer" scope.

Call site: `write_tool._write_memory_impl()` redacts `content` — the only
field this server ever passes to an embedder (see
`_resolve_collision()`'s `index.search(query_text=content, ...)` and
`index.upsert_payload(record_id, content, payload)` in write_tool.py) —
once, immediately after input validation and before anything else touches
it (collision search, injection detection, record construction, or
storage). Because `content` is also the same value both embedded *and*
persisted into the Qdrant payload (`memory_vector_store.py`'s
`MemoryRecord.content`/`to_payload()`, out of scope for this server to
modify), redacting it at this single point also prevents unredacted PII
from landing in the payload a later `search_memory` call could surface —
not just from reaching the embedder — without introducing a second,
divergent copy of the text.
"""

from __future__ import annotations

import re

# Order matters: more specific patterns run first so a later, broader
# pattern (credit-card-like digit runs) never gets a chance to partially
# consume a numeric sequence a more specific pattern (SSN) already owns.
# Phone numbers run last because US-format phone numbers (10-11 digits)
# never satisfy the credit-card pattern's 13-19 digit minimum, so ordering
# relative to it does not matter in practice -- kept last for readability
# (least specific pattern last).

# user@domain.tld -- standard, not exhaustive (no IDN/punycode handling).
_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# 123-45-6789 -- the one standard US SSN separator format. Deliberately not
# matching a bare 9-digit run (\d{9}) -- that would false-positive on far
# too many ordinary numeric identifiers to be worth the extra recall.
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

# 13-19 digits, optionally separated by single spaces or dashes -- covers
# Visa/Mastercard (16), Amex (15), and most other issuers' PAN lengths,
# with or without the usual 4-digit grouping. No Luhn check (deliberately
# out of scope -- a well-formed-looking but Luhn-invalid number is still
# worth redacting defensively; a false positive here just over-redacts).
_CREDIT_CARD_RE = re.compile(r"\b(?:\d[ -]?){13,19}\b")

# US-style 10-digit phone number, with or without a leading +1/1 country
# code, and with any of the common area-code/separator conventions
# ( (555) 123-4567 | 555-123-4567 | 555.123.4567 | 5551234567 | +1 555 123 4567 ).
# Bounded by (?<!\d)/(?!\d) rather than \b so a leading "+" doesn't defeat
# the boundary check.
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)")

_REDACTIONS = (
    (_EMAIL_RE, "[REDACTED_EMAIL]"),
    (_SSN_RE, "[REDACTED_SSN]"),
    (_CREDIT_CARD_RE, "[REDACTED_CC]"),
    (_PHONE_RE, "[REDACTED_PHONE]"),
)


def redact_pii(text: str) -> str:
    """Returns `text` with common PII patterns replaced by labeled
    placeholders (`[REDACTED_EMAIL]`, `[REDACTED_SSN]`, `[REDACTED_CC]`,
    `[REDACTED_PHONE]`). Non-string or empty input is returned unchanged --
    this function never raises and never changes the type of its input.
    """
    if not isinstance(text, str) or not text:
        return text
    redacted = text
    for pattern, placeholder in _REDACTIONS:
        redacted = pattern.sub(placeholder, redacted)
    return redacted
