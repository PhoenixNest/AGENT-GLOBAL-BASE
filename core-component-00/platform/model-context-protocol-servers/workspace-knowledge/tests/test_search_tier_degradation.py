"""Scenario-regression tests for SearchEngine's tiered search fallback chain
(SearchTier.HYBRID_QDRANT -> HYBRID -> BM25 -> RAWFS).

Added to close R1 (P1) from the 2026-09-01 MCP servers enterprise benchmark
assessment
(core-component-00/platform/benchmarks/model-context-protocol-servers/2026-09-01-mcp-servers-enterprise-assessment/enterprise-assessment.md,
Benchmark Row B6 / Remediation R1): `workspace-knowledge` had exactly one
first-party test file, unrelated to the tiered-search/degradation logic that
runs live in production and was directly observed degrading this session
(that assessment's S7 finding).

Pattern mirrors agent-memory/tests/test_embedder_reliability_fixes.py and
test_cross_server_health_comparison.py: force a dependency failure and
assert the server degrades to the next tier instead of raising, then check
whether/how it recovers once the forced condition is lifted -- verified
against the real implementation, not assumed.

Engine construction follows tests/test_upsert_delete_ordering_fix.py's
`_make_engine` pattern: SearchEngine.__new__() bypasses __init__ (and
therefore the real BM25/FAISS/Qdrant startup chain, which needs live
dependencies and workspace content this suite has no business depending
on), and every collaborator method the fallback chain calls is stubbed
directly on the instance.

FIXED -- N2 (P1), query-time chain now matches the documented chain (see
TestHybridQdrantFailureFallsToHybrid and
TestHybridQdrantAndHybridBothFailCascadesToBm25 below). Before this fix,
search_docs()'s docstring and the benchmark assessment both described the
chain as HYBRID_QDRANT -> HYBRID -> BM25 -> RAWFS -- accurate for
*initialization* (_init_faiss_background: SearchTier.HYBRID_QDRANT if
_qdrant_ready else SearchTier.HYBRID) but NOT for what _search_with_fallback
did at *query time*: a live Qdrant failure while already in HYBRID_QDRANT
tier dropped straight to SearchTier.BM25, skipping HYBRID entirely -- even
though the FAISS index and embedding model were already resident in memory
at that point (HYBRID_QDRANT is only reachable after the Phase 2 FAISS
build has already completed). A query-time Qdrant outage was therefore
losing semantic search capability it did not have to lose.
_search_with_fallback now demotes a HYBRID_QDRANT query failure to HYBRID
(local FAISS) first, and only falls further to BM25 if that HYBRID attempt
itself also fails -- see server.py's SearchEngine._search_with_fallback.

FINDING -- recovery is one-directional at runtime (see
TestRecoveryBehavior below): once _search_with_fallback demotes the tier,
nothing re-probes the higher tier on a later call, even after the
underlying dependency would now succeed. The only way the tier climbs back
up is an explicit rebuild_index() call. This is the same staleness shape
the benchmark assessment flagged for agent-memory's health_check
(B2/R2, "cached ready" vs. actual serviceability) -- here it is not a
staleness bug in reporting, it is simply how the fallback is designed: no
auto-recovery, degrade-and-stay until an operator/agent runs rebuild_index.
(Tracked as N3 in the same severity triage as N2 above; not yet fixed as of
this commit.)
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import server  # noqa: E402

SearchTier = server.SearchTier


def _make_engine(tier, **overrides):
    """Construct a SearchEngine for _search_with_fallback/health-block
    testing only, bypassing __init__ -- same bypass pattern as
    test_upsert_delete_ordering_fix.py's _make_engine, extended with the
    handful of extra attributes the fallback/health-check paths read."""
    engine = server.SearchEngine.__new__(server.SearchEngine)
    engine._tier = tier
    engine._degradation_reason = None
    engine._chunks = []
    engine._qdrant_ready = False
    engine._qdrant_client = None
    engine._collection_name = "workspace_knowledge"
    for name, value in overrides.items():
        setattr(engine, name, value)
    return engine


def _result(file="x.md", score=1.0, snippet="snippet"):
    return {"file": file, "section": "", "score": score, "snippet": snippet}


# ---------------------------------------------------------------------------
# HYBRID_QDRANT -> HYBRID (Qdrant unreachable at query time) -- N2
# ---------------------------------------------------------------------------


class TestHybridQdrantFailureFallsToHybrid:
    """A live query-time Qdrant failure while in HYBRID_QDRANT tier -- the
    exact scenario the 2026-09-01 benchmark assessment observed live (S7:
    "Qdrant Docker unreachable ... falling back to FAISS" during a real
    health_check/search_docs call in that session). N2 fix: the fallback
    now tries local FAISS search (HYBRID) before ever considering BM25."""

    def test_search_still_returns_a_result_not_an_exception(self):
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        engine._search_hybrid_qdrant = MagicMock(
            side_effect=ConnectionError("Qdrant Docker unreachable: timed out")
        )
        hybrid_results = [_result("a.md")]
        engine._search_hybrid = MagicMock(return_value=hybrid_results)
        # Must not be reached -- HYBRID succeeds, so the cascade should
        # never fall as far as BM25.
        engine._search_bm25 = MagicMock(
            side_effect=AssertionError("BM25 must not be tried when HYBRID succeeds")
        )

        results = engine._search_with_fallback("query", top_k=5)

        assert results == hybrid_results
        engine._search_hybrid.assert_called_once_with("query", 5)
        engine._search_bm25.assert_not_called()

    def test_tier_falls_to_hybrid_not_bm25(self):
        """N2 regression guard: a generic Qdrant-query exception at
        HYBRID_QDRANT demotes to HYBRID (local FAISS semantic search) and
        attempts it immediately, not straight to BM25 -- the fix for the
        exact gap this suite's module docstring used to document."""
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        engine._search_hybrid_qdrant = MagicMock(side_effect=RuntimeError("boom"))
        engine._search_hybrid = MagicMock(return_value=[])
        # If the runtime fallback ever regresses to skipping HYBRID again,
        # this must not be called -- this assertion is the regression guard
        # for that specific behavior.
        engine._search_bm25 = MagicMock(
            side_effect=AssertionError("BM25 must not be tried before HYBRID is attempted")
        )

        engine._search_with_fallback("query", top_k=5)

        assert engine._tier == SearchTier.HYBRID
        engine._search_hybrid.assert_called_once_with("query", 5)
        engine._search_bm25.assert_not_called()

    def test_degradation_reason_reflects_the_forced_condition(self):
        """When the HYBRID attempt succeeds, the degradation reason set by
        the Qdrant failure is left untouched -- it accurately describes why
        the engine is on HYBRID rather than HYBRID_QDRANT."""
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        engine._search_hybrid_qdrant = MagicMock(
            side_effect=ConnectionError("Qdrant Docker unreachable: timed out")
        )
        engine._search_hybrid = MagicMock(return_value=[])

        engine._search_with_fallback("query", top_k=5)

        assert "Qdrant search failed" in engine._degradation_reason
        assert "Qdrant Docker unreachable" in engine._degradation_reason

    def test_model_not_ready_is_a_temporary_stay_not_a_tier_drop(self):
        """The one RuntimeError message that does NOT demote the tier:
        "model not ready" means the FAISS/embedding model is still loading
        in the background init thread, so the current request is served
        from BM25 but the tier itself is left at HYBRID_QDRANT for the
        next request (see _search_with_fallback's RuntimeError branch).
        Unchanged by the N2 fix -- verified here against the real
        implementation to confirm the fix did not disturb it."""
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        engine._search_hybrid_qdrant = MagicMock(
            side_effect=RuntimeError("model not ready — encoding deferred to post-FAISS init")
        )
        bm25_results = [_result("b.md")]
        engine._search_bm25 = MagicMock(return_value=bm25_results)

        results = engine._search_with_fallback("query", top_k=5)

        assert results == bm25_results
        assert engine._tier == SearchTier.HYBRID_QDRANT  # NOT demoted
        assert "Qdrant search deferred" in engine._degradation_reason


