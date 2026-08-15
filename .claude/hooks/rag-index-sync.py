#!/usr/bin/env python3
"""H-RAG02: PostToolUse — RAG Index Sync on Doc Write (toggle-aware, phase-adaptive) (Python port)

Fires after Write or Edit tools modify .md files in KEY_DIRS.
Behavior is governed by
core-component-00/mcp-servers/workspace-knowledge/rag-system/rag-sync-state.json
(mode: auto|warn|off).
Phase adaptation: reads search_backend from state file to determine rebuild vs upsert path.
Phase 3 active (search_backend=qdrant): instructs upsert_document only; FAISS self-heals via
mtime on startup.

Ported from rag-index-sync.ps1 / rag-index-sync.sh for the OS-fork removal migration. Behavior
(including exit-code semantics) is intended to be identical to both originals: this hook is a
purely advisory PostToolUse notifier (it can only add `additionalContext`, never block or deny a
tool call), and every branch in both originals exits 0 — this port preserves that: it always
exits 0, on every path, including malformed/unexpected input.
"""

import json
import re
import sys
import time
from pathlib import Path

from _hook_log import log_invocation

KEY_DIRS = ("company/", "studio/", "core-component-00/", "telescope/")


def _load_state(state_file: Path):
    """Returns (mode, debounce_seconds, last_rebuild_at, backend), defaulting to
    warn/30/0/faiss for a missing file, an unreadable/non-JSON file, or any field
    that is absent/falsy in an otherwise-valid state file — mirrors both originals'
    per-field ``value or default`` fallback."""
    mode, debounce_seconds, last_rebuild_at, backend = "warn", 30, 0, "faiss"

    if state_file.is_file():
        try:
            state = json.loads(state_file.read_text())
            mode = state.get("mode") or "warn"
            debounce_seconds = state.get("debounce_seconds") or 30
            last_rebuild_at = state.get("last_rebuild_at") or 0
            backend = state.get("search_backend") or "faiss"
        except Exception:
            mode, debounce_seconds, last_rebuild_at, backend = "warn", 30, 0, "faiss"

    # last_rebuild_at: replicate the .sh original's digit-only guard EXACTLY, not
    # just "make it an int". The bash original does:
    #   case "$last_rebuild_at" in ''|*[!0-9]*) last_rebuild_at=0 ;; esac
    # which resets to 0 for the empty string OR any string containing a
    # non-digit character — that includes a leading '-' (negative numbers) and
    # a literal '.' (floats, even whole-number floats like 12.0), not just
    # values that fail int() outright. A plain int(x) coercion is too lenient:
    # int(-5) == -5 and int(12.5) == 12 both "succeed" in Python without ever
    # taking the reset branch, which would silently diverge from the .sh
    # original — e.g. a hand-edited/corrupted state file with a recent-looking
    # float last_rebuild_at would make this port wrongly treat a rebuild as
    # "within debounce" and suppress the advisory message, while the .sh
    # original (authoritative per the precedence rule) resets to 0 and fires
    # it. isdigit() reproduces the bash case pattern precisely: it is False
    # for '', for anything with a '-' or '.', and True only for a pure
    # nonnegative-integer string — matching str() of an int exactly, and
    # str() of a bool/float/negative/other JSON type never passing.
    last_rebuild_str = str(last_rebuild_at)
    last_rebuild_at = int(last_rebuild_str) if last_rebuild_str.isdigit() else 0

    # debounce_seconds: the .sh original has NO equivalent guard for this field
    # (only last_rebuild_at gets the digit-only case check) — a non-numeric
    # debounce_seconds in bash causes the `[ ... -lt "$debounce_seconds" ]`
    # arithmetic test to error to stderr and evaluate false, which fails the
    # debounce check *open* (never suppresses) while leaving the corrupt value
    # to also blow up the later `int(os.environ['DEB'])` state-file rewrite
    # (silently caught by that inline's own try/except, so the state file is
    # just left unwritten that turn). The .ps1 has no guard either and would
    # throw. Judgment call, kept as originally documented: coerce
    # debounce_seconds defensively here too so a corrupt/hand-edited state
    # file can never crash this hook — this is a deliberate, disclosed
    # divergence (safer: still debounces normally instead of firing on every
    # call), not an attempt at byte-for-byte parity like last_rebuild_at above.
    try:
        debounce_seconds = int(debounce_seconds)
    except (TypeError, ValueError):
        debounce_seconds = 30

    return mode, debounce_seconds, last_rebuild_at, backend


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    if not isinstance(data, dict):
        return 0

    tool_name = data.get("tool_name")
    if tool_name not in ("Write", "Edit"):
        return 0

    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0

    # Normalize to forward slashes for matching
    normalized_path = str(file_path).replace("\\", "/")

    in_key_dir = False
    for key_dir in KEY_DIRS:
        if re.search(r"(^|/)" + re.escape(key_dir), normalized_path):
            in_key_dir = True
            break
    if not in_key_dir:
        return 0

    if not re.search(r"\.md$", normalized_path):
        return 0

    # --- Resolve repo root from this script's own location (mirrors $PSScriptRoot's
    # two-parents-up climb in the .ps1, and BASH_SOURCE[0]'s dirname + ../../ in the
    # .sh — both resolve to the repo root without shelling out to git) ---
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    state_file = (
        repo_root
        / "core-component-00"
        / "mcp-servers"
        / "workspace-knowledge"
        / "rag-system"
        / "rag-sync-state.json"
    )

    mode, debounce_seconds, last_rebuild_at, backend = _load_state(state_file)
    session_id = data.get("session_id")

    # --- Select update tool for active migration phase ---
    update_tool = "upsert_document" if backend == "qdrant" else "rebuild_index"

    # --- Mode: off — exit silently ---
    if mode == "off":
        log_invocation("rag-index-sync", "PostToolUse", decision="off",
                        session_id=session_id, extra={"file_path": file_path})
        return 0

    # --- Mode: warn — passive notice only, no rebuild ---
    if mode == "warn":
        message = (
            "[RAG INDEX SYNC — H-RAG02 | MODE: WARN]\n"
            f"Indexed workspace document modified: {file_path}\n"
            "\n"
            "The workspace-knowledge index is now stale. Auto-sync is in WARN mode.\n"
            f"If you need up-to-date retrieval results this turn, call {update_tool} via the\n"
            "workspace-knowledge MCP before issuing search_docs, find_related_documents, or\n"
            "summarize_context queries.\n"
            "To enable automatic rebuilds: /rag-sync auto"
        )
        log_invocation("rag-index-sync", "PostToolUse", decision="warn",
                        session_id=session_id, extra={"file_path": file_path})
        print(
            json.dumps(
                {
                    "systemMessage": f"[H-RAG02: index stale — {file_path} modified (WARN mode)]",
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": message,
                    }
                }
            )
        )
        return 0

    # --- Mode: auto — debounce check, then emit rebuild instruction ---
    now = int(time.time())
    if (now - last_rebuild_at) < debounce_seconds:
        log_invocation("rag-index-sync", "PostToolUse", decision="debounced",
                        session_id=session_id, extra={"file_path": file_path})
        return 0  # within debounce window — suppress

    # Update last_rebuild_at in state file
    try:
        new_state = {
            "mode": mode,
            "debounce_seconds": debounce_seconds,
            "last_rebuild_at": now,
            "search_backend": backend,
        }
        state_file.write_text(json.dumps(new_state))
    except Exception:
        pass

    message = (
        "[RAG INDEX SYNC — H-RAG02 | MODE: AUTO]\n"
        f"Indexed workspace document modified: {file_path}\n"
        "\n"
        "Before issuing any search_docs, find_related_documents, summarize_context, or agent_knowledge_brief\n"
        f"query this turn, call {update_tool} via the workspace-knowledge MCP to ensure retrieval results\n"
        "reflect your changes.\n"
        "To switch to passive mode: /rag-sync warn    To disable: /rag-sync off"
    )
    log_invocation("rag-index-sync", "PostToolUse", decision="auto_rebuild",
                    session_id=session_id, extra={"file_path": file_path, "update_tool": update_tool})
    print(
        json.dumps(
            {
                "systemMessage": f"[H-RAG02: index rebuild required — {file_path} modified (AUTO mode)]",
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": message,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
