"""
Regression test for context-budget-alert.py's enforcement path (Harness
Implementation Plan, item I5, 2026-08-23).

Invokes the hook exactly as production does: a subprocess fed the hook's stdin
JSON contract, asserting on its stdout JSON. Run with:
    pytest .claude/hooks/test_context_budget_alert.py -v
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


def _write_transcript(path, size_kb, turn_count=20):
    """Write a valid JSONL transcript of at least size_kb: turn_count small
    user/assistant lines plus one padding line to reach the target size."""
    lines = []
    for i in range(turn_count):
        role = "user" if i % 2 == 0 else "assistant"
        lines.append(json.dumps({
            "type": role,
            "message": {"content": [{"type": "text", "text": f"turn {i} content about topic {i % 7}"}]},
        }))
    content = "\n".join(lines) + "\n"
    target_bytes = size_kb * 1024
    if len(content.encode("utf-8")) < target_bytes:
        pad_needed = target_bytes - len(content.encode("utf-8")) - 60
        content += json.dumps({
            "type": "user",
            "message": {"content": [{"type": "text", "text": "x" * max(pad_needed, 0)}]},
        }) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


class TestAlertOnlyBelowThresholds:
    def test_under_alert_threshold_produces_no_output(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        _write_transcript(str(transcript), size_kb=100, turn_count=5)
        proc = _run_hook(str(transcript))
        assert proc.returncode == 0
        assert proc.stdout.strip() == ""

    def test_between_alert_and_enforcement_alerts_without_compacting(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        _write_transcript(str(transcript), size_kb=800, turn_count=20)
        proc = _run_hook(str(transcript))
        assert proc.returncode == 0
        output = json.loads(proc.stdout)
        msg = output["hookSpecificOutput"]["additionalContext"]
        assert "CONTEXT BUDGET ALERT — H-CE01" in msg
        assert "ENFORCEMENT" not in msg
        assert "compaction routine ran" not in msg


class TestEnforcementCompaction:
    def test_over_enforcement_threshold_actually_compacts(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        _write_transcript(str(transcript), size_kb=2000, turn_count=300)
        proc = _run_hook(str(transcript))
        assert proc.returncode == 0
        output = json.loads(proc.stdout)
        msg = output["hookSpecificOutput"]["additionalContext"]
        assert "ENFORCEMENT" in msg
        assert "compaction routine ran automatically" in msg
        assert "Compacted content follows:" in msg
        assert "reduction" in output["systemMessage"]

    def test_unparseable_transcript_falls_back_to_plain_alert(self, tmp_path):
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
