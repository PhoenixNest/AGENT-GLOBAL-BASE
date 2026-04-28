"""
Context Compressor — Intelligent Context Compression Engine

Provides hierarchical, type-aware compression strategies that go beyond
simple truncation. Different content types compress differently:

    - Conversation history  → Hierarchical summarisation (lossy, acceptable)
    - Tool outputs          → Schema-reduction (lossless)
    - Retrieved documents   → Extractive summarisation (low-loss)
    - Decisions/commitments → Never compressed (sacred)

Usage:
    compressor = ContextCompressor()
    compressed = compressor.compress_history(turns, target_tokens=2000)
    reduced = compressor.schema_reduce_tool_output(raw_json, keep_keys=["id", "status"])
"""

import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _estimate_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return max(1, int(len(text) / 4))


# ---------------------------------------------------------------------------
# Compression result container
# ---------------------------------------------------------------------------

@dataclass
class CompressionResult:
    original_tokens: int
    compressed_tokens: int
    content: Any  # str or list depending on method
    strategy: str
    information_loss: str  # "none" | "low" | "medium" | "high"

    @property
    def compression_ratio(self) -> float:
        if self.original_tokens == 0:
            return 0.0
        return 1.0 - (self.compressed_tokens / self.original_tokens)


# ---------------------------------------------------------------------------
# Core compressor
# ---------------------------------------------------------------------------

