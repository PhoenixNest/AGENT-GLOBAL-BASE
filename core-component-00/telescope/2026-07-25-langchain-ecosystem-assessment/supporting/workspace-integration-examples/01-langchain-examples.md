# 01 — LangChain Examples (`langchain` 1.3.14)

**Prerequisite:** `00-conventions-and-baseline.md` — pins, environment, and the ASGF governance kit
these examples import.
**Status:** Reference examples, API surface verified against `langchain-ai/docs` via Context7 on
2026-07-26. **Partially executed 2026-07-27:** Examples 1, 2, and 4's core claims (a tool-bearing
agent with declared extra state keys, `ToolStrategy`'s Literal-field enforcement, and the tiered
model-routing guard) are proven by 5 real, passing tests in `verification/` (a standalone project
in this same folder — see its `README.md`). Examples 3, 5, and 6 remain unexecuted.

---

## What this product is, in one paragraph

LangChain v1 is an **agent framework wearing an old name**. The chain-composition identity that made
its reputation (LCEL, `Runnable`, `LLMChain`) is no longer the headline and, in the case of the
legacy chains, no longer in the package — it moved to `langchain-classic`. The headline is
`create_agent`: a prebuilt agent loop running on LangGraph's durable-execution runtime, with
cross-cutting concerns attached as **middleware** rather than subclasses. For CC-00 the durable
value is provider abstraction and integration breadth; the durable risk is that any tutorial written
before October 2025 teaches an API that no longer resolves.

---

## Example 1 — The governed agent baseline

**Use when:** you are building any agent in this workspace. This is the floor, not a demo.

**ASGF requirements exercised:** L1 role/persona, L1 system-vs-task separation, L1 behavioural
constraints, L2 four-slot (all three Mandatory items), L3 timeout, L3 typed error boundary, L3 token
budget, L3 rate-limit backoff, L3 tool whitelist, L3 tool-call limits, L3 PII in/out.

```python
"""Example 1 — a create_agent baseline that is ASGF-governed from the first line.

The point of this example is what is NOT here: no bare create_agent call, no
"You are a helpful assistant", no unbounded loop, no untimed model call.
"""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from cc00_langchain.asgf import cc00_middleware_stack
from cc00_langchain.telemetry import install_tracing

install_tracing(service_name="cc00-support-triage")

# --- ASGF L1: the system prompt is an identity document, not a greeting ------------
#
# "Role / persona defined" is Mandatory and the standard is explicit that
# "You are a helpful assistant" does NOT satisfy it. The three sections below map
# one-to-one onto three ASGF L1 requirements: role, behavioural constraints
# (the anti-pattern firewall), and escalation criteria.
SYSTEM_PROMPT = """\
# Role

You are the Support Triage Analyst for an internal engineering support queue. Your
expertise is limited to classifying inbound support requests and routing them. You
do not diagnose root causes, you do not propose code changes, and you do not
communicate with the reporter.

# Behavioural constraints (forbidden behaviours)

- Never widen scope beyond classification and routing. If a request tempts you to
  debug, classify it and stop.
- Never fail silently. If you cannot classify a request, return the `unclassifiable`
  category with a stated reason rather than guessing a plausible one.
- Never downgrade a severity to make a queue look healthier. Severity is a finding,
  not a target.
- Never invent a component name. Use only components present in the retrieved
  service catalogue.

# Escalation criteria

Escalate to a human — by returning `requires_human: true` with a reason — when:
- The request alleges data loss, a security breach, or a production outage.
- The request references a customer contract, legal exposure, or a regulator.
- Two classifications are equally supported by the evidence and the choice changes
  who is paged.

# Output

Reply only with the structured schema you have been given. No prose outside it.
"""

# --- ASGF L3: every model call has a timeout. A call with no timeout is not
# --- acceptable under the standard — this is the enforcement point.
model = init_chat_model(
    "anthropic:claude-sonnet-5",     # substitute the id your pinned package supports
    timeout=60,
    max_retries=0,                   # retries belong to TypedErrorBoundaryMiddleware,
                                     # not to the client — one retry policy, one place
)

agent = create_agent(
    model=model,
    tools=[classify_request, lookup_service_owner],   # defined in Example 3
    system_prompt=SYSTEM_PROMPT,
    middleware=cc00_middleware_stack(
        system_prompt=SYSTEM_PROMPT,
        task_type="factual_qa",       # CC-00 slot profile: 65% retrieved, 10% history
        max_tokens=128_000,
        max_model_calls=8,            # triage is bounded work; 8 is generous
    ),
)

result = agent.invoke(
    {
        "messages": [{"role": "user", "content": inbound_ticket_text}],
        # State keys FourSlotContextMiddleware reads. Absent-safe, but populating
        # them is what makes the four-slot structure real rather than nominal.
        "sacred_context": [
            "Severity definitions are fixed by the on-call policy and may not be reinterpreted.",
        ],
        "retrieved": service_catalogue_chunks,   # from CC-00 RAG — see 04 and 06
        "tool_outputs": [],
    }
)
```

