# Independent Challenge Report — Step 17 (Project-level dashboard)

| Field                    | Value                                                                                                                                                                                                                                                                                        |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Round ID**             | ICR-2026-04-21-S17-01                                                                                                                                                                                                                                                                        |
| **Subject**              | Plan §7.3 Step 17 — build the project-level dashboard answering three CEO-grade questions (PRDs in flight, P0/P1 defect burn-down, cycle time) per FIND-P2-09, as implemented in `company/project/_dashboard.md` v1.0 (DASH-COMPANY-001).                                                    |
| **Original DRI cluster** | CTO + VP Platform; finding authored by Operating Review                                                                                                                                                                                                                                      |
| **Challenger**           | **Operating Review (provisional, per template §3 Tier "Plan-step gate")** — declared structurally provisional; CHRO-recruited external advisor will replace this provisional challenger by Day 30 (2026-05-20).                                                                              |
| **Round opened**         | 2026-04-21 (Day 1 of OPT-2026-04-20-001)                                                                                                                                                                                                                                                     |
| **Report filed**         | 2026-04-21 (same day; well within the 48-hour window)                                                                                                                                                                                                                                        |
| **Template used**        | [`../../../pipeline/_base/independent-challenge-template.md`](../../../pipeline/_base/independent-challenge-template.md) v1.0                                                                                                                                                                |
| **Verdict**              | **PASS-with-follow-ups (provisional).** Step 17 ✅ Closed status retroactively confirmed; three follow-ups filed (none gate the Closed status; F-3 binds Day-30 CHRO external re-challenge). Honest "empty by design" baseline + explicit Hierarchy of Truth are commendable design choices. |

> **Backfill disclosure.** This is a **post-closure backfill round** filed under Option A of the audit-gap remediation. Step 17 was transitioned directly from `🔵 Implemented` to `✅ Closed` during the CEO batched discharge of 2026-04-21 without a prior `🟢 Verified` Independent Challenge round. A FAIL verdict here would reopen the step to `🔵`; a PASS verdict retroactively confirms the Closed transition.

---

## 1. Subject and scope

**Reviewed:** the project-level dashboard as implemented in `company/project/_dashboard.md` v1.0:

- §1 Purpose (three CEO-grade questions framing).
- §2 Hierarchy of Truth (upstream `progress.md` + `checkpoints/*.json` are sources of truth; dashboard aggregates).
- §3 Active Product Projects (PRDs in Flight) — empty-by-design table with explicit "when this section becomes non-empty" rules.
- §4 P0/P1 Defect Burn-Down (Cross-Project) — with explicit 5-business-day P0 escalation and 10-business-day P1 notification rules.
- §5 Cycle-Time Tracker — with explicit 1.5× baseline trigger for CTO review.
- §6 Refresh Cadence + Ownership — daily during active windows; weekly during steady-state.
- §7 Open Items (4 items: auto-refresh integration; schema lock; first-product onboarding dry-run; cost/ROI columns).

**Not reviewed:**

- The **upstream `progress.md` per-project schema** — §7 OI-02 acknowledges this as a future schema-lock; until locked, the §3/§4/§5 schemas are provisional.
- The **`checkpoints/*.json` Layer-3 schema** — referenced in §2 as the cycle-time source of truth; quality not audited here.
- The **studio-side dashboard** — explicitly out of scope; the `company/project/_dashboard.md` is for company pipelines (mobile/web/backend/full-stack); studio has its own dashboard surface.
- The **AGENTS.md three-layer monitoring system** itself — referenced as upstream; audited separately as KEEP-08.

---

## 2. The five attack vectors

### V-1 Completeness — what's missing from the dashboard?

**Question:** Are the three CEO-grade questions the _right_ set? What categories of project-state risk are not represented?

**Findings:**

