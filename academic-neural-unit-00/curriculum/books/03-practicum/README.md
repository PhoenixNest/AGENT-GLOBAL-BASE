# curriculum/practicum/ — Hands-On Coding Practicum (S2 Extension)

Bilingual (EN/ZH) hands-on coding companion to the standing 24-module curriculum, produced by
ANU-00 crew. Chartered 2026-08-27 by Dr. Naledi Mokoena, ANU-00 Lead, under CEO approval of
`academic-neural-unit-00/plans/2026-08-19-curriculum-coding-and-post-training-extension/curriculum-extension-plan.md`
(the "S2 plan") — Phase 1 of that plan's §4 production workflow.

Read this file before authoring or reviewing anything under `curriculum/practicum/`. It governs
this category's own additions on top of — not instead of — `curriculum/README.md`, which stays
canonical for everything it already covers.

---

## 1. Relationship to `curriculum/README.md`

This is a new sibling category to `introductory/`, `intermediate/`, and `advanced/`, not a
replacement for any convention those already follow. Every rule in `curriculum/README.md` still
binds practicum modules without change:

- §1 Purpose and Audience — same reader, same external interview-readiness bar.
- §4 Bilingual Format, §4.1 Metadata Block, §4.2 Ratified Terminology, §4.4 Section Citation
  Notation — all explanatory prose in a practicum module follows the same EN-paragraph-then-
  ZH-paragraph pattern, the same three-row metadata table, the same ratified Chinese renderings.
- §5 Citations — every claim still traces to a verified external source; the "not knowing is a
  permitted answer" rule still applies.
- §6 Review Process pattern (internal → external → synthesis) — reused in the shape the S2 plan's
  own §4 defines (Phase 3/4/5), not repeated here.
- §8 Rules for Authors and Reviewers — unchanged.

This file adds exactly two things the main README does not need: how code blocks are handled, and
the module→author table for this category. Where this file is silent, `curriculum/README.md`
governs.

**One convention note specific to code:** code blocks themselves are written once, language-
neutral, exactly as formulas and tables already are under `curriculum/README.md` §4 — only the
explanatory prose introducing or walking through a code block is bilingual-paired.

---

## 2. Purpose

