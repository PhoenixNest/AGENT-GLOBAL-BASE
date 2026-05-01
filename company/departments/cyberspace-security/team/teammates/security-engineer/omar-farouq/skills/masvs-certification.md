---
name: masvs-certification
description: Apply the full OWASP MASVS control set (L1 and L2) to certify mobile application compliance, producing a signed certification report with pass/fail status for each control and an overall compliance verdict for release gate approval.
version: "1.0.0"
---

# MASVS Certification

| Competency           | Description                                                     | Quality Criteria                                                                                                                |
| -------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------ | ------------------ | ------------------------------------------------------ |
| MASVS L1 Assessment  | Baseline security controls required for all mobile apps         | All 35 MASVS L1 controls assessed; each assigned Pass / Fail / N/A with evidence; zero unresolved Fail items in final report    |
| MASVS L2 Assessment  | Defence-in-depth controls for high-security mobile applications | All MASVS L2 controls assessed where in scope; Fail items classified by severity with remediation timelines                     |
| Evidence Collection  | Gathering proof for each MASVS control pass/fail determination  | Evidence includes tool output references, code line numbers, or configuration excerpts; assertions without evidence are invalid |
| Certification Report | Formal compliance certification document for release sign-off   | Report follows: Control ID                                                                                                      | Description | Status | Evidence Reference | Remediation (if Fail); signed by CSO for release gates |

## Execution Guidance

### MASVS L1 Control Categories

| Category       | Controls | Scope                                 |
| -------------- | -------- | ------------------------------------- |
| MASVS-STORAGE  | 1–6      | Data at rest security                 |
| MASVS-CRYPTO   | 1–6      | Cryptographic implementation          |
| MASVS-AUTH     | 1–12     | Authentication and session management |
| MASVS-NETWORK  | 1–6      | Network communication security        |
| MASVS-PLATFORM | 1–11     | Platform interaction security         |
| MASVS-CODE     | 1–8      | Code quality and build settings       |

### Certification Report Format

```markdown
# MASVS Compliance Certification — [App Name] v[Version]

**Assessment Date:** YYYY-MM-DD
**Assessor:** Omar Farouq, Security Engineer
**Level:** L1 / L2
**Overall Verdict:** PASS / CONDITIONAL PASS / FAIL

## Control Assessment Summary

| Control ID      | Description               | Status | Evidence                          |
| --------------- | ------------------------- | ------ | --------------------------------- |
| MASVS-STORAGE-1 | No sensitive data in logs | PASS   | ProGuard config; log review       |
| MASVS-CRYPTO-3  | No hardcoded keys         | FAIL   | jadx: BuildConfig.API_KEY line 42 |
```

A **CONDITIONAL PASS** requires all Fail items to be remediated before the next release gate. A **FAIL** blocks release.
