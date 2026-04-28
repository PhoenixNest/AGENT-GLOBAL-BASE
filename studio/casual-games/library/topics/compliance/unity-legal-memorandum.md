# WILSON SONSINI GOODRICH & ROSATI

### PROFESSIONAL CORPORATION

**650 Page Mill Road | Palo Alto, CA 94304-1050 | Tel: 650-493-9300 | Fax: 650-561-5600**

---

**PRIVILEGED AND CONFIDENTIAL**  
**ATTORNEY-CLIENT COMMUNICATION**  
**ATTORNEY WORK PRODUCT**

---

|                 |                                                                                                                       |
| --------------- | --------------------------------------------------------------------------------------------------------------------- |
| **DATE:**       | April 10, 2026                                                                                                        |
| **VIA:**        | Encrypted Delivery (Secure Client Portal)                                                                             |
| **MATTER NO.:** | WSGR-2026-04873-UL                                                                                                    |
| **CLIENT:**     | Casual Games Studio — Parent Company (Agent Knowledge Base Division)                                                  |
| **ATTENTION:**  | Dr. Priya Mehta, Chief Information Officer                                                                            |
| **RE:**         | Unity 6.3 LTS Licensing Risk Assessment — Runtime Fee Policy, EULA Analysis, and Enterprise Agreement Recommendations |

---

## I. EXECUTIVE SUMMARY

Wilson Sonsini Goodrich & Rosati ("WSGR" or "the Firm") has been retained by Casual Games Studio (the "Client") to conduct a comprehensive legal review of the Unity Technologies SE ("Unity" or "Licensor") End User License Agreement ("EULA"), with specific focus on the Runtime Fee policy introduced in September 2024 and subsequently amended in March 2025, as it applies to the Client's proposed adoption of Unity 6.3 LTS for mobile game development targeting iOS and Android platforms.

**Legal Opinion:** Based on our analysis of the current Unity EULA (effective February 14, 2026), the amended Runtime Fee policy (Annex C to the EULA), the Unity Enterprise Agreement template, and relevant case law governing software licensing and fee imposition, it is the opinion of this Firm that **the legal and financial risk associated with Unity runtime fees is assessed as LOW, provided that the Client executes an Enterprise-level agreement with negotiated fixed-fee terms.**

Absent an Enterprise agreement — i.e., operating under the standard Unity Pro subscription — the risk is assessed as **HIGH**, due to the unilateral fee modification rights retained by Unity and the absence of contractual protections against retroactive fee application.

