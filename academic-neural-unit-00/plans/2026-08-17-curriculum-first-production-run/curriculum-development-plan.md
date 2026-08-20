# ANU-00 Agent Development Curriculum — Development Plan

**Status:** Proposal — pending CEO approval (second review round)
**Prepared:** 2026-08-17
**Scope:** First full-draft production run of a bilingual (EN/ZH), three-level training textbook
series on agent development, plus its internal + external review cycle.

> This document is the CEO-facing proposal for how the curriculum will be produced. No textbook
> content, review, or template files described below have been written yet — only this plan and
> the empty directory skeleton it proposes. Implementation (running the authoring/review workflow)
> begins only after explicit CEO sign-off on this plan.

---

## 1. Context

The CEO wants ANU-00 to produce a bilingual (EN/ZH) introductory → intermediate → advanced
textbook series on agent development, rigorous enough that a graduate with no prior background
could pass real interviews at top AI labs and join ANU-00 or CC-00. Requirements from the CEO
brief:

1. Truthful, error-free content with verifiable sources for every formula/paper citation.
2. True bilingual writing — an English paragraph immediately followed by its Chinese translation,
   faithful/expressive/elegant (信达雅), never machine-like — one file, not two separate language
   files.
3. Written for a total beginner (no prior Agent development teaching/research background).
4. Benchmarked against internationally recognized standards, not just this workspace's internal
   conventions.
5. A two-tier review: ANU-00 internal reviewers check each document, then the ANU-00 Lead
   performs a comprehensive synthesis review over all internal reports plus a set of independent
   external reviews.

ANU-00 (`academic-neural-unit-00/`) already exists as a 10-person research org (crew, charter,
templates, knowledge-base) but has never produced a standing training-curriculum deliverable —
its existing `knowledge-base/` is scoped to point-in-time chartered-programme research reports,
not an evergreen textbook series. This plan adds a new top-level artifact category, two new
review templates, and a scripted multi-agent workflow (Claude Code's `Workflow` tool) to produce
and review the first full draft of the curriculum in one run, matching the model/effort tiers the
CEO specified (Opus 5 High Thinking for the Lead, Sonnet 5 High Thinking for team members).

Two scope decisions already confirmed with the CEO:

- External reviewers work **blind** — fresh agents with no ANU-00/CC-00 context, role-playing
  outside experts, to genuinely stress-test against real-world standards rather than workspace
  conventions.
- This run **stops after the Lead's comprehensive review report**. A revision pass (authors fixing
  flagged issues, re-review) is an explicit, separately-scoped follow-up run — not bundled into
  this one.

---

## 2. Directory structure (already created, currently empty except this file)

```
academic-neural-unit-00/curriculum/
├── curriculum-development-plan.md      ← this file
├── README.md                           ← (not yet written) category definition, audience,
│                                           bilingual + citation conventions, review process,
│                                           module index — written at Phase 1 (Charter)
├── introductory/                       ← 8 modules (empty, pending approval)
├── intermediate/                       ← 8 modules (empty, pending approval)
├── advanced/                           ← 8 modules (empty, pending approval)
└── reviews/
    ├── internal/                       ← 5 cluster review reports (empty, pending approval)
    ├── external/                       ← 2 blind external review reports (empty, pending approval)
    └── comprehensive-review.md         ← (not yet written) Lead's synthesis

academic-neural-unit-00/templates/curriculum/   ← (already created, empty) will hold the two new
                                                    review templates described in §3
```

Planned filenames for the 24 modules (level-prefixed, two-digit order, kebab-case), covering all
four CEO-selected topic areas at each level — Foundations; Agent Architecture & Design Patterns;
Prompt & Context Engineering; Multi-Agent Systems & Evaluation:

**`introductory/`**

1. `01-neural-networks-and-deep-learning-foundations.md`
2. `02-the-transformer-architecture-and-attention.md`
3. `03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`
4. `04-tool-use-and-function-calling-basics.md`
5. `05-prompt-engineering-fundamentals.md`
6. `06-context-windows-tokens-and-memory-basics.md`
7. `07-introduction-to-multi-agent-systems.md`
8. `08-why-and-how-we-evaluate-agents.md`

**`intermediate/`**