class TestHybridQdrantAndHybridBothFailCascadesToBm25:
    """Both HYBRID_QDRANT's own dependency (Qdrant) AND the HYBRID tier's
    dependency (local FAISS/embedding) failing -- the case N2's fix must
    still resolve correctly: HYBRID is genuinely attempted (not skipped),
    and only falls to BM25 because it too failed, not because Qdrant alone
    failed."""

    def test_cascades_through_hybrid_to_bm25_when_both_fail(self):
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        engine._search_hybrid_qdrant = MagicMock(side_effect=ConnectionError("qdrant down"))
        engine._search_hybrid = MagicMock(side_effect=RuntimeError("embed failure: gpu oom"))
        bm25_results = [_result("c.md")]
        engine._search_bm25 = MagicMock(return_value=bm25_results)

        results = engine._search_with_fallback("query", top_k=5)

        assert results == bm25_results
        assert engine._tier == SearchTier.BM25
        # Both intermediate tiers were genuinely attempted, in order -- the
        # core N2 regression guard: HYBRID is not skipped.
        engine._search_hybrid_qdrant.assert_called_once_with("query", 5)
        engine._search_hybrid.assert_called_once_with("query", 5)
        engine._search_bm25.assert_called_once_with("query", 5)
        # The reported reason reflects the most proximate failure (HYBRID),
        # since that's what actually caused the final BM25 demotion.
        assert "Hybrid search failed" in engine._degradation_reason
        assert "gpu oom" in engine._degradation_reason


