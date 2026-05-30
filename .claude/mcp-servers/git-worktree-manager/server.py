#!/usr/bin/env python3
"""
Git Worktree Manager MCP Server

Git worktree management for multi-agent parallel work.
Implements the git worktree isolation pattern from CC-00.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Git Worktree Manager")

# Workspace root from environment
WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", "."))


class GitWorktreeManager:
    """Manage git worktrees for multi-agent parallel work"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.worktrees_dir = workspace_root.parent / "worktrees"
    
    def _run_git_command(self, args: List[str], cwd: Optional[Path] = None) -> Dict[str, Any]:
        """Run a git command and return result"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=cwd or self.workspace_root,
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "success": True,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": e.stderr.strip() or e.stdout.strip(),
                "returncode": e.returncode,
            }
    
    def create_worktree(self, agent_name: str, task: str, base_branch: str = "master") -> Dict[str, Any]:
        """Create isolated worktree for agent"""
        
        # Create worktrees directory if it doesn't exist
        self.worktrees_dir.mkdir(exist_ok=True)
        
        # Generate branch name: agent/<agent-name>/<task>
        branch_name = f"agent/{agent_name}/{task}"
        
        # Generate worktree path
        worktree_path = self.worktrees_dir / f"agent-{agent_name}"
        
        # Check if worktree already exists
        if worktree_path.exists():
            return {
                "success": False,
                "error": f"Worktree already exists: {worktree_path}",
                "worktree_path": str(worktree_path),
            }
        
        # Create worktree
        result = self._run_git_command([
            "worktree", "add",
            str(worktree_path),
            "-b", branch_name,
            base_branch
        ])
        
        if not result["success"]:
            return {
                "success": False,
                "error": f"Failed to create worktree: {result.get('error')}",
            }
        
        return {
            "success": True,
            "agent_name": agent_name,
            "task": task,
            "branch_name": branch_name,
            "worktree_path": str(worktree_path),
            "base_branch": base_branch,
            "message": f"Created worktree for {agent_name} at {worktree_path}",
        }
    
    def remove_worktree(self, agent_name: str, force: bool = False) -> Dict[str, Any]:
        """Remove agent's worktree"""
        
        worktree_path = self.worktrees_dir / f"agent-{agent_name}"
        
        if not worktree_path.exists():
            return {
                "success": False,
                "error": f"Worktree not found: {worktree_path}",
            }
        
        # Remove worktree
        args = ["worktree", "remove", str(worktree_path)]
        if force:
            args.append("--force")
        
        result = self._run_git_command(args)
        
        if not result["success"]:
            return {
                "success": False,
                "error": f"Failed to remove worktree: {result.get('error')}",
            }
        
        # Prune worktree references
        self._run_git_command(["worktree", "prune"])
        
        return {
            "success": True,
            "agent_name": agent_name,
            "worktree_path": str(worktree_path),
            "message": f"Removed worktree for {agent_name}",
        }
    
    def list_worktrees(self) -> Dict[str, Any]:
        """List all worktrees"""
        
        result = self._run_git_command(["worktree", "list", "--porcelain"])
        
        if not result["success"]:
            return {
                "success": False,
                "error": f"Failed to list worktrees: {result.get('error')}",
            }
        
        # Parse worktree list
        worktrees = []
        current_worktree = {}
        
        for line in result["stdout"].split("\n"):
            if not line:
                if current_worktree:
                    worktrees.append(current_worktree)
                    current_worktree = {}
                continue
            
            if line.startswith("worktree "):
                current_worktree["path"] = line.split(" ", 1)[1]
            elif line.startswith("branch "):
                current_worktree["branch"] = line.split(" ", 1)[1]
            elif line.startswith("HEAD "):
                current_worktree["head"] = line.split(" ", 1)[1]
        
        if current_worktree:
            worktrees.append(current_worktree)
        
        return {
            "success": True,
            "count": len(worktrees),
            "worktrees": worktrees,
        }
    
    def merge_branch(
        self, 
        agent_name: str, 
        target_branch: str = "master",
        no_ff: bool = True
    ) -> Dict[str, Any]:
        """Merge agent's branch back to target branch"""
        
        # Get agent's branch name
        worktree_path = self.worktrees_dir / f"agent-{agent_name}"
        
        if not worktree_path.exists():
            return {
                "success": False,
                "error": f"Worktree not found: {worktree_path}",
            }
        
        # Get branch name from worktree
        result = self._run_git_command(
            ["rev-parse", "--abbrev-ref", "HEAD"],
            cwd=worktree_path
        )
        
        if not result["success"]:
            return {
                "success": False,
                "error": f"Failed to get branch name: {result.get('error')}",
            }
        
        branch_name = result["stdout"]
        
        # Switch to target branch in main workspace
        result = self._run_git_command(["checkout", target_branch])
        
        if not result["success"]:
            return {
                "success": False,
                "error": f"Failed to checkout {target_branch}: {result.get('error')}",
            }
        
        # Merge agent's branch
        merge_args = ["merge", branch_name]
        if no_ff:
            merge_args.append("--no-ff")
        
        result = self._run_git_command(merge_args)
        
        if not result["success"]:
            return {
                "success": False,
                "error": f"Merge failed: {result.get('error')}",
                "branch_name": branch_name,
                "target_branch": target_branch,
            }
        
        return {
            "success": True,
            "agent_name": agent_name,
            "branch_name": branch_name,
            "target_branch": target_branch,
            "message": f"Merged {branch_name} into {target_branch}",
        }


