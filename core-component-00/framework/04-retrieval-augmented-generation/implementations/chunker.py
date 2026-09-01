"""
Text Chunking — CC-00 RAG Layer 4 Reference Implementation

Three strategies matching the RAG module's chunking taxonomy:
  - FixedSizeChunker  : uniform windows with configurable overlap
  - SemanticChunker   : sentence-boundary splitting (regex-based, no spaCy dep)
  - HybridChunker     : sentence boundaries honoured within a size ceiling
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class Chunk:
    text: str
    index: int
    start_char: int
    end_char: int
    metadata: dict = field(default_factory=dict)


# Regex matching common sentence-ending punctuation followed by whitespace or EOS.
_SENTENCE_END = re.compile(r'(?<=[.!?])\s+')


def _split_sentences(text: str) -> List[str]:
    """Split text on sentence boundaries using punctuation heuristics."""
    parts = _SENTENCE_END.split(text.strip())
    return [p.strip() for p in parts if p.strip()]


class FixedSizeChunker:
    """
    Splits text into fixed-size character windows with optional overlap.

    Args:
        chunk_size: Maximum characters per chunk.
        overlap:    Characters of overlap between consecutive chunks.
    """

    def __init__(self, chunk_size: int = 512, overlap: int = 64) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("overlap must be >= 0 and < chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[Chunk]:
        chunks: List[Chunk] = []
        step = self.chunk_size - self.overlap
        start = 0
        idx = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(Chunk(
                text=text[start:end],
                index=idx,
                start_char=start,
                end_char=end,
            ))
            idx += 1
            start += step
        return chunks


class SemanticChunker:
    """
    Splits text on sentence boundaries, grouping sentences until
    a soft size limit is reached.

    Args:
        max_size: Soft character ceiling per chunk. A single sentence
                  exceeding this limit is emitted as its own chunk.
    """

    def __init__(self, max_size: int = 512) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self.max_size = max_size

    def chunk(self, text: str) -> List[Chunk]:
        sentences = _split_sentences(text)
        chunks: List[Chunk] = []
        current: List[str] = []
        current_len = 0
        char_pos = 0
        chunk_start = 0
        idx = 0

        for sentence in sentences:
            s_len = len(sentence)
            if current and current_len + 1 + s_len > self.max_size:
                body = " ".join(current)
                end = chunk_start + len(body)
                chunks.append(Chunk(
                    text=body,
                    index=idx,
                    start_char=chunk_start,
                    end_char=end,
                ))
                idx += 1
                chunk_start = end + 1
                current = []
                current_len = 0
            current.append(sentence)
            current_len += (1 + s_len) if current_len else s_len

        if current:
            body = " ".join(current)
            chunks.append(Chunk(
                text=body,
                index=idx,
                start_char=chunk_start,
                end_char=chunk_start + len(body),
            ))

        return chunks


class HybridChunker:
    """
    Sentence-aware chunker with a hard size ceiling.

    Builds chunks sentence-by-sentence. When adding the next sentence
    would exceed max_size, the current chunk is emitted. Overlap is
    preserved by carrying the last sentence forward into the next chunk.
    """

    def __init__(self, max_size: int = 512, overlap_sentences: int = 1) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        if overlap_sentences < 0:
            raise ValueError("overlap_sentences must be >= 0")
        self.max_size = max_size
        self.overlap_sentences = overlap_sentences

    def chunk(self, text: str) -> List[Chunk]:
        sentences = _split_sentences(text)
        chunks: List[Chunk] = []
        current: List[str] = []
        current_len = 0
        char_pos = 0
        idx = 0

        i = 0
        while i < len(sentences):
            sentence = sentences[i]
            addition = (1 + len(sentence)) if current else len(sentence)

            if current and current_len + addition > self.max_size:
                body = " ".join(current)
                chunks.append(Chunk(
                    text=body,
                    index=idx,
                    start_char=char_pos,
                    end_char=char_pos + len(body),
                ))
                idx += 1
                char_pos += len(body) + 1
                # Carry overlap sentences forward, then always add the triggering
                # sentence and advance i — guarantees progress even when the
                # overlap alone fills the window.
                current = current[-self.overlap_sentences:] if self.overlap_sentences else []
                current_len = sum(len(s) for s in current) + max(0, len(current) - 1)
                current.append(sentence)
                current_len += (1 + len(sentence)) if current_len else len(sentence)
                i += 1
            else:
                current.append(sentence)
                current_len += addition
                i += 1

        if current:
            body = " ".join(current)
            chunks.append(Chunk(
                text=body,
                index=idx,
                start_char=char_pos,
                end_char=char_pos + len(body),
            ))

        return chunks
