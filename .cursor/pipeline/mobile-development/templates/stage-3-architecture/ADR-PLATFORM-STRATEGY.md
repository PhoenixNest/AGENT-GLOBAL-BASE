# ADR-NNN: Platform Strategy

| Metadata          | Value                                                                     |
| ----------------- | ------------------------------------------------------------------------- |
| **ADR Number**    | ADR-NNN                                                                   |
| **Title**         | Platform Strategy — [Project Name]                                        |
| **Status**        | Proposed                                                                  |
| **Decision Date** | YYYY-MM-DD                                                                |
| **Authors**       | CTO (Dr. Kenji Nakamura), Platform Leads                                  |
| **Reviewers**     | CIO (Dr. Priya Mehta), CSO (Dr. Sarah Chen), VP Mobile (Marcus Andersson) |
| **Stage**         | 3 — Architecture                                                          |
| **Category**      | Platform / Architecture                                                   |

---

## Decision Statement

**Selected Approach:** [Native Dual-Track | KMP Cross-Platform | Flutter Cross-Platform]

> KMP and Flutter are mutually exclusive — exactly one cross-platform approach is selected, or native dual-track is chosen. Single-platform projects (Android-only or iOS-only) do not require this ADR.

---

## Context

Brief description of the project, its goals, and why the platform strategy decision is needed at this stage.

---

## Options Considered

| Option                 | Description                             | Pros                                                       | Cons                                                              |
| ---------------------- | --------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------- |
| Native Dual-Track      | Separate Swift/Kotlin codebases         | Platform-native UX, highest quality, lowest vendor lock-in | Highest cost, two codebases to maintain                           |
| KMP Cross-Platform     | Shared Kotlin business logic, native UI | 60-75% code sharing, platform-native UI, JetBrains-backed  | KMP iOS target maturity risk, C interop attack surface            |
| Flutter Cross-Platform | Single Dart codebase, Skia rendering    | 85-95% code sharing, single codebase                       | Google vendor lock-in, non-native UI rendering, younger ecosystem |

---

## Rationale

Why the selected approach was chosen over alternatives. Include team skills, time-to-market considerations, code sharing targets, and performance requirements.

---

## Trade-Offs

### What is Gained

- [List specific benefits]

### What is Sacrificed

- [List specific trade-offs vs. alternatives]

---

## TCO Projection (24-Month)

| Cost Dimension                     | Selected Approach | Alternative (Native) | Delta  |
| ---------------------------------- | ----------------- | -------------------- | ------ |
| **Engineering headcount**          | X FTEs            | Y FTEs               | +/- Z  |
| **SDK update cost**                | $X per quarter    | $Y per quarter       | +/- Z% |
| **Platform-specific feature cost** | $X per feature    | $Y per feature       | +/- Z% |
| **Total estimated 24-month cost**  | $X                | $Y                   | +/- Z% |

> Prepared by CIO with input from VP Mobile and Platform Leads.

---

## Vendor Lock-In Risk Matrix

| Risk Factor                               | Assessment                                                  | Mitigation        |
| ----------------------------------------- | ----------------------------------------------------------- | ----------------- |
| **Framework abandonment**                 | [Assess: KMP → JetBrains; Flutter → Google]                 | [Mitigation plan] |
| **Migration cost if switching to native** | [Estimate % of code reusable: KMP ~60-70%, Flutter ~10-20%] | [Mitigation plan] |
| **Open-source dependency risk**           | [Assess ecosystem maturity]                                 | [Mitigation plan] |
| **Exit strategy**                         | [Conditions that trigger reconsideration]                   | [Rollback plan]   |

---

## Performance SLA Alignment

| SLA                     | PRD Requirement | Selected Approach Can Meet? | Evidence / Risk |
| ----------------------- | --------------- | --------------------------- | --------------- |
| Cold start < 2s         | [Yes/No]        | [Assessment]                |
| Frame rate 60fps        | [Yes/No]        | [Assessment]                |
| Memory < 150MB          | [Yes/No]        | [Assessment]                |
| Network payload < 500KB | [Yes/No]        | [Assessment]                |

---

## Store & Compliance Implications

| Item                                       | Assessment                          | Mitigation   |
| ------------------------------------------ | ----------------------------------- | ------------ |
| App Store Review Guidelines compatibility  | [Any concerns with chosen approach] | [Mitigation] |
| Google Play Developer Policy compatibility | [Any concerns]                      | [Mitigation] |
| In-app purchase requirements               | [Platform-specific considerations]  | [Mitigation] |
| Background execution permissions           | [Platform-specific considerations]  | [Mitigation] |

---

## Team Capability Assessment