# ---------------------------------------------------------------------------
# HYBRID -> BM25 (embedding failure) -- unaffected by N2, still starts here
# ---------------------------------------------------------------------------


class TestHybridFailureDegradesToBM25:
    """HYBRID tier's own dependency -- the local FAISS index plus in-process
    embedding model / embedder-service -- failing (e.g. an embedding call
    error inside _search_semantic) must degrade to BM25 rather than
    raising. Engine starts directly at HYBRID (not reached via
    HYBRID_QDRANT), so N2's fix does not change this class's shape."""

    def test_search_still_returns_a_result_not_an_exception(self):
        engine = _make_engine(SearchTier.HYBRID)
        engine._search_hybrid = MagicMock(
            side_effect=RuntimeError(
                "embedder-service unavailable and in-process embedder not ready"
            )
        )
        bm25_results = [_result("c.md")]
        engine._search_bm25 = MagicMock(return_value=bm25_results)

        results = engine._search_with_fallback("query", top_k=5)

        assert results == bm25_results

    def test_tier_drops_to_bm25(self):
        engine = _make_engine(SearchTier.HYBRID)
        engine._search_hybrid = MagicMock(side_effect=RuntimeError("embed failure"))
        engine._search_bm25 = MagicMock(return_value=[])

        engine._search_with_fallback("query", top_k=5)

        assert engine._tier == SearchTier.BM25

    def test_degradation_reason_reflects_the_forced_condition(self):
        engine = _make_engine(SearchTier.HYBRID)
        engine._search_hybrid = MagicMock(side_effect=RuntimeError("embed failure: gpu oom"))
        engine._search_bm25 = MagicMock(return_value=[])

        engine._search_with_fallback("query", top_k=5)

        assert "Hybrid search failed" in engine._degradation_reason
        assert "embed failure: gpu oom" in engine._degradation_reason


# ---------------------------------------------------------------------------
# BM25 -> RAWFS (index unavailable)
# ---------------------------------------------------------------------------


class TestBm25FailureDegradesToRawfs:
    def test_search_still_returns_a_result_not_an_exception(self):
        engine = _make_engine(SearchTier.BM25)
        engine._search_bm25 = MagicMock(side_effect=RuntimeError("BM25 index corrupted"))
        rawfs_results = [_result("d.md")]
        engine._search_rawfs = MagicMock(return_value=rawfs_results)

        results = engine._search_with_fallback("query", top_k=5)

        assert results == rawfs_results

    def test_tier_drops_to_rawfs(self):
        engine = _make_engine(SearchTier.BM25)
        engine._search_bm25 = MagicMock(side_effect=RuntimeError("BM25 index corrupted"))
        engine._search_rawfs = MagicMock(return_value=[])

        engine._search_with_fallback("query", top_k=5)

        assert engine._tier == SearchTier.RAWFS

    def test_degradation_reason_reflects_the_forced_condition(self):
        engine = _make_engine(SearchTier.BM25)
        engine._search_bm25 = MagicMock(side_effect=RuntimeError("BM25 index corrupted"))
        engine._search_rawfs = MagicMock(return_value=[])

        engine._search_with_fallback("query", top_k=5)

        assert "BM25 search failed" in engine._degradation_reason
        assert "BM25 index corrupted" in engine._degradation_reason


class TestRawfsIsTheFloor:
    def test_rawfs_tier_calls_rawfs_directly_and_never_raises(self):
        engine = _make_engine(SearchTier.RAWFS)
        rawfs_results = [_result("e.md")]
        engine._search_rawfs = MagicMock(return_value=rawfs_results)

        results = engine._search_with_fallback("query", top_k=5)

        assert results == rawfs_results
        assert engine._tier == SearchTier.RAWFS  # nothing lower to fall to


