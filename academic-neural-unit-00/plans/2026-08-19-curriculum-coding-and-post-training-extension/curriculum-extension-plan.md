# ANU-00 Curriculum Extension — Hands-On Coding & Post-Training Track — Implementation Plan

**Status:** Approved by CEO; execution in progress — Phase 1 (Charter) and Phase 2 (Author)
complete, Phase 3 (Internal review) not yet started
**Prepared:** 2026-08-19
**Scope:** A bounded extension to the existing 24-module curriculum — a hands-on coding practicum
plus two new post-training modules — addressing the S-2 gap the Pass 3 comprehensive review
escalated (zero runnable code, zero RLHF/post-training coverage anywhere in the current corpus).

> This document is the CEO-facing proposal for how the extension will be produced. No practicum
> content, new modules, or review files described below have been written yet — only this plan.
> Implementation begins only after explicit CEO sign-off, the same gate the original
> `curriculum-development-plan.md` used.

---

## 1. Context

`academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md`
recorded, under scope decision **S-2**, two gaps mechanically confirmed across all 24 existing
modules: zero lines of runnable code, and zero substantive coverage of RLHF, DPO, PPO, GRPO, or
reward modeling (those terms appear only inside cited-paper titles, never in body text). Neither
was a defect against any author — no coding track or post-training coverage was ever in the
original ratified scope — but External Reviewer B, evaluating explicitly as a hiring-manager
persona, found both gaps bear directly on the curriculum's own stated goal: that a reader who
completes it should be able to "hold their own in a real technical interview at a serious AI lab."
The Pass 3 review recommended that closing this gap, if the CEO wants the interview-readiness claim
to hold at full strength, requires a second production run producing new material — not edits to
the existing 24 modules, which stay exactly as they are.

This plan is that second production run, scoped narrowly to the two named gaps only. It reuses
every convention already ratified in `curriculum/README.md` (audience, bilingual format, citation
rule, review process) rather than inventing new ones, and follows the same plan → CEO approval →
scripted `Workflow` production → review pattern the first run used.

**One binding constraint this plan must respect that the first run did not need to consider:**
root `CLAUDE.md` and `academic-neural-unit-00/CLAUDE.md` both state that no application code lives
under `academic-neural-unit-00/` — runnable code lives exclusively in `core-component-00/`. The
practicum therefore cannot commit executable files (`.py`, notebooks, etc.) into this tree. Every
exercise is authored as markdown containing complete, correct Python **code blocks** the reader
copies and runs on their own machine — teaching material that reads as code, not application code
this repository executes. This is a hard boundary, not a style choice, and every practicum author
must be briefed on it explicitly.

---

## 2. What Gets Added

### 2.1 Practicum — 6 new modules, new `curriculum/practicum/` directory

A new sibling category to `introductory/`, `intermediate/`, `advanced/` — not interleaved into the
existing 24, so none of their filenames or numbering changes. Each practicum module pairs with a
concept the main curriculum already taught, adds a complete, runnable (by the reader, locally)
Python code listing, and keeps the same bilingual EN/ZH paragraph convention for all explanatory
prose — only the code blocks themselves are language-neutral, per the existing bilingual-format
rule for code/formulas.

| #   | Module                                   | Pairs with                                  | Author                  |
| --- | ---------------------------------------- | ------------------------------------------- | ----------------------- |
| 01  | Building a Basic Agent Loop              | `introductory/03` (the agent loop)          | Dr. Kaito Fujimori      |
| 02  | Implementing Tool Use & Function Calling | `introductory/04`                           | Dr. Kaito Fujimori      |
| 03  | Building a ReAct Agent From Scratch      | `intermediate/03` (ReAct, Plan-and-Execute) | Dr. Inés Roldán         |
| 04  | Building a Minimal RAG Pipeline          | `intermediate/06` (RAG fundamentals)        | Dr. Rafael Ibarra-Costa |
| 05  | Implementing Scored Agent Memory         | `intermediate/04` (memory systems)          | Dr. Inés Roldán         |
| 06  | Building an Agent Evaluation Harness     | `intermediate/08` (evaluating agents)       | Dr. Mireille Dubois     |

Each module states which main-curriculum module it assumes as a prerequisite (per the existing
"must name which module" rule in `curriculum/README.md` §1), then walks the reader through writing
the code themselves — not a solved solution dropped whole, but built up step by step with the
reasoning for each step, consistent with the curriculum's existing "depth is the point, not a
summary" principle.

### 2.2 Post-Training — 2 new modules, appended to `advanced/`

Appended as `advanced/09` and `advanced/10` — the existing 8 advanced modules keep their numbers
unchanged; this is pure addition, not renumbering.

| #   | Module                                                    | Author             |
| --- | --------------------------------------------------------- | ------------------ |
| 09  | Reinforcement Learning from Human Feedback                | Dr. Samuel Okonkwo |
| 10  | Modern Post-Training Methods: DPO, GRPO & Reward Modeling | Dr. Aditi Bhandari |