**Note on the duplicated `system_prompt`.** It is passed both to `create_agent` and to the
middleware stack. That is deliberate, and it is the one wart in this design:
`FourSlotContextMiddleware` owns the System slot at assembly time, so it needs the text;
`create_agent` needs it for the runs where the middleware is disabled or reordered. Keeping them in
one Python constant means they cannot drift. If you find yourself passing two different strings, one
of them is dead.

**Verify before trusting:**

- Set `max_model_calls=1` and confirm the cap raises rather than silently truncating.
- Feed a ticket containing an email address; confirm `[REDACTED:email]` reaches the model.
- Break the model endpoint; confirm the failure classifies as `timeout`/`unknown` and the circuit
  breaker opens rather than retrying forever.

---

## Example 2 — Schema-constrained output (never prose)

**Use when:** the agent's output is consumed by another agent or any downstream system. Which, in
an enterprise setting, is nearly always.

**ASGF requirement:** L1 "Output format constrained" — **Mandatory** for any agent whose output is
consumed downstream. The schema must be explicit, not requested in prose.

```python
"""Example 2 — structured output via ToolStrategy / ProviderStrategy.

Asking a model to "reply in JSON" is the anti-pattern. It is a request, not a
constraint, and it fails exactly when the input is unusual — which is when you
most need the output to parse.
"""

from typing import Literal

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy
from pydantic import BaseModel, Field


class TriageResult(BaseModel):
    """The contract this agent owes its consumer. Field docs are prompt surface."""

    category: Literal[
        "bug", "feature-request", "access-request", "question", "unclassifiable"
    ] = Field(description="The single best category. Use 'unclassifiable' rather than guessing.")

    severity: Literal["p0", "p1", "p2", "p3"] = Field(
        description=(
            "p0 = data loss / security breach / production outage. "
            "p1 = core feature broken. p2 = degraded. p3 = cosmetic or advisory."
        )
    )

    component: str = Field(
        description="Component name, taken verbatim from the retrieved service catalogue."
    )

    requires_human: bool = Field(
        description="True when any escalation criterion in the system prompt is met."
    )

    reasoning: str = Field(
        description="Two sentences maximum. Why this category and severity, citing the evidence."
    )


agent = create_agent(
    model=model,
    tools=[classify_request, lookup_service_owner],
    system_prompt=SYSTEM_PROMPT,
    # ToolStrategy works across providers by expressing the schema as a tool call.
    # ProviderStrategy uses native structured-output support where the provider has
    # it — stricter and cheaper, but provider-dependent. Prefer ProviderStrategy when
    # your pinned provider supports it; ToolStrategy is the portable default.
    response_format=ToolStrategy(TriageResult),
    middleware=cc00_middleware_stack(system_prompt=SYSTEM_PROMPT, task_type="factual_qa"),
)
```

**Why `Literal` rather than `str`:** an enum in the schema is enforced by the parser. An enum
described in prose is enforced by hope. The same argument applies to `requires_human: bool` — the
escalation decision is a field the consumer can branch on, not a sentence someone has to read.

**Anti-pattern this replaces:**

```python
# DO NOT DO THIS. This is an ASGF L1 Mandatory failure.
system_prompt = "Classify the ticket and reply in JSON with category and severity."
```

---

## Example 3 — Tools as prompt surface

**Use when:** defining any tool. Tool descriptions are read by the model on every call — they are
part of the prompt, and they should be written with the same care.

**ASGF requirements:** L3 tool whitelist, L3 tool-call limits (both Required when tools are used).