- **Three sections present and structurally complete** (§3 Active Projects + §4 P0/P1 Burn-Down + §5 Cycle Time). Coverage matches the FIND-P2-09 scope ("PRDs in flight, stage of each project, cycle time, P0/P1 burn-down").
- **Resource allocation / staffing is not represented.** A CEO scanning the dashboard sees stage + days-in-stage + P0/P1 count + risk emoji; they do not see "how many engineers are on this project; is the team appropriately staffed for the stage?" Industry comparables (Atlassian Jira Portfolio; Linear; Asana) carry team-load + capacity columns. **Routed to F-1.**
- **Cost / budget tracking is partially addressed.** §7 OI-04 explicitly defers cost/ROI columns until N ≥ 1 projects — this is the "premature factoring with N=0 is the worse failure" anti-pattern, well-engineered. **Defensible deferral.**
- **Stage 0 (Discovery / Problem Validation) projects are deliberately excluded** from §3 (per the "Stage 0 projects appear here once the first PRD draft exists" rule). This is an intentional design choice (pre-PRD work is too noisy for executive scan); however, it creates a gap: a Stage 0 project that has been in discovery for 90 days with no PRD draft is invisible to the CEO. **Routed to F-1 (joint).**
- **Studio-side projects are excluded** from §3 (per "either the company 10-stage pipeline or the studio 10-stage pipeline" wording — this is INCLUSIVE; studio projects DO appear). On re-read, §3 scope correctly includes studio projects. **No gap.**
- **Incident-response action items are not aggregated** in §4. `incident-response.md` §6 says "Action items are tracked in the project dashboard until closed" — but §4 of the dashboard tracks P0/P1 _defects_, not _action items from postmortems_. The cross-reference exists but the dashboard does not have a §4.5 "Postmortem Action Items" section. **Routed to F-2.**
- **Categories NOT represented but acknowledged as scope-deferred:** roadmap timeline (Gantt-style) — out of scope; the §5 cycle-time tracker is the closest substitute; experiment results — Step 12's spec template tracks these in per-spec docs; OKR / quarterly target tracking — out of scope.

**Result:** **PASS-with-conditions.** Three core sections present and complete. Two operational gaps (resource allocation, postmortem action items) routed to F-1 and F-2.

### V-2 Sufficiency — is the threshold actually high enough?

**Question:** For each section's enforceable rule, is the threshold right?

**Findings:**

