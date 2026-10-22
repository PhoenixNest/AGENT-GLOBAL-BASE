# Research Report — Context and Command Threshold Plan

---

## Metadata

| Field                | Value                                                                            |
| -------------------- | -------------------------------------------------------------------------------- |
| **Investigation ID** | `2026-10-21-context-and-command-thresholds`                                      |
| **Date Started**     | 2026-10-21                                                                       |
| **Date Completed**   | In Progress                                                                      |
| **Status**           | In Progress                                                                      |
| **Investigator**     | CC-00 Harness Engineering (Kwame Asante) and Context Engineering (Mei-Ling Zhao) |
| **Laboratory**       | Core Component 00                                                                |
| **Module(s)**        | 02 Context Engineering, 03 Harness Engineering                                   |
| **Priority**         | Medium                                                                           |
| **Requestor**        | CEO                                                                              |

---

## Executive Summary

This report examines the context-based alert thresholds (H-CE01) and the command limits (H-HE01), sets them against vendor practice and Anthropic guidance, and proposes adjustments. It is a proposal for CEO review: nothing in it is carried out before the CEO decides, and no hook changes before then.

---

## Investigation Scope

### What Was Investigated

The current behaviour of the H-CE01 context budget alert and the H-HE01 tool rate limiter, the reference points set by vendor practice and Anthropic guidance, and what a Claude Code hook can see.

### Ownership and Implementation

Owner: Dr. Elias Vance, CC-00 Laboratory Director.

Implementation is by CC-00 Harness Engineering (Kwame Asante) and Context Engineering (Mei-Ling Zhao). Hooks are governance controls, so the change receives the independent review that `.claude/rules/layered-review.md` requires for risky work.

---

## Research Questions

1. Which adjustments to the context-based alert thresholds (H-CE01) does the evidence support?
2. Which adjustments to the command limits (H-HE01) does the evidence support?

---

## Findings

### Finding 1: H-CE01 context budget alert

`.claude/hooks/context-budget-alert.py` runs on `UserPromptSubmit`.

**Evidence:**

- It estimates tokens of the extracted user and assistant turn text in the transcript. It does not measure the full context: the system prompt, tool definitions, CLAUDE.md files and rules are not counted.
- The alert fires at 32,000 tokens and enforcement at 96,000. The code's only stated basis is a 3× ratio copied from its byte fallback (500 KB / 1,500 KB). No external source backs the values.
- It fires on every prompt once above 32,000. It has no once-per-crossing memory.
- Above 96,000 it runs `ContextCompressor.compress_history()` to a 4,000-token target and injects the compressed text as `additionalContext` on every prompt.

**Implications:**

- Claude Code adds `additionalContext` to the context ("String added to Claude's context alongside the submitted prompt", hooks documentation). A hook cannot remove anything from the context. The enforcement path therefore adds about 4,000 tokens per prompt instead of reducing the context.

---

### Finding 2: H-HE01 tool rate limiter

`.claude/hooks/harness-tool-rate-limiter.py` runs on `PreToolUse`, registered for `Bash|PowerShell` only.

**Evidence:**

- Per-turn limit: 150. Options at the limit: extend by 100, custom, end response.
- Session ceiling: 1,000. Options at the ceiling: extend by 500, custom, remove, end conversation.

**Implications:**

- Both count shell commands only. File reads, edits, searches and sub-agent calls are not counted, so neither limit measures effort or cost.

---

### Finding 3: Vendor practice

Vendor practice, verified against official documentation:

| Source                                | Practice                                                                                                                                                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Anthropic API, context editing        | Clears old tool results from 100,000 input tokens by default                                                                                                                                                                         |
| Anthropic API, server-side compaction | Defaults to 150,000 input tokens                                                                                                                                                                                                     |
| Claude Code, auto-compaction          | Compacts when the conversation reaches the model's context limit (about 967K for 1M-token models). `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (1-100) can only lower the trigger; `CLAUDE_CODE_AUTO_COMPACT_WINDOW` accepts 100,000-1,000,000 |
| Claude Code, limits                   | `--max-turns` and `--max-budget-usd` (print mode only) have no default                                                                                                                                                               |
| Claude Agent SDK                      | `max_turns` and `max_budget_usd` default to none                                                                                                                                                                                     |
| Gemini CLI                            | Compresses at 50% of the window (`model.compressionThreshold` 0.5); unlimited session turns by default                                                                                                                               |
| Google ADK                            | `max_llm_calls` 500 per run                                                                                                                                                                                                          |
| LangGraph                             | `recursion_limit` 1,000 steps per run                                                                                                                                                                                                |
| OpenAI Agents SDK                     | `max_turns` raises `MaxTurnsExceeded`                                                                                                                                                                                                |

---

### Finding 4: Anthropic guidance

Anthropic's guidance ("Effective context engineering for AI agents"; "How we built our multi-agent research system"):

- Compaction, and structured note-taking outside the context.
- Sub-agents return condensed results of 1,000-2,000 tokens.
- Context rot grows as the context fills.
- Token usage explained 80% of performance variance, and effort is scaled to task complexity.

