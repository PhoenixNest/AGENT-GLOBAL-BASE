# Enterprise-Level Engineering Assessment — [Module or System Name]

<!-- Copy this file into a NEW DATED FOLDER under the type-scoped benchmark tree (never into
     template/ itself), per `core-component-00/benchmarks/CLAUDE.md` § Directory Structure:

       benchmarks/engineering/<module-slug>/YYYY-MM-DD-<slug>/enterprise-assessment.md
       benchmarks/retrieval-augmented-generation/YYYY-MM-DD-<slug>/enterprise-assessment.md

     The file inside is always named `enterprise-assessment.md`.

     This is a BENCHMARK against the outside world, not an internal compliance check. If the
     question is "does this satisfy our own ASGF/pipeline rules," use
     `crew/director/elias-vance/skills/asgf-compliance-audit.md` instead. If the question is
     "how does our design compare to what production systems elsewhere are doing," use this. -->

---

## How to Use This Template

Read this section before filling anything in. The order below is the required order of work —
the Benchmark Table cannot be written before the Research Freshness table, because every cell in
it must point at a row that already exists there.

1. **Run the live research pass first.** Populate Research Freshness completely, including the
   verbatim excerpt for every source. A benchmark written from training-data recall is invalid
   regardless of how recent the assessor's cutoff is.
2. **Write the Benchmark Table second**, citing source IDs (`S1`, `S2`, …) in every row whose
   "Enterprise-Standard Practice" cell makes an external claim.
3. **Write the Remediation Plan third**, citing a Benchmark Table row ID (`B1`, `B2`, …) in every
   row, plus a one-line severity justification that quotes the governing severity scale.
4. **Name a Reviewer other than the Assessor** and have them check the excerpt-to-claim mapping
   before the document is treated as final.
5. Add an entry to `benchmarks/README.md`, then run
   `prettier --write "<file-path>"`.

### The One Property This Template Exists to Guarantee

Every external claim in this document must be traceable to text that a named source actually
contains. Logging that a search happened, that a URL was retrieved, and that a date was recent
does **not** establish this. Only a verbatim excerpt does. If an excerpt cannot be quoted, the
claim cannot be written — log the search as a negative result instead (see the Research
Freshness status vocabulary) and mark the corresponding benchmark dimension as unassessed.

### Adapting for a Documentation-Only Module

Some modules ship no runnable code — `engineering/prompt-engineering/` is the standing example:
knowledge base only, no `implementations/`, no `testing/` (see
`core-component-00/CLAUDE.md` § The Five-Module Engineering Stack). Benchmarking one requires an
adapted shape:

- **"Our Current State" cites document sections, not `file:line`** — e.g.
  `patterns/advanced-patterns.md § Chain-of-Thought`. A `file:line` citation into prose is
  spurious precision; a section anchor is the honest equivalent.
- **Benchmark the documented guidance against external practice** — does what we tell teams to
  write match what production systems elsewhere are doing? That is the question this template
  answers for a docs-only module.
- **Do not drift into internal doc-consistency auditing.** "Section X contradicts section Y,"
  "this doc is stale relative to that one," and "our own standard isn't followed here" are
  internal-compliance findings. They belong to
  `crew/director/elias-vance/skills/asgf-compliance-audit.md`, not to this template. A benchmark
  that fills up with internal-consistency findings has quietly stopped being a benchmark.
- **Test-coverage and performance dimensions are Not Applicable, not Gaps.** Mark them `N/A` with
  a one-line rationale rather than recording a gap the module's type makes meaningless.

---

## Metadata

| Field                           | Value                                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| **Assessment ID**               | `YYYY-MM-DD-<module-slug>`                                                            |
| **Date**                        | YYYY-MM-DD                                                                            |
| **Assessor**                    | [Name, role — typically Dr. Elias Vance + the relevant module lead(s)]                |
| **Reviewer**                    | [Name, role — MUST be a different person from the Assessor; see below]                |
| **Module(s) / System Assessed** | [e.g. `engineering/context-engineering/`, or "workspace-wide engineering design"]     |
| **Requestor**                   | [User / CEO / Research Programme]                                                     |
| **Prior Assessment**            | [Link to previous `enterprise-assessment.md` for this module, or "None — first pass"] |

