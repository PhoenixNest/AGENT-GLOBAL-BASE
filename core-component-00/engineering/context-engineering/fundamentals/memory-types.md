# Memory Types in Context Engineering

## Overview

LLMs have no native persistent memory. Everything the model "knows" during a session must be explicitly placed in the context window. Context engineering defines four memory types that map to four different cognitive functions — each with a different lifespan, storage layer, and retrieval strategy.

---

## The Four Memory Types

### 1. Working Memory

**Cognitive analogy:** Short-term focus — what you are thinking about right now.

| Property          | Value                                      |
| ----------------- | ------------------------------------------ |
| **Lifespan**      | Single turn                                |
| **Storage layer** | Active context window (tool output slot)   |
| **Capacity**      | Bounded by tool output slot budget (≤ 15%) |
| **Retrieval**     | Always present — no retrieval needed       |
| **Persistence**   | Discarded after model response             |

#### What working memory holds

| Content                                               | Purpose                                                     |
| ----------------------------------------------------- | ----------------------------------------------------------- |
| Current task description and immediate sub-goals      | Anchors the model's focus for this turn                     |
| Current step in a multi-step plan                     | Prevents the model from losing track of progress            |
| Tool call results relevant to the current step        | Ground truth for the current reasoning operation            |
| In-progress intermediate reasoning (chain-of-thought) | Allows the model to build incrementally toward a conclusion |

#### Implementation

Working memory is not a database — it lives entirely in the context window. The `WorkingMemory` class in `implementations/memory_store.py` provides a structured container for assembling the tool output slot.

```python
wm = WorkingMemory()
wm.set_task("Generate a REST API for user authentication")
wm.set_current_step("Step 2 of 4: Define endpoint schemas")
wm.add_tool_result("schema_validator", {"valid": True, "fields": ["username", "password"]})

# Serialise into context window tool output slot
context_fragment = wm.to_context_string()
```

---

### 2. Episodic Memory

**Cognitive analogy:** Autobiographical memory — what happened during this session.

| Property          | Value                                                         |
| ----------------- | ------------------------------------------------------------- |
| **Lifespan**      | Session (cleared between sessions by default)                 |
| **Storage layer** | In-session key-value store (Redis / in-memory dict)           |
| **Capacity**      | Unbounded storage; retrieval bounded by retrieved slot budget |
| **Retrieval**     | Recency-based (last N events) or semantic query               |
| **Persistence**   | Optional cross-session archival                               |

#### What episodic memory holds

| Content                                       | When It Matters                                               |
| --------------------------------------------- | ------------------------------------------------------------- |
| User decisions made during this session       | Prevents the model from re-opening closed decisions           |
| Commitments the agent has made                | Sacred — must survive compression and be re-injected verbatim |
| Tasks completed and their outcomes            | Enables progress tracking across a long session               |
| Errors encountered and how they were resolved | Prevents repeating the same failure mode                      |
| Clarifications the user provided              | Prevents the model from re-asking questions already answered  |

#### Why it matters

Without episodic memory, the model re-asks questions the user already answered. It forgets decisions made three turns ago. It contradicts itself across a long session. Episodic memory is the primary mechanism for **session coherence**.

#### Critical rule: decisions and commitments

Decisions and commitments are a special sub-class of episodic memory. They must be:

1. Stored verbatim (not summarised) in episodic memory immediately when made
2. Re-injected verbatim into every subsequent context window for the session duration
3. Never discarded by context compression

```python
em = EpisodicMemory(session_id="session-abc123")
em.record_event("decision", "User chose PostgreSQL over MySQL for the backend database")
em.record_event("commitment", "Agent committed to providing a complete migration script by end of session")

# Sacred context — re-injected on every turn
sacred = em.get_sacred_context()  # Returns all decisions + commitments verbatim
```

---

### 3. Semantic Memory

**Cognitive analogy:** General knowledge — facts that are always true regardless of session.

| Property          | Value                                                         |
| ----------------- | ------------------------------------------------------------- |
| **Lifespan**      | Cross-session (persistent)                                    |
| **Storage layer** | Vector database or structured database                        |
| **Capacity**      | Unbounded storage; retrieval bounded by retrieved slot budget |
| **Retrieval**     | Semantic similarity search or structured query                |
| **Persistence**   | Permanent until explicitly updated or deleted                 |

#### What semantic memory holds

| Content                                                | Notes                                                                |
| ------------------------------------------------------ | -------------------------------------------------------------------- |
| User preferences and working styles                    | Personalises agent behaviour across sessions                         |
| Domain knowledge specific to this organisation         | Supplements the model's parametric knowledge with org-specific facts |
| Frequently used configurations, templates, preferences | Reduces repetitive clarification across tasks                        |
| Project-specific terminology and conventions           | Ensures consistent vocabulary and style                              |
| Agent-learned facts from prior sessions                | Carries persistent conclusions forward; requires TTL management      |

