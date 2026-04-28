# Pipeline Base + Deltas — Pattern Guide

| Field          | Value                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**     | Authoritative                                                                                                                                                                                                                                                                                                                                                                                  |
| **Owner**      | Software Architect Rafael Okonkwo (under CTO Nakamura)                                                                                                                                                                                                                                                                                                                                         |
| **Effective**  | 2026-04-21                                                                                                                                                                                                                                                                                                                                                                                     |
| **Cross-Refs** | [`pipeline.md`](./pipeline.md), [`delta-template.md`](./delta-template.md), [`independent-challenge-template.md`](./independent-challenge-template.md), [`adr-template.md`](./adr-template.md), [`incident-response.md`](./incident-response.md), [`experimentation-spec-template.md`](./experimentation-spec-template.md), [`dogfood-telemetry-template.md`](./dogfood-telemetry-template.md) |

---

## 1. Why Base + Deltas

The four product pipeline shapes (mobile, web, backend, full-stack) share the same 10-stage skeleton, the same defect taxonomy (P0–P3), the same Progress Sync Protocol, and the same gate-criteria templates. Only the platform-specific blocks differ — the Platform Strategy Matrix, the per-stage technology mandates, and the platform compliance gates.

Maintaining four parallel pipeline files duplicates >90% of content and creates a structural drift hazard: every pipeline-level change requires editing four files, and changes that should have applied uniformly often land in only some of the four (i18n placement, stage 0 insertion, gate authority changes are the historical examples).

The fix is the standard "shared base + thin overlays per product type" pattern:

```text
company/pipeline/
├── _base/
│   ├── README.md                          ← this file
│   ├── pipeline.md                        ← canonical 10-stage skeleton (the SHARED truth)
│   ├── delta-template.md                  ← the shape every product pipeline must conform to
│   ├── adr-template.md                    ← canonical ADR shape (versionable, supersedable)
│   ├── independent-challenge-template.md  ← red-team review protocol for multi-condition gate reports
│   ├── incident-response.md               ← Sev ladder + on-call + blameless postmortem (Stage 11 universal)
│   ├── experimentation-spec-template.md   ← A/B test design template paired with Stage 1 PRDs
│   └── dogfood-telemetry-template.md      ← Stage 9.5 internal beta telemetry report shape
├── mobile-development/
│   └── delta.md                           ← pipeline-type-specific overlay (mobile)
├── web-development/
│   └── delta.md                           ← pipeline-type-specific overlay (web)
├── backend-api/
│   └── delta.md                           ← pipeline-type-specific overlay (backend)
├── full-stack/
│   └── delta.md                           ← pipeline-type-specific overlay (full-stack)
└── recruitment/                           ← UNCHANGED — recruitment is shape-incompatible (9-stage automated)
```

> **Recruitment is explicitly out of scope** for the base + delta pattern. Recruitment "differs in shape" from the four product pipelines (9 stages, automated cadence, candidate-centric flow). It remains a single self-contained pipeline file.

---

## 2. How the Pattern Works

| File                                | Purpose                                                                                                                                                                                                                        |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `pipeline.md`                       | The canonical 10-stage (plus Stage 0 and Stage 11) skeleton. Stages, severity model, Progress Sync Protocol, gate criteria. Uses `{{DELTA: ...}}` placeholder tokens for product-specific blocks.                              |
| `delta-template.md`                 | The required shape of every product pipeline's `delta.md`. Lists the placeholders each product must fill. A `delta.md` MUST address every placeholder; it MAY add product-specific concerns under "Additional Considerations." |
| `adr-template.md`                   | Canonical ADR shape used at every stage that produces an architectural decision. ADRs are versionable and supersedable — a superseding ADR carries a `Supersedes` field referencing the prior ADR ID.                          |
| `independent-challenge-template.md` | The protocol for red-team challenges to multi-condition gate reports. Five attack vectors, 48-hour time-box, designated independent challenger persona.                                                                        |
| `incident-response.md`              | Universal Stage 11 incident-response model: Sev0–Sev3 ladder, on-call rotation rules, blameless postmortem template, rollback authority chain.                                                                                 |
| `experimentation-spec-template.md`  | The A/B test design template paired with Stage 1 PRDs whenever a PRD-defined metric requires experimental validation.                                                                                                          |
| `dogfood-telemetry-template.md`     | The Stage 9.5 internal beta telemetry report shape (crash rates, ANR rates, opt-out rates, qualitative bug telemetry).                                                                                                         |

### 2.1 Resolution rules

When a project consults its pipeline:

1. Read the product `delta.md` first. The delta declares which product type the project belongs to and which placeholders it overrides.
2. For every concern the delta does NOT override, fall through to `_base/pipeline.md`.
3. ADRs, IDS, PRDs, and SRDs are produced using the templates listed in §2 above; product-specific extensions live in the delta.

### 2.2 Conformance

A `delta.md` is conformant if and only if:

- It addresses every required placeholder in `delta-template.md`.
- It does not contradict the universal rules in `_base/pipeline.md` (e.g., it cannot relax the P0 / P1 defect classification; it cannot waive the cross-cutting i18n requirement).
- Any extension under "Additional Considerations" is product-specific and does not introduce a new universal rule.

Non-conformance is a P1 defect against the delta and blocks the next gate review.

---

## 3. Authority and Sign-off

| Action                                         | Owner                                                                           |
| ---------------------------------------------- | ------------------------------------------------------------------------------- |
| Pattern stewardship + base content authorship  | Software Architect (Rafael Okonkwo)                                             |
| Per-product `delta.md` content authorship      | Pipeline-specific lead (e.g., VP Mobile for mobile delta, VP Web for web delta) |
| Sign-off on `delta.md` changes                 | CTO Nakamura + Software Architect                                               |
| Reference-update sign-off (cross-cutting docs) | Tech Writer (Henrik Larsen / Amina Razak)                                       |

---

## 4. Document Version History

| Version | Date           | Author             | Changes                                                                                                                                                                       |
| ------- | -------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | Software Architect | Initial authoritative pattern guide. `_base/` and four product `delta.md` files are the canonical resolution path; recruitment remains shape-incompatible and self-contained. |
