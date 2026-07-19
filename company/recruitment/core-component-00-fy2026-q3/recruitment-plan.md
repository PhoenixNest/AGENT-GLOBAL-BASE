# Core Component 00 Recruitment Plan — FY2026 Q3

| Field              | Value                                                                     |
| ------------------ | ------------------------------------------------------------------------- |
| **Document Type**  | Recruitment Plan                                                          |
| **Plan ID**        | `core-component-00-fy2026-q3`                                             |
| **Date**           | July 3, 2026                                                              |
| **Prepared By**    | Dr. Elias Vance (Laboratory Director) + CHRO Office (Dr. Evelyn Hartwell) |
| **Submitted To**   | CEO — Executive Review                                                    |
| **Classification** | Internal — Leadership Only                                                |
| **Status**         | Complete — all 3 phases, 11/11 roles filled                               |
| **Version**        | 1.3                                                                       |
| **Department**     | Core Component 00 — LLM Engineering Laboratory                            |

---

## Executive Summary

> CC-00 has operated as a single-person laboratory (Dr. Elias Vance only) since its charter on
> 2026-04-28, despite being a **mandatory dependency** at Stage 3 and Stage 5 of all four company
> development pipelines, the sole ASE governance authority for every LLM-powered system in the
> organization, and the owner of four production-grade modules carrying live `pytest` suites
> (Context, Harness, RAG, Multi-Agent Engineering). No other department or studio in this
> organization runs at 1:∞ staffing-to-scope ratio — the Casual Games Studio fields 39 crew across
> 7 divisions, and every company department has C-suite plus supervisors plus teammates. This gap
> was a standing single point of failure: any CC-00-touching pipeline stage, ASE audit, or
> production incident depended on one person's availability. This cycle hires 4 elite Research
> Engineers to give direct, accountable engineering ownership of the four coded modules, freeing
> Dr. Vance to focus on cross-module architecture, ASE ratification, and research-programme
> direction — the work only the Director's authority can do.

> **Amendment (2026-07-03, v1.1):** Following CEO review of Dr. Vance's post-hire Composition
> Assessment (`core-component-00/crew/README.md`), the CEO approved a second recruitment phase to
> close four structural gaps the 4-hire cycle above left open: bus factor of 1 on the two
> highest-load modules, absence of an independent research-scientist tier, absence of a dedicated
> safety/evaluation function, and absence of infrastructure support for the lab's heaviest
> dependency footprint. **The CEO's explicit directive: the lab does not outsource operations —
> every Phase 3 role is a direct FTE hire through the standard 9-stage pipeline, not a contractor
> or vendor engagement.** Phase 3 is scoped below.

> **Amendment (2026-07-03, v1.2):** The CEO reviewed the Phase 3 scope and directed that the two
> residual risks Dr. Vance logged as "not yet closed" — single-owner bus factor on Context
> Engineering and Harness Engineering — be closed **within this expansion, not deferred to next
> quarter.** The CEO's position: "address the issues you raised as part of the current workforce
> expansion plan," not postpone them to an unspecified future cycle. Phase 3 is expanded from 5 to
> 7 roles accordingly; bus factor is now closed on all four production-grade modules, not two.

| Metric              | Value                                                                                                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Total FTEs**      | 11 FTEs total (4 hired in Phases 1–2 + 7 in Phase 3: 2 × L4 Staff, 5 × L3 Senior)                                                                                         |
| **Phases**          | 3 (Phase 1: Leadership → Phase 2: Research Engineering ICs → Phase 3: Coherence & Capability Expansion, fully scoped)                                                     |
| **Timeline**        | Phases 1–2: 6 weeks (complete). Phase 3: 6 weeks (Weeks 1–6 — extended by 1 week to absorb 2 additional L3 hires)                                                         |
| **Hiring Model**    | Phase 3 staggered — Research Scientist and Safety & Evaluation Engineer (both L4) hired first as bar-raisers for all 5 L3 ICs, mirroring the Phase 1/2 sequencing pattern |
| **Hiring Standard** | Elite — no compromise on quality (L3 floor 17/20, L4 floor 18/20). All FTE, no outsourced/contractor roles, per CEO directive                                             |

---

## Division / Org Structure

