# academic-neural-unit-00/templates/ — ANU-00 Research Templates

Document templates for ANU-00's own research process. Established 2026-07-24 under CEO delegation
of full responsibility to Dr. Naledi Mokoena, ANU-00 Lead. `observation-record.md` added 2026-07-25
on CEO approval, closing a gap the original five did not cover: they captured how to reproduce a
_finding_, but nothing captured how to reproduce an _incident_ — the run that behaved oddly, the
configuration that failed. That is a different object and now has its own record.

---

## Why These Live Here and Not at Root

Root `templates/` holds shapes that are **genuinely generic across all four co-resident systems** —
that folder's own README is explicit that this is the only thing it holds. A research-programme
charter is not that: it encodes ANU-00's charter fields, its stage-of-inquiry test, and its crew's
specific design rules. Filing it at root would misrepresent an ANU-00 instrument as a
workspace-wide one.

The inverse rule holds too, and it is why this folder is smaller than it might have been: **where a
root template already covers the shape, ANU-00 uses it rather than growing a twin.**

| Need                                     | Use                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------- |
| Internal deliberation record             | `templates/meeting-records/meeting-minutes.md` (root)               |
| Multi-party sign-off on completed work   | `templates/review-records/final-review.md` (root)                   |
| Running propose-then-decide decision log | Follow the `formation-report.md` convention — a pattern, not a form |

---

## Directory Structure

```
templates/
├── README.md                                   ← this file
├── programme-records/                          ← the chartering side: before and around a programme
│   ├── research-programme-charter.md
│   ├── open-question-log.md
│   ├── observation-record.md
│   └── referral-note.md
└── knowledge-base/                             ← the archive side: what gets filed and how it is indexed
    ├── research-report.md
    └── taxonomy-change-record.md
```

Split by **which side of the process the document serves** — chartering a programme versus filing
and indexing its output — mirroring the reasoning root `templates/` uses for its own two
categories. A new template joins whichever side it belongs to, or founds a third category if
neither fits. Do not force a genuinely new shape into one of these two.

---

## Available Templates

| Template                                          | Pattern       | Owner                  | Use for                                                                                                                       |
| ------------------------------------------------- | ------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `programme-records/research-programme-charter.md` | Point-in-time | Dr. Mokoena (ratifies) | Chartering a research programme — all six steps of `research-programme-chartering.md`                                         |
| `programme-records/open-question-log.md`          | Append-only   | Dr. Mokoena            | The standing register a non-falsifiable question is routed to instead of being chartered                                      |
| `programme-records/observation-record.md`         | Point-in-time | Recording scientist    | Capturing one reproducible incident — a run, failure, or example — so another researcher can reproduce it from the file alone |
| `programme-records/referral-note.md`              | Point-in-time | Originating scientist  | Recording a production-tooling need discovered mid-research, scoped **out**                                                   |
| `knowledge-base/research-report.md`               | Point-in-time | Authoring scientist    | The knowledge-base entry every research-design skill requires                                                                 |
| `knowledge-base/taxonomy-change-record.md`        | Append-only   | Tobias Lindqvist       | Taxonomy current state plus its explicit, logged change history                                                               |

**Never mix the two patterns.** Point-in-time records get a new file when content changes;
append-only records get a new row or section and never lose a prior one.

---

## Design Rules These Templates Follow

Four rules govern everything in this folder. They are the acceptance bar a reviewer applies before
any new template joins it.

1. **Every required section traces to a documented rule.** Each mandatory field cites the skill file
   or charter clause that mandates it — `neural-systems-research-design.md` §4, `formation-report.md`
   §3.1, and so on. No section exists because it is standard academic practice. If a section cannot
   name its source, it does not belong in an ANU-00 template.
2. **Rigor is structural, not exhortative.** The falsifiability condition, the claim-type split, the
   effect-size table, and the boundary check are _fields you cannot leave blank without it showing_
   — not advice in a preamble that a rushed author skips.
3. **Negative results are first-class.** No template has a shape that makes a null, negative, or
   inconclusive finding look like an incomplete one. `applied-ai-feasibility-research.md` §4 makes
   this explicit; the report template's §6.2 enforces it.
4. **No tasking surface.** No template contains a field through which ANU-00 can be assigned work
   from outside. Origination is an enumerated, ANU-00-internal list; a referral note is a record,
   not a request. This is the `formation-report.md` §2 boundary made structural rather than
   trusted to vigilance.

---

## What Was Deliberately Not Templated

- **A standalone source-ledger template.** Cross-domain sourcing rigor
  (`cross-domain-literature-synthesis.md` §2) is real and must be captured — but a ledger that
  lives in its own file detaches from the claims it supports, which is precisely the failure mode
  the rule guards against. It is a required subsection of the research report (§3.1) instead.
- **A programme-closure or sign-off template.** Root `templates/review-records/final-review.md`
  already does this, and its "we verified, we didn't just assert" discipline is exactly what a
  research closure needs. A second one would fragment the convention.
- **A research-agenda tracker.** A multi-cycle agenda is a running decision log, whose correct form
  is the `formation-report.md` convention — read that document as a worked example rather than
  filling in a form.
- **A CEO or external topic-request form.** Deliberate, and the most important omission here. Even
  a form labelled as CEO-only would normalize external origination of ANU-00 research and create a
  shape trivially copied for other requesters. The CEO already has a direct line to the ANU-00 Lead;
  that conversation does not need an intake artifact, and building one would make the
  `formation-report.md` §2 boundary a matter of who fills in which field.

---

## Usage

1. Copy the template into its destination — normally
   `academic-neural-unit-00/knowledge-base/YYYY-MM-DD-<slug>/`. Never fill one in inside
   `templates/` itself. Each template's opening HTML comment states its exact destination.
2. Fill in every bracketed placeholder. Delete the instructional HTML comments once the section is
   complete — but read them first: several carry binding rules, not hints.
3. Delete the domain rows that do not apply (the charter's §3 table, the report's §5 subsections).
   Leaving irrelevant domain scaffolding in a filed record makes it harder to see what was actually
   required of it.
4. Run Prettier before finalizing, per root `CLAUDE.md` §1: `prettier --write "<file-path>"`.
