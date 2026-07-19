#!/usr/bin/env bash
# H-CE01: UserPromptSubmit — Context Budget Alert (bash port)
# Reads transcript_path file size as a session-length proxy. When it exceeds the
# threshold, injects additionalContext directing Claude to apply Sacred Context
# principles from CC-00 engineering/harness-engineering/implementations/context_monitor.py.

raw_input=$(cat)

transcript=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('transcript_path','') or '')")

[ -z "$transcript" ] && exit 0
[ ! -f "$transcript" ] && exit 0

size_bytes=$(wc -c < "$transcript" 2>/dev/null) || exit 0
size_kb=$(( (size_bytes + 512) / 1024 ))
threshold_kb=500

[ "$size_kb" -lt "$threshold_kb" ] && exit 0

msg="[CONTEXT BUDGET ALERT — H-CE01]
Session transcript size: ${size_kb} KB (threshold: ${threshold_kb} KB)

The session context is growing large. Apply Sacred Context principles before responding:
- Preserve decision-critical context (System and Working slots) losslessly
- Compress or summarize non-critical Conversation context where possible
- If approaching model context limits, invoke context_compressor.py patterns
- Prioritize: active task state > prior decisions > background knowledge
Reference: core-component-00/engineering/harness-engineering/implementations/context_monitor.py"

MSG="$msg" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'UserPromptSubmit','additionalContext':os.environ['MSG']}}))"
exit 0
