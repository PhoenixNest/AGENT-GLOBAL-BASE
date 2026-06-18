# COPPA Assessment Plan — Children's Privacy Compliance

**Document Owner:** Dr. Priya Mehta, CIO
**Co-Owner:** Dr. Sarah Chen, CSO
**Audit Reference:** CIO Technology Audit, Item 7 (R3 — COPPA / Minors Data Compliance Failure)
**Condition:** C2 — Initiate COPPA compliance assessment
**Severity:** 🔴 P0
**Date:** April 12, 2026
**Status:** Proposed — pending assessment execution

---

## 1. Executive Summary

### 1.1 Risk Statement

**R3 — COPPA / Minors Data Compliance Failure** (🔴 P0, Owner: CIO + CSO)

The Casual Games Studio has no privacy engineer, no COPPA compliance assessment initiated, and a data architecture (PlayFab Events → Kafka → Data Lake → BI) that processes player data which may include minors' data. The FTC enforces COPPA with penalties up to **$50,120 per violation**, and each affected child constitutes a separate violation. For a game with 100,000 underage users, maximum exposure = **$5.012 billion**.

The CIO Technology Audit (Item 7) classified this as a **P0 risk requiring immediate action**, and the Strategic Brief mandated:

> "Engage legal counsel + CSO (Dr. Sarah Chen) immediately. COPPA compliance assessment must be completed by Week 3."

**Condition C2** from the CIO Audit requires this assessment to be initiated by **Week 3** of studio setup. Failure to address this risk before Stage 3 (Vertical Slice) entry means data collection architecture will be designed without COPPA awareness, creating costly retrofit requirements and potential legal liability.

### 1.2 Action Plan

1. **Conduct FTC multi-factor test** to determine whether the game is "directed to children" — this determination drives the entire compliance strategy.
2. **Audit all third-party SDKs** (PlayFab, AdMob, Unity Ads, Firebase, etc.) for data collection practices and COPPA compliance.
3. **Draft a privacy policy** tailored to the game's data practices and audience.
4. **Align data architecture** (PlayFab Events → Kafka → Data Lake → BI) with COPPA requirements, including data minimization, age gates, and deletion automation.
5. **Produce a compliance assessment report** with a definitive determination and implementation roadmap.

---

## 2. COPPA Applicability Analysis

### 2.1 FTC Multi-Factor Test

The FTC determines whether a service is "directed to children" using a multi-factor test. Below is the preliminary analysis for the Casual Games Studio's mini-game portfolio.

| Factor                                                            | Assessment for Casual Mini-Games                                                                                                                                                                           | COPPA Indicator   |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| **Subject matter** — Is the content child-oriented?               | Casual mini-games (puzzles, matching, simple arcade) are enjoyed by all ages. Content is non-violent, non-mature. Not explicitly child-oriented, but not adult-oriented either.                            | ⚠️ Neutral        |
| **Visual style** — Cartoons, bright colors, animated characters?  | Casual mini-games typically use bright colors, simple cartoon visuals, and animated characters. This is standard for the genre and appeals to all ages, but may be perceived as child-oriented by the FTC. | ⚠️ Likely Yes     |
| **Language** — Child-directed language?                           | Game text is expected to be simple, clear, and family-friendly. No profanity, no complex vocabulary. This is standard for casual games but may be interpreted as child-directed.                           | ⚠️ Likely Yes     |
| **Advertising** — Child-directed advertising?                     | If the game uses behavioral advertising (AdMob, Unity Ads), the ad content served may include child-directed ads. This is a significant risk factor.                                                       | ⚠️ To be assessed |
| **Empirical evidence** — Actual audience data?                    | No empirical data yet — studio is pre-launch. Post-launch analytics will provide this data.                                                                                                                | ❓ Unknown        |
| **Age of models/characters** — Are characters children?           | Depends on game art direction. If characters are cartoon animals, fantasy creatures, or abstract shapes, this may lean child-oriented. If characters are adults or neutral, less so.                       | ⚠️ To be assessed |
| **Child-oriented celebrities or voices** — Appealing to children? | Unlikely for casual mini-games unless specific IP partnerships are pursued.                                                                                                                                | ❌ Likely No      |

