"""
Executable pytest suite for the Investigator-Authored Write Path's identity
enforcement (implementations/reflection_authoring.py).

Closes the Independent Safety Self-Review's §2.2 (Dr. Wieczorek's Open
finding: a non-empty-string check on `logged_by` is a formatting check, not
identity verification) AND the follow-up finding MISTAKE-2026-07-16-001
(both recorded in core-component-00/telescope/2026-07-14-reflexion-memory-system/
research-report.md § Audit History): the two-factor git-identity +
roster-name check alone does not distinguish a human operator from a
co-located AI agent process. These tests exercise:

  1. The two-factor mechanism itself: an authenticated git identity read
     from git config (never from a caller-supplied argument), independently
     checked against the module-level AUTHORIZED_GIT_IDENTITIES constant,
     AND a `logged_by` value independently checked against the module-level
     AUTHORIZED_INVESTIGATOR_NAMES constant (the CC-00 Laboratory Roster).
     Neither allowlist is a caller-overridable function parameter — tests
     monkeypatch the module-level constants directly.
  2. ReflectionMemory.record_reflection()'s and PersistentMemorySink.
     write_reflection()'s IdentityVerification gates (closing the
     direct-import and direct-sink-call bypasses) are covered in
     test_reflection_memory.py, not duplicated here.
  3. require_governance_confirmation()'s TTY-required, typed-confirmation
     gate for GOVERNANCE_TRIGGERS record types — both its rejection cases
     (non-TTY stdin, wrong typed confirmation) and its acceptance case,
     including that it returns the confirmed reflection_id so
     author_reflection() can fold it into the IdentityVerification token
     (the composition-gap fix — see TestAuthorReflectionEndToEnd's
     assertion on IdentityVerification.governance_confirmation).

Each git-identity test constructs its own throwaway git repository under
tmp_path and points GIT_CONFIG_GLOBAL/GIT_CONFIG_SYSTEM at nonexistent
files, so these tests never read (and can never be affected by) the real
developer machine's actual global git configuration.

Run with:
    pytest testing/test_reflection_authoring.py -v
"""

import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import implementations.reflection_authoring as ra
from implementations.reflection_authoring import (
    AUTHORIZED_GIT_IDENTITIES,
    AUTHORIZED_INVESTIGATOR_NAMES,
    HumanConfirmationRequiredError,
    IdentityError,
    IdentityVerification,
    UnverifiedReflectionError,
    _build_default_sink,
    _load_shared_embedder,
    author_reflection,
    get_authenticated_git_identity,
    require_governance_confirmation,
    verify_authorized_identity,
)


def _isolated_env(tmp_path):
    """An environment where git config resolution cannot see the real
    developer machine's global/system config — only whatever this test
    explicitly sets in the throwaway repo's local .git/config."""
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = str(tmp_path / "nonexistent-global-gitconfig")
    env["GIT_CONFIG_SYSTEM"] = str(tmp_path / "nonexistent-system-gitconfig")
    return env


def _init_repo(tmp_path, name=None, email=None):
    repo = tmp_path / "repo"
    repo.mkdir()
    env = _isolated_env(tmp_path)
    subprocess.run(["git", "init"], cwd=repo, env=env, capture_output=True, check=True)
    if name is not None:
        subprocess.run(["git", "config", "user.name", name], cwd=repo, env=env, check=True)
    if email is not None:
        subprocess.run(["git", "config", "user.email", email], cwd=repo, env=env, check=True)
    return repo, env


# ---------------------------------------------------------------------------
# get_authenticated_git_identity — reads real git config, isolated per test
# ---------------------------------------------------------------------------

class TestGetAuthenticatedGitIdentity:
    def test_reads_configured_local_identity(self, tmp_path):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        identity = get_authenticated_git_identity(cwd=str(repo), env=env)
        assert identity == ("Test Investigator", "test@example.com")

    def test_raises_when_name_and_email_unset(self, tmp_path):
        repo, env = _init_repo(tmp_path)  # no user.name / user.email set anywhere
        with pytest.raises(IdentityError):
            get_authenticated_git_identity(cwd=str(repo), env=env)

    def test_raises_when_only_name_set(self, tmp_path):
        repo, env = _init_repo(tmp_path, name="Only Name")
        with pytest.raises(IdentityError):
            get_authenticated_git_identity(cwd=str(repo), env=env)

    def test_raises_when_only_email_set(self, tmp_path):
        repo, env = _init_repo(tmp_path, email="only@example.com")
        with pytest.raises(IdentityError):
            get_authenticated_git_identity(cwd=str(repo), env=env)


