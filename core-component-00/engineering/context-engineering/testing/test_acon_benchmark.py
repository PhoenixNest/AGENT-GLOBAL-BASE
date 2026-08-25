"""
ACON vs ContextCompressor Benchmark

Compares ContextCompressor.compress_history() against a simulated ACON
(Agent Context Optimization Network) approach on 3 synthetic 100-turn sessions.

ACON methodology: adaptive compression based on turn importance scores.
Recent turns + tool outputs score higher; filler turns score lower.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.context_compressor import (
    ContextCompressor,
    _estimate_tokens,
    estimate_turns_tokens,
    format_turns_for_estimation,
)
from typing import List, Dict


def _make_session(n_turns: int, session_type: str) -> List[Dict]:
    turns = []
    for i in range(n_turns):
        if session_type == "coding":
            if i % 10 == 0:
                role, content = (
                    "assistant",
                    f"Here is the implementation for step {i}: def func_{i}(): return {i} * 2",
                )
            elif i % 5 == 0:
                role, content = "user", f"Now implement step {i} with error handling"
            else:
                role, content = (
                    "user" if i % 2 == 0 else "assistant",
                    f"OK, understood. Moving to item {i}.",
                )
        elif session_type == "research":
            if i % 8 == 0:
                role, content = (
                    "assistant",
                    f"Finding {i}: The study at arXiv:{2500+i}.{10000+i} shows a {i}% improvement in accuracy when using the proposed method.",
                )
            else:
                role, content = (
                    "user" if i % 2 == 0 else "assistant",
                    f"What about approach {i}? Consider this alternative perspective on the topic.",
                )
        else:
            role = "user" if i % 2 == 0 else "assistant"
            content = f"Turn {i}: general conversation about topic {i % 7}. This is a medium-length message."
        turns.append({"role": role, "content": content})
    return turns


SAMPLE_SESSIONS = [
    {"name": "coding_session", "turns": _make_session(100, "coding")},
    {"name": "research_session", "turns": _make_session(100, "research")},
    {"name": "general_session", "turns": _make_session(100, "general")},
]


def acon_compress(turns: List[Dict], target_tokens: int) -> List[Dict]:
    """Simulate ACON adaptive compression via importance scoring."""

    def score_turn(i: int, turn: Dict) -> float:
        recency = i / len(turns)
        is_tool = "def " in turn.get("content", "") or "arXiv" in turn.get(
            "content", ""
        )
        length_score = min(len(turn.get("content", "")) / 200.0, 1.0)
        return recency * 0.5 + (0.3 if is_tool else 0.0) + length_score * 0.2

    scored = [(score_turn(i, t), i, t) for i, t in enumerate(turns)]
    scored.sort(reverse=True)
    kept = []
    total = 0
    for score, idx, turn in scored:
        cost = _estimate_tokens(turn.get("content", ""))
        if total + cost <= target_tokens:
            kept.append((idx, turn))
            total += cost
    kept.sort(key=lambda x: x[0])
    return [t for _, t in kept]


# Contractual token-accounting basis for this benchmark: every token count
# below — original, ContextCompressor's own internal accounting, and ACON's
# — is measured via estimate_turns_tokens() (the role-prefixed, joined
# transcript form). Summing per-turn content estimates in isolation
# undercounts (it omits role-label/separator overhead) and disagrees with
# what compress_history() itself compresses against — that mismatch used to
# make this benchmark flaky. See context_compressor.format_turns_for_estimation.
COMPRESSION_TARGET_FRACTION = 0.5  # compress each session down to half its size
RATIO_FLOOR = 0.30  # ContextCompressor must cut at least 30% of tokens once compression runs
CONTINUITY_FLOOR = 1.0  # every designated decision turn must survive verbatim


def _decision_indices(turns: List[Dict]) -> List[int]:
    """Indices of turns carrying irreversible information for this session —
    the same markers ACON's importance scoring treats as `is_tool` (code
    definitions, cited findings). These are the turns a real agent could not
    afford to lose to compression."""
    markers = ("def ", "arXiv")
    return [i for i, t in enumerate(turns) if any(m in t.get("content", "") for m in markers)]


def test_acon_vs_context_compressor():
    compressor = ContextCompressor()
    for session in SAMPLE_SESSIONS:
        turns = session["turns"]
        original_tokens = estimate_turns_tokens(turns)
        target_tokens = max(1, int(original_tokens * COMPRESSION_TARGET_FRACTION))
        decision_indices = _decision_indices(turns)

        cc_result = compressor.compress_history(
            turns, target_tokens=target_tokens, sacred_turns=decision_indices
        )
        acon_result = acon_compress(turns, target_tokens=target_tokens)
        acon_tokens = estimate_turns_tokens(acon_result)

        assert cc_result.compressed_tokens < original_tokens, (
            f"ContextCompressor did not reduce tokens for {session['name']}"
        )
        assert acon_tokens < original_tokens, (
            f"ACON did not reduce tokens for {session['name']}"
        )

        assert cc_result.compression_ratio >= RATIO_FLOOR, (
            f"{session['name']}: ContextCompressor ratio {cc_result.compression_ratio:.1%} "
            f"below floor {RATIO_FLOOR:.0%}"
        )

        if decision_indices:
            compressed_text = format_turns_for_estimation(cc_result.content)
            survived = sum(
                1 for i in decision_indices if turns[i]["content"] in compressed_text
            )
            continuity = survived / len(decision_indices)
            assert continuity >= CONTINUITY_FLOOR, (
                f"{session['name']}: decision continuity {continuity:.0%} "
                f"below floor {CONTINUITY_FLOOR:.0%} "
                f"({survived}/{len(decision_indices)} decision turns survived)"
            )


def run_benchmark():
    compressor = ContextCompressor()
    print(
        f"{'Session':<20} {'Original':>10} {'CC Tokens':>10} {'CC Ratio':>9} {'ACON Tokens':>12} {'ACON Ratio':>11}"
    )
    print("-" * 80)
    for session in SAMPLE_SESSIONS:
        turns = session["turns"]
        orig = estimate_turns_tokens(turns)
        target_tokens = max(1, int(orig * COMPRESSION_TARGET_FRACTION))
        cc = compressor.compress_history(
            turns, target_tokens=target_tokens, sacred_turns=_decision_indices(turns)
        )
        acon = acon_compress(turns, target_tokens=target_tokens)
        acon_tok = estimate_turns_tokens(acon)
        print(
            f"{session['name']:<20} {orig:>10} {cc.compressed_tokens:>10} {cc.compression_ratio:>8.1%} {acon_tok:>12} {1 - acon_tok/orig:>10.1%}"
        )


if __name__ == "__main__":
    run_benchmark()