**Reviewer requirement.** An assessment with no named Reviewer, or whose Reviewer is its own
Assessor, is a **draft** — not a finding, not citable, and not eligible for the index in
`benchmarks/README.md`. The Reviewer's specific obligation is not a general read-through: they
must independently confirm that (a) every Research Freshness excerpt actually appears in the
cited source, (b) every excerpt actually supports the claim it is attached to, and (c) every
Benchmark Table and Remediation Plan row carries the source and row IDs this template requires.
Per `crew/CLAUDE.md` § Authority Scope, the Reviewer may be the paired module lead, another
module lead, or Dr. Tomasz Wieczorek (Safety & Evaluation) for an independent check.

---

## Research Freshness (Mandatory)

<!-- This section exists to structurally enforce two non-negotiable rules:

     1. An enterprise benchmark cannot be satisfied by training-data knowledge alone, regardless
        of how recent the assessor's knowledge cutoff is. "Enterprise-standard practice" is a
        moving target — citing it requires a live retrieval pass in the same session the
        assessment is written, every time this template is used.

     2. A retrieval pass proves only that a search happened. The Verbatim Excerpt column is what
        proves the claim came from what the search returned. Both are required. -->

**Knowledge cutoff of assessor:** [Date] — flag any claim below sourced from training data alone
with `[Knowledge Cutoff - verify]`.

**Live research performed this session:** [Yes/No — must be Yes for this document to be valid]

### Source Register

| ID  | Claim Supported                              | Query Run           | Source       | Retrieval Date | Verbatim Excerpt                             | Status                                     |
| --- | -------------------------------------------- | ------------------- | ------------ | -------------- | -------------------------------------------- | ------------------------------------------ |
| S1  | [the specific claim this source establishes] | [search query text] | [Title](URL) | YYYY-MM-DD     | "[exact quoted text copied from the source]" | Verified — excerpt supports claim          |
| S2  | [claim that was sought but not found]        | [search query text] | —            | YYYY-MM-DD     | —                                            | Searched — no supporting source found      |
| S3  | [claim sourced from our own code/docs]       | [n/a — internal]    | `path:line`  | YYYY-MM-DD     | "[exact quoted text copied from that file]"  | Internal — verified against primary source |

### Rules for This Table

- **One row per source-claim pair, not per search.** If one source supports three distinct
  claims, it gets three rows (`S4`, `S5`, `S6`) — each with its own excerpt. A single row whose
  excerpt supports only one of three attached claims is exactly the failure this column exists to
  prevent.
- **The excerpt must be copied, not paraphrased.** Quotation marks, exact wording, no
  reconstruction from memory of what the page said. If the source is a PDF or a video
  transcript, quote the passage and give the locator (page, section, timestamp).
- **The excerpt must support the claim on its own.** Read the excerpt in isolation: if a reader
  seeing only that text would not conclude the claim, the pairing fails — either find a better
  passage or downgrade the claim. An excerpt that contradicts the claim, or that comes from a
  different source than the one credited, is a fabrication, not a citation error.
- **A claim with no matching excerpt cannot be written.** There is no "verified by search"
  shortcut, no "the source generally discusses this" allowance, and no forcing a weak passage to
  stand in for one that does not exist.
- **Negative results are logged, not deleted.** If a search for supporting evidence found
  nothing, keep the row with status `Searched — no supporting source found`. An honest empty
  result is a valid, useful outcome; a silently dropped search is an audit-trail hole.

### Status Vocabulary

