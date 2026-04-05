# OWASP MASVS Mastery — Training Curriculum

**Owner:** Dr. Sarah Chen, Chief Security Officer
**Department:** Cyberspace Security → Engineering Enablement
**Framework:** OWASP Mobile Application Security Verification Standard v2024.05
**Probation Window:** 30 calendar days from enrollment date

---

## Curriculum Overview

| Track | Audience | Level | Duration | Verification |
|-------|----------|-------|----------|-------------|
| **Track A — Full Mastery** | James Wright (Lead Security Engineer) | Certification-grade | 4 weeks, ~40 hours | Written exam + practical audit exercise |
| **Track B — Framework Review** | Natalia Petrova (Security Architect) | Architecture integration | 4 weeks, ~20 hours | Threat model deliverables + CSO review session |
| **Track C — Executive Briefing** | David Okonkwo (VP Platform Engineering) | Strategic overview | 1 session, 2 hours | Comprehension check (oral + written Q&A) |

---

## 1. Module Objectives

### Track A — James Wright (Lead Security Engineer) — Full Mastery

Upon completion, James must be able to:

1. **Recite** all eight MASVS verification categories (V1–V8) and explain the security domain each covers, including all individual requirements at L1 and L2 levels.
2. **Perform** a complete MASVS-based security audit of an iOS or Android application, producing a verification results document with per-requirement pass/fail/na ratings and evidence citations.
3. **Operate** MobSF (Mobile Security Framework) for automated SAST/DAST analysis and interpret its MASVS-mapped output to produce a remediation roadmap.
4. **Instrument** an application with Frida for dynamic analysis: hook methods, intercept cryptographic operations, bypass SSL pinning, and detect runtime instrumentation.
5. **Map** identified vulnerabilities to CVSS v3.1 scores and correlate them with MASVS requirements to produce a prioritized remediation plan.
6. **Write** a MASVS-aligned Security Requirements Document (SRD) for a new mobile product, referencing specific V-category requirements as acceptance criteria.

### Track B — Natalia Petrova (Security Architect) — Framework Review

Upon completion, Natalia must be able to:

1. **Navigate** the MASVS taxonomy and explain how each V-category maps to architectural decision points in a mobile application.
2. **Map** STRIDE threat categories to MASVS verification categories, producing a cross-reference matrix for any given mobile architecture.
3. **Conduct** a mobile threat modeling session using MASVS as the verification baseline, identifying which V-categories apply to each trust boundary and data flow.
4. **Integrate** MASVS requirements into the Stage 3 Architecture Review process (ADRs, TSD) so that security verification is a first-class concern in engineering packages.
5. **Produce** a MASVS gap analysis report for an existing application architecture, identifying which V-categories are covered, which are partially covered, and which are absent.

### Track C — David Okonkwo (VP Platform Engineering) — Executive Briefing

Upon completion, David must be able to:

1. **Explain** what OWASP MASVS is, why it matters to the platform, and the business impact of L1 vs. L2 compliance.
2. **Describe** how MASVS categories translate into platform security gates at Stages 1, 6, 8, and 10 of the development pipeline.
3. **Articulate** the resource investment required (tooling, personnel, timeline) for the engineering organization to achieve MASVS L1 compliance across all mobile products.
4. **Approve or challenge** a MASVS compliance roadmap presented by the CSO office, understanding trade-offs between security posture and delivery velocity.

---

## 2. Prerequisites

### Track A — James Wright

| Prerequisite | Verification Method |
|-------------|---------------------|
| 3+ years mobile security engineering experience (iOS or Android) | Resume review + HR confirmation |
| Familiarity with OWASP Top 10 (web) | CSO interview: 10-question verbal check |
| Basic understanding of cryptography (symmetric, asymmetric, hashing, certificates) | CSO interview: explain TLS handshake and key exchange |
| Command-line proficiency (bash, Python scripting) | Practical: run a MobSF scan from CLI |
| Access to a macOS or Linux workstation with Android Studio / Xcode installed | IT provision confirmed |