| Role                | Assigned           | Capability            | Gap                               |
| ------------------- | ------------------ | --------------------- | --------------------------------- |
| Android Lead        | Kofi Asante-Mensah | Strong native Android | [Any KMP/Flutter training needed] |
| iOS Lead            | Seo-Yeon Park      | Strong native iOS     | [Any KMP/Flutter training needed] |
| Cross-Platform Lead | Mei-Ling Johansson | KMP + Flutter         | [Capacity constraints]            |
| KMP Engineers       | [List names]       | [Skill assessment]    | [Training needed]                 |
| Flutter Engineers   | [List names]       | [Skill assessment]    | [Training needed]                 |

> Note: Current KMP-capable roster: Mei-Ling + Dmitri + Fatima (3 engineers). Plan assumes 5-6 for PRIMARY track. Gap of 2-3 engineers. Mitigation: borrow Priya Narayanan + Sofia Rezende from Android track.

---

## STRIDE-Based Threat Model

> Authored by Security Architect (Natalia Petrova), reviewed by CSO (Dr. Sarah Chen).

| Threat Category            | Assessment                                   | Mitigation |
| -------------------------- | -------------------------------------------- | ---------- |
| **Spoofing**               | [Identity/authentication risks per platform] | [Controls] |
| **Tampering**              | [Code/data integrity risks]                  | [Controls] |
| **Repudiation**            | [Logging/audit risks]                        | [Controls] |
| **Information Disclosure** | [Data exposure risks]                        | [Controls] |
| **Denial of Service**      | [Availability risks]                         | [Controls] |
| **Elevation of Privilege** | [Authorization risks]                        | [Controls] |

**Platform-specific attack surface notes:**

- **KMP:** C interop bridge between Kotlin/Native and iOS APIs is additional attack surface. Keychain access via platform adapter.
- **Flutter:** Dart VM runtime, platform channel serialization, third-party crypto packages (`flutter_secure_storage`, `pointycastle`) require independent security audit.
- **Native:** Dual implementation doubles security review burden but each platform's security model is mature and well-understood.

---

## Track Activation Mapping

Based on the selected platform strategy, the following track configuration is activated:

| Track                    | Status                   | Engineers | Lead               |
| ------------------------ | ------------------------ | --------- | ------------------ |
| Track A (Android)        | [FULL / LIGHT / Dormant] | [N]       | Kofi Asante-Mensah |
| Track B (iOS)            | [FULL / LIGHT / Dormant] | [N]       | Seo-Yeon Park      |
| Track C (Cross-Platform) | [PRIMARY / Dormant]      | [N]       | Mei-Ling Johansson |

**Track semantics:**

- **FULL** = End-to-end feature implementation
- **LIGHT** = Platform-specific integration only (UI glue, platform APIs, native dependencies)
- **PRIMARY** = Owns shared codebase producing binaries for multiple platforms
- **Dormant** = Reassigned to tech debt, test automation, cross-training, SDK migration prep

---

## Reassignment Plan for Dormant Tracks

| Dormant Track | Engineers Freed | Reassignment                                                        |
| ------------- | --------------- | ------------------------------------------------------------------- |
| [Track name]  | [N engineers]   | [Tech debt / Test automation / Cross-training / SDK migration prep] |

---

## Contract Versioning (KMP/Flutter only)

> The shared module's public API contract must be versioned. If it changes mid-Stage-5, all platform integration tracks must be notified immediately.

- **Contract version format:** `shared-module-vX.Y.Z`
- **Notification mechanism:** PR comment + PROGRESS.md update + CTO notification
- **Verification checkpoints:** 30% contract verification + 70% integration verification

---

## Decision

**Decision:** [Native Dual-Track | KMP Cross-Platform | Flutter Cross-Platform] is selected for [Project Name].

**Approved by:**

| Role | Name               | Signature | Date |
| ---- | ------------------ | --------- | ---- |
| CTO  | Dr. Kenji Nakamura |           |      |
| CIO  | Dr. Priya Mehta    |           |      |
| CSO  | Dr. Sarah Chen     |           |      |

**Stage 3 Gate Approval:** This ADR is **locked** upon Stage 3 gate approval. Any deviation requires a new ADR (Stage 3 re-entry). Switching between KMP and Flutter after Stage 3 requires a full stage rollback (Stage 3 re-entry, ADR re-authorship, Implementation Plan re-baseline).

---

## Consequences

### Positive

- [Expected benefits]

### Risks

- [Identified risks and mitigations]

### Future Review Triggers

- [Conditions that would trigger reconsideration, e.g., KMP iOS target deprecation, Flutter ecosystem collapse]

---

_ADR-NNN — Platform Strategy — [Project Name]_
_Status: [Proposed | Approved | Superseded | Deprecated]_