### 2.2 Preliminary Determination

**Determination: Mixed Audience — Leans Toward "Directed to Children"**

**Confidence Level: 65%**

**Rationale:**

Casual mini-games occupy a gray area in the FTC's framework. The visual style (bright colors, cartoon graphics, simple animations) and language (simple, family-friendly text) strongly align with child-oriented content. However, the subject matter (puzzles, matching games, arcade mechanics) is genuinely enjoyed by all age groups, and the studio's stated target audience is "all ages 12+."

**Key insight from the COPPA reference document:**

> "For casual mini-games: If your game uses cartoon art, simple mechanics, bright colors, or family-friendly themes, it is **likely** to be classified as child-directed by the FTC's test, even if your stated target audience is all ages."

The FTC has consistently held that **stated intent is not determinative** — the actual content and its appeal to children matters more than the developer's stated target audience. Given the visual and language factors, the preliminary determination is that the games **will likely be classified as directed to children** unless specific design choices are made to signal an older audience.

### 2.3 Recommended Classification Strategy

The studio has two viable paths:

| Path                                        | Strategy                                                                                                                                                                                              | Risk Level                                        | Effort |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ------ |
| **A: Accept COPPA applicability**           | Design all games as COPPA-compliant from Day 1. Set age rating to 4+/9+. Implement parental consent, data minimization, and deletion mechanisms.                                                      | Low (fully compliant)                             | High   |
| **B: Design to avoid COPPA classification** | Set age rating to 12+. Avoid child-oriented art styles, characters, and themes. Disable behavioral advertising. State clearly that the game is not directed to children under 13. Implement age gate. | Medium (FTC may still classify as child-directed) | Medium |

**Recommendation: Path A — Accept COPPA applicability.**

The casual mini-game genre is inherently appealing to children, and attempting to design around COPPA classification is a legal risk that is difficult to eliminate. The FTC's multi-factor test is applied holistically, and even if individual factors are addressed, the cumulative effect may still trigger COPPA. Full compliance is the safer, more sustainable approach.

---

## 3. Compliance Assessment Plan

### 3.1 Based on Preliminary Determination (Mixed Audience — Leans "Directed to Children")

The studio should implement a **hybrid compliance approach** that treats all users as potentially under 13 until an age gate confirms otherwise. This is the most defensible position under COPPA.

### 3.2 Full COPPA Compliance Plan

| Requirement                      | Implementation                                                                                                                                                                       | Owner             | Timeline |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- | -------- |
| **Verifiable parental consent**  | Implement age gate on first launch. If user indicates < 13, block data collection until parental consent is obtained (credit card verification, signed consent form, or video call). | CSO + Engineering | Week 4–6 |
| **Privacy policy**               | Publish comprehensive privacy policy specifically addressing children's data. Accessible from app store listing and in-app Settings screen.                                          | CSO + Legal       | Week 3–4 |
| **Data minimization**            | Collect only data strictly necessary for gameplay. Do not collect device ID, precise location, or behavioral data from users under 13.                                               | CIO + CSO         | Week 3–4 |
| **No conditional participation** | Do not require children to provide more information than necessary. No "give us your email to play."                                                                                 | CPO + CSO         | Week 3–4 |
| **Parental rights**              | Provide mechanism for parents to review, delete, and refuse further collection of their child's data. Parental contact email and process documented.                                 | CSO + Legal       | Week 5–6 |
| **Data security**                | Encrypt all children's data at rest and in transit. Implement access controls and retention limits.                                                                                  | CSO + CTO         | Week 4–5 |
| **Data retention limits**        | Automatic deletion of children's data after 12 months of inactivity. Retention policy documented and automated.                                                                      | CIO + CTO         | Week 5–6 |
| **No behavioral advertising**    | Disable personalized/targeted ads for all users. Use only contextual (non-targeted) ads. Comply with Google Play Families Ads Program.                                               | CSO + CTO         | Week 4–5 |