### Track B — Natalia Petrova

| Prerequisite | Verification Method |
|-------------|---------------------|
| 5+ years software architecture experience (any domain) | Resume review + HR confirmation |
| Familiarity with STRIDE or equivalent threat modeling methodology | CSO interview: walk through a STRIDE analysis |
| Understanding of mobile platform security models (iOS Keychain, Android Keystore) | CSO interview: compare iOS/Android secure storage |
| Access to architecture diagramming tools (draw.io, Lucidchart, or equivalent) | IT provision confirmed |

### Track C — David Okonkwo

| Prerequisite | Verification Method |
|-------------|---------------------|
| Current role as VP Platform Engineering | HR confirmation |
| No technical prerequisites — briefing is designed for executive-level strategic understanding | N/A |

---

## 3. Weekly Schedule (4 Weeks)

### TRACK A — James Wright (Full Mastery)

#### Week 1: MASVS Framework Overview + Mobile Threat Landscape

| Session | Topic | Duration | Format | Deliverable |
|---------|-------|----------|--------|-------------|
| A1.1 | **MASVS Introduction** — History, purpose, L1 vs. L2 vs. R levels, how MASVS fits into the SDLC | 90 min | Lecture + discussion | One-page summary: "Why MASVS matters to our org" |
| A1.2 | **V1: Architecture, Design & Threat Modeling** — All L1/L2 requirements, threat modeling integration | 120 min | Lecture + walkthrough | Completed V1 checklist against a reference app |
| A1.3 | **V2: Data Storage & Privacy** — All L1/L2 requirements, platform storage mechanisms, privacy implications | 120 min | Lecture + lab | Data storage audit checklist for iOS and Android |
| A1.4 | **Mobile Threat Landscape 2026** — Current attack vectors, notable breaches, trend analysis | 90 min | CSO-led briefing | Annotated bibliography of 5 recent mobile security incidents |
| A1.5 | **Tool Setup** — Install and configure MobSF, Frida, objection, Android emulator, iOS simulator | 120 min | Hands-on lab | Screenshot-verified setup report for all tools |

**Week 1 Total:** ~10.5 hours
**Week 1 Gate:** CSO reviews V1 checklist and tool setup report. Pass requires correct identification of ≥80% of V1 requirements in the reference app.

---

#### Week 2: MASVS V3–V4 Deep Dive + MobSF Practical

| Session | Topic | Duration | Format | Deliverable |
|---------|-------|----------|--------|-------------|
| A2.1 | **V3: Cryptography** — All L1/L2 requirements, key management, algorithm selection, secure random number generation, certificate validation | 150 min | Lecture + code review | Cryptographic implementation checklist (20 items) |
| A2.2 | **V4: Authentication & Session Management** — All L1/L2 requirements, biometric auth, session tokens, OAuth/OIDC flows, credential storage | 150 min | Lecture + lab | Auth flow threat model for a sample mobile API |
| A2.3 | **MobSF Deep Dive** — Static analysis, dynamic analysis, API testing, report interpretation, MASVS mapping in MobSF output | 180 min | Hands-on lab | Full MobSF scan report on Diva Android app with annotated findings |
| A2.4 | **MobSF → Remediation Roadmap** — Translating scan findings into prioritized engineering tasks, linking to MASVS requirements | 90 min | Workshop | Remediation roadmap document (prioritized backlog with MASVS references) |

**Week 2 Total:** ~9.5 hours
**Week 2 Gate:** CSO reviews MobSF scan report and remediation roadmap. Pass requires: (a) correct identification of ≥75% of known vulnerabilities in the sample app, (b) remediation items correctly mapped to MASVS V3/V4 requirements.

---

#### Week 3: MASVS V5–V8 Deep Dive + Frida Practical

