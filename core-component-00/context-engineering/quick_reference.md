# Context Engineering Quick Reference

## Slot Budget by Task Type

| Task Type               | System | History | Retrieved | Tool Output | Notes                  |
| ----------------------- | ------ | ------- | --------- | ----------- | ---------------------- |
| Factual Q&A             | 10%    | 10%     | 65%       | 15%         | Maximise retrieval     |
| Code generation         | 15%    | 20%     | 45%       | 20%         | Balance spec + history |
| Creative writing        | 20%    | 50%     | 20%       | 10%         | History carries voice  |
| Tool-augmented research | 10%    | 15%     | 35%       | 40%         | Tools dominate         |
| Multi-turn reasoning    | 15%    | 55%     | 20%       | 10%         | History is the state   |
| Agent orchestration     | 20%    | 10%     | 30%       | 40%         | System + tools lead    |

---

## Memory Type Selector

| I need to...                       | Memory Type | Lifespan    | Implementation                   |
| ---------------------------------- | ----------- | ----------- | -------------------------------- |
| Track what happened this session   | Episodic    | Session     | `EpisodicMemory`                 |
| Store facts that outlive sessions  | Semantic    | Persistent  | `SemanticMemory`                 |
| Encode how to behave in situations | Procedural  | Persistent  | `ProceduralMemory`               |
| Track current sub-goal progress    | Working     | Single turn | `WorkingMemory` (active context) |

---

## Context Assembly Decision Matrix

| Condition                              | Action                                           |
| -------------------------------------- | ------------------------------------------------ |
| Token budget > 90% before assembly     | Compress history first                           |
| Task is retrieval-heavy                | Increase retrieved slot to 50–65%                |
| Session > 20 turns                     | Summarise history into a single episodic entry   |
| Subagent delegation                    | Use scoped handoff — system + task excerpt only  |
| New session, known user                | Load semantic memory; skip episodic              |
| Contradictory retrieved content        | Label sources; let model adjudicate              |
| User input contains injection patterns | Validate before history append; reject if unsafe |

---

## Compression Priority Ladder

Compress in this order (highest priority to keep → lowest):

1. **Decisions and commitments** — never compress
2. **Tool outputs (validated)** — schema-reduce only
3. **System instructions** — never compress
4. **Current task / working memory** — never compress
5. **Recent conversation turns (last 3)** — compress lightly
6. **Retrieved documents** — extractive summarise
7. **Old conversation turns** — hierarchical summarise
8. **Resolved errors / retry attempts** — discard

---

## Context Quality Threat Detection

| Signal                                                 | Threat                          | Response                                       |
| ------------------------------------------------------ | ------------------------------- | ---------------------------------------------- |
| Model contradicts a prior commitment                   | Context poisoning or role drift | Re-inject commitment verbatim into system slot |
| Model repeats the same answer across turns             | Echo chamber                    | Inject a challenge probe in next turn          |
| Retrieved content references dates > 6 months ago      | Staleness                       | Add freshness filter; flag to user             |
| Response confidence is high but factual accuracy drops | Attention dilution              | Move key facts to beginning/end of their slot  |
| User message contains `"ignore previous"`              | Prompt injection                | Block history append; log security event       |

---

## Multi-Agent Handoff Tier Selection

| Scenario                              | Tier                | What to Forward                         |
| ------------------------------------- | ------------------- | --------------------------------------- |
| Subagent continues the same task      | Full                | Entire context window                   |
| Subagent handles one bounded sub-task | Scoped              | System + task excerpt + relevant memory |
| Subagent is a pure tool wrapper       | Minimal             | System + task description only          |
| Subagent is untrusted / third-party   | Minimal + sanitised | System only; no history or memory       |

---

## Token Budget Thresholds

| Threshold   | Action                                              |
| ----------- | --------------------------------------------------- |
| < 60% used  | Healthy — proceed normally                          |
| 60–75% used | Monitor — log usage rate                            |
| 75–85% used | Warn — compress history on next turn                |
| 85–90% used | Prune — compress history immediately                |
| > 90% used  | Block — do not call model; emergency compress first |

---

## Implementation File Map

| Need                                 | File                                                                        |
| ------------------------------------ | --------------------------------------------------------------------------- |
| Assemble a full context window       | `implementations/context_assembler.py` — `ContextAssembler`                 |
| Store and retrieve episodic events   | `implementations/memory_store.py` — `EpisodicMemory`                        |
| Store and retrieve persistent facts  | `implementations/memory_store.py` — `SemanticMemory`                        |
| Track current task state             | `implementations/memory_store.py` — `WorkingMemory`                         |
| Compress history intelligently       | `implementations/context_compressor.py` — `ContextCompressor`               |
| Prepare a multi-agent handoff packet | `implementations/context_assembler.py` — `ContextAssembler.build_handoff()` |
