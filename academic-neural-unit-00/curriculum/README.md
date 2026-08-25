# academic-neural-unit-00/curriculum/ — ANU-00 Agent Development Curriculum

Standing bilingual (EN/ZH) training textbook series on agent development, produced by ANU-00 crew.
Chartered 2026-08-17 by Dr. Naledi Mokoena, ANU-00 Lead, under CEO approval of
`academic-neural-unit-00/plans/2026-08-17-curriculum-first-production-run/curriculum-development-plan.md`.

Read this file before authoring, reviewing, or filing anything under `curriculum/`. It is the
canonical statement of the audience, the bilingual convention, the citation convention, the review
process, and the ratified module→author assignment. Where an authoring or review prompt disagrees
with this file, this file governs.

---

## 1. Purpose and Audience

The curriculum exists to take one specific reader from zero to hire-ready: **a new ANU-00 or CC-00
joiner with no prior background in machine learning, artificial intelligence, or agent
development.** Not a refresher for someone who already knows the material, and not a survey for a
manager who needs vocabulary — a genuine from-nothing course of study.

The bar is external, not internal. A reader who works through all 24 modules in order should be
able to hold their own in a real technical interview at a serious AI lab, and to start
contributing to ANU-00 research or CC-00 engineering without a second onboarding. That bar is what
makes the citation rule in §5 non-negotiable: a curriculum benchmarked only against this
workspace's own conventions would teach a reader to pass here and nowhere else.

Three consequences follow, and every author is bound by them:

- **Introductory modules define every term before using it.** No assumed coursework, no assumed
  mathematics beyond secondary-school algebra, no undefined jargon. If a term is used, it was
  defined earlier in the same document or in an earlier module.
- **Intermediate and advanced modules may assume only what earlier curriculum modules taught, and
  must name which module.** "As covered in `introductory/02`" is the required form. "As is well
  known" and "recall from your linear algebra course" are not — the reader has no outside
  coursework to recall.
- **Depth is the point.** Each module is a textbook chapter, not a summary: worked examples
  throughout, and for intermediate and advanced modules, real named algorithms and formulas
  grounded in verified citations. A module that could be replaced by a well-written blog post has
  missed its brief.

---

## 2. Why This Is a Category of Its Own, Not a `knowledge-base/` Entry

`academic-neural-unit-00/knowledge-base/` holds **point-in-time findings from chartered research
programmes** — `YYYY-MM-DD-<slug>/research-report.md`, each one the output of a specific research
question that passed the falsifiability check and the stage-of-inquiry test in
`crew/lead/naledi-mokoena/skills/research-programme-chartering.md`. A knowledge-base entry answers
a question asked on a particular date and is superseded by a later dated entry, never edited into
agreement with it.

Curriculum documents are a different object in four ways, and forcing them into the knowledge-base
convention would misrepresent all four:

| Property        | `knowledge-base/`                        | `curriculum/`                                          |
| --------------- | ---------------------------------------- | ------------------------------------------------------ |
| What it records | A finding — what we learned on a date    | Settled teaching material — what a newcomer must learn |
| Lifecycle       | Point-in-time; superseded, never revised | Standing; revised in place as the field moves          |
| Organized by    | Date and programme slug                  | Level and topic cluster                                |
| Originated by   | A chartered research question            | A training need                                        |

The knowledge base is dated because a finding belongs to its moment. The curriculum is levelled
because a reader belongs to a stage. Filing an evergreen chapter on the transformer architecture
under `2026-08-17-transformers/` would date material that is not dated, and hide it from the
reader who needs it most.

This is also **not** a violation of the no-tasking boundary (`formation-report.md` §2). The
curriculum is a training deliverable ANU-00 produces for its own and CC-00's incoming people — it
is not ANU-00 being tasked to de-risk an item on CC-00's roadmap, and no module carries an
external request surface. Curriculum modules make no research claims of their own; where a module
touches an open research question, it says so and points at the literature rather than asserting
an ANU-00 finding.

---

## 3. Directory Structure

