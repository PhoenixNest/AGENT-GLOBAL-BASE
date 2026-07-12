"""
Executable pytest suite for EpisodicMemory, SemanticMemory,
ProceduralMemory, and WorkingMemory.

Run with:
    pytest testing/test_memory_store.py -v
"""

import sys
import os
import time
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.memory_store import (
    EpisodicMemory,
    EpisodicEvent,
    SemanticMemory,
    SemanticFact,
    ProceduralMemory,
    WorkingMemory,
    SACRED_EVENT_TYPES,
)


# ---------------------------------------------------------------------------
# EpisodicMemory
# ---------------------------------------------------------------------------

class TestEpisodicMemory:
    def test_record_event_stores_event(self):
        em = EpisodicMemory(session_id="test")
        em.record_event("general", "User asked about auth")
        assert len(em) == 1

    def test_decision_is_sacred(self):
        em = EpisodicMemory()
        event = em.record_event("decision", "Use PostgreSQL")
        assert event.sacred is True

    def test_commitment_is_sacred(self):
        em = EpisodicMemory()
        event = em.record_event("commitment", "Deliver migration script by EOD")
        assert event.sacred is True

    def test_general_event_is_not_sacred(self):
        em = EpisodicMemory()
        event = em.record_event("general", "User said hello")
        assert event.sacred is False

    def test_get_sacred_context_returns_only_sacred(self):
        em = EpisodicMemory()
        em.record_event("decision", "Use PostgreSQL")
        em.record_event("general", "User asked a question")
        em.record_event("commitment", "Provide tests")
        sacred = em.get_sacred_context()
        assert len(sacred) == 2
        assert all("PostgreSQL" in s or "tests" in s for s in sacred)

    def test_sacred_context_includes_verbatim_content(self):
        em = EpisodicMemory()
        em.record_event("decision", "Use PostgreSQL over MySQL")
        sacred = em.get_sacred_context()
        assert any("PostgreSQL over MySQL" in s for s in sacred)

    def test_recent_turns_returns_last_n(self):
        em = EpisodicMemory()
        for i in range(10):
            em.record_event("general", f"Event {i}")
        recent = em.recent_turns(n=3)
        assert len(recent) == 3

    def test_advance_turn_increments_counter(self):
        em = EpisodicMemory()
        t1 = em.advance_turn()
        t2 = em.advance_turn()
        assert t2 == t1 + 1

    def test_turn_number_recorded_on_event(self):
        em = EpisodicMemory()
        em.advance_turn()
        em.advance_turn()
        event = em.record_event("general", "something")
        assert event.turn == 2

    def test_clear_removes_all_events(self):
        em = EpisodicMemory()
        em.record_event("decision", "Use Redis")
        em.clear()
        assert len(em) == 0

    def test_get_events_by_type(self):
        em = EpisodicMemory()
        em.record_event("decision", "Use Redis")
        em.record_event("general", "Hello")
        em.record_event("decision", "Use PostgreSQL")
        decisions = em.get_events_by_type("decision")
        assert len(decisions) == 2

    def test_summarise_returns_string(self):
        em = EpisodicMemory()
        for i in range(5):
            em.record_event("general", f"Event {i} content here")
        summary = em.summarise(max_tokens=100)
        assert isinstance(summary, str)
        assert len(summary) > 0


# ---------------------------------------------------------------------------
# SemanticMemory
# ---------------------------------------------------------------------------