1. `01-training-dynamics-optimization-and-generalization.md`
2. `02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`
3. `03-agent-design-patterns-react-plan-execute-reflexion.md`
4. `04-agent-memory-systems-short-term-long-term-episodic.md`
5. `05-advanced-prompting-cot-few-shot-structured-output.md`
6. `06-rag-fundamentals-retrieval-embeddings-and-grounding.md`
7. `07-multi-agent-communication-and-coordination-protocols.md`
8. `08-evaluating-agent-systems-benchmarks-and-methodology.md`

**`advanced/`**

1. `01-scaling-laws-and-emergent-capabilities.md`
2. `02-mixture-of-experts-and-modern-architecture-variants.md`
3. `03-agent-harness-engineering-production-grade-agent-loops.md`
4. `04-agentic-safety-guardrails-and-governance-patterns.md`
5. `05-advanced-context-engineering-long-context-and-budgeting.md`
6. `06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`
7. `07-multi-agent-orchestration-worktree-isolation-and-consensus.md`
8. `08-rigorous-agent-evaluation-statistical-methodology.md`

**`reviews/internal/`:** `foundations-cluster-review.md`,
`agent-architecture-cluster-review.md`, `prompt-context-cluster-review.md`,
`multi-agent-evaluation-cluster-review.md`, `structural-bilingual-taxonomy-review.md`.

**`reviews/external/`:** `external-technical-accuracy-review.md`,
`external-interview-readiness-review.md`.

`curriculum/README.md` will document: purpose and audience, why this is a distinct category from
`knowledge-base/` (standing training material, not a chartered-programme finding), the bilingual
paragraph-pairing convention, the citation convention (§4 below), the review process, and an index
table of all 24 modules with author/reviewer attribution.

---

## 3. Two new templates (not yet written)

Location: `academic-neural-unit-00/templates/curriculum/` (directory already created).

- **`internal-review-report.md`** — for ANU-00 crew peer review. Sections: reviewer identity +
  cluster/docs covered; per-document checklist (factual accuracy, citation validity, pedagogical
  fit for a zero-background reader, bilingual quality — flag anything "machine-like" —, structural
  completeness); a required "problems found" table (doc, location, issue, severity); an explicit
  null-result rule (a clean doc must say so, not be left blank); reviewer's per-doc verdict
  (pass / needs revision).
- **`external-review-report.md`** — for the blind outside-expert pass. Sections: reviewer's
  assumed persona and evaluation lens (technical-accuracy vs. interview-readiness); the specific
  external standard(s) benchmarked against (named courses/textbooks/papers, with links); a claim
  spot-check table (claim, doc/location, verified against, verdict); a citation audit (every
  formula/paper citation found, checked for existence and correct representation); an overall
  "would this curriculum get someone through a real interview" verdict with reasoning.

Both templates will get a one-line entry added to `academic-neural-unit-00/templates/README.md`'s
inventory, consistent with its existing format.

The **Lead's comprehensive review** deliberately reuses the existing root
`templates/review-records/final-review.md` unchanged — this matches ANU-00's own stated
convention (multi-party sign-off on completed work reuses the root template rather than growing a
twin). Its "Method" table will cite the 5 internal + 2 external review reports as the records
checked, one `## [Reviewer] — [Area]` section per review synthesized, ending in a per-document
Joint Recommendation.

---

## 4. Content conventions (to be enforced via the authoring prompt, checked in review)

- **Bilingual pairing:** every paragraph (including headers/callouts) is written in English, then
  immediately followed by its Chinese translation as the next paragraph — one file, not two.
  Translation must read as native technical Chinese (信达雅), not transliteration.
- **Citations:** a `## References` section at the end of each doc, split into `### External
Sources` (real papers/textbooks/courses, markdown-linked — e.g. arXiv links, Goodfellow et al.,
  Sutton & Barto, Vaswani et al. "Attention Is All You Need", Stanford CS224N/CS231n,
  Anthropic/OpenAI engineering docs) and `### Internal Cross-References` (other curriculum docs).
  Authors must use web search/fetch to verify every cited paper/formula actually exists and is
  represented correctly — no fabricated citations. This directly satisfies the CEO's accuracy
  requirement and the "internationally recognized, not local workspace" standard.
- **Audience:** zero prior background — introductory docs must not assume ML/CS coursework;
  intermediate/advanced build strictly on what earlier docs already taught.

---

## 5. Production workflow (to run only after CEO approval of this plan)

Uses Claude Code's `Workflow` tool rather than manual agent-by-agent orchestration, because the
CEO specified two distinct model/effort tiers (Opus 5 High Thinking for the Lead, Sonnet 5 High
Thinking for team members) and `Workflow`'s per-call `model`/`effort` options are the only
mechanism that can set both together.