| Status                                       | Meaning                                                                                              | Permitted Downstream Use                                                                            |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `Verified — excerpt supports claim`          | The quoted text appears in the cited source and supports the claim on its own reading                | Citable in any Benchmark Table or Remediation Plan row                                              |
| `Searched — no supporting source found`      | A genuine search was run; nothing found that supports the claim                                      | **Not citable.** The dependent benchmark dimension is marked `Unassessed — no source` (see below)   |
| `Partial — excerpt supports a weaker claim`  | The source supports something narrower than what was sought                                          | Citable **only** for the narrower claim, restated in the Benchmark Table to match the excerpt       |
| `Contradicted — source states the opposite`  | The search found the reverse of the expected claim                                                   | Citable, but the Benchmark Table cell must state the source's actual position, not the expected one |
| `Internal — verified against primary source` | Claim comes from CC-00's own code, docstrings, README, or docs, and was opened and read this session | Citable; subject to the Internal-Source Verification clause below                                   |

### Internal-Source Verification (Mandatory)

A claim is **not** exempt from verification because its source is inside this workspace.
Internal sources carry the same failure mode as external ones — a plausible-looking attribution
that the actual text does not support — and they are more dangerous because they feel
pre-trusted.

Apply the identical standard:

- **Open the file and read the passage this session.** Do not cite a docstring, README line, test
  name, or config default from recall of having read it before.
- **Quote it verbatim in the Source Register** with a `path:line` locator, status
  `Internal — verified against primary source`.
- **A citation embedded in our own code is a claim about the outside world, not an internal
  fact.** An arXiv reference, a vendor benchmark number, an RFC, or a "standard practice" note
  found inside one of our docstrings or READMEs asserts something external. Verifying that our
  file says it establishes only that our file says it. Before repeating it as an
  Enterprise-Standard Practice claim, retrieve the referenced work itself and register it as a
  separate external source with its own excerpt. If the referenced work cannot be retrieved or
  does not say what our file attributes to it, that discrepancy is itself a finding.
- **"Our Current State" claims are internal claims and get the same treatment** — a `file:line`
  or doc-section citation must point at text that actually says what the cell says.

---

## Assessment Scope

### What Was Assessed

[Which module(s), file(s), or workspace-wide design surface this assessment covers]

### Why Now

[Trigger for this assessment — CEO directive, scheduled cadence, incident, new module shipped]

### Out of Scope

