# Context Engineering Integration Guide

## How to Wire Context Engineering with Harness Engineering and RAG

This guide shows concrete integration patterns for combining `context-engineering/` with the other two production modules in `core-component-00`.

---

## Integration 1: Context Engineering + Harness Engineering

### The Relationship

Harness Engineering handles **runtime safety** (error boundaries, token limits, tool boundaries).
Context Engineering handles **information architecture** (what goes in the window before the call).

They are sequential: context engineering assembles the window → harness engineering executes the call safely.

```
[Context Engineering]       [Harness Engineering]
ContextAssembler.build()  → SafeModelCall.execute(context)
EpisodicMemory.record()   → ContextMonitor.check_budget()
```

### Integration Pattern

```python
from context_engineering.implementations.context_assembler import ContextAssembler
from context_engineering.implementations.memory_store import EpisodicMemory, SemanticMemory, WorkingMemory
from harness_engineering.implementations.context_monitor import ContextMonitor
from harness_engineering.implementations.error_boundary import SafeModelCall

# --- Session setup ---
assembler = ContextAssembler(max_tokens=128_000)
monitor = ContextMonitor(max_tokens=128_000)
episodic = EpisodicMemory(session_id=session_id)
semantic = SemanticMemory()

# --- Per-turn flow ---
async def handle_turn(user_input: str) -> str:
    # Step 1: Check harness budget BEFORE assembly
    if not monitor.check_budget(current_messages):
        current_messages = monitor.prune_conversation(keep_recent_turns=4)

    # Step 2: Retrieve relevant memory
    facts = semantic.query(user_input, top_k=3)
    recent_events = episodic.recent_turns(n=5)

    # Step 3: Assemble context
    assembler.reset()
    assembler.set_system(system_prompt)
    assembler.add_retrieved([{"content": f["value"], "source": f["key"]} for f in facts])
    assembler.add_history(current_messages + recent_events)
    assembler.add_sacred_context(*episodic.get_sacred_context())

    context = assembler.build(task_type=classify_task(user_input))

    # Step 4: Execute safely via harness
    safe_call = SafeModelCall(client, model_id="claude-opus-4", timeout=30)
    result = await safe_call.execute(
        prompt=context.messages,
        schema=output_schema,
    )

    # Step 5: Update memory
    episodic.advance_turn()
    episodic.record_event("general", f"User asked: {user_input[:50]}")

    return result["data"]
```

### Key Integration Points

| Context Engineering Output             | Harness Engineering Consumer                          |
| -------------------------------------- | ----------------------------------------------------- |
| `AssembledContext.total_tokens`        | `ContextMonitor` validates this stays within budget   |
| `AssembledContext.messages`            | `SafeModelCall.execute()` receives this as its prompt |
| `EpisodicMemory.get_sacred_context()`  | Fed into `ContextAssembler.add_sacred_context()`      |
| `ContextAssembler.build()` token count | `ContextMonitor.check_budget()` verifies pre-call     |

---

## Integration 2: Context Engineering + RAG

### The Relationship

RAG produces retrieved documents.
Context Engineering decides which of those documents to include, in which slot, and in what priority order.

```
[RAG]                           [Context Engineering]
VectorDB.search(query)       → ContextAssembler.add_retrieved(docs, relevance_scores)
Reranker.rerank(candidates)  → _priority_fill() uses relevance_scores from reranker
ACL.filter(docs, user)       → Filtered docs passed to assembler (pre-filtered)
```

### Integration Pattern

```python
from context_engineering.implementations.context_assembler import ContextAssembler
from context_engineering.implementations.context_compressor import ContextCompressor

# Assume these are your existing RAG components:
# embedding_service, vector_db, reranker, acl_controller

async def build_rag_context(query: str, user: User, max_tokens: int = 128_000):
    # Step 1: RAG retrieval
    query_embedding = await embedding_service.embed(query)
    candidates = await vector_db.search(query_embedding, top_k=20)

    # Step 2: ACL filter (BEFORE assembly — never filter after)
    authorised = acl_controller.filter(candidates, user=user)

    # Step 3: Rerank
    reranked = await reranker.rerank(query, authorised, top_k=10)
    relevance_scores = [r.score for r in reranked]
    docs = [{"content": r.content, "source": r.source, "timestamp": r.timestamp}
            for r in reranked]

    # Step 4: Compress documents that exceed per-doc budget
    compressor = ContextCompressor()
    compressed_docs = []
    per_doc_budget = (max_tokens * 0.30) // max(len(docs), 1)  # 30% retrieved slot
    for doc in docs:
        if len(doc["content"]) > per_doc_budget * 4:  # Rough char estimate
            result = compressor.extractive_compress(doc["content"], target_tokens=per_doc_budget)
            compressed_docs.append({**doc, "content": result.content})
        else:
            compressed_docs.append(doc)

    # Step 5: Assemble context
    assembler = ContextAssembler(max_tokens=max_tokens)
    assembler.set_system(system_prompt)
    assembler.add_retrieved(compressed_docs, query=query, relevance_scores=relevance_scores)

    return assembler.build(task_type="factual_qa")
```

### Key Integration Points

| RAG Output               | Context Engineering Consumer                                 |
| ------------------------ | ------------------------------------------------------------ |
| Vector search candidates | `ContextAssembler.add_retrieved()` with relevance scores     |
| Reranker scores          | Passed as `relevance_scores` to drive priority-fill ordering |
| ACL-filtered documents   | Must be filtered **before** passing to assembler             |
| Document timestamps      | Passed in doc metadata; used for recency scoring             |

---

## Integration 3: Full Stack (Context + Harness + RAG)

The complete production flow combining all three modules:

```
User Query
    ↓
[RAG] Retrieve relevant documents (vector search + rerank + ACL filter)
    ↓
[Context Engineering] Assemble context window
    - Load episodic memory (sacred context + recent events)
    - Load semantic memory (user preferences, project facts)
    - Inject retrieved documents (priority-scored)
    - Inject working memory (current task state)
    ↓
[Harness Engineering] Validate and execute
    - ContextMonitor: Check token budget before call
    - SafeModelCall: Execute with timeout + schema validation
    - Error boundary: Handle timeout / rate-limit / validation errors
    ↓
[Context Engineering] Update memory
    - Record turn in episodic memory
    - Extract and store any new decisions (mark as sacred)
    - Update working memory with task progress
    ↓
Response to user
```

---

## Common Mistakes

| Mistake                                            | Problem                                                           | Fix                                                                                                    |
| -------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Calling `ContextMonitor` before `ContextAssembler` | Monitor checks raw message list, missing assembled context        | Call assembler first; pass `AssembledContext.total_tokens` to monitor                                  |
| ACL filtering after assembly                       | Unauthorised content already in context                           | Always ACL-filter RAG results before passing to assembler                                              |
| Storing RAG results in episodic memory             | Episodic memory is for events, not documents                      | Documents belong in the retrieved slot; only the _decision to use_ a document goes in episodic         |
| Running compressor after assembler                 | Compression should happen before assembly to inform priority-fill | Compress individual documents before `add_retrieved()`; apply history compression inside the assembler |

---

**Version:** 1.0
**Last Updated:** 2026-04-28
**See also:** [Workspace Strategy](./strategy.md) · [context_assembler.py](core-component-00/engineering/context-engineering/implementations/context_assembler.py) · [Harness Engineering README](core-component-00/engineering/harness-engineering/README.md) · [RAG README](core-component-00/retrieval-augmented-generation/README.md)
