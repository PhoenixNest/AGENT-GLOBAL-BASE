# Phase 1 Audit — Internal Cross-Reference Links & Non-Public Citations

**Round:** 2026-08-26 external-audience remediation
**Scope:** All 24 curriculum modules (`introductory/`, `intermediate/`, `advanced/`) plus
`curriculum/README.md`, per
`academic-neural-unit-00/plans/2026-08-26-curriculum-external-audience-remediation/external-audience-remediation-plan.md`
§6 Phase 1.
**Method:** Full-corpus pattern scan (`grep -oE`) for every Markdown link pointing at a
workspace-relative path, plus a targeted scan for prose citations of non-public internal
documents by path. Every match was spot-checked against its surrounding line to confirm it is a
genuine workspace-relative reference, not a code sample or false positive.

---

## 1. Internal cross-reference link mesh

**694 links** found across all 25 files, all following one uniform pattern:

```
[<link text>](/academic-neural-unit-00/curriculum/<tier>/<NN-slug>.md[#<anchor>])
```

`<tier>` is one of `introductory`, `intermediate`, `advanced`. Every link resolves only inside
this repository (workspace-root-relative path); none is reachable by a reader without repository
access, confirming plan §2 item 1.

This uniformity matters for Phase 3: since every one of the 694 links shares the same regex-
matchable shape, the conversion in Phase 3(a) is done as a single scripted, masked pass rather
than 694 individual hand-edits.

### Per-file link count

| File                                                                             |   Links |
| -------------------------------------------------------------------------------- | ------: |
| `curriculum/README.md`                                                           |       0 |
| `advanced/01-scaling-laws-and-emergent-capabilities.md`                          |       7 |
| `advanced/02-mixture-of-experts-and-modern-architecture-variants.md`             |      62 |
| `advanced/03-agent-harness-engineering-production-grade-agent-loops.md`          |      20 |
| `advanced/04-agentic-safety-guardrails-and-governance-patterns.md`               |      62 |
| `advanced/05-advanced-context-engineering-long-context-and-budgeting.md`         |      18 |
| `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`             |      15 |
| `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`      |      31 |
| `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`               |      69 |
| `intermediate/01-training-dynamics-optimization-and-generalization.md`           |       7 |
| `intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md` |      24 |
| `intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md`          |      34 |
| `intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`          |      17 |
| `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`           |      13 |
| `intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md`         |      39 |
| `intermediate/07-multi-agent-communication-and-coordination-protocols.md`        |      29 |
| `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md`         |      55 |
| `introductory/01-neural-networks-and-deep-learning-foundations.md`               |      10 |
| `introductory/02-the-transformer-architecture-and-attention.md`                  |      29 |
| `introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`             |      27 |
| `introductory/04-tool-use-and-function-calling-basics.md`                        |      21 |
| `introductory/05-prompt-engineering-fundamentals.md`                             |       3 |
| `introductory/06-context-windows-tokens-and-memory-basics.md`                    |      32 |
| `introductory/07-introduction-to-multi-agent-systems.md`                         |      39 |
| `introductory/08-why-and-how-we-evaluate-agents.md`                              |      31 |
| **Total**                                                                        | **694** |

This matches the plan's own estimate ("~700 links," §1) built during reader-feedback-log Entries
12–13.

**Note on `curriculum/README.md`:** 0 links matching the internal-link pattern were found — its
existing cross-references to individual modules use a different (already-relative-within-the-repo
but differently formatted) convention. Flagged for the Lead to confirm out of an abundance of
caution; not counted in the 694 since it does not match the uniform pattern the Phase 3 script
targets. [See Agent B's companion report for a targeted second look if the Lead wants one.]

## 2. Citations to non-public internal documents

Two distinct citations of `core-component-00/` paths were found, of materially different
severity:

| Location                                                                                                                                        | Cited path                                                                                         | Severity                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Notes |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`, §4 (lines ~138–251, two citations at lines 168 and 171, EN + ZH)   | `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md` | **High** — this is Pass 3's original S-1 finding. The entire §4 case study ("Git Worktree Isolation as Multi-Agent Infrastructure") is built around a real internal incident and cites this document as its primary, load-bearing source. Unreachable and unverifiable by an outside reader. Per plan §2 item 2, needs either a citable public-source reframe or demotion to a secondary internal note behind a public-source primary example.                                                                                                                                                                             |
| `advanced/05-advanced-context-engineering-long-context-and-budgeting.md`, §7 table, "Compaction and retrieval as escape valves" row (line ~302) | `core-component-00/engineering/context-engineering/` (directory, not a specific document)          | **Low** — a single parenthetical aside ("a technique developed further in `core-component-00/engineering/context-engineering/`-style production systems this curriculum does not duplicate here"). Not cited as evidence for a claim; the sentence's actual claim stands on its own without the citation. Easiest fix: drop the parenthetical or generalize it to "in production context-engineering systems" without the internal path. Not previously flagged by Pass 3 (outside the one passage the external reviewers happened to hit) — new finding from this audit, in scope per plan §2 item 4 (corpus-wide sweep). |

No other `core-component-00/`, `company/`, or `studio/` path citations were found anywhere else
in the 25-file corpus.

## 3. Non-md internal citation scan (secondary check)

A separate scan for internal citations not in Markdown-link form (bare paths in prose or code
spans) turned up only the two rows in §2 above — no additional hits.

---

**Handoff to Phase 3:** every link in §1 shares one regex-matchable shape
(`\]\(/academic-neural-unit-00/curriculum/[^)]+\.md[^)]*\)`) — safe for a single scripted,
masked-and-verified conversion pass rather than manual editing. The two §2 citations need
different treatment: `advanced/07` needs substantive authoring (case-study reframe), `advanced/05`
needs a one-line trim.
