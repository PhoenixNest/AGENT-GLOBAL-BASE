"""
Reflection Authoring — the Investigator-Authored Write Path

The only sanctioned way to construct and persist a ReflectionRecord
(implementations/memory_store.py). Per
core-component-00/telescope/2026-07-14-reflexion-memory-system/supporting/
01-technical-options.md §4, no MCP tool exists or should ever exist to let
an agent call this write path directly ("Option A" was evaluated and
rejected) — this module is a short, low-ceremony script a named human
investigator runs directly, matching the "Investigator-Authored Write Path"
("Option B") the CEO finalized.

Identity enforcement — the actual security boundary, stated plainly (revised
2026-07-16, after two rounds of implementation + adversarial review):

    FOR GOVERNANCE_TRIGGERS RECORDS (process_violation / defect_root_cause /
    ase_exception_closure — the sacred=True-by-default category, and the
    only category MISTAKE-001's Phase 3 migration will use), THE ACTUAL
    SECURITY BOUNDARY IS PROCEDURAL, NOT ANYTHING IN THIS FILE: genuine,
    live, in-transcript confirmation from the real human user (the CEO, or
    Dr. Vance under CEO-delegated authority, confirming directly in the
    live coordinating session — never relayed through an intermediary
    agent) is required before any such record is treated as authorized to
    persist for real. This mirrors the precedent already tested and proven
    in this workspace for `.claude/hooks/` self-modification: a delegated
    agent was blocked from self-modifying hooks even with a relayed quote
    of the user's authorization, because consent must be present directly
    in the transcript of whoever performs the action. See
    supporting/03-deployment-guidelines.md's revised Phase 1 "done" gate and
    research-report.md's § Audit History, MISTAKE-2026-07-16-001 entry, for
    the full reasoning behind this pivot. Nothing below changes that.

    Why code alone cannot be the boundary: two full rounds of
    implementation + adversarial review by Dr. Wieczorek established that
    no purely code-level check running inside Claude Code's own
    tool-execution environment can make this write path unforgeable — an
    agent has the same import access a human developer does, so any layer
    (a git-identity check, a token, a TTY prompt) is skippable by calling
    something lower (the sink, the raw JSONL/Qdrant calls). First pass:
    Wieczorek showed the git-identity + roster-name check alone passes for
    any co-located agent process, since it authenticates the machine, not
    the operator. Second pass, after `IdentityVerification` and the
    TTY-gated confirmation were added: Wieczorek showed both were still
    skippable — by fabricating an `IdentityVerification` directly (which
    also silently skipped the confirmation step, since that step lived one
    layer up and nothing forced it to run), or by calling
    `PersistentMemorySink.write_reflection()` directly, bypassing
    `ReflectionMemory` and every check in it. This is a structural ceiling,
    not an engineering gap awaiting a cleverer fix — a third code layer
    would only hand a third adversarial pass its next bypass.

    What the code layers below actually are — legitimate defense-in-depth
    against careless/accidental misuse, explicitly NOT claimed as
    unforgeable or as the boundary:

    1. Git-identity + roster-name attribution: (1) the machine's
       `git config user.name`/`user.email` must appear on
       AUTHORIZED_GIT_IDENTITIES, and (2) `logged_by` must independently
       name a real person on the CC-00 Laboratory Roster
       (AUTHORIZED_INVESTIGATOR_NAMES), never "agent." Real and useful for
       its own narrower purpose — knowing who plausibly authored a record —
       but not identity *enforcement* on its own.
    2. `ReflectionMemory.record_reflection()` (memory_store.py) requires a
       verified `IdentityVerification` token — closes the *zero-effort*
       direct-import bypass (a bare logged_by string), not the fabricated-
       token bypass (Python has no true encapsulation; see
       `IdentityVerification`'s docstring).
    3. `require_governance_confirmation()` demands a real interactive TTY
       and a typed confirmation of the reflection_id for GOVERNANCE_TRIGGERS
       types, and its result is now folded into the `IdentityVerification`
       token itself (`governance_confirmation`) rather than being a
       separately-skippable step — closing the *composition* gap Wieczorek's
       second pass found (a fabricated token no longer silently bypasses
       confirmation; it must also carry a matching `governance_confirmation`
       value). This still does not make the token unforgeable — it is a
       plain dataclass field, directly settable by any caller who
       constructs the object themselves.
    4. `PersistentMemorySink.write_reflection()` (memory_vector_store.py)
       independently re-checks the same `IdentityVerification` requirements
       — closes the *direct-sink-call* bypass Wieczorek's second pass found
       (constructing a bare `ReflectionRecord` and calling the sink
       directly, skipping `ReflectionMemory` entirely). This is not the
       floor either: `JSONLMemoryLog.append_reflection()` and
       `QdrantMemoryIndex.upsert_payload()` remain directly callable
       beneath it with no check of any kind.

    AUTHORIZED_GIT_IDENTITIES / AUTHORIZED_INVESTIGATOR_NAMES are
    module-level constants only — not caller-overridable function
    parameters. An earlier revision exposed them as optional keyword
    arguments on verify_authorized_identity()/author_reflection() for test
    convenience; that was itself a second, compounding gap (a production
    call surface that could redefine "who is authorized" was reachable by
    any caller, not test-only in practice). Tests now monkeypatch the
    module-level constants directly (standard pytest pattern), matching how
    any other module-level policy constant in this codebase would be
    tested.

    Dr. Wieczorek's remaining role is scoped to confirming (a) these two
    bounded fixes don't regress anything and (b) this docstring is honest —
    not to further bypass-hunting, since code is no longer claimed as the
    boundary (supporting/03-deployment-guidelines.md's revised Phase 1
    "done" gate).

Usage (CLI):
    python reflection_authoring.py \\
        --reflection-id REFLECT-001 \\
        --trigger-type process_violation \\
        --source-event-ref "core-component-00/telescope/.../mistake-log.md#MISTAKE-001" \\
        --summary "..." \\
        --root-cause "..." \\
        --remediation "..." \\
        --scope-of-applicability "..." \\
        --logged-by "Mei-Ling Zhao"

    For a GOVERNANCE_TRIGGERS --trigger-type, this must be run from a real
    interactive terminal — it will prompt for a typed confirmation of the
    reflection_id and refuse to proceed over a non-interactive stdin (a
    plain script/subprocess invocation with no TTY attached).

Usage (library, e.g. from a REPL or another trusted script):
    from implementations.reflection_authoring import author_reflection
    record = author_reflection(
        reflection_id="REFLECT-001",
        trigger_type="process_violation",
        source_event_ref="...",
        summary="...",
        root_cause="...",
        remediation="...",
        scope_of_applicability="...",
        logged_by="Mei-Ling Zhao",
    )
"""