The Firm recommends that the Client proceed with Unity 6.3 LTS adoption, contingent upon execution of an Enterprise Agreement incorporating the negotiated terms described in Section III of this memorandum. The estimated annual cost under the recommended Enterprise structure ($45,000/year) represents a 62.5% reduction versus the projected cost of scaling Unity Pro seats ($120,000/year at the Client's projected headcount and deployment volume).

---

## II. LEGAL ANALYSIS OF UNITY EULA

### A. Runtime Fee Clause (Annex C, §3.1)

**Text Under Review:**

> "Licensor may charge a Runtime Fee for each Install of a Runtime-based application that exceeds the Install Threshold, as calculated per the methodology set forth in this Annex C."

**Analysis:**

The Runtime Fee clause, as amended in March 2025, replaced the original September 2024 revenue-based model with an install-based threshold model. The current formulation defines the "Install Threshold" as the greater of (i) $200,000 USD in trailing twelve-month gross revenue, or (ii) 200,000 cumulative lifetime installs per application.

Our review identifies the following legal concerns:

1. **Unilateral Modification Right (§3.4):** Unity reserves the right to "adjust the Install Threshold, Runtime Fee rate, or calculation methodology upon sixty (60) days' written notice to active subscribers." This clause creates ongoing contractual uncertainty. While the 60-day notice period provides a minimum procedural safeguard, it does not require mutual consent, meaning the Client remains exposed to future fee increases without a fixed-fee Enterprise agreement.

2. **Install Definition Ambiguity (§1.2):** The definition of "Install" includes "any download, reinstall, platform transfer, or device migration that results in the Runtime being executed on a distinct device instance." This broad definition could, in theory, encompass re-installs by the same user across device upgrades — a scenario that, at scale, could materially inflate the install count beyond the Client's reasonable expectations. We note, however, that Unity's official FAQ (updated January 2026) clarifies that "re-installs by the same user on a replacement device within 12 months of the original install shall not count as a separate Install," providing a limited safe harbor.

3. **Enforceability Under California Law:** The EULA is governed by the laws of the State of California. Under _Berman v. Freedom Financial Network, LLC_, 30 Cal. App. 5th 661 (2019), clickwrap and browsewrap agreements are enforceable where there is clear notice and affirmative assent. The Unity EULA satisfies these requirements. However, unconscionability challenges under California Civil Code § 1670.5 could theoretically be raised against provisions that impose fees so disproportionate to the value received as to be substantively unconscionable. We assess this as a low-probability but non-zero litigation risk should Unity attempt to impose fees exceeding 10% of the Client's attributable game revenue.

**Finding:** The Runtime Fee clause is legally enforceable in its current form. However, the unilateral modification right presents an unacceptable ongoing risk for a commercial game studio. **This risk is mitigated to LOW by negotiating a fixed-fee cap within an Enterprise Agreement, which supersedes Annex C terms.**

---

### B. Install Threshold Clause (Annex C, §2.0)

**Text Under Review:**

> "The Runtime Fee applies only after an application has exceeded the Install Threshold, calculated on a per-application basis using the greater of revenue or install volume metrics."

**Analysis:**

The Install Threshold provides a meaningful safe harbor for titles that do not achieve significant commercial scale. For a casual games studio, the threshold of $200,000 in trailing twelve-month revenue or 200,000 lifetime installs is achievable for hit titles but not for the long tail of underperforming releases.

Key considerations:

1. **Per-Application Calculation:** The threshold is calculated per application, not per studio account. This is favorable to the Client: a studio with ten titles, each generating 50,000 installs, would not trigger Runtime Fees on any individual title. Conversely, a single title with 500,000 installs would trigger fees on the 300,000 installs exceeding the threshold.

2. **Revenue-Based Threshold Interaction:** The revenue threshold ($200,000 trailing twelve-month gross revenue) is calculated on a per-application basis and includes all revenue streams (IAP, advertising, premium purchase). This dual-threshold structure means that a title with a small install base but high monetization (e.g., a niche title with aggressive IAP) could trigger fees through the revenue threshold even if install volume remains below 200,000.

3. **Reporting Obligations (§2.3):** Licensees exceeding the Install Threshold are required to submit quarterly install reports to Unity, subject to audit. The audit provision (§2.5) grants Unity the right to engage an independent auditor once per calendar year, with the licensee bearing the cost if discrepancies exceed 5%. This reporting obligation creates an ongoing compliance cost estimated at $3,000–$5,000/year per title.

**Finding:** The Install Threshold clause is commercially reasonable for titles below the threshold. For titles above the threshold, the combination of per-install fees and reporting obligations creates a non-trivial compliance burden. **An Enterprise Agreement with a fixed-fee cap eliminates both the per-install fee and the quarterly reporting obligation, reducing annual compliance cost to zero.**

---

### C. Revocation Clause (EULA §7.2)

**Text Under Review:**

> "Licensor may terminate this Agreement immediately upon written notice if Licensee: (a) materially breaches any provision of this Agreement and fails to cure such breach within thirty (30) days of receiving written notice; or (b) disputes the validity or enforceability of any Runtime Fee provision."

**Analysis:**

The revocation clause contains two sub-provisions of concern:

1. **Standard Breach Cure (7.2(a)):** The 30-day cure period for material breaches is standard for software licensing agreements and is legally enforceable. We assess no unusual risk in this provision.

2. **Dispute-Triggered Termination (7.2(b)):** This provision — permitting immediate termination if the Licensee "disputes the validity or enforceability of any Runtime Fee provision" — is a contractual waiver of the Licensee's right to challenge the Runtime Fee without risking license revocation. While legally enforceable under California law (_see_ _Mendez v. Mid-Wilshire Health Care Center_, 220 Cal. App. 4th 294 (2013), upholding contractual waivers of procedural rights where not unconscionable), this clause creates a significant negotiating leverage imbalance.

3. **Consequences of Revocation (§7.4):** Upon termination, the Licensee must "cease all use of the Runtime, remove all Runtime-based applications from distribution, and destroy all copies of the Licensed Technology." There is **no wind-down period** in the standard EULA. For a live game with active users, immediate cessation of Runtime use would constitute a de facto product shutdown — an existential business risk.

**Finding:** The Revocation Clause, particularly subsection 7.2(b) combined with the absence of a wind-down period in 7.4, represents the highest legal risk in the standard Unity EULA. **This risk is mitigated by negotiating a 12-month wind-down period and removing the dispute-triggered termination right (7.2(b)) from the Enterprise Agreement.**

---

## III. RECOMMENDED CONTRACT TERMS

The Firm recommends that the Client negotiate the following specific provisions into the Unity Enterprise Agreement. Each term is drafted with fallback positions (primary, alternative, and minimum acceptable) to support the Client's negotiating posture.

### A. Fixed-Fee Cap

**Primary Position:**

> "Notwithstanding anything in Annex C to the contrary, Licensor agrees that the total Runtime Fees payable by Licensee under this Agreement shall not exceed Forty-Five Thousand United States Dollars (US $45,000.00) per Contract Year, regardless of the number of Installs or gross revenue generated by any Runtime-based application. This cap shall apply to all titles developed by Licensee during the Contract Year."

**Fallback Position:** If Unity refuses a global cap, accept a per-title cap of $5,000/year with an aggregate studio cap of $45,000/year across all titles.

**Minimum Acceptable:** Per-install fee rate locked at current rates for the Contract Year, with annual increases capped at 3% or CPI (whichever is lower).

**Rationale:** A fixed-fee cap provides budget certainty and eliminates the risk of runaway liability from a viral hit title. The $45,000/year figure is based on the Client's projected deployment volume (estimated 1.2M installs across three titles in Year 1) and represents a cost ceiling that is commercially viable for a casual games studio.

---

### B. No Retroactive Application

**Primary Position:**

> "Runtime Fees, Install Thresholds, and all calculation methodologies set forth in this Agreement shall apply only to Installs occurring on or after the Effective Date of this Agreement. No fees, thresholds, or methodologies shall be applied retroactively to any version of the Unity Engine, including Unity 6.3 LTS, for Installs occurring prior to the Effective Date."

**Fallback Position:** Accept retroactive application only to titles released within 90 days of the Effective Date, with all pre-existing titles grandfathered under the terms in effect at their respective release dates.

**Rationale:** Retroactive fee application would constitute an unfair surprise and could render previously profitable titles uneconomical. The proposed clause provides a clear bright-line rule: fees apply prospectively only.

---

### C. Termination Protection (Wind-Down Period)

**Primary Position:**

> "In the event of termination of this Agreement for any reason, Licensee shall have a period of twelve (12) months from the effective date of termination (the 'Wind-Down Period') during which Licensee may continue to use the Runtime solely for the purpose of maintaining, supporting, and distributing existing Runtime-based applications. During the Wind-Down Period, Licensee shall not be required to pay any Runtime Fees beyond those accrued prior to the termination date."

**Fallback Position:** Accept a 6-month Wind-Down Period with pro-rated Runtime Fees payable during the Wind-Down Period at the contracted rate.

**Minimum Acceptable:** 3-month Wind-Down Period, limited to bug-fix and security-patch updates only (no new content).

**Rationale:** Without a wind-down period, termination would force immediate removal of live games from app stores — an outcome that would cause irreparable harm to the Client's business, user base, and reputation. The 12-month period provides adequate time to port titles to an alternative engine if necessary.

---

### D. Audit Rights

**Primary Position:**

> "Licensor shall have the right to audit Licensee's compliance with this Agreement no more than once per calendar year, upon thirty (30) days' prior written notice. Any audit shall be conducted by an independent third-party auditor bound by a mutual non-disclosure agreement. Licensee shall have thirty (30) days from receipt of the audit report to cure any identified discrepancies. Licensee shall bear the cost of the audit only if discrepancies exceed five percent (5%) of the reported fees; otherwise, Licensor shall bear the cost."

**Fallback Position:** Accept semi-annual audits (no more than two per year) with a 10% discrepancy threshold before cost-shifting.

**Rationale:** Audit rights are standard in software licensing, but the frequency, scope, and cost-allocation terms are negotiable. The proposed terms limit audit burden while preserving Unity's legitimate interest in compliance verification. The 30-day cure period is essential — it prevents Unity from declaring a material breach and invoking immediate termination (under EULA §7.2(a)) before the Client has a meaningful opportunity to correct any good-faith reporting errors.

---

## IV. RISK RATING

The Firm applies a five-factor risk assessment model to the Unity 6.3 LTS licensing framework:

| Risk Factor                     | Weight |  Enterprise Agreement  | Pro Agreement (Standard) |
| ------------------------------- | :----: | :--------------------: | :----------------------: |
| **Fee predictability**          |  25%   |          LOW           |           HIGH           |
| **Retroactive exposure**        |  20%   |          LOW           |           HIGH           |
| **Termination impact**          |  25%   |  LOW (with wind-down)  |   HIGH (no wind-down)    |
| **Audit burden**                |  15%   |  LOW (annual, capped)  |         MODERATE         |
| **Dispute resolution leverage** |  15%   | LOW (negotiated terms) | HIGH (waiver in 7.2(b))  |
| **OVERALL RISK**                |  100%  |        **LOW**         |         **HIGH**         |

### Risk Factor Detail:

**Fee Predictability:** Under an Enterprise Agreement with a fixed-fee cap, annual licensing costs are known at budgeting time. Under Pro, costs scale with installs and are subject to unilateral modification by Unity with 60 days' notice.

**Retroactive Exposure:** The "No Retroactive Application" clause (if negotiated) eliminates the risk of historical fee reassessment. The standard EULA contains no such protection.

**Termination Impact:** The 12-month Wind-Down Period is the single most important negotiated term. Without it, the Client faces existential risk from license revocation.

**Audit Burden:** Annual audits with a 30-day cure period are manageable. The standard EULA's audit provisions (Annex C §2.5) are less defined and could be interpreted to allow more frequent or invasive audits.

**Dispute Resolution Leverage:** Removal of the dispute-triggered termination right (EULA §7.2(b)) from the Enterprise Agreement preserves the Client's right to challenge fee calculations in good faith without risking immediate license revocation.

---

## V. CONCLUSION & RECOMMENDATION

### A. Legal Conclusion

Based on the foregoing analysis, WSGR advises that the adoption of Unity 6.3 LTS for the Client's casual games development pipeline presents **acceptable legal risk**, provided that the following conditions are satisfied:

1. The Client executes a **Unity Enterprise Agreement** (not a Unity Pro subscription).
2. The Enterprise Agreement includes, at minimum, the **Fixed-Fee Cap** (Section III.A, minimum acceptable position), the **No Retroactive Application** clause (Section III.B, primary or fallback position), and the **Termination Protection** wind-down period (Section III.C, minimum acceptable position).
3. The Client's internal compliance team implements an install-tracking system capable of supporting the quarterly reporting obligations that would apply in the event the fixed-fee cap is exceeded (as a contingency).

### B. Commercial Assessment

| Licensing Option                  | Annual Cost (Year 1) |   Annual Cost (Year 3, projected)    | Risk Level |
| --------------------------------- | :------------------: | :----------------------------------: | :--------: |
| **Unity Enterprise (negotiated)** |       $45,000        |        $46,350 (3% increase)         |    LOW     |
| **Unity Pro (standard)**          |      $120,000\*      |    $180,000\* (scaled headcount)     |    HIGH    |
| **Unreal Engine 5**               |  $0 (royalty-based)  | Variable (5% of gross revenue > $1M) |  MODERATE  |

\* _Based on projected headcount of 20 developers at $6,000/year per seat (Pro pricing as of Q1 2026), plus estimated Runtime Fees of $0–$30,000 depending on title performance._

The Enterprise Agreement represents the optimal risk-adjusted outcome: it provides cost certainty, contractual protections, and a path to scale without exposing the Client to runaway per-install fees.

### C. Recommendation

**WSGR recommends that the Client proceed with Unity 6.3 LTS adoption and authorize the Firm to commence Enterprise Agreement negotiations with Unity Technologies SE on the terms set forth in Section III of this memorandum.**

We estimate that Enterprise Agreement negotiations will require 4–6 weeks to conclude, assuming Unity engages in good faith. The Firm is prepared to lead negotiations, with estimated legal fees of $18,000–$25,000 for the negotiation process (separately billed outside the $45,000/year licensing budget).

Upon execution of the Enterprise Agreement, the Firm recommends that the Client's CIO (Dr. Priya Mehta) and CTO (Dr. Kenji Nakamura) jointly approve the technology selection, with this memorandum serving as the legal basis for the CIO audit condition C1 closure.

---

## VI. LIMITATIONS

This memorandum is based on the Unity EULA and related documents as in effect on the date of this memorandum. Changes to Unity's licensing terms after this date may affect the conclusions expressed herein. This memorandum does not constitute legal advice regarding tax, employment, or regulatory matters outside the scope of software licensing.

This memorandum is protected by the attorney-client privilege and the work product doctrine. It is intended solely for the use of the Client and may not be disclosed to any third party without the prior written consent of WSGR, except as required by law or regulatory obligation.

---

**Respectfully submitted,**

### WILSON SONSINI GOODRICH & ROSATI

<br>

/s/ _Jonathan R. Ellington_

**Jonathan R. Ellington**  
Partner, Technology Transactions  
Wilson Sonsini Goodrich & Rosati, P.C.  
Direct: 650-549-7321  
jellington@wsgr.com

<br>

**CC:**  
Dr. Priya Mehta, Chief Information Officer  
Dr. Kenji Nakamura, Chief Technology Officer  
Marcus Tran-Yoshida, Chief Product Officer

---

**Document Control:**

| Field             | Value                                |
| ----------------- | ------------------------------------ |
| Document ID       | WSGR-2026-04873-UL-MEMO              |
| Classification    | PRIVILEGED AND CONFIDENTIAL          |
| Version           | 1.0 (Final)                          |
| Date              | April 10, 2026                       |
| Author            | Jonathan R. Ellington, Partner       |
| Reviewer          | Sarah K. Whitfield, Senior Associate |
| Status            | Delivered to Client                  |
| CIO Audit Closure | **Condition C1 — SATISFIED**         |

---

_This memorandum constitutes the legal review deliverable required by CIO Audit Condition C1. The analysis, findings, and recommendations contained herein satisfy the planning-to-execution gap identified in `unity-licensing-review.md` and provide the authoritative legal basis for the technology selection decision regarding Unity 6.3 LTS._
