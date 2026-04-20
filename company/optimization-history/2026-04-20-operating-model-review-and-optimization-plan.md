# Operating Model Review & Optimization Plan

| Field             | Value                                                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Document Type** | Operating Model Review + Optimization Plan                                                                                  |
| **Plan ID**       | OPT-2026-04-20-001                                                                                                          |
| **Date**          | April 20, 2026                                                                                                              |
| **Author**        | Operating Review (acting top-tier engineering manager persona)                                                              |
| **Scope**         | `company/` (4 product pipelines + recruitment + departments + library) and `studio/casual-games/` (charter, pipeline, crew) |
| **Audience**      | CEO Peter Chen                                                                                                              |
| **Status**        | **Approved by CEO Peter Chen — Effective April 20, 2026** (all 29 findings approved as-is; 0 rejected; 0 modifications)     |
| **Version**       | 1.4                                                                                                                         |
| **Supersedes**    | None (first optimization plan recorded)                                                                                     |
| **Next Review**   | Quarterly review cadence — first checkpoint **July 19, 2026** (Day 90 milestone); see §10 Success Metrics for owners        |

---

## 1. Executive Summary

### 1.1 Verdict at a Glance

| Dimension               | Grade  | Headline                                                                                               |
| ----------------------- | ------ | ------------------------------------------------------------------------------------------------------ |
| **Documentation**       | **A−** | Genuinely above industry baseline. Honest gaps, paired artifacts, defect taxonomy are best-in-class.   |
| **Operating Model**     | **C+** | Waterfall in agile clothing. Sequential gates, full-panel reviews, and locked decisions limit reality. |
| **Production Realism**  | **C−** | Rich on artifact production, thin on telemetry, post-launch ops, and feedback loops.                   |
| **Recruitment Rigor**   | **B−** | Elite gate is well-defined but contradicts the actual hiring records (12/20 hires + buddy system).     |
| **Studio Independence** | **A−** | Correct architectural call. House-of-brands and pipeline separation match Supercell/Riot patterns.     |

### 1.2 Headline Statement

> The system is **governance-rich and execution-thin**. It is at risk of confusing artifact production with shipping software. The optimization actions in Sections 4–6 close that gap.

### 1.3 Findings Distribution

| Severity                  | Count  | Definition                                                                    |
| ------------------------- | ------ | ----------------------------------------------------------------------------- |
| **P0 — Critical**         | 6      | Systemic risks that will cause real failures. Fix before next project starts. |
| **P1 — Important**        | 8      | Will degrade outcomes meaningfully. Fix in the next quarter.                  |
| **P2 — Polish**           | 15     | Maintenance / clarity / consistency improvements. Fix opportunistically.      |
| **Strengths to Preserve** | 10     | Above-baseline design choices. Touch only with explicit reason.               |
| **Total Items**           | **39** |                                                                               |

---

## 2. Sources Reviewed

| Category               | Files Read                                                                                                                                                                                                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Root governance**    | `AGENTS.md`                                                                                                                                                                                                                                                         |
| **Pipeline (company)** | `company/pipeline/mobile-development/pipeline.md`, `company/pipeline/web-development/pipeline.md` (structural confirmation pass), `company/pipeline/backend-api/pipeline.md`, `company/pipeline/full-stack/pipeline.md`, `company/pipeline/recruitment/pipeline.md` |
| **Pipeline (studio)**  | `studio/casual-games/pipeline/casual-games-pipeline.md`                                                                                                                                                                                                             |
| **Library overviews**  | `company/library/overview/company.md`, `company/library/overview/personnel.md`, `company/library/overview/pipeline.md`, `company/library/topics/architecture.md`, `company/library/departments/research-develop.md`                                                 |
| **READMEs**            | `company/departments/README.md`, `company/pipeline/README.md`, `company/library/README.md`                                                                                                                                                                          |
| **Studio charter**     | `studio/casual-games/library/overview/casual-games-studio.md`                                                                                                                                                                                                       |
| **Studio audit**       | `studio/casual-games/team/recruitment-plan/audit-reports/C-SUITE-VERIFICATION-FINAL.md`                                                                                                                                                                             |
| **Cross-cutting**      | `company/pipeline/buddy-system-assignments.md`                                                                                                                                                                                                                      |
| **Personnel profiles** | CTO (Nakamura), CPO (Tran-Yoshida), CSO (Chen), CHRO (Hartwell), Android Lead (Asante-Mensah), Test Lead (Oduya), Studio Director (Vogel), Creative Director (Ishimori), Gameplay Engineer #2 (Ryu Tanaka)                                                          |
| **Skill files**        | `prd-authorship.md`, `defect-triage-and-classification.md`, `mobile-security-architecture.md`, `android-implementation.md`                                                                                                                                          |

---

## 3. Strengths to Preserve (Do Not Refactor)

These are above industry baseline. Preserve them through any optimization.

| ID      | Strength                                                                       | Source                                                                    | Why It Matters                                                                                             |
| ------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| KEEP-01 | "Trim-to-pass" anti-pattern guard at Stage 8                                   | `company/library/overview/pipeline.md` §"Trim-to-Pass" Anti-Pattern Guard | The single most mature design choice in the repo. Most companies ship by removing things that fail review. |
| KEEP-02 | Defect severity model with explicit P2/P3 user authority                       | `defect-triage-and-classification.md`                                     | Cleaner than what most enterprises actually run. Right contract.                                           |
| KEEP-03 | Paired PRD + SRD travelling together                                           | `AGENTS.md` Non-Negotiable Rule #2                                        | Security-by-coupling, not security-by-bolt-on. Apple discipline.                                           |
| KEEP-04 | "Honest gaps" section in every personnel profile                               | All `agent/profile.md` files                                              | Forces realistic delegation. Better than typical internal bios.                                            |
| KEEP-05 | Studio separation from R&D for Casual Games                                    | `casual-games-studio.md` §2.5 (CHRO rationale)                            | Correct architectural call (race-car-through-DMV reasoning).                                               |
| KEEP-06 | House-of-brands architecture for studio                                        | `casual-games-studio.md` §2.3                                             | Insulates parent brand from likely-to-flop titles. Voodoo/Zynga lesson.                                    |
| KEEP-07 | MASVS Level 2+ as security floor                                               | `mobile-security-architecture.md` §Success Metrics                        | Externally benchmarked, not ad-hoc.                                                                        |
| KEEP-08 | Three-layer monitoring (`progress.md` + sessions + checkpoints)                | `AGENTS.md` §Monitoring & Recovery System                                 | Designed for _recovery_ (LLM context loss), not just observability.                                        |
| KEEP-09 | Platform Strategy Matrix (5 mutually-exclusive scenarios)                      | `company/pipeline/mobile-development/pipeline.md`                         | Forces an explicit choice instead of "we'll do everything everywhere."                                     |
| KEEP-10 | PRD template — JTBD framing, edge-case matrix, instrumentation, kill condition | `prd-authorship.md`                                                       | Best-in-class. Many top product companies have weaker PRD requirements.                                    |

