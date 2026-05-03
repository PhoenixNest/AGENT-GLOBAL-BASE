"""
Context Budget Monitor Pattern Implementation

This module provides context monitoring and pruning utilities to prevent
token budget overflow in long-running conversations.
"""

import sys
from typing import List, Dict, Any

# Simplified token estimation (use proper model in production)
TOKENS_PER_WORD = 1.3
TOKENS_PER_CHAR = 0.1
SYSTEM_INSTRUCTIONS_TOKENS = 500


class ContextMonitor:
    """
    Monitors and manages conversation context budget.

    Usage:
        monitor = ContextMonitor(max_tokens=128000)
        if monitor.check_budget(messages):
            # Proceed normally
        else:
            messages = monitor.prune_conversation()
    """

    def __init__(
        self, max_tokens: int = 128000, warn_at: float = 0.75, prune_at: float = 0.80
    ):
        self.max_tokens = max_tokens
        self.warn_threshold = max_tokens * warn_at
        self.prune_threshold = max_tokens * prune_at
        self.history: List[Dict[str, Any]] = []
        self.token_counts_per_turn: Dict[int, int] = {}

    def add_message(self, role: str, content: str):
        """Record a message and estimate its token count."""
        tokens = self._estimate_tokens(content)
        turn_count = len(self.history) + 1
        self.history.append({"role": role, "content": content})
        self.token_counts_per_turn[turn_count] = tokens

    def check_budget(self, messages: List[Dict[str, Any]]) -> bool:
        """
        Check if messages are within budget.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys

        Returns:
            True if within budget, False if over
        """
        total_tokens = sum(self.token_counts_per_turn.values())

        ratio = total_tokens / self.max_tokens

        if ratio > 1.0:
            print(
                f"ERROR: Context overflow! Usage: {total_tokens}/{self.max_tokens} tokens",
                file=sys.stderr,
            )
            return False

        elif total_tokens > self.prune_threshold:
            print(
                f"WARNING: At prune threshold ({ratio*100:.0f}% of budget)",
                file=sys.stderr,
            )
            # Trigger pruning
            self.prune_conversation()
            return True

        elif total_tokens > self.warn_threshold:
            print(
                f"INFO: Context approaching budget ({ratio*100:.0f}% of budget)",
                file=sys.stderr,
            )
            return True  # Continue normally but log warning

        return True

    def prune_conversation(
        self, keep_recent_turns: int = 3, summarize_old: bool = True
    ):
        """
        Prune conversation history while keeping key context.

        Args:
            keep_recent_turns: Number of most recent turns to preserve
            summarize_old: Whether to replace old turns with summary

        Returns:
            Pruned list of messages
        """
        if len(self.history) <= keep_recent_turns:
            print("INFO: Not enough history to prune", file=sys.stderr)
            return self.history[:keep_recent_turns]

        # Keep recent turns
        recent_history = self.history[-keep_recent_turns:]

        # Summarize older turns if enabled
        if summarize_old:
            old_turns = self.history[:-keep_recent_turns]
            summary = self._create_summary(old_turns)

            # Insert summary after system/initial context, before recent turns
            return [summary] + recent_history

        # Otherwise just keep most recent N turns
        return self.history[-keep_recent_turns:]

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for text using tiktoken or heuristic fallback."""
        try:
            import tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except ImportError:
            if len(text) > 500:
                return int(len(text) * TOKENS_PER_CHAR) + 50
            return int(len(text.split()) * TOKENS_PER_WORD)

    def _create_summary(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a concise summary of old messages as a message dict."""
        summaries = []
        for msg in messages:
            content = msg.get("content", "")
            if "summary" not in msg:  # Don't double-summarize
                summary_line = (
                    f"[{msg['role'].capitalize()} said] {self._summarize_text(content)}"
                )
                summaries.append(summary_line)

        summary_text = " ".join(summaries)[:500]  # Cap at ~500 tokens
        return {"role": "system", "content": f"[Conversation summary] {summary_text}"}

    def _summarize_text(self, text: str) -> str:
        """Create one-sentence summary of text."""
        if len(text) < 20:
            return text

        # Simple heuristic: first few words usually capture essence
        words = text.split()[:15]
        return " ".join(words) + ("..." if len(words) < 15 else "")