### 3.3 GDPR-K Alignment

| Requirement                         | Implementation                                                                  | Owner             | Timeline |
| ----------------------------------- | ------------------------------------------------------------------------------- | ----------------- | -------- |
| **Age of consent (EU)**             | Set to 16 (highest EU threshold) to ensure compliance across all member states. | CSO + Legal       | Week 4   |
| **Privacy notice (child-friendly)** | Create simplified, child-readable version of privacy policy.                    | CDO + CSO         | Week 5   |
| **Parental consent (EU)**           | Same mechanism as COPPA, applied to EU users under 16.                          | CSO + Engineering | Week 5–6 |

---

## 4. SDK Data Practice Audit

### 4.1 Third-Party SDK Inventory

| SDK                            | Purpose                                           | Data Collection Types                                                     | COPPA Compliance Status                                   | Google Play Families Compliance         | Recommended Actions                                                                                                                                      |
| ------------------------------ | ------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PlayFab**                    | Backend services (auth, economy, data, analytics) | Player ID, session data, game events, custom data, device info            | ⚠️ Configurable — must be configured for COPPA compliance | ⚠️ Requires configuration               | 1. Enable PlayFab's COPPA-compliant mode. 2. Disable device ID collection for users < 13. 3. Implement data retention policy in PlayStream.              |
| **AdMob**                      | Advertising                                       | Device ID (GAID), ad interactions, approximate location, app usage        | ⚠️ COPPA mode available                                   | ✅ Families-compliant mode available    | 1. Enable `tagForChildDirectedTreatment(true)`. 2. Disable personalized ads for all users. 3. Use only contextual ad placement.                          |
| **Unity Ads**                  | Advertising                                       | Device ID (IDFA/GAID), ad interactions, approximate location              | ⚠️ COPPA mode available                                   | ⚠️ Requires configuration               | 1. Enable COPPA-compliant mode in Unity Ads SDK. 2. Disable interest-based targeting. 3. Verify ad creative is family-safe.                              |
| **Firebase**                   | Analytics, Crash Reporting, Remote Config         | App usage, crash data, device info, approximate location, user properties | ⚠️ Configurable — must be configured for COPPA compliance | ⚠️ Requires configuration               | 1. Disable advertising ID collection. 2. Disable Firebase Analytics for users < 13 (or use anonymized mode). 3. Implement data deletion API integration. |
| **Unity Engine**               | Game runtime, analytics                           | Device info, OS version, Unity Analytics events (if enabled)              | ⚠️ Configurable                                           | ⚠️ Requires configuration               | 1. Disable Unity Analytics or enable anonymized mode. 2. Do not collect persistent identifiers for users < 13.                                           |
| **Google Play Games Services** | Achievements, leaderboards, cloud saves           | Player ID, game progress, social graph                                    | ⚠️ Requires age-gated access                              | ✅ Compliant if age-rated appropriately | 1. Integrate with age gate. 2. Disable social features for users < 13.                                                                                   |
| **Apple Game Center**          | Achievements, leaderboards                        | Apple ID, game progress                                                   | ⚠️ Requires age-gated access                              | N/A (Apple platform)                    | 1. Integrate with age gate. 2. Disable social features for users < 13.                                                                                   |

### 4.2 SDK Audit Summary

**Critical Findings:**

1. **AdMob and Unity Ads are the highest-risk SDKs** — both collect advertising identifiers (GAID/IDFA), which are classified as "personal information" under COPPA even when collected alone. These SDKs **must** have COPPA-compliant modes enabled before any data collection begins.

2. **Firebase Analytics collects behavioral data** by default, which when combined with persistent identifiers constitutes personal information under COPPA. Firebase must be configured to either (a) disable analytics for users < 13, or (b) operate in fully anonymized mode.

3. **PlayFab's COPPA compliance is configurable but not automatic** — the studio must explicitly configure PlayFab to disable device ID collection, enforce data retention limits, and implement parental consent workflows.

