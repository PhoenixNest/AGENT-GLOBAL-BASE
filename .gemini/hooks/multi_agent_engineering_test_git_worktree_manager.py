"""
Tests for GitWorktreeManager — Filesystem Isolation for Agent Swarms

Note: These tests require a real Git repository. They create temporary
repos and worktrees for testing purposes.
"""

import os
import pytest
import subprocess
import tempfile
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.git_worktree_manager import GitWorktreeManager, WorktreeInfo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary Git repository for testing."""
    repo = tmp_path / "test-repo"
    repo.mkdir()

    subprocess.run(["git", "init"], cwd=repo, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test Agent"],
        cwd=repo,
        capture_output=True,
        check=True,
    )

    # Create initial commit (required for worktree operations)
    readme = repo / "README.md"
    readme.write_text("# Test Repo")
    subprocess.run(["git", "add", "."], cwd=repo, capture_output=True, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=repo,
        capture_output=True,
        check=True,
    )

    return repo


@pytest.fixture
def manager(git_repo):
    """Create a GitWorktreeManager instance for the test repo."""
    return GitWorktreeManager(repo_path=git_repo)


# ---------------------------------------------------------------------------
# Initialization Tests
# ---------------------------------------------------------------------------


class TestInitialization:
    def test_valid_repo(self, git_repo):
        manager = GitWorktreeManager(repo_path=git_repo)
        assert manager.repo_path == git_repo

    def test_invalid_repo(self, tmp_path):
        with pytest.raises(ValueError, match="Not a git repository"):
            GitWorktreeManager(repo_path=tmp_path / "not-a-repo")


# ---------------------------------------------------------------------------
# Worktree Lifecycle Tests
# ---------------------------------------------------------------------------


class TestWorktreeLifecycle:
    def test_create_worktree(self, manager, git_repo):
        wt = manager.create_worktree("backend", "dark-mode-api")

        assert wt.agent_name == "backend"
        assert wt.task_id == "dark-mode-api"
        assert wt.branch == "agent/backend/dark-mode-api"
        assert wt.is_active is True
        assert wt.path.exists()

    def test_list_worktrees(self, manager):
        manager.create_worktree("backend", "task-1")
        manager.create_worktree("frontend", "task-2")

        worktrees = manager.list_worktrees()
        assert len(worktrees) == 2

    def test_remove_worktree(self, manager):
        wt = manager.create_worktree("backend", "task-1")
        manager.remove_worktree(wt)

        assert wt.is_active is False
        assert len(manager.list_worktrees()) == 0

    def test_cleanup_all(self, manager):
        manager.create_worktree("backend", "task-1")
        manager.create_worktree("frontend", "task-2")
        manager.cleanup_all()

        assert len(manager.list_worktrees()) == 0


# ---------------------------------------------------------------------------
# Commit and Merge Tests
# ---------------------------------------------------------------------------


class TestCommitAndMerge:
    def test_commit_in_worktree(self, manager):
        wt = manager.create_worktree("backend", "task-1")

        # Create a file in the worktree
        test_file = wt.path / "new_feature.py"
        test_file.write_text("def hello(): return 'world'")

        # Commit
        manager.commit(wt, "Add hello function")

        # Verify commit exists on the branch
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=wt.path,
            capture_output=True,
            text=True,
        )
        assert "hello function" in result.stdout


# ---------------------------------------------------------------------------
# WorktreeInfo Tests
# ---------------------------------------------------------------------------


class TestWorktreeInfo:
    def test_branch_full(self):
        wt = WorktreeInfo(
            path=Path("/tmp/test"),
            branch="agent/backend/task-1",
            agent_name="backend",
            task_id="task-1",
        )
        assert wt.branch_full == "agent/backend/task-1"
