"""
Executable pytest suite for ContextMonitor and TokenBudgetManager.

Run with:
    pytest testing/test_context_monitor.py -v
"""

import sys
import os

# Make the implementations package importable when running from the module root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.context_monitor import (
    ContextMonitor,
    TokenBudgetManager,
    estimate_prompt_tokens,
    suggest_pruning_strategy,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_messages(n: int, tokens_each: int = 100):
    """Return a synthetic message list and pre-load the monitor's token counts."""
    msgs = []
    for i in range(n):
        msgs.append({"role": "user" if i % 2 == 0 else "assistant", "content": f"message {i}"})
    return msgs


def _monitor_with_usage(ratio: float, max_tokens: int = 128_000) -> ContextMonitor:
    """Return a ContextMonitor whose token count equals ratio * max_tokens."""
    monitor = ContextMonitor(max_tokens=max_tokens)
    total = int(ratio * max_tokens)
    monitor.token_counts_per_turn[1] = total
    monitor.history = [{"role": "user", "content": "x" * total}]
    return monitor


# ---------------------------------------------------------------------------
# ContextMonitor.check_budget
# ---------------------------------------------------------------------------

class TestCheckBudget:
    def test_healthy_usage_returns_true(self):
        monitor = _monitor_with_usage(0.50)
        assert monitor.check_budget([]) is True

    def test_warn_threshold_returns_true_and_logs(self, capsys):
        monitor = _monitor_with_usage(0.77)  # above warn (0.75), below prune (0.80)
        result = monitor.check_budget([])
        assert result is True
        captured = capsys.readouterr()
        assert "approaching budget" in captured.err.lower()

    def test_prune_threshold_triggers_pruning(self, capsys):
        monitor = _monitor_with_usage(0.85)  # above prune threshold (0.80)
        result = monitor.check_budget([])
        assert result is True
        captured = capsys.readouterr()
        assert "prune threshold" in captured.err.lower()

    def test_overflow_returns_false_and_logs(self, capsys):
        monitor = _monitor_with_usage(1.05)
        result = monitor.check_budget([])
        assert result is False
        captured = capsys.readouterr()
        assert "overflow" in captured.err.lower()

    def test_exact_boundary_warn_at_75(self):
        # Exactly at warn threshold: total_tokens == warn_threshold
        monitor = ContextMonitor(max_tokens=1000, warn_at=0.75, prune_at=0.80)
        monitor.token_counts_per_turn[1] = 750
        monitor.history = [{"role": "user", "content": "x"}]
        result = monitor.check_budget([])
        assert result is True  # Should warn but not fail

    def test_exact_boundary_prune_at_80(self):
        monitor = ContextMonitor(max_tokens=1000, warn_at=0.75, prune_at=0.80)
        monitor.token_counts_per_turn[1] = 800
        monitor.history = [{"role": "user", "content": "x"}]
        result = monitor.check_budget([])
        assert result is True  # Should prune but not fail


# ---------------------------------------------------------------------------
# ContextMonitor.prune_conversation
# ---------------------------------------------------------------------------

class TestPruneConversation:
    def test_prune_keeps_recent_turns(self):
        monitor = ContextMonitor()
        for i in range(10):
            monitor.add_message("user" if i % 2 == 0 else "assistant", f"turn {i}")
        pruned = monitor.prune_conversation(keep_recent_turns=3)
        # summary dict + 3 recent turns
        assert len(pruned) == 4

    def test_prune_summary_is_dict_with_role_and_content(self):
        monitor = ContextMonitor()
        for i in range(6):
            monitor.add_message("user" if i % 2 == 0 else "assistant", f"turn {i}")
        pruned = monitor.prune_conversation(keep_recent_turns=2)
        summary = pruned[0]
        assert isinstance(summary, dict), "Summary must be a dict, not a str"
        assert "role" in summary
        assert "content" in summary

    def test_no_prune_when_history_too_short(self):
        monitor = ContextMonitor()
        monitor.add_message("user", "hello")
        monitor.add_message("assistant", "world")
        pruned = monitor.prune_conversation(keep_recent_turns=3)
        assert len(pruned) == 2  # Nothing to prune

    def test_prune_without_summarize(self):
        monitor = ContextMonitor()
        for i in range(8):
            monitor.add_message("user" if i % 2 == 0 else "assistant", f"turn {i}")
        pruned = monitor.prune_conversation(keep_recent_turns=3, summarize_old=False)
        assert len(pruned) == 3  # Only recent turns, no summary prepended


# ---------------------------------------------------------------------------
# TokenBudgetManager
# ---------------------------------------------------------------------------

class TestTokenBudgetManager:
    def test_initial_remaining_equals_max(self):
        mgr = TokenBudgetManager(max_tokens=10_000)
        assert mgr.get_remaining_budget() == 10_000

    def test_record_tokens_reduces_budget(self):
        mgr = TokenBudgetManager(max_tokens=10_000)
        mgr.record_tokens("system", 500)
        assert mgr.get_remaining_budget() == 9_500

    def test_is_within_budget_true_for_small_addition(self):
        mgr = TokenBudgetManager(max_tokens=1_000)
        mgr.record_tokens("system", 100)
        assert mgr.is_within_budget(new_tokens=800) is True

    def test_is_within_budget_false_when_over(self):
        mgr = TokenBudgetManager(max_tokens=1_000)
        mgr.record_tokens("system", 900)
        assert mgr.is_within_budget(new_tokens=200) is False

    def test_budget_percentage(self):
        mgr = TokenBudgetManager(max_tokens=1_000)
        mgr.record_tokens("system", 500)
        assert mgr.get_budget_percentage() == 50.0

    def test_warn_threshold_is_75_percent(self):
        mgr = TokenBudgetManager(max_tokens=1_000)
        assert mgr.get_warning_threshold_tokens() == 750

    def test_prune_threshold_is_80_percent(self):
        mgr = TokenBudgetManager(max_tokens=1_000)
        assert mgr.get_prune_threshold_tokens() == 800


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

class TestUtilityFunctions:
    def test_estimate_prompt_tokens_short_text(self):
        tokens = estimate_prompt_tokens("hello world")
        assert tokens > 0

    def test_estimate_prompt_tokens_long_text(self):
        long_text = "word " * 200
        tokens = estimate_prompt_tokens(long_text)
        assert tokens > 100

    def test_suggest_pruning_strategy_none_below_60(self):
        result = suggest_pruning_strategy(500, 1_000, [])
        assert result["action"] == "none"

    def test_suggest_pruning_strategy_warn_between_60_and_75(self):
        result = suggest_pruning_strategy(700, 1_000, [])
        assert result["action"] == "warn_only"

    def test_suggest_pruning_strategy_prune_between_75_and_85(self):
        result = suggest_pruning_strategy(800, 1_000, [])
        assert result["action"] == "prune_old"

    def test_suggest_pruning_strategy_emergency_above_85(self):
        result = suggest_pruning_strategy(900, 1_000, [])
        assert result["action"] == "emergency_prune"