4. **No SDK on the inventory is "COPPA-compliant out of the box"** — every SDK requires explicit configuration to meet COPPA requirements. This configuration must be documented, tested, and verified before launch.

### 4.3 SDK Vetting Checklist (Per CIO Audit Item 7, R10)

| Check                                        | Status      | Notes                                              |
| -------------------------------------------- | ----------- | -------------------------------------------------- |
| SDK privacy policy reviewed                  | Not started | Must be completed for each SDK                     |
| SDK COPPA/Families compliance mode verified  | Not started | Must be tested in staging environment              |
| SDK data collection minimized for users < 13 | Not started | Configuration required per SDK                     |
| SDK cross-compatibility assessed             | Not started | Per CIO Audit Item 7, R10 — SDK conflicts possible |
| SDK removal plan documented                  | Not started | Fallback plan if SDK is found non-compliant        |

---

## 5. Privacy Policy Draft

### 5.1 Privacy Policy Template

```markdown
# Privacy Policy — [Game Name]

**Last Updated:** [Date]
**Effective Date:** [Date]

## 1. Introduction

[Studio Name] ("we," "our," or "us") respects your privacy and is committed to protecting the personal information of all players, including children. This Privacy Policy explains what information we collect, how we use it, and your rights regarding your data.

**Important Notice Regarding Children:** Our games may be played by users of all ages. We comply with the Children's Online Privacy Protection Act (COPPA) and the General Data Protection Regulation (GDPR) as they apply to children's data. If you are under 13 (or under 16 in the European Economic Area), please read the "Children's Privacy" section carefully.

## 2. Information We Collect

### 2.1 Information You Provide

- **Account Information:** Username, email address (if you create an account).
- **Parental Consent Information:** If you are a parent providing consent for a child under 13, we may collect your email address for verification purposes.

### 2.2 Information Collected Automatically

- **Gameplay Data:** Game progress, achievements, scores, in-game purchases, and play session duration.
- **Device Information:** Device type, operating system version, language settings, and app version.
- **Usage Analytics:** App interaction data, feature usage, and crash reports (anonymized for users under 13).
- **Advertising Data:** If you are 13 or older, we may show ads. We do not collect advertising identifiers (GAID/IDFA) from users under 13.

### 2.3 Information We DO NOT Collect from Children Under 13

- Device advertising identifiers (GAID, IDFA)
- Precise geolocation
- Persistent identifiers not necessary for gameplay
- Behavioral data combined with persistent identifiers
- Photos, videos, or audio recordings
- Contact information (email, phone) without parental consent

## 3. How We Use Your Information

We use the information we collect to:

- Provide, operate, and improve our games.
- Process in-game purchases and manage your account.
- Send service-related communications (e.g., password resets, policy updates).
- Analyze gameplay to improve game design and fix bugs.
- Comply with legal obligations.

**For users under 13:** We use only the minimum information necessary to provide the game experience. We do not use children's data for marketing, behavioral advertising, or profiling.

## 4. Third-Party Services and SDKs

Our games use the following third-party services:

| Service             | Purpose                                     | Data Shared                                       | COPPA-Compliant Mode                           |
| ------------------- | ------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- |
| PlayFab (Microsoft) | Backend services, authentication, game data | Player ID, game events, session data              | Yes — configured for COPPA compliance          |
| AdMob (Google)      | Advertising (13+ only)                      | Anonymized ad interaction data                    | Yes — child-directed treatment enabled         |
| Unity Ads           | Advertising (13+ only)                      | Anonymized ad interaction data                    | Yes — COPPA mode enabled                       |
| Firebase (Google)   | Analytics, crash reporting                  | Anonymized usage data (under 13); full data (13+) | Yes — configured for age-based data collection |

These third-party services have their own privacy policies. We require all SDKs to operate in COPPA-compliant mode for users under 13.

## 5. Data Sharing

We do not sell, trade, or rent personal information to third parties. We may share data with:

- **Service Providers:** PlayFab, AdMob, Unity Ads, and Firebase — only to the extent necessary to provide game services, and only in COPPA-compliant mode for users under 13.
- **Legal Requirements:** If required by law, regulation, or legal process.
- **Business Transfers:** In the event of a merger, acquisition, or sale of assets, user data may be transferred. Users will be notified of any such change.

## 6. Parental Rights

If you are a parent or guardian of a child under 13, you have the following rights:

- **Review:** Request to review the personal information we have collected from your child.
- **Delete:** Request deletion of your child's personal information.
- **Refuse:** Refuse further collection or use of your child's personal information.
- **Revoke Consent:** Revoke previously provided parental consent at any time.

To exercise these rights, contact us at: **[privacy@studiostudio.com]**

If we learn that we have collected personal information from a child under 13 without verifiable parental consent, we will delete that information promptly.

## 7. Data Retention and Deletion

- **Users 13 and older:** We retain your data for as long as your account is active or as needed to provide game services. You may request deletion at any time.
- **Users under 13:** We automatically delete children's data after **12 months of inactivity**. Parents may request earlier deletion at any time.
- **Upon account deletion:** All associated personal information is permanently deleted from our systems within 30 days.

## 8. Data Security

We implement industry-standard security measures to protect your data:

- Encryption of data in transit (TLS 1.3) and at rest (AES-256).
- Access controls limiting data access to authorized personnel only.
- Regular security audits and vulnerability assessments.
- Compliance with OWASP Mobile Application Security Verification Standard (MASVS).

## 9. International Data Transfers

If you are located in the European Economic Area (EEA), your data may be transferred to and processed in countries outside the EEA. We ensure appropriate safeguards are in place, including Standard Contractual Clauses, to protect your data.

## 10. Changes to This Privacy Policy

We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the updated policy in the game's Settings screen and on our website. Continued use of the game after changes constitutes acceptance of the updated policy.

## 11. Contact Us

If you have questions about this Privacy Policy or our data practices, please contact:

- **Email:** privacy@studiostudio.com
- **Address:** [Studio Name], [Address]
- **Data Protection Officer:** [DPO Name], dpo@studiostudio.com

**For parents:** If you believe your child has provided personal information without your consent, please contact us immediately at privacy@studiostudio.com, and we will take steps to delete the information.
```