# ---------------------------------------------------------------------------
# verify_authorized_identity — the full two-factor gate
# ---------------------------------------------------------------------------

def _patch_allowlists(monkeypatch, git_identities=None, investigator_names=None):
    """Monkeypatch the module-level allowlist constants directly — the
    standard pytest pattern this module's tests now use in place of the
    removed authorized_git_identities/authorized_investigator_names
    function parameters (that surface was itself a second, compounding gap:
    see this module's docstring)."""
    if git_identities is not None:
        monkeypatch.setattr(ra, "AUTHORIZED_GIT_IDENTITIES", set(git_identities))
    if investigator_names is not None:
        monkeypatch.setattr(ra, "AUTHORIZED_INVESTIGATOR_NAMES", set(investigator_names))


class TestVerifyAuthorizedIdentityRejection:
    def test_rejects_unset_git_identity_regardless_of_logged_by(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path)  # unauthenticated environment
        _patch_allowlists(monkeypatch, git_identities={("Test Investigator", "test@example.com")})
        with pytest.raises(IdentityError):
            verify_authorized_identity("Mei-Ling Zhao", cwd=str(repo), env=env)

    def test_rejects_git_identity_not_on_allowlist(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Unauthorized Person", email="nobody@example.com")
        _patch_allowlists(monkeypatch, git_identities={("Test Investigator", "test@example.com")})
        with pytest.raises(IdentityError, match="not on the authorized-investigator"):
            verify_authorized_identity("Mei-Ling Zhao", cwd=str(repo), env=env)

    def test_rejects_logged_by_agent_even_with_authorized_git_identity(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(monkeypatch, git_identities={("Test Investigator", "test@example.com")})
        with pytest.raises(IdentityError, match="agent"):
            verify_authorized_identity("agent", cwd=str(repo), env=env)

    def test_rejects_logged_by_not_on_roster_even_with_authorized_git_identity(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Mei-Ling Zhao"},
        )
        with pytest.raises(IdentityError, match="Laboratory Roster"):
            verify_authorized_identity("Totally Made Up Person", cwd=str(repo), env=env)

    def test_rejects_empty_logged_by(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(monkeypatch, git_identities={("Test Investigator", "test@example.com")})
        with pytest.raises(IdentityError):
            verify_authorized_identity("", cwd=str(repo), env=env)

    def test_authorized_git_identity_alone_is_not_sufficient(self, tmp_path, monkeypatch):
        """Both factors are independently required — an authorized git
        identity paired with an unrecognized logged_by name must still be
        rejected (this is what distinguishes the mechanism from a
        single-factor check)."""
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Mei-Ling Zhao"},
        )
        with pytest.raises(IdentityError):
            verify_authorized_identity("Random Unrecognized Name", cwd=str(repo), env=env)


class TestVerifyAuthorizedIdentityAcceptance:
    def test_accepts_authorized_git_identity_and_roster_name(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Mei-Ling Zhao"},
        )
        identity = verify_authorized_identity("Mei-Ling Zhao", cwd=str(repo), env=env)
        assert isinstance(identity, IdentityVerification)
        assert identity.git_identity == ("Test Investigator", "test@example.com")
        assert identity.logged_by == "Mei-Ling Zhao"

    def test_accepts_dr_prefixed_logged_by_after_normalization(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Elias Vance"},
        )
        identity = verify_authorized_identity("Dr. Elias Vance", cwd=str(repo), env=env)
        assert identity.git_identity == ("Test Investigator", "test@example.com")
        assert identity.logged_by == "Dr. Elias Vance"  # stored verbatim, only matching is normalized

    def test_default_allowlists_are_the_module_constants_when_not_overridden(self):
        # Sanity check the production defaults are non-empty and internally
        # consistent — the real acceptance path (using the real workspace
        # git identity) is exercised in TestAuthorReflectionRealWorkspace.
        assert len(AUTHORIZED_GIT_IDENTITIES) >= 1
        assert "Mei-Ling Zhao" in AUTHORIZED_INVESTIGATOR_NAMES

    def test_verify_authorized_identity_alone_carries_no_governance_confirmation(self, tmp_path, monkeypatch):
        """verify_authorized_identity() and require_governance_confirmation()
        are deliberately decoupled — only author_reflection() bridges them
        (via dataclasses.replace()). A token from verify_authorized_identity()
        alone must never carry a governance_confirmation, so a caller who
        skips the confirmation step entirely gets a token that fails
        record_reflection()'s/write_reflection()'s governance check for
        GOVERNANCE_TRIGGERS records (see test_reflection_memory.py's
        TestGovernanceConfirmationComposition for that check itself)."""
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Mei-Ling Zhao"},
        )
        identity = verify_authorized_identity("Mei-Ling Zhao", cwd=str(repo), env=env)
        assert identity.governance_confirmation is None


class TestAllowlistOverrideSurfaceRemoved:
    """MISTAKE-2026-07-16-001's remediation item 2: authorized_git_identities
    / authorized_investigator_names must no longer be accepted as function
    parameters on verify_authorized_identity() or author_reflection() —
    exposing them was itself a compounding gap (a production call surface
    reachable by any caller could redefine "who is authorized"). These
    tests confirm the parameters were actually removed, not merely
    undocumented."""

    def test_verify_authorized_identity_rejects_authorized_git_identities_kwarg(self, tmp_path):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        with pytest.raises(TypeError):
            verify_authorized_identity(
                "Mei-Ling Zhao",
                cwd=str(repo),
                env=env,
                authorized_git_identities={("Test Investigator", "test@example.com")},
            )

    def test_verify_authorized_identity_rejects_authorized_investigator_names_kwarg(self, tmp_path):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        with pytest.raises(TypeError):
            verify_authorized_identity(
                "Mei-Ling Zhao",
                cwd=str(repo),
                env=env,
                authorized_investigator_names={"Mei-Ling Zhao"},
            )

    def test_author_reflection_rejects_authorized_git_identities_kwarg(self, tmp_path):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        with pytest.raises(TypeError):
            author_reflection(
                reflection_id="REFLECT-X",
                trigger_type="director_flagged",
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                cwd=str(repo),
                env=env,
                authorized_git_identities={("Test Investigator", "test@example.com")},
            )

    def test_author_reflection_rejects_authorized_investigator_names_kwarg(self, tmp_path):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        with pytest.raises(TypeError):
            author_reflection(
                reflection_id="REFLECT-X",
                trigger_type="director_flagged",
                source_event_ref="ref",
                summary="s",
                root_cause="c",
                remediation="r",
                scope_of_applicability="a",
                logged_by="Mei-Ling Zhao",
                cwd=str(repo),
                env=env,
                authorized_investigator_names={"Mei-Ling Zhao"},
            )


# ---------------------------------------------------------------------------
# require_governance_confirmation — TTY-required, typed-confirmation gate
# for GOVERNANCE_TRIGGERS record types only
# ---------------------------------------------------------------------------

class _FakeStdin:
    """A stand-in for sys.stdin whose .isatty() is controllable — tests
    never need (or want) a real interactive terminal attached to the test
    runner to exercise this function's control flow."""

    def __init__(self, is_tty: bool):
        self._is_tty = is_tty

    def isatty(self) -> bool:
        return self._is_tty


class TestRequireGovernanceConfirmation:
    def test_rejects_non_tty_stdin(self):
        with pytest.raises(HumanConfirmationRequiredError, match="not a real TTY"):
            require_governance_confirmation(
                "REFLECT-001", "process_violation", stdin=_FakeStdin(is_tty=False)
            )

    def test_stdin_without_isatty_method_is_treated_as_non_tty(self):
        """A stdin-like object that raises on .isatty() (or lacks it
        entirely) must degrade to "not a TTY," never crash or, worse,
        silently pass the check."""
        class _BrokenStdin:
            def isatty(self):
                raise RuntimeError("no such stream")

        with pytest.raises(HumanConfirmationRequiredError):
            require_governance_confirmation(
                "REFLECT-001", "process_violation", stdin=_BrokenStdin()
            )

    def test_accepts_correct_typed_confirmation_on_a_real_tty(self):
        # Returns the confirmed reflection_id — author_reflection() folds
        # this into IdentityVerification.governance_confirmation.
        result = require_governance_confirmation(
            "REFLECT-001",
            "process_violation",
            stdin=_FakeStdin(is_tty=True),
            prompt_fn=lambda _prompt: "REFLECT-001",
        )
        assert result == "REFLECT-001"

    def test_rejects_mismatched_typed_confirmation(self):
        with pytest.raises(HumanConfirmationRequiredError, match="did not match"):
            require_governance_confirmation(
                "REFLECT-001",
                "process_violation",
                stdin=_FakeStdin(is_tty=True),
                prompt_fn=lambda _prompt: "some-other-id",
            )

    def test_rejects_empty_typed_confirmation(self):
        with pytest.raises(HumanConfirmationRequiredError):
            require_governance_confirmation(
                "REFLECT-001",
                "process_violation",
                stdin=_FakeStdin(is_tty=True),
                prompt_fn=lambda _prompt: "",
            )

    def test_strips_surrounding_whitespace_before_comparing(self):
        # Must not raise — a trailing newline/space from a real terminal
        # shouldn't cause a false rejection. Returns the canonical
        # (unpadded) reflection_id, not the raw typed text.
        result = require_governance_confirmation(
            "REFLECT-001",
            "process_violation",
            stdin=_FakeStdin(is_tty=True),
            prompt_fn=lambda _prompt: "  REFLECT-001  \n",
        )
        assert result == "REFLECT-001"


# ---------------------------------------------------------------------------
# author_reflection — end-to-end: identity gate + governance-confirmation
# gate block/allow record construction
# ---------------------------------------------------------------------------

class _RecordingSink:
    def __init__(self):
        self.calls = []

    def write_reflection(self, record, identity):
        self.calls.append((record, identity))


class TestAuthorReflectionEndToEnd:
    def _kwargs(self, **overrides):
        base = dict(
            reflection_id="REFLECT-TEST-001",
            trigger_type="process_violation",  # a GOVERNANCE_TRIGGERS type
            source_event_ref="core-component-00/telescope/x/mistake-log.md#MISTAKE-001",
            summary="summary text",
            root_cause="root cause text",
            remediation="remediation text",
            scope_of_applicability="scope text",
            logged_by="Mei-Ling Zhao",
        )
        base.update(overrides)
        return base

    def test_rejected_identity_never_constructs_a_record(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path)  # unauthenticated
        _patch_allowlists(monkeypatch, git_identities={("Test Investigator", "test@example.com")})
        sink = _RecordingSink()
        with pytest.raises(IdentityError):
            author_reflection(sink=sink, cwd=str(repo), env=env, **self._kwargs())
        assert sink.calls == []  # never reached the write path

    def test_rejected_identity_never_reaches_governance_confirmation(self, tmp_path, monkeypatch):
        """Ordering check: identity must be verified before the (more
        expensive, interactive) governance-confirmation step runs — an
        unauthenticated caller should never even see the confirmation
        prompt."""
        repo, env = _init_repo(tmp_path)  # unauthenticated
        _patch_allowlists(monkeypatch, git_identities={("Test Investigator", "test@example.com")})
        prompt_calls = []

        def _tracking_prompt(_msg):
            prompt_calls.append(_msg)
            return "REFLECT-TEST-001"

        with pytest.raises(IdentityError):
            author_reflection(
                cwd=str(repo),
                env=env,
                stdin=_FakeStdin(is_tty=True),
                prompt_fn=_tracking_prompt,
                **self._kwargs(),
            )
        assert prompt_calls == []

    def test_accepted_identity_and_confirmation_constructs_and_writes_through(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Mei-Ling Zhao"},
        )
        sink = _RecordingSink()
        record = author_reflection(
            sink=sink,
            cwd=str(repo),
            env=env,
            stdin=_FakeStdin(is_tty=True),
            prompt_fn=lambda _prompt: "REFLECT-TEST-001",
            **self._kwargs(),
        )
        assert record.reflection_id == "REFLECT-TEST-001"
        assert record.sacred is True  # process_violation is a GOVERNANCE_TRIGGERS type
        assert len(sink.calls) == 1
        written_record, written_identity = sink.calls[0]
        assert written_record.reflection_id == "REFLECT-TEST-001"
        # The composition-gap fix: require_governance_confirmation()'s result
        # was folded into the IdentityVerification token itself before it
        # reached the sink, not left as a separate, already-forgotten step.
        assert written_identity.governance_confirmation == "REFLECT-TEST-001"

    def test_governance_trigger_without_tty_is_rejected_even_with_valid_identity(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Mei-Ling Zhao"},
        )
        sink = _RecordingSink()
        with pytest.raises(HumanConfirmationRequiredError):
            author_reflection(
                sink=sink,
                cwd=str(repo),
                env=env,
                stdin=_FakeStdin(is_tty=False),
                **self._kwargs(),
            )
        assert sink.calls == []  # rejected before construction

    def test_non_governance_trigger_skips_confirmation_entirely(self, tmp_path, monkeypatch):
        """director_flagged is not in GOVERNANCE_TRIGGERS — no TTY/typed
        confirmation should be required, even over non-interactive stdin."""
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Mei-Ling Zhao"},
        )
        sink = _RecordingSink()
        record = author_reflection(
            sink=sink,
            cwd=str(repo),
            env=env,
            stdin=_FakeStdin(is_tty=False),  # would fail require_governance_confirmation if invoked
            **self._kwargs(trigger_type="director_flagged"),
        )
        assert record.reflection_id == "REFLECT-TEST-001"
        assert record.sacred is False

    def test_invalid_trigger_type_still_rejected_after_identity_passes(self, tmp_path, monkeypatch):
        repo, env = _init_repo(tmp_path, name="Test Investigator", email="test@example.com")
        _patch_allowlists(
            monkeypatch,
            git_identities={("Test Investigator", "test@example.com")},
            investigator_names={"Mei-Ling Zhao"},
        )
        sink = _RecordingSink()
        with pytest.raises(ValueError):
            author_reflection(
                sink=sink,
                cwd=str(repo),
                env=env,
                **self._kwargs(trigger_type="not_a_real_trigger"),
            )


