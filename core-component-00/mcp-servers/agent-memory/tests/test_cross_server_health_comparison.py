"""
Automated cross-server health_check comparison — Recommendation 2 from
core-component-00/telescope/2026-07-17-agent-memory-client-instability/research-report.md:

    "Add a lightweight comparison test that calls both servers' health_check
    back-to-back in CI-like conditions, so a future regression like Finding 3
    surfaces automatically instead of requiring a manual CEO-requested review
    to discover."

Finding 3 in that report was: agent-memory's health_check reported
reachable=false with all-zero point counts while workspace-knowledge,
querying the *same* qdrant-memory instance in the same breath, reported
correctly (root-caused and fixed in Findings 4/5 of that report — an
always-on in-process embedder-warmup thread wedging on a scipy import and
blocking QdrantClient's constructor process-wide). This file is structured in
two layers, per that design intent:

1. TestCompareMemoryInstanceHealthLogic — pure, deterministic tests of the
   divergence-detection logic itself (health_comparison.py), fixed injected
   inputs, no live Qdrant instance required at all. Proves the comparator is
   correct independent of whether any live infrastructure is reachable right
   now.
2. TestLiveCrossServerComparison — a live integration test against the real
   qdrant-memory instance (http://localhost:6335 by default), calling each
   server's *own* memory-instance health-check code path (not a shared,
   pre-built client) so a future asymmetry like Finding 3 — one server's own
   client-construction path failing while the other's succeeds — would
   actually be caught. pytest.skip()s cleanly if qdrant-memory is
   unreachable, matching this workspace's own graceful-degradation
   discipline rather than failing the whole suite in environments with no
   live Qdrant (e.g. a fresh clone, CI without the qdrant-memory container
   running).
"""
import importlib.util
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from health_comparison import compare_memory_instance_health  # noqa: E402

_MCP_SERVERS_ROOT = Path(__file__).resolve().parents[2]
_WORKSPACE_KNOWLEDGE_SERVER_PATH = _MCP_SERVERS_ROOT / "workspace-knowledge" / "server.py"


# ---------------------------------------------------------------------------
# Layer 1 — pure comparison-logic tests, fixed inputs, no live Qdrant needed
# ---------------------------------------------------------------------------


class TestCompareMemoryInstanceHealthLogic:
    def test_identical_blocks_do_not_diverge(self):
        block = {
            "reachable": True,
            "point_counts": {"memory_semantic": 4, "memory_episodic": 0},
        }
        result = compare_memory_instance_health(block, dict(block))
        assert result["diverged"] is False
        assert result["differences"] == []

    def test_differing_reachable_is_flagged(self):
        block_a = {"reachable": False, "point_counts": {}}
        block_b = {"reachable": True, "point_counts": {}}
        result = compare_memory_instance_health(block_a, block_b)
        assert result["diverged"] is True
        assert {"field": "reachable", "a": False, "b": True} in result["differences"]

    def test_differing_point_count_for_shared_collection_is_flagged(self):
        block_a = {"reachable": True, "point_counts": {"memory_semantic": 0}}
        block_b = {"reachable": True, "point_counts": {"memory_semantic": 4}}
        result = compare_memory_instance_health(block_a, block_b)
        assert result["diverged"] is True
        assert {"field": "point_counts.memory_semantic", "a": 0, "b": 4} in result["differences"]

    def test_collection_present_only_on_one_side_is_flagged(self):
        block_a = {"reachable": True, "point_counts": {"memory_reflection": 4}}
        block_b = {"reachable": True, "point_counts": {}}
        result = compare_memory_instance_health(block_a, block_b)
        assert result["diverged"] is True
        assert {"field": "point_counts.memory_reflection", "a": 4, "b": None} in result["differences"]

    def test_multiple_differences_are_all_reported_not_just_the_first(self):
        block_a = {
            "reachable": False,
            "point_counts": {"memory_semantic": 0, "memory_episodic": 0},
        }
        block_b = {
            "reachable": True,
            "point_counts": {"memory_semantic": 4, "memory_episodic": 0},
        }
        result = compare_memory_instance_health(block_a, block_b)
        assert result["diverged"] is True
        assert len(result["differences"]) == 2

    def test_empty_point_counts_on_both_sides_does_not_diverge(self):
        result = compare_memory_instance_health(
            {"reachable": False, "point_counts": {}}, {"reachable": False, "point_counts": {}}
        )
        assert result["diverged"] is False

    def test_missing_point_counts_key_is_handled_without_raising(self):
        result = compare_memory_instance_health({"reachable": True}, {"reachable": True})
        assert result["diverged"] is False


# ---------------------------------------------------------------------------
# Layer 2 — live integration test against the real qdrant-memory instance
# ---------------------------------------------------------------------------


def _load_module(module_name: str, file_path: Path):
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class TestLiveCrossServerComparison:
    def test_agent_memory_and_workspace_knowledge_agree_on_memory_instance(
        self, agent_memory_server, tmp_path_factory, monkeypatch
    ):
        # Reachability gate first, using agent-memory's own real production
        # health_check() code path (not a hand-rolled duplicate probe) — this
        # also means the reachability check itself is the same code this test
        # is regression-guarding, not a separate assumption about it.
        block_a = agent_memory_server.health_check()["memory_instance"]
        if not block_a["reachable"]:
            pytest.skip(
                "qdrant-memory unreachable (agent_memory_server.health_check() "
                f"reported reachable=False) — skipping live cross-server comparison. "
                f"detail: {block_a.get('error')}"
            )

        # Only pay workspace-knowledge/server.py's import cost (it constructs
        # a full SearchEngine over the workspace at module import time) once
        # we know there's a live qdrant-memory instance to actually compare
        # against. WORKSPACE_ROOT is pointed at a throwaway empty directory
        # first so that construction's BM25/file-scan step has nothing to
        # walk — this test only needs _memory_instance_health_block(), which
        # does not depend on WORKSPACE_ROOT or the `engine` global at all.
        empty_root = tmp_path_factory.mktemp("wk-root-for-cross-server-test")
        monkeypatch.setenv("WORKSPACE_ROOT", str(empty_root))
        wk_server = _load_module("workspace_knowledge_server", _WORKSPACE_KNOWLEDGE_SERVER_PATH)

        # Each server exercises its OWN client-construction path here — not a
        # shared client object — since Finding 3's actual failure mode was
        # one server's own construction path hanging/failing while the
        # other's succeeded. A shared client would not have caught that.
        block_b = wk_server._memory_instance_health_block()

        result = compare_memory_instance_health(block_a, block_b)
        assert not result["diverged"], (
            "agent-memory and workspace-knowledge disagree about the same "
            f"live qdrant-memory instance's memory_instance state: {result['differences']}"
        )