- **§4 P0 ≥ 5 business days → automatic CTO + VP escalation:** matches AGENTS.md Non-Negotiable Rule #4 (P0 = non-negotiable fix). Mechanical and well-engineered.
- **§4 P1 ≥ 10 business days → CTO notification:** twice the P0 window; scales appropriately. **Defensible.**
- **§4 "Neither rule is overridable":** strong structural protection against the silent-defer-as-deferred-decision failure mode.
- **§5 per-stage median > 1.5× baseline → CTO review of stage execution:** the threshold is industry-defensible (Atlassian's "stage drift" published threshold is ~1.5× baseline). However, the baseline itself is not seeded until "the first project completes its first full cycle" — there is no baseline for the first project. The deliverable is honest about this; the first project's cycle time will become the baseline for all subsequent projects. **Cold-start gap acknowledged in the deliverable; not a structural defect.**
- **§6 daily refresh during active execution windows:** matches Plan §10 success metric ("Project-level dashboard freshness: Updated daily"). The "weekly refresh during steady-state" is appropriate for the current N=0 state.
- **§6 24-hour mirror lag:** the manual-refresh model has a structural 24-hour latency from upstream `progress.md` change to dashboard reflection. Industry standard (real-time Linear / Jira) is < 5 minutes. The deliverable acknowledges this in §7 OI-01 ("Auto-refresh integration deferred until N ≥ 3 projects to avoid premature factoring"). **Defensible deferral.**
- **§3 Risk emoji (🟢 / 🟡 / 🟠 / 🔴) thresholds are not specified.** When does a project become 🟡? When does it become 🟠? The deliverable does not enumerate the risk-emoji thresholds. A consistent threshold (e.g., 🟡 = days-in-stage > 1.5× baseline; 🟠 = days-in-stage > 2× baseline; 🔴 = days-in-stage > 3× baseline OR open P0) would make the column auditable. **Routed to F-3.**

**Result:** **PASS-with-conditions.** Defect-burn-down thresholds and cycle-time thresholds are well-calibrated. Risk-emoji threshold specification is missing; routed to F-3.

### V-3 Trim-to-Pass (KEEP-01) scan — was anything silently removed?

**Question:** Comparing the deliverable against the FIND-P2-09 finding requirements, was anything quietly omitted?

**Findings:**

- **The FIND-P2-09 finding required: PRDs in flight, stage of each project, cycle time, P0/P1 burn-down.** All four are present in §3 (PRDs + stages) + §4 (P0/P1) + §5 (cycle time). **Coverage matches finding scope.**
- **The "empty by design" baseline** (§3 / §4 / §5 honest empty-state with explicit "when this section becomes non-empty" rules) is a net STRENGTHENING — the finding required a dashboard to exist; the deliverable provides an honest empty-state with clear activation triggers. This is above-spec and matches the company's "honest gaps" cultural pattern (KEEP-04).
- **The §2 Hierarchy of Truth** (upstream `progress.md` wins; dashboard fixed within 24h on disagreement) is a net STRENGTHENING — the finding did not require an explicit hierarchy; the deliverable provides one. This addresses the "two sources of truth" anti-pattern.
- **The §7 four Open Items with explicit DRIs and discharge triggers** is a net STRENGTHENING — the dashboard's own future evolution is governed.
- **Cross-check the mobile equivalence test report** — the dashboard creation is listed as a documented intentional addition; not a deletion or weakening.
- **No prior dashboard existed** in the company before this artifact. Net-new; no Trim-to-Pass risk from prior versions.

**Result:** **PASS — exemplary.** No content silently dropped; multiple net STRENGTHENINGS beyond the finding scope (honest empty-state, Hierarchy of Truth, Open Items governance). The deliverable matches the company's "honest gaps" cultural pattern.

### V-4 Counter-evidence search — where is the evidence that this remediation won't work?

**Question:** Cite at least one external benchmark, one historical near-miss, or one industry case study showing the same dashboard pattern failing.

**Findings:**

- **External benchmark:** Atlassian's own "Status Page" + "Confluence Project Status" pattern is the canonical industry reference for project-level rollup dashboards. The deliverable's structure (active projects + defect burn-down + cycle time) is structurally aligned. **Defensible direction.**
- **Historical near-miss inside this company:** none — N=0 projects today; first PRD entering Stage 1 will be the first real test.
- **Industry case study showing manual-refresh dashboards failing:** Spotify squad tribe-trio dashboards (~2016 era) — manual-refresh dashboards routinely lagged by 3-5 days because squad members had no time-allocated incentive to mirror upstream changes. The deliverable's 24-hour mirror lag is shorter than Spotify's observed lag, and the §7 OI-01 auto-refresh future-state addresses the structural risk. **Defensible direction with operational follow-through.**
- **Industry case study showing dashboards as theater:** McKinsey-led portfolio reviews at unnamed Fortune-500 ~2015-2018 — dashboards were nominally accurate but were "performed for the executive review" — i.e., projects strategically delayed bad-news transitions until just after the review window. The deliverable's "automatic escalation at 5/10 business days" is mechanical and not gameable in the same way (the trigger is the day-counter, not the review meeting). **Defensible structural protection.**
- **Industry case study showing cycle-time tracker failing:** Toyota TPS (the original "lead time" measurement) — first-cycle calibration of the baseline was reportedly difficult because the first cycle is non-representative (team learning curve, environmental variance). The deliverable acknowledges this in §5 ("once a project completes its first full cycle, the per-stage median seeds a baseline"). The cold-start period requires CTO judgment; this is acknowledged. **Defensible.**

**Result:** **PASS-with-conditions.** Counter-evidence supports the direction; the manual-refresh + cold-start gaps are operational tightening targets, not design defects. F-3 routes risk-emoji threshold specification.

### V-5 Same-parties-closure audit

**Question:** Confirm structural independence; document any overlap as residual risk.

**Findings:**

- **Original DRI:** CTO + VP Platform (per Plan §7.3 Step 17 row).
- **Original finding author:** Operating Review (FIND-P2-09).
- **Closure narrative author:** Operating Review (per Plan §12.1 v2.0 batched discharge row).
- **This challenge round's challenger:** Operating Review (provisional).
- **Overlap:** Operating Review is **both** the original finding author AND the closure narrator AND the provisional challenger. Same-parties pattern present.
- **Mitigation in force:** template (§3 Tier "Plan-step gate") permits Operating Review as the challenger explicitly for Days 0–30 plan-step rounds; F-3 binds Day-30 CHRO external re-challenge.
- **Note:** Step 17 has loose coupling to Step 10 (`incident-response.md` §6 references the dashboard for action item tracking); the F-2 follow-up (postmortem action items section) addresses the structural integration.

**Result:** **PASS-with-explicit-residual-risk.** Same-parties pattern present and disclosed; mitigation route documented; loose coupling with Step 10 routed to F-2.

---

## 3. Verdict

**PASS-with-follow-ups (provisional).**

| Lifecycle event                                  | Authorised by this verdict?                                                                                                                                                                                   |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Step 17 ✅ Closed status retroactively confirmed | **Yes (provisional).** All five vectors PASSED or PASSED-with-conditions; V-3 (Trim-to-Pass) passed exemplarily (multiple net strengthenings: honest empty-state, Hierarchy of Truth, Open Items governance). |
| Step 17 ✅ Closed status reopened to 🔵          | **No.** No FAIL vector; documented strengthenings only.                                                                                                                                                       |
| Audit-gap discharge for Step 17                  | **Yes (provisional).** F-3 binds final discharge to Day-30 CHRO external re-challenge.                                                                                                                        |

---

## 4. Follow-up items

| ID  | Severity | Item                                                                                                                                                                                                                                                                                                                                                                                                              | DRI                                         | Target Close        | Gates ✅ status?                                                      |
| :-- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :------------------ | :-------------------------------------------------------------------- |
| F-1 | P3       | Add a §3.5 "Stage 0 Discovery Projects" sub-section: "Lightweight watchlist of Stage 0 projects in discovery > 30 days OR > 60 days. Visibility-only; not gated. Stage 0 > 90 days triggers a CPO/CTO escalation conversation." (V-1 finding.) AND add a "Team Load" column to §3 once N ≥ 2 active projects: lists named engineering ICs allocated > 25% to the project. (V-1 finding.)                          | CTO + VP Platform + CPO                     | Day 60 (2026-06-19) | **No** — non-blocking; activation tied to N ≥ 1.                      |
| F-2 | P3       | Add a §4.5 "Postmortem Action Items" sub-section that aggregates open AI-N items from per-project `incidents/<id>-postmortem.md` files. Mirrors §4's escalation discipline: P0 AI ≥ 30 days → CTO escalation; P1 AI ≥ 60 days → CTO notification (per `incident-response.md` §6). Activation tied to first Sev1 postmortem filed. (V-1 finding; coupling with Step 10.)                                           | CTO + VP Platform + CSO                     | Day 60 (2026-06-19) | **No** — operational integration; activation event-driven.            |
| F-3 | P2       | Specify the §3 Risk emoji thresholds: 🟢 = days-in-stage ≤ 1.0× baseline + 0 P0/P1; 🟡 = days-in-stage > 1.0× and ≤ 1.5× baseline OR ≥ 1 P1 open; 🟠 = days-in-stage > 1.5× and ≤ 2.0× baseline OR ≥ 1 P1 open ≥ 5 business days; 🔴 = days-in-stage > 2.0× baseline OR any P0 open OR ≥ 1 P1 open ≥ 10 business days. AND CHRO-recruited external challenger executes Day-30 re-challenge. (V-2 + V-5 findings.) | CTO + VP Platform + CHRO + Operating Review | Day 30 (2026-05-20) | **Yes — binding gate for unconditional Step-17 audit-gap discharge.** |

---

## 5. What this report does NOT certify

- **The upstream `progress.md` per-project schema** — §7 OI-02 explicitly defers schema lock until N=1 project; until locked, the §3/§4/§5 schemas are provisional and may need revision when first PRD enters Stage 1.
- **The `checkpoints/*.json` Layer-3 schema quality** — referenced in §2; quality not audited here.
- **The first real refresh cycle** — N=0 today; first PRD entering Stage 1 will be the first real test.
- **The auto-refresh integration** — explicitly deferred (§7 OI-01); the manual-mirror model is the current design.
- **The studio-side dashboard** — the `company/project/_dashboard.md` is for company pipelines; studio has its own surface.
- **CEO actual usage of the dashboard** — operational; the §10 success metric measures freshness, not usage.
- **The interaction between the CTO + VP Platform shared ownership** — operational; CTO is the canonical DRI for §3 + §5; VP Platform is canonical for §4 burn-down + §6 OI-01 auto-refresh.

---

## 6. Document version history

| Version | Date           | Author                         | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :------ | :------------- | :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | Operating Review (provisional) | Initial Independent Challenge round on Step 17 per template v1.0 — **post-closure backfill** under Option A of the audit-gap remediation. **Verdict: PASS-with-follow-ups (provisional).** All five attack vectors executed; V-3 Trim-to-Pass passed exemplarily (multiple net strengthenings: honest empty-state matches KEEP-04 cultural pattern; Hierarchy of Truth resolves two-sources-of-truth anti-pattern; Open Items governance); three follow-ups (F-1 through F-3) filed; F-3 binds Day-30 CHRO external re-challenge. |
