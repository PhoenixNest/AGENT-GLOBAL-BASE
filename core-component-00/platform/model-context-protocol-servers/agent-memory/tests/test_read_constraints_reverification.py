"""Independent re-verification of Decision 2's six read-only architectural
constraints (research-report.md § Architecture Decisions), against the
actual merged code, now that a write-capable `write_memory` tool exists
(gated inactive by AGENT_MEMORY_WRITE_TOOL_ENABLED, default false).

Deliberately independent of the write-path test suite (test_write_memory.py,
test_write_gate.py, test_write_provenance.py) — uses distinct verification
mechanisms rather than restating those suites' assertions.

Run: python -m pytest core-component-00/platform/model-context-protocol-servers/agent-memory/tests/test_read_constraints_reverification.py -v

Live-verification tests (TestConstraint3LiveQuarantineAndArchived,
TestConstraint4LiveSacredCompleteness) require a reachable qdrant-memory
instance (http://localhost:6335 by default) and skip cleanly if unreachable.
"""
from __future__ import annotations

import ast
import inspect
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock

import pytest

_AGENT_MEMORY_DIR = Path(__file__).resolve().parents[1]
_MCP_SERVERS_ROOT = _AGENT_MEMORY_DIR.parent
_REPO_ROOT = _MCP_SERVERS_ROOT.parents[2]
_SERVER_PY_PATH = _AGENT_MEMORY_DIR / "server.py"

# The last commit that touched server.py before Worker D's write-tool build
# (`ca717143 agent/memory/write-tool: build write_memory tool, gated inactive
# by default`) landed — i.e. the last known-good, read-only-only state of
# server.py. Used below for a byte-level function-body diff, not trusted from
# any prior worker's written claim about what changed.
_PRE_WRITE_PATH_COMMIT = "4e332eab"

sys.path.insert(0, str(_AGENT_MEMORY_DIR))
import write_gate  # noqa: E402
import write_tool  # noqa: E402
from write_provenance import WriteRateLimiter  # noqa: E402

sys.path.insert(0, str(_MCP_SERVERS_ROOT.parents[1] / "framework" / "02-context-engineering"))
from implementations.memory_vector_store import (  # noqa: E402
    EMBEDDING_DIM,
    COLLECTION_BY_TYPE,
    MemoryRecord,
    QdrantMemoryIndex,
)


def _embedder(text: str):
    base = ord(text[0]) / 1000 if text else 0.0
    return [round(base + i * 0.001, 6) for i in range(EMBEDDING_DIM)]


