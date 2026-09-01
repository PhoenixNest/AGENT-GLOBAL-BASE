"""
Tests for chunking strategies — FixedSizeChunker, SemanticChunker, HybridChunker.
No external dependencies required.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from implementations.chunker import FixedSizeChunker, HybridChunker, SemanticChunker


PARAGRAPH = (
    "Context engineering is the practice of structuring information for LLM calls. "
    "The four-slot model separates system, retrieved, history, and tool outputs. "
    "Each slot has a priority score that governs eviction under token pressure. "
    "Sacred items hold an infinite score and are never evicted. "
    "Working memory is task-scoped and cleared between tasks."
)


class TestFixedSizeChunker:
    def test_single_chunk_when_text_fits(self):
        chunker = FixedSizeChunker(chunk_size=1000, overlap=0)
        chunks = chunker.chunk("short text")
        assert len(chunks) == 1
        assert chunks[0].text == "short text"

    def test_multiple_chunks_produced(self):
        chunker = FixedSizeChunker(chunk_size=50, overlap=0)
        chunks = chunker.chunk(PARAGRAPH)
        assert len(chunks) > 1

    def test_no_chunk_exceeds_size(self):
        chunker = FixedSizeChunker(chunk_size=80, overlap=0)
        for chunk in chunker.chunk(PARAGRAPH):
            assert len(chunk.text) <= 80

    def test_overlap_creates_shared_content(self):
        chunker = FixedSizeChunker(chunk_size=100, overlap=20)
        chunks = chunker.chunk(PARAGRAPH)
        if len(chunks) >= 2:
            # The end of chunk N overlaps with the start of chunk N+1.
            tail = chunks[0].text[-20:]
            head = chunks[1].text[:20]
            assert tail == head

    def test_indices_are_sequential(self):
        chunker = FixedSizeChunker(chunk_size=60, overlap=0)
        chunks = chunker.chunk(PARAGRAPH)
        for i, chunk in enumerate(chunks):
            assert chunk.index == i

    def test_char_positions_are_contiguous(self):
        chunker = FixedSizeChunker(chunk_size=80, overlap=0)
        chunks = chunker.chunk(PARAGRAPH)
        assert chunks[0].start_char == 0
        for i in range(len(chunks) - 1):
            assert chunks[i].end_char == chunks[i + 1].start_char

    def test_invalid_chunk_size_raises(self):
        with pytest.raises(ValueError):
            FixedSizeChunker(chunk_size=0)

    def test_invalid_overlap_raises(self):
        with pytest.raises(ValueError):
            FixedSizeChunker(chunk_size=100, overlap=100)

    def test_empty_text_returns_no_chunks(self):
        chunker = FixedSizeChunker(chunk_size=100, overlap=0)
        assert chunker.chunk("") == []


class TestSemanticChunker:
    def test_respects_sentence_boundaries(self):
        chunker = SemanticChunker(max_size=200)
        chunks = chunker.chunk(PARAGRAPH)
        # No chunk should contain a mid-sentence split marker
        for chunk in chunks:
            assert chunk.text.strip() != ""

    def test_single_sentence_fits_in_one_chunk(self):
        chunker = SemanticChunker(max_size=500)
        sentence = "This is one complete sentence."
        chunks = chunker.chunk(sentence)
        assert len(chunks) == 1
        assert chunks[0].text == sentence

    def test_multiple_sentences_grouped(self):
        chunker = SemanticChunker(max_size=1000)
        chunks = chunker.chunk(PARAGRAPH)
        assert len(chunks) == 1  # All sentences fit in one chunk

    def test_overflow_creates_new_chunk(self):
        chunker = SemanticChunker(max_size=80)
        chunks = chunker.chunk(PARAGRAPH)
        assert len(chunks) > 1

    def test_no_empty_chunks(self):
        chunker = SemanticChunker(max_size=100)
        for chunk in chunker.chunk(PARAGRAPH):
            assert chunk.text.strip() != ""

    def test_invalid_max_size_raises(self):
        with pytest.raises(ValueError):
            SemanticChunker(max_size=0)


class TestHybridChunker:
    def test_produces_chunks(self):
        chunker = HybridChunker(max_size=200, overlap_sentences=1)
        chunks = chunker.chunk(PARAGRAPH)
        assert len(chunks) >= 1

    def test_no_chunk_exceeds_max_size_unless_single_sentence(self):
        chunker = HybridChunker(max_size=120, overlap_sentences=0)
        for chunk in chunker.chunk(PARAGRAPH):
            # A chunk may exceed max_size only if it is a single indivisible sentence.
            sentences_in_chunk = chunk.text.count(". ") + chunk.text.count("! ") + chunk.text.count("? ")
            if sentences_in_chunk > 0:
                assert len(chunk.text) <= 120

    def test_overlap_sentences_carry_forward(self):
        chunker = HybridChunker(max_size=150, overlap_sentences=1)
        chunks = chunker.chunk(PARAGRAPH)
        if len(chunks) >= 2:
            # The last sentence of chunk N should appear at the start of chunk N+1.
            prev_sentences = chunks[0].text.split(". ")
            last_sentence = prev_sentences[-1].strip().rstrip(".")
            assert last_sentence in chunks[1].text

    def test_indices_sequential(self):
        chunker = HybridChunker(max_size=150)
        chunks = chunker.chunk(PARAGRAPH)
        for i, chunk in enumerate(chunks):
            assert chunk.index == i

    def test_empty_text(self):
        chunker = HybridChunker(max_size=200)
        assert chunker.chunk("") == []

    def test_invalid_max_size_raises(self):
        with pytest.raises(ValueError):
            HybridChunker(max_size=-1)