class TestSemanticMemory:
    def test_store_and_get_fact(self):
        sm = SemanticMemory()
        sm.store("user_stack", "Prefers FastAPI, PostgreSQL")
        result = sm.get("user_stack")
        assert result == "Prefers FastAPI, PostgreSQL"

    def test_get_missing_key_returns_none(self):
        sm = SemanticMemory()
        assert sm.get("nonexistent") is None

    def test_expired_fact_returns_none(self):
        sm = SemanticMemory()
        # 1e-7 days ~= 8.6 ms TTL; sleep well past it for a reliable margin.
        sm.store("temp_fact", "Temporary value", expires_after_days=1e-7)
        time.sleep(0.05)  # Allow expiry
        assert sm.get("temp_fact") is None

    def test_non_expired_fact_returns_value(self):
        sm = SemanticMemory()
        sm.store("perm_fact", "Permanent value", expires_after_days=365)
        assert sm.get("perm_fact") == "Permanent value"

    def test_invalidate_removes_fact(self):
        sm = SemanticMemory()
        sm.store("key", "value")
        removed = sm.invalidate("key")
        assert removed is True
        assert sm.get("key") is None

    def test_invalidate_nonexistent_returns_false(self):
        sm = SemanticMemory()
        assert sm.invalidate("nonexistent") is False

    def test_query_returns_relevant_facts(self):
        sm = SemanticMemory()
        sm.store("db_pref", "User prefers PostgreSQL database")
        sm.store("lang_pref", "User prefers Python")
        results = sm.query("database preference", top_k=3)
        assert len(results) >= 1
        assert any("PostgreSQL" in r["value"] for r in results)

    def test_query_respects_top_k(self):
        sm = SemanticMemory()
        for i in range(10):
            sm.store(f"fact_{i}", f"fact about topic number {i}")
        results = sm.query("fact topic", top_k=3)
        assert len(results) <= 3

    def test_evict_expired_removes_stale_facts(self):
        sm = SemanticMemory()
        # 1e-7 days ~= 8.6 ms TTL; sleep well past it for a reliable margin.
        sm.store("stale", "value", expires_after_days=1e-7)
        sm.store("fresh", "value", expires_after_days=365)
        time.sleep(0.05)
        removed_count = sm.evict_expired()
        assert removed_count >= 1
        assert sm.get("fresh") == "value"

    def test_len_counts_stored_facts(self):
        sm = SemanticMemory()
        sm.store("a", "1")
        sm.store("b", "2")
        assert len(sm) == 2


# ---------------------------------------------------------------------------
# ProceduralMemory
# ---------------------------------------------------------------------------

class TestProceduralMemory:
    def test_register_and_activate_skill(self):
        pm = ProceduralMemory()
        pm.register("code_review", "Review for correctness and security.")
        instruction = pm.activate("code_review")
        assert instruction == "Review for correctness and security."

    def test_activate_unregistered_skill_returns_none(self):
        pm = ProceduralMemory()
        assert pm.activate("unknown_skill") is None

    def test_list_skills_returns_registered_names(self):
        pm = ProceduralMemory()
        pm.register("skill_a", "Do A")
        pm.register("skill_b", "Do B")
        skills = pm.list_skills()
        assert "skill_a" in skills
        assert "skill_b" in skills

    def test_len_counts_registered_procedures(self):
        pm = ProceduralMemory()
        pm.register("s1", "...")
        pm.register("s2", "...")
        assert len(pm) == 2


# ---------------------------------------------------------------------------
# WorkingMemory
# ---------------------------------------------------------------------------

class TestWorkingMemory:
    def test_set_task_and_serialise(self):
        wm = WorkingMemory()
        wm.set_task("Build authentication API")
        context = wm.to_context_string()
        assert "Build authentication API" in context

    def test_set_current_step_appears_in_context(self):
        wm = WorkingMemory()
        wm.set_current_step("Step 2 of 4: Define schemas")
        context = wm.to_context_string()
        assert "Step 2 of 4" in context

    def test_complete_step_moves_to_completed(self):
        wm = WorkingMemory()
        wm.set_current_step("Step 1")
        wm.complete_step("Step 1")
        context = wm.to_context_string()
        assert "Step 1" in context  # Appears in completed

    def test_add_tool_result_appears_in_context(self):
        wm = WorkingMemory()
        wm.add_tool_result("schema_validator", {"valid": True})
        context = wm.to_context_string()
        assert "schema_validator" in context

    def test_add_note_appears_in_context(self):
        wm = WorkingMemory()
        wm.add_note("User needs async endpoints")
        context = wm.to_context_string()
        assert "async endpoints" in context

    def test_clear_resets_all_state(self):
        wm = WorkingMemory()
        wm.set_task("Task A")
        wm.set_current_step("Step 1")
        wm.clear()
        context = wm.to_context_string()
        assert "Task A" not in context
        assert "Step 1" not in context

    def test_method_chaining(self):
        wm = WorkingMemory()
        result = wm.set_task("Task").set_current_step("Step 1").add_note("Note")
        assert result is wm  # Returns self for chaining