```
curriculum/
├── README.md                           ← this file — canonical conventions and module index
├── introductory/                       ← 8 modules — zero prior background assumed
├── intermediate/                       ← 8 modules — builds strictly on introductory/
├── advanced/                           ← 8 modules — builds strictly on intermediate/
└── reviews/
    ├── README.md                       ← the dated-round filing convention (read before adding a new round)
    ├── 2026-08-18-first-review-cycle/  ← Pass 1 (internal/), Pass 2 (external/), Pass 3 (comprehensive-review.md)
    │   ├── internal/                   ← 5 ANU-00 cluster review reports
    │   ├── external/                   ← 2 blind external review reports
    │   └── comprehensive-review.md     ← Lead's synthesis review (root final-review.md shape)
    └── 2026-08-19-remediation-review/  ← Pass 4: 4 independent re-reviews + the Lead's closing synthesis
```

Filenames are level-prefixed, two-digit ordered, kebab-case. The `#` column of the module index in
§7 is the filename prefix.

The CEO-approved plan that authorized this production run lives at
`academic-neural-unit-00/plans/2026-08-17-curriculum-first-production-run/curriculum-development-plan.md`
— not inside this folder. Plans and the deliverables they authorize are filed separately; see
`academic-neural-unit-00/plans/README.md` for the convention and why.

Review reports are **point-in-time records**, following the same rule as
`knowledge-base/research-report.md`: a re-review after a revision pass is a new file with a
cross-reference, never an edit to the report it supersedes. The two review templates live at
`academic-neural-unit-00/templates/curriculum/`.

**Every review round files into its own dated subfolder** of `reviews/` —
`YYYY-MM-DD-<round-slug>/`, the same dated-entry pattern `knowledge-base/` uses — so that multiple
future rounds of internal and external review never collide or land ambiguously in a flat folder.
Full convention: `reviews/README.md`.

---

## 4. Bilingual Format

Reproduced verbatim below as the single canonical copy. Authors write to it; internal reviewers
check against it; no authoring or review prompt may paraphrase or relax it.

BILINGUAL FORMAT (mandatory, applies to every heading and every paragraph in the document body):

- Write one English paragraph, then immediately write its Chinese translation as the very next
  paragraph (blank line between), before moving to the next English paragraph. Never batch all
  English first and all Chinese after.
- Section headings: English heading on its own markdown heading line, e.g. "## 2. The Attention
  Mechanism", followed immediately on the next line by the Chinese translation of that heading
  only, formatted as a bold line, e.g. “**注意力机制**”, then a blank line, then the English body
  paragraph, then its Chinese translation paragraph, and so on through the section.
- Chinese translation must be natural, idiomatic technical Chinese — faithful to meaning (信),
  fluent and clear (达), and well-crafted (雅). Never transliterate or produce stilted
  "machine-like" phrasing. Do not just gloss English terms with pinyin.
- Code blocks, math/formulas, and tables are written once (language-neutral, not duplicated), but
  any prose sentence introducing or explaining them still follows the EN-paragraph-then-ZH-paragraph
  pattern. Formulas are written in LaTeX — see §4.3.
- Keep technical terms consistent: settle on one Chinese rendering of a term and use that rendering
  for that term everywhere in the document — and across the whole curriculum wherever §4.2 has
  ratified one.
- **Inline parenthetical glossing — the form “English term（中文）” — is reserved for proper nouns
  and named entities, on first use only.** A proper noun here means a named model, framework,
  benchmark, paper, or method that carries an established name: “ReAct（推理与行动协同）”,
  “Chinchilla（龙猫模型）”, “Transformer（变换器）”. Gloss such a name once, at its first
  appearance in the document, then use the name alone thereafter.
- **Ordinary technical concepts must NOT receive an inline gloss.** Terms such as loss function,
  embedding vector, token, or context window are translated by the paired
  English-paragraph-then-Chinese-paragraph structure and by nothing else — the English paragraph
  names them in English, its Chinese translation names them in Chinese, and that pairing _is_ the
  translation. Writing “loss function（损失函数）” duplicates work the structure already does and
  clutters the line. If a concept genuinely needs more than a one-word rendering to land, define it
  in a sentence in both paragraphs; do not smuggle the definition into a parenthesis.