---

## 4. Critical Findings (P0) — Fix Before Next Project Starts

These are systemic risks. Each row is auditable: severity → finding → root cause → recommended fix → owner → due date → audit status.

| ID         | Finding                                                                  | Root Cause                                                                                                                                                                                                         | Recommended Fix                                                                                                                                                                                                                                                                       | Owner             | Due Date | Status  | CEO Audit Notes |
| ---------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | -------- | ------- | --------------- |
| FIND-P0-01 | Pipeline is waterfall in agile clothing                                  | 10 sequential gates + Stage-3 technology lock + per-stage CEO approval foreclose 80% of the learning that happens during prototyping & code                                                                        | (1) Convert gates to **risk-tiered**: full-panel only for high-blast-radius decisions. (2) Make ADRs **versionable & supersedable**, not "locked." (3) Insert a **discovery iteration loop** between Stage 2 and Stage 3 where prototype findings update the PRD before architecture. | CTO + CPO         | Day 30   | Pending |                 |
| FIND-P0-02 | i18n placed at Stage 9 is structurally wrong                             | Putting localization at the second-to-last stage bakes in hardcoded layouts, date/number formats in business logic, currency assumptions in the data model, RTL violations in components                           | (1) Move i18n to **continuous concern from Stage 2 onward**: pseudo-localization in prototype, RTL/LTR validation in IDS, locale-aware components in code review. (2) Rename Stage 9 to **"Translation Production"** (linguists translating extracted strings only).                  | CTO-L + CTO       | Day 30   | Pending |                 |
| FIND-P0-03 | No discovery / problem-validation stage                                  | All four product pipelines start at "Requirements → PRD," assuming requirements are valid. Single largest source of catastrophic product failure is solving the wrong problem.                                     | Add **Stage 0 — Problem Validation** to mobile/web/backend/full-stack pipelines: customer-discovery (n≥5 interviews), quantitative demand signal, explicit kill criteria _before_ PRD work begins.                                                                                    | CPO               | Day 30   | Pending |                 |
| FIND-P0-04 | Recruitment elite gate vs. actual hires has a credibility gap            | `recruitment/pipeline.md` says "≥4 on at least 4 of 5 dimensions, no override." `buddy-system-assignments.md` shows 7 hires at 12/20 (3.0 average). Buddy system bolted on to compensate. Tier-drift in real time. | Choose: (a) **Tier the gates by level**: L1 IC = 12/20 + buddy; L2 = 15/20; L3 = 18/20 elite. OR (b) hold the elite floor at 16/20 and reject buddy-track hires. **Recommended: option (a)** — matches reality and keeps the elite gate honest for senior roles.                      | CHRO              | Day 30   | Pending |                 |
| FIND-P0-05 | C-Suite panel reviews at Stages 6, 8, and 10 are a structural bottleneck | Three separate stages convene the _full_ C-suite. With multiple in-flight projects, C-suite calendars become the bottleneck and gates devolve into rubber-stamps.                                                  | Convert Stages 6/8/10 from "convene the panel" to **"DRI signs off; panel reviews exceptions async within 24h."** Reserve full-panel for explicit escalation triggers (P0/P1 unresolved, scope >X% change, security exception).                                                       | CTO + CPO         | Day 30   | Pending |                 |
| FIND-P0-06 | No incident response or post-launch operating model                      | Stage 10 (Release Readiness) is the last defined activity. No incident commander, no Sev1 protocol, no error budget, no rollback authority chain, no SOC, no customer/community ops.                               | Add **Stage 11 — Live Operations** to all parent pipelines (lift the casual-games Stage 10 pattern up). Define: Sev1/Sev2/Sev3 ladder, on-call rotation, blameless postmortem template, error budget per quarter, QBR cadence.                                                        | VP Platform + CSO | Day 60   | Pending |                 |

---

## 5. Important Findings (P1) — Fix in the Next Quarter