class TestAuthorReflectionRealWorkspace:
    """Exercises the production default allowlists (no overrides) against
    this actual repository's real git identity — the genuine acceptance
    case a human investigator hits when running the script for real in this
    workspace."""

    def test_real_workspace_identity_is_authorized(self):
        # This repository's committed history is authored entirely under one
        # git identity (see git-workflow.md / `git log`) — verify that
        # identity is the one this script's default allowlist recognizes,
        # so the production default path is actually exercised, not just
        # the test-only override path.
        identity = get_authenticated_git_identity()
        assert identity in AUTHORIZED_GIT_IDENTITIES

    def test_real_workspace_identity_accepts_a_roster_investigator(self):
        sink = _RecordingSink()
        record = author_reflection(
            reflection_id="REFLECT-TEST-REAL-001",
            trigger_type="director_flagged",
            source_event_ref="core-component-00/telescope/x/ref",
            summary="summary",
            root_cause="cause",
            remediation="fix",
            scope_of_applicability="scope",
            logged_by="Mei-Ling Zhao",
            sink=sink,
        )
        assert record.logged_by == "Mei-Ling Zhao"
        assert len(sink.calls) == 1


# ---------------------------------------------------------------------------
# _load_shared_embedder — the shared-model-cache embedder loading mechanism
# for the CLI authoring path (Kwame Asante's completeness-gap flag: the CLI
# path must actually be able to produce a working embedder, not silently
# always construct the index with embedder=None).
#
# Real model_dir/loader are injected here (mirroring this module's existing
# DI convention, e.g. QdrantMemoryIndex's injectable client/embedder) so
# these tests exercise the real control flow deterministically, without
# requiring the real ~90MB all-MiniLM-L6-v2 weights to be provisioned in
# this environment (mcp-servers/_shared/models/ is gitignored — provisioned
# per-machine via provision_model.py, not checked into the repo).
# ---------------------------------------------------------------------------