This is a **correction to the rule as it previously stood.** The earlier wording told authors to
gloss "technical terms" generally, with no proper-noun restriction. All eight authors followed it
faithfully, which produced 310 inline glosses across the 24 modules — a convention defect, not an
authoring one (`reviews/2026-08-18-first-review-cycle/comprehensive-review.md`, item C-3). The narrower rule above replaces that
wording outright; where an existing module glosses an ordinary term, it is the module that is now
out of conformance, not this rule.

One file per module holds both languages. There is no `*-zh.md` twin, and there never will be —
split-language files drift, and a reader comparing a paragraph against its translation is the
cheapest error check this curriculum has.

### 4.1 Module Metadata Block — One Canonical Format

Every module opens with a metadata block, and there is exactly **one permitted format**: a
three-row Markdown table carrying Level, Cluster, and Author, with English and Chinese as two
columns of the same table rather than two separate lines. This is mandatory for every module going
forward.

The block sits directly beneath the English H1 title and its bold Chinese title line, and is
followed by a `---` rule before the first section heading. Example:

```markdown
# What Is an AI Agent? Concepts & the Agent Loop

**什么是 AI 智能体？概念与智能体循环**

| Field   | English                                                                 | 中文                                        |
| ------- | ----------------------------------------------------------------------- | ------------------------------------------- |
| Level   | Introductory                                                            | 入门                                        |
| Cluster | Agent Architecture & Design Patterns                                    | 智能体架构与设计模式                        |
| Author  | Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00 | ANU-00 智能体系统研究员 Kaito Fujimori 博士 |

---
```

Binding details:

- **All three rows are required.** A block missing the Author row (or any other row) is
  non-conformant, not merely terse.
- **Both columns are required on every row.** The block is bilingual for the same reason every
  heading is — a table row with only the English or only the Chinese cell filled in does not
  conform.
- **Author is the full roster identity** — name, roster role, and `ANU-00` — matching
  `academic-neural-unit-00/crew/README.md`, not a bare surname.
- **No other format is permitted.** This supersedes the bold key-value-line format (Amendment 1's
  "Format B"), which is itself now deprecated — see Amendment 2 below for why. Pipe-tables,
  italicized or plain narrative paragraphs, partial two-field lines, the bold key-value line, and
  omitting the block entirely have all been in use at one point across this curriculum's history;
  all are now deprecated in favor of this one table format.

### 4.2 Ratified Terminology

Where a term has more than one defensible Chinese rendering, the choice is ratified once here and
binds every module — consistency across the corpus is a reader-facing property, and an author's
local preference does not outrank it.

| English term                        | Canonical Chinese | Deprecated            |
| ----------------------------------- | ----------------- | --------------------- |
| harness (agent / execution harness) | 运行框架          | 执行框架 — do not use |

**harness → 运行框架** (resolving C-1). Eight modules across three clusters had split between
`执行框架` and `运行框架`. `运行框架` is canonical: it was the majority usage, and it was the choice
of both modules that make harnesses their actual subject. `执行框架` was a competing translation
used in some earlier drafts and is **deprecated** — it must not appear in new modules, and the
existing occurrences (`introductory/03`, `introductory/04`, `intermediate/07`, `advanced/08`) are
corrected under the C-1 harmonization scope, not left standing as an author's preference.

### 4.3 Math/Formula Notation

Every formula is written in **LaTeX**, delimited inline as `$...$` within the surrounding sentence.
A formula is not re-typeset differently for its English occurrence versus its Chinese occurrence —
per the "written once, language-neutral" rule in §4 above, the same LaTeX span sits inside both the
English paragraph and its Chinese translation. Display equations set off on their own line use
`$$...$$`, reserved for equations complex enough (multi-line derivations, an equation the text
calls out by name) that inlining would break the sentence — the corpus default is inline.

