"""
Tests for HandoffPacket — Inter-Agent Context Transfer

Covers: construction, serialization, validation, and token estimation.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.handoff_packet import HandoffPacket, HandoffTier


class TestHandoffTier:
    def test_tier_values(self):
        assert HandoffTier.FULL.value == "full"
        assert HandoffTier.SCOPED.value == "scoped"
        assert HandoffTier.MINIMAL.value == "minimal"

    def test_tier_from_string(self):
        assert HandoffTier("scoped") == HandoffTier.SCOPED


class TestHandoffPacketCreation:
    def test_default_values(self):
        packet = HandoffPacket()
        assert packet.tier == HandoffTier.SCOPED
        assert packet.task == ""
        assert packet.budget == 128_000

    def test_minimal_packet(self):
        packet = HandoffPacket(
            tier=HandoffTier.MINIMAL,
            task="Calculate sum of 2 + 2",
            acceptance_criteria=["Return integer result"],
        )
        assert packet.tier == HandoffTier.MINIMAL
        assert packet.conversation_history is None

    def test_full_packet(self):
        packet = HandoffPacket(
            tier=HandoffTier.FULL,
            task="Review entire codebase",
            conversation_history=[
                {"role": "user", "content": "Review my code"},
                {"role": "assistant", "content": "I'll review it"},
            ],
            sacred_context=["Must use Python 3.12+"],
        )
        assert packet.tier == HandoffTier.FULL
        assert len(packet.conversation_history) == 2


class TestSerialization:
    def test_round_trip(self):
        original = HandoffPacket(
            tier=HandoffTier.SCOPED,
            task="Build API endpoint",
            acceptance_criteria=["Returns 200 OK"],
            sacred_context=["Use REST, not GraphQL"],
            relevant_files=["src/api.py"],
            budget=64_000,
            metadata={"priority": "high"},
        )
        data = original.to_dict()
        restored = HandoffPacket.from_dict(data)

        assert restored.tier == original.tier
        assert restored.task == original.task
        assert restored.acceptance_criteria == original.acceptance_criteria
        assert restored.sacred_context == original.sacred_context
        assert restored.relevant_files == original.relevant_files
        assert restored.budget == original.budget
        assert restored.metadata == original.metadata

    def test_from_dict_defaults(self):
        packet = HandoffPacket.from_dict({})
        assert packet.tier == HandoffTier.SCOPED
        assert packet.task == ""


class TestValidation:
    def test_valid_scoped_packet(self):
        packet = HandoffPacket(
            tier=HandoffTier.SCOPED,
            task="Build something",
        )
        assert packet.validate() == []

    def test_empty_task(self):
        packet = HandoffPacket(tier=HandoffTier.SCOPED)
        issues = packet.validate()
        assert "Task description is empty" in issues

    def test_full_without_history(self):
        packet = HandoffPacket(
            tier=HandoffTier.FULL,
            task="Review code",
        )
        issues = packet.validate()
        assert "Full tier requires conversation_history" in issues

    def test_minimal_with_history(self):
        packet = HandoffPacket(
            tier=HandoffTier.MINIMAL,
            task="Calculate",
            conversation_history=[{"role": "user", "content": "hi"}],
        )
        issues = packet.validate()
        assert "Minimal tier should not include conversation_history" in issues

    # -- Fleet-origin check for conversation_history (GSMSE remediation T15) --

    def test_all_turns_matching_fleet_no_cross_fleet_issue(self):
        packet = HandoffPacket(
            tier=HandoffTier.SCOPED,
            task="Build something",
            conversation_history=[
                {"role": "user", "content": "hi", "fleet_id": "fleet-a"},
                {"role": "assistant", "content": "hello", "fleet_id": "fleet-a"},
            ],
        )
        issues = packet.validate(expected_fleet_id="fleet-a")
        assert issues == []

    def test_single_cross_fleet_turn_flagged_with_index_and_ids(self):
        packet = HandoffPacket(
            tier=HandoffTier.SCOPED,
            task="Build something",
            conversation_history=[
                {"role": "user", "content": "hi", "fleet_id": "fleet-a"},
                {"role": "assistant", "content": "hello", "fleet_id": "fleet-b"},
            ],
        )
        issues = packet.validate(expected_fleet_id="fleet-a")
        assert len(issues) == 1
        assert "conversation_history[1]" in issues[0]
        assert "fleet='fleet-b'" in issues[0]
        assert "expected='fleet-a'" in issues[0]

    def test_multiple_cross_fleet_turns_each_flagged_separately(self):
        packet = HandoffPacket(
            tier=HandoffTier.SCOPED,
            task="Build something",
            conversation_history=[
                {"role": "user", "content": "a", "fleet_id": "fleet-b"},
                {"role": "assistant", "content": "b", "fleet_id": "fleet-a"},
                {"role": "user", "content": "c", "fleet_id": "fleet-c"},
            ],
        )
        issues = packet.validate(expected_fleet_id="fleet-a")
        assert len(issues) == 2
        assert "conversation_history[0]" in issues[0]
        assert "fleet='fleet-b'" in issues[0]
        assert "conversation_history[2]" in issues[1]
        assert "fleet='fleet-c'" in issues[1]

    def test_turn_missing_fleet_id_flagged_as_unverified_origin(self):
        # Regression guard for a fail-open default found in a real pilot
        # run: validate()'s `if turn_fleet is not None` guard meant a turn that
        # omits the "fleet_id" key entirely (turn.get("fleet_id") -> None)
        # was silently treated as compliant — a fail-open default that would
        # let a turn bypass the cross-fleet check simply by omitting the
        # key. validate() now flags a missing fleet_id as an unverified-
        # origin issue in its own right. This test must keep failing (i.e.
        # keep asserting the turn is flagged) if that fail-closed behavior
        # regresses.
        packet = HandoffPacket(
            tier=HandoffTier.SCOPED,
            task="Build something",
            conversation_history=[
                {"role": "user", "content": "hi"},
            ],
        )
        issues = packet.validate(expected_fleet_id="fleet-a")
        assert len(issues) == 1
        assert "conversation_history[0]" in issues[0]
        assert "missing fleet_id" in issues[0]

    def test_expected_fleet_id_none_skips_cross_fleet_check(self):
        packet = HandoffPacket(
            tier=HandoffTier.SCOPED,
            task="Build something",
            conversation_history=[
                {"role": "user", "content": "a", "fleet_id": "fleet-b"},
                {"role": "assistant", "content": "b", "fleet_id": "fleet-c"},
            ],
        )
        issues = packet.validate()
        assert issues == []


class TestTokenEstimation:
    def test_basic_estimate(self):
        packet = HandoffPacket(
            tier=HandoffTier.SCOPED,
            task="Build a REST API for user management",
        )
        assert packet.estimated_tokens > 0

    def test_full_packet_higher_tokens(self):
        minimal = HandoffPacket(
            tier=HandoffTier.MINIMAL,
            task="Calculate 2+2",
        )
        full = HandoffPacket(
            tier=HandoffTier.FULL,
            task="Calculate 2+2",
            conversation_history=[
                {"role": "user", "content": "A" * 1000},
            ],
        )
        assert full.estimated_tokens > minimal.estimated_tokens
