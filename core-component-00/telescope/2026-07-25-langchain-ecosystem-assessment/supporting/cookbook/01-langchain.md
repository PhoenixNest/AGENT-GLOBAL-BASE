# LangChain — Enterprise User Manual

**Package:** `langchain` · **Version:** 1.3.14 · **Stars:** 142,575 · **Status:** Active

---

## 1. Introduction

### What it is

LangChain is an agent framework: a uniform interface over chat models, tools, and structured output,
built around one primitive — `create_agent` — that runs a model-calls-tools-repeats loop on top of a
durable execution engine. As of version 1.0 (October 2025), this is a deliberate identity shift from
the library's earlier years, when its centre of gravity was LCEL (the LangChain Expression Language)
and chain composition via the `|` operator. That machinery still exists underneath as the substrate
for wiring components together, but it is no longer the headline, and legacy chains, retrievers, the
indexing API, and the `hub` module have moved into a separate `langchain-classic` package. Any
tutorial or code sample written before October 2025 describing `LLMChain`, `initialize_agent`, or
`AgentExecutor` is describing an API that no longer resolves from the `langchain` package.

### Core principles

| Principle                           | What it means in practice                                                                                                                                                                                                                          |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Provider abstraction**            | A uniform chat-model interface across essentially every provider. Swapping one model for another is a one-line change, not a rewrite — the single most durable value the library has ever delivered.                                               |
| **The agent loop is the primitive** | Call model → model picks tools → execute → repeat until no tool call. Everything else attaches around that loop.                                                                                                                                   |
| **Middleware over inheritance**     | Cross-cutting concerns (model routing, summarisation, guardrails, PII handling) attach as `AgentMiddleware` objects rather than subclasses — the single most important v1 design decision, because it is where governance controls attach cleanly. |
| **Durable execution**               | State lives in a checkpointer, so an agent can be interrupted, persisted, resumed, and even time-travelled. Agents survive process death.                                                                                                          |
| **Explicit graph topology**         | Multi-agent structure is a declared graph of nodes and edges, not emergent behaviour.                                                                                                                                                              |
| **Composability via Runnables**     | LCEL survives as the substrate for non-agentic pipelines and for wiring components together.                                                                                                                                                       |

### Why organisations adopt it

Four honest reasons, in order of weight:

1. **Integration breadth is the actual moat.** Well over a thousand pre-built integrations across
   model providers, vector stores, document loaders, and tools. The value is not that the
   abstractions are elegant — it is that the connector you need already exists.
2. **Provider portability as vendor-risk insurance.** A provider price change, outage, or
   deprecation becomes a configuration edit rather than a rewrite. For an enterprise this is a
   procurement argument as much as a technical one.
3. **The successor runtime solved the control problem that made the early library distrusted.**
   Opaque abstractions, uncontrollable agent behaviour, and impossible debugging were legitimate
   2023-era criticisms. Explicit graphs, checkpointing, and interrupts answered them directly.
4. **Ecosystem gravity.** Largest community, most tutorials, best model familiarity with the API,
   easiest hiring — self-reinforcing and rational to weight in a build-vs-buy decision.

### Enterprise framing

For a non-technical stakeholder: LangChain is the connective tissue between "the model" and
"everything the model needs to call to be useful" — search, databases, internal tools, other agents —
with the specific promise that switching which model powers the system later is cheap. Its risk
profile is the mirror image of its strength: breadth invites over-adoption, and the single most common
production failure mode in LangChain projects is using more of the framework than the task actually
needs.

---

## 2. Usage

### Installation

```powershell
pip install langchain langchain-anthropic   # or langchain-openai, etc. — pick your provider
```

### A governed minimal agent

```python
"""A minimal agent, with the discipline a production deployment actually needs
built in from the first line — not a bare create_agent call.
"""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

# --- Identity is a governance document, not a greeting. ---------------------
# "You are a helpful assistant" defines no expertise boundary and no
# escalation path. A real system prompt states role, forbidden behaviours,
# and when to hand off to a human — all three are load-bearing, not optional.
SYSTEM_PROMPT = """\
# Role
You are a support-ticket triage analyst. You classify inbound requests and
route them. You do not diagnose root causes and you do not contact reporters.

# Forbidden behaviours
- Never widen scope beyond classification. If tempted to debug, classify and stop.
- Never guess a category silently. Return "unclassifiable" with a stated reason instead.

# Escalation criteria
Escalate — return requires_human=true — on any alleged data loss, security
breach, or production outage.
"""

model = init_chat_model(
    "anthropic:claude-sonnet-5",
    timeout=60,       # every model call needs an explicit timeout — an unbounded
                       # call is a production incident waiting to happen
    max_retries=0,     # retries belong in a dedicated error-boundary middleware,
                       # not scattered between the client and the agent loop
)

agent = create_agent(
    model=model,
    tools=[classify_ticket, lookup_owner],   # keep the tool list short and narrowly typed —
                                              # tool-selection accuracy degrades sharply as it grows
    system_prompt=SYSTEM_PROMPT,
)

result = agent.invoke({"messages": [{"role": "user", "content": inbound_ticket_text}]})
print(result["messages"][-1].content)
```

