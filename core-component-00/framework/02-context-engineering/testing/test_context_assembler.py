"""
Executable pytest suite for ContextAssembler and HandoffPacket.

Run with:
    pytest testing/test_context_assembler.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.context_assembler import (
    ContextAssembler,
    ContextItem,
    HandoffPacket,
    BUDGET_PROFILES,
    VALID_TASK_TYPES,
    _priority_fill,
    _anchor_order,
)


# ---------------------------------------------------------------------------
# ContextItem
# ---------------------------------------------------------------------------

class TestContextItem:
    def test_sacred_item_has_infinite_score(self):
        item = ContextItem(content="critical", slot="history", sacred=True)
        assert item.score == float("inf")

    def test_non_sacred_score_within_range(self):
        item = ContextItem(content="text", slot="retrieved",
                           relevance=0.8, recency=0.5, importance=0.6)
        assert 0.0 < item.score <= 1.0

    def test_token_count_positive(self):
        item = ContextItem(content="hello world", slot="system")
        assert item.token_count() > 0

    def test_higher_relevance_gives_higher_score(self):
        low = ContextItem(content="x", slot="retrieved", relevance=0.1)
        high = ContextItem(content="x", slot="retrieved", relevance=0.9)
        assert high.score > low.score


# ---------------------------------------------------------------------------
# _priority_fill
# ---------------------------------------------------------------------------

class TestPriorityFill:
    def _make_items(self, n, tokens_each=10):
        items = []
        for i in range(n):
            items.append(ContextItem(
                content="word " * tokens_each,
                slot="retrieved",
                relevance=i / n,
            ))
        return items

    def test_fills_within_budget(self):
        items = self._make_items(10)
        budget = 30
        selected = _priority_fill(items, budget)
        total = sum(i.token_count() for i in selected)
        assert total <= budget

    def test_sacred_items_always_included(self):
        items = self._make_items(5)
        items[0].sacred = True
        selected = _priority_fill(items, budget_tokens=5)  # tiny budget
        assert any(i.sacred for i in selected)

    def test_higher_score_items_preferred(self):
        low_score = ContextItem(content="low", slot="retrieved", relevance=0.1)
        high_score = ContextItem(content="high relevance content", slot="retrieved", relevance=0.9)
        selected = _priority_fill([low_score, high_score], budget_tokens=200)
        contents = [i.content for i in selected]
        assert "high relevance content" in contents

    def test_empty_items_returns_empty(self):
        assert _priority_fill([], 1000) == []


# ---------------------------------------------------------------------------
# _anchor_order
# ---------------------------------------------------------------------------

class TestAnchorOrder:
    def test_single_item_unchanged(self):
        item = ContextItem(content="only", slot="retrieved", relevance=0.5)
        result = _anchor_order([item])
        assert len(result) == 1

    def test_highest_score_is_first(self):
        items = [
            ContextItem(content="low", slot="retrieved", relevance=0.2),
            ContextItem(content="high", slot="retrieved", relevance=0.9),
            ContextItem(content="mid", slot="retrieved", relevance=0.5),
        ]
        ordered = _anchor_order(items)
        assert ordered[0].relevance == 0.9

    def test_second_highest_is_last(self):
        items = [
            ContextItem(content="a", slot="retrieved", relevance=0.9),
            ContextItem(content="b", slot="retrieved", relevance=0.7),
            ContextItem(content="c", slot="retrieved", relevance=0.3),
            ContextItem(content="d", slot="retrieved", relevance=0.1),
        ]
        ordered = _anchor_order(items)
        assert ordered[-1].relevance == 0.7


# ---------------------------------------------------------------------------
# ContextAssembler.build
# ---------------------------------------------------------------------------

class TestContextAssemblerBuild:
    def _make_assembler(self, max_tokens=10_000):
        return ContextAssembler(max_tokens=max_tokens)

    def test_build_returns_assembled_context(self):
        a = self._make_assembler()
        a.set_system("You are a helpful assistant.")
        result = a.build(task_type="factual_qa")
        assert result.messages
        assert result.total_tokens > 0

    def test_system_message_is_first(self):
        a = self._make_assembler()
        a.set_system("Be helpful.")
        result = a.build()
        assert result.messages[0]["role"] == "system"

    def test_unknown_task_type_falls_back(self, capsys):
        a = self._make_assembler()
        a.set_system("Role.")
        result = a.build(task_type="nonexistent_type")
        assert result.task_type == "multi_turn_reason"
        captured = capsys.readouterr()
        assert "falling back" in captured.err

    def test_all_valid_task_types_build_successfully(self):
        for task_type in VALID_TASK_TYPES:
            a = self._make_assembler()
            a.set_system("Role.")
            result = a.build(task_type=task_type)
            assert result.task_type == task_type

    def test_retrieved_content_appears_in_system_message(self):
        a = self._make_assembler()
        a.set_system("Role.")
        a.add_retrieved([{"content": "auth pattern doc", "source": "docs/auth.md"}])
        result = a.build(task_type="factual_qa")
        system_content = result.messages[0]["content"]
        assert "auth pattern doc" in system_content

    def test_sacred_context_injected_into_messages(self):
        a = self._make_assembler()
        a.set_system("Role.")
        a.add_sacred_context("User chose PostgreSQL over MySQL")
        a.add_history([{"role": "user", "content": "Hello"}])
        result = a.build()
        history_msg = next((m for m in result.messages if m["role"] != "system"), None)
        assert history_msg is not None
        assert "PostgreSQL" in history_msg["content"]

    def test_slot_usage_keys_present(self):
        a = self._make_assembler()
        a.set_system("Role.")
        result = a.build()
        assert "system" in result.slot_usage

    def test_total_tokens_within_safety_buffer(self):
        a = self._make_assembler(max_tokens=5_000)
        a.set_system("Role.")
        result = a.build()
        assert result.total_tokens <= int(5_000 * ContextAssembler.SAFETY_BUFFER) + 50

    def test_reset_clears_accumulated_context(self):
        a = self._make_assembler()
        a.set_system("Role.")
        a.add_retrieved([{"content": "doc content", "source": "doc.md"}])
        a.reset()
        result = a.build()
        assert "doc content" not in result.messages[0]["content"]


# ---------------------------------------------------------------------------
# ContextAssembler.build_handoff
# ---------------------------------------------------------------------------

class TestBuildHandoff:
    def test_full_handoff_includes_retrieved(self):
        a = ContextAssembler()
        a.set_system("Role.")
        a.add_retrieved([{"content": "doc", "source": "s.md"}])
        packet = a.build_handoff(tier="full", subagent_task="Write the module")
        assert len(packet.retrieved) > 0

    def test_minimal_handoff_excludes_retrieved(self):
        a = ContextAssembler()
        a.set_system("Role.")
        a.add_retrieved([{"content": "doc", "source": "s.md"}])
        packet = a.build_handoff(tier="minimal", subagent_task="Calculate total")
        assert len(packet.retrieved) == 0

    def test_invalid_tier_raises_value_error(self):
        a = ContextAssembler()
        a.set_system("Role.")
        with pytest.raises(ValueError, match="Invalid handoff tier"):
            a.build_handoff(tier="unknown", subagent_task="Task")

    def test_handoff_packet_has_correct_tier(self):
        a = ContextAssembler()
        a.set_system("Role.")
        packet = a.build_handoff(tier="scoped", subagent_task="Write auth module")
        assert packet.tier == "scoped"

    def test_scoped_handoff_uses_relevant_decisions(self):
        a = ContextAssembler()
        a.set_system("Role.")
        decisions = ["Use PostgreSQL", "Use JWT for auth"]
        packet = a.build_handoff(
            tier="scoped",
            subagent_task="Build login endpoint",
            relevant_decisions=decisions,
        )
        assert "Use PostgreSQL" in packet.sacred_context


# ---------------------------------------------------------------------------
# Budget profiles completeness
# ---------------------------------------------------------------------------

class TestBudgetProfiles:
    def test_all_profiles_sum_to_one(self):
        for name, profile in BUDGET_PROFILES.items():
            total = sum(profile.values())
            assert abs(total - 1.0) < 1e-9, f"Profile '{name}' sums to {total}, not 1.0"

    def test_all_profiles_have_four_slots(self):
        required_slots = {"system", "retrieved", "history", "tools"}
        for name, profile in BUDGET_PROFILES.items():
            assert set(profile.keys()) == required_slots, \
                f"Profile '{name}' missing slots: {required_slots - set(profile.keys())}"