class TokenBudgetManager:
    """
    Advanced context management with budget allocation tracking.
    """

    def __init__(self, max_tokens: int = 128000):
        self.max_tokens = max_tokens
        self.budget_allocation = {
            "system": 0.15,  # 15% for system instructions
            "user_queries": 0.3,  # 30% for user input
            "conversation_history": 0.4,  # 40% for history
            "tool_outputs": 0.2,  # 20% for tool responses
        }
        self.current_usage = 0
        self.turn_counts = {k: 0 for k in self.budget_allocation}

    def record_tokens(self, category: str, tokens: int):
        """Record token usage by category."""
        if category not in self.turn_counts:
            return
        self.turn_counts[category] += 1
        # Simplified tracking - implement per-category limits in production
        self.current_usage += tokens

    def get_remaining_budget(self) -> int:
        """Get remaining token budget."""
        return max(0, self.max_tokens - self.current_usage)

    def get_budget_percentage(self) -> float:
        """Get current usage as percentage of budget."""
        if self.max_tokens == 0:
            return 0
        return (self.current_usage / self.max_tokens) * 100

    def is_within_budget(self, new_tokens: int = 0) -> bool:
        """Check if adding new tokens would exceed budget."""
        return self.current_usage + new_tokens <= self.max_tokens

    def get_warning_threshold_tokens(self) -> int:
        """Get token count at warning threshold (75%)."""
        return int(self.max_tokens * 0.75)

    def get_prune_threshold_tokens(self) -> int:
        """Get token count at prune threshold (80%)."""
        return int(self.max_tokens * 0.80)


def estimate_prompt_tokens(prompt: str) -> int:
    """Estimate token count for a prompt."""
    # Simplified estimation - use proper tokenizer in production
    text = prompt.replace("\\n", "\n").replace("  ", " ")

    if len(text) > 500:
        return len(text) * 1.3 + 50
    return len(text.split()) * 1.3


def suggest_pruning_strategy(
    current_tokens: int, max_tokens: int, messages: List
) -> Dict:
    """
    Analyze context and suggest pruning strategy.

    Args:
        current_tokens: Current token usage
        max_tokens: Maximum allowed tokens
        messages: Current message history

    Returns:
        Pruning recommendations
    """
    ratio = current_tokens / max_tokens if max_tokens > 0 else 1

    if ratio < 0.6:
        return {
            "action": "none",
            "message": "Context usage is healthy (<60%)",
            "recommendation": None,
        }
    elif ratio < 0.75:
        return {
            "action": "warn_only",
            "message": f"Approaching budget (use at {ratio*100:.0f}%)",
            "recommendation": "Consider summarizing older turns before next response",
        }
    elif ratio < 0.85:
        return {
            "action": "prune_old",
            "message": f"At prune threshold ({ratio*100:.0f}%)",
            "recommendation": "Prune oldest conversation turns, keep last 3-4 exchanges",
        }
    else:
        return {
            "action": "emergency_prune",
            "message": f"Critical budget usage ({ratio*100:.0f}%)",
            "recommendation": "Summarize entire history to single paragraph, then proceed",
        }


# Example usage in production code:
"""
async def handle_conversation_turn(user_input: str) -> str:
    # Add user input to context
    context.append({"role": "user", "content": user_input})

    # Check budget before generating response
    if not monitor.check_budget(context):
        log_info("Context pruning triggered")
        context = monitor.prune_conversation(keep_recent_turns=4)

    # Generate response
    response = await model.generate(prompt=build_prompt(context))

    # Add to history
    context.append({"role": "assistant", "content": response})

    return response.content
"""