| Session | Topic | Duration | Format | Deliverable |
|---------|-------|----------|--------|-------------|
| A3.1 | **V5: Network Communication** — All L1/L2 requirements, TLS configuration, certificate pinning, secure API design, data-in-transit protection | 120 min | Lecture + lab | Network security test plan (MITM, pinning bypass, replay attack scenarios) |
| A3.2 | **V6: Platform Interaction** — All L1/L2 requirements, IPC security, intents/URL schemes, keyboard cache, clipboard, screenshots, WebView security | 120 min | Lecture + lab | Platform interaction vulnerability checklist for iOS and Android |
| A3.3 | **V7: Code Quality & Build Settings** — All L1/L2 requirements, compiler flags, debug builds, third-party library management, SBOM | 90 min | Lecture + review | Build configuration security audit template |
| A3.4 | **V8: Resilience Against Reverse Engineering** — All L1/L2 requirements, obfuscation, anti-tampering, root/jailbreak detection, RASP | 120 min | Lecture + lab | Reverse engineering resistance assessment framework |
| A3.5 | **Frida Practical Lab** — Hooking Java/Kotlin methods, Objective-C/Swift method swizzling, SSL pinning bypass, crypto interception, custom script writing | 180 min | Hands-on lab | 3 custom Frida scripts: (1) hook auth method, (2) intercept crypto key, (3) bypass SSL pinning |
| A3.6 | **Objection Runtime Exploration** — Automated Frida-based analysis, file system exploration, keychain/keystore inspection | 90 min | Hands-on lab | Objection session transcript with findings documented |

**Week 3 Total:** ~12 hours
**Week 3 Gate:** CSO reviews Frida scripts and V5–V8 checklists. Pass requires: (a) all 3 Frida scripts execute successfully against the sample app, (b) V5–V8 checklists correctly assess ≥80% of known weaknesses in the sample app.

---

#### Week 4: Full Mobile Security Audit Exercise + Written Exam

| Session | Topic | Duration | Format | Deliverable |
|---------|-------|----------|--------|-------------|
| A4.1 | **Audit Exercise Briefing** — CSO provides a previously unseen mobile application (APK or IPA). James conducts a full MASVS audit. | 30 min | Briefing | N/A |
| A4.2 | **Audit Execution** — James performs static analysis (MobSF), dynamic analysis (Frida), manual review, and produces a complete MASVS verification report covering all V1–V8 categories. | 480 min | Independent work (2 full days) | Complete MASVS Verification Report with per-requirement ratings, evidence, and findings |
| A4.3 | **Audit Report Review** — CSO and James walk through the report together. CSO presents the ground-truth audit results for comparison. | 120 min | Review session | Delta analysis: James's findings vs. ground truth |
| A4.4 | **Written Examination** — Closed-book exam covering all V1–V8 categories, practical scenario analysis, and MASVS-to-SRD translation. | 120 min | Written exam | Completed exam (see Section 5 for passing criteria) |
| A4.5 | **Debrief & Certification Decision** — CSO provides feedback, discusses gaps, and makes pass/fail determination. | 60 min | 1:1 session | Certification decision documented |

**Week 4 Total:** ~13.5 hours
**Week 4 Gate:** Combined audit exercise + written exam results determine certification (see Section 5).

---

### TRACK B — Natalia Petrova (Framework Review)

#### Week 1: MASVS Taxonomy + STRIDE-to-MASVS Mapping

| Session | Topic | Duration | Format | Deliverable |
|---------|-------|----------|--------|-------------|
| B1.1 | **MASVS for Architects** — Framework structure, L1/L2/R levels, how MASVS maps to architectural decision points | 90 min | CSO 1:1 briefing | One-page architecture-MASVS alignment summary |
| B1.2 | **STRIDE-to-MASVS Mapping Exercise** — For each STRIDE category, identify corresponding MASVS V-categories and specific requirements | 120 min | Workshop | Completed STRIDE→MASVS cross-reference matrix |
| B1.3 | **Mobile Platform Security Models** — iOS security architecture (Secure Enclave, Keychain, ATS, code signing) and Android security architecture (SafetyNet/Play Integrity, hardware-backed keystore, SELinux) | 120 min | Lecture + discussion | Platform security model comparison document |