# Initialize worktree manager
worktree_manager = GitWorktreeManager(WORKSPACE_ROOT)


@mcp.tool()
def create_worktree(
    agent_name: str, 
    task: str, 
    base_branch: str = "master"
) -> str:
    """
    Create isolated git worktree for agent.
    
    Args:
        agent_name: Name of the agent (e.g., "backend", "frontend")
        task: Task description (e.g., "dark-mode-api")
        base_branch: Base branch to branch from (default: "master")
    
    Returns:
        JSON string with worktree creation results
    """
    result = worktree_manager.create_worktree(agent_name, task, base_branch)
    return json.dumps(result, indent=2)


@mcp.tool()
def remove_worktree(agent_name: str, force: bool = False) -> str:
    """
    Remove agent's worktree.
    
    Args:
        agent_name: Name of the agent
        force: Force removal even if worktree has uncommitted changes
    
    Returns:
        JSON string with removal results
    """
    result = worktree_manager.remove_worktree(agent_name, force)
    return json.dumps(result, indent=2)


@mcp.tool()
def list_worktrees() -> str:
    """
    List all git worktrees.
    
    Returns:
        JSON string with list of worktrees
    """
    result = worktree_manager.list_worktrees()
    return json.dumps(result, indent=2)


@mcp.tool()
def merge_branch(
    agent_name: str, 
    target_branch: str = "master",
    no_ff: bool = True
) -> str:
    """
    Merge agent's branch back to target branch.
    
    Args:
        agent_name: Name of the agent
        target_branch: Target branch to merge into (default: "master")
        no_ff: Use --no-ff flag for merge (default: True)
    
    Returns:
        JSON string with merge results
    """
    result = worktree_manager.merge_branch(agent_name, target_branch, no_ff)
    return json.dumps(result, indent=2)


@mcp.tool()
def get_worktree_status(agent_name: str) -> str:
    """
    Get status of agent's worktree.
    
    Args:
        agent_name: Name of the agent
    
    Returns:
        JSON string with worktree status
    """
    worktree_path = worktree_manager.worktrees_dir / f"agent-{agent_name}"
    
    if not worktree_path.exists():
        return json.dumps({
            "success": False,
            "error": f"Worktree not found: {worktree_path}",
        }, indent=2)
    
    # Get git status
    result = worktree_manager._run_git_command(
        ["status", "--short"],
        cwd=worktree_path
    )
    
    if not result["success"]:
        return json.dumps({
            "success": False,
            "error": f"Failed to get status: {result.get('error')}",
        }, indent=2)
    
    # Get branch name
    branch_result = worktree_manager._run_git_command(
        ["rev-parse", "--abbrev-ref", "HEAD"],
        cwd=worktree_path
    )
    
    return json.dumps({
        "success": True,
        "agent_name": agent_name,
        "worktree_path": str(worktree_path),
        "branch": branch_result.get("stdout", "unknown"),
        "status": result["stdout"],
        "has_changes": bool(result["stdout"]),
    }, indent=2)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