This replaces the plain-Unicode math notation (`θ`, `√`, `≈`, `Σ`, subscript/superscript
characters) used in the curriculum's first production run — see Amendment 3 below for why, and the
corpus-wide conversion it authorized.

Binding details:

- **Standard LaTeX commands only** (`\frac`, `\sqrt`, `\sum`, `\alpha`…`\omega`, `\leftarrow`,
  `\approx`, subscripts via `_`, superscripts via `^`) — no custom macros, and no Unicode math
  characters mixed into a LaTeX span.
- **Meaning-preserving is the only requirement that matters.** Converting notation must never
  change what a formula says. A converted formula is checked against the citation it traces to
  (§5), not against the pre-conversion Unicode text — the old notation is not kept as a shadow copy
  anywhere once a module is converted.
- **Three structural patterns silently break rendering — checked mechanically on every module, not
  by eye (Amendment 4).** All three were found live in the corpus after the Amendment 3 conversion
  and are now binding review checks (`templates/curriculum/internal-review-report.md` Check 5):
  1. **Never wrap a `$$...$$` display block inside a triple-backtick code fence.** A fenced block
     renders as literal preformatted text — no renderer looks inside one for `$`. If a formula was
     inherited from a pre-LaTeX worked example that used a fence to align plain-text output, remove
     the fence; `\begin{bmatrix}`/`\begin{cases}` do their own alignment.
  2. **A `$$...$$` line must contain nothing else** — no leading or trailing prose on the same line,
     not even a short parenthetical. Give the explanation its own lead-in sentence, bilingual-paired
     like any other sentence, immediately before the equation.
  3. **Never let a `$...$` span fall inside a single backtick code span** (`` `$x$` ``) — a backtick
     code span suppresses math rendering for exactly the same reason a fence does.

### 4.4 Section Citation & Academic Range Notation (§ vs §§)

In accordance with international academic publishing standards (Chicago Manual of Style §10.42, Bluebook Rule 3.3) and CEO ratification (2026-08-24, Entry 14):

- **Singular Section Citations:** Reference a single section using the singular section sign `§X` in English (e.g., `[§4](#...)` or `Section 4`) and `[第 X 节](#...)` in Chinese.
- **Plural Section & Range Citations:** Reference a range or multiple sections using the academic plural double section sign `§§X–Y` in English (e.g., `[§§2–5](#...)` representing _"Sections 2 through 5"_) and `[第 X–Y 节](#...)` in Chinese.
- **Interactive Hyperlinks:** All intra-document section citations are rendered as clickable markdown anchor links (`[§X](#...)`, `[§§X–Y](#...)`) targeting the corresponding section heading ID.

---

## 5. Citations

Reproduced verbatim below as the single canonical copy. This section carries the CEO's accuracy
requirement; a fabricated or misrepresented citation is the most serious defect a module can have,
and internal reviewers are instructed to treat it as blocking.

CITATIONS (mandatory):

- End every document with a heading "## References" immediately followed by its Chinese translation
  “**参考文献**”, split into two subsections: "### External Sources" and "### Internal
  Cross-References".
- Every formula, named result, or paper claim you state must trace to a real, verifiable external
  source (a real paper, textbook, or course) cited in External Sources as a markdown link:
  "- [Title](URL)". Use WebSearch/WebFetch to confirm the source actually exists and that you are
  representing it correctly (correct authors, correct claim, correct formula) BEFORE citing it —
  never invent a citation or cite from memory without verification.
- If you cannot verify a claim you were about to make, do not state it as fact — soften it, remove
  it, or find a verifiable source instead.
- Internal Cross-References lists other curriculum modules this document builds on or connects to,
  as relative markdown links.
- Audience: the reader has NO prior background in ML, AI, or agent development. Introductory-level
  docs must define every term before using it. Intermediate/advanced docs may assume only what
  earlier curriculum modules already taught — name which module, don't assume outside coursework.