```python
"""Example 3 — narrow, well-named, registry-backed tools.

Tool-selection accuracy degrades sharply as tool count grows. The discipline is:
few tools, narrow types, and a description that tells the model when NOT to use it.
"""

from typing import Literal

from langchain.tools import tool

from cc00_langchain.cc00_path import TOOL_REGISTRY, ToolRegistry

registry = ToolRegistry(TOOL_REGISTRY)


@tool
def lookup_service_owner(component: str) -> str:
    """Return the on-call owner for a component in the service catalogue.

    Use this ONLY after you have settled on a component name. Do not use it to
    discover component names — it returns an error for unknown components rather
    than a suggestion, and calling it speculatively wastes a bounded call budget.

    Args:
        component: Exact component name from the service catalogue.
    """
    if not registry.is_allowed_tool("lookup_service_owner"):
        raise PermissionError("Tool not whitelisted in the CC-00 registry.")
    return _catalogue.owner_of(component)


@tool
def classify_request(
    text: str,
    hint: Literal["auto", "bug", "feature-request"] = "auto",
) -> dict:
    """Score a support request against the classification taxonomy.

    Returns per-category confidence scores. This is an ADVISORY signal — you own
    the final classification and may overrule it when the retrieved catalogue
    contradicts the score. Do not call it more than once per ticket; a second call
    on the same text returns the same scores.

    Args:
        text: The raw ticket body.
        hint: Optional prior. Leave as "auto" unless the reporter stated a category.
    """
    return _classifier.score(text, hint=hint)
```

**The three rules encoded above:**

| Rule                                             | Where it shows up                                        |
| ------------------------------------------------ | -------------------------------------------------------- |
| Tell the model **when not to** call the tool     | "Do not use it to discover component names"              |
| State the **idempotence / cost** characteristics | "a second call on the same text returns the same scores" |
| Type narrowly                                    | `Literal["auto", "bug", "feature-request"]`, not `str`   |

**Registry alignment matters.** `ToolGovernanceMiddleware` raises at wiring time if a tool is not in
`TOOL_REGISTRY`. That is intentional: the alternative — dropping the tool silently — produces an
agent that fails in a way that looks like a model problem and is actually a config problem. Register
new tools in `core-component-00/framework/03-harness-engineering/implementations/tool_registry.py`,
where the timeout, per-task call cap, and `requires_approval` flag live together.

---

## Example 4 — Model routing: spend capability where it matters

**Use when:** a workload mixes cheap high-volume calls with a few decision-critical ones. This is
also the **only correct way to use the local LM Studio tier** in this workspace.

**ASGF requirement:** none directly — this is cost and hardware discipline from Findings 5–6.

```python
"""Example 4 — route by task, not by default.

Finding 6: an 8B local model is a large quality downgrade specifically in
tool-calling reliability, which is the one capability an agent loop cannot tolerate
being flaky. So the routing rule is not "local when possible" — it is
"local ONLY when no tool call is at stake".
"""

from typing import Callable

from langchain.agents.middleware import AgentMiddleware, ModelRequest
from langchain.agents.middleware.types import ModelResponse
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

reasoning_model = init_chat_model("anthropic:claude-sonnet-5", timeout=60, max_retries=0)

# Scoped tier. NOT installed on this machine — see 00 §4.
local_model = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed",
    model="<the model id LM Studio reports>",
    timeout=120,
)


class TieredModelMiddleware(AgentMiddleware):
    """Send tool-free classification to the local tier; everything else to the API."""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        # The guard, not a heuristic: if ANY tool is on the request, the local
        # model is disqualified regardless of how simple the task looks.
        if request.tools:
            return handler(request.override(model=reasoning_model))

        if _is_bulk_classification(request):
            return handler(request.override(model=local_model))

        return handler(request.override(model=reasoning_model))
```

**The failure mode this prevents:** an 8B model that fumbles a tool schema produces malformed calls,
retry storms, and — worst — silent wrong answers. None of that is compensated for by local inference
being fast and free.

---

## Example 5 — Knowing when _not_ to use LangChain

**Use when:** the task is a single model call with a schema.

**ASGF requirement:** none. This is best practice #10 from the research report, and it is the one
most often ignored.

```python
"""Example 5 — the abstraction tax is only worth paying for what it buys.

An agent loop buys you: tool selection, durability, multi-step reasoning. If the
task is "read this text, return this schema", you are paying for a loop that will
execute exactly once.
"""

from langchain.chat_models import init_chat_model

model = init_chat_model("anthropic:claude-sonnet-5", timeout=30, max_retries=0)
structured = model.with_structured_output(TriageResult)

result = structured.invoke(
    [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": inbound_ticket_text},
    ]
)
```

