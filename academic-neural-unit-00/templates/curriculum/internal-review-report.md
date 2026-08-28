# Internal Curriculum Review — [Cluster Name] Cluster

<!-- Copy this file to academic-neural-unit-00/curriculum/reviews/YYYY-MM-DD-<round-slug>/internal/<cluster>-review.md
     — one dated round folder per review cycle, per curriculum/reviews/README.md. Never fill one
     in inside templates/ itself.

     Point-in-time record (academic-neural-unit-00/templates/README.md § Available Templates).
     A re-review after a revision pass is a NEW file with a cross-reference back to this one —
     never an edit to it. Editing a filed review destroys the record of what the curriculum
     looked like when it was reviewed, which is the only thing a review report is for.

     Scope note: this template is for ANU-00 crew peer review of curriculum modules. It is not a
     research finding — no claim register, no falsifiability condition. Those belong to
     knowledge-base/research-report.md and do not apply to teaching material. -->

**Reviewer:** [Name, ANU-00 role per `crew/README.md`]
**Cluster reviewed:** [Foundations / Agent Architecture & Design Patterns / Prompt & Context
Engineering / Multi-Agent Systems & Evaluation / Structural–bilingual–taxonomy, all 24 docs]
**Documents covered:** [Relative paths, one per line — every document in scope, listed
individually. A count without paths is not a scope statement.]
**Review date:** [YYYY-MM-DD]
**Review pass:** [Pass 1 — internal cluster review (first cycle) / Re-review of `<prior file>`]

<!-- Reviewer identity is required, not courtesy attribution. curriculum/README.md §6 forbids
     anyone reviewing a cluster they authored into; that constraint cannot be checked after the
     fact unless the reviewer and the documents are both named here. -->

---

## 0. Independence Declaration

<!-- Required. curriculum/README.md §6: "Authors do not review their own work at any stage, and no
     reviewer reviews a cluster they authored into." State it explicitly rather than leaving it to
     be inferred from the roster — a conflict that is never written down is a conflict nobody
     catches. -->

**Did I author any document in this cluster?** [No / Yes — which, and stop: reassign the review]

**Anything else that would compromise independence:** [Named plainly, or "None"]

---

## 1. Method

<!-- This section exists to prevent the single most common failure mode of a review: restating the
     document's own claims instead of checking them. It is the same discipline root
     templates/review-records/final-review.md § Method imposes, applied per-document.

     Binding, and the reason this section is first: FACTUAL ACCURACY IS SPOT-CHECKED
     INDEPENDENTLY. Confirming that a cited source exists and that the author's sentence matches
     the author's own citation is the floor, not the check. The check is whether the claim is
     true — verified against a source you went and found, not only the one the author handed you.
     curriculum-development-plan.md §1 makes truthful, error-free content the CEO's first stated
     requirement; a review that only audits internal consistency cannot deliver it. -->

I am not restating the documents' own claims. For each document below I checked the material
directly before signing this.

| What I did                                | Detail                                                                                             |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Independent sources consulted             | [Papers/textbooks/courses I opened MYSELF, not ones the doc cited — or "None", which is a finding] |
| Author-supplied citations opened          | [How many of the cited links I actually resolved, out of how many total]                           |
| Claims spot-checked against those sources | [How many, and how selected — worst-case first, or sampled, or exhaustive]                         |
| Chinese-language read                     | [Read in full / sampled — say which, and how much]                                                 |

---

## 2. Per-Document Checklist

<!-- One block per document in scope. Copy the block as many times as needed; do not collapse
     several documents into one shared verdict — a cluster-level pass hides a single broken
     chapter, which is exactly the outcome a per-document checklist exists to prevent.

     The five checks below are not interchangeable and none may be skipped. Each maps to a stated
     requirement: (1) and (2) to curriculum-development-plan.md §1.1 and curriculum/README.md §5
     (truthful content, verifiable sources); (3) to §1.3 and README §1 (zero-background reader);
     (4) to §1.2 and README §4 (信达雅, never machine-like); (5) to README §4–§5 (bilingual pairing
     and the References section are structural, so their absence is checkable, not a matter of
     taste). -->

### 2.[N] `[relative/path/to/document.md]`

**Author:** [Name]

| #   | Check                                         | Verdict       | Notes                                                                                                                                                                                                                                                                                                                                                                                        |
| --- | --------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Factual accuracy — independently spot-checked | [Pass / Fail] | [Which claims I checked, against WHICH source I found myself. "The author's citations support the text" is not an answer to this row.]                                                                                                                                                                                                                                                       |
| 2   | Citation validity                             | [Pass / Fail] | [Links resolve; authors/year/claim correctly represented; no citation of a paper that does not say what the doc says it says]                                                                                                                                                                                                                                                                |
| 3   | Pedagogical fit for a zero-background reader  | [Pass / Fail] | [Every term defined before use (introductory), or the specific earlier module named (intermediate/advanced); worked examples present; genuine textbook depth, not a skim]                                                                                                                                                                                                                    |
| 4   | Bilingual quality (信达雅)                    | [Pass / Fail] | [See the mandatory instruction below this table]                                                                                                                                                                                                                                                                                                                                             |
| 5   | Structural completeness                       | [Pass / Fail] | [EN¶→ZH¶ pairing throughout; bold ZH line under every heading; `## References` + `**参考文献**` present with both subsections; terminology introduced once as `term（术语）` and used consistently; for any formula-bearing document — no `$$...$$` block inside a code fence, no leading/trailing content on a `$$...$$` line, no `$...$` span inside a single backtick span (README §4.3)] |