**Phase 1 — Charter (1 agent, Opus/high):** Dr. Naledi Mokoena (ANU-00 Lead) reads her profile +
skill file, charters the curriculum programme, and finalizes the module→author assignment table
below. Output: `curriculum/README.md`.

**Phase 2 — Author (8 agents, Sonnet/high, parallel):** one agent per crew member, each producing
all of that member's assigned docs (full bilingual text + verified references) in one call,
matched to crew specialization:

| Author                                            | Docs                                                     |
| ------------------------------------------------- | -------------------------------------------------------- |
| Dr. Yuna Baek (AI/Neural Networks)                | Intro 01, Intro 02, Inter 02, Adv 02                     |
| Dr. Samuel Okonkwo (ML Theory)                    | Inter 01, Adv 01                                         |
| Dr. Kaito Fujimori (Agent Coordination Theory)    | Intro 03, Intro 04, Inter 03, Adv 04, Intro 07, Inter 07 |
| Dr. Inés Roldán (Software Engineering Research)   | Inter 04, Adv 03                                         |
| Dr. Wei-Ling Tan (Applied AI Feasibility)         | Intro 05, Inter 05, Adv 05, Adv 06                       |
| Dr. Rafael Ibarra-Costa (Cross-Domain Generalist) | Intro 06, Inter 06                                       |
| Dr. Mireille Dubois (LLM Evaluation)              | Intro 08, Inter 08, Adv 08                               |
| Dr. Aditi Bhandari (Foundational AI Lead)         | Adv 07                                                   |

**Phase 3 — Internal review (5 agents, Sonnet/high, parallel, after Phase 2):** cross-cluster peer
review — no one reviews their own cluster:

| Reviewer                | Reviews                                                                 |
| ----------------------- | ----------------------------------------------------------------------- |
| Dr. Mireille Dubois     | Foundations cluster (6 docs)                                            |
| Dr. Aditi Bhandari      | Agent Architecture cluster (6 docs)                                     |
| Dr. Yuna Baek           | Prompt & Context cluster (6 docs)                                       |
| Dr. Rafael Ibarra-Costa | Multi-Agent & Evaluation cluster (6 docs)                               |
| Tobias Lindqvist        | All 24 docs — structural/taxonomy/bilingual-formatting consistency only |

**Phase 4 — External blind review (2 agents, Sonnet/high, parallel, after Phase 2):** fresh
agents, no ANU-00/CC-00 context, given only the finished doc files:

- Reviewer A: "outside PhD-level AI researcher" — technical-accuracy + citation-audit lens.
- Reviewer B: "hiring manager/technical interviewer at a top AI lab" — interview-readiness lens,
  explicitly benchmarking against named real courses/papers/industry bars.

**Phase 5 — Comprehensive review (1 agent, Opus/high, after Phases 3 & 4):** Dr. Mokoena reads
all 5 internal + 2 external review reports and produces `curriculum/reviews/
comprehensive-review.md` as a filled root `final-review.md` — a per-document pass/needs-revision
verdict plus an overall Joint Recommendation for the CEO.

**Total: 17 agents** (1 + 8 + 5 + 2 + 1) — above this session's 15-agent default guideline,
justified by the CEO's explicit "Large (7+ docs/level)" scope choice; flagged here for
transparency rather than silently exceeded.

---

## 6. Verification (after the workflow run)

- File count check: 24 docs + 5 internal reviews + 2 external reviews + 1 comprehensive review =
  32 new files, plus `curriculum/README.md` and the 2 new templates.
- Confirm every doc has interleaved EN/ZH paragraphs and a non-empty `## References` section with
  real, resolvable external links.
- Run `prettier --write` over every created/modified Markdown file per workspace convention.
- Spot-check 2–3 citations per level against their linked source to confirm no fabricated
  references slipped through.
- Read `comprehensive-review.md` to confirm it reaches a clear per-document verdict rather than
  restating the sub-reports.
- Report back: what passed outright, what the Lead flagged as needing revision, and a recommended
  scope for the follow-up revision run.

---

## 7. Approval gate

**Next step:** CEO reviews this document (directory structure, module list, author/reviewer
assignments, template design, workflow architecture, and the 17-agent scope). Implementation
(running Phases 1–5 above) begins only after explicit CEO sign-off here.