class _FakeSentenceTransformer:
    """Minimal stand-in for sentence_transformers.SentenceTransformer's
    public surface this module actually uses (.encode(text) -> vector-like
    with .tolist())."""

    def __init__(self, model_dir: str):
        self.model_dir = model_dir

    class _FakeVector:
        def __init__(self, values):
            self._values = values

        def tolist(self):
            return self._values

    def encode(self, text: str):
        return self._FakeVector([float(len(text))] * 4)


class TestLoadSharedEmbedder:
    def test_returns_none_when_model_dir_missing(self, tmp_path):
        missing_dir = tmp_path / "does-not-exist"
        assert _load_shared_embedder(model_dir=missing_dir) is None

    def test_returns_none_when_model_dir_present_but_empty(self, tmp_path):
        empty_dir = tmp_path / "empty-model-dir"
        empty_dir.mkdir()
        assert _load_shared_embedder(model_dir=empty_dir) is None

    def test_returns_working_callable_when_model_dir_present_and_loader_succeeds(self, tmp_path):
        model_dir = tmp_path / "sentence-transformers--all-MiniLM-L6-v2"
        model_dir.mkdir()
        (model_dir / "config.json").write_text("{}")  # non-empty marker file

        embedder = _load_shared_embedder(model_dir=model_dir, loader=_FakeSentenceTransformer)

        assert embedder is not None
        assert callable(embedder)
        vector = embedder("hello world")
        assert isinstance(vector, list)
        assert len(vector) == 4

    def test_returns_none_when_loader_raises(self, tmp_path):
        model_dir = tmp_path / "sentence-transformers--all-MiniLM-L6-v2"
        model_dir.mkdir()
        (model_dir / "config.json").write_text("{}")

        def _failing_loader(_path: str):
            raise RuntimeError("simulated load failure")

        assert _load_shared_embedder(model_dir=model_dir, loader=_failing_loader) is None

    def test_default_model_dir_matches_shared_cache_slug_convention(self):
        from implementations.reflection_authoring import _shared_model_dir

        resolved = _shared_model_dir()
        assert resolved.parts[-4:] == (
            "mcp-servers",
            "_shared",
            "models",
            "sentence-transformers--all-MiniLM-L6-v2",
        )


