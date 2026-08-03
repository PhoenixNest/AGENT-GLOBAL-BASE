"""Verifies the runnable claims in workspace-integration-examples/01-langchain-examples.md.

Scope is deliberately narrower than the file itself: 01's Example 1 (governed baseline) and
Example 2 (schema-constrained output) share their `create_agent` / four-slot-state shape with
enterprise-examples/'s already-tested flagship agent, so this module does not re-prove that
shape. It proves the three claims specific to THIS file that nothing else in the investigation
has executed: a tool-bearing agent builds against a custom state schema, ToolStrategy's
Literal-field schema is enforced by the parser (not by prose), and Example 4's tiered-routing
guard sends any tool-bearing request to the reasoning model regardless of task shape.
"""

from typing import Annotated, Any, Callable, Literal, TypedDict

import pytest
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelRequest
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field, ValidationError

from cc00_wie_verification.fakes import ToolCapableFakeChatModel


class GovernedAgentState(TypedDict, total=False):
    """A minimal stand-in for the doc's four-slot state -- just enough to prove the
    "tool-bearing agent accepts extra declared state keys" claim, not a reimplementation
    of ContextAssembler."""

    messages: Annotated[list, "add_messages placeholder -- default reducer is fine here"]
    sacred_context: list[str]
    retrieved: list[Any]
    tool_outputs: list[Any]


@tool
def lookup_service_owner(component: str) -> str:
    """Return the on-call owner for a component. Use only after a component name is settled."""
    return f"owner-of-{component}"


def test_governed_agent_baseline_builds_and_invokes_with_declared_state():
    model = ToolCapableFakeChatModel(responses=["Routed to on-call: owner-of-billing"])
    agent = create_agent(
        model=model,
        tools=[lookup_service_owner],
        system_prompt="You are the Support Triage Analyst. Classify and route only.",
        state_schema=GovernedAgentState,
    )

    result = agent.invoke(
        {
            "messages": [HumanMessage(content="Billing API is down")],
            "sacred_context": ["Severity definitions are fixed by on-call policy."],
            "retrieved": [],
            "tool_outputs": [],
        }
    )

    assert result["messages"][-1].content == "Routed to on-call: owner-of-billing"


class TriageResult(BaseModel):
    """The Example 2 contract, reproduced verbatim from the doc."""

    category: Literal["bug", "feature-request", "access-request", "question", "unclassifiable"] = (
        Field(description="The single best category.")
    )
    severity: Literal["p0", "p1", "p2", "p3"] = Field(description="p0 = outage; p3 = cosmetic.")
    component: str = Field(description="Component name, verbatim from the catalogue.")
    requires_human: bool = Field(description="True when an escalation criterion is met.")
    reasoning: str = Field(description="Two sentences maximum.")


def test_schema_constrained_output_agent_builds_with_tool_strategy():
    model = ToolCapableFakeChatModel(responses=["irrelevant -- construction is what's tested"])
    agent = create_agent(
        model=model,
        tools=[],
        system_prompt="Classify and return the declared schema only.",
        response_format=ToolStrategy(TriageResult),
    )
    assert agent is not None


def test_triage_result_literal_fields_are_enforced_by_the_parser_not_prose():
    # A valid instance constructs cleanly.
    TriageResult(
        category="bug",
        severity="p1",
        component="billing-api",
        requires_human=False,
        reasoning="Two sentences of reasoning.",
    )
    # An out-of-enum category is rejected at construction, not left to the model to "behave".
    with pytest.raises(ValidationError):
        TriageResult(
            category="not-a-real-category",
            severity="p1",
            component="billing-api",
            requires_human=False,
            reasoning="x",
        )


class TieredModelMiddleware(AgentMiddleware):
    """Example 4, reproduced: local tier ONLY when no tool is on the request."""

    def __init__(self, reasoning_model, local_model, is_bulk_classification: Callable):
        self.reasoning_model = reasoning_model
        self.local_model = local_model
        self._is_bulk_classification = is_bulk_classification

    def wrap_model_call(self, request: ModelRequest, handler):
        if request.tools:
            return handler(request.override(model=self.reasoning_model))
        if self._is_bulk_classification(request):
            return handler(request.override(model=self.local_model))
        return handler(request.override(model=self.reasoning_model))


def _make_request(tools):
    reasoning_model = ToolCapableFakeChatModel(responses=["reasoning-tier"])
    return ModelRequest(model=reasoning_model, messages=[HumanMessage(content="x")], tools=tools)


def test_tiered_routing_sends_any_tool_bearing_request_to_the_reasoning_model():
    reasoning_model = ToolCapableFakeChatModel(responses=["reasoning-tier"])
    local_model = ToolCapableFakeChatModel(responses=["local-tier"])
    middleware = TieredModelMiddleware(
        reasoning_model=reasoning_model,
        local_model=local_model,
        is_bulk_classification=lambda request: True,  # would route local if the guard didn't win
    )

    request = _make_request(tools=[lookup_service_owner])
    used_models = []

    def handler(req):
        used_models.append(req.model)
        return None

    middleware.wrap_model_call(request, handler)
    assert used_models == [reasoning_model], (
        "A tool-bearing request must never reach the local tier, "
        "regardless of how simple the task looks (Finding 6)."
    )


def test_tiered_routing_sends_tool_free_bulk_classification_to_the_local_model():
    reasoning_model = ToolCapableFakeChatModel(responses=["reasoning-tier"])
    local_model = ToolCapableFakeChatModel(responses=["local-tier"])
    middleware = TieredModelMiddleware(
        reasoning_model=reasoning_model,
        local_model=local_model,
        is_bulk_classification=lambda request: True,
    )

    request = _make_request(tools=[])
    used_models = []

    def handler(req):
        used_models.append(req.model)
        return None

    middleware.wrap_model_call(request, handler)
    assert used_models == [local_model]