---

### Finding 5: What a hook can see

Claude Code documentation:

- Hooks receive `session_id`, `transcript_path`, `cwd` and `hook_event_name`, but not the model or its window size. Only `SessionStart` may receive `model`.
- The status line command receives `context_window.used_percentage` (input, cache-creation and cache-read tokens of the latest response), `context_window.context_window_size` (200,000 by default, 1,000,000 for extended-context models) and `cost.total_cost_usd` (a client-side estimate).
- The transcript is JSONL whose entry format is internal and changes between versions.
- A `PreCompact` hook exists (matchers `manual`, `auto`) and can block compaction.
- No documented way exists for a hook to start compaction.

---

## Recommendations

### Proposed Design

#### 1. Measure the real context

A small status-line writer records, per session, `used_percentage`, `context_window_size` and `cost.total_cost_usd` into a state file in the system temp folder. H-CE01 reads it.

The status line is one command per settings scope, so the writer chains to any status line the User already runs and never replaces it.

When no fresh value exists (non-interactive runs, sub-agents, a stale file), H-CE01 falls back to the existing turn-text estimate, expressed as a fraction of a configured window size.

#### 2. Bands as fractions of the window

The bands are fractions of the auto-compact window: the model's window, or the smaller value set in `CLAUDE_CODE_AUTO_COMPACT_WINDOW`. The hook and Claude Code's own compaction therefore share one base. On a 1M-token model, 50% of the full window is 500,000 tokens, well past where context rot sets in, so a working window below 1M for this workspace is set from the calibration data (see Calibration).

Each band fires once per upward crossing. The last band reached is kept in the state file, and a compaction resets it.

- **50%.** One advisory that the context is half full; apply Sacred Context.
- **70%.** Session-boundary update. The orchestrator brings `progress.md`, `session-log.md` and `checkpoint.json` up to date and copies the User's standing directives verbatim into `progress.md`, so a later compaction loses nothing.
- **85%.** The hook recommends that the User run `/compact` after the boundary update.

Claude Code's own auto-compaction near the limit stays as the hard backstop. A `PreCompact` hook (`auto`) does not block. It records that compaction happened, so the next prompt's alert points the session at `progress.md` to restore working state.

Why these values. 50% follows Gemini CLI's default and acts before context rot sets in. 70% leaves room to write the boundary files: 60,000 tokens on a 200,000 window, 300,000 on a 1M window. 85% sits before Claude Code's own trigger. They are engineering judgments, not vendor-set constants, and are recalibrated after two weeks of logged data (see Calibration).

#### 3. Remove the fixed alert and the enforcement injection

The 96,000 enforcement injection and the fixed 32,000 alert are removed. The 85% band replaces enforcement with real compaction by Claude Code.

#### 4. Per-turn runaway guard

The shell cap stays at 150 per turn. For two weeks the hook also logs, and never blocks on, the count of all tool calls per turn. An all-tools per-turn cap is then proposed from that data (for example three times the 99th percentile observed), so the cap is grounded in this workspace's own usage.

#### 5. Session budget in place of the command ceiling

The 1,000-command session ceiling is replaced by a session budget measured in estimated cost (`cost.total_cost_usd` from the state file).

The default is no hard ceiling, matching vendor defaults. The User can set a budget per session. At the budget, the hook first requires the session-boundary update, then asks whether to extend the budget, checkpoint and continue, or checkpoint and end.

The cost figure is a client-side estimate and can differ from the bill.

#### 6. Session-boundary triggers

The approved session-boundary rule takes its triggers from this report. The triggers are: the 70% band, the session budget, the User's request, and the end of each CEO round.

### Calibration

After release, the existing hook log is collected for two weeks (`log_invocation` already records the signal). The owners adjust bands and caps from that data, with the CEO's decision.

### Delivery and Review

CC-00 implements the work, with unit tests covering:

- a band crossing fires once;
- the band resets after compaction;
- a stale or missing state file falls back to the estimate;
- status-line chaining;
- timing.

It receives independent review and is recorded in a CC-00 maintenance record. It is live only after the CEO releases it.

---

## References

### External Sources

- Claude Code hooks documentation
- Anthropic API, context editing
- Anthropic API, server-side compaction
- Claude Code, auto-compaction and limits
- Claude Agent SDK
- Gemini CLI
- Google ADK
- LangGraph
- OpenAI Agents SDK
- "Effective context engineering for AI agents" (Anthropic)
- "How we built our multi-agent research system" (Anthropic)

---

## Open Questions

Limits of the proposed design:

- The status line does not run in non-interactive (`-p`) sessions or inside sub-agents, so the fallback estimate applies there.
- The transcript format is internal.
- The cost estimate differs from billing.
- A hook can recommend compaction but cannot start it.

---

## Version History

| Version | Date       | Author           | Changes                 |
| ------- | ---------- | ---------------- | ----------------------- |
| 1.0     | 2026-10-21 | CC-00 Laboratory | Initial research report |
