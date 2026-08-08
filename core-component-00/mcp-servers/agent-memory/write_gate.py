"""
write_gate.py — Human-facing confirmation gate + quarantine lane for a future
write-capable agent-memory MCP tool.

Built in response to reversal condition 1 of
telescope/2026-07-10-agent-memory-architecture/supporting/11-write-path-threat-model-phase1.md
§4 item 1 (see also §3.2 and §5): "A concrete write-tool design ... that routes
high-consequence writes ... through a genuinely human-facing, structurally-enforced
confirmation step — a PreToolUse/PostToolUse hook pair in the H-P01 shape, not an
in-process flag or docstring warning — with routine, non-colliding new-fact writes
going through a write-then-quarantine-then-async-review lane instead of a blocking
one."

No MCP write tool exists yet — that is Worker D's job, built on top of this module.
This file builds the gate mechanism and quarantine primitives standalone, with a
clear interface for Worker D to call into:

    gate = WriteConfirmationGate()
    lane = gate.classify(memory_type, sacred, would_collide_with_existing)
    if lane == "high_consequence":
        gate.request_confirmation(session_id, summary)
        # ... turn ends; PreToolUse hook (write-memory-gate-enforcer.py) blocks
        # every tool call except AskUserQuestion for this session until either
        # AskUserQuestion is called (PostToolUse hook write-memory-gate-clear.py
        # clears the marker) or the 15-minute stale-marker fail-safe fires ...
        allowed, reason = gate.check_confirmation(session_id)
        if not allowed:
            return {"written": False, "reason": reason}
    else:
        # commit immediately with status="quarantined" (see "Quarantine lane
        # contract" below) — never blocks.
        ...

---------------------------------------------------------------------------
REFLECT-003 compliance statement (read before relying on this module)
---------------------------------------------------------------------------

core-component-00/engineering/context-engineering/memory/reflection/reflection-log.jsonl
entry REFLECT-003 found, against a directly analogous mechanism in this same
workspace (the Investigator-Authored Write Path's identity-enforcement layer for
GOVERNANCE_TRIGGERS records), that no purely code-level check running inside
Claude Code's own tool-execution environment can be unforgeable — any
Python-importable layer is skippable by calling something lower, because an agent
has the same import access a human developer does. REFLECT-003's remediation was
not to delete the code-level layers but to reclassify them: keep them as
defense-in-depth against careless/accidental misuse, and move the actual security
boundary to genuine, live, in-transcript human confirmation, never relayed through
an intermediary agent.

This module follows that same shape, honestly:

- `WriteConfirmationGate` (the marker-file mechanism below) and the
  write-memory-gate-enforcer.py/write-memory-gate-clear.py hook pair are
  code-level layers. They are NOT an unforgeable boundary — exactly like
  `IdentityVerification` (memory_store.py) and the H-P01 marker mechanism it was
  itself modeled on, a caller who reads this module's source could construct
  marker files directly, delete them, or call whatever write path exists lower
  than this gate, bypassing it entirely. This module does not claim otherwise.
- What this module DOES provide, honestly bounded: it raises the bar against the
  zero-effort bypass (an agent silently skipping confirmation because nothing
  checks whether it happened), and it makes the confirmation step structurally
  hard to skip *for a normal interactive Claude Code session calling
  agent-memory through this workspace's own harness* — the same scope the H-P01
  pair itself claims, no broader. See the "Hook enforcement boundary" note below
  for the exact limitation statement.
- The actual security boundary for high-consequence writes, per REFLECT-003, is
  the live AskUserQuestion exchange itself — a real human answering a real
  question in the transcript — not this module's marker file or the hook pair
  that enforces waiting for it. This module's job is to make skipping that wait
  structurally awkward, not to make the wait itself unforgeable.

---------------------------------------------------------------------------
Hook enforcement boundary — exact, non-overclaiming scope statement
---------------------------------------------------------------------------

write-memory-gate-enforcer.py (PreToolUse) / write-memory-gate-clear.py
(PostToolUse, matcher: AskUserQuestion) provide a structurally-enforced
confirmation gate for writes initiated FROM AN INTERACTIVE CLAUDE CODE SESSION —
the primary real caller of agent-memory in this workspace, per
mcp-servers/agent-memory/README.md and the architecture decisions in
telescope/2026-07-10-agent-memory-architecture/. Within that scope, the hook
pair makes it structurally awkward (not impossible — see the REFLECT-003
statement above) for an agent to proceed with other tool calls in the same
session while a high-consequence write's confirmation marker is pending.

This is NOT a guarantee that holds against every conceivable MCP client. A
different MCP host, a direct stdio/HTTP client speaking the MCP protocol to this
server outside of Claude Code's own hook-executing harness, or a caller that
invokes agent-memory's Python functions directly (bypassing the MCP tool-call
layer entirely) is not touched by this mechanism at all — the hooks are
Claude-Code-harness-level constructs, not part of the MCP server process itself,
and nothing in this module or the hook pair can observe or block such a caller.
State this limitation plainly rather than imply "unforgeable": these hooks
narrow the failure window for the one real, in-scope caller this workspace
actually has today; they are not a network- or protocol-level security boundary.

---------------------------------------------------------------------------
Quarantine lane contract (per threat-model §3.2)
---------------------------------------------------------------------------

Routine new-fact writes with no existing-record collision (classify() ==
"routine") commit immediately — never block on human confirmation, which would
defeat the tool's purpose for the common case — but land in a distinct,
non-retrievable-by-default status lane pending async review:

    record.status = "quarantined"

This is a NEW status value, alongside memory_vector_store.py's existing
"active" | "dormant" | "archived" used by MemoryRecord.status. This module does
NOT modify memory_vector_store.py — MemoryRecord.status is a plain `str` field
with no enum/validation constraint (see that module, MemoryRecord dataclass,
`status: str = "active"  # "active" | "dormant" | "archived"`), so assigning
"quarantined" to it requires no schema change. Worker D owns wiring
`status="quarantined"` into the actual write path when it is built.

Verified, not assumed: "quarantined" records are never returned by
`search_memory` under any existing flag combination, with no change to
`search_memory` itself required. Confirmed by reading
`agent-memory/server.py::_search_memory_impl` directly —

    statuses = ["active"]
    if include_dormant:
        statuses.append("dormant")
    if include_archived:
        statuses.append("archived")

`statuses` is built from a hardcoded `["active"]` base plus two boolean
opt-in flags (`include_dormant`, `include_archived`) that are the ONLY caller-
controllable inputs to this list. There is no third flag, no free-form status
parameter, and no code path that appends anything other than the literal
strings "dormant"/"archived" to `statuses`. A record with `status="quarantined"`
therefore cannot be matched by the Qdrant `MatchAny(any=statuses)` filter
`QdrantMemoryIndex.search()` builds from this list under ANY combination of
`include_dormant`/`include_archived`, today or without a code change to add a
new parameter — exactly the "never retrievable by default, and not reachable
by any existing flag" property the quarantine lane requires.

Promotion out of quarantine (`status="quarantined"` -> `status="active"`) or
rejection (`status="quarantined"` -> `status="archived"`) is performed by
`promote_quarantined_write()` / `reject_quarantined_write()` below. Per
`memory_store.py`'s `write_reflection()` precedent (a write path that is
deliberately NOT exposed as an `@mcp.tool()` — only callable from trusted
internal code), these two functions are NOT MCP-agent-callable either. They
require a `ReviewerConfirmation` token — the same "raise the bar against the
zero-effort bypass, do not claim unforgeability" shape as `memory_store.py`'s
`IdentityVerification` — so a human-driven review script/pass, not a bare
agent-facing tool call, is the only sanctioned way to graduate or reject a
quarantined record.
"""

