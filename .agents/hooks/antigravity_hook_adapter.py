#!/usr/bin/env python3
"""
antigravity_hook_adapter.py — Google Antigravity Lifecycle Hook Adapter.

Bridges Antigravity lifecycle events (PreInvocation, PreToolUse, PostToolUse, Stop)
to workspace governance policies, CC-00 prompt optimization (H-P01), ASGF compliance (H-P03),
and Git/shell safety rules.

State Directory Isolation:
  Strictly isolated to .agents/hooks/.state/ — zero footprint in .claude/.
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Workspace and State Paths (Strictly within .agents/)
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
_AGENTS_DIR = _SCRIPT_DIR.parent
_WORKSPACE_ROOT = _AGENTS_DIR.parent
_STATE_DIR = _SCRIPT_DIR / ".state"
_STATE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# CC-00 Prompt Quality Dimensions (H-P01 Parity)
# ---------------------------------------------------------------------------
_DIM1_ROLE_RE = re.compile(
    r"\b(act as|as (the|a)|role|persona|expert in|lead|engineer|director|cdo|cto|cpo|clo|chro|cio|cso)\b",
    re.IGNORECASE,
)
_DIM2_FORMAT_RE = re.compile(
    r"\b(format|table|markdown|list|bullet|report|json|schema|adr|tsv|csv|diagram|code snippet)\b",
    re.IGNORECASE,
)
_DIM3_GROUNDING_RE = re.compile(
    r"\b(stage \d|pipeline|asgf|adr-|department|rules/|company/|studio/|core-component-00/|cc-00|telescope)\b",
    re.IGNORECASE,
)
_DIM4_VERB_RE = re.compile(
    r"\b(create|write|generate|review|analyze|implement|refactor|explain|fix|update|add|remove|build|design|audit|produce|draft|summarize|compare|evaluate|plan|scaffold|describe)\b",
    re.IGNORECASE,
)
_DIM5_CONSTRAINT_RE = re.compile(
    r"\b(don't|do not|must not|never|only|without|avoid|exclude|limit to|max|strictly|ensure)\b",
    re.IGNORECASE,
)

ALL_MISSING_LABELS = [
    "role/persona context",
    "output format specification",
    "workspace or pipeline grounding",
    "clear imperative task verb",
    "constraints or acceptance criteria",
]
QUALITY_THRESHOLD = 3


# ---------------------------------------------------------------------------
# ASGF Governance Violations Pattern List (H-P03 Parity)
# ---------------------------------------------------------------------------
ASGF_VIOLATIONS = [
    (
        r"skip.{0,40}(stage|gate|pipeline|review|approval)",
        "Pipeline stages cannot be skipped — AGENTS.md §8 (hard stop)",
    ),
    (
        r"(downgrade|change|override|ignore|bypass).{0,40}(P0|P1|severity|defect|critical|blocker)",
        "P0/P1 defect classification is non-overridable — AGENTS.md §8",
    ),
    (
        r"(remove|weaken|disable|trim|strip).{0,30}(feature|security|functionality|test).{0,30}(pass|review|gate|check)",
        "Trim-to-Pass is a P0 defect — removing features to pass a review is blocked — AGENTS.md §8",
    ),
    (
        r"(force.{0,10}push|push.{0,10}(-f\b|--force\b)).{0,20}(master|main)",
        "Force-pushing to master is prohibited — AGENTS.md §6, rules/git-workflow.md",
    ),
    (
        r"auto.{0,20}advance.{0,20}(stage|gate|pipeline)",
        "Auto-advancing past User Approval gates is forbidden — AGENTS.md §8",
    ),
]


# ---------------------------------------------------------------------------
# Event Handlers
# ---------------------------------------------------------------------------
def handle_pre_invocation(payload: dict) -> dict:
    """PreInvocation: Score prompt quality ONLY on fresh USER_INPUT events."""
    conv_id = payload.get("conversationId", "")
    transcript_path = payload.get("transcriptPath")

    if not transcript_path or not os.path.exists(transcript_path):
        return {}

    # Read the absolute latest entry in transcript
    last_entry = None
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in reversed(f.readlines()):
                line = line.strip()
                if line:
                    try:
                        last_entry = json.loads(line)
                        break
                    except Exception:
                        continue
    except Exception:
        pass

    if not last_entry:
        return {}

    # ONLY evaluate if the absolute last step in transcript is a fresh USER_INPUT
    entry_type = last_entry.get("type", "")
    entry_source = last_entry.get("source", "")
    if entry_type != "USER_INPUT" and entry_source != "USER_EXPLICIT":
        # Intermediate agent turn (e.g. after tool calls, ask_question, etc.) -> Bypass
        return {}

    latest_user_text = last_entry.get("content", "")
    if not latest_user_text:
        return {}

    # Strip system reminders if embedded in user text
    clean_text = re.sub(r"<system-reminder>.*?</system-reminder>", "", latest_user_text, flags=re.DOTALL).strip()

    # 1. Bypass Confirmation Answers (from ask_question or user confirmation)
    is_confirmation = bool(re.match(
        r"^\s*(A\d+:|\(Recommended\)|yes\b|no\b|ok\b|approve\b|proceed\b|looks good\b|that works\b|perfect\b)",
        clean_text,
        re.IGNORECASE
    ))
    if is_confirmation:
        if conv_id:
            marker_path = _STATE_DIR / f"h-p01-pending-{conv_id}.json"
            if marker_path.is_file():
                try:
                    os.remove(marker_path)
                except OSError:
                    pass
        return {}

    # 2. Check ASGF Violations
    inject_steps = []
    detected = []
    for pattern, rule in ASGF_VIOLATIONS:
        if re.search(pattern, clean_text, re.IGNORECASE):
            detected.append(rule)

    if detected:
        rule_list = "\n".join(f"  * {r}" for r in detected)
        ephemeral = (
            f"[ASGF GOVERNANCE ALERT — H-P03]\n"
            f"Potential governance violation detected in user prompt:\n{rule_list}\n"
            f"Adhere strictly to AGENTS.md §8 and ASGF standards."
        )
        inject_steps.append({"ephemeralMessage": ephemeral})

    # 3. Bypass short prompts (<20 chars) and slash commands
    if len(clean_text) < 20 or clean_text.startswith("/"):
        return {"injectSteps": inject_steps} if inject_steps else {}

    # 4. Native CC-00 Prompt Quality Scoring (H-P01)
    score = 0
    missing = []
    if _DIM1_ROLE_RE.search(clean_text):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[0])

    if _DIM2_FORMAT_RE.search(clean_text):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[1])

    if _DIM3_GROUNDING_RE.search(clean_text):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[2])

    if _DIM4_VERB_RE.search(clean_text):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[3])

    if _DIM5_CONSTRAINT_RE.search(clean_text):
        score += 1
    else:
        missing.append(ALL_MISSING_LABELS[4])

    if score < QUALITY_THRESHOLD and conv_id:
        # Write pending marker strictly inside .agents/hooks/.state/
        marker_path = _STATE_DIR / f"h-p01-pending-{conv_id}.json"
        try:
            with open(marker_path, "w", encoding="utf-8") as f:
                json.dump({"pending": True, "ts": datetime.datetime.now().isoformat(), "score": score}, f)
        except OSError:
            pass

        missing_str = ", ".join(missing)
        reminder = (
            f"[PROMPT OPTIMIZER — H-P01]\n"
            f"<status>\n"
            f"Quality score: {score}/5 (threshold: {QUALITY_THRESHOLD}/5)\n"
            f"Missing dimensions: {missing_str}\n"
            f"</status>\n"
            f"<context>\n"
            f"This prompt is below the quality threshold. Complete step 2 confirmation using ask_question before proceeding.\n"
            f"</context>"
        )
        inject_steps.append({"ephemeralMessage": f"<system-reminder>\n{reminder}\n</system-reminder>"})

    return {"injectSteps": inject_steps} if inject_steps else {}


def handle_pre_tool_use(payload: dict) -> dict:
    """PreToolUse: Gate tool execution against state markers and safety rules."""
    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})
    conv_id = payload.get("conversationId", "")

    # 1. Enforce H-P01 Prompt Quality Gate
    if conv_id and tool_name != "ask_question":
        marker_path = _STATE_DIR / f"h-p01-pending-{conv_id}.json"
        if marker_path.is_file():
            try:
                with open(marker_path, "r", encoding="utf-8") as f:
                    marker = json.load(f)
                ts = datetime.datetime.fromisoformat(marker["ts"])
                now = datetime.datetime.now(ts.tzinfo) if ts.tzinfo else datetime.datetime.now()
                # Stale age safety valve: 15 minutes
                if (now - ts).total_seconds() > 900:
                    try:
                        os.remove(marker_path)
                    except OSError:
                        pass
                else:
                    return {
                        "decision": "deny",
                        "reason": f"[H-P01] Tool call '{tool_name}' blocked: prompt optimization confirmation is pending."
                    }
            except Exception:
                pass

    # 2. Git & Shell Command Safety Guards
    if tool_name == "run_command":
        cmd = args.get("CommandLine", "").strip()
        if re.search(r"(force.{0,10}push|push.{0,10}(-f\b|--force\b)).{0,20}(master|main)", cmd, re.IGNORECASE):
            return {
                "decision": "deny",
                "reason": "[GIT GUARD] Force-pushing to master/main is prohibited per AGENTS.md §6 and git-workflow.md."
            }

    return {"decision": "allow"}


def handle_post_tool_use(payload: dict) -> dict:
    """PostToolUse: Clear confirmation markers on ask_question completion."""
    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    conv_id = payload.get("conversationId", "")

    if tool_name == "ask_question" and conv_id:
        marker_path = _STATE_DIR / f"h-p01-pending-{conv_id}.json"
        if marker_path.is_file():
            try:
                os.remove(marker_path)
            except OSError:
                pass

    return {}


def handle_stop(payload: dict) -> dict:
    """Stop: Clean exit."""
    return {"decision": "continue" if payload.get("error") and not payload.get("fullyIdle") else "stop"}


# ---------------------------------------------------------------------------
# Main CLI Entry Point
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity Lifecycle Hook Adapter")
    parser.add_argument("--event", required=True, choices=["PreInvocation", "PreToolUse", "PostToolUse", "Stop"])
    args = parser.parse_args()

    raw_input = sys.stdin.read().strip()
    payload = {}
    if raw_input:
        try:
            payload = json.loads(raw_input)
        except Exception:
            payload = {}

    if args.event == "PreInvocation":
        result = handle_pre_invocation(payload)
    elif args.event == "PreToolUse":
        result = handle_pre_tool_use(payload)
    elif args.event == "PostToolUse":
        result = handle_post_tool_use(payload)
    elif args.event == "Stop":
        result = handle_stop(payload)
    else:
        result = {}

    sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
