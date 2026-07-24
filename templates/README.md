# templates/ — Cross-System Document Templates

Reusable document templates for processes that span more than one of the workspace's co-resident
systems (The Company, The Studio, the CC-00 Lab, ANU-00). Established 2026-07-23, extracted from
the documents produced during ANU-00's formation and staffing
(`academic-neural-unit-00/formation/2026-07-23-formation-meeting/`).

---

## Why This Folder Exists

Every existing template in this workspace lives inside the one system it serves —
`company/recruitment/template/`, `company/pipeline/_base/templates/`. That's correct for
system-specific artifacts (a recruitment plan, a PRD). It breaks down for documents whose _shape_
is genuinely generic across every system: a record of an internal meeting, or a joint sign-off
before closing something out. Putting those inside any one system's folder would misrepresent them
as belonging to that system. `templates/` at the workspace root is the shared home for exactly
that category — nothing else.

**Not everything from ANU-00's formation became a template here.** Two of its four output
documents generalize cleanly (below); two don't and were deliberately left out — see § What Didn't
Become a Template.

---

## Directory Structure

```
templates/
├── README.md                          ← this index
├── meeting-records/                   ← in-progress deliberation: captured while a meeting happens
│   └── meeting-minutes.md
└── review-records/                    ← post-hoc confirmation: captured after work is already done
    └── final-review.md
```

Categorized by **when in a process the record is produced**, not by which system uses it — every
template here is cross-system by definition (§ Why This Folder Exists). `meeting-records/` holds
templates for documenting a discussion as it happens; `review-records/` holds templates for
certifying completed work afterward. Each category currently holds one template; new templates
join whichever category matches their moment in the process, or found a new category if neither
fits — don't force a genuinely new shape into one of these two just to avoid adding a category.

---

## Available Templates

| Template                             | Category        | Use for                                                                        |
| ------------------------------------ | --------------- | ------------------------------------------------------------------------------ |
| `meeting-records/meeting-minutes.md` | Meeting Records | Any internal deliberative meeting where attendees discuss and record decisions |
| `review-records/final-review.md`     | Review Records  | Any multi-party sign-off verifying completion before closing a body of work    |

### `meeting-records/meeting-minutes.md`

Generic internal-meeting record: attendees + roles, agenda, numbered discussion sections,
decisions-recorded table, next steps. Candidate future uses (same category, same folder once
built): CC-00 research-programme chartering discussions, Company Stage 6 Architecture &
Conformance Review panel deliberations, Studio crew composition or project greenlight/kill
discussions, any future new-entity formation.

### `review-records/final-review.md`

Generic joint-verification record: named reviewers, an explicit method section proving each
reviewer checked primary records rather than restating prior claims, per-reviewer findings, and a
joint recommendation. The "we verified, we didn't just assert" discipline is the part worth
enforcing every time this template is used — don't let a reviewer skip straight to a conclusion.
Candidate future uses (same category, same folder once built): Company QBR (Stage 11 Live
Operations), CHRO hiring-outcome audits for any department's recruitment cycle, Stage 8 Testing →
Integrity Verification sign-off, any cross-department joint approval.

---

## What Didn't Become a Template

- **A "formation report" template was deliberately not created.** That document's real shape is a
  _running decision log_ — a charter/proposal section followed by an append-only sequence of
  numbered sections, one per new ruling, never rewriting a prior one, closed with an explicit
  closure section. That's a **convention to follow**, not a fill-in-the-blank form, since how many
  rounds of decisions it accumulates isn't knowable in advance. If you're documenting a
  propose-then-decide-over-time thread (an ADR, a phased pipeline change, another new-entity
  formation), follow this pattern by reading
  `academic-neural-unit-00/formation/2026-07-23-formation-meeting/formation-report.md` as a worked
  example, rather than filling in a template.
- **Role-profile / prospective-hire documents were not templated here** — that's already covered
  by `company/recruitment/template/recruitment-plan.md`. Creating a second, competing template for
  the same job would fragment the convention rather than standardize it.

---

## Usage

1. Copy the relevant template (from its category subfolder, e.g.
   `templates/meeting-records/meeting-minutes.md`) into the folder where the record belongs (the
   meeting's own system — `company/`, `studio/`, `core-component-00/`, or
   `academic-neural-unit-00/` — not into `templates/` itself).
2. Fill in every bracketed placeholder. Delete instructional HTML comments once the section is
   filled in.
3. Follow the workspace's Prettier and naming conventions (root `CLAUDE.md` §1, §5) before
   finalizing.
4. **Both templates are point-in-time snapshots, not living documents — new content gets a new
   file, not an edit to a past one.** A `meeting-minutes.md` instance is the record of one specific
   meeting; if a later event changes something discussed there, add a pointer note in the _new_
   document (or in whatever ongoing report tracks the decision) rather than editing the original
   minutes. Same for `final-review.md` — a second review is a new instance, not an addendum to the
   first. This is the opposite convention from a `formation-report.md`-style running decision log
   (§ What Didn't Become a Template), which is deliberately append-only in a single file — don't
   mix the two patterns.