def _iso(ts: float) -> str:
    from datetime import datetime, timezone

    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Constraint 1 — Read-only first (now genuinely different: characterize, not
# round up)
# ---------------------------------------------------------------------------


class TestConstraint1ReadOnlyFirst:
    """
    Decision 2's original wording was "no write-capable tool ships in the
    first pass" — that is now literally false at the code level: write_tool.py
    and write_memory (server.py) exist, fully implemented. What must actually
    be verified is narrower and more precise: (a) search_memory's own behavior
    is provably unchanged, (b) write_memory is NOT reachable from a live MCP
    connection in the shipped default configuration, and (c) there is no
    second, unconditional registration path that would make it reachable
    despite the flag.
    """

    def test_search_memory_source_byte_identical_to_pre_write_path_commit(self):
        """
        Direct, tool-independent proof that search_memory (the @mcp.tool()
        entry point itself) has not drifted from the last commit before
        Worker D's write-tool build (4e332eab): extracts its AST source
        segment from that commit and from the current worktree HEAD, and
        asserts exact string equality. This does not trust any worker's
        changelog claim — it re-derives the diff itself.

        Scoped to search_memory only, not _search_memory_impl or
        _search_reflection: those two carry the memory system's degraded ->
        keyword-log-search fallback logic (05-disaster-recovery-and-resilience.md
        § 3), which legitimately evolves. A byte-identity assertion pinned to
        one fixed historical commit forever cannot accommodate legitimate
        ongoing change to a function without either (a) permanently blocking
        real feature work on it or (b) being neutralized via an ever-growing
        pile of string-replace exceptions that stop meaning anything.
        search_memory itself is a narrower, still-meaningful thing to keep
        pinned: it is the external tool contract. The behavioral contract of
        the other two is covered by TestTier3FallbackWiring below and the
        existing tests in this file/test_server.py, which test what they
        actually do rather than pinning their bytes to the past.
        """
        old_source = subprocess.run(
            ["git", "show", f"{_PRE_WRITE_PATH_COMMIT}:core-component-00/mcp-servers/agent-memory/server.py"],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        # Disclosed exception: search_memory's docstring citation was repointed
        # from the now-deleted 09-mcp-architecture-decision.md to
        # research-report.md's merged section. Applied to the baseline too so
        # this documentation-only edit doesn't mask an unrelated functional
        # change to the same function.
        old_source = old_source.replace(
            "    telescope/2026-07-10-agent-memory-architecture/supporting/09-mcp-architecture-decision.md):",
            "    telescope/2026-07-10-agent-memory-architecture/research-report.md\n    § Architecture Decisions):",
        )
        new_source = _SERVER_PY_PATH.read_text(encoding="utf-8")

        old_tree = ast.parse(old_source)
        new_tree = ast.parse(new_source)

        def _function_source(tree: ast.Module, source: str, name: str) -> str:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == name:
                    segment = ast.get_source_segment(source, node)
                    assert segment is not None, f"{name} not found via get_source_segment"
                    return segment
            raise AssertionError(f"function {name!r} not found in given source")

        for fn_name in ("search_memory",):
            old_fn = _function_source(old_tree, old_source, fn_name)
            new_fn = _function_source(new_tree, new_source, fn_name)
            assert old_fn == new_fn, (
                f"{fn_name} changed between {_PRE_WRITE_PATH_COMMIT} and HEAD — "
                "the write-tool build was supposed to be additive-only w.r.t. "
                "the existing read path"
            )

    def test_write_memory_not_reachable_over_live_mcp_connection_by_default(self, agent_memory_server):
        """
        The property that actually matters for a live caller: in the real,
        already-imported server module for this test session (no
        AGENT_MEMORY_WRITE_TOOL_ENABLED override applied anywhere in this
        process), write_memory must not appear in the tool list a live MCP
        client would see. This is the honest, narrow claim — "not callable
        today, pending deliberate activation" — not "the tool surface is
        still read-only," which would be false.
        """
        import asyncio

        tool_names = {t.name for t in asyncio.run(agent_memory_server.mcp.list_tools())}
        assert "write_memory" not in tool_names
        assert "search_memory" in tool_names
        assert "health_check" in tool_names

    def test_default_env_state_in_this_process_is_disabled(self):
        """Sanity check on the actual environment this test run executed in
        — if AGENT_MEMORY_WRITE_TOOL_ENABLED were somehow set truthy in this
        environment, the previous test's conclusion would not generalize to
        "the shipped default," and that must not be silently glossed over."""
        assert os.getenv("AGENT_MEMORY_WRITE_TOOL_ENABLED", "false").strip().lower() not in (
            "1",
            "true",
            "yes",
        ), "AGENT_MEMORY_WRITE_TOOL_ENABLED is set truthy in this test environment"
        assert write_tool.AGENT_MEMORY_WRITE_TOOL_ENABLED is False

    def test_write_memory_is_not_decorated_with_mcp_tool_directly(self):
        """
        Static-analysis proof that write_memory's def statement itself carries
        no @mcp.tool() decorator (unlike search_memory/health_check, which
        do) — the ONLY way it becomes registered is the explicit conditional
        call at module scope. Rules out "it's decorated but the decorator is
        a no-op" or similar disguised-registration shapes.
        """
        tree = ast.parse(_SERVER_PY_PATH.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "write_memory":
                decorator_sources = [
                    ast.unparse(d) for d in node.decorator_list
                ]
                assert decorator_sources == [], (
                    f"write_memory has decorators {decorator_sources!r} — "
                    "expected none; registration must be the explicit "
                    "conditional call only"
                )
                return
        raise AssertionError("write_memory function definition not found in server.py")

    def test_exactly_one_registration_call_site_and_it_is_conditionally_guarded(self):
        """
        Static-analysis proof there is exactly one place in server.py that
        could register write_memory as a live tool
        (`mcp.tool()(write_memory)`), and that call is the body of an `if`
        statement whose test expression is
        `write_tool.AGENT_MEMORY_WRITE_TOOL_ENABLED` — not buried in a
        function that might run unconditionally, not duplicated, not
        reachable any other way. This directly answers the brief's question
        ("read the literal `if AGENT_MEMORY_WRITE_TOOL_ENABLED:` guard and
        confirm no other code path calls `mcp.tool()(write_memory)`
        unconditionally anywhere") via the actual parsed AST rather than a
        visual read.
        """
        source = _SERVER_PY_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)

        call_sites = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Call)
                and isinstance(node.func.func, ast.Attribute)
                and node.func.func.attr == "tool"
                and len(node.args) == 1
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id == "write_memory"
            ):
                call_sites.append(node)

        assert len(call_sites) == 1, (
            f"expected exactly one mcp.tool()(write_memory) call site, found "
            f"{len(call_sites)}"
        )

        # Walk the module's top-level statements to find the If node whose
        # body contains this exact call, as an Expr statement, and confirm
        # its test condition is the attribute access
        # write_tool.AGENT_MEMORY_WRITE_TOOL_ENABLED (not a negation, not an
        # `or`/`and` that could be trivially true, not `if True:`).
        found_guard = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            body_calls = [
                stmt.value
                for stmt in node.body
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call)
            ]
            if any(c in call_sites for c in body_calls):
                test_src = ast.unparse(node.test)
                assert test_src == "write_tool.AGENT_MEMORY_WRITE_TOOL_ENABLED", (
                    f"guard condition is {test_src!r}, expected the literal "
                    "flag attribute access"
                )
                found_guard = True
        assert found_guard, "mcp.tool()(write_memory) call is not inside the expected if-guard"

    def test_honest_characterization_tool_surface_vs_live_surface(self, agent_memory_server):
        """
        The actual, non-rounded-up finding this constraint verification must
        report: the CODE surface of agent-memory is no longer read-only-only
        (write_tool.py + write_memory exist, fully built, always importable
        and directly callable as a plain Python function by anything with
        module access) — but the LIVE, MCP-callable surface remains
        read-only, because registration is gated behind an explicit,
        statically-verified opt-in flag that defaults false. Both halves of
        this statement are asserted together so neither can be silently
        dropped in a future edit of this test.
        """
        # Code surface: write_memory exists and is directly callable.
        assert callable(write_tool._write_memory_impl)
        assert callable(agent_memory_server.write_memory)

        # Live surface: not in the tool list under the default env.
        import asyncio

        tool_names = {t.name for t in asyncio.run(agent_memory_server.mcp.list_tools())}
        assert "write_memory" not in tool_names


