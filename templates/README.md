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

## Available Templates

| Template             | Use for                                                                        |
| -------------------- | ------------------------------------------------------------------------------ |
| `meeting-minutes.md` | Any internal deliberative meeting where attendees discuss and record decisions |
| `final-review.md`    | Any multi-party sign-off verifying completion before closing a body of work    |

### `meeting-minutes.md`

Generic internal-meeting record: attendees + roles, agenda, numbered discussion sections,
decisions-recorded table, next steps. Candidate future uses: CC-00 research-programme chartering
discussions, Company Stage 6 Architecture & Conformance Review panel deliberations, Studio crew
composition or project greenlight/kill discussions, any future new-entity formation.

### `final-review.md`

Generic joint-verification record: named reviewers, an explicit method section proving each
reviewer checked primary records rather than restating prior claims, per-reviewer findings, and a
joint recommendation. The "we verified, we didn't just assert" discipline is the part worth
enforcing every time this template is used — don't let a reviewer skip straight to a conclusion.
Candidate future uses: Company QBR (Stage 11 Live Operations), CHRO hiring-outcome audits for any
department's recruitment cycle, Stage 8 Testing → Integrity Verification sign-off, any
cross-department joint approval.

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

1. Copy the relevant template into the folder where the record belongs (the meeting's own system —
   `company/`, `studio/`, `core-component-00/`, or `academic-neural-unit-00/` — not into
   `templates/` itself).
2. Fill in every bracketed placeholder. Delete instructional HTML comments once the section is
   filled in.
3. Follow the workspace's Prettier and naming conventions (root `CLAUDE.md` §1, §5) before
   finalizing.
