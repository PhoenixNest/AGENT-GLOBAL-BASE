"""Verifies the runnable claims in workspace-integration-examples/02-langgraph-examples.md.

enterprise-examples/ already proves single-thread checkpoint pause/resume and a single
interrupt() approval gate (its flagship graph, Example 3 in the doc), so this module does not
repeat that. It proves three claims the flagship never exercised: the four-slot state's
`sacred_context` reducer is genuinely append-only (a node cannot erase it), a checkpointer
keeps two thread_ids' state fully isolated (the Finding-7 trust-boundary claim), and a
hierarchical Command topology with a fixed node set actually enforces "every specialist
reports only to the supervisor."
"""

import operator
import sqlite3
from typing import Annotated, Literal, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command


class FourSlotState(TypedDict, total=False):
    sacred_context: Annotated[list[str], operator.add]
    tool_outputs: Annotated[list[tuple], operator.add]
    visited: Annotated[list[str], operator.add]


def test_sacred_context_reducer_is_append_only_and_cannot_be_erased():
    def node_a(state: FourSlotState) -> dict:
        return {"sacred_context": ["Severity is fixed by policy."]}

    def node_b(state: FourSlotState) -> dict:
        # A node "clearing" sacred_context returns []. With an add reducer this must
        # append nothing, not erase what node_a already wrote -- the doc's exact claim.
        return {"sacred_context": []}

    builder = StateGraph(FourSlotState)
    builder.add_node("a", node_a)
    builder.add_node("b", node_b)
    builder.add_edge(START, "a")
    builder.add_edge("a", "b")
    builder.add_edge("b", END)
    graph = builder.compile()

    result = graph.invoke({"sacred_context": []})
    assert result["sacred_context"] == ["Severity is fixed by policy."]


def test_checkpointer_keeps_two_thread_ids_fully_isolated(tmp_path):
    def increment(state: FourSlotState) -> dict:
        return {"tool_outputs": [("increment", 1)]}

    builder = StateGraph(FourSlotState)
    builder.add_node("increment", increment)
    builder.add_edge(START, "increment")
    builder.add_edge("increment", END)

    db_path = tmp_path / "checkpoints.sqlite"
    connection = sqlite3.connect(str(db_path), check_same_thread=False)
    checkpointer = SqliteSaver(connection)
    graph = builder.compile(checkpointer=checkpointer)

    config_a = {"configurable": {"thread_id": "triage-A"}}
    config_b = {"configurable": {"thread_id": "triage-B"}}

    graph.invoke({"tool_outputs": []}, config=config_a)
    graph.invoke({"tool_outputs": []}, config=config_a)  # thread A: two increments
    graph.invoke({"tool_outputs": []}, config=config_b)  # thread B: one increment

    state_a = graph.get_state(config_a).values
    state_b = graph.get_state(config_b).values

    assert len(state_a["tool_outputs"]) == 2, "Thread A must see only its own history."
    assert len(state_b["tool_outputs"]) == 1, "Thread B must not inherit thread A's state."


def test_hierarchical_command_topology_routes_every_specialist_back_to_supervisor():
    """A simplified two-specialist version of Example 4's supervisor/classifier/
    cataloguer/historian topology -- proves the declared, non-emergent property: every
    specialist edge returns to the supervisor, and the supervisor alone decides completion."""

    def supervisor(state: FourSlotState) -> Command[Literal["classifier", "cataloguer", "synthesise"]]:
        done = {name for name, _ in state.get("tool_outputs", [])}
        for specialist in ("classifier", "cataloguer"):
            if specialist not in done:
                return Command(goto=specialist)
        return Command(goto="synthesise")

    def classifier(state: FourSlotState) -> dict:
        return {"tool_outputs": [("classifier", "bug")], "visited": ["classifier"]}

    def cataloguer(state: FourSlotState) -> dict:
        return {"tool_outputs": [("cataloguer", "billing-api")], "visited": ["cataloguer"]}

    def synthesise(state: FourSlotState) -> dict:
        return {"visited": ["synthesise"]}

    builder = StateGraph(FourSlotState)
    builder.add_node("supervisor", supervisor)
    builder.add_node("classifier", classifier)
    builder.add_node("cataloguer", cataloguer)
    builder.add_node("synthesise", synthesise)
    builder.add_edge(START, "supervisor")
    builder.add_edge("classifier", "supervisor")
    builder.add_edge("cataloguer", "supervisor")
    builder.add_edge("synthesise", END)
    graph = builder.compile()

    # The declared node set is exactly four nodes plus the implicit START/END --
    # nothing dynamically added at runtime (ASGF L5: no emergent topology).
    declared_nodes = set(graph.get_graph().nodes) - {"__start__", "__end__"}
    assert declared_nodes == {"supervisor", "classifier", "cataloguer", "synthesise"}

    result = graph.invoke({"tool_outputs": [], "visited": []})
    assert result["visited"] == ["classifier", "cataloguer", "synthesise"], (
        "Both specialists must run, in supervisor-controlled order, before synthesis -- "
        "neither specialist may hand off to the other directly."
    )


def test_command_handoff_tier_invariants_are_enforced_at_construction():
    """Example 5's tier table, reproduced as a checkable invariant: Full requires
    conversation_history, Minimal forbids it -- a mis-tiered packet must fail before
    it is ever sent, not after a specialist silently over- or under-reads it."""

    def build_handoff_dict(tier: str, conversation_history=None) -> dict:
        packet = {"tier": tier, "sacred_context": ["fixed by policy"]}
        if conversation_history is not None:
            packet["conversation_history"] = conversation_history

        if tier == "full" and "conversation_history" not in packet:
            raise ValueError("Full tier requires conversation_history.")
        if tier == "minimal" and "conversation_history" in packet:
            raise ValueError("Minimal tier forbids conversation_history.")
        return packet

    # Correct usage for each tier constructs cleanly.
    build_handoff_dict("full", conversation_history=[{"role": "user", "content": "hi"}])
    build_handoff_dict("minimal")

    # Mis-tiered packets fail at construction, not at the receiving specialist.
    try:
        build_handoff_dict("full")
        assert False, "Full tier without conversation_history should have raised."
    except ValueError:
        pass

    try:
        build_handoff_dict("minimal", conversation_history=[{"role": "user", "content": "hi"}])
        assert False, "Minimal tier with conversation_history should have raised."
    except ValueError:
        pass
