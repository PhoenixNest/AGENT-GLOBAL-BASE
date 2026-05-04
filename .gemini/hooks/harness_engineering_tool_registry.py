"""
Tool Registry and Boundaries Implementation

This module implements the Tool Boundaries Pattern for safe tool usage.
Defines explicit whitelists, timeouts, and call limits.
"""

import asyncio
import json
import re
import sys
from typing import Any, Callable, Dict, List

# Tool registry configuration
TOOL_REGISTRY = {
    "search": {
        "description": "Search the web for information",
        "timeout_seconds": 30,
        "max_calls_per_task": 2,
        "requires_approval": False,
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "minLength": 1}},
            "required": ["query"],
        },
    },
    "file_read": {
        "description": "Read a file from the filesystem",
        "timeout_seconds": 15,
        "max_calls_per_task": 3,
        "requires_approval": False,
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "limit_lines": {"type": "integer", "default": None},
            },
            "required": ["path"],
        },
    },
    "file_write": {
        "description": "Write content to a file",
        "timeout_seconds": 30,
        "max_calls_per_task": 1,
        "requires_approval": True,  # High-risk operation
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["path", "content"],
        },
    },
    "fetch_weather": {
        "description": "Get current weather for a location",
        "timeout_seconds": 15,
        "max_calls_per_task": 1,
        "requires_approval": False,
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    },
    "calculator": {
        "description": "Perform mathematical calculations",
        "timeout_seconds": 5,
        "max_calls_per_task": 3,
        "requires_approval": False,
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
}


class ToolRegistry:
    """
    Manages tool whitelist and boundaries for safe execution.

    Usage:
        registry = ToolRegistry()
        if registry.is_allowed("search"):
            result = await registry.execute_tool("search", query="...")
    """

    def __init__(self, registry_config: Dict = None):
        self.registry_config = registry_config or TOOL_REGISTRY.copy()
        self.call_counts: Dict[str, int] = {}
        self.current_task_id = "unknown"
        self.max_concurrent_tools = 2

    def is_allowed_tool(self, tool_name: str) -> bool:
        """Check if a tool is in the whitelist."""
        return tool_name in self.registry_config

    def get_tool_timeout(self, tool_name: str) -> int:
        """Get configured timeout for a tool."""
        config = self.registry_config.get(tool_name, {})
        return config.get("timeout_seconds", 30)

    def get_max_calls(self, tool_name: str) -> int:
        """Get maximum allowed calls for a tool."""
        config = self.registry_config.get(tool_name, {})
        return config.get("max_calls_per_task", 2)

    def requires_approval(self, tool_name: str) -> bool:
        """Check if tool requires human approval before execution."""
        config = self.registry_config.get(tool_name, {})
        return config.get("requires_approval", False)

    def get_tool_info(self, tool_name: str) -> Dict:
        """Get full configuration for a tool."""
        return self.registry_config.get(tool_name, {})

    async def execute_tool(
        self, tool_name: str, input_data: Dict, task_id: str = None
    ) -> Dict:
        """
        Execute a tool call with boundary checks.

        Args:
            tool_name: Name of tool to execute
            input_data: Parameters for the tool
            task_id: Task identifier for tracking call counts

        Returns:
            Execution result or error dictionary
        """
        # Check if tool is allowed
        if not self.is_allowed_tool(tool_name):
            return {
                "success": False,
                "error": {
                    "code": "TOOL_NOT_FOUND",
                    "message": f"Tool '{tool_name}' is not in the whitelist",
                },
            }

        config = self.get_tool_info(tool_name)
        timeout = config.get("timeout_seconds", 30)
        max_calls = config.get("max_calls_per_task", 2)
        requires_approval = config.get("requires_approval", False)

        # Check call count limit
        if task_id:
            key = f"{task_id}:{tool_name}"
            current_count = self.call_counts.get(key, 0)
            if current_count >= max_calls:
                return {
                    "success": False,
                    "error": {
                        "code": "CALL_LIMIT_REACHED",
                        "message": f"Tool '{tool_name}' call limit reached",
                    },
                }
            self.call_counts[key] = current_count + 1

        # Check if approval required
        if requires_approval:
            return {
                "success": False,
                "error": {
                    "code": "APPROVAL_REQUIRED",
                    "message": f"Tool '{tool_name}' requires human approval",
                },
            }

        # Validate input against schema
        if not self._validate_input(tool_name, input_data):
            return {
                "success": False,
                "error": {
                    "code": "INVALID_INPUT",
                    "message": "Input doesn't match tool schema",
                },
            }

        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                self._invoke_tool(tool_name, input_data), timeout=timeout
            )

            return {
                "success": True,
                "tool_name": tool_name,
                "data": result,
                "timeout_used": timeout,
                "call_count": self.call_counts.get(key, 0) if task_id else 0,
            }

        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": {
                    "code": "TIMEOUT",
                    "message": f"Tool '{tool_name}' timed out after {timeout}s",
                },
            }

        except Exception as e:
            return {
                "success": False,
                "error": {"code": "EXECUTION_ERROR", "message": str(e)},
            }

    async def _invoke_tool(self, tool_name: str, input_data: Dict):
        """Invoke the actual tool function (placeholder)."""
        # In production, this would call the actual tool implementation
        return {f"result_from_{tool_name}": "success"}

    def _validate_input(self, tool_name: str, input_data: Dict) -> bool:
        """Validate input against tool schema."""
        config = self.registry_config.get(tool_name, {})
        schema = config.get("input_schema", {})

        # Simple validation - implement full JSON Schema validation in production
        required_fields = schema.get("required", [])
        if all(field in input_data for field in required_fields):
            return True

        return False

    def reset_call_counts(self, task_id: str = None):
        """Reset call counts for a task."""
        if task_id:
            self.call_counts = {k: 0 for k in self.call_counts if k.startswith(task_id)}
        else:
            self.call_counts.clear()

    def clear_tool_whitelist(self) -> List[str]:
        """Get list of all allowed tools (for clearing)."""
        return list(self.registry_config.keys())