**Week 1 Total:** ~5.5 hours
**Week 1 Gate:** CSO reviews cross-reference matrix. Pass requires correct mapping of ≥80% of STRIDE categories to their primary MASVS V-categories.

---

#### Week 2: Mobile Threat Modeling — Scenario 1

| Session | Topic | Duration | Format | Deliverable |
|---------|-------|----------|--------|-------------|
| B2.1 | **Scenario 1 Briefing: Mobile Banking App** — Architecture overview, data flows, trust boundaries, regulatory context (PCI-DSS) | 60 min | Briefing | N/A |
| B2.2 | **Threat Modeling Session** — Identify assets, enumerate threats using STRIDE, map to MASVS V-categories, define verification criteria | 180 min | Independent work | Threat model document with MASVS-mapped verification requirements |
| B2.3 | **Review with CSO** — Walk through threat model, discuss gaps, refine MASVS mappings | 90 min | Review session | Revised threat model with CSO annotations |

**Week 2 Total:** ~5.5 hours
**Week 2 Gate:** CSO reviews threat model. Pass requires: (a) all trust boundaries identified, (b) ≥80% of relevant MASVS V-categories mapped to threats, (c) verification criteria defined for each mapped requirement.

---

#### Week 3: Mobile Threat Modeling — Scenarios 2 & 3

| Session | Topic | Duration | Format | Deliverable |
|---------|-------|----------|--------|-------------|
| B3.1 | **Scenario 2 Briefing: Social Messaging App** — E2E encryption, media handling, contact discovery, notification payloads | 60 min | Briefing | N/A |
| B3.2 | **Threat Modeling Session — Scenario 2** | 150 min | Independent work | Threat model document with MASVS mappings |
| B3.3 | **Scenario 3 Briefing: Enterprise MDM Client** — Device enrollment, policy enforcement, remote wipe, certificate provisioning | 60 min | Briefing | N/A |
| B3.4 | **Threat Modeling Session — Scenario 3** | 150 min | Independent work | Threat model document with MASVS mappings |
| B3.5 | **MASVS Gap Analysis Framework** — Develop a reusable template for conducting MASVS gap analysis on any application architecture | 90 min | Workshop | MASVS Gap Analysis Template (reusable artifact) |

**Week 3 Total:** ~8.5 hours
**Week 3 Gate:** CSO reviews both threat models and the gap analysis template. Pass requires same criteria as Week 2 for both scenarios, plus a functional, reusable template.

---

#### Week 4: MASVS Framework Review Session with CSO

| Session | Topic | Duration | Format | Deliverable |
|---------|-------|----------|--------|-------------|
| B4.1 | **Framework Integration Review** — How MASVS integrates into Stage 1 (SRD), Stage 3 (Architecture), Stage 6 (Code Review), Stage 8 (Integrity Verification), and Stage 10 (Release Readiness) | 90 min | CSO 1:1 session | MASVS Integration Playbook for the pipeline |
| B4.2 | **30-Day Output Review** — Review all deliverables from Weeks 1–3, discuss lessons learned, identify areas for continued development | 90 min | Review session | Personal development plan for post-probation period |
| B4.3 | **Framework Review Sign-off** — CSO evaluates overall competency and makes pass/fail determination | 60 min | Evaluation session | Framework Review Completion certificate |

**Week 4 Total:** ~4 hours
**Week 4 Gate:** Combined review of all deliverables determines framework review completion (see Section 5).

---

### TRACK C — David Okonkwo (VP Platform Engineering) — Executive Briefing

#### Single Session: 2-Hour MASVS Executive Briefing