class TestCascadingFailureReachesRawfsFloor:
    """Multiple dependencies down simultaneously (Qdrant AND local
    FAISS/Hybrid AND BM25) must still resolve to RAWFS results rather than
    raising or getting stuck partway down the chain. Explicitly stubs
    _search_hybrid too (unlike before the N2 fix, when it was never
    reached from HYBRID_QDRANT) so the full four-tier cascade is exercised
    deterministically end to end."""

    def test_every_tier_failing_still_returns_rawfs_results(self):
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        engine._search_hybrid_qdrant = MagicMock(side_effect=ConnectionError("qdrant down"))
        engine._search_hybrid = MagicMock(side_effect=RuntimeError("hybrid down"))
        engine._search_bm25 = MagicMock(side_effect=RuntimeError("bm25 down"))
        rawfs_results = [_result("f.md")]
        engine._search_rawfs = MagicMock(return_value=rawfs_results)

        results = engine._search_with_fallback("query", top_k=5)

        assert results == rawfs_results
        assert engine._tier == SearchTier.RAWFS
        # Confirms the cascade actually walked all four tiers in order,
        # rather than short-circuiting past any of them.
        engine._search_hybrid_qdrant.assert_called_once()
        engine._search_hybrid.assert_called_once()
        engine._search_bm25.assert_called_once()


# ---------------------------------------------------------------------------
# health_check()'s document_knowledge_base block
# ---------------------------------------------------------------------------


class TestHealthCheckReflectsSearchTierAndDegradationReason:
    """Exercises _document_kb_health_block() -- the function health_check()'s
    "document_knowledge_base" block delegates to -- against the module-level
    `engine` global, monkeypatched per test. Same technique
    _memory_instance_health_block_impl's docstring documents as what makes
    agent-memory's cross-server health_check comparison test possible.
    _document_kb_health_block() is a thin accessor over engine._tier /
    engine._degradation_reason -- it required no code change for N2, since
    it already reports whatever the (now-corrected) fallback chain leaves
    those two fields holding."""

    @pytest.mark.parametrize(
        "tier,reason",
        [
            (SearchTier.HYBRID_QDRANT, None),
            (SearchTier.HYBRID, "Qdrant Docker unreachable — falling back to FAISS: timed out"),
            (SearchTier.BM25, "Hybrid search failed: RuntimeError('embed failure')"),
            (SearchTier.RAWFS, "BM25 search failed: RuntimeError('bm25 corrupted')"),
        ],
    )
    def test_search_tier_and_degradation_reason_fields(self, monkeypatch, tier, reason):
        engine = _make_engine(tier)
        engine._degradation_reason = reason
        engine._qdrant_ready = False
        engine._qdrant_client = None
        monkeypatch.setattr(server, "engine", engine)

        block = server._document_kb_health_block()

        assert block["search_tier"] == tier.value
        assert block["degradation_reason"] == reason
        assert block["reachable"] is False  # qdrant_ready False in every case above

    def test_reachable_true_when_qdrant_client_healthy(self, monkeypatch):
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        client = MagicMock()
        client.get_collection.return_value = MagicMock(points_count=42)
        engine._qdrant_ready = True
        engine._qdrant_client = client
        monkeypatch.setattr(server, "engine", engine)

        block = server._document_kb_health_block()

        assert block["reachable"] is True
        assert block["point_count"] == 42

    def test_reachable_false_when_client_call_raises_despite_ready_flag(self, monkeypatch):
        """_qdrant_ready can be stale relative to actual live serviceability
        -- _document_kb_health_block does not simply trust the cached flag,
        it re-probes get_collections()/get_collection() live and reports
        reachable=False if that probe itself fails. Confirms
        workspace-knowledge's health_check does NOT have the same
        cached-snapshot staleness the benchmark assessment flagged for
        agent-memory (B2)."""
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        client = MagicMock()
        client.get_collections.side_effect = ConnectionError("qdrant just died")
        engine._qdrant_ready = True
        engine._qdrant_client = client
        monkeypatch.setattr(server, "engine", engine)

        block = server._document_kb_health_block()

        assert block["reachable"] is False

    def test_health_check_tool_surfaces_the_same_fields(self, monkeypatch):
        engine = _make_engine(SearchTier.BM25)
        engine._degradation_reason = "Hybrid search failed: simulated"
        monkeypatch.setattr(server, "engine", engine)
        # health_check() also computes memory_instance -- stub that path so
        # this test stays scoped to document_knowledge_base and doesn't
        # require a live qdrant-memory connection.
        monkeypatch.setattr(
            server, "_memory_instance_health_block", lambda: {"reachable": False}
        )

        result = server.health_check()

        assert result["document_knowledge_base"]["search_tier"] == "bm25"
        assert (
            result["document_knowledge_base"]["degradation_reason"]
            == "Hybrid search failed: simulated"
        )


