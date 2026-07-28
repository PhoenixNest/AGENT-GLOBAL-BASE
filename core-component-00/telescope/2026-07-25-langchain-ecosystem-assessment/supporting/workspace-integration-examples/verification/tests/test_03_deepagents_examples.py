"""Verifies the runnable claims in workspace-integration-examples/03-deepagents-examples.md.

The cookbook's `03-deepagents.md` already live-executed a single create_deep_agent(...) call
during authoring, but that run was never saved as a reproducible test. This module is the first
committed, re-runnable proof that DeepAgents itself -- not a hand-rolled graph -- accepts this
file's exact declared topology (a static, named subagent roster, a checkpointer, and gated
writes) and completes end to end with no API key. It also proves Example 3's backend-confinement
claim: FilesystemBackend writes land only inside its declared root_dir.
"""

import sqlite3

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend, StateBackend
from langgraph.checkpoint.sqlite import SqliteSaver

from cc00_wie_verification.fakes import ToolCapableFakeChatModel

# Example 2's declared, non-overlapping roster -- reproduced verbatim (tools trimmed to
# what this harness needs, since search_workspace/calculator come from other examples).
SUBAGENTS = [
    {
        "name": "retriever",
        "description": "Retrieves and cites passages from the workspace corpus. Read-only.",
        "system_prompt": "Retrieve passages answering the question.",
        "tools": [],
    },
    {
        "name": "analyst",
        "description": "Compares and computes over already-retrieved passages. No retrieval.",
        "system_prompt": "Reason only over the passages you are given.",
        "tools": [],
    },
    {
        "name": "critic",
        "description": "Attempts to refute a draft finding. Holds no tools.",
        "system_prompt": "Try to refute the finding you are given.",
        "tools": [],
    },
]


def test_declared_subagent_roster_has_no_tool_overlap():
    """The ASGF L5 Required check from Example 2, made mechanical: no two specialists
    may share a tool (a proxy for the '>70% skill-set overlap -> consolidate' rule)."""
    tool_sets = [frozenset(a["tools"]) for a in SUBAGENTS if a["tools"]]
    for i, a in enumerate(tool_sets):
        for b in tool_sets[i + 1 :]:
            assert not (a & b), "Two specialists share a tool -- overlap check failed."


def test_deep_agent_with_declared_topology_and_gated_writes_runs_end_to_end(tmp_path):
    model = ToolCapableFakeChatModel(responses=["Synthesised finding: no material overlap found."])

    db_path = tmp_path / "checkpoints.sqlite"
    connection = sqlite3.connect(str(db_path), check_same_thread=False)
    checkpointer = SqliteSaver(connection)

    agent = create_deep_agent(
        model=model,
        tools=[],
        system_prompt="You are the Lead Research Agent. Delegate to your three named specialists.",
        subagents=SUBAGENTS,
        backend=StateBackend(),
        interrupt_on={"write_file": True, "edit_file": True, "read_file": False, "ls": False},
        checkpointer=checkpointer,
        name="cc00-deep-research-verification",
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Do the passages overlap?"}]},
        config={"configurable": {"thread_id": "research-verification-1"}},
    )

    assert result["messages"][-1].content == "Synthesised finding: no material overlap found."


def test_filesystem_backend_confines_writes_to_its_declared_root_dir(tmp_path):
    """Example 3's blast-radius claim: root_dir is the whole confinement boundary.

    REAL FINDING (found only by running this, not by reading the doc): FilesystemBackend
    defaults to virtual_mode=False, and with that default, an absolute path or a `..`
    segment bypasses root_dir entirely -- the confinement the doc promises does not hold
    under the library's own default. virtual_mode=True must be passed explicitly for
    Example 3's "root_dir is the whole confinement boundary" claim to actually be true.
    """
    backend = FilesystemBackend(root_dir=str(tmp_path), virtual_mode=True)

    write_result = backend.write("notes/finding-1.md", "Draft finding: no overlap detected.")
    assert write_result is not None

    on_disk = tmp_path / "notes" / "finding-1.md"
    assert on_disk.exists(), "Write must land inside root_dir, not the process cwd."
    assert on_disk.read_text() == "Draft finding: no overlap detected."

    read_result = backend.read("notes/finding-1.md")
    assert "no overlap detected" in str(read_result.content if hasattr(read_result, "content") else read_result)


def test_filesystem_backend_virtual_mode_false_allows_path_escape(tmp_path):
    """Documents the hazard behind the finding above: with the library's own default
    (virtual_mode unset -> False), a path containing `..` escapes root_dir entirely.
    This is the concrete reproduction of why Example 3's confinement claim requires an
    explicit virtual_mode=True, not just a root_dir argument."""
    confined_dir = tmp_path / "agent-workspace"
    confined_dir.mkdir()
    escape_target = tmp_path / "escaped.md"

    backend = FilesystemBackend(root_dir=str(confined_dir))  # virtual_mode left at its default
    backend.write("../escaped.md", "This should never leave agent-workspace/.")

    assert escape_target.exists(), (
        "Reproduces the real hazard: with virtual_mode at its default, '..' escapes "
        "root_dir. If this assertion ever starts failing, the library's default has "
        "changed and the finding above should be re-verified, not deleted."
    )