| Segment | Topic | Duration | Format |
|---------|-------|----------|--------|
| C1 | **What is OWASP MASVS?** — Framework purpose, history, industry adoption, L1 vs. L2 vs. R levels | 20 min | CSO presentation |
| C2 | **The Eight Verification Categories** — High-level overview of V1–V8, what each protects, business relevance | 25 min | CSO presentation with examples |
| C3 | **MASVS in Our Pipeline** — How MASVS requirements map to Stages 1, 6, 8, and 10; current compliance posture; gap areas | 25 min | CSO presentation with company-specific data |
| C4 | **Resource Investment** — Tooling costs (MobSF, commercial tools), personnel requirements (security engineers, training), timeline to L1 compliance across all products | 20 min | CSO presentation with budget estimates |
| C5 | **Risk & Compliance Implications** — Regulatory alignment (GDPR, PCI-DSS), audit readiness, competitive advantage of MASVS certification | 15 min | CSO presentation |
| C6 | **Comprehension Check** — 10-question oral/written Q&A covering segments C1–C5 | 15 min | Interactive Q&A |

**Total Session:** 2 hours
**Verification:** Comprehension check (see Section 5).

---

## 4. Verification Methods

### Track A — James Wright

| Verification Component | Method | Weight |
|----------------------|--------|--------|
| **MASVS Verification Report** (Week 4 audit exercise) | Practical: Complete audit of unseen mobile application, scored against CSO ground-truth results | 40% |
| **Written Examination** (Week 4) | Closed-book: 50 questions covering all V1–V8 categories, scenario analysis, SRD translation | 35% |
| **Weekly Deliverables** (Weeks 1–3) | Quality assessment of checklists, MobSF reports, Frida scripts, remediation roadmaps | 15% |
| **Tool Proficiency** | Demonstrated ability to operate MobSF and Frida independently | 10% |

**Verification Schedule:**

- Weeks 1–3: CSO reviews deliverables within 48 hours of submission; provides written feedback
- Week 4 Day 3: Audit report review (1:1 walkthrough with CSO)
- Week 4 Day 4: Written examination (120 minutes, closed-book)
- Week 4 Day 5: Debrief and certification decision

---

### Track B — Natalia Petrova

| Verification Component | Method | Weight |
|----------------------|--------|--------|
| **STRIDE→MASVS Cross-Reference Matrix** (Week 1) | Accuracy of threat-category-to-verification-category mappings | 15% |
| **Threat Model Documents** (Scenarios 1–3, Weeks 2–3) | Completeness of threat identification, accuracy of MASVS mappings, quality of verification criteria | 45% (15% each) |
| **MASVS Gap Analysis Template** (Week 3) | Reusability, completeness, alignment with company architecture review process | 15% |
| **MASVS Integration Playbook** (Week 4) | Practical applicability to Stages 1, 3, 6, 8, 10 of the pipeline | 15% |
| **Framework Review Session** (Week 4) | CSO evaluation of overall understanding and architectural integration capability | 10% |

**Verification Schedule:**

- Weeks 1–3: CSO reviews each deliverable within 48 hours; provides written feedback
- Week 4 Day 1: Integration playbook review
- Week 4 Day 2: Final review session with CSO
- Week 4 Day 3: Framework review completion decision

---

### Track C — David Okonkwo

| Verification Component | Method | Weight |
|----------------------|--------|--------|
| **Comprehension Check Q&A** (10 questions) | Oral + written: 5 multiple-choice, 3 short-answer, 2 strategic scenario questions | 100% |

**Sample Questions:**

1. What is the difference between MASVS L1 and L2? When would we require L2?
2. Which MASVS category addresses certificate pinning? Why does this matter for our platform?
3. If our Android app fails V8 (Resilience) requirements, what is the business risk?
4. How does MASVS compliance affect our Stage 10 Release Readiness gate?
5. What resource investment would be required to bring all three mobile products to L1 compliance?

**Verification Schedule:**

- Same day as briefing: Q&A administered at end of session
- CSO evaluates responses within 24 hours; provides pass/fail determination

---

## 5. Pass/Fail Criteria

### Track A — James Wright (Lead Security Engineer)

**PASS requires ALL of the following:**