from __future__ import annotations

import argparse
import dataclasses
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, List, Optional, Sequence, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from implementations.memory_store import (  # noqa: E402
    GOVERNANCE_TRIGGERS,
    IdentityVerification,
    ReflectionMemory,
    ReflectionRecord,
    TRIGGER_TYPES,
    UnverifiedReflectionError,
)


# ---------------------------------------------------------------------------
# Authorization allowlists
# ---------------------------------------------------------------------------
#
# AUTHORIZED_GIT_IDENTITIES — (name, email) tuples permitted to run this
# script. This workspace has exactly one real human operator's git identity
# configured (see the repository's actual `git log` authorship); this is
# not a guess — it matches every commit currently in this repository's
# history. Extend this set only when a second human operator's git identity
# is genuinely provisioned for this workspace.
AUTHORIZED_GIT_IDENTITIES: Set[Tuple[str, str]] = {
    ("PhoenixNest", "xenomega@163.com"),
}

# AUTHORIZED_INVESTIGATOR_NAMES — the CC-00 Laboratory Roster
# (core-component-00/crew/CLAUDE.md "Laboratory Roster" table). logged_by
# must name one of these real persons-of-record — never "agent", never an
# arbitrary string. Stored without honorifics ("Dr."); comparison strips
# a leading "Dr. " from the supplied value before matching.
AUTHORIZED_INVESTIGATOR_NAMES: Set[str] = {
    "Elias Vance",
    "Idris Farouk",
    "Mei-Ling Zhao",
    "Kwame Asante",
    "Sofia Almeida",
    "Amara Nwosu-Chen",
    "Tomasz Wieczorek",
    "Ravi Deshmukh",
    "Amina Yusuf",
    "Diego Fontán",
    "Hana Kobayashi",
    "Connor O'Malley",
}


class IdentityError(Exception):
    """Raised when the authoring environment or the claimed investigator
    fails the identity-enforcement check. Distinct from ValueError (which
    ReflectionRecord.__post_init__ already raises for schema-level
    problems) so callers can tell "this isn't a valid record" apart from
    "this record was rejected before construction because the caller isn't
    who they claim to be"."""


