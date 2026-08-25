"""
Regression test for context-budget-alert.py's enforcement path (Harness
Implementation Plan, item I5, 2026-08-23) and its token-count trigger
(Harness Implementation Plan, item I1, 2026-08-25).

Invokes the hook exactly as production does: a subprocess fed the hook's stdin
JSON contract, asserting on its stdout JSON. Run with:
    pytest .claude/hooks/test_context_budget_alert.py -v

No tiktoken is installed in this environment, so the hook's token estimator falls
back to a plain len(text)/4 heuristic (see context_compressor.py's _estimate_tokens).
Transcript sizes below are chosen against that heuristic with generous margins so
these tests remain correct if tiktoken is later installed.
"""

import json
import os
import subprocess
import sys

HOOK_PATH = os.path.join(os.path.dirname(__file__), "context-budget-alert.py")


def _run_hook(transcript_path, session_id="test-session"):
    payload = json.dumps({"transcript_path": transcript_path, "session_id": session_id})
    return subprocess.run(
        [sys.executable, HOOK_PATH],
        input=payload,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _write_transcript_for_tokens(path, target_tokens, turn_count=20):
    """Write a valid JSONL transcript whose extracted turn TEXT content totals
    approximately target_tokens tokens under the char/4 fallback estimator —
    the signal the hook's token-count trigger actually measures, independent of
    the file's total byte size (which includes JSON structure/overhead the hook
    does not count)."""
    lines = []
    base_texts = []
    for i in range(turn_count):
        role = "user" if i % 2 == 0 else "assistant"
        text = f"turn {i} content about topic {i % 7}"
        base_texts.append(text)
        lines.append(json.dumps({
            "type": role,
            "message": {"content": [{"type": "text", "text": text}]},
        }))
    base_chars = sum(len(t) for t in base_texts)
    target_chars = target_tokens * 4
    pad_chars = max(target_chars - base_chars, 0)
    if pad_chars:
        lines.append(json.dumps({
            "type": "user",
            "message": {"content": [{"type": "text", "text": "x" * pad_chars}]},
        }))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


class TestAlertOnlyBelowThresholds:
    def test_under_alert_threshold_produces_no_output(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        _write_transcript_for_tokens(str(transcript), target_tokens=10_000, turn_count=5)
        proc = _run_hook(str(transcript))
        assert proc.returncode == 0
        assert proc.stdout.strip() == ""

    def test_between_alert_and_enforcement_alerts_without_compacting(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        _write_transcript_for_tokens(str(transcript), target_tokens=60_000, turn_count=20)
        proc = _run_hook(str(transcript))
        assert proc.returncode == 0
        output = json.loads(proc.stdout)
        msg = output["hookSpecificOutput"]["additionalContext"]
        assert "CONTEXT BUDGET ALERT — H-CE01" in msg
        assert "ENFORCEMENT" not in msg
        assert "compaction routine ran" not in msg
        assert "tokens" in msg


class TestEnforcementCompaction:
    def test_over_enforcement_threshold_actually_compacts(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        _write_transcript_for_tokens(str(transcript), target_tokens=150_000, turn_count=300)
        proc = _run_hook(str(transcript))
        assert proc.returncode == 0
        output = json.loads(proc.stdout)
        msg = output["hookSpecificOutput"]["additionalContext"]
        assert "ENFORCEMENT" in msg
        assert "compaction routine ran automatically" in msg
        assert "Compacted content follows:" in msg
        assert "reduction" in output["systemMessage"]

    def test_unparseable_transcript_falls_back_to_byte_size_safety_net(self, tmp_path):
        # No turns can be parsed at all, so no token estimate is possible — the hook
        # must fall back to the byte-size safety net rather than silently doing nothing.
        transcript = tmp_path / "transcript.jsonl"
        with open(transcript, "w", encoding="utf-8") as f:
            f.write("not json\n")
            f.write("x" * (1600 * 1024) + "\n")  # not valid JSON either
        proc = _run_hook(str(transcript))
        assert proc.returncode == 0
        output = json.loads(proc.stdout)
        msg = output["hookSpecificOutput"]["additionalContext"]
        assert "ENFORCEMENT" not in msg
        assert "CONTEXT BUDGET ALERT — H-CE01" in msg
        assert "byte-size fallback" in msg


class TestTokenCountVsByteSizeDivergence:
    def test_large_non_text_metadata_does_not_trigger_token_based_alert(self, tmp_path):
        # Byte-size and token-count disagree here on purpose: most of the file's bytes
        # sit in fields _load_turns_from_transcript never extracts as conversational
        # text (a tool-result-shaped object with no "content" key), so raw byte-size
        # comfortably exceeds both legacy KB thresholds while the actual token-count
        # estimate of real turn text stays near zero. This is exactly the gap Harness
        # R10 flagged: a byte-size-only signal would have over-triggered here.
        transcript = tmp_path / "transcript.jsonl"
        lines = [json.dumps({
            "type": "user",
            "message": {"content": [{"type": "text", "text": "hello"}]},
        })]
        for _ in range(5):
            lines.append(json.dumps({"type": "tool_result", "toolUseResult": {"blob": "x" * 400_000}}))
        with open(transcript, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        assert os.path.getsize(transcript) > 1500 * 1024  # would have crossed both legacy thresholds

        proc = _run_hook(str(transcript))
        assert proc.returncode == 0
        assert proc.stdout.strip() == ""  # token-based signal stays near zero: no alert at all