**But note what you gave up**, and decide deliberately rather than by omission: no middleware means
no four-slot assembly, no token budget, no typed error boundary, no PII scrubbing. For a genuinely
one-shot internal call that may be the right trade. For anything that touches user data or runs
unattended, it is not — wrap it in the CC-00 harness (`SafeModelCall` in
`error_boundary.py`) even when you skip the agent loop. **"Simple enough to skip the agent" is not
the same as "simple enough to skip the harness."**

---

## Example 6 — Migrating this workspace's stale v0.x references

**Use when:** acting on Finding 9. This is live technical debt in
`core-component-00/framework/04-retrieval-augmented-generation/`, severity P2, and it is real regardless of
whether LangChain is ever adopted.

**The hazard, restated:** `requirements.txt` pins `langchain>=0.1.0`. That open-ended constraint
**resolves to 1.3.14 today** — a different, incompatible library from the one the surrounding
documentation was written against. Anyone who runs that install gets code samples that fail on
import, with no signal explaining why.

| Location                            | v0.x as written                                                      | v1 equivalent                                                             |
| ----------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `tools/utility-guide.md:598`        | `from langchain.text_splitter import RecursiveCharacterTextSplitter` | `from langchain_text_splitters import RecursiveCharacterTextSplitter`     |
| `components/quick-reference.md:232` | same                                                                 | same                                                                      |
| `integrations/reference.md:96, 273` | same (two occurrences)                                               | same                                                                      |
| `components/quick-reference.md:180` | `from langchain.retrievers import ContextualCompressionRetriever`    | `from langchain_classic.retrievers import ContextualCompressionRetriever` |
| `components/quick-reference.md:470` | LangSmith tracing example                                            | **Delete** — commercial dependency, excluded by the CEO constraint        |
| `requirements.txt:30-31`            | `langchain>=0.1.0`, `langchain-community>=0.0.19`                    | Pin exactly (00 §3), **or remove entirely** if LangChain is not adopted   |
| `architecture/overview.md:60`       | Names "LangChain/LlamaIndex" as the RAG Orchestrator                 | An architectural claim never realised — correct the text or implement it  |

```python
# The general v0 -> v1 shape. Legacy chains, retrievers, the indexing API, and the
# hub module all moved OUT of `langchain` and into `langchain-classic`.

from langchain.chains import LLMChain            # v0.x — does not resolve in v1
from langchain_classic.chains import LLMChain    # v1 — resolves, but see below
```

**Do not treat `langchain-classic` as the migration target.** It is a compatibility shelf, not a
destination. An `LLMChain` in v1 is almost always better expressed as a direct model call with
structured output (Example 5) or as `create_agent` (Example 1). Reach for `langchain-classic` only
to keep something alive while you replace it.

**Recommended sequencing** (this is the P2 cleanup, and it does not depend on the adoption
decision):

1. Decide adoption first. If LangChain is declined, **delete** lines 30–31 of `requirements.txt`
   rather than repinning them — a pinned dependency on an unused library is still drift.
2. If adopted, replace the open-ended pins with the exact set from `00 §3`.
3. Fix the four import samples regardless of the decision. They are wrong either way.
4. Delete the LangSmith example regardless. It is excluded by constraint.
5. Correct `architecture/overview.md:60` so it describes what the RAG module actually is —
   a first-party implementation — rather than an orchestrator that was never built.

---

## Anti-pattern summary for this product

| Anti-pattern                                                   | Why it fails                                                                                |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Bare `create_agent(model, tools, system_prompt)` in production | Confers no ASGF control. Every Mandatory L2/L3 item is unmet.                               |
| "You are a helpful assistant"                                  | Explicitly named in the standard as **not** satisfying L1 role definition.                  |
| "Reply in JSON"                                                | A request, not a constraint. Fails on unusual input. L1 Mandatory failure.                  |
| Twenty tools on one agent                                      | Tool-selection accuracy degrades sharply with count. Split the agent or the tools.          |
| Retry policy on both client and middleware                     | Two independent retry budgets multiply. Pick one place — the middleware.                    |
| Following any tutorial dated 2023–2024                         | Teaches `LLMChain` / `initialize_agent` / `AgentExecutor` — an API that no longer resolves. |
| Local 8B model driving tool calls                              | The single failure mode an agent loop cannot absorb. Finding 6.                             |

---

**Document status:** Reference examples — unexecuted.
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-26
