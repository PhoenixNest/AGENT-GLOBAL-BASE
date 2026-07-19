#!/usr/bin/env bash
# H-HE01: PreToolUse (Bash|PowerShell) — Tool Rate Limiter v2 (per-turn + session ceiling) (bash port)
#
# Maintains two independent counters per session:
#   1. Per-turn counter  — resets at the start of every prompt (via H-HE01-RESET hook)
#   2. Session counter   — cumulative for the entire chat session; never resets
#
# Two independent AskUserQuestion trigger paths:
#   Path A (per-turn limit, default 150)
#   Path B (session ceiling, default 1000)
#
# Reference: core-component-00/engineering/harness-engineering/implementations/tool_registry.py

raw_input=$(cat)

session_id=$(echo "$raw_input" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(d.get('session_id','') or '')")

[ -z "$session_id" ] && exit 0

safe_id=$(printf '%s' "$session_id" | tr -c 'a-zA-Z0-9' '-')
base="${TMPDIR:-/tmp}"

# --- File paths ---
turn_counter_file="$base/cc00-tool-counter-turn-$safe_id.txt"
turn_limit_file="$base/cc00-tool-limit-turn-$safe_id.txt"
session_counter_file="$base/cc00-tool-counter-session-$safe_id.txt"
session_limit_file="$base/cc00-tool-limit-session-$safe_id.txt"

# --- Read limits ---
default_turn_limit=150
default_session_limit=1000

read_positive_int() {
    # $1 = file; echoes parsed int if file holds a positive integer, else nothing
    [ -f "$1" ] || return
    local raw
    raw=$(tr -d '[:space:]' < "$1")
    case "$raw" in
        ''|*[!0-9]*) return ;;
    esac
    [ "$raw" -gt 0 ] 2>/dev/null && printf '%s' "$raw"
}

max_turn_calls=$default_turn_limit
parsed=$(read_positive_int "$turn_limit_file")
[ -n "$parsed" ] && max_turn_calls=$parsed

max_session_calls=$default_session_limit
parsed=$(read_positive_int "$session_limit_file")
[ -n "$parsed" ] && max_session_calls=$parsed

# --- Increment counters ---
read_count() {
    [ -f "$1" ] || { printf '0'; return; }
    local raw
    raw=$(tr -d '[:space:]' < "$1")
    case "$raw" in
        ''|*[!0-9]*) printf '0' ;;
        *) printf '%s' "$raw" ;;
    esac
}

turn_count=$(read_count "$turn_counter_file")
turn_count=$((turn_count + 1))
printf '%s' "$turn_count" > "$turn_counter_file"

session_count=$(read_count "$session_counter_file")
session_count=$((session_count + 1))
printf '%s' "$session_count" > "$session_counter_file"

# --- Path A: Per-turn limit check ---
if [ "$turn_count" -gt "$max_turn_calls" ]; then
    new_turn_limit=$((max_turn_calls + 100))

    msg="[TOOL RATE LIMITER — H-HE01 PATH A] Per-turn tool-call limit reached: $turn_count / $max_turn_calls calls this prompt.

MANDATORY: Use the AskUserQuestion tool to ask the user:

Question: \"Per-turn tool-call limit reached ($turn_count / $max_turn_calls this prompt). How would you like to proceed?\"

Options:
  A) \"Extend this turn by 100\" — raise the per-turn cap to $new_turn_limit for the remainder of this response only.
     Action: use the Write tool to write \"$new_turn_limit\" to: $turn_limit_file
     Then retry the blocked command.

  B) \"Set a custom limit\" — raise the per-turn cap to a number of the user's choosing.
     Action: ask the user \"How many additional tool calls would you like to allow this turn?\" then
     add their answer to $max_turn_calls and use the Write tool to write the result to: $turn_limit_file
     Then retry the blocked command.

  C) \"End this response\" — wrap up the current response and stop.
     Action: summarise progress and do not retry the blocked command.

NOTE: Any extension granted here is automatically removed at the start of the next prompt.
Reference: core-component-00/engineering/harness-engineering/implementations/tool_registry.py"

    reason="[TOOL RATE LIMITER — H-HE01] Per-turn limit reached: $turn_count / $max_turn_calls. See additionalContext for AskUserQuestion instructions."

    MSG="$msg" REASON="$reason" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':os.environ['REASON'],'additionalContext':os.environ['MSG']}}))"
    exit 0
fi

# --- Path B: Session ceiling check (only if Path A passed) ---
if [ "$session_count" -gt "$max_session_calls" ]; then
    new_session_limit=$((max_session_calls + 500))

    msg="[TOOL RATE LIMITER — H-HE01 PATH B] Session tool-call ceiling reached: $session_count / $max_session_calls total this session.

MANDATORY: Use the AskUserQuestion tool to ask the user:

Question: \"Session tool-call ceiling reached ($session_count / $max_session_calls total). How would you like to proceed?\"

Options:
  A) \"Extend session by 500\" — raise the session ceiling to $new_session_limit.
     Action: use the Write tool to write \"$new_session_limit\" to: $session_limit_file
     Then retry the blocked command.

  B) \"Set a custom session ceiling\" — raise the session ceiling to a number of the user's choosing.
     Action: ask the user \"How many additional session tool calls would you like to allow?\" then
     add their answer to $max_session_calls and use the Write tool to write the result to: $session_limit_file
     Then retry the blocked command.

  C) \"Remove session ceiling\" — no ceiling for the rest of this session.
     Action: use the Write tool to write \"999999\" to: $session_limit_file
     Then retry the blocked command.

  D) \"End conversation\" — wrap up and stop.
     Action: summarise progress and do not retry the blocked command.

Reference: core-component-00/engineering/harness-engineering/implementations/tool_registry.py"

    reason="[TOOL RATE LIMITER — H-HE01] Session ceiling reached: $session_count / $max_session_calls. See additionalContext for AskUserQuestion instructions."

    MSG="$msg" REASON="$reason" python3 -c "import os,json; print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':os.environ['REASON'],'additionalContext':os.environ['MSG']}}))"
    exit 0
fi

# Under both limits — allow through
exit 0
