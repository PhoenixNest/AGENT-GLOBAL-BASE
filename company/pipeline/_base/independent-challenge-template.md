# Independent Challenge Round — Template

| Field             | Value                                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------------------------------- |
| **Document Type** | Process template (the "Red Team Review" instrument)                                                             |
| **Owner**         | CTO Nakamura (delegated to Software Architect Rafael Okonkwo)                                                   |
| **Effective**     | 2026-04-21                                                                                                      |
| **Cross-Refs**    | [`pipeline.md`](./pipeline.md) Stages 6 / 8 / 10 / 11 — this template is invoked at every multi-condition gate. |

---

## 1. Purpose

> **The problem this template solves.** Multi-condition gate reports — "all 24 conditions satisfied," "all 12 release-checklist rows green," "all 8 P0 items closed" — carry a structural vulnerability when the conditions are authored, the evidence is assembled, and the sign-off is requested by the same DRI cluster. There is no external check that the conditions were the _right_ conditions, no adversarial scan for what the listed conditions did not cover, and no "what's missing" pass.
>
> This template is the **operating instrument** that breaks that closure. It defines a single, repeatable challenge protocol that every multi-condition gate report must pass before its corresponding step transitions from `🔵 Implemented` to `🟢 Verified`.

The pattern is borrowed from the Bezos red-team review and adapted to this company's pipeline lifecycle. It is **not** a re-audit of the work; it is an adversarial scan for what the original DRIs missed.

---

## 2. When to Invoke

A challenge round is **mandatory** when ALL of the following are true:

| Condition                              | Threshold                                                                                                                                                                                                  |
| :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Multi-condition gate report exists** | The artifact under review asserts ≥ 5 distinct conditions / criteria / checklist rows that must all be met. (Single-condition decisions go through normal sign-off, not this template.)                    |
| **Same-parties-closure risk**          | The conditions were authored AND the evidence was assembled AND the sign-off is being requested by overlapping DRIs (≥ 1 person sits on both the authoring side and the closure side).                     |
| **Step is at `🔵 Implemented`**        | The work is done; the question is verification, not implementation. The challenge is not an early-stage design review.                                                                                     |
| **Closure carries irreversible cost**  | If the closure is wrong, the cost to undo it exceeds the cost of the 48-hour challenge window. (Practically true for every Stage 6 / 8 / 10 / 11 gate; not always true for low-blast-radius polish items.) |

A challenge round is **also recommended** for any step that has stayed at `🔵 Implemented` for **> 2 weeks** without progressing to `🟢`. Long dwell at 🔵 is itself evidence that a structural blocker — likely the missing challenge — is suppressing close.

A challenge round is **NOT required** for:

- Single-DRI content edits inside an existing section (no closure event).
- Status flips that don't transition the lifecycle past `🔵`.
- Daily-log appends, risk-register additions, or backlog grooming (no gate criterion involved).

---

## 3. Who Challenges (Designated Challenger Persona)

The challenger must be **structurally independent** of the DRI cluster that authored the work. "Structurally independent" means:

- Did not author the original conditions / criteria / checklist.
- Did not produce the evidence being verified.
- Is not in the sign-off chain for closure.
- Reports through a different leadership branch where practical (e.g., CHRO-recruited external advisor; CSO challenging a CPO close; Software Architect challenging a CTO close — under delegation).

| Tier               | Default challenger                                                                                                                                                                          | Notes                                                                                                                           |
| :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------ |
| **Stage 6 / 8**    | Software Architect (Rafael Okonkwo) when CTO is on the closure side; CIO (Dr. Priya Mehta) when CTO _and_ Software Architect both authored; external advisor when both are on closure side. | Software Architect is the standing pre-delegated challenger for Stage 6/8 conformance.                                          |
| **Stage 10**       | A C-suite peer who did **not** sign Stage 8 (e.g., CSO challenges a CPO + CTO close; CDO challenges a CSO + CIO close).                                                                     | Stage 10 is the company's last-defense gate. Cross-functional challenge required.                                               |
| **Stage 11**       | VP Quality (when VP Platform + CSO close); VP Platform (when CSO + VP Quality close). Postmortems in Stage 11 ALSO trigger this template if ≥ 5 action items.                               | Live-ops gate reports are the highest-frequency closure surface; rotate the challenger to prevent collusion.                    |
| **Plan-step gate** | An external advisor recruited by the CHRO (the "Independent Reviewer" persona).                                                                                                             | The external advisor is required for plan-step gate reports because plan-step DRIs typically cluster across multiple functions. |

**Forbidden challenger compositions:**

- Anyone who authored the conditions being challenged.
- The DRI requesting the closure.
- Anyone in the direct reporting line of the DRI requesting closure for the matter at hand.

---

## 4. Protocol — The Five Attack Vectors