- Write with genuine textbook depth per module (not a skim) — worked examples, and for
  intermediate/advanced modules, real named algorithms/formulas grounded in your verified citations.

**Not knowing is a permitted answer.** Where the literature is genuinely unsettled — a contested
scaling result, a benchmark whose validity is disputed — say so and cite both sides. Presenting a
contested position as settled fact to keep a chapter tidy is a worse defect than admitting the
uncertainty, and reviewers will flag it as one.

---

## 6. Review Process

Three passes, in order. Authors do not review their own work at any stage, and no reviewer reviews
a cluster they authored into.

**Pass 1 — Internal cluster review (5 reviewers, ANU-00 crew).** Four reviewers each take one
topic cluster (6 documents spanning all three levels), plus one structural reviewer across all 24.
Filed to `reviews/2026-08-18-first-review-cycle/internal/` on the
`academic-neural-unit-00/templates/curriculum/internal-review-report.md` template.

| Reviewer                | Reviews                                                                 | Output file                                |
| ----------------------- | ----------------------------------------------------------------------- | ------------------------------------------ |
| Dr. Mireille Dubois     | Foundations cluster (6 docs)                                            | `foundations-cluster-review.md`            |
| Dr. Aditi Bhandari      | Agent Architecture & Design Patterns cluster (6 docs)                   | `agent-architecture-cluster-review.md`     |
| Dr. Yuna Baek           | Prompt & Context Engineering cluster (6 docs)                           | `prompt-context-cluster-review.md`         |
| Dr. Rafael Ibarra-Costa | Multi-Agent Systems & Evaluation cluster (6 docs)                       | `multi-agent-evaluation-cluster-review.md` |
| Tobias Lindqvist        | All 24 docs — structural/taxonomy/bilingual-formatting consistency only | `structural-bilingual-taxonomy-review.md`  |

Internal reviewers **independently spot-check facts** — they do not simply confirm that the
author's own citations support the author's own text. Checking that a cited paper exists is the
floor; checking that the module's claim is what that paper actually says is the requirement.

**Pass 2 — Blind external review (2 reviewers).** Fresh reviewers with no ANU-00 or CC-00 context,
given only the finished module files, role-playing genuine outside experts. This pass exists
precisely to catch what internal review cannot: material that reads as correct to people who share
the same assumptions. Filed to `reviews/2026-08-18-first-review-cycle/external/` on the
`academic-neural-unit-00/templates/curriculum/external-review-report.md` template.

| Reviewer | Persona and lens                                                             | Output file                              |
| -------- | ---------------------------------------------------------------------------- | ---------------------------------------- |
| A        | Outside PhD-level AI researcher — technical accuracy and citation audit      | `external-technical-accuracy-review.md`  |
| B        | Hiring manager / technical interviewer at a top AI lab — interview readiness | `external-interview-readiness-review.md` |

**Pass 3 — Comprehensive synthesis review (ANU-00 Lead).** Dr. Mokoena reads all 5 internal and
2 external reports and produces `reviews/2026-08-18-first-review-cycle/comprehensive-review.md` using the root
`templates/review-records/final-review.md` template unchanged — per ANU-00's standing convention
that multi-party sign-off on completed work reuses the root shape rather than growing a twin. Its
"Method" table cites the 7 sub-reports as the records checked; it reaches a **per-document
pass / needs-revision verdict** and a Joint Recommendation for the CEO. Synthesis means reaching a
verdict the sub-reports did not, not restating them.

**Scope boundary for this run:** the process stops at the comprehensive review. Authors fixing
flagged issues, and any re-review, is a separately scoped follow-up run — a "needs revision"
verdict in this cycle is a complete result of this cycle, not an unfinished one.

---

## 7. Module Index

24 modules, 8 per level, covering all four topic clusters at every level. Author assignment is
ratified — it is the sign-off required by
`crew/lead/naledi-mokoena/skills/research-programme-chartering.md` §5, applied here to a training
deliverable rather than a research programme, and it is not delegable.

