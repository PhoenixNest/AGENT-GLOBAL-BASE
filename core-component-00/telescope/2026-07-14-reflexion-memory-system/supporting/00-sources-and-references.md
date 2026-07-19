# Supporting Document 00 — Sources and References

**Programme:** `2026-07-14-reflexion-memory-system`
**Purpose:** Full bibliography for every external claim cited in `research-report.md` and its
supporting documents. This is the authoritative source list — the main report's References
section is a condensed pointer to this file, not a substitute for it.

---

## Anthropic / Claude Research Team Sources

| #   | Source                                                                    | Retrieved                                                                                                   | Used For                                                                                                                                                                    |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Bai, Y. et al., "Constitutional AI: Harmlessness from AI Feedback" (2022) | From established knowledge, cross-checked against `crew/director/elias-vance/agent/profile.md` (2026-07-14) | Finding 1 — the critique-then-revise-against-a-standing-principle-set pattern; Dr. Vance's own founding-contributor lineage                                                 |
| 2   | Anthropic Engineering — "How we built our multi-agent research system"    | 2026-07-14 (live web fetch)                                                                                 | Finding 1 — tool-testing agent's diagnose-and-rewrite loop; external-memory-under-truncation pattern; lead-agent synthesis/iteration loop; citation-agent verification pass |
| 3   | Wire Blog — "Anthropic's Managed Agents memory: what it changes"          | 2026-07-14 (live web fetch)                                                                                 | Finding 1 — audit-first design (per-write timestamp/source attribution/rollback), freshness model and "context poisoning" warning, per-agent/per-workspace/shared scoping   |

**Freshness note:** Sources 2 and 3 describe features (a 2025 multi-agent research system writeup
and an April 2026 Managed Agents public beta) that sit at or past this investigator's training
cutoff. Both were retrieved via live web search on 2026-07-14 specifically because of this,
consistent with this workspace's RAG freshness protocol — they are not recalled from training
data. Source 1 (Constitutional AI, 2022) is well-established prior art within training data and
was not re-fetched; it is corroborated by an internal document (Dr. Vance's own crew profile)
already citing it as a founding contribution, which is treated as independent internal
confirmation rather than circular sourcing, since the profile predates this investigation.

---

## Academic / Industry Comparator Sources

| #   | Source                                                                                                             | Retrieved                                        | Used For                                                                                                                    |
| --- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| 4   | Shinn, N. et al., "Reflexion: Language Agents with Verbal Reinforcement Learning," NeurIPS 2023 (arXiv:2303.11366) | 2026-07-14 (live web fetch, arXiv abstract page) | Finding 2 — Actor/Evaluator/Self-Reflection triad; episodic memory buffer of reflections; 91% pass@1 HumanEval result       |
| 5   | `github.com/noahshinn/reflexion` (official repository)                                                             | 2026-07-14 (live web fetch)                      | Finding 2 — `ReflexionStrategy` enum confirming reflection as a distinct, selectable strategy layered over ordinary history |
| 6   | Park, J. S. et al., "Generative Agents: Interactive Simulacra of Human Behavior" (2023; ar5iv:2304.03442)          | 2026-07-14 (live web search synthesis)           | Finding 3 — importance-gated reflection-tree construction; recency+importance+relevance retrieval scoring                   |
| 7   | AgentPatterns.ai — "Generative Agents Memory Stream: Three-Layer Architecture for Long-Running Agent Sessions"     | 2026-07-14 (search result summary)               | Finding 3 — secondary confirmation of the reflection-tree abstraction mechanism                                             |

---

## Internal Workspace Sources

| #   | Source                                                                                                      | Purpose                                                                                                                                                                                                             |
| --- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 8   | `core-component-00/context-engineering/implementations/memory_store.py`                                     | Existing four-type taxonomy (`EpisodicEvent`, `SemanticFact`, `ProceduralMemory`, `WorkingMemory`); `SACRED_EVENT_TYPES`; `event_type == "error"` as the nearest existing attachment point                          |
| 9   | `core-component-00/mcp-servers/agent-memory/README.md`                                                      | Current live architecture: 3 Qdrant collections, JSONL-first source of truth, `active → dormant → archived` lifecycle, `sacred` flag, and — critically — the explicit, reasoned absence of a write-capable MCP tool |
| 10  | `core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md` (+ its `supporting/`) | Prior programme establishing the Memory-as-Corpus principle, the decay/consolidation policy, and the precedent for benchmarking against Anthropic + academic SOTA before designing                                  |
| 11  | `REFLECT-004` in the `memory_reflection` collection (formerly the 2026-07-13-mcp-embedder-service-redesign Programme's `MISTAKE-001`) | The standing, named commitment this report closes: "the workspace's reflexion framework... is not yet operational... entries are migrated into it"                                                                  |
| 12  | `core-component-00/agent-systems-engineering/governance/adr-ase-001.md` (EX-001 Exceptions Log entry)       | Governance-level precedent for formally logging and closing a remediated finding, distinct from but complementary to the reflexion design                                                                           |
| 13  | `crew/director/elias-vance/agent/profile.md`; `crew/safety-evaluation/tomasz-wieczorek/agent/profile.md`    | Investigator/self-reviewer identity, authority scope, and — for Dr. Vance specifically — direct lineage to Constitutional AI                                                                                        |

---

## Sources Considered and Not Cited

- MemGPT/Letta, Mem0, and Zep/Graphiti — all three were already surveyed in depth by the prior
  `2026-07-10-agent-memory-architecture` programme for general memory-decay design. This
  investigation deliberately did not re-survey them, since the CEO's mandate here is specifically
  a _reflection_ system benchmarked against Anthropic's own team plus top-tier reflection-specific
  architectures (Reflexion, Generative Agents), not a re-run of the general memory-architecture
  survey. Their findings remain valid and are referenced by pointer, not duplicated.

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-14-reflexion-memory-system`