### Schema-constrained output — never prose

```python
"""Asking a model to "reply in JSON" is a request, not a constraint, and it
fails exactly when the input is unusual. A typed schema is enforced by the
parser instead of hoped for.
"""

from typing import Literal

from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel, Field


class TriageResult(BaseModel):
    category: Literal["bug", "feature-request", "access-request", "unclassifiable"] = Field(
        description="Use 'unclassifiable' rather than guessing when evidence is thin."
    )
    severity: Literal["p0", "p1", "p2", "p3"]
    requires_human: bool


agent = create_agent(
    model=model,
    tools=[classify_ticket, lookup_owner],
    system_prompt=SYSTEM_PROMPT,
    # ToolStrategy expresses the schema as a tool call and works across
    # providers. Prefer a provider's native structured-output mode when
    # available — it is stricter and cheaper — and fall back to ToolStrategy
    # for portability.
    response_format=ToolStrategy(TriageResult),
)
```

### Middleware — where cross-cutting concerns actually belong

```python
"""wrap_model_call receives both the outgoing request and the downstream
handler, so it can inspect, rewrite, retry, or budget every model call. This
is the mechanism, not tool wrappers or prompt engineering, for anything that
needs to apply uniformly across every call an agent makes.
"""

from typing import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest
from langchain.agents.middleware.types import ModelResponse


class RetryWithBackoff(AgentMiddleware):
    def __init__(self, max_retries: int = 3) -> None:
        self.max_retries = max_retries

    def wrap_model_call(
        self, request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        for attempt in range(self.max_retries):
            try:
                return handler(request)
            except Exception:
                if attempt == self.max_retries - 1:
                    raise
                # Exponential backoff WITH jitter — immediate retry on a
                # rate-limit response is the standard way to make the problem worse.
                import random
                import time

                time.sleep((2**attempt) + random.uniform(0, 0.5))


agent = create_agent(
    model=model, tools=[...], system_prompt=SYSTEM_PROMPT,
    middleware=[RetryWithBackoff(max_retries=3)],
)
```

### Ten practices worth internalising

1. Start with `create_agent`; drop to a hand-built graph only once the prebuilt loop stops fitting.
2. Pin every package exactly — the ecosystem versions independently, and a security-relevant
   component (checkpointers) has shipped CVEs against unpinned installs historically.
3. Put cross-cutting concerns in middleware, not in tools or prompts.
4. Constrain output with schemas, never with prose instructions.
5. Keep tools few, well-named, and narrowly typed.
6. Always attach a checkpointer for anything multi-turn.
7. Gate irreversible actions behind a human-approval interrupt.
8. Bound the loop — max iterations, timeouts, tool-call caps.
9. Manage context deliberately, before the window overflows, not after.
10. Do not wrap what you do not need — a single schema-constrained call is sometimes just a call.

---

## 3. Alternatives and rationale

| Framework           | Wins when                                                                                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LlamaIndex**      | The system is fundamentally retrieval over a large, heterogeneous document corpus. Purpose-built for it; faster to production for pure RAG.                                  |
| **CrewAI**          | You want a role/task "crew" running in an afternoon. Materially lower time-to-first-working-agent; teams that bounce off a steeper learning curve elsewhere often land here. |
| **AutoGen**         | The work is research on dynamic, open-ended multi-agent conversation patterns rather than a production pipeline.                                                             |
| **Pydantic AI**     | Strict type safety is the primary requirement and the team already lives in Pydantic. Smallest, cleanest surface of the alternatives.                                        |
| **Semantic Kernel** | The organisation standardises on Microsoft/.NET enterprise tooling and wants that ecosystem's conventions.                                                                   |

**Rationale for choosing LangChain when it is chosen:** at roughly 142,575 stars — more than the
next several closest alternatives combined — its lead is a breadth lead, not a per-feature quality
lead, and that distinction should drive the decision. Adopt it when the binding constraint is
integration breadth, provider portability, or the need for a well-audited multi-agent control
surface (durable execution, explicit topology, human-approval gates). Do not adopt it as a default
simply because it is the most popular option — a narrower framework or no framework at all is
frequently the better engineering choice for a bounded task, and the honest failure mode to guard
against is using more of the framework than the problem requires.

---

## 4. Integrations

| Integrates with                              | How                                                                                                                                                                                     |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The underlying durable-execution runtime** | `create_agent` compiles to a graph on that runtime — every durability, checkpointing, and interrupt primitive documented in `02-langgraph.md` applies underneath every LangChain agent. |
| **`langchain-mcp-adapters`**                 | Converts MCP servers into ordinary LangChain tools — see `04-langchain-mcp-adapters.md`.                                                                                                |
| **DeepAgents**                               | A pre-configured, opinionated `create_agent` with planning, filesystem, and delegation middleware already wired — see `03-deepagents.md`.                                               |
| **Vector stores and embedding providers**    | Hundreds of integrations, reached through the same tool/retriever abstractions as any other LangChain component.                                                                        |
| **Observability**                            | A commercial hosted tracing platform exists from the same organisation; self-hosted OpenTelemetry is the open-source-only alternative.                                                  |

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