[What was explicitly not assessed in this pass, and why — e.g. "Harness Engineering excluded;
see the paired harness-engineering assessment folder instead"]

---

## Verdict Vocabulary (Binding)

Every Benchmark Table row closes with exactly one of these four verdicts, or `N/A` /
`Unassessed — no source`. The vocabulary is fixed: do not invent adjacent labels
("Mostly passes", "Ahead in spirit", "Effectively at parity"), because each label below carries a
different evidentiary bar and a softened synonym smuggles a claim past its bar.

| Verdict                    | Means                                                                                   | Evidentiary Bar                                                                                                                                                                                                                                                                                          |
| -------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pass at parity**         | Our implementation does substantively what current external practice does               | One `Verified` external source whose excerpt describes the practice, **plus** an internal citation showing we do it. Both IDs appear in the row.                                                                                                                                                         |
| **Pass, ahead**            | Our implementation does something current external practice does not, or does it better | **Highest bar in this template.** Requires a `Verified` external excerpt that positively establishes the comparison — a source stating the limitation, a benchmark showing the delta, or an explicit external statement of where the practice stops. Absence of evidence is not evidence of being ahead. |
| **Partial**                | We do part of what external practice does; a named element is missing or weaker         | A `Verified` external excerpt describing the full practice, plus an internal citation showing which specific element we implement and which we do not. "Partial" without naming the missing element is not a finding.                                                                                    |
| **Gap**                    | External practice does something we do not do at all                                    | A `Verified` external excerpt describing the practice, plus a stated basis for the absence (searched the module and it is not present — say where you looked).                                                                                                                                           |
| **N/A**                    | The dimension does not apply to this module's type                                      | One-line rationale (e.g. "documentation-only module — no test suite to benchmark").                                                                                                                                                                                                                      |
| **Unassessed — no source** | The dimension was in scope but no supporting source was found                           | The corresponding `Searched — no supporting source found` row ID. This is an honest outcome and is preferred over any of the four verdicts above backed by a weak citation.                                                                                                                              |

### Prohibited Claim Forms

- **Unsourced negative claims about industry practice are forbidden.** "Not commonly
  documented", "rare in production systems", "most teams do not do this", "no major framework
  offers this" — each asserts a fact about the state of the industry, and each requires the same
  `Verified` excerpt as any positive claim. A negative claim is harder to source, not exempt from
  sourcing. If no source establishes it, delete the claim; do not soften it into a hedge
  ("appears to be uncommon") and keep it.
- **`Pass, ahead` may not rest on the assessor's inability to find a counterexample.** "I
  searched and found nothing comparable" supports `Unassessed — no source`, never `Pass, ahead`.
- **Do not upgrade a verdict to balance the table.** A benchmark reporting only gaps is a valid
  result. So is one reporting only parity.

---

## Benchmark Table

The core deliverable. One row per dimension assessed. Every "Enterprise-Standard Practice" cell
must cite the Source ID(s) that support it, and every "Our Current State" cell must cite a
`file:line` (code modules) or document section (documentation-only modules).

| ID  | Dimension                       | Our Current State                            | Internal Source ID(s) | Enterprise-Standard Practice          | External Source ID(s) | Verdict                                        | Severity     |
| --- | ------------------------------- | -------------------------------------------- | --------------------- | ------------------------------------- | --------------------- | ---------------------------------------------- | ------------ |
| B1  | [e.g. Token budget enforcement] | [what the code/docs actually do — file:line] | S3                    | [what current external practice does] | S1                    | [Pass at parity / Pass, ahead / Partial / Gap] | [P0–P3 or —] |
| B2  | [dimension in scope, unsourced] | [what we do — file:line]                     | S7                    | —                                     | S2                    | Unassessed — no source                         | —            |

**Rules.**

- **No orphan claims.** A row whose Enterprise-Standard Practice cell is non-empty and whose
  External Source ID(s) cell is empty is incomplete — fill it or delete the claim. The same
  applies to Our Current State and its Internal Source ID(s).
- **Multiple IDs are fine, vague ones are not.** `S1, S4` is acceptable; "see Sources" is not.
- **Row IDs are stable within the document.** The Remediation Plan references them; do not
  renumber after writing it.
- **Severity is populated only for `Partial` and `Gap` rows**, using the scale named in the
  Remediation Plan below. `Pass` and `N/A` rows carry `—`.
- Populate with as many rows as the assessed surface warrants. Do not pad with rows that carry no
  real finding — a short table of real gaps beats a long table of restated non-findings.

---

## Severity-Ordered Remediation Plan

One row per `Partial` or `Gap` finding, ordered by severity (P0 first), not by benchmark row
order or by layer.

| ID  | Priority    | Benchmark Row | Gap               | Source ID(s) | Owner                                              | Fix                         | Severity Justification                                                      |
| --- | ----------- | ------------- | ----------------- | ------------ | -------------------------------------------------- | --------------------------- | --------------------------------------------------------------------------- |
| R1  | P0/P1/P2/P3 | B1            | [restate the gap] | S1, S3       | [crew member per `crew/CLAUDE.md` Authority Scope] | [concrete remediation step] | [Scale name] — "[quoted scale text]"; [why this finding meets that wording] |

**Rules.**

- **Every row must cite a Benchmark Table row ID.** This is structural, not advisory: a
  remediation row with an empty or non-existent Benchmark Row reference is invalid and must be
  removed or given a supporting benchmark row. A fix with no benchmarked finding behind it is an
  opinion, and this document does not carry opinions.
- **Every row must cite the Source ID(s)** that established the gap — inherited from its
  benchmark row, not re-derived.
- **Every row must carry a one-line severity justification** in the form specified below.
- Owners are named individuals per `crew/CLAUDE.md` § Authority Scope, not teams.

### Severity Justification Requirement

Two severity scales exist in this workspace and they do not mean the same thing. The assessor
must state **which scale governs this assessment**, quote the specific text of the level applied,
and state in one line why the finding meets that wording. "P1 — degrades quality" restates the
label; it does not justify it.

**Scale A — ASGF Gap Severity** (`crew/director/elias-vance/skills/asgf-compliance-audit.md` §
Gap Severity Classification). The default for benchmarks of CC-00 modules, so findings here
compose cleanly with any follow-on ASGF audit:

| Level  | Verbatim definition to quote                                                              |
| ------ | ----------------------------------------------------------------------------------------- |
| **P0** | "Gap that will cause production failure under normal load or after extended sessions"     |
| **P1** | "Gap that will degrade output quality or reliability at scale but does not cause outages" |
| **P2** | "Gap that reduces engineering maintainability or makes the system harder to extend"       |
| **P3** | "Improvement opportunity with no current reliability impact"                              |

**Scale B — Workspace general QA defect scale** (root `CLAUDE.md` § Pipeline Guardrails). Applies
when a finding concerns a shipping product surface rather than a CC-00 engineering module:

| Level  | Verbatim definition to quote                                                                              |
| ------ | --------------------------------------------------------------------------------------------------------- |
| **P0** | "A crash, data-loss, or security breach (P0) … blocks release and cannot be downgraded to advance a gate" |
| **P1** | "… or broken core feature (P1) blocks release and cannot be downgraded to advance a gate"                 |

**Declared scale for this assessment:** [Scale A — ASGF / Scale B — workspace QA] — [one line on
why this scale governs the assessed surface]

**At the P0 boundary, be explicit.** P0 is the level that changes the Compliance Verdict, so a
P0 classification must show the finding satisfying the quoted wording, not merely sounding
serious. Under Scale A, a design shortcoming that has never produced a failure and has no
identified load or session-length trigger is not "will cause production failure" — it is P1 or
P2. Under Scale B, "important" is not "crash, data-loss, or security breach". Mixing the two
scales inside one document is a defect: pick one, declare it, apply it throughout, and if a
finding genuinely belongs to the other scale, say so explicitly in that row's justification.

---

## Compliance Verdict

**[Meets Enterprise Standard / Conditional — P1 gaps open / Below Standard — P0 gaps present]**

[2-3 sentence synthesis: does this module/system stand up against current external practice, and
what's the single biggest lever to close the gap if not]

### Evidence Completeness Statement

Required. State plainly, in the assessor's own words:

- How many benchmark rows carry a `Verified` external source, and how many are
  `Unassessed — no source`.
- Any dimension the assessor believed important but could not source.
- Whether the Reviewer named in Metadata has completed the excerpt-to-claim check.

A verdict rendered over a table with substantial unassessed rows must say so here. An assessment
that hides its coverage gaps behind a confident verdict is worse than one that reports thin
coverage honestly.

---

## Sources

<!-- Mirror every source cited in the Research Freshness Source Register, as markdown
     hyperlinks, prefixed with its source ID. Mandatory — do not omit even though the Source
     Register already lists them. Include internal sources as plain paths, and include
     negative-result rows with an explicit "no source found" note so the list matches the
     register one-for-one. -->

- **S1** — [Title](URL)
- **S2** — _Searched, no supporting source found: "[query text]"_
- **S3** — `path/to/internal/file.py:120`

---

## Version History

| Version | Date       | Author | Changes                       |
| ------- | ---------- | ------ | ----------------------------- |
| 1.0     | YYYY-MM-DD | [Name] | Initial enterprise assessment |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-16
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
