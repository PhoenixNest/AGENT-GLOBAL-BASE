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

from implementations.context_compressor import ContextCompressor, _estimate_tokens
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


TARGET_TOKENS = 1500


def test_acon_vs_context_compressor():
    compressor = ContextCompressor()
    for session in SAMPLE_SESSIONS:
        turns = session["turns"]
        original_tokens = sum(_estimate_tokens(t["content"]) for t in turns)
        cc_result = compressor.compress_history(turns, target_tokens=TARGET_TOKENS)
        acon_result = acon_compress(turns, target_tokens=TARGET_TOKENS)
        acon_tokens = sum(_estimate_tokens(t["content"]) for t in acon_result)
        assert cc_result.compressed_tokens < original_tokens, (
            f"ContextCompressor did not reduce tokens for {session['name']}"
        )
        assert acon_tokens < original_tokens, (
            f"ACON did not reduce tokens for {session['name']}"
        )


def run_benchmark():
    compressor = ContextCompressor()
    print(
        f"{'Session':<20} {'Original':>10} {'CC Tokens':>10} {'CC Ratio':>9} {'ACON Tokens':>12} {'ACON Ratio':>11}"
    )
    print("-" * 80)
    for session in SAMPLE_SESSIONS:
        turns = session["turns"]
        orig = sum(_estimate_tokens(t["content"]) for t in turns)
        cc = compressor.compress_history(turns, target_tokens=TARGET_TOKENS)
        acon = acon_compress(turns, target_tokens=TARGET_TOKENS)
        acon_tok = sum(_estimate_tokens(t["content"]) for t in acon)
        print(
            f"{session['name']:<20} {orig:>10} {cc.compressed_tokens:>10} {cc.compression_ratio:>8.1%} {acon_tok:>12} {1 - acon_tok/orig:>10.1%}"
        )


if __name__ == "__main__":
    run_benchmark()
