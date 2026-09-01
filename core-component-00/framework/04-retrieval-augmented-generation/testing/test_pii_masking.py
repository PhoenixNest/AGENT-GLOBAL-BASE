"""
Tests for PII masking (RAG R2 remediation, I2).

All fixtures use obviously synthetic PII values (`.invalid` email domains,
`555-01xx`-style NANP-reserved fictional phone numbers, `000-`-prefixed
synthetic SSNs, and the well-known 4111-1111-1111-1111 Visa test card
number) — never real personal data.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from implementations.pii_masking import mask_pii
from implementations.pipeline import RAGPipeline
from implementations.retrieval import Document


# ---------------------------------------------------------------------------
# Unit tests — mask_pii()
# ---------------------------------------------------------------------------

class TestMaskPii:
    def test_masks_email_address(self):
        result = mask_pii("Contact me at jane.doe@example.invalid for details.")
        assert "jane.doe@example.invalid" not in result
        assert "[EMAIL_REDACTED]" in result

    def test_masks_short_phone_number(self):
        result = mask_pii("Call the test line at 555-0100 today.")
        assert "555-0100" not in result
        assert "[PHONE_REDACTED]" in result

    def test_masks_full_phone_number_with_area_code(self):
        result = mask_pii("Reach support at (555) 555-0199.")
        assert "555-0199" not in result
        assert "[PHONE_REDACTED]" in result

    def test_masks_ssn_like_pattern(self):
        result = mask_pii("Synthetic SSN for testing: 000-12-3456.")
        assert "000-12-3456" not in result
        assert "[SSN_REDACTED]" in result

    def test_masks_credit_card_like_pattern_with_spaces(self):
        result = mask_pii("Test card number 4111 1111 1111 1111 is a known test value.")
        assert "4111 1111 1111 1111" not in result
        assert "[CC_REDACTED]" in result

    def test_masks_credit_card_like_pattern_with_dashes(self):
        result = mask_pii("Card 4111-1111-1111-1111 was charged for the test order.")
        assert "4111-1111-1111-1111" not in result
        assert "[CC_REDACTED]" in result

    def test_masks_multiple_patterns_in_one_text(self):
        text = "Email jane@example.invalid or call 555-0100, card 4111-1111-1111-1111."
        result = mask_pii(text)
        assert "jane@example.invalid" not in result
        assert "555-0100" not in result
        assert "4111-1111-1111-1111" not in result
        assert "[EMAIL_REDACTED]" in result
        assert "[PHONE_REDACTED]" in result
        assert "[CC_REDACTED]" in result

    def test_leaves_non_pii_text_untouched(self):
        text = "Context engineering structures information for LLM calls."
        assert mask_pii(text) == text

    def test_empty_string_returns_empty(self):
        assert mask_pii("") == ""


# ---------------------------------------------------------------------------
# Integration — RAGPipeline.ingest() masks before the embedder call
# ---------------------------------------------------------------------------

class TestPipelineMasksBeforeEmbedding:
    def test_embedder_never_receives_raw_email(self):
        captured = []

        def spy_embedder(text):
            captured.append(text)
            return [0.0] * 8

        pipeline = RAGPipeline(embedder=spy_embedder)
        docs = [Document(id="doc-pii-1", text="Reach me at jane.doe@example.invalid anytime.")]
        pipeline.ingest(docs)

        assert captured, "embedder was never called"
        for text in captured:
            assert "jane.doe@example.invalid" not in text
            assert "[EMAIL_REDACTED]" in text

    def test_embedder_never_receives_raw_phone_or_ssn(self):
        captured = []

        def spy_embedder(text):
            captured.append(text)
            return [0.0] * 8

        pipeline = RAGPipeline(embedder=spy_embedder)
        docs = [Document(
            id="doc-pii-2",
            text="Call 555-0100 or reference synthetic SSN 000-12-3456 for the test case.",
        )]
        pipeline.ingest(docs)

        joined = " ".join(captured)
        assert "555-0100" not in joined
        assert "000-12-3456" not in joined

    def test_vector_store_payload_stores_masked_text_not_raw_pii(self):
        stored_payloads = []

        class RecordingStore:
            def upsert(self, id, vector, payload):
                stored_payloads.append(payload)

            def search(self, vector, top_k=5, user_role=None):
                return []

        def embedder(text):
            return [0.0] * 8

        pipeline = RAGPipeline(embedder=embedder, vector_store=RecordingStore())
        docs = [Document(id="doc-pii-3", text="Card 4111-1111-1111-1111 charged for the test order.")]
        pipeline.ingest(docs)

        assert stored_payloads
        for payload in stored_payloads:
            assert "4111-1111-1111-1111" not in payload["text"]

    def test_local_bm25_index_does_not_retain_raw_pii(self):
        pipeline = RAGPipeline()
        docs = [Document(id="doc-pii-4", text="Contact jane.doe@example.invalid about the order.")]
        pipeline.ingest(docs)

        for doc in pipeline._documents.values():
            assert "jane.doe@example.invalid" not in doc.text

    def test_ingest_without_pii_is_unaffected(self):
        pipeline = RAGPipeline()
        docs = [Document(id="doc-clean", text="Context engineering structures information for LLM calls.")]
        total = pipeline.ingest(docs)
        assert total > 0
        for doc in pipeline._documents.values():
            assert doc.text == "Context engineering structures information for LLM calls."