### 5.2 Privacy Policy Placement

| Platform        | Requirement                             | Implementation                                               |
| --------------- | --------------------------------------- | ------------------------------------------------------------ |
| **App Store**   | Privacy policy URL in App Store Connect | Submit URL during app submission                             |
| **Google Play** | Privacy policy URL in Play Console      | Submit URL in Data Safety section                            |
| **In-app**      | Accessible from Settings screen         | "Privacy Policy" button in Settings → links to hosted policy |

---

## 6. Data Architecture COPPA Alignment

### 6.1 Current Data Pipeline Architecture

```
PlayFab Events → Kafka → Data Lake (S3/Azure Blob) → BI Dashboards
```

This pipeline was designed for analytics and business intelligence purposes. Under COPPA, every component must be COPPA-aware.

### 6.2 Data Minimization Principles

| Principle                          | Implementation                                                                                                                           |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Collect only what is necessary** | For users < 13: collect only gameplay data (scores, progress, session length). No device ID, no location, no behavioral data.            |
| **Anonymize at source**            | PlayStream events for users < 13 must have all persistent identifiers stripped before entering the Kafka pipeline.                       |
| **Separate pipelines by age**      | Maintain separate data streams for users < 13 and users 13+. Children's data must never be combined with behavioral or advertising data. |
| **No cross-referencing**           | Children's data must not be joinable with any other dataset that could re-identify the child.                                            |

### 6.3 Age Gate Implementation Plan