# ---------------------------------------------------------------------------
# search_docs() tool wrapper
# ---------------------------------------------------------------------------


class TestSearchDocsToolNeverRaises:
    def test_returns_results_and_meta_reflecting_forced_tier(self, monkeypatch):
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        engine._search_hybrid_qdrant = MagicMock(side_effect=ConnectionError("qdrant down"))
        # Stubbed to fail too, so the tool-wrapper call deterministically
        # cascades all the way to BM25 in one call (N2: HYBRID is genuinely
        # attempted first, not skipped).
        engine._search_hybrid = MagicMock(side_effect=RuntimeError("hybrid down"))
        bm25_results = [_result("g.md")]
        engine._search_bm25 = MagicMock(return_value=bm25_results)
        monkeypatch.setattr(server, "engine", engine)

        result = server.search_docs(query="anything", top_k=5)

        assert result["results"] == bm25_results
        assert result["_meta"]["search_tier"] == "bm25"
        assert "Hybrid search failed" in result["_meta"]["degradation_reason"]

    def test_rawfs_floor_via_the_tool_wrapper(self, monkeypatch):
        engine = _make_engine(SearchTier.RAWFS)
        rawfs_results = [_result("h.md")]
        engine._search_rawfs = MagicMock(return_value=rawfs_results)
        monkeypatch.setattr(server, "engine", engine)

        result = server.search_docs(query="anything", top_k=5)

        assert result["results"] == rawfs_results
        assert result["_meta"]["search_tier"] == "rawfs"


# ---------------------------------------------------------------------------
# Recovery behavior
# ---------------------------------------------------------------------------


class TestRecoveryBehavior:
    """What the code actually does once the forced condition is lifted --
    verified against the real implementation rather than assumed (see
    module docstring FINDING). N3 (not yet fixed as of this commit) will
    replace test_no_automatic_recovery_on_next_call_once_demoted below with
    tests for a bounded, cooldown-gated re-probe -- see the module
    docstring's N3 finding."""

    def test_no_automatic_recovery_on_next_call_once_demoted(self):
        """Once _search_with_fallback demotes the tier, it never re-tries
        the higher tier on a later call, even if the underlying dependency
        would now succeed -- there is no re-probe/reconnect logic inside
        _search_with_fallback itself. N2's fix changed *which* tier a
        Qdrant failure demotes to (HYBRID, not BM25 -- see
        TestHybridQdrantFailureFallsToHybrid), but not this: once demoted,
        recovery is still one-directional until N3 lands."""
        engine = _make_engine(SearchTier.HYBRID_QDRANT)
        engine._search_hybrid_qdrant = MagicMock(side_effect=ConnectionError("qdrant down"))
        engine._search_hybrid = MagicMock(return_value=[])
        engine._search_bm25 = MagicMock(return_value=[])

        engine._search_with_fallback("query", top_k=5)
        assert engine._tier == SearchTier.HYBRID  # N2: demoted to HYBRID, not BM25

        # "Recover" the dependency -- it would now succeed if tried again.
        engine._search_hybrid_qdrant = MagicMock(return_value=[_result("i.md")])

        engine._search_with_fallback("query", top_k=5)

        assert engine._tier == SearchTier.HYBRID  # still demoted
        engine._search_hybrid_qdrant.assert_not_called()  # never retried

    def test_explicit_rebuild_restores_the_tier(self, tmp_path):
        """The only way the tier climbs back up is a full rebuild_index()
        call, which reruns _initialize_search_engine() from scratch.
        Verified here by stubbing that reinit chain (real BM25/FAISS/Qdrant
        work is out of scope for this suite -- see
        test_upsert_delete_ordering_fix.py and this file's own bypass
        pattern) and confirming rebuild() invokes it and adopts whatever
        tier it lands on. engine._INDEX_DIR is redirected to a tmp_path so
        this never touches the real embedding/ directory's on-disk FAISS
        state."""
        engine = _make_engine(SearchTier.BM25)
        engine._degradation_reason = "Qdrant search failed: simulated"
        engine._INDEX_DIR = tmp_path  # never touch the real embedding/ dir
        engine._init_thread = None

        def _fake_reinit():
            engine._tier = SearchTier.HYBRID_QDRANT
            engine._degradation_reason = None
            engine._init_thread = None

        engine._initialize_search_engine = _fake_reinit

        engine.rebuild()

        assert engine._tier == SearchTier.HYBRID_QDRANT
        assert engine._degradation_reason is None