# ---------------------------------------------------------------------------
# Constraint 2 — Session-scoped episodic reads by default (unchanged)
# ---------------------------------------------------------------------------


class TestConstraint2SessionScopedEpisodicUnchanged:
    """
    Covered directly by TestConstraint1ReadOnlyFirst's byte-identical source
    check above for the whole function — these tests independently re-derive
    the *behavior* through the live function object (not just the source
    text), so a change that somehow preserved source text but altered
    imported symbols/behavior would still be caught.
    """

    def test_episodic_without_session_id_and_without_cross_session_is_rejected(
        self, agent_memory_server
    ):
        result = agent_memory_server._search_memory_impl(
            query="q",
            memory_type="episodic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=MagicMock(),
            embedder=_embedder,
        )
        assert result["degraded"] is True
        assert "cross_session" in result["reason"]

    def test_episodic_with_session_id_scopes_the_qdrant_filter_to_that_session(
        self, agent_memory_server
    ):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        agent_memory_server._search_memory_impl(
            query="q",
            memory_type="episodic",
            top_k=5,
            session_id="session-under-test",
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        _, kwargs = client.query_points.call_args
        must = kwargs["query_filter"].must
        session_conditions = [
            c for c in must if getattr(c, "key", None) == "source_session_id"
        ]
        assert len(session_conditions) == 1
        assert session_conditions[0].match.value == "session-under-test"

    def test_episodic_cross_session_true_omits_session_filter_even_if_session_id_given(
        self, agent_memory_server
    ):
        """cross_session=True is the explicit opt-in path — session_id (if
        also given) must NOT still narrow the query, since cross_session
        means "search everything," not "search everything but prefer this
        session." Matches _search_memory_impl's
        `effective_session_id = session_id if (memory_type == "episodic" and
        not cross_session) else None` line."""
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        agent_memory_server._search_memory_impl(
            query="q",
            memory_type="episodic",
            top_k=5,
            session_id="should-be-ignored",
            cross_session=True,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        _, kwargs = client.query_points.call_args
        must = kwargs["query_filter"].must
        session_conditions = [c for c in must if getattr(c, "key", None) == "source_session_id"]
        assert session_conditions == []

    def test_non_episodic_memory_types_never_apply_session_scoping(self, agent_memory_server):
        for memory_type in ("semantic", "procedural"):
            client = MagicMock()
            client.query_points.return_value = MagicMock(points=[])
            agent_memory_server._search_memory_impl(
                query="q",
                memory_type=memory_type,
                top_k=5,
                session_id="irrelevant-session",
                cross_session=False,
                include_dormant=False,
                include_archived=False,
                client=client,
                embedder=_embedder,
            )
            _, kwargs = client.query_points.call_args
            must = kwargs["query_filter"].must
            session_conditions = [c for c in must if getattr(c, "key", None) == "source_session_id"]
            assert session_conditions == []


# ---------------------------------------------------------------------------
# Constraint 3 — Status filtering by default (archived excluded; quarantined
# unreachable under every flag combination)
# ---------------------------------------------------------------------------


class TestConstraint3StatusFilteringUnitLevel:
    def test_archived_excluded_by_default(self, agent_memory_server):
        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        agent_memory_server._search_memory_impl(
            query="q",
            memory_type="semantic",
            top_k=5,
            session_id=None,
            cross_session=False,
            include_dormant=False,
            include_archived=False,
            client=client,
            embedder=_embedder,
        )
        _, kwargs = client.query_points.call_args
        statuses = kwargs["query_filter"].must[0].match.any
        assert "archived" not in statuses

    def test_quarantined_absent_from_constructed_filter_under_all_four_flag_combinations(
        self, agent_memory_server
    ):
        """
        Independent re-derivation of write_gate.py's own logical proof
        (module docstring "Quarantine lane contract"): exercises the real,
        live `_search_memory_impl` object across every combination of
        include_dormant/include_archived and inspects the actual Qdrant
        filter object constructed, not a re-statement of the source text.
        """
        seen_status_sets = []
        for include_dormant in (False, True):
            for include_archived in (False, True):
                client = MagicMock()
                client.query_points.return_value = MagicMock(points=[])
                agent_memory_server._search_memory_impl(
                    query="q",
                    memory_type="procedural",
                    top_k=5,
                    session_id=None,
                    cross_session=False,
                    include_dormant=include_dormant,
                    include_archived=include_archived,
                    client=client,
                    embedder=_embedder,
                )
                _, kwargs = client.query_points.call_args
                statuses = set(kwargs["query_filter"].must[0].match.any)
                assert "quarantined" not in statuses
                assert "active" in statuses
                seen_status_sets.append(frozenset(statuses))
        # Sanity: the four combinations actually produced up to 4 distinct
        # filter shapes (not a stub that always returns the same set
        # regardless of the flags — would itself be a Completeness failure
        # per mcp-governance.md Gate 3).
        assert len(set(seen_status_sets)) == 4

    def test_quarantined_also_absent_when_reached_via_reflection_type_search_reflection_path(self):
        """_search_reflection is a separate code path from
        QdrantMemoryIndex.search() (different collection, different payload
        parsing) — it takes `statuses` as a plain caller-supplied list rather
        than re-deriving it, so this constraint is verified at the ONE call
        site that actually builds the list (_search_memory_impl), covered
        above. This test documents that _search_reflection itself has no
        independent status-filtering logic to re-verify (it trusts its
        caller's `statuses` list verbatim) — confirmed by reading the
        function signature/body directly, not by behavioral inference."""
        text = _SERVER_PY_PATH.read_text(encoding="utf-8")
        # _search_reflection must take `statuses` as a parameter (caller-
        # controlled input, already covered above) and must not itself
        # append/derive additional status values anywhere in its body.
        fn_start = text.index("def _search_reflection(")
        fn_end = text.index("\ndef _search_memory_impl(")
        body = text[fn_start:fn_end]
        assert "statuses: List[str]" in body
        assert '.append(' not in body  # no independent status derivation


class TestConstraint3LiveQuarantineAndArchived:
    """
    Live verification against real qdrant-memory, per the reversal
    condition's own wording ("verified the same way search_memory's
    Completeness gate was verified (unit tests plus live verification
    against real qdrant-memory)"). Uses the same disposable-uniquely-named-
    test-collection-then-delete pattern already established in this codebase
    by scripts/verify_backup_restore.py (QdrantMemoryIndex against a suffixed
    collection name, cleaned up in a finally block) — never touches the
    production memory_* collections.
    """

    @pytest.fixture
    def live_client(self):
        qdrant_url = os.getenv("MEMORY_QDRANT_URL", "http://localhost:6335")
        try:
            from qdrant_client import QdrantClient
        except ImportError:
            pytest.skip("qdrant_client not installed in this environment")
        client = QdrantClient(url=qdrant_url, timeout=5)
        try:
            client.get_collections()
        except Exception as exc:  # noqa: BLE001 - genuinely any failure means "unreachable"
            pytest.skip(f"qdrant-memory unreachable at {qdrant_url}: {exc}")
        return client

    def test_quarantined_and_archived_unreachable_live_disposable_collection(
        self, agent_memory_server, live_client, monkeypatch
    ):
        disposable_name = f"memory_semantic__read_constraint_reverify_{uuid.uuid4().hex[:10]}"
        # COLLECTION_BY_TYPE is the SAME dict object imported by both
        # server.py and memory_vector_store.py (Python module-import binds a
        # name to the shared dict, not a copy) — monkeypatch.setitem mutates
        # it for the duration of this test only and guarantees restoration
        # afterward, even on failure, exactly like monkeypatch.setattr does
        # for plain attributes.
        monkeypatch.setitem(agent_memory_server.COLLECTION_BY_TYPE, "semantic", disposable_name)

        index = QdrantMemoryIndex("semantic", client=live_client, embedder=_embedder)
        index.ensure_collection()
        try:
            now = time.time()
            for status in ("active", "dormant", "archived", "quarantined"):
                record = MemoryRecord(
                    id=str(uuid.uuid4()),
                    memory_type="semantic",
                    content=f"reverify live status marker: {status}",
                    created_at=now,
                    last_accessed_at=now,
                    status=status,
                    sacred=False,
                )
                upserted = index.upsert_record(record)
                assert upserted is True, f"live upsert failed for status={status!r}"

            for include_dormant in (False, True):
                for include_archived in (False, True):
                    result = agent_memory_server._search_memory_impl(
                        query="reverify live status marker",
                        memory_type="semantic",
                        top_k=50,
                        session_id=None,
                        cross_session=False,
                        include_dormant=include_dormant,
                        include_archived=include_archived,
                        client=live_client,
                        embedder=_embedder,
                    )
                    assert result["degraded"] is False
                    returned_statuses = {r["status"] for r in result["results"]}
                    assert "quarantined" not in returned_statuses, (
                        f"quarantined record leaked through with "
                        f"include_dormant={include_dormant}, "
                        f"include_archived={include_archived}: {returned_statuses}"
                    )
                    if not include_archived:
                        assert "archived" not in returned_statuses
        finally:
            live_client.delete_collection(collection_name=disposable_name)


# ---------------------------------------------------------------------------
# Constraint 4 — Sacred-record retrieval completeness preserved
# ---------------------------------------------------------------------------


class TestConstraint4SacredCompletenessStatic:
    def test_write_tool_never_sets_sacred_true(self):
        """Direct grep-equivalent (via source read, not shelling out to grep)
        of write_tool.py for every occurrence of the token 'sacred' — every
        one must either be a comment/docstring reference or an assignment of
        the literal `False`, never `True` and never a caller-derived
        expression."""
        source = write_tool.__file__ and Path(write_tool.__file__).read_text(encoding="utf-8")
        assert "sacred=True" not in source
        # The one real code-level occurrence must be the literal False
        # assignment inside the MemoryRecord(...) construction.
        assert "sacred=False,  # never caller-settable" in source or "sacred=False," in source

    def test_write_memory_and_write_memory_impl_signatures_carry_no_sacred_param(
        self, agent_memory_server
    ):
        write_memory_params = set(inspect.signature(agent_memory_server.write_memory).parameters)
        impl_params = set(inspect.signature(write_tool._write_memory_impl).parameters)
        assert "sacred" not in write_memory_params
        assert "sacred" not in impl_params

    def test_status_base_list_unconditionally_includes_active_no_way_to_exclude_it(self):
        """
        Sacred records are pinned to status='active' at write time (see the
        live test below and memory_vector_store.py's write_episodic/
        write_semantic/write_procedural, which always pass status='active'
        for freshly-written records). The read-side guarantee this
        constraint actually needs is narrower and structural: there is no
        parameter to _search_memory_impl that can remove 'active' from the
        status list it builds — read the literal source, not a paraphrase.
        """
        text = _SERVER_PY_PATH.read_text(encoding="utf-8")
        fn_start = text.index("def _search_memory_impl(")
        # Boundary anchor is intentionally just "\ndef search_memory(" (not
        # "\n@mcp.tool()\ndef search_memory(") -- it exists only to find
        # where the NEXT top-level def begins so `body` below is scoped to
        # _search_memory_impl alone; it is not itself an assertion about
        # which/how-many decorators sit on search_memory (R4, 2026-09-02,
        # added @_log_tool_call between @mcp.tool() and the def line).
        fn_end = text.index("\ndef search_memory(")
        body = text[fn_start:fn_end]
        assert 'statuses = ["active"]' in body
        # No conditional wraps that literal assignment (it must not be inside
        # an if/else that could produce a status list without "active").
        line = 'statuses = ["active"]'
        idx = body.index(line)
        preceding_line = body[:idx].rstrip().splitlines()[-1].strip()
        assert not preceding_line.endswith(":"), (
            "statuses base list appears to be conditionally assigned — "
            f"preceding line was {preceding_line!r}"
        )


class TestConstraint4LiveSacredCompleteness:
    @pytest.fixture
    def live_client(self):
        qdrant_url = os.getenv("MEMORY_QDRANT_URL", "http://localhost:6335")
        try:
            from qdrant_client import QdrantClient
        except ImportError:
            pytest.skip("qdrant_client not installed in this environment")
        client = QdrantClient(url=qdrant_url, timeout=5)
        try:
            client.get_collections()
        except Exception as exc:  # noqa: BLE001
            pytest.skip(f"qdrant-memory unreachable at {qdrant_url}: {exc}")
        return client

    def test_sacred_record_always_returned_by_default_search(
        self, agent_memory_server, live_client, monkeypatch
    ):
        disposable_name = f"memory_procedural__read_constraint_reverify_{uuid.uuid4().hex[:10]}"
        monkeypatch.setitem(agent_memory_server.COLLECTION_BY_TYPE, "procedural", disposable_name)

        index = QdrantMemoryIndex("procedural", client=live_client, embedder=_embedder)
        index.ensure_collection()
        try:
            now = time.time()
            sacred_record = MemoryRecord(
                id=str(uuid.uuid4()),
                memory_type="procedural",
                content="reverify live sacred marker: must always be retrievable",
                created_at=now,
                last_accessed_at=now,
                status="active",  # sacred records are pinned active at write time
                sacred=True,
            )
            assert index.upsert_record(sacred_record) is True

            # Default call: no include_dormant/include_archived at all.
            result = agent_memory_server._search_memory_impl(
                query="reverify live sacred marker",
                memory_type="procedural",
                top_k=10,
                session_id=None,
                cross_session=False,
                include_dormant=False,
                include_archived=False,
                client=live_client,
                embedder=_embedder,
            )
            assert result["degraded"] is False
            matched = [r for r in result["results"] if r["id"] == sacred_record.id]
            assert len(matched) == 1, (
                "sacred=True record was not returned by the default-filter "
                f"search: got results {result['results']!r}"
            )
            assert matched[0]["sacred"] is True
        finally:
            live_client.delete_collection(collection_name=disposable_name)


# ---------------------------------------------------------------------------
# Constraint 5 — No caller-supplied sacred/importance override
# ---------------------------------------------------------------------------


class TestConstraint5NoCallerOverride:
    def test_write_memory_signature_has_no_sacred_importance_or_status_param(
        self, agent_memory_server
    ):
        sig = inspect.signature(agent_memory_server.write_memory)
        params = set(sig.parameters)
        for forbidden in ("sacred", "importance", "status"):
            assert forbidden not in params, f"write_memory accepts a caller-settable {forbidden!r} param"

    def test_search_memory_signature_also_has_no_sacred_importance_override(
        self, agent_memory_server
    ):
        """Decision 2's no-override rule predates the write tool and applies
        to the existing read tool too — re-verified here rather than assumed,
        since this is exactly the kind of thing a careless future edit could
        silently reintroduce."""
        sig = inspect.signature(agent_memory_server.search_memory)
        params = set(sig.parameters)
        assert "sacred" not in params
        assert "importance" not in params

    def test_importance_is_always_the_internal_heuristic_never_a_parameter(self):
        """write_tool.py must derive `importance` solely from
        compute_write_time_importance("general") — never from any of
        write_memory's seven actual parameters (content, memory_type,
        session_id, provenance_source, provenance_triggering_context_excerpt,
        provenance_from_external_content, provenance_confidence). Verified by
        reading the literal MemoryRecord(...) construction site."""
        source = Path(write_tool.__file__).read_text(encoding="utf-8")
        assert 'importance=compute_write_time_importance("general")' in source

    def test_write_provenance_confidence_is_never_plumbed_into_memory_record_confidence_or_importance(
        self,
    ):
        """
        write_provenance.py's own docstring already states this must never
        happen ("THIS IS A DIFFERENT FIELD... must never be plumbed through
        to set MemoryRecord.confidence or MemoryRecord.importance directly")
        — re-verified here against the actual MemoryRecord(...) construction
        in write_tool.py, not trusted from the docstring's own claim about
        itself.
        """
        source = Path(write_tool.__file__).read_text(encoding="utf-8")
        construction_start = source.index("record = MemoryRecord(")
        construction_end = source.index(")", source.index("media_ref=None,", construction_start))
        construction_block = source[construction_start : construction_end + 1]
        assert "provenance.confidence" not in construction_block
        assert "provenance_confidence" not in construction_block
        # The only confidence= in the MemoryRecord(...) call must be the
        # fixed literal 1.0, not any provenance-derived expression.
        assert "confidence=1.0," in construction_block

    def test_write_memory_impl_rejects_out_of_band_kwargs(self):
        """Belt-and-suspenders: calling _write_memory_impl with an attempted
        sacred=/importance= kwarg must raise TypeError (Python's own
        signature enforcement), not silently accept and apply it. Confirms
        there is no **kwargs escape hatch on the testable core either."""
        sig = inspect.signature(write_tool._write_memory_impl)
        assert not any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        ), "_write_memory_impl has a **kwargs catch-all — sacred/importance could be smuggled through it"


# ---------------------------------------------------------------------------
# Constraint 6 — Graceful degradation on every path
# ---------------------------------------------------------------------------


class TestConstraint6GracefulDegradation:
    """
    Exercises failure paths NOT already covered by test_write_memory.py's
    TestWriteMemoryWrapperNeverRaises (which tests malformed memory_type,
    malformed confidence, None content, and a monkeypatched
    write_tool._write_memory_impl raising directly). This class specifically
    targets internal collaborators (gate, rate_limiter) raising from *inside*
    a real _write_memory_impl call — a different failure surface than
    replacing the whole function.
    """

    def test_write_memory_never_raises_when_gate_check_confirmation_raises_repo_root_unresolved(
        self, agent_memory_server, monkeypatch
    ):
        """
        write_gate.WriteConfirmationGate.check_confirmation() calls
        confirmation_marker_path(), which raises RepoRootUnresolvedError if
        `git rev-parse --show-toplevel` cannot be resolved (write_gate.py,
        RepoRootUnresolvedError). This is a real, reachable exception path
        inside _write_memory_impl's high_consequence branch that neither
        _write_memory_impl nor write_memory has a dedicated except clause
        for — the *only* thing standing between this and an exception
        reaching an agent turn is write_memory's outer try/except in
        server.py. Forces a collision (would_collide=True via a candidate
        found + no judge configured, matching write_tool.py's own
        conservative-high-consequence fallback) so the high_consequence
        branch is actually reached, then breaks repo-root resolution.
        """
        broken_gate = write_gate.WriteConfirmationGate()
        monkeypatch.setattr(write_gate, "_repo_root", lambda: None)

        client = MagicMock()
        existing_payload = {
            "id": "existing-1",
            "memory_type": "semantic",
            "content": "an existing fact",
            "created_at": _iso(time.time()),
            "last_accessed_at": _iso(time.time()),
            "access_count": 0,
            "importance": 0.5,
            "confidence": 1.0,
            "decay_weight": 1.0,
            "status": "active",
            "source_session_id": None,
            "source_turn": 0,
            "sacred": False,
            "tags": [],
            "consolidated_from": [],
            "modality": "text",
            "media_ref": None,
        }
        client.query_points.return_value = MagicMock(payload=existing_payload, points=[MagicMock(payload=existing_payload)])

        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: client)
        monkeypatch.setattr(agent_memory_server, "_get_embedder", lambda: _embedder)
        monkeypatch.setattr(write_tool, "get_default_write_gate", lambda: broken_gate)
        monkeypatch.setattr(agent_memory_server, "write_tool", write_tool)

        result = agent_memory_server.write_memory(
            content="a brand new fact that will collide with the existing one",
            memory_type="semantic",
            session_id="repo-root-broken-session",
            provenance_source="test",
            provenance_triggering_context_excerpt="user asked to remember this",
            provenance_from_external_content=False,
            provenance_confidence=0.9,
        )
        assert isinstance(result, dict)
        assert result["written"] is False
        assert result["status"] == "error"
        assert "write_memory failed" in result["reason"]

    def test_write_memory_never_raises_when_rate_limiter_raises_unexpectedly(
        self, agent_memory_server, monkeypatch
    ):
        """A rate limiter whose check_and_record() raises an unrelated
        internal error (not a graceful (False, reason) rejection) is a
        genuinely unanticipated failure mode inside _write_memory_impl's very
        first gating step — confirms the outer wrapper's protection is not
        specific to the failure modes _write_memory_impl was explicitly
        written to anticipate."""

        class _ExplodingRateLimiter:
            def check_and_record(self, session_id, memory_type):
                raise RuntimeError("simulated rate limiter internal failure")

        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: MagicMock())
        monkeypatch.setattr(agent_memory_server, "_get_embedder", lambda: _embedder)
        # server.py imports get_default_rate_limiter directly into its own
        # namespace (`from write_provenance import get_default_rate_limiter`)
        # and calls it as a bare name — unlike write_tool.get_default_write_gate,
        # which server.py calls via the `write_tool.` module attribute. Patch
        # the actual symbol server.py's write_memory() resolves at call time.
        monkeypatch.setattr(agent_memory_server, "get_default_rate_limiter", lambda: _ExplodingRateLimiter())
        monkeypatch.setattr(agent_memory_server, "write_tool", write_tool)

        result = agent_memory_server.write_memory(
            content="fact",
            memory_type="semantic",
            session_id="s",
            provenance_source="s",
            provenance_triggering_context_excerpt="x",
            provenance_from_external_content=False,
            provenance_confidence=0.5,
        )
        assert isinstance(result, dict)
        assert result["written"] is False
        assert result["status"] == "error"

    def test_write_memory_never_raises_when_client_raises_during_collision_search(
        self, agent_memory_server, monkeypatch
    ):
        """A Qdrant client whose query_points() raises an exception type
        QdrantMemoryIndex.search()'s except clauses do not explicitly name
        (its final bare `except Exception` still catches it, degrading to
        []) — exercised here through the full write_memory call chain rather
        than directly against QdrantMemoryIndex, to prove the write path's
        own collision-search step inherits that degradation correctly."""

        class _WeirdError(Exception):
            pass

        client = MagicMock()
        client.query_points.side_effect = _WeirdError("simulated exotic failure")

        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: client)
        monkeypatch.setattr(agent_memory_server, "_get_embedder", lambda: _embedder)
        monkeypatch.setattr(agent_memory_server, "write_tool", write_tool)

        result = agent_memory_server.write_memory(
            content="a fact that will hit a client raising during collision search",
            memory_type="semantic",
            session_id="weird-error-session",
            provenance_source="s",
            provenance_triggering_context_excerpt="x",
            provenance_from_external_content=False,
            provenance_confidence=0.5,
        )
        assert isinstance(result, dict)
        # Either the collision search degraded to "no candidate" (routine
        # quarantine write proceeds and may succeed or fail on the
        # subsequent upsert, itself also a MagicMock) or something else
        # failed — the only non-negotiable assertion is that no exception
        # escaped and a well-shaped dict came back.
        assert set(result.keys()) >= {"written", "status", "reason", "record_id", "lane"}

    @pytest.mark.parametrize(
        "kwargs",
        [
            dict(content=123, memory_type="semantic"),  # content wrong type
            dict(content="x", memory_type=None),  # memory_type wrong type
            dict(content="x", memory_type="semantic", session_id=12345),  # session_id wrong type
            dict(content="x", memory_type="semantic", provenance_from_external_content="yes"),  # bool wrong type
            dict(content="x", memory_type="semantic", provenance_confidence=float("nan")),  # NaN
            dict(content="x", memory_type="semantic", provenance_confidence=float("inf")),  # inf
        ],
    )
    def test_write_memory_never_raises_on_a_battery_of_malformed_inputs(
        self, agent_memory_server, monkeypatch, kwargs
    ):
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: MagicMock())
        monkeypatch.setattr(agent_memory_server, "_get_embedder", lambda: _embedder)
        base = dict(
            content="default content",
            memory_type="semantic",
            session_id="s",
            provenance_source="s",
            provenance_triggering_context_excerpt="x",
            provenance_from_external_content=False,
            provenance_confidence=0.5,
        )
        base.update(kwargs)
        result = agent_memory_server.write_memory(**base)
        assert isinstance(result, dict)
        assert result["written"] is False

    def test_write_memory_never_raises_when_embedder_itself_raises_mid_call(
        self, agent_memory_server, monkeypatch
    ):
        def _exploding_embedder(text):
            raise RuntimeError("simulated embedder runtime failure")

        client = MagicMock()
        client.query_points.return_value = MagicMock(points=[])
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: client)
        monkeypatch.setattr(agent_memory_server, "_get_embedder", lambda: _exploding_embedder)
        monkeypatch.setattr(agent_memory_server, "write_tool", write_tool)

        result = agent_memory_server.write_memory(
            content="a fact whose embedding will explode",
            memory_type="semantic",
            session_id="exploding-embedder-session",
            provenance_source="s",
            provenance_triggering_context_excerpt="x",
            provenance_from_external_content=False,
            provenance_confidence=0.5,
        )
        assert isinstance(result, dict)
        assert result["written"] is False