<!-- CHECK 4 — MANDATORY INSTRUCTION, not a suggestion.
     You must actively flag anything "machine-like": word-order calques from English, a technical
     term rendered by pinyin or left in English where a standard Chinese term exists, translated
     idioms that no Chinese technical writer would produce, sentences that parse but that a native
     reader would not write. Quote the offending Chinese sentence in the problems table and give
     the wording you would use instead. curriculum-development-plan.md §1.2 requires translation
     that is faithful, expressive and elegant (信达雅) and "never machine-like" — a check that only
     confirms the Chinese exists and means roughly the right thing does not satisfy it.
     "Translation reads fine" with nothing quoted is not a completed check 4. -->

**Problems found in this document:** [Count, or the explicit sentence required by §4 below]

**Verdict:** [Pass / Needs revision — and if needs revision, the single blocking reason in one line]

<!-- Verdict rule: a document with any Fail row above is "Needs revision". A document may also be
     "Needs revision" with all rows Pass if the problems table carries a P1 — say so and why.
     Never record a verdict that the rows above do not support. -->

---

## 3. Problems Found

<!-- One table for the whole cluster, so the author of any single document can find their items and
     the Lead can see the cluster's shape at a glance. Every row must be actionable: a location
     precise enough to navigate to, and an issue statement precise enough to act on without
     asking the reviewer what they meant. -->

| #   | Document                | Location                          | Issue                                                       | Severity |
| --- | ----------------------- | --------------------------------- | ----------------------------------------------------------- | -------- |
| 1   | [`path/to/document.md`] | [§ number / heading / line range] | [What is wrong, specifically — and what correct looks like] | [P0–P3]  |

**Severity scale:**

| Severity | Meaning                                                                                                                                                                                                    |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P0**   | Fabricated, non-existent, or materially misrepresented citation; a stated formula or named result that is wrong. Blocking without exception.                                                               |
| **P1**   | A factual claim that is wrong or unsupportable; a term used before it is defined in an introductory module; a section that assumes outside coursework. Blocking.                                           |
| **P2**   | Machine-like or inconsistent Chinese; broken EN¶→ZH¶ pairing; missing worked example where the material needs one; thin treatment of a topic the module is named after. Non-blocking but must be recorded. |
| **P3**   | Wording, formatting, or terminology polish.                                                                                                                                                                |

<!-- P0 is separated from P1 deliberately. curriculum-development-plan.md §1.1 makes verifiable
     sourcing the CEO's first requirement and curriculum/README.md §5 calls a fabricated citation
     the most serious defect a module can have — it must not be gradable down into "a factual
     issue" to let a cluster pass. -->

---

## 4. Clean Documents — State Them Plainly

<!-- REQUIRED SECTION. academic-neural-unit-00/templates/README.md § Design Rules, rule 3: no ANU-00
     template may have a shape that makes a null result look like an incomplete one. A reviewer who
     found nothing wrong with a document must SAY SO, in words, here. An empty problems table read
     alongside an unfilled section is indistinguishable from a review that was never finished, and
     the Lead's synthesis review cannot tell the two apart. -->

For every document I reviewed and found genuinely clean, I state so explicitly:

- [`path/to/document.md`] — **Reviewed in full; no problems found.** [One line on what I checked
  hardest and what survived it. A clean verdict earns more trust when it names what could have
  failed.]

**If no document was clean, say that instead:** [e.g. "Every document in this cluster carries at
least one recorded problem." — do not leave this section empty either way.]

---

## 5. Cluster-Level Verdict

| Document                | Verdict                 | Blocking severity present |
| ----------------------- | ----------------------- | ------------------------- |
| [`path/to/document.md`] | [Pass / Needs revision] | [P0 / P1 / None]          |

**Cluster summary:** [How many pass outright, how many need revision. Do not average the cluster
into a single grade — the Lead's synthesis needs the per-document verdicts, not a mood.]

**The one thing I would fix first, if only one thing could be fixed:** [Name it.]

---

## 6. Scope Boundary

<!-- Required, per curriculum/README.md §6: this review cycle stops at the Lead's comprehensive
     review. A reviewer's job here is to find and record, not to rewrite. Recording an issue is
     complete work; a "needs revision" verdict is a complete result of this cycle, not an
     unfinished one. -->

**Did I edit any curriculum document?** [No — issues are recorded here for the author / Yes, and
why, which requires the Lead's agreement]

**Out of scope for this review:** [Anything I noticed but deliberately did not judge — e.g. another
cluster's documents, the module→author assignment, the curriculum's overall scope. Note it; do not
rule on it.]

---

**[Reviewer Name], [ANU-00 role] — [YYYY-MM-DD]**
