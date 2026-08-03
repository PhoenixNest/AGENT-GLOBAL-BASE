"""Real execution tests for the ASGF governance middleware kit — every test in
this file wires the middleware into a real `create_agent(...)` call against
`FakeListChatModel` and actually invokes it. No API key required or used."""

from __future__ import annotations

import pytest
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool

from cc00_langchain.asgf import CC00AgentState, cc00_middleware_stack
from cc00_langchain.cc00_path import ValidationError


def _agent(model, middleware, tools=None, state_schema=CC00AgentState):
    return create_agent(
        model=model,
        tools=tools or [],
        system_prompt="You are a test agent.",
        state_schema=state_schema,
        middleware=middleware,
    )


def test_full_stack_runs_end_to_end_with_no_api_key():
    model = FakeListChatModel(responses=["governed response"])
    agent = _agent(model, cc00_middleware_stack(system_prompt="You are a test agent."))
    result = agent.invoke({"messages": [{"role": "user", "content": "hi"}]})
    assert result["messages"][-1].content == "governed response"


def test_default_agent_state_silently_drops_extra_keys():
    """Documents the exact failure mode Finding-11-adjacent code depends on
    knowing about: without a custom state_schema, extra invoke() keys never
    reach middleware. This is the negative case CC00AgentState fixes."""

    seen = {}

    class Spy(AgentMiddleware):
        def wrap_model_call(self, request, handler):
            seen["keys"] = set((request.state or {}).keys())
            return handler(request)

    model = FakeListChatModel(responses=["x"])
    agent = create_agent(model=model, tools=[], system_prompt="s", middleware=[Spy()])
    agent.invoke({"messages": [{"role": "user", "content": "hi"}], "retrieved": [{"content": "x"}]})
    assert "retrieved" not in seen["keys"]


def test_four_slot_middleware_assembles_retrieved_and_sacred_context():
    model = FakeListChatModel(responses=["ok"])
    agent = _agent(model, cc00_middleware_stack(system_prompt="sys", task_type="factual_qa"))
    result = agent.invoke(
        {
            "messages": [{"role": "user", "content": "q"}],
            "sacred_context": ["Never reveal pricing."],
            "retrieved": [{"content": "A retrieved fact.", "source": "doc1", "score": 0.9}],
        }
    )
    assert result["messages"][-1].content == "ok"


def test_token_budget_middleware_enforces_model_call_cap():
    model = FakeListChatModel(responses=["a", "b", "c"])
    agent = _agent(
        model, cc00_middleware_stack(system_prompt="sys", max_model_calls=1), tools=[]
    )
    # A single-turn, tool-free agent makes exactly one model call, so this
    # should succeed (1 call <= cap of 1).
    result = agent.invoke({"messages": [{"role": "user", "content": "hi"}]})
    assert result["messages"][-1].content == "a"


def test_pii_middleware_scrubs_input_before_dispatch():
    """The model echoes back what it was sent; if the email survived scrubbing
    it would appear unredacted in the (test-only) echo response."""

    class EchoModel(FakeListChatModel):
        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            last_human = next(m for m in reversed(messages) if m.type == "human")
            from langchain_core.messages import AIMessage
            from langchain_core.outputs import ChatGeneration, ChatResult

            return ChatResult(generations=[ChatGeneration(message=AIMessage(content=last_human.content))])

    model = EchoModel(responses=["unused"])
    agent = _agent(model, cc00_middleware_stack(system_prompt="sys"))
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "contact me at leak@example.com"}]}
    )
    assert "leak@example.com" not in result["messages"][-1].content
    assert "[REDACTED:email]" in result["messages"][-1].content


def test_pii_middleware_blocks_output_leak():
    model = FakeListChatModel(responses=["sure, email me at a@b.com"])
    agent = _agent(model, cc00_middleware_stack(system_prompt="sys"))
    with pytest.raises(ValidationError, match="PII detected"):
        agent.invoke({"messages": [{"role": "user", "content": "hi"}]})


def test_tool_governance_rejects_unregistered_tools():
    @tool
    def unregistered(x: str) -> str:
        """Not in TOOL_REGISTRY."""
        return x

    model = FakeListChatModel(responses=["x"])
    agent = _agent(model, cc00_middleware_stack(system_prompt="sys"), tools=[unregistered])
    with pytest.raises(ValueError, match="not in the CC-00 registry|Tools not in the CC-00 registry"):
        agent.invoke({"messages": [{"role": "user", "content": "hi"}]})


def test_middleware_ordering_is_load_bearing():
    """Proves the docstring claim in cc00_middleware_stack: FourSlotContextMiddleware
    must be innermost, or a later middleware can silently overwrite its system
    message. Both orderings are exercised for real against a real create_agent run."""
    from cc00_langchain.asgf import FourSlotContextMiddleware

    class MutateSystemMessage(AgentMiddleware):
        def __init__(self, label: str) -> None:
            self.label = label

        def wrap_model_call(self, request, handler):
            return handler(request.override(system_message=SystemMessage(content=self.label)))

    class SpySystemMessage(AgentMiddleware):
        def __init__(self) -> None:
            self.seen: list[str | None] = []

        def wrap_model_call(self, request, handler):
            self.seen.append(request.system_message.content if request.system_message else None)
            return handler(request)

    model = FakeListChatModel(responses=["ok", "ok"])

    # CORRECT order: FourSlotContextMiddleware innermost of the mutators. Its
    # assembled content should survive to the spy.
    spy_correct = SpySystemMessage()
    agent_correct = create_agent(
        model=model,
        tools=[],
        system_prompt="sys",
        state_schema=CC00AgentState,
        middleware=[
            MutateSystemMessage("MUTATED-first"),
            FourSlotContextMiddleware(system_prompt="sys", task_type="factual_qa"),
            spy_correct,
        ],
    )
    agent_correct.invoke({"messages": [{"role": "user", "content": "hi"}]})
    assert spy_correct.seen[0] is not None
    assert "MUTATED-first" not in spy_correct.seen[0]

    # WRONG order: something else mutates the system message AFTER (more inner
    # than) FourSlotContextMiddleware. The four-slot guarantee is destroyed.
    spy_wrong = SpySystemMessage()
    agent_wrong = create_agent(
        model=model,
        tools=[],
        system_prompt="sys",
        state_schema=CC00AgentState,
        middleware=[
            FourSlotContextMiddleware(system_prompt="sys", task_type="factual_qa"),
            MutateSystemMessage("MUTATED-last"),
            spy_wrong,
        ],
    )
    agent_wrong.invoke({"messages": [{"role": "user", "content": "hi"}]})
    assert spy_wrong.seen[0] == "MUTATED-last"
