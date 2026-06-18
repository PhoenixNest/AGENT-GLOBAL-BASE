# company/pipeline/ — Development Pipeline Definitions

Canonical source for all company development pipeline specifications. The `pipeline.md` inside each
subfolder is the highest-authority document for that pipeline — it overrides any summary or overview.

---

## Pipeline Variants

| Folder                | Pipeline        | Stages        | Pattern                              |
| --------------------- | --------------- | ------------- | ------------------------------------ |
| `_base/`              | Shared skeleton | 10-stage base | Source of truth for shared structure |
| `mobile-development/` | Mobile          | 13 stages     | `_base/` + mobile delta              |
| `web-development/`    | Web             | 13 stages     | `_base/` + web delta                 |
| `backend-api/`        | Backend API     | 13 stages     | `_base/` + API delta                 |
| `full-stack/`         | Full-Stack      | 13 stages     | `_base/` + full-stack delta          |
| `recruitment/`        | Recruitment     | 9 stages      | Standalone — does not use `_base/`   |

**Choose the pipeline by project type.** Do not conflate the mobile, web, API, and full-stack
pipelines — they share a base but have pipeline-specific stage deltas, templates, and agent
ownership. The recruitment pipeline is entirely separate and shares no structure with the others.

---

## Base + Delta Pattern

The four development pipelines (Mobile, Web, Backend API, Full-Stack) extend a shared 10-stage
skeleton:

```
pipeline/_base/          ← Shared stage structure, templates, monitoring templates
pipeline/<type>/         ← Type-specific delta (overrides and additions)
  pipeline.md            ← THE canonical truth for this pipeline (read this first)
  templates/             ← Stage-specific templates
  templates/monitoring/  ← progress.md / session-log.md / checkpoint.json templates
```

When working on a specific pipeline, **always read that pipeline's `pipeline.md` first** — not the
base skeleton — as deltas may override base behaviour.

---

## Stage Gate Rules (all development pipelines)

Stages marked ✅ are **hard stops**. You must present the completed deliverable, request user
sign-off, and wait. Never auto-advance.

| Rule                      | Applies At                                                                                      |
| ------------------------- | ----------------------------------------------------------------------------------------------- |
| Technology Decision Lock  | Stage 3 — ADRs and TSD locked on user approval; changes require new ADR + full Stage 3 re-entry |
| PRD + SRD Pairing         | Stage 1 onward — these two documents travel together through all stages                         |
| Stage 6 Remediation Loop  | After any remediation, the full review panel process repeats from the beginning                 |
| P0/P1 Defect Non-Override | All stages — crash, data-loss, security breach, or core feature failure cannot be downgraded    |
| Trim-to-Pass Forbidden    | Stage 6/8 — removing features or disabling security to pass review is itself a P0 defect        |

---

## Progress Monitoring (Stage 4+)

Any project at or beyond Stage 4 must maintain three files inside the project folder:

| File              | Purpose                     |
| ----------------- | --------------------------- |
| `progress.md`     | Real-time state             |
| `session-log.md`  | Audit trail                 |
| `checkpoint.json` | Machine-readable milestones |

Use the templates in `pipeline/<type>/templates/monitoring/` to create these files.

Any task exceeding its estimate by >20% triggers a CTO → CPO schedule risk notification.

---

## ASE Template Parity

All four development pipelines have achieved 100% ASE template parity. Monitoring templates in each
pipeline's `templates/monitoring/` folder conform to the ASE compliance standard defined in
`core-component-00/agent-systems-engineering/governance/compliance-standard.md`.

---

## Rules

- Read the specific pipeline's `pipeline.md` before producing any stage artifact.
- Never conflate stage numbers across different pipelines — stage 5 in Mobile ≠ stage 5 in Recruitment.
- The `_base/` folder is a reference skeleton — the typed pipeline's delta is the binding document.
- Do not edit `pipeline.md` to reflect technology changes made after Stage 3 approval. Create a new
  ADR and re-enter Stage 3 instead.
