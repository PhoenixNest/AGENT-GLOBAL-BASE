#!/usr/bin/env python3
# H-CE01: UserPromptSubmit — Context Budget Alert (Python port)
# Reads transcript_path file size as a session-length proxy. When it exceeds the
# threshold, injects additionalContext directing Claude to apply Sacred Context
# principles from CC-00 engineering/harness-engineering/implementations/context_monitor.py.
#
# Ports .claude/hooks/context-budget-alert.ps1 and .claude/hooks/context-budget-alert.sh
# to a single stdlib-only Python 3 implementation. This hook never denies/blocks a
# turn — every code path below terminates with exit 0 — but as of the enforcement
# path below it is no longer purely advisory text: past a second, higher threshold
# it actually runs compression, not just an alert message.
#
# --- Enforcement path (Harness Engineering Remediation, item I5, 2026-08-23) ------
# The CC-00 Context/Harness benchmarks (2026-08-16) flagged this hook as stopping at
# an advisory alert with no code path that actually compresses anything (Context R1,
# relocated into the Harness Implementation Plan as item I5 because the fix lands in
# this Harness-owned hook file). Past ENFORCEMENT_THRESHOLD_KB, this hook now invokes
# core-component-00/engineering/context-engineering/implementations/context_compressor.py's
# ContextCompressor.compress_history() directly against the transcript and injects
# the actual compacted result — not a repeated reminder — as additionalContext.
# Below that threshold (but above ALERT_THRESHOLD_KB) it still only alerts, unchanged
# from before. The byte-size signal is an interim proxy for utilization, same as the
# alert path already used — a true token-count signal is a distinct follow-up, not a
# blocker for this fix. Full arbitration: core-component-00/remediation/engineering/
# harness-engineering/2026-08-17-harness-engineering-remediation/log/
# 02-approval-i1-i5-arbitrated.md.
# -----------------------------------------------------------------------------------

import json
import os
import sys

from _hook_log import log_invocation

ALERT_THRESHOLD_KB = 500
ENFORCEMENT_THRESHOLD_KB = 1500
COMPRESSOR_TARGET_TOKENS = 4000


def _load_turns_from_transcript(transcript_path: str, max_lines: int = 5000):
    """Best-effort parse of a transcript JSONL file into
    {"role": ..., "content": ...} dicts for ContextCompressor.compress_history().
    Skips lines that don't parse or don't look like a message — this feeds an
    advisory enforcement path, not a strict schema validator, so odd/partial
    input degrades to fewer turns rather than raising."""
    turns = []
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if not isinstance(obj, dict):
                    continue
                role = obj.get("type") or obj.get("role")
                message = obj.get("message") if isinstance(obj.get("message"), dict) else obj
                content = message.get("content") if isinstance(message, dict) else None
                if isinstance(content, list):
                    content = " ".join(
                        block.get("text", "")
                        for block in content
                        if isinstance(block, dict) and block.get("type") == "text"
                    )
                if not isinstance(content, str) or not content:
                    continue
                turns.append({"role": role or "user", "content": content})
    except OSError:
        return []
    return turns


def _run_enforcement_compaction(transcript_path: str, session_id):
    """Actually invoke ContextCompressor.compress_history() against the transcript
    — the enforcement action itself, not just a repeated alert. Returns a
    CompressionResult, or None if there was nothing usable to compress."""
    hooks_dir = os.path.dirname(os.path.abspath(__file__))
    ce_root = os.path.normpath(
        os.path.join(hooks_dir, "..", "..", "core-component-00", "engineering", "context-engineering")
    )
    if ce_root not in sys.path:
        sys.path.insert(0, ce_root)

    from implementations.context_compressor import ContextCompressor

    turns = _load_turns_from_transcript(transcript_path)
    if not turns:
        return None

    compressor = ContextCompressor()
    result = compressor.compress_history(turns, target_tokens=COMPRESSOR_TARGET_TOKENS)

    log_invocation(
        "context-budget-alert", "UserPromptSubmit", decision="enforcement_compaction_run",
        session_id=session_id,
        extra={
            "strategy": result.strategy,
            "original_tokens": result.original_tokens,
            "compressed_tokens": result.compressed_tokens,
        },
    )
    return result