| Level        | #   | Title                                                                     | Author                  | Cluster                              |
| ------------ | --- | ------------------------------------------------------------------------- | ----------------------- | ------------------------------------ |
| introductory | 01  | Neural Networks & Deep Learning Foundations                               | Dr. Yuna Baek           | Foundations                          |
| introductory | 02  | The Transformer Architecture & Attention                                  | Dr. Yuna Baek           | Foundations                          |
| introductory | 03  | What Is an AI Agent? Concepts & the Agent Loop                            | Dr. Kaito Fujimori      | Agent Architecture & Design Patterns |
| introductory | 04  | Tool Use & Function Calling Basics                                        | Dr. Kaito Fujimori      | Agent Architecture & Design Patterns |
| introductory | 05  | Prompt Engineering Fundamentals                                           | Dr. Wei-Ling Tan        | Prompt & Context Engineering         |
| introductory | 06  | Context Windows, Tokens & Memory Basics                                   | Dr. Rafael Ibarra-Costa | Prompt & Context Engineering         |
| introductory | 07  | Introduction to Multi-Agent Systems                                       | Dr. Kaito Fujimori      | Multi-Agent Systems & Evaluation     |
| introductory | 08  | Why & How We Evaluate Agents                                              | Dr. Mireille Dubois     | Multi-Agent Systems & Evaluation     |
| intermediate | 01  | Training Dynamics: Optimization & Generalization                          | Dr. Samuel Okonkwo      | Foundations                          |
| intermediate | 02  | Attention Deep Dive: Multi-Head Attention, KV-Cache & Positional Encoding | Dr. Yuna Baek           | Foundations                          |
| intermediate | 03  | Agent Design Patterns: ReAct, Plan-and-Execute & Reflexion                | Dr. Kaito Fujimori      | Agent Architecture & Design Patterns |
| intermediate | 04  | Agent Memory Systems: Short-Term, Long-Term & Episodic Memory             | Dr. Inés Roldán         | Agent Architecture & Design Patterns |
| intermediate | 05  | Advanced Prompting: Chain-of-Thought, Few-Shot & Structured Output        | Dr. Wei-Ling Tan        | Prompt & Context Engineering         |
| intermediate | 06  | RAG Fundamentals: Retrieval, Embeddings & Grounding                       | Dr. Rafael Ibarra-Costa | Prompt & Context Engineering         |
| intermediate | 07  | Multi-Agent Communication & Coordination Protocols                        | Dr. Kaito Fujimori      | Multi-Agent Systems & Evaluation     |
| intermediate | 08  | Evaluating Agent Systems: Benchmarks & Methodology                        | Dr. Mireille Dubois     | Multi-Agent Systems & Evaluation     |
| advanced     | 01  | Scaling Laws & Emergent Capabilities                                      | Dr. Samuel Okonkwo      | Foundations                          |
| advanced     | 02  | Mixture-of-Experts & Modern Architecture Variants                         | Dr. Yuna Baek           | Foundations                          |
| advanced     | 03  | Agent Harness Engineering: Building Production-Grade Agent Loops          | Dr. Inés Roldán         | Agent Architecture & Design Patterns |
| advanced     | 04  | Agentic Safety, Guardrails & Governance Patterns                          | Dr. Kaito Fujimori      | Agent Architecture & Design Patterns |
| advanced     | 05  | Advanced Context Engineering: Long-Context & Context Budgeting            | Dr. Wei-Ling Tan        | Prompt & Context Engineering         |
| advanced     | 06  | RAG at Scale: Hybrid Search, Reranking & Evaluation                       | Dr. Wei-Ling Tan        | Prompt & Context Engineering         |
| advanced     | 07  | Multi-Agent Orchestration: Worktree Isolation & Consensus                 | Dr. Aditi Bhandari      | Multi-Agent Systems & Evaluation     |
| advanced     | 08  | Rigorous Agent Evaluation: Statistical Methodology                        | Dr. Mireille Dubois     | Multi-Agent Systems & Evaluation     |

### 7.1 Filenames