| Criterion | Threshold |
|-----------|-----------|
| **Written Examination** | ≥ 80% (40/50 questions correct) |
| **MASVS Verification Report** | ≥ 75% alignment with CSO ground-truth results (i.e., correctly identifies ≥75% of known vulnerabilities and correctly assesses ≥75% of V-category requirements) |
| **Weekly Deliverables** | All weekly gates passed (Weeks 1–3) with CSO sign-off |
| **Tool Proficiency** | Demonstrated independent operation of MobSF (full scan + report interpretation) and Frida (custom script writing + execution) |
| **Critical Knowledge** | 100% correct on questions covering: (a) V3 cryptography requirements, (b) V5 network communication requirements, (c) SSL pinning implementation and bypass detection |

**FAIL conditions (any one triggers failure):**

| Condition |
|-----------|
| Written examination score < 80% |
| MASVS Verification Report alignment < 75% with ground truth |
| Any weekly gate not passed after one remediation attempt |
| Incorrect answer on any critical knowledge question |
| Unable to demonstrate independent tool operation |

**Remediation:** One remediation attempt is permitted for failed weekly gates. The written examination and audit exercise may be retaken once after a 7-day study period. A second failure terminates the probation.

---

### Track B — Natalia Petrova (Security Architect)

**PASS requires ALL of the following:**

| Criterion | Threshold |
|-----------|-----------|
| **STRIDE→MASVS Matrix** | ≥ 80% correct mappings |
| **Threat Model Documents** (all 3 scenarios) | ≥ 80% completeness: all trust boundaries identified, ≥80% of relevant MASVS V-categories mapped, verification criteria defined |
| **MASVS Gap Analysis Template** | CSO judgment: template is reusable, complete, and aligned with company architecture review process |
| **MASVS Integration Playbook** | CSO judgment: playbook is practically applicable to pipeline stages and addresses real integration challenges |

**FAIL conditions (any one triggers failure):**

| Condition |
|-----------|
| STRIDE→MASVS Matrix accuracy < 80% after one remediation attempt |
| Any threat model document < 80% completeness after one remediation attempt |
| Gap Analysis Template deemed non-functional by CSO after one revision |
| Integration Playbook deemed not applicable to company processes |

**Remediation:** One remediation attempt permitted for any failed component. A second failure terminates the probation.

---

### Track C — David Okonkwo (VP Platform Engineering)

**PASS requires:**

| Criterion | Threshold |
|-----------|-----------|
| **Comprehension Check** | ≥ 70% (7/10 questions correct) |
| **Strategic Understanding** | Demonstrates ability to articulate MASVS business impact and resource requirements (evaluated subjectively by CSO) |

**FAIL conditions:**

| Condition |
|-----------|
| Comprehension Check score < 70% |

**Remediation:** One follow-up briefing session (1 hour) is permitted to address knowledge gaps, followed by a re-administered Q&A (new questions, same format).

---

## 6. Resources

### Primary References

| Resource | URL | Purpose |
|----------|-----|---------|
| **OWASP MASVS v2024.05** (Official Documentation) | <https://mas.owasp.org/MASVS/> | Authoritative framework reference — all tracks |
| **OWASP MASVS PDF Download** | <https://github.com/OWASP/owasp-masvs/releases> | Offline reference for exam preparation |
| **OWASP MSTG** (Mobile Security Testing Guide) | <https://mas.owasp.org/MSTG/> | Detailed testing procedures — Track A only |
| **OWASP MASVS Checklist** | <https://github.com/OWASP/owasp-masvs/blob/master/checklists/MASVS-checklist.md> | Per-requirement verification checklist — all tracks |

### Tools