def _run_git_config(key: str, cwd: Optional[str], env: Optional[dict] = None) -> Optional[str]:
    """Read one git config key the same way git itself resolves it (local
    config overrides global, exactly as `git commit` would use it to
    attribute authorship). Returns None if the key is unset or git is
    unavailable — never raises, so the caller can produce one clear
    IdentityError instead of a raw subprocess traceback.

    `env` is exposed purely for deterministic test isolation (e.g. pointing
    GIT_CONFIG_GLOBAL at a nonexistent file so a test's "unset identity"
    case does not accidentally read the real developer machine's global git
    config); production callers should leave it as None to inherit the
    real process environment, which is what makes this check meaningful."""
    try:
        result = subprocess.run(
            ["git", "config", key],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def get_authenticated_git_identity(
    cwd: Optional[str] = None, env: Optional[dict] = None
) -> Tuple[str, str]:
    """
    Read the authenticated (name, email) git identity for the environment
    this script is running in, exactly as git itself would resolve
    `user.name` / `user.email` for commit authorship.

    Args:
        cwd: Directory to resolve git config from (defaults to the current
             working directory). Tests pass a temp repo's path here so the
             check is deterministic and does not depend on whatever the
             real developer machine happens to have configured globally.
        env: See _run_git_config — test isolation only.

    Raises:
        IdentityError: if either user.name or user.email is unset. This is
            the "unauthenticated environment" rejection case — a formatting
            check on logged_by cannot catch this, since a caller could
            still type any name into --logged-by regardless of what git
            actually knows about the machine's identity.
    """
    name = _run_git_config("user.name", cwd, env=env)
    email = _run_git_config("user.email", cwd, env=env)
    if not name or not email:
        raise IdentityError(
            "No authenticated git identity is configured for this environment "
            "(git config user.name / user.email must both be set) — refusing to "
            "author a ReflectionRecord under an unauthenticated session."
        )
    return (name, email)


def _normalize_investigator_name(logged_by: str) -> str:
    name = logged_by.strip()
    if name.lower().startswith("dr. "):
        name = name[4:].strip()
    return name


def verify_authorized_identity(
    logged_by: str,
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
) -> IdentityVerification:
    """
    The two-factor identity-enforcement gate. Must pass before any
    ReflectionRecord is constructed. See this module's docstring
    ("Identity enforcement — honest current state") for what this check
    does and does not guarantee — in particular, it does not distinguish a
    human operator from a co-located AI agent process
    (MISTAKE-2026-07-16-001).

    Always checks against the module-level AUTHORIZED_GIT_IDENTITIES /
    AUTHORIZED_INVESTIGATOR_NAMES constants — there is no caller-supplied
    override. Tests that need a different allowlist monkeypatch those
    constants directly (e.g. `monkeypatch.setattr(reflection_authoring,
    "AUTHORIZED_GIT_IDENTITIES", {...})`), never pass one through this
    function's arguments.

    Args:
        logged_by: The investigator name the caller claims to be authoring
                   as (the value that will become ReflectionRecord.logged_by).
        cwd: Directory to resolve the git identity from (see
             get_authenticated_git_identity). Defaults to the current
             working directory in production use; tests override this.
        env: See _run_git_config — test isolation only.

    Returns:
        An IdentityVerification token for this exact logged_by value,
        required by ReflectionMemory.record_reflection() (memory_store.py).

    Raises:
        IdentityError: if the git identity is unset, not on the allowlist,
            or `logged_by` does not name an authorized investigator (or is
            literally "agent").
    """
    identity = get_authenticated_git_identity(cwd=cwd, env=env)
    if identity not in AUTHORIZED_GIT_IDENTITIES:
        raise IdentityError(
            f"git identity {identity!r} is not on the authorized-investigator "
            "git-identity allowlist for this workspace — refusing to author a "
            "ReflectionRecord from this environment."
        )

    if not logged_by or logged_by.strip().lower() == "agent":
        raise IdentityError(
            "logged_by must name a real investigator of record — 'agent' or an "
            "empty value is never accepted, per ReflectionRecord's own design "
            "intent (01-technical-options.md §1)."
        )

    normalized = _normalize_investigator_name(logged_by)
    if normalized not in AUTHORIZED_INVESTIGATOR_NAMES:
        raise IdentityError(
            f"logged_by={logged_by!r} does not name a person on the CC-00 "
            "Laboratory Roster (core-component-00/crew/CLAUDE.md) — refusing to "
            "author a ReflectionRecord under an unrecognized investigator name."
        )

    return IdentityVerification(logged_by=logged_by, git_identity=identity)


class HumanConfirmationRequiredError(Exception):
    """Raised when a GOVERNANCE_TRIGGERS record's authoring attempt cannot
    obtain a real interactive human confirmation — either stdin is not a
    real TTY, or the typed confirmation did not match. See
    require_governance_confirmation() and this module's docstring for the
    disclosed limitation of this mechanism (it raises the bar; it does not
    make the path unforgeable)."""


def require_governance_confirmation(
    reflection_id: str,
    trigger_type: str,
    stdin: Optional[Any] = None,
    prompt_fn: Optional[Callable[[str], str]] = None,
) -> str:
    """
    For GOVERNANCE_TRIGGERS record types only (process_violation /
    defect_root_cause / ase_exception_closure — the sacred=True-by-default
    category, and the only category MISTAKE-001's Phase 3 migration will
    use): require the operator to type the literal reflection_id back at a
    real interactive TTY prompt before authoring proceeds.

    Returns the confirmed reflection_id (not just None) so the caller
    (author_reflection()) can fold it into the IdentityVerification token's
    governance_confirmation field — this closes the *composition* gap Dr.
    Wieczorek's second adversarial pass found: previously, this confirmation
    was a step callable code could simply not call (record_reflection() and
    write_reflection() had no way to tell whether it had run at all). Now a
    caller who wants a GOVERNANCE_TRIGGERS record accepted has to also
    fabricate a matching governance_confirmation value on the token they
    construct, not merely skip this function.

    This still does not make the authoring path unforgeable in an absolute
    sense — per MISTAKE-2026-07-16-001's disclosed conclusion, nothing
    purely code-level running in this environment can be, and this
    composition fix does not change that conclusion. A caller willing to
    deliberately script a fake TTY (e.g. via pty allocation) can still
    defeat the TTY check itself; a caller willing to read this module's
    source can still construct an IdentityVerification with a hand-set
    governance_confirmation without ever calling this function. What this
    does do is remove the "single non-interactive script invocation" attack
    Dr. Wieczorek demonstrated against the git-identity check alone, and
    close the specific composition gap his second pass found — raising the
    bar, not claiming the bar can't be cleared. For GOVERNANCE_TRIGGERS
    records, the actual security boundary is procedural (see this module's
    docstring), not this function.

    Args:
        reflection_id: Must be typed back exactly (after stripping
                       surrounding whitespace) to confirm.
        trigger_type: Included in the prompt text for operator clarity.
        stdin: Overrides the stream checked for .isatty() — test-only.
        prompt_fn: Overrides how the confirmation value is collected
                   (defaults to the builtin input()) — test-only, so tests
                   never need a real TTY to exercise this function's logic.

    Raises:
        HumanConfirmationRequiredError: if stdin is not a real TTY, or the
            typed confirmation does not exactly match reflection_id.
    """
    stream = stdin if stdin is not None else sys.stdin
    try:
        is_tty = bool(stream.isatty())
    except Exception:
        is_tty = False
    if not is_tty:
        raise HumanConfirmationRequiredError(
            f"Authoring a {trigger_type!r} reflection ({reflection_id}) is a "
            "GOVERNANCE_TRIGGERS record and requires an interactive human "
            "confirmation — stdin is not a real TTY. Governance-triggered "
            "reflections cannot be authored from a non-interactive script "
            "invocation."
        )

    ask = prompt_fn if prompt_fn is not None else input
    typed = ask(
        f"This is a GOVERNANCE_TRIGGERS reflection ({trigger_type}) — sacred "
        f"by default and will block Phase 3 migration gates. Type the "
        f"reflection_id exactly to confirm you are a human operator "
        f"authoring this record: "
    )
    if typed.strip() != reflection_id:
        raise HumanConfirmationRequiredError(
            f"Typed confirmation did not match reflection_id {reflection_id!r} "
            "— refusing to author this governance-triggered reflection."
        )
    return reflection_id


def author_reflection(
    reflection_id: str,
    trigger_type: str,
    source_event_ref: str,
    summary: str,
    root_cause: str,
    remediation: str,
    scope_of_applicability: str,
    logged_by: str,
    severity: Optional[str] = None,
    sacred: bool = False,
    status: str = "active",
    migrated_from: Optional[str] = None,
    sink: Optional[Any] = None,
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
    stdin: Optional[Any] = None,
    prompt_fn: Optional[Callable[[str], str]] = None,
) -> ReflectionRecord:
    """
    The Investigator-Authored Write Path entry point: verify identity,
    require a live human confirmation for GOVERNANCE_TRIGGERS records, then
    construct + validate + write-through a new ReflectionRecord via
    ReflectionMemory.record_reflection() (implementations/memory_store.py).

    Args:
        stdin, prompt_fn: Passed through to require_governance_confirmation()
                           for GOVERNANCE_TRIGGERS trigger types — test-only,
                           see that function's docstring. Ignored for
                           non-governance trigger types (no confirmation
                           step runs).

    Raises:
        IdentityError: if verify_authorized_identity() rejects the caller
            (see that function). Raised before any ReflectionRecord is
            constructed — an unauthorized caller never gets as far as
            schema validation or the governance-confirmation step.
        HumanConfirmationRequiredError: for GOVERNANCE_TRIGGERS trigger
            types only, if require_governance_confirmation() is not
            satisfied (see that function). Raised after identity
            verification but before record construction.
        UnverifiedReflectionError: should not occur in normal operation —
            record_reflection() would raise this only if the identity
            token this function itself obtained and passed through were
            somehow invalid, which indicates a bug in this function, not a
            caller error.
        ValueError: if the record itself is invalid per
            ReflectionRecord.__post_init__ (e.g. an unknown trigger_type) —
            this is a schema-level rejection, distinct from an identity or
            confirmation rejection, and can only be reached once both of
            those have already passed.
    """
    identity = verify_authorized_identity(logged_by, cwd=cwd, env=env)

    if trigger_type in GOVERNANCE_TRIGGERS:
        confirmed_reflection_id = require_governance_confirmation(
            reflection_id, trigger_type, stdin=stdin, prompt_fn=prompt_fn
        )
        # Fold the confirmation result into the token itself rather than
        # leaving it a separate, skippable step — closes the composition
        # gap Wieczorek's second pass found. IdentityVerification is
        # frozen, so this produces a new instance via dataclasses.replace()
        # rather than mutating in place.
        identity = dataclasses.replace(
            identity, governance_confirmation=confirmed_reflection_id
        )

    memory = ReflectionMemory(sink=sink)
    return memory.record_reflection(
        reflection_id=reflection_id,
        trigger_type=trigger_type,
        source_event_ref=source_event_ref,
        summary=summary,
        root_cause=root_cause,
        remediation=remediation,
        scope_of_applicability=scope_of_applicability,
        logged_by=logged_by,
        identity=identity,
        severity=severity,
        sacred=sacred,
        status=status,
        migrated_from=migrated_from,
    )


# Shared embedding-model cache convention (.claude/rules/mcp-governance.md):
# core-component-00/mcp-servers/_shared/models/<slug>/, slug = "/" -> "--".
# agent-memory's production embedder resolves to this exact model/dimension
# (sentence-transformers/all-MiniLM-L6-v2, 384-dim — matches
# memory_vector_store.EMBEDDING_DIM and the memory_reflection collection
# created for this Programme). This script runs standalone, outside the
# agent-memory MCP server process, so it cannot reuse that server's
# background-loaded embedder — it loads its own copy directly from the same
# shared cache, per the coordinator's direction and the cache's own
# documented purpose (any CC-00 process that needs this model reads it
# straight out of its slug directory; there is no shared init sequence
# between processes).
_SHARED_EMBEDDER_SLUG = "sentence-transformers--all-MiniLM-L6-v2"


def _shared_model_dir() -> Path:
    # core-component-00/context-engineering/implementations/ -> core-component-00/
    return (
        Path(__file__).resolve().parents[2]
        / "mcp-servers"
        / "_shared"
        / "models"
        / _SHARED_EMBEDDER_SLUG
    )


def _load_shared_embedder(
    model_dir: Optional[Path] = None,
    loader: Optional[Callable[[str], Any]] = None,
) -> Optional[Callable[[str], List[float]]]:
    """
    Load the shared all-MiniLM-L6-v2 embedder directly via
    sentence_transformers.SentenceTransformer, from the shared model cache
    (models/ is gitignored/provisioned locally, per
    mcp-servers/_shared/.gitignore — genuinely absent on a fresh checkout
    until `provision_model.py sentence-transformers/all-MiniLM-L6-v2` has
    been run there).

    Returns a Callable[[str], List[float]] embedder on success, or None if
    the shared model directory is missing/empty or loading fails for any
    other reason — a soft-degrade case, never a hard failure of the whole
    authoring run (the caller, _build_default_sink(), still returns a
    working JSONL-only sink either way).

    Args:
        model_dir: Overrides the resolved shared-cache path — test-only.
        loader: Overrides the SentenceTransformer constructor — test-only,
                so unit tests exercise this function's real control flow
                (missing dir / present dir / load failure) without needing
                the real ~90MB model on disk, mirroring this module's
                existing dependency-injection convention (QdrantMemoryIndex's
                injectable client/embedder, memory_vector_store.py's
                injectable Qdrant client throughout).
    """
    resolved_dir = model_dir if model_dir is not None else _shared_model_dir()
    if not resolved_dir.is_dir() or not any(resolved_dir.iterdir()):
        print(
            f"WARNING: shared embedder model cache not found at {resolved_dir} "
            "— reflections will be written to reflection-log.jsonl only; "
            "memory_reflection's vector index will stay empty until this is "
            "provisioned (core-component-00/mcp-servers/_shared/provision_model.py "
            "sentence-transformers/all-MiniLM-L6-v2).",
            file=sys.stderr,
        )
        return None

    try:
        if loader is not None:
            model = loader(str(resolved_dir))
        else:
            from sentence_transformers import SentenceTransformer  # type: ignore

            model = SentenceTransformer(str(resolved_dir))
    except Exception as exc:
        print(
            f"WARNING: could not load the shared embedder from {resolved_dir} "
            f"({exc}) — reflections will be written to reflection-log.jsonl only.",
            file=sys.stderr,
        )
        return None

    def _embed(text: str) -> List[float]:
        vector = model.encode(text)
        return vector.tolist() if hasattr(vector, "tolist") else list(vector)

    return _embed


def _build_default_sink() -> Any:
    """Best-effort construction of a real PersistentMemorySink wired to the
    live qdrant-memory instance, for CLI use. Falls back to a JSONL-only
    sink (log write-through still happens; the Qdrant index simply stays
    behind until the next rebuild) if qdrant_client or the shared embedder
    are unavailable — matching this module's degrade-gracefully precedent
    rather than failing the whole authoring run over an optional index."""
    from implementations.memory_vector_store import (
        JSONLMemoryLog,
        PersistentMemorySink,
        QdrantMemoryIndex,
    )

    log = JSONLMemoryLog()
    indices = {}
    embedder = _load_shared_embedder()
    try:
        from qdrant_client import QdrantClient  # type: ignore

        client = QdrantClient(url="http://localhost:6335")
        index = QdrantMemoryIndex("reflection", client=client, embedder=embedder)
        index.ensure_collection()
        indices["reflection"] = index
    except Exception as exc:  # pragma: no cover - environment-dependent
        print(
            f"WARNING: could not wire a live Qdrant index for reflections "
            f"({exc}); writing to reflection-log.jsonl only.",
            file=sys.stderr,
        )
    return PersistentMemorySink(log=log, indices=indices)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Author and persist a ReflectionRecord (Investigator-Authored Write Path).",
    )
    parser.add_argument("--reflection-id", required=True)
    parser.add_argument("--trigger-type", required=True, choices=sorted(TRIGGER_TYPES))
    parser.add_argument("--source-event-ref", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--root-cause", required=True)
    parser.add_argument("--remediation", required=True)
    parser.add_argument("--scope-of-applicability", required=True)
    parser.add_argument("--logged-by", required=True)
    parser.add_argument("--severity", choices=["P0", "P1"], default=None)
    parser.add_argument("--sacred", action="store_true", default=False)
    parser.add_argument("--status", choices=["active", "dormant", "archived"], default="active")
    parser.add_argument("--migrated-from", default=None)
    args = parser.parse_args(argv)

    try:
        record = author_reflection(
            reflection_id=args.reflection_id,
            trigger_type=args.trigger_type,
            source_event_ref=args.source_event_ref,
            summary=args.summary,
            root_cause=args.root_cause,
            remediation=args.remediation,
            scope_of_applicability=args.scope_of_applicability,
            logged_by=args.logged_by,
            severity=args.severity,
            sacred=args.sacred,
            status=args.status,
            migrated_from=args.migrated_from,
            sink=_build_default_sink(),
        )
    except (IdentityError, HumanConfirmationRequiredError, UnverifiedReflectionError, ValueError) as exc:
        print(f"REJECTED: {exc}", file=sys.stderr)
        return 1

    print(f"Authored {record.reflection_id} (sacred={record.sacred}, logged_by={record.logged_by!r})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