| Level          | Files                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `introductory` | `01-neural-networks-and-deep-learning-foundations.md`, `02-the-transformer-architecture-and-attention.md`, `03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`, `04-tool-use-and-function-calling-basics.md`, `05-prompt-engineering-fundamentals.md`, `06-context-windows-tokens-and-memory-basics.md`, `07-introduction-to-multi-agent-systems.md`, `08-why-and-how-we-evaluate-agents.md`                                                                                                          |
| `intermediate` | `01-training-dynamics-optimization-and-generalization.md`, `02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`, `03-agent-design-patterns-react-plan-execute-reflexion.md`, `04-agent-memory-systems-short-term-long-term-episodic.md`, `05-advanced-prompting-cot-few-shot-structured-output.md`, `06-rag-fundamentals-retrieval-embeddings-and-grounding.md`, `07-multi-agent-communication-and-coordination-protocols.md`, `08-evaluating-agent-systems-benchmarks-and-methodology.md` |
| `advanced`     | `01-scaling-laws-and-emergent-capabilities.md`, `02-mixture-of-experts-and-modern-architecture-variants.md`, `03-agent-harness-engineering-production-grade-agent-loops.md`, `04-agentic-safety-guardrails-and-governance-patterns.md`, `05-advanced-context-engineering-long-context-and-budgeting.md`, `06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`, `07-multi-agent-orchestration-worktree-isolation-and-consensus.md`, `08-rigorous-agent-evaluation-statistical-methodology.md`       |

### 7.2 Assignment Rationale and Roster Confirmation

Every author above is a current ANU-00 crew member, and every assignment matches that member's
documented specialty on the roster (`academic-neural-unit-00/crew/README.md`). Confirmed at ratification:

| Author                  | Roster role (`crew/README.md`)                  | Modules | Why this author                               |
| ----------------------- | ----------------------------------------------- | ------- | --------------------------------------------- |
| Dr. Yuna Baek           | Research Scientist — AI / Neural Networks       | 4       | Architecture and neural-network internals     |
| Dr. Samuel Okonkwo      | Research Scientist — Machine Learning Theory    | 2       | Optimization, generalization, scaling laws    |
| Dr. Kaito Fujimori      | Research Scientist — Agent Systems Research     | 6       | Agent loop, patterns, coordination, safety    |
| Dr. Inés Roldán         | Research Scientist — Software Engineering / CS  | 2       | Systems-engineering modules (memory, harness) |
| Dr. Wei-Ling Tan        | Research Scientist — Applied AI Systems         | 4       | Applied prompting, context, retrieval         |
| Dr. Rafael Ibarra-Costa | Research Scientist — Generalist                 | 2       | Cross-cutting entry-level bridging modules    |
| Dr. Mireille Dubois     | Research Scientist — LLM Systems                | 3       | Evaluation across all three levels            |
| Dr. Aditi Bhandari      | Staff Research Scientist — Foundational AI Lead | 1       | Advanced orchestration; L4 depth              |

Two crew members are deliberately **not** authors. Tobias Lindqvist (Knowledge Systems Engineer)
takes the structural/taxonomy/bilingual-consistency review across all 24 documents — his mandate
is indexing and consistency, not subject-matter authorship. Dr. Mokoena authors nothing so that
the comprehensive synthesis review in Pass 3 is not a review of her own work.

Cluster review assignments in §6 were checked against this table: no reviewer reviews a cluster
they authored into. Dubois reviews Foundations (authored by Baek and Okonkwo); Bhandari reviews
Agent Architecture (Fujimori, Roldán); Baek reviews Prompt & Context (Tan, Ibarra-Costa);
Ibarra-Costa reviews Multi-Agent & Evaluation (Fujimori, Dubois, Bhandari).

---

## 8. Rules for Authors and Reviewers

1. **This README governs.** Where an authoring prompt, a review prompt, or a habit conflicts with
   §4, §5, or §6, this file wins. Raise the conflict with Dr. Mokoena rather than resolving it
   silently in the document.