| Role                                           | Level | Count | Reports To       | Department        | Phase |
| ---------------------------------------------- | ----- | ----- | ---------------- | ----------------- | ----- |
| Staff Research Engineer, Multi-Agent Eng. Lead | L4    | 1     | Dr. Elias Vance  | Core Component 00 | 1     |
| Senior Research Engineer                       | L3    | 3     | Dr. Elias Vance  | Core Component 00 | 2     |
| Staff Research Scientist                       | L4    | 1     | Dr. Elias Vance  | Core Component 00 | 3     |
| Staff Safety & Evaluation Engineer             | L4    | 1     | Dr. Elias Vance  | Core Component 00 | 3     |
| Infrastructure Engineer                        | L3    | 1     | Dr. Elias Vance  | Core Component 00 | 3     |
| Senior Research Engineer II, Multi-Agent Eng.  | L3    | 1     | Dr. Idris Farouk | Core Component 00 | 3     |
| Senior Research Engineer II, RAG               | L3    | 1     | Sofia Almeida    | Core Component 00 | 3     |
| Senior Research Engineer II, Context Eng.      | L3    | 1     | Mei-Ling Zhao    | Core Component 00 | 3     |
| Senior Research Engineer II, Harness Eng.      | L3    | 1     | Kwame Asante     | Core Component 00 | 3     |