| Component               | Design Specification                                                                                                                                                                                                      | Owner       |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| **First-launch prompt** | On first launch, display age prompt: "How old are you?" with a simple numeric selector. No personal information collected at this stage.                                                                                  | CDO + CPO   |
| **If age ≥ 13**         | Proceed with normal data collection. Store age flag (not exact date of birth) in PlayFab player data.                                                                                                                     | Engineering |
| **If age < 13**         | Enter COPPA-compliant mode: (a) Block all behavioral data collection. (b) Display parental consent flow. (c) If consent not obtained, restrict to gameplay-only mode with no data persistence beyond the current session. | Engineering |
| **Age flag storage**    | Store only a boolean flag (`is_under_13: true/false`) in PlayFab player data. Do NOT store exact date of birth.                                                                                                           | Engineering |
| **Re-verification**     | Re-verify age annually or if the user's age flag is inconsistent with gameplay patterns.                                                                                                                                  | Engineering |

### 6.4 Parental Consent Flow Design

```
┌──────────────────────────────────────────────────────────────────┐
│                    Parental Consent Flow                         │
│                                                                  │
│  Child (< 13) detected                                           │
│       ↓                                                          │
│  Display: "We need a parent's permission to save your progress." │
│       ↓                                                          │
│  Parent provides email                                           │
│       ↓                                                          │
│  Send consent request email with:                                │
│    - Link to Privacy Policy                                      │
│    - Description of data collected                               │
│    - Consent button + decline button                             │
│       ↓                                                          │
│  Parent clicks "Consent"                                         │
│       ↓                                                          │
│  Verify consent (credit card $0.01 charge OR signed form)        │
│       ↓                                                          │
│  Consent recorded → Enable full gameplay features                │
│       ↓                                                          │
│  Parent can revoke consent at any time via email link            │
│       ↓                                                          │
│  If consent revoked → Delete child's data, revert to session-only│
└──────────────────────────────────────────────────────────────────┘
```

### 6.5 Data Retention/Deletion Automation Plan

| Pipeline Component            | COPPA Requirement                    | Implementation                                                                                                                                                |
| ----------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PlayFab Player Data**       | Delete after 12 months inactivity    | PlayStream event triggers Azure Function to delete player data after 12-month inactivity. Parental deletion requests processed within 7 days.                 |
| **Kafka Events**              | No persistent identifiers for < 13   | Kafka consumer strips identifiers before writing to Data Lake. Events for users < 13 are anonymized at the producer level.                                    |
| **Data Lake (S3/Azure Blob)** | Separate storage for children's data | Children's data stored in isolated bucket/container with stricter access controls. Automatic deletion after 12 months via lifecycle policy.                   |
| **BI Dashboards**             | No individual child data in reports  | BI dashboards aggregate children's data only. No individual-level queries on children's data. Access restricted to authorized analysts.                       |
| **Deletion API**              | Parental deletion requests           | Implement PlayFab `DeleteMasterPlayerAccount` API integration. Deletion cascades to Kafka, Data Lake, and BI systems. Automated confirmation email to parent. |

### 6.6 COPPA Compliance Architecture Checklist

| Check                                                  | Status      | Owner               |
| ------------------------------------------------------ | ----------- | ------------------- |
| Age gate implemented at first launch                   | Not started | Engineering         |
| COPPA-compliant mode activated for users < 13          | Not started | Engineering         |
| Persistent identifiers stripped from children's events | Not started | Backend Engineering |
| Separate data storage for children's data              | Not started | Data Engineering    |
| Automated deletion after 12-month inactivity           | Not started | Data Engineering    |
| Parental consent flow implemented                      | Not started | Engineering         |
| Parental deletion request mechanism                    | Not started | Engineering         |
| BI dashboards exclude individual children's data       | Not started | Data Analyst        |
| SDK COPPA modes enabled and tested                     | Not started | CSO + Engineering   |
| Privacy policy published and accessible                | Not started | CSO + Legal         |

---

## 7. Timeline — Week-by-Week Milestones

### Week 3 (April 27 – May 3, 2026) — Assessment Initiation

| Day | Milestone                                     | Owner     | Deliverable                          |
| --- | --------------------------------------------- | --------- | ------------------------------------ |
| 1   | CIO + CSO joint kickoff meeting               | CIO + CSO | Assessment scope confirmed           |
| 2–3 | FTC multi-factor test completed (Section 2)   | CIO + CSO | Preliminary determination documented |
| 4   | SDK inventory compiled (Section 4)            | CSO       | SDK audit table completed            |
| 5   | **Gate: C2 condition — assessment initiated** | CIO + CSO | ✅ COPPA assessment plan approved    |