# ---------------------------------------------------------------------------
# Sacred event types constant
# ---------------------------------------------------------------------------

class TestSacredEventTypes:
    def test_decision_is_in_sacred_types(self):
        assert "decision" in SACRED_EVENT_TYPES

    def test_commitment_is_in_sacred_types(self):
        assert "commitment" in SACRED_EVENT_TYPES

    def test_general_is_not_sacred(self):
        assert "general" not in SACRED_EVENT_TYPES


# ---------------------------------------------------------------------------
# Optional write-through sink (memory_vector_store.PersistentMemorySink)
# ---------------------------------------------------------------------------

class _RecordingSink:
    """Minimal duck-typed sink — mirrors PersistentMemorySink's public methods
    without depending on memory_vector_store.py, keeping this test file focused
    on memory_store.py's own contract (calls the sink, doesn't crash if it fails)."""

    def __init__(self, fail=False):
        self.fail = fail
        self.episodic_calls = []
        self.semantic_calls = []
        self.procedural_calls = []

    def write_episodic(self, event, session_id):
        if self.fail:
            raise RuntimeError("simulated sink failure")
        self.episodic_calls.append((event, session_id))

    def write_semantic(self, fact):
        if self.fail:
            raise RuntimeError("simulated sink failure")
        self.semantic_calls.append(fact)

    def write_procedural(self, skill_name, instruction, source_session_id=None):
        if self.fail:
            raise RuntimeError("simulated sink failure")
        self.procedural_calls.append((skill_name, instruction, source_session_id))


class TestEpisodicMemorySinkWriteThrough:
    def test_no_sink_preserves_default_behaviour(self):
        em = EpisodicMemory(session_id="s1")
        em.record_event("general", "no sink configured")
        assert len(em) == 1

    def test_record_event_calls_sink(self):
        sink = _RecordingSink()
        em = EpisodicMemory(session_id="s1", sink=sink)
        em.record_event("general", "hello")
        assert len(sink.episodic_calls) == 1
        _, session_id = sink.episodic_calls[0]
        assert session_id == "s1"

    def test_sink_failure_does_not_break_the_write(self):
        sink = _RecordingSink(fail=True)
        em = EpisodicMemory(session_id="s1", sink=sink)
        event = em.record_event("general", "still recorded in-memory")
        assert event is not None
        assert len(em) == 1


class TestSemanticMemorySinkWriteThrough:
    def test_no_sink_preserves_default_behaviour(self):
        sm = SemanticMemory()
        sm.store("k", "v")
        assert sm.get("k") == "v"

    def test_store_calls_sink(self):
        sink = _RecordingSink()
        sm = SemanticMemory(sink=sink)
        sm.store("user_stack", "FastAPI")
        assert len(sink.semantic_calls) == 1
        assert sink.semantic_calls[0].key == "user_stack"

    def test_sink_failure_does_not_break_the_write(self):
        sink = _RecordingSink(fail=True)
        sm = SemanticMemory(sink=sink)
        fact = sm.store("k", "v")
        assert fact is not None
        assert sm.get("k") == "v"


class TestProceduralMemorySinkWriteThrough:
    def test_no_sink_preserves_default_behaviour(self):
        pm = ProceduralMemory()
        pm.register("skill", "do it")
        assert pm.activate("skill") == "do it"

    def test_register_calls_sink(self):
        sink = _RecordingSink()
        pm = ProceduralMemory(sink=sink, source_session_id="s1")
        pm.register("code_review", "check security")
        assert len(sink.procedural_calls) == 1
        skill_name, instruction, session_id = sink.procedural_calls[0]
        assert skill_name == "code_review"
        assert session_id == "s1"

    def test_sink_failure_does_not_break_the_write(self):
        sink = _RecordingSink(fail=True)
        pm = ProceduralMemory(sink=sink)
        pm.register("skill", "instruction")  # must not raise
        assert pm.activate("skill") == "instruction"