| Tool | Purpose | Installation | Tracks |
|------|---------|-------------|--------|
| **MobSF** (Mobile Security Framework) | Automated SAST/DAST, MASVS-mapped reports | `git clone https://github.com/MobSF/Mobile-Security-Framework-MobSF.git` + `./setup.sh` | A |
| **Frida** | Dynamic instrumentation, method hooking, runtime analysis | `pip install frida-tools` + platform-specific frida-server | A |
| **Objection** | Frida-based runtime exploration toolkit | `pip install objection` | A |
| **jadx** | Android APK decompiler | Download from <https://github.com/skylot/jadx> | A |
| **Hopper / Ghidra** | iOS binary analysis | Ghidra: <https://ghidra-sre.org/> | A (reference only) |
| **Burp Suite Community** | Network traffic interception, API testing | <https://portswigger.net/burp/communitydownload> | A |
| **draw.io** | Architecture diagramming, threat modeling | <https://app.diagrams.net/> | B |

### Sample Applications for Training

| Application | Platform | Purpose | Source |
|-------------|----------|---------|--------|
| **DIVA** (Damn Insecure and Vulnerable App) | Android | Intentionally vulnerable — MobSF and Frida practice | <https://github.com/payatu/diva-android> |
| **DVIA** (Damn Vulnerable iOS App) | iOS | Intentionally vulnerable — Frida practice | <http://damnvulnerableiosapp.com/> |
| **InsecureBankv2** | Android (app + server) | Full-stack mobile security testing | <https://github.com/dineshshetty/Android-InsecureBankv2> |
| **OWASP GoatDroid** | Android | Realistic vulnerable mobile app | <https://github.com/OWASP/GoatDroid> |

### Supplementary Reading

| Resource | Purpose | Track |
|----------|---------|-------|
| **OWASP Mobile Top 10 (2024)** | Context for most critical mobile risks | A, B, C |
| **NIST SP 800-53 Rev. 5** (Mobile Device Security) | Enterprise mobile security controls | B, C |
| **Google Android Security Best Practices** | Platform-specific guidance | A |
| **Apple iOS Security Guide** | Platform-specific guidance | A |
| **CVSS v3.1 Specification** | Vulnerability scoring methodology | A |
| **PCI Mobile Payment Security Standard** | Payment-specific mobile requirements | A, B |

### Internal References

| Document | Location | Purpose |
|----------|----------|---------|
| Security Risk Assessment Framework | `.qwen/skills/security-risk-assessment.md` | CSO risk assessment methodology |
| Application Security Hardening | `.qwen/skills/application-security-hardening.md` | Hardening techniques and tools |
| Mobile Security Architecture | `.qwen/skills/mobile-security-architecture.md` | Platform security models |
| 10-Stage Development Pipeline | `.qwen/workflows/pipeline.md` | Pipeline integration context |

---

## Appendix A: MASVS Verification Categories Reference

| Category | Code | Focus Area | L1 Requirements | L2 Requirements |
|----------|------|------------|----------------|----------------|
| Architecture, Design & Threat Modeling | V1 | Threat models, architecture diagrams, security design | 8 | 3 |
| Data Storage & Privacy | V2 | Local data protection, keychain/keystore, privacy | 10 | 4 |
| Cryptography | V3 | Algorithm selection, key management, crypto implementation | 6 | 4 |
| Authentication & Session Management | V4 | Auth flows, biometrics, session tokens, credential storage | 8 | 4 |
| Network Communication | V5 | TLS, certificate pinning, secure API design | 6 | 3 |
| Platform Interaction | V6 | IPC, intents, WebView, clipboard, keyboard, screenshots | 8 | 2 |
| Code Quality & Build Settings | V7 | Compiler flags, debug builds, dependency management | 5 | 2 |
| Resilience Against Reverse Engineering | V8 | Obfuscation, anti-tampering, root detection, RASP | 5 | 4 |

## Appendix B: Probation Tracking

| Trainee | Track | Enrollment Date | Week 1 Gate | Week 2 Gate | Week 3 Gate | Week 4 Gate | Final Decision |
|---------|-------|----------------|-------------|-------------|-------------|-------------|---------------|
| James Wright | A — Full Mastery | | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending |
| Natalia Petrova | B — Framework Review | | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending |
| David Okonkwo | C — Executive Briefing | | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending | ☐ Pending |

**Completed by:** Dr. Sarah Chen, CSO
**Date:** _______________