2. **Verify before citing, every time.** §5 is a procedure, not an aspiration. A citation you did
   not open is a citation you did not verify.
3. **A clean result must be stated plainly.** A reviewer who found nothing wrong with a document
   says so explicitly — silence reads as an unfinished review, and ANU-00 templates are built so a
   null result never looks like an incomplete one (`academic-neural-unit-00/templates/README.md` § Design Rules, rule 3).
4. **Point-in-time discipline for reviews.** A re-review is a new file with a cross-reference to
   the report it supersedes, never an edit to it.
5. **Run Prettier before finalizing** any file created or modified here, per root `CLAUDE.md` §1:
   `prettier --write "<file-path>"`.

---

**Ratified by:** Dr. Naledi Mokoena, ANU-00 Lead — 2026-08-17
**Under:** CEO approval of `academic-neural-unit-00/plans/2026-08-17-curriculum-first-production-run/curriculum-development-plan.md`
**Roster cross-check:** `academic-neural-unit-00/crew/README.md`, confirmed consistent 2026-08-17 (§7.2)

**Amendment 1 — 2026-08-18, Dr. Naledi Mokoena, ANU-00 Lead.** Resolves the three corpus-wide
convention items raised by `reviews/2026-08-18-first-review-cycle/comprehensive-review.md`: C-2 (§4.1 — one canonical metadata
block format, Format B, mandatory), C-3 (§4 — inline glossing narrowed to proper nouns and named
entities on first use, replacing the earlier "technical terms" wording that caused the over-use),
and C-1 (§4.2 — `harness` = 运行框架 canonical, `执行框架` deprecated). This amendment changes the
convention only. Bringing the 24 existing modules into conformance is the separately scoped
remediation run, not part of this amendment.

**Amendment 2 — 2026-08-19, Dr. Naledi Mokoena, ANU-00 Lead, under CEO direction.** Replaces
Amendment 1's metadata-block format (§4.1 "Format B" — a bold key-value line + separate Chinese
mirror line) with a three-row bilingual Markdown table (Level / Cluster / Author, English and
Chinese as two columns of one table). Same three required fields, same placement beneath the title
lines, same full-roster-identity rule for Author — only the presentation changes, for readability:
a rendered table is more scannable than two parallel styled-text lines. All 24 existing modules'
metadata blocks were reformatted to this table in the same pass that ratified it, so this amendment
and its corpus-wide application landed together rather than in two separately scoped steps.

**Amendment 3 — 2026-08-19, Dr. Naledi Mokoena, ANU-00 Lead, under CEO direction.** Replaces the
plain-Unicode math notation used throughout the first production run (§4.3) with LaTeX, delimited
`$...$` inline / `$$...$$` for display equations — a cleaner, publication-grade presentation than
Unicode symbols, and one that renders correctly wherever the corpus is read on GitHub's web UI. All
13 formula-bearing modules were converted to LaTeX in the same pass that ratified this amendment,
each formula checked against its original for meaning-preservation, not left as a follow-up
remediation item.

**Amendment 4 — 2026-08-20, Dr. Naledi Mokoena, ANU-00 Lead.** Two readers hit live KaTeX render
failures the Amendment 3 conversion pass did not catch: a `$$...$$` block in
`introductory/01-neural-networks-and-deep-learning-foundations.md` with a nested `$...$` span
trailing on the same line (parser error), and three `$$...$$` blocks in
`introductory/02-the-transformer-architecture-and-attention.md` left inside a triple-backtick code
fence inherited from the pre-conversion worked example (rendered as literal text, not math). Both
are now §4.3 binding rules, and a corpus-wide sweep across all 24 modules — code-fence-trapped math,
trailing-content-after-`$$`, `$` inside a single backtick span, and paragraph-level delimiter
balance — found no further instances after the two fixes. `templates/curriculum/internal-review-report.md`
Check 5 (Structural completeness) now names all three patterns explicitly, so every future cluster
reviewer checks for them on every formula-bearing document, not only the structural specialist.