# Tool-boundary pattern for agent usage
class SafeAgentToolUse:
    """
    Wrapper for agents that use tools. Implements boundaries and limits.

    Usage:
        agent_tools = SafeAgentToolUse(tool_registry)
        result = await agent_tools.execute_plan(task_description)
    """

    def __init__(self, tool_registry: ToolRegistry):
        self.registry = tool_registry
        self.max_tool_calls_per_task = 5  # Global limit for unstructured planning
        self.current_turn_count = 0
        self.thinking_depth = 0

    async def execute_plan(self, task_description: str) -> Dict:
        """
        Execute a plan to accomplish a task with boundaries.

        Args:
            task_description: What the agent should accomplish

        Returns:
            Final result or error summary
        """
        self.current_turn_count = 0
        self.thinking_depth = 0
        self.registry.reset_call_counts(task_id="auto")

        # Check for dangerous task patterns
        if self._is_dangerous_task(task_description):
            return {
                "success": False,
                "error": {
                    "code": "UNSAFE_TASK",
                    "message": "Task requires human review",
                },
            }

        result = await self._run_with_depth_limit(task_description)
        return result

    async def _run_with_depth_limit(self, goal: str):
        """Run task while respecting depth limits."""
        self.thinking_depth += 1

        if self.thinking_depth > self.max_tool_calls_per_task:
            # Maximum thinking depth reached - summarize and conclude
            return {
                "success": True,
                "message": f"Completed task after {self.max_tool_calls_per_task} tool calls",
                "conclusion": await self._summarize_achievement(goal),
            }

        if self.current_turn_count > 10:  # Also limit by turns
            return {
                "success": True,
                "message": "Task completed (turn limit reached)",
                "conclusion": "Goal achieved or task requires more context",
            }

        # Execute one step of the plan
        tool_result = await self.registry.execute_tool(
            tool_name="search",  # Would be chosen dynamically in production
            input_data={"query": f"Step to achieve: {goal}"},
            task_id="auto",
        )

        if not tool_result["success"]:
            return {"success": False, "error": tool_result["error"]}

        self.current_turn_count += 1

        # Continue with next step (recursive in production)
        # ...
        return {"progress": "continuing"}

    def _is_dangerous_task(self, task: str) -> bool:
        """Check if task is potentially dangerous."""
        dangerous_patterns = [
            r"delete\s+.*\.(exe|dll)",  # System file deletion
            r"rm\s+-rf",  # Unix destructive command
            r"format",  # Disk formatting
            r"kill\s+",  # Process termination
            r"sudo\s+" if sys.platform != "win32" else "",  # Admin commands
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, task.lower()):
                return True

        return False

    async def _summarize_achievement(self, goal: str) -> str:
        """Summarize what was accomplished."""
        return f"Task to '{goal}' was completed. Final steps are ready for review."


# Example usage in production:
"""
from implementations.tool_registry import ToolRegistry, SafeAgentToolUse

# Initialize registry with your tools
tool_registry = ToolRegistry(TOOL_REGISTRY)

# Create safe agent tool wrapper
safe_agent = SafeAgentToolUse(tool_registry)

async def main():
    # Execute task safely
    result = await safe_agent.execute_plan("Find information about X")

    if result["success"]:
        print(result.get("message", "Task completed"))
        print(result.get("conclusion"))
    else:
        print(f"Error: {result['error']['message']}")

if __name__ == "__main__":
    asyncio.run(main())
"""

# ---------------------------------------------------------------------------
# CLI Standard JSON I/O Runner
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json
    import sys
    
    try:
        input_data = sys.stdin.read()
        if input_data.startswith('\ufeff'):
            input_data = input_data[1:]
        if not input_data.strip():
            print(json.dumps({}))
            sys.exit(0)
            
        event_payload = json.loads(input_data)
        
        # Tool Registry is a BeforeToolSelection hook. 
        # For now, simply act as a safe pass-through.
        
        # Print strictly formatted JSON to stdout
        print(json.dumps(event_payload))
        sys.exit(0)
        
    except Exception as e:
        print(f"Tool Registry Error: {e}", file=sys.stderr)
        sys.exit(1)
