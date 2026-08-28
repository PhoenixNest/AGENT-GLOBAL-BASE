"""
Tests for ContextCompressor's utilization-based compaction trigger (Context R2)
and the sacred-turn preservation fix that underpins decision continuity (Context R3).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.context_compressor import ContextCompressor, estimate_turns_tokens


def _turns(n: int) -> list:
    return [{"role": "user" if i % 2 == 0 else "assistant", "content": f"turn {i} content"} for i in range(n)]


class TestUtilizationTrigger:
    def test_default_trigger_is_seventy_five_percent(self):
        compressor = ContextCompressor()
        assert compressor.utilization_trigger == 0.75

    def test_trigger_is_configurable(self):
        compressor = ContextCompressor(utilization_trigger=0.5)
        assert compressor.utilization_trigger == 0.5

    def test_invalid_trigger_raises(self):
        for bad in (0.0, -0.1, 1.5):
            try:
                ContextCompressor(utilization_trigger=bad)
                assert False, f"expected ValueError for utilization_trigger={bad}"
            except ValueError:
                pass

    def test_current_utilization_computes_fraction(self):
        compressor = ContextCompressor()
        assert compressor.current_utilization(750, 1000) == 0.75
        assert compressor.current_utilization(100, 0) == 0.0

    def test_should_trigger_compaction_below_threshold_is_false(self):
        compressor = ContextCompressor(utilization_trigger=0.75)
        assert compressor.should_trigger_compaction(700, 1000) is False

    def test_should_trigger_compaction_at_threshold_is_true(self):
        compressor = ContextCompressor(utilization_trigger=0.75)
        assert compressor.should_trigger_compaction(750, 1000) is True

    def test_should_trigger_compaction_above_threshold_is_true(self):
        compressor = ContextCompressor(utilization_trigger=0.75)
        assert compressor.should_trigger_compaction(900, 1000) is True

    def test_compress_if_triggered_below_threshold_returns_turns_unchanged(self):
        compressor = ContextCompressor(utilization_trigger=0.75)
        turns = _turns(20)
        result = compressor.compress_if_triggered(turns, current_tokens=100, max_tokens=1000)
        assert result.strategy == "below_utilization_trigger"
        assert result.content == turns
        assert result.compressed_tokens == result.original_tokens

    def test_compress_if_triggered_above_threshold_fires_compaction(self):
        compressor = ContextCompressor(utilization_trigger=0.5, keep_recent_turns=3)
        turns = _turns(50)
        current_tokens = estimate_turns_tokens(turns)
        max_tokens = int(current_tokens / 0.6)  # utilization ~60% > 50% trigger
        result = compressor.compress_if_triggered(turns, current_tokens=current_tokens, max_tokens=max_tokens)
        assert result.strategy != "below_utilization_trigger"
        assert result.compressed_tokens < current_tokens

    def test_compress_if_triggered_respects_explicit_target(self):
        compressor = ContextCompressor(utilization_trigger=0.5)
        turns = _turns(50)
        current_tokens = estimate_turns_tokens(turns)
        max_tokens = int(current_tokens / 0.6)
        result = compressor.compress_if_triggered(
            turns, current_tokens=current_tokens, max_tokens=max_tokens, target_tokens=10
        )
        assert result.compressed_tokens <= current_tokens


class TestSacredTurnAbsoluteIndexing:
    """Regression coverage for the tiering-loop index bug: sacred turns must
    survive verbatim regardless of which compression tier they fall into."""

    def test_sacred_turn_in_final_tier_of_older_turns_survives(self):
        compressor = ContextCompressor(keep_recent_turns=3)
        turns = _turns(60)
        sacred_idx = 55  # falls in older_turns (turns[:-3]) near its end, i.e. tier 3
        turns[sacred_idx]["content"] = "SACRED_MARKER_DO_NOT_LOSE"
        result = compressor.compress_history(turns, target_tokens=50, sacred_turns=[sacred_idx])
        contents = [t.get("content") for t in result.content]
        assert "SACRED_MARKER_DO_NOT_LOSE" in contents

    def test_sacred_turn_in_first_tier_of_older_turns_survives(self):
        compressor = ContextCompressor(keep_recent_turns=3)
        turns = _turns(60)
        sacred_idx = 2  # falls in the first tier of older_turns
        turns[sacred_idx]["content"] = "SACRED_MARKER_EARLY"
        result = compressor.compress_history(turns, target_tokens=50, sacred_turns=[sacred_idx])
        contents = [t.get("content") for t in result.content]
        assert "SACRED_MARKER_EARLY" in contents

    def test_multiple_sacred_turns_across_all_tiers_survive(self):
        compressor = ContextCompressor(keep_recent_turns=3)
        turns = _turns(60)
        sacred_indices = [2, 25, 50]
        for i, idx in enumerate(sacred_indices):
            turns[idx]["content"] = f"SACRED_MARKER_{i}"
        result = compressor.compress_history(turns, target_tokens=50, sacred_turns=sacred_indices)
        contents = [t.get("content") for t in result.content]
        for i in range(len(sacred_indices)):
            assert f"SACRED_MARKER_{i}" in contents


class TestEstimateTurnsTokens:
    def test_matches_internal_accounting_basis(self):
        turns = _turns(10)
        compressor = ContextCompressor()
        result = compressor.compress_history(turns, target_tokens=10_000)
        assert result.original_tokens == estimate_turns_tokens(turns)