### Week 4 (May 4–10, 2026) — SDK Audit & Privacy Policy

| Day | Milestone                                                      | Owner             | Deliverable                 |
| --- | -------------------------------------------------------------- | ----------------- | --------------------------- |
| 1–2 | SDK COPPA compliance mode testing (AdMob, Unity Ads, Firebase) | CSO + Engineering | SDK compliance test results |
| 3   | Privacy policy draft completed (Section 5)                     | CSO + Legal       | Draft privacy policy        |
| 4   | Legal review of privacy policy                                 | Legal Counsel     | Reviewed privacy policy     |
| 5   | Age gate design finalized                                      | CDO + CPO         | Age gate UX specification   |

### Week 5 (May 11–17, 2026) — Data Architecture Alignment

| Day | Milestone                                      | Owner               | Deliverable                 |
| --- | ---------------------------------------------- | ------------------- | --------------------------- |
| 1–2 | Data minimization configuration in PlayFab     | Backend Engineering | PlayFab COPPA config        |
| 3   | Kafka producer anonymization logic implemented | Backend Engineering | Code review required        |
| 4   | Data Lake lifecycle policy for children's data | Data Engineering    | Lifecycle policy configured |
| 5   | Parental consent flow prototype                | Engineering         | Prototype for review        |

### Week 6 (May 18–24, 2026) — Integration Testing & Sign-Off

| Day | Milestone                                                                             | Owner             | Deliverable                             |
| --- | ------------------------------------------------------------------------------------- | ----------------- | --------------------------------------- |
| 1–2 | End-to-end COPPA compliance testing (age gate → consent → data collection → deletion) | Engineering + CSO | Test results                            |
| 3   | SDK compliance verification (all SDKs in COPPA mode)                                  | CSO               | SDK compliance sign-off                 |
| 4   | Final compliance assessment report                                                    | CIO + CSO         | COPPA Assessment Report                 |
| 5   | **Gate: C2 condition satisfied**                                                      | CIO + CSO         | ✅ COPPA compliance assessment complete |

### Post-Assessment (Ongoing)

| Milestone                      | Frequency                                | Owner       | Notes                                 |
| ------------------------------ | ---------------------------------------- | ----------- | ------------------------------------- |
| SDK audit (new SDK additions)  | Per SDK                                  | CSO         | Every new SDK must pass COPPA review  |
| Privacy policy review          | Every 6 months or after material changes | CSO + Legal | Update for new data practices         |
| COPPA/GDPR-K compliance review | Annually or after game update            | CSO + Legal | Full compliance audit                 |
| Data retention audit           | Annually                                 | CSO         | Verify deletion automation is working |
| Age rating review              | After any content change                 | CSO         | Ensure rating still matches content   |

---

## 8. Escalation Triggers

| Trigger                                              | Action                                                                    | Escalation To       |
| ---------------------------------------------------- | ------------------------------------------------------------------------- | ------------------- |
| FTC issues guidance that changes COPPA applicability | Re-assess determination, update compliance plan                           | CIO + CSO → C-Suite |
| SDK vendor discontinues COPPA-compliant mode         | Replace SDK immediately, notify users                                     | CSO → CTO           |
| Parental complaint received                          | Investigate within 48 hours, remediate if valid                           | CSO + Legal         |
| Data breach involving children's data                | Notify FTC within 24 hours, notify affected parents, engage legal counsel | CSO → CIO → CEO     |
| PlayFab changes data collection policies             | Re-assess data pipeline COPPA alignment                                   | CIO + CSO           |

---

**Approved By:** Dr. Priya Mehta, CIO
**Co-Approved By:** Dr. Sarah Chen, CSO
**Date:** April 12, 2026
**Next Review:** April 27, 2026 (Week 3 assessment kickoff)