from __future__ import annotations

import datetime
import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple

# Mirrors prompt-gate-enforcer.py's 15-minute stale-marker fail-safe exactly —
# same rationale: if the confirmation step never completes for some other
# reason (the turn ended without one, the session was abandoned), the marker
# must not deadlock the session forever. Clearing it does not select an
# answer for the user — it only restores pre-gate behavior.
STALE_MARKER_SECONDS = 900

# Own marker filename prefix — deliberately distinct from H-P01's
# "h-p01-pending-<session_id>.json" so this gate's state never collides with
# or is cleared by H-P01's own enforcer/clear hook pair, and vice versa. Two
# independent gates, two independent marker namespaces, same directory.
MARKER_PREFIX = "mem-write-pending-"

_STATE_DIR_PARTS = (".claude", "hooks", ".state")


def _repo_root() -> Optional[Path]:
    """Best-effort `git rev-parse --show-toplevel`, exactly the resolution
    approach prompt-gate-enforcer.py / prompt-gate-clear.py / prompt-optimizer.py
    already use — so this module resolves the correct repo root whether it is
    invoked from the MCP server process (agent-memory/server.py, cwd could be
    anywhere the host launched it from) or from a test (cwd is typically the
    repo or a subdirectory of it). Returns None on any failure; callers decide
    how to handle that (WriteConfirmationGate raises, since a gate that can't
    resolve where to write its marker cannot make any safe claim either way)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    root = result.stdout.strip()
    return Path(root) if root else None


class RepoRootUnresolvedError(RuntimeError):
    """Raised when `git rev-parse --show-toplevel` cannot be resolved. A gate
    that cannot find its own marker directory must not silently pretend
    confirmation is unnecessary — fail loud rather than fail open."""


class WriteConfirmationGate:
    """Human-facing confirmation gate for high-consequence agent-memory writes.

    See this module's docstring for the full REFLECT-003 compliance statement
    and the honest scope/limitation of what "structurally enforced" means here.
    """

    def classify(
        self,
        memory_type: str,
        sacred: bool,
        would_collide_with_existing: bool,
    ) -> str:
        """Returns "high_consequence" or "routine".

        high_consequence if ANY of:
          - sacred is True
          - would_collide_with_existing is True (a judge verdict would
            archive/overwrite an existing record — Worker D wires this from
            Worker B's judge-output design; see threat-model §2.2 item 2 and
            §3.2 for why a collision is treated as high-consequence
            regardless of memory_type)
          - memory_type == "reflection" (the memory_reflection collection is
            the Investigator-Authored Write Path's own domain — see
            memory_store.py's module-level comment: "No MCP write tool exists
            or should ever be added for this memory type" — so any
            hypothetical write-tool path that could still reach it must be
            treated as maximally sensitive, not routine, even before Worker D
            decides whether to route reflection writes through this gate at
            all)

        Everything else is "routine" — eligible for the write-then-quarantine
        lane instead of blocking confirmation (threat-model §3.2).
        """
        if sacred or would_collide_with_existing or memory_type == "reflection":
            return "high_consequence"
        return "routine"

    def confirmation_marker_path(self, session_id: str) -> Path:
        """Path to this gate's own pending-confirmation marker for
        `session_id` — analogous to H-P01's
        `.claude/hooks/.state/h-p01-pending-<session_id>.json`, but under this
        gate's own filename prefix (see module-level `MARKER_PREFIX`), never
        colliding with or reusing H-P01's marker namespace.

        Raises RepoRootUnresolvedError if the repo root cannot be resolved —
        deliberately not a silent None/empty-path return, since a caller that
        can't determine where the marker lives must not proceed as though no
        marker exists.
        """
        root = _repo_root()
        if root is None:
            raise RepoRootUnresolvedError(
                "could not resolve repo root via `git rev-parse --show-toplevel` "
                "— refusing to guess a marker path"
            )
        return root.joinpath(*_STATE_DIR_PARTS, f"{MARKER_PREFIX}{session_id}.json")

    def request_confirmation(self, session_id: str, summary: str) -> None:
        """Writes a pending-confirmation marker for `session_id`, blocking
        every subsequent tool call in that session except AskUserQuestion
        once write-memory-gate-enforcer.py (PreToolUse) is wired in (see this
        module's docstring for the exact settings.json snippet and why it is
        NOT wired in by this build).

        Marker shape mirrors H-P01's own marker exactly (`{"pending": True,
        "ts": <ISO timestamp>}`), plus a `summary` field so a reviewing human
        (or a future audit pass) can see what write is pending confirmation
        without having to reconstruct it from the transcript. The `ts` field
        uses the same `datetime.datetime.now().isoformat()` shape H-P01's
        prompt-optimizer.py writes, so write-memory-gate-enforcer.py's
        15-minute stale-marker fail-safe logic (mirroring
        prompt-gate-enforcer.py's) can parse it identically.
        """
        marker_path = self.confirmation_marker_path(session_id)
        marker_path.parent.mkdir(parents=True, exist_ok=True)
        marker = {
            "pending": True,
            "ts": datetime.datetime.now().isoformat(),
            "summary": summary,
        }
        marker_path.write_text(json.dumps(marker), encoding="utf-8")

    def check_confirmation(self, session_id: str) -> Tuple[bool, str]:
        """Returns (allowed, reason).

        Mirrors H-P01's file-presence-means-still-pending contract exactly:
        marker present and not stale = not yet confirmed = not allowed. No
        marker (never requested, or already cleared by
        write-memory-gate-clear.py after a real AskUserQuestion call) =
        allowed. A stale marker (>15 minutes old, mirroring
        prompt-gate-enforcer.py's own fail-safe) is treated as "the
        confirmation step never completed for some other reason" — cleared,
        and treated as allowed, rather than deadlocking the session forever.
        Clearing a stale marker does not select an answer for the caller; it
        only restores pre-gate behavior, exactly as prompt-gate-enforcer.py's
        own comment states for H-P01.
        """
        marker_path = self.confirmation_marker_path(session_id)
        if not marker_path.is_file():
            return True, "no pending confirmation marker for this session — write may proceed"

        try:
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
            ts = datetime.datetime.fromisoformat(marker["ts"])
            now = datetime.datetime.now(ts.tzinfo) if ts.tzinfo else datetime.datetime.now()
            age_seconds = (now - ts).total_seconds()
            is_stale = age_seconds > STALE_MARKER_SECONDS
        except Exception:
            # Unparseable/corrupt marker — mirrors prompt-gate-enforcer.py's
            # own except-clause behavior: treat as stale rather than as
            # "confirmed" or as an unrecoverable error.
            is_stale = True

        if is_stale:
            try:
                marker_path.unlink()
            except OSError:
                pass
            return (
                True,
                "pending marker was stale (>15min, mirroring H-P01's fail-safe) — "
                "cleared; write may proceed",
            )

        return (
            False,
            "confirmation still pending for this session — write blocked until "
            "AskUserQuestion is answered (or the 15-minute stale-marker fail-safe fires)",
        )


# ---------------------------------------------------------------------------
# Quarantine lane — promotion / rejection (NOT MCP-agent-callable)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ReviewerConfirmation:
    """Opaque proof that a human reviewer confirmed a promote/reject decision
    for a specific quarantined record. Modeled directly on
    `memory_store.IdentityVerification` — same honest limitation applies:
    this is NOT a cryptographic guarantee. Python has no true encapsulation;
    a caller who reads this module's source could construct a
    `ReviewerConfirmation` instance directly without a real review having
    happened. What this class narrows, honestly:

    - closes the zero-effort bypass (calling `promote_quarantined_write(record,
      "yes")` with a bare string, or omitting the argument) — raises the bar
      to "requires deliberately fabricating this token"
    - binds the confirmation to a specific `record_id` and `decision`, so a
      confirmation obtained for one record/decision cannot be silently reused
      for a different one
    - is not itself the security boundary (per REFLECT-003 — no code-level
      check is), it is defense-in-depth plus a machine-checkable audit trail
      of who confirmed what and when
    """

    reviewer: str
    record_id: str
    decision: str  # "promote" | "reject"
    confirmed_at: float = field(default_factory=time.time)


class InvalidReviewerConfirmationError(ValueError):
    """Raised by promote_quarantined_write()/reject_quarantined_write() when
    `reviewer_confirmation` is missing, not a genuine ReviewerConfirmation
    instance, or does not match the record/decision being acted on."""


def _require_valid_confirmation(record, reviewer_confirmation, expected_decision: str) -> None:
    if not isinstance(reviewer_confirmation, ReviewerConfirmation):
        raise InvalidReviewerConfirmationError(
            f"{expected_decision}_quarantined_write() requires a genuine "
            "ReviewerConfirmation token — refusing to act on a forged, bare-string, "
            "or missing confirmation, regardless of caller."
        )

    if not reviewer_confirmation.reviewer:
        raise InvalidReviewerConfirmationError(
            "ReviewerConfirmation requires a non-empty reviewer name."
        )

    record_id = getattr(record, "id", None)
    if reviewer_confirmation.record_id != record_id:
        raise InvalidReviewerConfirmationError(
            f"ReviewerConfirmation was issued for record_id={reviewer_confirmation.record_id!r}, "
            f"not {record_id!r} — refusing to act under a mismatched confirmation."
        )

    if reviewer_confirmation.decision != expected_decision:
        raise InvalidReviewerConfirmationError(
            f"ReviewerConfirmation carries decision={reviewer_confirmation.decision!r}, "
            f"expected {expected_decision!r} for this call."
        )

    record_status = getattr(record, "status", None)
    if record_status != "quarantined":
        raise InvalidReviewerConfirmationError(
            f"{expected_decision}_quarantined_write() only operates on records with "
            f"status='quarantined' — this record has status={record_status!r}."
        )


def promote_quarantined_write(record, reviewer_confirmation: ReviewerConfirmation) -> bool:
    """Promotes a quarantined record to status="active" after human review.

    NOT MCP-agent-callable — mirrors memory_store.py's `write_reflection()`
    precedent: this function must only be imported and called from a trusted
    internal review script/pass, never exposed as an `@mcp.tool()` or any
    other agent-facing surface. Requires a genuine `ReviewerConfirmation`
    whose `record_id` matches `record.id` and whose `decision == "promote"`.

    Returns True on success. Raises InvalidReviewerConfirmationError on any
    forged/missing/mismatched confirmation, or if `record.status` is not
    already "quarantined".
    """
    _require_valid_confirmation(record, reviewer_confirmation, expected_decision="promote")
    record.status = "active"
    return True


def reject_quarantined_write(record, reviewer_confirmation: ReviewerConfirmation) -> bool:
    """Rejects a quarantined record, moving it to status="archived" (never
    deleted outright — consistent with this workspace's existing archive-not-
    delete discipline elsewhere in the memory system) after human review.

    NOT MCP-agent-callable — same precedent and requirement as
    `promote_quarantined_write()` above, with `decision == "reject"`.

    Returns True on success. Raises InvalidReviewerConfirmationError on any
    forged/missing/mismatched confirmation, or if `record.status` is not
    already "quarantined".
    """
    _require_valid_confirmation(record, reviewer_confirmation, expected_decision="reject")
    record.status = "archived"
    return True


# ---------------------------------------------------------------------------
# settings.json wiring snippet (NOT applied by this build — see module
# docstring "Hook enforcement boundary" and the build brief's scope note:
# modifying the harness's own live hook configuration is out of scope for
# this worktree's automated build. A human, or the orchestrator with explicit
# review, applies this deliberately by merging it into .claude/settings.json).
#
# Same event/matcher shape as the existing H-P01 pair
# (prompt-gate-enforcer.py under PreToolUse matcher "*", prompt-gate-clear.py
# under PostToolUse matcher "AskUserQuestion") — see .claude/settings.json's
# existing "PreToolUse"/"PostToolUse" arrays for where these entries would be
# added (as new hook entries alongside the existing ones, not replacing them):
#
# PreToolUse (add to the existing matcher: "*" group's "hooks" array,
# alongside prompt-gate-enforcer.py):
#     {
#       "type": "command",
#       "command": "uv",
#       "args": ["run", "${CLAUDE_PROJECT_DIR}/.claude/hooks/write-memory-gate-enforcer.py"]
#     }
#
# PostToolUse (add a new matcher group, mirroring the existing
# matcher: "AskUserQuestion" group that clears H-P01's own marker):
#     {
#       "matcher": "AskUserQuestion",
#       "hooks": [
#         {
#           "type": "command",
#           "command": "uv",
#           "args": ["run", "${CLAUDE_PROJECT_DIR}/.claude/hooks/write-memory-gate-clear.py"]
#         }
#       ]
#     }
#
# (This can be merged into the SAME matcher: "AskUserQuestion" PostToolUse
# group that already exists for prompt-gate-clear.py, by adding this hook
# entry to that group's "hooks" array, rather than creating a second group
# with the same matcher — either shape is valid; a single merged group is
# slightly tidier.)
# ---------------------------------------------------------------------------