Module 09 covers the RLHF pipeline (reward model training, PPO fine-tuning) grounded in the
original InstructGPT/RLHF papers — a natural extension of Dr. Okonkwo's existing training-dynamics
modules (`intermediate/01`, `advanced/01`). Module 10 covers the post-2023 methods that moved past
vanilla RLHF (DPO, GRPO, and reward-modeling alternatives), assigned to Dr. Bhandari as
Foundational-AI-Lead-level material connecting foundation-model training practice to the rest of
the corpus. Both follow the exact same worked-example, verified-citation standard as the existing
24 — formulas re-derivable, every claim traced to a real paper, no exceptions for being new.

**8 new modules total.**

---

## 3. Conventions (reused, not reinvented)

- **Audience, bilingual format, citation rule:** exactly as ratified in `curriculum/README.md` §1,
  §4, §5 — no changes. Practicum code blocks follow the existing "code blocks are written once,
  language-neutral" rule; only the surrounding explanatory prose is bilingual.
- **Metadata block, inline-gloss rule:** exactly as amended 2026-08-18 (Amendment 1, README §4.1
  and §4.2) — the new modules are written correctly to this standard from the start, not
  remediated into it after the fact the way the first run's modules had to be.
- **New rule, practicum-specific:** every code block must be independently executed or hand-traced
  by its author before the module is filed — a claim that code "works" is not sufficient; the
  author's method (mental trace, scratch-run, or cited test) must be stated in the module itself,
  the same evidentiary standard the review cycle already holds formula claims to.
- **No application code under `academic-neural-unit-00/`.** Restated from §1 above because it is
  the one genuinely new constraint this plan introduces relative to the first run.

---

## 4. Production Workflow (to run only after CEO approval)

Same `Workflow`-tool pattern as the first run, scaled to 8 new modules instead of 24.

**Phase 1 — Charter (1 agent, Opus/high):** Dr. Mokoena charters the extension, writes
`curriculum/practicum/README.md` conventions section (or a §9 addition to the main
`curriculum/README.md` — her call at charter time) documenting the practicum's purpose, the
no-application-code constraint, and the finalized module→author table above.

**Phase 2 — Author (5 agents, Sonnet/high, parallel):** one agent per crew member (Fujimori: 2
practicum modules; Roldán: 2 practicum modules; Ibarra-Costa: 1 practicum module; Dubois: 1
practicum module; Okonkwo: 1 post-training module — run alongside a 6th agent for Bhandari's 1
post-training module). **6 agents total** for authoring.

**Phase 3 — Internal review (3 agents, Sonnet/high, parallel):** cross-cluster peer review, no
author reviews their own work — Baek reviews the 6 practicum modules plus `advanced/10`, Bhandari
reviews `advanced/09` only (Okonkwo's module — she does not review her own `advanced/10`),
Lindqvist runs the same structural/metadata/bilingual-formatting pass used in the first run,
extended with a fourth check: does every code block show its verification method, per the new
practicum-specific rule in §3.

**Correction (2026-08-27, under CEO ruling):** the original wording here — "Bhandari reviews the
post-training pair she didn't write plus spot-checks Okonkwo's" — was self-contradictory, since §2.2
assigns Bhandari as the author of `advanced/10`, one half of that pair; reviewing it would have
violated the no-self-review rule stated in this same section. The CEO resolved this by reassigning
`advanced/10`'s review to Baek and narrowing Bhandari's Phase 3 scope to `advanced/09` only, as
reflected in the corrected assignment above.

**Phase 4 — External blind review (2 agents, Sonnet/high, parallel):** same two personas as the
first run (technical-accuracy, interview-readiness), plus this run's reviewers must additionally
confirm every practicum code block is actually correct Python that produces the claimed output —
not just that citations exist.

**Phase 5 — Comprehensive review (1 agent, Opus/high):** Dr. Mokoena synthesizes, same
methodology as Pass 3 (independent re-checking, not restating sub-reports), producing a new dated
review round under `curriculum/reviews/` per that folder's own convention.

**Total: 13 agents** (1 + 6 + 3 + 2 + 1) — within this session's 15-agent default guideline, unlike
the first run.

---

## 5. Verification (after the workflow run)

- File count: 8 new modules + charter README update + review round files.
- Every practicum code block re-run or hand-traced independently by at least one reviewer (not
  just the author) before the module can pass — this is the practicum-specific addition to the
  standard citation/claim verification the first run already required.
- Confirm zero files under `academic-neural-unit-00/` are executable application code — markdown
  containing code blocks only.
- Run `prettier --write` over every created/modified file.
- Report back: what passed, what needs revision, using the same per-document verdict table format
  Pass 3 established.

---

## 6. Approval Gate

**Next step:** CEO reviews this plan (the 8-module scope, author assignments, the
no-application-code handling, and the 13-agent workflow). Implementation begins only after explicit
CEO sign-off here — the same gate `curriculum-development-plan.md` used before any of the first 24
modules were written.