class TestBuildDefaultSinkWiresEmbedder:
    def test_build_default_sink_actually_calls_load_shared_embedder(self, monkeypatch):
        """Regression test for Kwame Asante's completeness-gap flag:
        _build_default_sink() must genuinely attempt to load the shared
        embedder (call _load_shared_embedder()), not silently skip that
        call and hand QdrantMemoryIndex a hardcoded embedder=None. This is
        checked directly against the call itself — independent of whether a
        live Qdrant instance or qdrant_client happens to be available in
        this environment, which the rest of _build_default_sink() degrades
        around regardless."""
        import implementations.reflection_authoring as ra
        from unittest.mock import MagicMock

        sentinel_embedder = MagicMock(name="sentinel_embedder")
        load_calls = MagicMock(return_value=sentinel_embedder)
        monkeypatch.setattr(ra, "_load_shared_embedder", load_calls)

        _build_default_sink()

        load_calls.assert_called_once()

    def test_build_default_sink_passes_loaded_embedder_into_qdrant_index(self, monkeypatch):
        """When both a shared embedder and qdrant_client are available, the
        embedder _load_shared_embedder() returns must be the same object
        handed to QdrantMemoryIndex — not discarded in favour of None."""
        pytest.importorskip("qdrant_client")

        import implementations.reflection_authoring as ra
        from implementations import memory_vector_store
        from unittest.mock import MagicMock

        sentinel_embedder = MagicMock(name="sentinel_embedder")
        monkeypatch.setattr(ra, "_load_shared_embedder", lambda: sentinel_embedder)
        monkeypatch.setattr(memory_vector_store, "QdrantClient", MagicMock(), raising=False)
        monkeypatch.setattr("qdrant_client.QdrantClient", MagicMock())

        captured = {}
        real_index_cls = memory_vector_store.QdrantMemoryIndex

        class _CapturingIndex(real_index_cls):
            def __init__(self, memory_type, client=None, embedder=None, dim=384):
                captured["embedder"] = embedder
                super().__init__(memory_type, client=client, embedder=embedder, dim=dim)

            def ensure_collection(self):
                return None  # no real network call in this test

        monkeypatch.setattr(memory_vector_store, "QdrantMemoryIndex", _CapturingIndex)

        _build_default_sink()

        assert captured.get("embedder") is sentinel_embedder

    def test_no_shared_model_falls_back_to_none_embedder_gracefully(self, monkeypatch, tmp_path):
        missing_dir = tmp_path / "not-provisioned"

        import implementations.reflection_authoring as ra

        monkeypatch.setattr(ra, "_shared_model_dir", lambda: missing_dir)

        sink = _build_default_sink()  # must not raise even with no model and possibly no live Qdrant
        assert sink is not None