Closes the first of two gaps `curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md`
recorded under scope decision **S-2**: zero runnable code anywhere in the existing 24-module
corpus. External Reviewer B (hiring-manager persona) found this bears directly on the curriculum's
own stated goal — a reader who completes it should be able to hold their own in a real technical
interview at a serious AI lab. Practicum modules do not replace or edit any of the existing 24
modules; those stay exactly as they are. Each practicum module pairs with a concept the main
curriculum already taught, names that module as its explicit prerequisite (per the existing "must
name which module" rule, `curriculum/README.md` §1), and walks the reader through building the
code themselves, step by step with the reasoning for each step — not a solved solution dropped
whole.

The second S-2 gap (zero RLHF/post-training coverage) is closed separately, as `advanced/09` — Reinforcement Learning from Human Feedback and
`advanced/10` — Modern Post-Training Methods: DPO, GRPO & Reward Modeling inside the existing `curriculum/advanced/` folder — see `curriculum/README.md`
Amendment 5 for that ratification. This file covers the practicum category only.

---

## 3. The No-Application-Code Boundary (hard constraint)

Root `CLAUDE.md` §2 and `academic-neural-unit-00/CLAUDE.md` both state that no application code
lives under `academic-neural-unit-00/` — runnable code lives exclusively in `core-component-00/`.
This is a hard boundary, not a style choice, and it binds every practicum module without
exception:

- A practicum module is a markdown document containing complete, correct Python **code blocks**
  the reader copies and runs on their own machine. It is teaching material that reads as code, not
  application code this repository executes.
- No practicum module may commit an executable file (`.py`, `.ipynb`, or any other runnable
  artifact) anywhere under `academic-neural-unit-00/`. Every exercise lives entirely inside
  fenced code blocks in the module's own markdown file.
- Every practicum author must be briefed on this constraint explicitly before authoring begins —
  restated here so Phase 2 (Author) inherits it directly from this charter rather than from a
  paraphrase.

---

## 4. Code Verification Rule (new, practicum-specific)

Every code block must be independently executed or hand-traced by its own author before the
module is filed. A claim that code "works" is not sufficient on its own — the author's
verification method (mental trace, scratch-run, or cited test) must be stated in the module
itself, next to the code block it verifies. This is the same evidentiary standard
`curriculum/README.md` §5 already holds formula and citation claims to, applied here to code.

Internal review (Phase 3 of the S2 plan) adds a fourth structural check on top of the existing
three (`curriculum/README.md` §4.3's rendering checks): does every code block show its
verification method. External review (Phase 4) additionally confirms every practicum code block
is actually correct Python that produces the claimed output — not just that a verification-method
line is present.

---

## 5. Module → Author Table (ratified at charter)

Six modules. Filenames are level-prefixed, two-digit ordered, kebab-case — same convention as
`curriculum/README.md` §7.1. Author assignment matches each crew member's documented specialty on
the roster (`academic-neural-unit-00/crew/README.md`), consistent with the S2 plan §2.1.

| #   | Title                                    | Filename                                           | Pairs With                                                                        | Author                                                                  |
| --- | ---------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 01  | Building a Basic Agent Loop              | `01-building-a-basic-agent-loop.md`                | `introductory/03` — What Is an AI Agent? Concepts & the Agent Loop                | Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00 |
| 02  | Implementing Tool Use & Function Calling | `02-implementing-tool-use-and-function-calling.md` | `introductory/04` — Tool Use & Function Calling Basics                            | Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00 |
| 03  | Building a ReAct Agent From Scratch      | `03-building-a-react-agent-from-scratch.md`        | `intermediate/03` — Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion    | Dr. Inés Roldán, Research Scientist — Software Engineering / CS, ANU-00 |
| 04  | Building a Minimal RAG Pipeline          | `04-building-a-minimal-rag-pipeline.md`            | `intermediate/06` — RAG Fundamentals: Retrieval, Embeddings & Grounding           | Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00        |
| 05  | Implementing Scored Agent Memory         | `05-implementing-scored-agent-memory.md`           | `intermediate/04` — Agent Memory Systems: Short-Term, Long-Term & Episodic Memory | Dr. Inés Roldán, Research Scientist — Software Engineering / CS, ANU-00 |
| 06  | Building an Agent Evaluation Harness     | `06-building-an-agent-evaluation-harness.md`       | `intermediate/08` — Evaluating Agent Systems: Benchmarks & Methodology            | Dr. Mireille Dubois, Research Scientist — LLM Systems, ANU-00           |

This table is the sign-off required by
`crew/lead/naledi-mokoena/skills/research-programme-chartering.md` §5, applied here to a training
deliverable rather than a research programme, and it is not delegable. It is finalized as of this
charter and does not change without a new Lead ratification.

**Roster cross-check:** all four authors above are current ANU-00 crew members
(`academic-neural-unit-00/crew/README.md`), and each assignment matches the same specialty mapping
`curriculum/README.md` §7.2 already used for that author's original modules — no new fit
justification needed. No author reviews their own practicum module at Phase 3, per the same
no-self-review rule `curriculum/README.md` §6 states for the main corpus.

---

## 6. Directory Structure

```
curriculum/books/03-practicum/
├── README.md                                          ← this file
├── 01-building-a-basic-agent-loop.md
├── 02-implementing-tool-use-and-function-calling.md
├── 03-building-a-react-agent-from-scratch.md
├── 04-building-a-minimal-rag-pipeline.md
├── 05-implementing-scored-agent-memory.md
└── 06-building-an-agent-evaluation-harness.md
```

No module files exist yet as of this charter (Phase 1) — authoring is Phase 2 of the S2 plan's §4
production workflow, which has not started under this document.

---

**Ratified by:** Dr. Naledi Mokoena, ANU-00 Lead — 2026-08-27
**Under:** CEO approval of
`academic-neural-unit-00/plans/2026-08-19-curriculum-coding-and-post-training-extension/curriculum-extension-plan.md`,
Phase 1 (Charter) of that plan's §4
**Roster cross-check:** `academic-neural-unit-00/crew/README.md`, confirmed consistent 2026-08-27
