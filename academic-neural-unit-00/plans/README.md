# academic-neural-unit-00/plans/ — CEO-Facing Implementation Plans

Every ANU-00 initiative that requires CEO sign-off **before** production work begins gets its plan
filed here — not inside the deliverable's own folder. `curriculum-development-plan.md` originally
lived directly under `curriculum/`, alongside the finished modules it produced; that conflated two
different objects (a proposal awaiting approval, and the delivered artifact the proposal produced)
in one folder, and would not have scaled to a second curriculum-related plan without ambiguity
about which plan a given file belonged to. This folder exists to keep that separation clean, for
the curriculum and for any future ANU-00 deliverable that needs the same CEO approval gate.

---

## Rule

Every plan gets its own dated subfolder, the same `YYYY-MM-DD-<slug>/` pattern used by
`knowledge-base/` and `curriculum/reviews/`:

```
plans/
├── README.md                                          ← this file
├── YYYY-MM-DD-<plan-slug>/
│   └── <plan-name>.md                                 ← the plan itself, plus any supporting docs
└── YYYY-MM-DD-<plan-slug>/                             ← the next plan, independent of the first
    └── ...
```

- **Date** = the date the plan was drafted/submitted for approval (matching the date already on
  the document — do not invent a different one).
- **Slug** = a short, specific description of what the plan is for — `curriculum-first-production-run`,
  not a generic `plan-1`.
- A plan's **Status** field inside the document itself (Proposal / Approved / Superseded) is the
  source of truth for whether it's still awaiting sign-off — the folder location does not change
  once a plan is approved and executed. The plan stays exactly where it was approved; the resulting
  deliverable is filed and revised independently under its own top-level folder
  (`curriculum/`, or whatever the deliverable's category turns out to be).
- Once execution starts, the deliverable and its own review/revision records live and evolve under
  their own folder (e.g. `curriculum/`), not here. This folder holds the plan that authorized the
  work, not a running log of the work itself.

## Existing Plans

| Plan                                                        | Date       | Produced                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `2026-08-17-curriculum-first-production-run/`               | 2026-08-17 | The 24-module bilingual curriculum under `curriculum/` (approved and executed)                                                                                                                                                                                                               |
| `2026-08-19-curriculum-coding-and-post-training-extension/` | 2026-08-19 | 8 new modules (coding practicum + post-training track) addressing the Pass 3 review's scope decision S-2 — **approved by CEO; execution was deferred until after the external-audience remediation below, which closed 2026-08-26 — now unblocked, pending explicit CEO direction to begin** |
| `2026-08-26-curriculum-external-audience-remediation/`      | 2026-08-26 | Content-independence remediation across the existing 24 modules addressing the Pass 3 review's scope decision S-1, per CEO ruling that the curriculum now serves an external, general-purpose audience — **approved by CEO 2026-08-26; executed and closed the same day**                    |

## Why Not Just Leave the Plan Inside the Deliverable's Folder

A plan and its deliverable are different objects with different lifecycles: the plan is a
point-in-time proposal that either gets approved once and then stays historical, while the
deliverable it authorizes (`curriculum/`) is a standing, revised-in-place body of work with its own
internal organization (module levels, dated review rounds, and so on). Filing both under the same
folder — as the original `curriculum/curriculum-development-plan.md` placement did — works for
exactly one plan, but breaks down the moment a second, related plan needs to exist (e.g. a
follow-up production run extending the same curriculum): there is no way to tell, from a flat
folder, which plan authorized which files without reading every document's own dates and cross-
references. Dating and separating the plans the same way `knowledge-base/` and `curriculum/reviews/`
already do avoids that ambiguity from the start.
