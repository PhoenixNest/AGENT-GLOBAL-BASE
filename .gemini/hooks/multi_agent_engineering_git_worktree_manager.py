"""
Git Worktree Manager — Filesystem Isolation for Agent Swarms

Provides programmatic lifecycle management for Git worktrees used
as isolated execution environments for multi-agent development.

Version: 1.0
Last Updated: 2026-04-29
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class WorktreeInfo:
    """Represents a provisioned Git worktree."""

    path: Path
    branch: str
    agent_name: str
    task_id: str
    is_active: bool = True

    @property
    def branch_full(self) -> str:
        return f"agent/{self.agent_name}/{self.task_id}"


class GitWorktreeManager:
    """
    Manages Git worktree lifecycle for multi-agent swarms.

    Each agent gets its own worktree (filesystem clone) with a dedicated
    branch. This provides complete filesystem isolation — agents cannot
    see each other's uncommitted changes.

    Usage:
        manager = GitWorktreeManager(repo_path=Path("/my/repo"))
        wt = manager.create_worktree("backend", "dark-mode-api")
        # ... agent works in wt.path ...
        manager.commit(
            wt,
            message="add dark mode API endpoint",
            details=[
                "add POST /api/settings/theme accepting { mode: light | dark }",
                "validate unknown values and return HTTP 400 with descriptive error",
                "register endpoint in the application router",
                "add unit test stubs for validation and happy-path coverage",
            ],
        )
        manager.merge(wt, target_branch="main")
        manager.remove_worktree(wt)
    """

    def __init__(self, repo_path: Path, worktree_base: Optional[Path] = None):
        self.repo_path = Path(repo_path)
        self.worktree_base = worktree_base or self.repo_path.parent
        self._worktrees: dict[str, WorktreeInfo] = {}

        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Not a git repository: {self.repo_path}")

    def create_worktree(
        self,
        agent_name: str,
        task_id: str,
        base_branch: str = "HEAD",
    ) -> WorktreeInfo:
        """Create a new worktree with a dedicated branch for an agent."""
        branch = f"agent/{agent_name}/{task_id}"
        wt_path = self.worktree_base / f"agent-{agent_name}"

        self._run_git(["worktree", "add", str(wt_path), "-b", branch, base_branch])

        info = WorktreeInfo(
            path=wt_path,
            branch=branch,
            agent_name=agent_name,
            task_id=task_id,
        )
        self._worktrees[branch] = info
        logger.info("Created worktree: %s → %s", branch, wt_path)
        return info

    def commit(
        self,
        worktree: WorktreeInfo,
        message: str,
        details: Optional[List[str]] = None,
        add_all: bool = True,
    ) -> str:
        """Commit changes in the given worktree.

        Args:
            worktree: The worktree to commit in.
            message: Brief subject line describing the change in imperative mood
                     (e.g. "add dark mode API endpoint"). Prefixed automatically
                     with ``agent/<name>: ``. Keep to ≤72 characters total.
            details: Hyphenated bullet points for the commit body. Each item
                     becomes a ``- `` prefixed line. Providing at least 2–4
                     items describing *what* changed and *why* is required;
                     omitting the body is a P2 audit-trail defect.
            add_all: Stage all tracked and untracked changes before committing.
        """
        subject = f"agent/{worktree.agent_name}: {message}"

        if details:
            body = "\n".join(f"- {item}" for item in details)
            full_message = f"{subject}\n\n{body}"
        else:
            full_message = subject

        if add_all:
            self._run_git(["add", "-A"], cwd=worktree.path)

        result = self._run_git(
            ["commit", "-m", full_message],
            cwd=worktree.path,
        )
        return result

    def merge(
        self,
        worktree: WorktreeInfo,
        target_branch: str = "main",
    ) -> str:
        """Merge the worktree's branch into the target branch."""
        self._run_git(["checkout", target_branch])
        result = self._run_git(
            [
                "merge",
                worktree.branch,
                "--no-ff",
                "-m",
                f"Merge {worktree.branch}",
            ]
        )
        return result

    def remove_worktree(self, worktree: WorktreeInfo) -> None:
        """Remove a worktree and optionally delete its branch."""
        self._run_git(["worktree", "remove", str(worktree.path), "--force"])
        worktree.is_active = False
        self._worktrees.pop(worktree.branch, None)
        logger.info("Removed worktree: %s", worktree.branch)

    def list_worktrees(self) -> list[WorktreeInfo]:
        """Return all active worktrees managed by this instance."""
        return [wt for wt in self._worktrees.values() if wt.is_active]

    def prune(self) -> None:
        """Remove stale worktree entries from Git's tracking."""
        self._run_git(["worktree", "prune"])

    def cleanup_all(self) -> None:
        """Remove all managed worktrees and prune."""
        for wt in list(self._worktrees.values()):
            try:
                self.remove_worktree(wt)
            except subprocess.CalledProcessError:
                logger.warning("Failed to remove worktree: %s", wt.branch)
        self.prune()

    # -- Internal ----------------------------------------------------------

    def _run_git(
        self,
        args: list[str],
        cwd: Optional[Path] = None,
    ) -> str:
        """Execute a git command and return stdout."""
        cmd = ["git"] + args
        working_dir = cwd or self.repo_path

        result = subprocess.run(
            cmd,
            cwd=working_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
