#!/usr/bin/env bash
# H-RAG01: UserPromptSubmit — RAG Knowledge Freshness Flag (bash port)
# Detects prompts containing time-sensitive language and injects additionalContext
# requiring Claude to disclose knowledge cutoff, flag stale claims, and cite
# retrieval dates. Grounded in CC-00 RAG Engineering freshness architecture.

raw_input=$(cat)

prompt=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('prompt','') or '')")

[ -z "$prompt" ] && exit 0
echo "$prompt" | grep -qE '^[[:space:]]*/' && exit 0

detected=0
echo "$prompt" | grep -qiE '\b(latest version|most recent version|current version)\b' && detected=1
echo "$prompt" | grep -qiE '\b(as of today|as of now|right now|currently|at the moment)\b' && detected=1
echo "$prompt" | grep -qiE '\b(latest release|new release|recent release)\b' && detected=1
echo "$prompt" | grep -qiE '\b(up to date|up-to-date|what.s new)\b' && detected=1
echo "$prompt" | grep -qiE '\b(this year|in [0-9]{4}|recent changes|recently added|just released)\b' && detected=1
echo "$prompt" | grep -qiE '\b(what version|which version|is.+supported|does.+support)\b' && detected=1

[ "$detected" -eq 0 ] && exit 0

msg="[RAG FRESHNESS FLAG — H-RAG01]
This prompt contains time-sensitive language.

Before responding, apply CC-00 RAG freshness protocol:
1. Disclose your knowledge cutoff (August 2025) when it affects accuracy
2. Mark potentially stale claims with [Knowledge Cutoff - verify]
3. If workspace telescope/ research reports exist on this topic, cite them
4. Prefer workspace documents (pipeline.md, library/, CC-00 docs) over training knowledge for workspace-specific facts
5. If retrieving external information, state the retrieval date
Reference: CC-00 RAG Engineering — retrieval freshness and source attribution"

MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'UserPromptSubmit','additionalContext':os.environ['MSG']}}))"
exit 0