**Reporting-line fix (v1.3, audit Finding #1):** the four paired Senior Research Engineer II
roles report to their Phase 1/2 incumbent (module co-owner), not to Dr. Vance directly — Farouk,
Almeida, Zhao, and Asante each pick up their first direct report, formalizing the "module
co-ownership" pairing the plan already described in § Training Plan Summary. Dr. Vance's direct
reports drop from 11 to 7 (Farouk, Zhao, Asante, Almeida, Research Scientist, Safety & Evaluation
Engineer, Infrastructure Engineer) — within the healthy 5–8 span-of-control range.

Module assignment (Phases 1–2): 1 Research Engineer per production-grade module (Context
Engineering, Harness Engineering, Retrieval-Augmented Generation, Multi-Agent Engineering).
`prompt-engineering/` is documentation-only with no test infrastructure and remains directly held
by Dr. Vance.

Module assignment (Phase 3, v1.2 — fully scoped): all four production-grade modules now get a
second engineer, not just the two highest-load ones. Multi-Agent Engineering and RAG were
sequenced first in the original v1.1 scope because they carry the heaviest combined load (Farouk
absorbs ASE audit execution on top of his module; Almeida absorbs RAG's heavy dependency footprint
on top of hers) — that prioritization stands within Phase 3's internal sequencing, but per CEO
direction, Context Engineering and Harness Engineering are no longer deferred to a future cycle;
they close in this same phase. Every module now has bus factor 2. The Research Scientist and
Safety & Evaluation Engineer remain cross-cutting roles spanning all four modules. The
Infrastructure Engineer remains cross-cutting, with RAG's dependency footprint as primary focus.

---

## Phased Hiring Timeline

### Phase 1: Leadership (Weeks 1–2)

| Seq | Role                              | Level | Vetting Authority | Tier Floor |
| --- | --------------------------------- | ----- | ----------------- | ---------- |
| 1.1 | Staff Research Engineer, MAE Lead | L4    | CHRO + Dr. Vance  | 18/20      |

**Phase gate:** L4 hire accepted, background-checked, and onboarded — available to co-evaluate
Phase 2 candidates per top-tier benchmarking practice (Amazon-style bar-raiser participation).

### Phase 2: Research Engineering ICs (Weeks 3–6)

| Seq | Role                                           | Level | Vetting Authority           | Tier Floor |
| --- | ---------------------------------------------- | ----- | --------------------------- | ---------- |
| 2.1 | Senior Research Engineer — Context Engineering | L3    | CHRO + Dr. Vance + MAE Lead | 17/20      |
| 2.2 | Senior Research Engineer — Harness Engineering | L3    | CHRO + Dr. Vance + MAE Lead | 17/20      |
| 2.3 | Senior Research Engineer — RAG                 | L3    | CHRO + Dr. Vance + MAE Lead | 17/20      |

**Phase gate:** All 3 IC roles filled with candidates meeting or exceeding the L3 floor; crew
folder structure established at `core-component-00/crew/` and all 4 agent profiles published.

### Phase 3: Coherence & Capability Expansion (Weeks 1–6) — CEO-approved 2026-07-03, fully scoped v1.2

| Seq | Role                                           | Level | Vetting Authority                                       | Tier Floor |
| --- | ---------------------------------------------- | ----- | ------------------------------------------------------- | ---------- |
| 3.1 | Staff Research Scientist                       | L4    | CHRO + Dr. Vance                                        | 18/20      |
| 3.2 | Staff Safety & Evaluation Engineer             | L4    | CHRO + Dr. Vance                                        | 18/20      |
| 3.3 | Senior Research Engineer II — Multi-Agent Eng. | L3    | CHRO + Dr. Vance + Research Scientist + Safety Engineer | 17/20      |
| 3.4 | Senior Research Engineer II — RAG              | L3    | CHRO + Dr. Vance + Research Scientist + Safety Engineer | 17/20      |
| 3.5 | Senior Research Engineer II — Context Eng.     | L3    | CHRO + Dr. Vance + Research Scientist + Safety Engineer | 17/20      |
| 3.6 | Senior Research Engineer II — Harness Eng.     | L3    | CHRO + Dr. Vance + Research Scientist + Safety Engineer | 17/20      |
| 3.7 | Infrastructure Engineer                        | L3    | CHRO + Dr. Vance + Research Scientist + Safety Engineer | 17/20      |

**Sequencing within Phase 3:** 3.1–3.2 (the two L4 bar-raisers) hire first, exactly as in v1.1.
3.3–3.4 (Multi-Agent, RAG — the highest-load modules) fill next. 3.5–3.7 (Context, Harness,
Infrastructure) fill in the same phase, not a subsequent one — the only change from v1.1 is that
these three no longer wait for a future cycle to open.

**Phase gate:** All 7 roles filled with candidates meeting or exceeding tier floor; bus factor
closed on **all four** production-grade modules, not just two; ASE compliance audits (executed by
Farouk) gain an independent adversarial check from the Safety & Evaluation Engineer;
`core-component-00/crew/` gains a `research-science/`, `safety-evaluation/`, and `infrastructure/`
role folder, and each of the four existing module folders gains a second engineer subfolder; all
Phase 3 hires are **direct FTEs — no contractor, vendor, or outsourced arrangement of any kind**,
per CEO directive.

**Rationale for scope (fully closed, not "postpone"):** This phase now directly answers the CEO's
stated bar for the lab without a residual gap: internal coherence and cohesion (bus factor closed
on all four modules, not two), high operational standards (independent safety/evaluation
function, not self-audited), top-tier research capability (a second PI-capable researcher, not
execution-only engineers), and industry foresight (dedicated infra capacity frees the RAG owner to
look outward instead of firefighting her own dependency stack). The v1.1 decision to prioritize
Multi-Agent Engineering and RAG first, and defer Context/Harness Engineering to a future cycle,
was a sequencing judgment about which risk was most urgent — not a judgment that the other two
didn't matter. The CEO's direction confirms they matter now; Phase 3 reflects that in full.

**Amendment (2026-07-03, v1.3):** The CEO delegated both execution and decision-making authority
for this initiative to Dr. Vance and resolved the two open findings from his pre-execution audit.
**(1) Infrastructure Engineer redundancy — resolved, not redundant.** R&D's DevOps Lead and SRE
Engineers serve the parent company's own operations; they hold no standing mandate over CC-00's
dependency footprint. The Infrastructure Engineer role proceeds exactly as scoped in v1.2 — a
dedicated lab-level infra function, distinct from R&D's bench, not a duplicate of it.
**(2) Reporting-line span-of-control — fixed in § Division / Org Structure below**, per Dr.
Vance's own audit finding. Timeline pacing (audit Finding #4) is accepted as scoped under
delegated authority; if it slips, Dr. Vance now holds standing authority to adjust it without
further CEO review.

---

## Compensation Strategy

Compensation follows the standard L3/L4 bands defined in the CHRO-owned quarterly configuration
artifact `compensation-bands.md` (`company/pipeline/recruitment/pipeline.md` § Quarterly
Configuration Cycle). No role-specific adjustments were requested for this cycle.

**No-outsourcing policy (Phase 3):** Per explicit CEO directive, all 7 Phase 3 roles are budgeted
and compensated as direct FTEs under standard `compensation-bands.md` levels. No portion of Phase
3 scope — including the Infrastructure Engineer role, which might otherwise be filled via a
staffing vendor or managed-service contract at other organizations — may be fulfilled through a
contractor, consultancy, or outsourced-operations arrangement. If a role genuinely cannot be
filled as a direct FTE within the pipeline's standard channels, it is escalated to CHRO and Dr.
Vance for re-scoping, not routed around this policy via a contract vehicle.

---

## Vetting Standards

All candidates passed through the 9-stage pipeline defined in
[`company/pipeline/recruitment/pipeline.md`](../../pipeline/recruitment/pipeline.md).

| Tier | Level  | Minimum Vetting Score | Secondary Reviewer                                                   |
| ---- | ------ | --------------------- | -------------------------------------------------------------------- |
| L3   | Senior | 17/20                 | CTO + VP (n/a — CHRO + Dept Head substituted; CC-00 has no VP layer) |
| L4   | Staff  | 18/20                 | CHRO + C-Suite (Dr. Vance acting as Dept Head)                       |

---

## Sourcing Channels

| Channel                                                                                                | Priority | Notes                                                                                 |
| ------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------- |
| Competitor talent watchlist (Anthropic, DeepMind, Meta AI, Cohere)                                     | High     | Direct alumni network for context/harness/RAG/multi-agent specialists                 |
| Direct network / referrals                                                                             | High     | Weighted 1.5× per Meta-style referral-quality practice                                |
| Specialist LLM/ML research job boards + publication databases                                          | Medium   | Used for RAG and multi-agent PhD-level candidates                                     |
| Open-source signal detection (GitHub)                                                                  | Medium   | Stripe-style signal for harness/reliability candidates                                |
| Research-scientist / safety-eval specialist networks (conference speaker lists, publication databases) | High     | Phase 3 only — sourcing for Research Scientist and Safety & Evaluation Engineer roles |

All Phase 3 sourcing goes through the same direct-hire channels above. Staffing agencies and
outsourced-recruiting vendors are explicitly out of scope — sourcing identifies FTE candidates
only, consistent with the no-outsourcing policy in § Compensation Strategy.

---

## Training Plan Summary

| Phase   | Mandatory Modules                                                                                                                                                                                                                                                                                                                                                        | Delivered By                        | Deadline |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------- | -------- |
| Phase 1 | CC-00 module architecture onboarding, ASE governance framework                                                                                                                                                                                                                                                                                                           | Dr. Vance                           | Day 30   |
| Phase 2 | Owned-module deep dive, workspace conventions, ASE compliance basics                                                                                                                                                                                                                                                                                                     | MAE Lead + Dr. Vance                | Day 30   |
| Phase 3 | Research-programme onboarding (Research Scientist), ASE audit shadowing + independent red-team standup (Safety & Evaluation Engineer), module co-ownership handoff with existing engineer — all 4 module pairs: Zhao↔CE-II, Asante↔HE-II, Almeida↔RAG-II, Farouk↔MAE-II (Research Engineers II), dev-environment/dependency ownership transfer (Infrastructure Engineer) | Dr. Vance + relevant Phase 1/2 hire | Day 30   |

---

## Contingency Planning

| Scenario                                    | Trigger                     | Response                                                                                                                                                        |
| ------------------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Phase 1 L4 candidate withdraws              | Offer declined / withdrawal | Dr. Vance + CHRO conduct Phase 2 evaluation alone; reopen Phase 1 in parallel                                                                                   |
| Any Phase 2 L3 candidate fails vetting gate | Vetting score below 17/20   | Auto-reject per pipeline rules; re-source within 2 weeks without delaying the other Phase 2 hires                                                               |
| Either Phase 3 L4 candidate withdraws       | Offer declined / withdrawal | Dr. Vance + CHRO conduct the 5 L3 evaluations with one bar-raiser instead of two; reopen the L4 seat in parallel — never fill it with a contractor as a stopgap |
| Any Phase 3 L3 candidate fails vetting gate | Vetting score below 17/20   | Auto-reject per pipeline rules; re-source within 2 weeks; the vacant seat stays open and FTE-only, never bridged with contract labor                            |

---

## Document Version History

| Version | Date       | Author                          | Changes                                                                                                                                                                                                                                                                                                                                                          |
| ------- | ---------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-07-03 | Dr. Vance + CHRO Office         | Cycle complete — 4/4 roles filled, all hires above tier floor                                                                                                                                                                                                                                                                                                    |
| 1.1     | 2026-07-03 | Dr. Vance + CHRO Office         | CEO-approved Phase 3 opened: Research Scientist, Safety & Evaluation Engineer, 2nd Multi-Agent Eng., 2nd RAG Eng., Infrastructure Engineer. All 5 roles direct FTE — no outsourcing, per CEO directive. Status reopened from Complete to In Progress.                                                                                                            |
| 1.2     | 2026-07-03 | Dr. Vance + CHRO Office         | CEO directed the two residual risks (Context Eng., Harness Eng. bus factor) be closed within this expansion, not deferred. Phase 3 expanded 5→7 roles: added Senior Research Engineer II — Context Engineering and — Harness Engineering. Total lab FTEs 9→11. Bus factor now closed on all four production-grade modules.                                       |
| 1.3     | 2026-07-03 | Dr. Vance (delegated authority) | CEO delegated execution + decision authority to Dr. Vance; resolved Infrastructure Engineer redundancy question (not redundant — R&D DevOps/SRE serve the parent company only). Applied Dr. Vance's own audit fix: the 4 paired Senior Research Engineer II roles now report to their Phase 1/2 incumbent, not Dr. Vance directly. His direct reports drop 11→7. |