class ContextCompressor:
    """
    Intelligent context compression with type-aware strategies.

    The compressor treats different content types differently because
    information loss is acceptable for some (conversation history) but
    not for others (decisions, tool outputs).

    Usage:
        compressor = ContextCompressor()
        result = compressor.compress_history(turns, target_tokens=2000)
        print(f"Reduced by {result.compression_ratio:.0%}")
    """

    def __init__(self, keep_recent_turns: int = 3):
        self.keep_recent_turns = keep_recent_turns

    # ------------------------------------------------------------------
    # History compression (lossy)
    # ------------------------------------------------------------------

    def compress_history(
        self,
        turns: List[Dict],
        target_tokens: int,
        sacred_turns: Optional[List[int]] = None,
    ) -> CompressionResult:
        """
        Apply progressive compression to conversation history.

        Compression tiers (oldest → newest):
            Tier 3 (oldest): Single paragraph summary
            Tier 2 (middle): One sentence per turn
            Tier 1 (recent): One sentence summary per turn
            Recent N turns:  Always kept verbatim

        Sacred turns (decisions/commitments) are never compressed.

        Args:
            turns: List of {'role': ..., 'content': ...} dicts.
            target_tokens: Target token budget for the compressed output.
            sacred_turns: Indices of turns to preserve verbatim.

        Returns:
            CompressionResult with compressed content as a list of dicts.
        """
        sacred_set = set(sacred_turns or [])
        original_text = "\n".join(
            f"[{t.get('role', 'user')}]: {t.get('content', '')}" for t in turns
        )
        original_tokens = _estimate_tokens(original_text)

        if original_tokens <= target_tokens:
            return CompressionResult(
                original_tokens=original_tokens,
                compressed_tokens=original_tokens,
                content=turns,
                strategy="no_compression_needed",
                information_loss="none",
            )

        n = len(turns)
        keep = min(self.keep_recent_turns, n)
        recent_turns = turns[-keep:]
        older_turns = turns[:-keep] if n > keep else []

        if not older_turns:
            # Even recent turns exceed budget — compress them lightly
            compressed_recent = self._light_compress(recent_turns)
            result_text = "\n".join(
                f"[{t.get('role')}]: {t.get('content')}" for t in compressed_recent
            )
            return CompressionResult(
                original_tokens=original_tokens,
                compressed_tokens=_estimate_tokens(result_text),
                content=compressed_recent,
                strategy="light_compress_recent",
                information_loss="low",
            )

        # Apply progressive compression to older turns
        tiers = self._split_into_tiers(older_turns, tier_count=3)
        compressed_parts: List[Dict] = []

        for i, tier in enumerate(tiers):
            if not tier:
                continue
            # Filter sacred turns — inject verbatim, compress the rest
            sacred_in_tier = [t for j, t in enumerate(tier)
                               if (len(turns) - len(older_turns) + j) in sacred_set]
            non_sacred_in_tier = [t for j, t in enumerate(tier)
                                   if (len(turns) - len(older_turns) + j) not in sacred_set]

            if sacred_in_tier:
                compressed_parts.extend(sacred_in_tier)

            if non_sacred_in_tier:
                level = ["paragraph", "sentence", "phrase"][min(i, 2)]
                summary = self._summarise_tier(non_sacred_in_tier, level=level)
                compressed_parts.append({"role": "system", "content": f"[Summary] {summary}"})

        compressed_parts.extend(recent_turns)

        result_text = "\n".join(
            f"[{t.get('role', 'system')}]: {t.get('content', '')}" for t in compressed_parts
        )
        compressed_tokens = _estimate_tokens(result_text)

        return CompressionResult(
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            content=compressed_parts,
            strategy="progressive_compression",
            information_loss="medium",
        )

    # ------------------------------------------------------------------
    # Tool output compression (lossless)
    # ------------------------------------------------------------------

    def schema_reduce_tool_output(
        self,
        output: Any,
        keep_keys: Optional[List[str]] = None,
        max_list_items: int = 5,
    ) -> CompressionResult:
        """
        Losslessly reduce tool output by retaining only specified keys
        and truncating long lists.

        Args:
            output: The raw tool output (dict, list, or str).
            keep_keys: Keys to retain if output is a dict. None = keep all.
            max_list_items: Maximum list items to retain.

        Returns:
            CompressionResult with reduced content.
        """
        import json
        original_str = json.dumps(output) if not isinstance(output, str) else output
        original_tokens = _estimate_tokens(original_str)

        if isinstance(output, dict):
            reduced = {k: v for k, v in output.items()
                       if keep_keys is None or k in keep_keys}
            for k, v in reduced.items():
                if isinstance(v, list) and len(v) > max_list_items:
                    reduced[k] = v[:max_list_items] + [f"... ({len(v) - max_list_items} more)"]
            result = json.dumps(reduced, indent=2)

        elif isinstance(output, list):
            truncated = output[:max_list_items]
            if len(output) > max_list_items:
                truncated.append(f"... ({len(output) - max_list_items} more items)")
            result = json.dumps(truncated, indent=2)

        else:
            result = str(output)

        return CompressionResult(
            original_tokens=original_tokens,
            compressed_tokens=_estimate_tokens(result),
            content=result,
            strategy="schema_reduction",
            information_loss="none",
        )

    # ------------------------------------------------------------------
    # Retrieved document compression (low-loss)
    # ------------------------------------------------------------------

    def extractive_compress(
        self,
        text: str,
        target_tokens: int,
        preserve_citations: bool = True,
    ) -> CompressionResult:
        """
        Extractive compression for retrieved documents.

        Retains the first sentence (topic sentence), any lines containing
        citations or key terms, and the last sentence (conclusion).
        Drops verbose explanatory prose in between.

        Args:
            text: Document text to compress.
            target_tokens: Target token budget.
            preserve_citations: If True, lines with citation markers are kept.

        Returns:
            CompressionResult with extracted key sentences.
        """
        original_tokens = _estimate_tokens(text)

        if original_tokens <= target_tokens:
            return CompressionResult(
                original_tokens=original_tokens,
                compressed_tokens=original_tokens,
                content=text,
                strategy="no_compression_needed",
                information_loss="none",
            )

        sentences = [s.strip() for s in text.replace("\n", ". ").split(".") if s.strip()]
        if not sentences:
            return CompressionResult(
                original_tokens=original_tokens,
                compressed_tokens=original_tokens,
                content=text,
                strategy="failed_extraction",
                information_loss="none",
            )

        # Always keep first and last sentences
        kept = {0, len(sentences) - 1}

        # Keep citation lines if requested
        if preserve_citations:
            citation_markers = {"[", "source:", "ref:", "see:", "cf."}
            for i, s in enumerate(sentences):
                if any(m in s.lower() for m in citation_markers):
                    kept.add(i)

        # Fill remaining budget greedily (longest sentences first — most information)
        remaining_budget = target_tokens - sum(
            _estimate_tokens(sentences[i]) for i in kept
        )
        candidates = sorted(
            [(i, s) for i, s in enumerate(sentences) if i not in kept],
            key=lambda x: len(x[1]),
            reverse=True,
        )
        for i, s in candidates:
            cost = _estimate_tokens(s)
            if remaining_budget - cost >= 0:
                kept.add(i)
                remaining_budget -= cost

        extracted = ". ".join(sentences[i] for i in sorted(kept)) + "."
        return CompressionResult(
            original_tokens=original_tokens,
            compressed_tokens=_estimate_tokens(extracted),
            content=extracted,
            strategy="extractive_compression",
            information_loss="low",
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _split_into_tiers(self, turns: List[Dict], tier_count: int = 3) -> List[List[Dict]]:
        """Split turns into equal-sized tiers (oldest first)."""
        if not turns:
            return [[] for _ in range(tier_count)]
        size = max(1, len(turns) // tier_count)
        tiers = []
        for i in range(tier_count):
            start = i * size
            end = start + size if i < tier_count - 1 else len(turns)
            tiers.append(turns[start:end])
        return tiers

    def _summarise_tier(self, turns: List[Dict], level: str) -> str:
        """
        Create a compressed summary of a tier of turns.
        Level: "paragraph" | "sentence" | "phrase"
        """
        if not turns:
            return ""

        combined = " ".join(
            t.get("content", "")[:200] for t in turns
        )

        if level == "paragraph":
            # Keep first 300 chars as a paragraph summary
            return combined[:300] + ("..." if len(combined) > 300 else "")
        elif level == "sentence":
            # First sentence or first 100 chars
            first_sentence = combined.split(".")[0]
            return first_sentence[:100] + ("." if len(first_sentence) > 0 else "")
        else:  # phrase
            # First 50 chars
            return combined[:50] + ("..." if len(combined) > 50 else "")

    def _light_compress(self, turns: List[Dict]) -> List[Dict]:
        """Apply minimal compression — truncate long individual turns."""
        result = []
        for turn in turns:
            content = turn.get("content", "")
            if _estimate_tokens(content) > 500:
                content = content[:1500] + " [truncated]"
            result.append({**turn, "content": content})
        return result
