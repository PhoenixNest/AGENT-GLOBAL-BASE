#!/usr/bin/env bash
# H-RAG02: PostToolUse — RAG Index Sync on Doc Write (toggle-aware, phase-adaptive) (bash port)
# Fires after Write or Edit tools modify .md files in KEY_DIRS.
# Behavior is governed by .claude/mcp-servers/workspace-knowledge/rag-system/rag-sync-state.json (mode: auto|warn|off).
# Phase adaptation: reads search_backend from state file to determine rebuild vs upsert path.

raw_input=$(cat)

tool_name=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('tool_name','') or '')")

case "$tool_name" in
    Write|Edit) ;;
    *) exit 0 ;;
esac

file_path=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print((d.get('tool_input') or {}).get('file_path','') or '')")

[ -z "$file_path" ] && exit 0

normalized_path=$(printf '%s' "$file_path" | tr '\\' '/')

in_key_dir=0
for dir in "company/" "studio/" "core-component-00/" "telescope/"; do
    echo "$normalized_path" | grep -qE "(^|/)$dir" && in_key_dir=1
done

[ "$in_key_dir" -eq 0 ] && exit 0
echo "$normalized_path" | grep -qE '\.md$' || exit 0

# --- Read toggle state (defaults to warn if state file absent) ---
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
state_file="$script_dir/../mcp-servers/workspace-knowledge/rag-system/rag-sync-state.json"

mode="warn"
debounce_seconds=30
last_rebuild_at=0
backend="faiss"

if [ -f "$state_file" ]; then
    state_vals=$(STATE_FILE="$state_file" python3 -c "
import os,json
try:
    s=json.load(open(os.environ['STATE_FILE']))
except Exception:
    print('warn|30|0|faiss'); raise SystemExit
mode=s.get('mode') or 'warn'
deb=s.get('debounce_seconds') or 30
lra=s.get('last_rebuild_at') or 0
be=s.get('search_backend') or 'faiss'
print(f'{mode}|{deb}|{lra}|{be}')")
    mode="${state_vals%%|*}"; rest="${state_vals#*|}"
    debounce_seconds="${rest%%|*}"; rest="${rest#*|}"
    last_rebuild_at="${rest%%|*}"; backend="${rest##*|}"
fi

# --- Select update tool for active migration phase ---
if [ "$backend" = "qdrant" ]; then
    update_tool="upsert_document"
else
    update_tool="rebuild_index"
fi

# --- Mode: off — exit silently ---
[ "$mode" = "off" ] && exit 0

# --- Mode: warn — passive notice only, no rebuild ---
if [ "$mode" = "warn" ]; then
    msg="[RAG INDEX SYNC — H-RAG02 | MODE: WARN]
Indexed workspace document modified: $file_path

The workspace-knowledge index is now stale. Auto-sync is in WARN mode.
If you need up-to-date retrieval results this turn, call $update_tool via the
workspace-knowledge MCP before issuing search_docs, find_related_documents, or
summarize_context queries.
To enable automatic rebuilds: /rag-sync auto"
    MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PostToolUse','additionalContext':os.environ['MSG']}}))"
    exit 0
fi

# --- Mode: auto — debounce check, then emit rebuild instruction ---
now=$(date -u +%s)
case "$last_rebuild_at" in
    ''|*[!0-9]*) last_rebuild_at=0 ;;
esac
if [ "$((now - last_rebuild_at))" -lt "$debounce_seconds" ]; then
    exit 0
fi

# Update last_rebuild_at in state file
STATE_FILE="$state_file" MODE="$mode" DEB="$debounce_seconds" NOW="$now" BACKEND="$backend" python3 -c "
import os,json
try:
    with open(os.environ['STATE_FILE'],'w') as f:
        json.dump({'mode':os.environ['MODE'],'debounce_seconds':int(os.environ['DEB']),'last_rebuild_at':int(os.environ['NOW']),'search_backend':os.environ['BACKEND']},f)
except Exception:
    pass" 2>/dev/null

msg="[RAG INDEX SYNC — H-RAG02 | MODE: AUTO]
Indexed workspace document modified: $file_path

Before issuing any search_docs, find_related_documents, summarize_context, or agent_knowledge_brief
query this turn, call $update_tool via the workspace-knowledge MCP to ensure retrieval results
reflect your changes.
To switch to passive mode: /rag-sync warn    To disable: /rag-sync off
Reference: telescope/2026-06-25-qdrant-migration-plan/plans/05-hook-design.md"

MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PostToolUse','additionalContext':os.environ['MSG']}}))"
exit 0
