"""Human-facing confirmation gate and quarantine lane for write-capable agent-memory writes."""

from __future__ import annotations

import datetime
import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple

# No code-level check here is unforgeable (REFLECT-003: an agent has the same
# import access a human developer does). The real boundary is a live human
# answering AskUserQuestion; this gate only makes skipping that wait awkward
# for a normal interactive Claude Code session — it does not bind other MCP
# clients calling this server directly.

STALE_MARKER_SECONDS = 900
MARKER_PREFIX = "mem-write-pending-"
_STATE_DIR_PARTS = (".claude", "hooks", ".state")


def _repo_root() -> Optional[Path]:
    """`git rev-parse --show-toplevel`, or None on failure."""
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
    """Raised when the repo root cannot be resolved."""


class WriteConfirmationGate:
    """Human-facing confirmation gate for high-consequence agent-memory writes."""

    def classify(
        self,
        memory_type: str,
        sacred: bool,
        would_collide_with_existing: bool,
    ) -> str:
        """Returns "high_consequence" (sacred, would archive/overwrite an
        existing record, or memory_type == "reflection") or "routine"
        (everything else — eligible for write-then-quarantine)."""
        if sacred or would_collide_with_existing or memory_type == "reflection":
            return "high_consequence"
        return "routine"

    def confirmation_marker_path(self, session_id: str) -> Path:
        """Path to this gate's pending-confirmation marker for `session_id`.

        Raises RepoRootUnresolvedError if the repo root cannot be resolved.
        """
        root = _repo_root()
        if root is None:
            raise RepoRootUnresolvedError(
                "could not resolve repo root via `git rev-parse --show-toplevel` "
                "— refusing to guess a marker path"
            )
        return root.joinpath(*_STATE_DIR_PARTS, f"{MARKER_PREFIX}{session_id}.json")

    def request_confirmation(self, session_id: str, summary: str) -> None:
        """Writes a pending-confirmation marker for `session_id`."""
        marker_path = self.confirmation_marker_path(session_id)
        marker_path.parent.mkdir(parents=True, exist_ok=True)
        marker = {
            "pending": True,
            "ts": datetime.datetime.now().isoformat(),
            "summary": summary,
        }
        marker_path.write_text(json.dumps(marker), encoding="utf-8")

    def check_confirmation(self, session_id: str) -> Tuple[bool, str]:
        """Returns (allowed, reason). No marker, or a stale marker
        (>15 min), means allowed; a fresh marker means blocked."""
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
            is_stale = True

        if is_stale:
            try:
                marker_path.unlink()
            except OSError:
                pass
            return (
                True,
                "pending marker was stale (>15min) — cleared; write may proceed",
            )

        return (
            False,
            "confirmation still pending for this session — write blocked until "
            "AskUserQuestion is answered (or the 15-minute stale-marker fail-safe fires)",
        )


# Quarantine lane: routine writes commit immediately with status="quarantined"
# (a plain str value, no schema change to MemoryRecord). Never returned by
# search_memory, since its status-filter list only ever contains "active" plus
# opt-in "dormant"/"archived" — verified against agent-memory/server.py's
# _search_memory_impl. Promotion/rejection below are NOT MCP-agent-callable.


@dataclass(frozen=True)
class ReviewerConfirmation:
    """Proof that a human reviewer confirmed a promote/reject decision for a
    specific quarantined record. Not a cryptographic guarantee — narrows the
    zero-effort bypass and binds the confirmation to one record_id/decision."""

    reviewer: str
    record_id: str
    decision: str  # "promote" | "reject"
    confirmed_at: float = field(default_factory=time.time)


class InvalidReviewerConfirmationError(ValueError):
    """Raised when `reviewer_confirmation` is missing, forged, or mismatched."""


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
    Not MCP-agent-callable. Raises InvalidReviewerConfirmationError on any
    forged/missing/mismatched confirmation."""
    _require_valid_confirmation(record, reviewer_confirmation, expected_decision="promote")
    record.status = "active"
    return True


def reject_quarantined_write(record, reviewer_confirmation: ReviewerConfirmation) -> bool:
    """Rejects a quarantined record to status="archived" (never deleted)
    after human review. Not MCP-agent-callable."""
    _require_valid_confirmation(record, reviewer_confirmation, expected_decision="reject")
    record.status = "archived"
    return True
