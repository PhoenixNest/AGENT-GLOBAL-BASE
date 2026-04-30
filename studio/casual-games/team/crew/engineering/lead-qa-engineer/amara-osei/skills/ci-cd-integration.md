---
name: studio-qa-ci-cd-integration
description: CI/CD pipeline design for automated game testing — Unity Cloud Build or GitHub Actions integration, test trigger rules, build artifact management, and multi-studio pipeline standards. Owned by Amara Osei (Lead QA Engineer). Trigger: CI/CD, build pipeline, automated builds, GitHub Actions, Unity Cloud Build, test automation pipeline, continuous integration.
version: "1.0.0"
---

# CI/CD Integration

**Skill Owner:** Amara Osei (Lead QA Engineer)
**Applies To:** Build Automation, Test Trigger Rules, Artifact Management, Pipeline Standards

## Tools & Frameworks

| Tool/Framework    | Version Context | Usage                                         |
| ----------------- | --------------- | --------------------------------------------- |
| GitHub Actions    | Latest          | Primary CI/CD runner for all builds and tests |
| Unity Test Runner | Built-in        | Unit and integration test execution in-engine |
| Unity Cloud Build | Latest          | Remote build distribution for QA/stakeholders |
| Firebase Test Lab | Latest          | Cloud device testing triggered by CI          |
| Fastlane          | Latest          | iOS/Android build signing and distribution    |
| Slack             | API             | Build status notifications                    |
| JIRA              | Latest          | Defect creation from failed tests             |

## Pipeline Architecture

```
[Commit / PR]
    │
    ├─► [Fast Gate — <5 min]
    │       Unit Tests (Unity Test Runner, EditMode)
    │       Compile Check (all platforms)
    │       Lint / Code Style
    │
    ├─► [Integration Gate — <15 min] (on PR merge to develop)
    │       PlayMode Integration Tests
    │       Android/iOS Build (Development mode)
    │       Smoke Test on Firebase Test Lab (min spec device)
    │
    └─► [Nightly Build — <60 min]
            Full Regression Suite (Unity Test Runner + Appium)
            Firebase Test Lab (min spec + target spec devices)
            Build size report
            Performance benchmark (FPS, memory, load time)
            Test report → JIRA (auto-create tickets for new failures)
            Slack notification: pass/fail + artifact link
```

## Real-World Production Scenarios

### Scenario 1: Designing the Fast Gate

**Context:** Engineers need fast feedback (<5 min) on every commit without slowing iteration.
**Process:**

1. Run only EditMode unit tests (no game startup required) — these run in <60 seconds
2. Add a compile check for all build targets (Android, iOS, Standalone) — catches missing assemblies early
3. All fast gate jobs run in parallel on a GitHub Actions matrix
4. Fast gate failure blocks PR merge; author must fix before re-requesting review

### Scenario 2: Handling a Flaky Test

**Context:** A PlayMode test fails intermittently (30% failure rate) in the integration gate.
**Process:**

1. Quarantine the flaky test immediately: add `[Ignore("Flaky — JIRA-XXX")]` attribute to prevent blocking clean PRs
2. Assign a JIRA ticket to the SDET responsible for the test area
3. Root cause analysis: run the test 100 times locally in isolation to confirm intermittency
4. Common causes: `WaitForSeconds` with insufficient buffer, UnityEvent ordering assumptions, async code without proper `await`
5. Fix, remove quarantine, confirm 100 clean runs before re-enabling in gate
6. Track flaky test count on the QA dashboard; target ≤3 quarantined tests at any time

### Scenario 3: Setting Up the Nightly Build for a New Title

**Context:** New title entering Stage 5; first nightly build pipeline needs to be established.
**Process:**

1. Clone the pipeline template from the studio's shared GitHub Actions workflow library
2. Configure Unity license activation (Unity Build Server license or seat-based)
3. Set up signing: Android keystore and iOS provisioning profile stored as GitHub Secrets
4. Configure Firebase Test Lab credentials and device matrix
5. Set up JIRA integration: webhook that auto-creates a bug ticket for any test that was passing yesterday and failing today (new regression)
6. First nightly run serves as the baseline; all future runs are compared against it

## Measurable Quality Standards

| Standard                  | Target                                | Measurement Method                        |
| ------------------------- | ------------------------------------- | ----------------------------------------- |
| Fast gate execution time  | ≤5 minutes                            | GitHub Actions timing                     |
| Integration gate time     | ≤15 minutes                           | GitHub Actions timing                     |
| Nightly build reliability | ≥95% success rate (non-test failures) | 30-day rolling average                    |
| Flaky test count          | ≤3 quarantined at any time            | QA dashboard                              |
| Time to detect regression | ≤24 hours (nightly cadence)           | JIRA ticket creation date vs. commit date |

## Industry Best Practice References

- **Zynga CI/CD Playbook** (internal reference — Amara's prior methodology)
- **Unity Testing Documentation** — Unity Test Framework guide
- **Google Firebase Test Lab Documentation** — Device matrix and test execution
- **GitHub Actions Documentation** — Workflow syntax and best practices