def _render_compacted_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        lines = [
            f"[{turn.get('role', 'system')}]: {turn.get('content', '')}"
            for turn in content
            if isinstance(turn, dict)
        ]
        return "\n".join(lines)
    return str(content)


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    # Guard against non-dict top-level JSON (e.g. a JSON array/number), which
    # the bash original's inline `d.get(...)` would crash on (uncaught
    # AttributeError -> traceback on stderr, though it still nets out to
    # exit 0 for the outer bash script). The ps1 original never crashes here
    # because PowerShell property access on a non-object silently yields
    # $null. We reconcile on the ps1 original's silent behavior.
    transcript = ""
    if isinstance(data, dict):
        transcript = data.get("transcript_path", "") or ""

    if not transcript:
        return 0
    if not os.path.isfile(transcript):
        return 0

    try:
        size_bytes = os.path.getsize(transcript)
    except OSError:
        return 0

    # Round to nearest KB via the bash original's "+512, integer-divide"
    # arithmetic (round-half-up). The ps1 original instead calls
    # [math]::Round(bytes / 1KB), which is .NET banker's rounding
    # (round-half-to-even) — the two originals disagree only at an exact
    # half-KB boundary. We follow the bash original here since that is the
    # version actually wired into settings.json's UserPromptSubmit hook chain
    # (invoked via `bash ... context-budget-alert.sh` regardless of platform).
    size_kb = (size_bytes + 512) // 1024
    threshold_kb = ALERT_THRESHOLD_KB

    session_id = data.get("session_id") if isinstance(data, dict) else None

    if size_kb < threshold_kb:
        log_invocation("context-budget-alert", "UserPromptSubmit", decision="under_threshold",
                        session_id=session_id, extra={"size_kb": size_kb})
        return 0

    log_invocation("context-budget-alert", "UserPromptSubmit", decision="threshold_exceeded",
                    session_id=session_id, extra={"size_kb": size_kb})

    compaction_result = None
    if size_kb >= ENFORCEMENT_THRESHOLD_KB:
        try:
            compaction_result = _run_enforcement_compaction(transcript, session_id)
        except Exception:
            # Advisory-hook contract: a compaction failure degrades to the plain
            # alert below, it never fails the turn.
            compaction_result = None

    if compaction_result is not None:
        msg = (
            "[CONTEXT BUDGET ALERT — H-CE01 — ENFORCEMENT]\n"
            f"Session transcript size: {size_kb} KB "
            f"(alert: {threshold_kb} KB, enforcement: {ENFORCEMENT_THRESHOLD_KB} KB)\n"
            "\n"
            f"context_compressor.py's compaction routine ran automatically "
            f"(strategy={compaction_result.strategy}, "
            f"{compaction_result.original_tokens} -> {compaction_result.compressed_tokens} tokens, "
            f"{compaction_result.compression_ratio:.0%} reduction).\n"
            "Treat the compacted history below as the basis for continuing the session — do not "
            "re-expand the full transcript back into context.\n"
            "\n"
            "Compacted content follows:\n"
            f"{_render_compacted_content(compaction_result.content)}"
        )
        system_message = (
            f"[H-CE01: enforcement compaction ran — "
            f"{compaction_result.compression_ratio:.0%} reduction]"
        )
    else:
        msg = (
            "[CONTEXT BUDGET ALERT — H-CE01]\n"
            f"Session transcript size: {size_kb} KB (threshold: {threshold_kb} KB)\n"
            "\n"
            "The session context is growing large. Apply Sacred Context principles before responding:\n"
            "- Preserve decision-critical context (System and Working slots) losslessly\n"
            "- Compress or summarize non-critical Conversation context where possible\n"
            "- If approaching model context limits, invoke context_compressor.py patterns\n"
            "- Prioritize: active task state > prior decisions > background knowledge\n"
            "Reference: core-component-00/engineering/harness-engineering/implementations/context_monitor.py"
        )
        system_message = f"[H-CE01: context budget alert — transcript at {size_kb} KB (threshold {threshold_kb} KB)]"

    output = {
        "systemMessage": system_message,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": msg,
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