#### Freshness management

Semantic memory has a **TTL (time-to-live)** problem. Facts that were true 6 months ago may no longer be true. Every semantic memory record must carry a `created_at` timestamp and an optional `expires_at` or `confidence_decay_rate`.

```python
sm = SemanticMemory(vector_store=qdrant_client)
sm.store(
    key="user_preference_stack",
    value="User prefers FastAPI over Flask, PostgreSQL over SQLite, pytest over unittest",
    metadata={"created_at": "2026-04-28", "confidence": 0.95, "expires_after_days": 180}
)

# Retrieve relevant facts for current task
facts = sm.query("Which database should I use for this project?", top_k=3)
```

---

### 4. Procedural Memory

**Cognitive analogy:** Muscle memory — how to do things, not what happened.

| Property          | Value                                                |
| ----------------- | ---------------------------------------------------- |
| **Lifespan**      | Cross-session (persistent)                           |
| **Storage layer** | Agent profile / system prompt / skill files          |
| **Capacity**      | Bounded by system slot budget                        |
| **Retrieval**     | Loaded at session start; skill-triggered mid-session |
| **Persistence**   | Updated via agent profile versioning                 |

#### What procedural memory holds

| Content                                                      | How It Is Loaded                                                      |
| ------------------------------------------------------------ | --------------------------------------------------------------------- |
| Agent skills (how to perform a specific domain task)         | Loaded at session start or triggered mid-session via skill activation |
| Workflow templates (how to execute a pipeline stage)         | Injected via system prompt when the pipeline stage is entered         |
| Coding conventions (how this team structures code)           | Part of the permanent system slot for engineering agents              |
| Communication style rules (how formal to be with this user)  | Set at session start from the agent profile                           |
| Tool usage patterns (which tool to call for which task type) | Encoded in the system prompt or in skill files                        |

#### How procedural memory differs from the others

Procedural memory is not retrieved on-demand — it is **loaded at the start of the session** via the system prompt and skill activations. It does not go in the retrieved slot; it goes in the system slot.

In this workspace, the 213+ skill files and 77 agent profiles are the procedural memory store.

---

## Memory Type Comparison

| Dimension                     | Working            | Episodic                  | Semantic                         | Procedural                |
| ----------------------------- | ------------------ | ------------------------- | -------------------------------- | ------------------------- |
| **Stores**                    | Current task state | Session events            | Persistent facts                 | Behavioural patterns      |
| **Lives in**                  | Tool output slot   | Retrieved slot (on query) | Retrieved slot (on query)        | System slot               |
| **Managed by**                | `WorkingMemory`    | `EpisodicMemory`          | `SemanticMemory`                 | Agent profile / skills    |
| **Persists across sessions?** | No                 | Optional                  | Yes                              | Yes                       |
| **Compressed?**               | Never              | Old events summarised     | Facts retained, prose compressed | Versioned, not compressed |
| **Sacred content?**           | Current step       | Decisions + commitments   | User identity preferences        | Core role definition      |

---

## Memory Retrieval Strategy by Task Type

| Task Type               | Working      | Episodic                | Semantic                  | Procedural          |
| ----------------------- | ------------ | ----------------------- | ------------------------- | ------------------- |
| First turn, new session | Load task    | Empty                   | Query preferences         | Load role + skills  |
| Continuing session      | Update step  | Query recent events     | Query task-relevant facts | Stable (pre-loaded) |
| Resuming old session    | Load task    | Query prior decisions   | Query prior preferences   | Load role + skills  |
| Subagent delegation     | Load subtask | Forward relevant events | Forward relevant facts    | Scoped skills only  |

---

## Anti-Patterns to Avoid

| Anti-Pattern                                | Problem                                                       | Fix                                                            |
| ------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------- |
| Dumping all episodic memory into every turn | Token budget overflow; attention dilution                     | Query episodic memory by relevance; inject only what is needed |
| Using semantic memory as a conversation log | Semantic memory is for facts, not events                      | Use episodic memory for events; semantic for durable facts     |
| Compressing decisions and commitments       | Model contradicts itself or re-opens closed decisions         | Mark commitments as sacred; never compress                     |
| Storing procedural memory in retrieved slot | Conflicts with factual retrieved content; authority confusion | Procedural memory belongs in system slot only                  |
| Never expiring semantic memory              | Model reasons from stale facts                                | Set TTL on all semantic memory records                         |

---

**Version:** 1.0
**Last Updated:** 2026-04-28
**See also:** [Context Window Anatomy](./context-window-anatomy.md) · [Assembly Patterns](core-component-00/engineering/context-engineering/patterns/assembly-patterns.md) · [memory_store.py](core-component-00/engineering/context-engineering/implementations/memory_store.py)