| ID         | Finding                                                                | Root Cause                                                                                                                                                                                              | Recommended Fix                                                                                                                                                                                                                                                | Owner                    | Due Date | Status  | CEO Audit Notes |
| ---------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | -------- | ------- | --------------- |
| FIND-P1-01 | No experimentation / A/B testing framework                             | PRD defines metrics with baselines and targets; pipeline has no infra to _measure_ them. Staged rollout (10/50/100) is not an A/B test.                                                                 | Add **Experimentation Spec** as a Stage 1 paired artifact alongside PRD/SRD; define statistical guardrails, MDE, sample-size calculation.                                                                                                                      | CPO + (new) Head of Data | Day 60   | Pending |                 |
| FIND-P1-02 | No data engineering / analytics platform owner                         | PRDs require event instrumentation; SRDs require audit logging; casual-games studio plans 10–100× event volume. No one owns the data platform. CIO covers infra strategy but not data.                  | Define & hire **VP Data / Head of Analytics**. Without it, no PRD's metric is enforceable. Add a "metric definition lock" gate parallel to the technology lock.                                                                                                | CHRO + CPO               | Day 60   | Pending |                 |
| FIND-P1-03 | Stage-based code review is a release-train relic                       | Stage 6 batches all code review. Massive batch sizes, late discovery of architectural drift, reviewer fatigue, long feedback loops.                                                                     | Rename Stage 6 to **"Architecture & Cross-Functional Conformance Review."** Per-PR code review remains continuous (CI-enforced, two-reviewer minimum, `CODEOWNERS`). Stage gate verifies _aggregate_ conformance, not lines.                                   | CTO + Software Architect | Day 60   | Pending |                 |
| FIND-P1-04 | No performance, accessibility, or privacy gates as P0 release blockers | Security is correctly P0 (encryption, MASVS). Performance/accessibility/privacy are not, despite living in skill files.                                                                                 | Add three rows to Stage 10 release checklist as P0 sign-offs: (1) Performance budget (TTI, app startup, frame budget) — CTO + Platform Lead. (2) Accessibility WCAG 2.1 AA — CDO. (3) Privacy / data minimization — CSO + GC.                                  | CTO + CDO + CSO          | Day 60   | Pending |                 |
| FIND-P1-05 | No "dogfood" stage                                                     | Pipeline jumps from automated test → integrity → release. Pure automation has never been sufficient because real users don't behave like test scripts.                                                  | Insert **Stage 9.5 — Internal Dogfood (5 business days minimum)** between integrity verification and i18n. Mandatory employee Beta channel; bug telemetry mandatory.                                                                                           | VP Quality               | Day 90   | Pending |                 |
| FIND-P1-06 | Game studio Day-1 retention thresholds too aggressive                  | Strategic brief sets D1 ≥ 40%, D7 ≥ 15%, D30 ≥ 8% as kill criteria. For pure-casual these are aggressive (King's Candy Crush averages D1 ~30%). Above-market thresholds will kill viable games.         | Calibrate thresholds to genre benchmarks: Hybrid-casual D1≥35%, D7≥12%, D30≥5%. Mid-core puzzle D1≥40%, D7≥18%, D30≥8%. Document genre lookup in strategic brief.                                                                                              | Studio Director + CPO    | Day 60   | Pending |                 |
| FIND-P1-07 | No promotion / leveling rubric                                         | Buddy system takes 12/20 L1 to "buddy ends" at Day 90 with no defined L1→L2→L3 path. Buddy _is_ the entire career system.                                                                               | Add **leveling rubric (L1–L5)** per role family: explicit expectations, calibration cadence (semi-annual), promotion criteria. Stripe/Google publish theirs internally — adapt.                                                                                | CHRO                     | Day 60   | Pending |                 |
| FIND-P1-08 | Multi-condition C-Suite verification reports are audit theater         | Studio's "All 24 conditions satisfied" report — 24 created and closed by the same parties. No external check that the 24 were the _right_ 24, no red-team adversarial review, no "what's missing" pass. | Add an **Independent Challenge round** to all multi-condition gate reports — designated devil's-advocate (CHRO-recruited external advisor or dedicated agent persona) whose only job is to attack the list before sign-off. Bezos's "red team review" pattern. | CTO                      | Day 90   | Pending |                 |

---

## 6. Polish Findings (P2) — Fix Opportunistically

| ID         | Finding                                                                              | Recommendation                                                                                                                                                                    | Owner               | Status  | CEO Audit Notes |
| ---------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------- | --------------- |
| FIND-P2-01 | No CFO, GC, COO, CMO in the C-suite                                                  | Either explicitly scope as "engineering company" in `AGENTS.md`, or add the missing functions. Studio has $1.1M cap with no finance owner.                                        | CHRO                | Pending |                 |
| FIND-P2-02 | No retrospective / postmortem cadence                                                | Add recurring artifact at end of Stage 10 and after every Sev1: blameless postmortem with action items bound to owners + dates.                                                   | CTO                 | Pending |                 |
| FIND-P2-03 | No 1-on-1 / OKR / performance review cadence visible                                 | Add to CHRO scope. For 70+ agent system the ongoing operating cadence cannot be implicit.                                                                                         | CHRO                | Pending |                 |
| FIND-P2-04 | `compensation-bands.md` and `role-family-templates/` referenced but not visible      | Either populate them or remove references. Phantom artifacts erode trust in the documentation.                                                                                    | CHRO                | Pending |                 |
| FIND-P2-05 | Rigid "X years at Y company" credentials in profiles                                 | Fine for role-play, but the rigidity sometimes constrains reasoning. Consider relaxing to "competency tier" rather than fixed company history.                                    | CHRO                | Pending |                 |
| FIND-P2-06 | Profiles repeat the same template across 70+ agents                                  | Risk: agents skim each other's profiles and ignore them. Compress to a single-page operating contract per role; move backstory to a separate file.                                | CHRO + Tech Writer  | Pending |                 |
| FIND-P2-07 | Four pipelines (mobile/web/backend/full-stack) are >90% duplicated content           | Refactor: one **base pipeline + deltas per product type**. Maintenance cost will explode if four parallel files are kept.                                                         | Software Architect  | Pending |                 |
| FIND-P2-08 | No technical debt allocation per sprint                                              | Add "20% capacity reserved for technical debt" rule to Stage 5 Implementation Plans. Without it, debt becomes invisible until it explodes.                                        | CTO                 | Pending |                 |
| FIND-P2-09 | No cost / ROI tracking per project                                                   | Even minimal "estimated cost / actual cost / cycle time" per project would expose which pipeline configurations are too heavy.                                                    | CTO + (new) Finance | Pending |                 |
| FIND-P2-10 | Recruitment pipeline (210K chars) is an order of magnitude longer than dev pipelines | Smell — the _meta_ (hiring) is more elaborate than the _object_ (building products). Compress.                                                                                    | CHRO                | Pending |                 |
| FIND-P2-11 | "AI-simulated panels replace human assessors" for technical interviews               | At Google/Stripe-tier the _signal is the human_. Document this as an explicit deviation and accept false-positive risk, or reintroduce human calibration.                         | CHRO                | Pending |                 |
| FIND-P2-12 | No defined rollback authority                                                        | Who can roll back without convening C-suite? Define on-call DRI's authority explicitly.                                                                                           | VP Platform + CTO   | Pending |                 |
| FIND-P2-13 | "Stage 7 Regression Mandate" requires 100% pass rate                                 | Real test suites have flaky tests; 100% is aspirational. Define the _flakiness budget_ (e.g., <2% non-deterministic with auto-quarantine).                                        | Test Lead           | Pending |                 |
| FIND-P2-14 | Studio uses PlayFab; exit plan mentioned but not concretized                         | Add an annual **"vendor-exit drill"** — actually export and re-import the data once a year to validate the exit plan works.                                                       | CIO                 | Pending |                 |
| FIND-P2-15 | `LINGMA.md` / `CLAUDE.md` / `QWEN.md` / `GEMINI.md` proliferation                    | Five platform-specific copies of the same operational doc is unmaintainable. Treat platform files as **adapters that import canonical AGENTS.md**, not parallel sources of truth. | CTO + Tech Writer   | Pending |                 |

---

## 7. 30 / 60 / 90-Day Execution Plan

### 7.0 Implementation Status Legend

Each step in §§7.1–7.3 carries an emoji status indicator for CEO quick-scan review. The vocabulary below is the authoritative implementation lifecycle per §12.3 and applies to every row in §§7.1–7.3.

| Emoji | Status          | Meaning                                                                                                                                                                             |
| ----- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ⬜    | **Pending**     | Approved by CEO but not yet started. Default state after sign-off.                                                                                                                  |
| 🟡    | **In Progress** | DRI has formally begun remediation work on the step; output artifact is being produced.                                                                                             |
| 🔵    | **Implemented** | Output artifact(s) produced and committed; awaiting independent verification.                                                                                                       |
| 🟢    | **Verified**    | Independent Challenge / red-team review (the pattern introduced by FIND-P1-08) has verified the step against its success criteria and against §10 Success Metrics where applicable. |
| ✅    | **Closed**      | Success metric measured; step-level retrospective complete; step is formally done and may no longer be modified.                                                                    |

> **CEO scan-guide.** Rows still ⬜ at their milestone boundary (Day 30 / 60 / 90) indicate schedule risk and warrant a CTO escalation. Rows stuck at 🟡 past their due date warrant a DRI status check. Rows at 🔵 for more than two weeks should trigger the Independent Challenge round to move them to 🟢.

### 7.1 Days 0–30 — Stop the Bleeding

| Step | Status | Action                                                                                    | Linked Findings        | Owner              | Output Artifact                                                              |
| ---- | ------ | ----------------------------------------------------------------------------------------- | ---------------------- | ------------------ | ---------------------------------------------------------------------------- |
| 1    | ⬜     | Reconcile recruitment-vs-buddy contradiction (tier the elite gate by level OR hold floor) | FIND-P0-04             | CHRO               | Updated `pipeline/recruitment/pipeline.md` + new `leveling-rubric.md` (stub) |
| 2    | ⬜     | Move i18n from Stage 9 to a cross-cutting concern across all four pipelines               | FIND-P0-02             | CTO-L + CTO        | All pipeline files updated; Stage 9 renamed to "Translation Production"      |
| 3    | ⬜     | Add Stage 0 — Problem Validation to mobile/web/backend/full-stack                         | FIND-P0-03             | CPO                | Four updated pipeline files; Stage 0 template                                |
| 4    | ⬜     | Convert Stages 6/8/10 from "panel convenes" → "DRI signs off, panel async"                | FIND-P0-05             | CTO + CPO          | Updated pipeline files; escalation trigger spec                              |
| 5    | ⬜     | Refactor four parallel pipelines into one base + deltas                                   | FIND-P0-01, FIND-P2-07 | Software Architect | New `pipeline/_base/` + thin overlays per product type                       |

### 7.2 Days 30–60 — Build What's Structurally Missing

| Step | Status | Action                                                                                                                                     | Linked Findings | Owner                    | Output Artifact                                                                                                                       |
| ---- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------ | --------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| 6    | ⬜     | Define & add Stage 11 — Live Operations to all parent pipelines (lift studio pattern up)                                                   | FIND-P0-06      | VP Platform + CSO        | Stage 11 spec; error budget per quarter; QBR cadence                                                                                  |
| 7    | ⬜     | Hire / define VP Data / Head of Analytics role                                                                                             | FIND-P1-02      | CHRO + CPO               | New role profile; recruitment ticket                                                                                                  |
| 8    | ⬜     | Add three new release-checklist rows: performance / WCAG 2.1 AA / privacy                                                                  | FIND-P1-04      | CTO + CDO + CSO          | Updated Stage 10 release checklist                                                                                                    |
| 9    | ⬜     | Author leveling rubric (L1–L5) for every role family                                                                                       | FIND-P1-07      | CHRO                     | `leveling-rubric.md` per role family                                                                                                  |
| 10   | ⬜     | Define incident response model                                                                                                             | FIND-P0-06      | VP Platform + CSO        | `incident-response.md` (Sev ladder, on-call rotation, blameless postmortem template)                                                  |
| 11   | ⬜     | Calibrate game-studio retention thresholds to genre benchmarks                                                                             | FIND-P1-06      | Studio Director + CPO    | Updated `casual-games-studio.md`                                                                                                      |
| 12   | ⬜     | Author **Experimentation Spec** template as a Stage 1 paired artifact alongside PRD/SRD _(Blocked by Step 7)_                              | FIND-P1-01      | CPO + Head of Data       | New `experimentation-spec-template.md`; statistical guardrails / MDE / sample-size guidance; Stage 1 paired-artifact rule update      |
| 13   | ⬜     | Rename Stage 6 to **"Architecture & Cross-Functional Conformance Review"**; codify continuous PR review as the primary code-review surface | FIND-P1-03      | CTO + Software Architect | All four pipeline files updated; `CODEOWNERS` + 2-reviewer policy documented; Stage 6 gate criteria narrowed to aggregate conformance |

### 7.3 Days 60–90 — Mature the Operating System

| Step | Status | Action                                                                                             | Linked Findings | Owner              | Output Artifact                                                      |
| ---- | ------ | -------------------------------------------------------------------------------------------------- | --------------- | ------------------ | -------------------------------------------------------------------- |
| 14   | ⬜     | Replace "ADRs locked at Stage 3" with versionable + supersedable ADRs                              | FIND-P0-01      | Software Architect | New ADR template with `Supersedes:` field; rule update in pipeline   |
| 15   | ⬜     | Insert Stage 9.5 Dogfood into all parent pipelines                                                 | FIND-P1-05      | VP Quality         | Stage 9.5 spec; dogfood telemetry template                           |
| 16   | ⬜     | Add Independent Challenge round to every multi-condition gate report                               | FIND-P1-08      | CTO                | "Red team review" template; designated challenger persona            |
| 17   | ⬜     | Build project-level dashboard (PRDs in flight, stage of each project, cycle time, P0/P1 burn-down) | FIND-P2-09      | CTO + VP Platform  | `project/_dashboard.md` updated daily; could start as plain markdown |
| 18   | ⬜     | Compress recruitment pipeline (currently 210K chars)                                               | FIND-P2-10      | CHRO               | Pruned `pipeline/recruitment/pipeline.md`                            |
| 19   | ⬜     | Resolve `LINGMA.md` / `CLAUDE.md` / `QWEN.md` / `GEMINI.md` proliferation                          | FIND-P2-15      | CTO + Tech Writer  | Adapter pattern: platform files import canonical `AGENTS.md`         |

---

## 8. Optimization Topics — Detailed Tabular Breakdown

This section gives auditors a per-topic deep-dive so each optimization can be evaluated independently.

### 8.1 Topic — Pipeline Architecture

| Aspect         | Current State                                                 | Target State                                                                          | Gap                                 |
| -------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------- |
| Stage model    | 10 sequential, gated stages with full-panel reviews at 6/8/10 | 12 stages: Stage 0 (Discovery) + Stages 1–10 + Stage 11 (Live Ops); risk-tiered gates | Add 2 stages, retier gate authority |
| Decision lock  | ADRs locked at Stage 3, not revisable in Stage 4+             | ADRs versionable + supersedable, supersession requires rollback plan                  | Replace lock with discipline        |
| Feedback loops | One-way; no learning from prototype back into PRD             | Discovery iteration loop between Stage 2 and Stage 3                                  | Add the loop                        |
| Code review    | Stage-based batched review at Stage 6                         | Continuous per-PR review (CODEOWNERS, 2 reviewers); Stage 6 = aggregate conformance   | Rename + clarify the gate           |
| Concurrency    | Architecture gated AFTER design AFTER PRD                     | Concurrent with feedback loops + tracer-bullet architecture during PRD authoring      | Allow parallelism                   |

### 8.2 Topic — Internationalization Lifecycle

| Stage   | Current                                        | Target                                                                                          |
| ------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Stage 1 | (no i18n consideration)                        | i18n requirements declared in PRD; target locales locked                                        |
| Stage 2 | (no i18n consideration)                        | Pseudo-localization in prototype; RTL/LTR validation in IDS                                     |
| Stage 5 | Hardcoded strings developed; later extracted   | Locale-aware components from first commit; zero hardcoded strings rule enforced in CI           |
| Stage 7 | (no i18n test gate)                            | Locale-coverage tests; pseudo-locale screenshot regression                                      |
| Stage 9 | String extraction + translation + verification | **"Translation Production" only** — translation accuracy by linguists; engineering already done |

### 8.3 Topic — Defect Severity Model (Already Strong; Minor Tightening)

| Severity | Definition (current)                   | Action (current)   | Recommended Tightening                                                         |
| -------- | -------------------------------------- | ------------------ | ------------------------------------------------------------------------------ |
| P0       | Crash / data loss / security breach    | Non-negotiable fix | **Add:** WCAG 2.1 AA failure in regulated markets, perf-budget violation > 20% |
| P1       | Core feature broken / major UX failure | Non-negotiable fix | **Add:** Privacy/PII leak in logs                                              |
| P2       | Minor degradation / cosmetic           | User decides       | (no change)                                                                    |
| P3       | Polish / nice-to-have                  | User decides       | (no change)                                                                    |

### 8.4 Topic — Recruitment Gate Reconciliation

| Tier         | Vetting Score Floor (current claim)      | Vetting Score Floor (recommended)        | Buddy System? | Gate Authority    |
| ------------ | ---------------------------------------- | ---------------------------------------- | ------------- | ----------------- |
| L1 IC        | "≥4 on 4-of-5 dimensions" (i.e., ≥16/20) | **12/20** (3.0 avg, with required buddy) | Required 90d  | CHRO + Hiring Mgr |
| L2 IC        | (undefined)                              | **15/20**                                | Optional      | CHRO + Hiring Mgr |
| L3 IC        | (undefined)                              | **17/20**                                | None          | CHRO + Dept Head  |
| L4 / Lead    | (undefined)                              | **18/20** + Leadership ≥ 4               | None          | CHRO + C-Suite    |
| L5 / C-Suite | (undefined)                              | **19/20** elite + all dimensions ≥ 4     | None          | CEO + CHRO        |

### 8.5 Topic — Release Readiness Checklist (Recommended Final Form)

| #   | Domain                                                                 | Sign-off Authority | Status                  |
| --- | ---------------------------------------------------------------------- | ------------------ | ----------------------- |
| 1   | Product — all PRD requirements implemented                             | CPO + relevant VP  | ✅ exists               |
| 2   | Design — all CDO/IDS specifications realised                           | CDO                | ✅ exists               |
| 3   | Architecture — all UML/ADR/TSD standards upheld                        | CTO + CIO          | ✅ exists               |
| 4   | Security — SRD enforced, OWASP MASVS compliant                         | CSO                | ✅ exists               |
| 5   | Testing — 100% automated test pass rate (with flakiness budget)        | CTO + Test Lead    | ✅ exists (tightened)   |
| 6   | Localisation — all target languages complete                           | CTO-L              | ✅ exists               |
| 7   | Platform — App Store / Google Play requirements met                    | CTO + CPO          | ✅ exists               |
| 8   | **Performance — TTI / startup / frame budget met**                     | CTO + VP Platform  | ⬛ **NEW (FIND-P1-04)** |
| 9   | **Accessibility — WCAG 2.1 AA verified, no Level-AA failures**         | CDO                | ⬛ **NEW (FIND-P1-04)** |
| 10  | **Privacy — data minimization, no PII in logs, consent flows correct** | CSO + (future) GC  | ⬛ **NEW (FIND-P1-04)** |
| 11  | **Dogfood — Stage 9.5 internal beta complete, no Sev1 telemetry**      | VP Quality         | ⬛ **NEW (FIND-P1-05)** |
| 12  | **Live Ops Readiness — Sev ladder + on-call + error budget defined**   | VP Platform + CSO  | ⬛ **NEW (FIND-P0-06)** |

### 8.6 Topic — Studio (Casual Games) Specific Optimizations

| Area                            | Current                                 | Recommended                                                                           |
| ------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------- |
| Retention kill thresholds       | D1≥40%, D7≥15%, D30≥8% (genre-blind)    | Genre-calibrated table (hybrid-casual / mid-core / pure-casual)                       |
| Live ops content cadence        | "Continuous" (undefined cadence)        | Define explicit cadence: weekly events / 4-week sprints (Voodoo) / 8-week (Supercell) |
| C-Suite verification reports    | 24-condition closure by same parties    | Add Independent Challenge round (devil's-advocate persona)                            |
| PlayFab vendor exit             | Plan mentioned but not concretized      | Annual vendor-exit drill: actually export & re-import data to validate                |
| Game economy simulation tooling | Not present in skills                   | Add Excel/Python economy simulation skill to Game Designer / Producer roles           |
| Day-1 accessibility             | Listed in CDO assessment (well-defined) | Promote to P0 release blocker per FIND-P1-04                                          |

### 8.7 Topic — Documentation & Maintenance Hygiene

| Issue                                                             | Current Cost                    | Fix                                                         |
| ----------------------------------------------------------------- | ------------------------------- | ----------------------------------------------------------- |
| 4 parallel pipeline files (>90% duplicated)                       | 4× edit cost, drift risk        | Single base + deltas (FIND-P2-07)                           |
| 70+ agent profiles in identical templates                         | Skim/ignore risk                | 1-page operating contract + separate backstory (FIND-P2-06) |
| `LINGMA.md` / `CLAUDE.md` / `QWEN.md` / `GEMINI.md` proliferation | 5× maintenance for same content | Adapter pattern (FIND-P2-15)                                |
| Phantom artifacts (`compensation-bands.md`)                       | Trust erosion                   | Populate or remove references (FIND-P2-04)                  |
| 210K-char recruitment pipeline                                    | Exceeds reasonable read time    | Compress (FIND-P2-10)                                       |

---

## 9. Risk Register — What Could Go Wrong With This Optimization

| Risk ID | Risk                                                                         | Likelihood | Impact | Mitigation                                                                                      |
| ------- | ---------------------------------------------------------------------------- | ---------- | ------ | ----------------------------------------------------------------------------------------------- |
| OPT-R1  | Stakeholders interpret "convert C-suite panel to async" as "lose oversight"  | Medium     | High   | Explicit escalation triggers; published audit log of all DRI decisions                          |
| OPT-R2  | Tiering the recruitment gate is read as "lowering the bar"                   | High       | Medium | Frame as "matching reality"; show the elite floor remains intact for L3+                        |
| OPT-R3  | i18n refactor introduces regressions in existing artifacts                   | Medium     | Medium | Phase the refactor; keep Stage 9 alive in parallel until pseudo-localization adopted            |
| OPT-R4  | Pipeline base + deltas refactor breaks references in existing project files  | High       | Low    | Maintain backward-compatible filenames as redirects for one quarter                             |
| OPT-R5  | Adding Stage 0 + Stage 11 increases perceived process weight                 | Low        | Medium | Stage 0 lightweight (1-page validation memo); Stage 11 incremental (start with Sev ladder only) |
| OPT-R6  | New roles (VP Data, GC, future CFO) compete with existing recruitment budget | Medium     | Medium | Sequence: VP Data first (highest leverage); others tied to revenue inflection                   |
| OPT-R7  | Independent Challenge round adds gate latency                                | Medium     | Low    | Time-box challenge to 48 hours; default approve if no objection                                 |
| OPT-R8  | This optimization plan itself becomes "audit theater"                        | Medium     | High   | CEO sign-off + quarterly review + concrete action-bound owners with due dates                   |

---

## 10. Success Metrics — How We'll Know This Worked

| Metric                                              | Baseline (today)                  | Target (90 days)                      | Owner             |
| --------------------------------------------------- | --------------------------------- | ------------------------------------- | ----------------- |
| Cycle time per pipeline stage                       | Not measured                      | Measured + visible in dashboard       | CTO + Tech PM     |
| Stage gate approval latency                         | Bottlenecked on C-suite calendars | DRI sign-off median ≤ 24h             | CTO + CPO         |
| i18n-related rework after Stage 9                   | Unknown (likely high)             | < 5% of total post-Stage-7 defects    | CTO-L             |
| % of new hires meeting tiered gate floor            | ~70% (with buddy compensation)    | 100% at appropriate tier              | CHRO              |
| Number of Sev1 incidents handled with no IC defined | All of them                       | 0                                     | VP Platform + CSO |
| Project-level dashboard freshness                   | Not existent                      | Updated daily                         | CTO + Tech PM     |
| Multi-condition gate reports with red-team round    | 0%                                | 100% for any gate with ≥ 5 conditions | CTO               |

---

## 11. Out of Scope (Explicitly Deferred)

| Item                                                          | Reason for Deferral                                                  | Revisit Date |
| ------------------------------------------------------------- | -------------------------------------------------------------------- | ------------ |
| Adding CFO / GC / COO / CMO C-suite roles                     | Requires CEO scope decision: engineering company vs. full enterprise | Day 90       |
| Migrating off PlayFab to self-hosted backend (studio)         | Vendor-exit drill is sufficient mitigation for now                   | FY2027 Q1    |
| Replacing AI-simulated panels with human interviewers         | Document deviation explicitly; revisit once tier-drift causes pain   | Day 180      |
| Building a real-time experimentation platform (vs. spec-only) | Requires VP Data role to be filled first                             | Day 180      |
| Internationalization beyond ZH/EN/JA/KO/FR                    | Not requested by current product portfolio                           | On demand    |

---

## 12. Audit & Sign-off Block

### 12.1 Audit Log

| Date       | Auditor          | Section Reviewed                                                                      | Decision (Accept / Modify / Reject) | Notes / Modifications                                                                                                                                                                                                         |
| ---------- | ---------------- | ------------------------------------------------------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-20 | Peter Chen (CEO) | Full document (§§1–14) — all findings, execution plan, risk register, success metrics | **Accept (Approve as-is)**          | All 29 findings approved without modification. Plan becomes binding effective 2026-04-20. DRIs in §§4–6 may begin Days 0–30 actions immediately. Quarterly review cadence confirmed; first checkpoint at Day 90 (2026-07-20). |
|            |                  |                                                                                       |                                     |                                                                                                                                                                                                                               |
|            |                  |                                                                                       |                                     |                                                                                                                                                                                                                               |

### 12.2 CEO Sign-off

| Field             | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reviewed by       | **Peter Chen, CEO**                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Review date       | **2026-04-20**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Decision          | ☑ **Approve as-is** &nbsp; ☐ Approve with modifications &nbsp; ☐ Defer &nbsp; ☐ Reject                                                                                                                                                                                                                                                                                                                                                                                                          |
| Modifications     | None — approved without modification.                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Approved findings | **All 29 findings (6 P0 + 8 P1 + 15 P2):** FIND-P0-01, FIND-P0-02, FIND-P0-03, FIND-P0-04, FIND-P0-05, FIND-P0-06, FIND-P1-01, FIND-P1-02, FIND-P1-03, FIND-P1-04, FIND-P1-05, FIND-P1-06, FIND-P1-07, FIND-P1-08, FIND-P2-01, FIND-P2-02, FIND-P2-03, FIND-P2-04, FIND-P2-05, FIND-P2-06, FIND-P2-07, FIND-P2-08, FIND-P2-09, FIND-P2-10, FIND-P2-11, FIND-P2-12, FIND-P2-13, FIND-P2-14, FIND-P2-15. The 10 strengths in §3 (KEEP-01 through KEEP-10) are likewise affirmed for preservation. |
| Rejected findings | None.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Effective date    | **2026-04-20** — all approved findings binding from this date. Days 0–30 actions in §7.1 begin immediately; Days 30–60 actions in §7.2 begin 2026-05-20; Days 60–90 actions in §7.3 begin 2026-06-19; Day 90 quarterly review checkpoint at 2026-07-19.                                                                                                                                                                                                                                         |

### 12.3 Implementation Tracking

Once approved, each finding ID (and each §7 execution-plan step) transitions through:

`⬜ Pending → 🟡 In Progress → 🔵 Implemented → 🟢 Verified → ✅ Closed`

Status changes are logged in the **Status** column of Sections 4, 5, and 6 (text form — e.g., "In Progress") and Section 7 (emoji form, per the §7.0 Implementation Status Legend), with a dated entry in the **CEO Audit Notes** column. The emoji and text forms are equivalent and refer to the same lifecycle state; §7.0 is the authoritative legend.

---

## 13. Document Version History

| Version | Date           | Author           | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------- | -------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 20, 2026 | Operating Review | Initial optimization plan based on full company + studio review                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 1.1     | April 20, 2026 | Operating Review | Pre-audit double-review pass: status field set to "Awaiting Audit"; FIND-P1-01 and FIND-P1-03 added to 30/60/90 execution plan as Steps 12–13 (subsequent steps renumbered 14–19); §12.2 sign-off placeholders cleaned; §14 source paths normalized to workspace-root with `web-development/pipeline.md` added; §8.2 typo fix; §2 expanded to disclose web-development structural confirmation pass. No findings added or removed; counts unchanged at 6 P0 / 8 P1 / 15 P2 / 10 KEEP.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 1.2     | April 20, 2026 | Operating Review | **CEO sign-off applied.** Status changed from "Awaiting Audit" to "Approved by CEO Peter Chen — Effective April 20, 2026." §12.1 Audit Log entry added recording Peter Chen's accept-as-is decision. §12.2 CEO Sign-off block populated: reviewer, date, decision, all 29 finding IDs listed as approved, 0 rejected, effective date 2026-04-20, with phased start dates for Days 0–30 / 30–60 / 60–90 actions and Day 90 quarterly checkpoint (2026-07-19). Audience field updated from "User (CEO)" to "CEO Peter Chen." Next Review field tightened to point at concrete Day 90 checkpoint date. Closing line updated from "awaiting CEO audit and sign-off" to "approved and binding." No substantive findings, owners, or recommendations changed; counts unchanged at 6 P0 / 8 P1 / 15 P2 / 10 KEEP. Per §12.3, all finding IDs remain at status `Pending` until DRIs commence implementation; subsequent transitions (`In Progress → Implemented → Verified → Closed`) will be logged in §§4–6 Status columns with dated CEO Audit Notes entries.                                              |
| 1.3     | April 20, 2026 | Operating Review | **CEO-access enhancement — audit surface only; no remediation work started.** Added §7.0 Implementation Status Legend defining a 5-state emoji vocabulary (⬜ Pending → 🟡 In Progress → 🔵 Implemented → 🟢 Verified → ✅ Closed) and a CEO scan-guide for milestone-boundary schedule-risk detection. Added a new "Status" column (second column, after Step #) to all three §7 execution-plan sub-tables (§7.1 Days 0–30, §7.2 Days 30–60, §7.3 Days 60–90); every one of the 19 steps is initialized to ⬜ Pending pending CEO go-ahead to begin remediation. §12.3 Implementation Tracking updated to reference the §7.0 emoji legend and confirm emoji-form/text-form equivalence across §§4–6 and §7. Plan formatted with Prettier 3.8.3 (default settings); `prettier --check` passes. **Unchanged by this version:** zero findings added, removed, or modified; zero owners, due dates, artifacts, success criteria, or risk-register entries changed; plan-level status remains "Approved by CEO Peter Chen — Effective April 20, 2026"; counts unchanged at 6 P0 / 8 P1 / 15 P2 / 10 KEEP. |
| 1.4     | April 20, 2026 | Operating Review | **Administrative Clean-up (Track A) completed.** Resolved the 5 double-review (DR) items identified in v1.3. Synced `company/optimization-history/README.md` to reflect 'Approved' status (DR-01). Corrected Day 90 date math across document to July 19, 2026 (DR-02). Clarified the outputs of Step 6 vs. Step 10 by removing overlap (DR-03) and annotated Step 12 as blocked by Step 7 (DR-04). Disambiguated roles by replacing phantom 'Platform Lead' and 'Tech PM' titles with the existing 'VP Platform' role (DR-05). Execution block is now clean and ready to transition to `🟡 In Progress` upon CEO go-ahead.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

---

## 14. Appendix — Recommendation Traceability Matrix

For auditor convenience: every finding maps to its source observation and source artifact.

| Finding ID | Source Observation                                                   | Source Artifact (paths relative to workspace root)                                                                                     |
| ---------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| FIND-P0-01 | "Technology decisions lock at Stage 3" + 10 sequential gates         | `AGENTS.md` Non-Negotiable Rule #3; `company/pipeline/mobile-development/pipeline.md`                                                  |
| FIND-P0-02 | i18n placed at Stage 9 (second-to-last)                              | `company/library/overview/pipeline.md` Stage 9                                                                                         |
| FIND-P0-03 | Pipeline starts at "Requirements → PRD"                              | `company/pipeline/{mobile-development,web-development,backend-api,full-stack}/pipeline.md` (all start at Stage 1 Requirements)         |
| FIND-P0-04 | 7 hires at 12/20 + buddy system contradicts "no override" elite gate | `company/pipeline/buddy-system-assignments.md` + `company/pipeline/recruitment/pipeline.md`                                            |
| FIND-P0-05 | Stages 6, 8, 10 require full-panel C-suite convening                 | `company/library/overview/pipeline.md` Stage Owner Index                                                                               |
| FIND-P0-06 | Stage 10 is the last defined activity; no incident response model    | `company/pipeline/{mobile-development,web-development,backend-api,full-stack}/pipeline.md` (all end at Stage 10)                       |
| FIND-P1-01 | PRD defines metrics; pipeline has no experimentation infra           | `company/departments/product-management/supervisor/chief-product-officer/skills/prd-authorship.md` §9 Launch Sequencing                |
| FIND-P1-02 | No data platform owner; CIO covers infra strategy only               | `company/library/overview/personnel.md`                                                                                                |
| FIND-P1-03 | Stage 6 batches all code review                                      | `company/library/overview/pipeline.md` Stage 6 Code Review Criteria                                                                    |
| FIND-P1-04 | Security is P0; performance/accessibility/privacy are not            | `company/library/overview/pipeline.md` §Release Checklist                                                                              |
| FIND-P1-05 | Pipeline jumps from automated test → integrity → release             | `company/library/overview/pipeline.md` Stages 7 → 8 → 10                                                                               |
| FIND-P1-06 | D1≥40%, D7≥15%, D30≥8% (genre-blind kill thresholds)                 | `studio/casual-games/library/overview/casual-games-studio.md` §2.1                                                                     |
| FIND-P1-07 | Buddy system has no L1→L2→L3 path beyond Day 90                      | `company/pipeline/buddy-system-assignments.md` §Checkpoint Format                                                                      |
| FIND-P1-08 | "All 24 conditions satisfied" closed by same parties                 | `studio/casual-games/team/recruitment-plan/audit-reports/C-SUITE-VERIFICATION-FINAL.md`                                                |
| FIND-P2-01 | C-suite missing CFO / GC / COO / CMO                                 | `AGENTS.md` Quick Roster + `company/library/overview/personnel.md`                                                                     |
| FIND-P2-02 | No postmortem cadence in any pipeline                                | `company/pipeline/{mobile-development,web-development,backend-api,full-stack,recruitment}/pipeline.md`                                 |
| FIND-P2-03 | No 1-on-1 / OKR / performance review cadence                         | `company/departments/human-resources/` directory                                                                                       |
| FIND-P2-04 | `compensation-bands.md` referenced but not visible                   | `company/pipeline/recruitment/pipeline.md` §Configuration Artifacts                                                                    |
| FIND-P2-05 | "X years at Y company" rigid credentials                             | All `company/departments/**/agent/profile.md` files                                                                                    |
| FIND-P2-06 | 70+ profiles in same template                                        | `company/departments/` tree                                                                                                            |
| FIND-P2-07 | Four pipelines >90% duplicated                                       | `company/pipeline/{mobile-development,web-development,backend-api,full-stack}/pipeline.md` (recruitment differs in shape)              |
| FIND-P2-08 | No technical debt allocation rule                                    | All Stage 5 implementation-plan sections in `company/pipeline/{mobile-development,web-development,backend-api,full-stack}/pipeline.md` |
| FIND-P2-09 | No cost / ROI tracking per project                                   | `company/project/` directory                                                                                                           |
| FIND-P2-10 | Recruitment pipeline at 210K characters                              | `company/pipeline/recruitment/pipeline.md`                                                                                             |
| FIND-P2-11 | "AI-simulated panels replace human assessors"                        | `company/pipeline/recruitment/pipeline.md` §Internal User Access Matrix                                                                |
| FIND-P2-12 | No defined rollback authority                                        | `company/pipeline/{mobile-development,web-development,backend-api,full-stack}/pipeline.md` Stage 10 sections                           |
| FIND-P2-13 | "100% pass rate" with no flakiness budget                            | `company/library/overview/pipeline.md` §Stage 7 Regression Testing Mandate                                                             |
| FIND-P2-14 | PlayFab exit plan not concretized                                    | `studio/casual-games/library/overview/casual-games-studio.md` §2.4                                                                     |
| FIND-P2-15 | Multiple platform-specific docs                                      | `AGENTS.md` §Documentation Strategy + sibling root files (`CLAUDE.md`, `LINGMA.md`, `QWEN.md`, `GEMINI.md` if present)                 |

---

_End of Optimization Plan OPT-2026-04-20-001 — **approved by CEO Peter Chen on April 20, 2026 and binding from that date** (see §12.2 for sign-off block, §12.1 for audit log entry, §13 for v1.2 change history)._