A challenge round is a **single 48-hour window**. The challenger executes the five attack vectors below and produces a single report (template in §5). Time-boxing is non-negotiable — challenge latency would otherwise become its own gate-blocker. If the challenger cannot complete the round in 48 hours, the round defaults to **conditional PASS** with the open vectors noted as follow-ups, and the step transitions to `🟢` — but the open vectors then block the step's transition to `✅ Closed`.

| #   | Vector                             | Question the challenger must answer                                                                                                                                                                                                                                                              |
| :-- | :--------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| V-1 | **Completeness (what's missing?)** | Are the conditions / criteria themselves the _right_ set? What categories of risk are not represented in the list? If the report lists N conditions, is there an N+1 the original DRIs didn't see?                                                                                               |
| V-2 | **Sufficiency (are they enough?)** | For each listed condition, is the threshold actually high enough? Is the evidence actually meeting the threshold, or being normalized to a passing reading by the way it's measured?                                                                                                             |
| V-3 | **Trim-to-Pass (KEEP-01) scan**    | Was anything silently removed, weakened, narrowed, or relabelled to make a failing condition pass? Compare the closure narrative against the prior version of the artifact (or the legacy file it supersedes). Any quiet drop = automatic `FAIL`.                                                |
| V-4 | **Counter-evidence search**        | Where is the evidence that this remediation _won't_ work? Cite at least one external benchmark, one historical near-miss in this company, or one industry case study showing the same condition failing under similar circumstances. Absence of a counter-search is itself evidence of weakness. |
| V-5 | **Same-parties-closure audit**     | Confirm in writing that the challenger is structurally independent per §3. Confirm that no condition in the report was both authored and signed off by the same person without a peer review. Where overlap exists, document it as a residual risk.                                              |

The five vectors are **mandatory and ordered**. V-3 (Trim-to-Pass scan) is the only vector that can produce an automatic `FAIL` — the other four can produce `PASS-with-conditions` outcomes routed to follow-up.

---

## 5. Report Shape (The Deliverable)

Every challenge round produces a single Markdown report at:

```text
company/pipeline/<product>/independent-challenge-stage-<X>-<date>.md   (for stage-gate challenges)
studio/<studio>/independent-challenge-<topic>-<date>.md                (for studio-scoped challenges)
company/optimization-history/<plan-id>/independent-challenge-<topic>.md (for plan-step challenges)
```

The report MUST contain:

| Section                                  | Content                                                                                                                                                                                                                                                     |
| :--------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **§0 Header metadata**                   | Subject, original DRI cluster, challenger identity + structural-independence statement, date the round opened, date the report was filed (must be ≤ 48h apart).                                                                                             |
| **§1 Subject and scope**                 | One paragraph: what the challenger reviewed, what they did NOT review (e.g., upstream/downstream scope boundaries).                                                                                                                                         |
| **§2 The five attack vectors**           | One sub-section per vector (V-1 through V-5). Each sub-section ends with a result: `PASS` / `PASS-with-conditions` / `FAIL`. V-3 (Trim-to-Pass) result is bolded for CEO scan.                                                                              |
| **§3 Verdict**                           | One of: **PASS** (no follow-ups; step may transition `🔵 → 🟢`); **PASS-with-follow-ups** (step may transition `🔵 → 🟢` AND the follow-ups gate `🟢 → ✅ Closed`); **FAIL** (step stays at `🔵`; remediation cycle reopened with the failed vector named). |
| **§4 Follow-up items**                   | Each item: ID, severity (P0–P3), DRI, target close date, gating relationship to step `🟢 → ✅ Closed`.                                                                                                                                                      |
| **§5 What this report does NOT certify** | Boundary statement. Names the residual risks the challenger could not eliminate within the 48-hour window.                                                                                                                                                  |
| **§6 Document version history**          | Same shape as the base pipeline.                                                                                                                                                                                                                            |

---

## 6. Authority and Sign-off

| Action                                        | Authority                                                                                                                          |
| :-------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| Template ownership                            | Software Architect Rafael Okonkwo (under CTO Nakamura)                                                                             |
| Challenger assignment for an individual round | DRI requesting closure proposes; CTO confirms (or CIO if CTO is on the closure side)                                               |
| Verdict authority                             | The challenger alone. Verdicts are not negotiable inside the 48-hour window; appeals route to CTO (or CEO if CTO on closure side). |
| `🔵 → 🟢` lifecycle flip                      | Original DRI, citing the challenge report's verdict in their close note.                                                           |
| Template revisions (this file)                | Software Architect, with CTO sign-off.                                                                                             |

---

## 8. Document Version History

| Version | Date           | Author             | Changes                                                                                                                                                                                                                                                                                         |
| :------ | :------------- | :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | April 21, 2026 | Software Architect | Initial template authored. Five attack vectors fixed (V-1 Completeness, V-2 Sufficiency, V-3 Trim-to-Pass, V-4 Counter-evidence, V-5 Same-parties-closure audit). 48-hour time-box. Designated challenger persona ("Independent Reviewer") recruited via the standard L4/L5 elite-gate process. |
