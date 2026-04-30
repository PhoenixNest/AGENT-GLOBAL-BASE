---
name: competency-tracking
description: "Engineer competency frameworks, multi-rater assessment instruments, and progress dashboards for R&D teams; design structured 90-day probationary evaluations with explicit pass/fail criteria that surface readiness signals and drive targeted development plans."
version: "1.0.0"
---

| Competency              | Description                                                                           | Quality Criteria                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Matrix Design           | Build role-family-specific competency frameworks with measurable behavioral anchors   | Can design a 5-7 dimension matrix with 4 proficiency levels per role family; validated by CTO and CHRO |
| Assessment Frameworks   | Create multi-rater evaluation instruments (self, peer, supervisor, objective metrics) | Assessment inter-rater reliability ≥0.75 (Cronbach's alpha); completion rate ≥95%                      |
| Progress Dashboards     | Build visual dashboards that surface competency trends, gaps, and readiness signals   | Dashboard updated weekly; consumed by 100% of supervisors in 1:1 preparation                           |
| Probationary Evaluation | Design and execute structured 90-day evaluations with explicit pass/fail criteria     | 100% of probationary reviews completed on Day 85-90; zero legal or procedural challenges               |
| Performance Baselining  | Establish objective starting metrics for new hires at Day 1 and Week 1                | Baseline documented within 5 business days of hire; signed off by supervisor and new hire              |
| Onboarding ROI          | Calculate return on onboarding investment (ramp time cost vs. productivity output)    | ROI model updated quarterly; presented to CHRO with actionable recommendations                         |

## Execution Guidance

### Competency Matrix Architecture

Each role family has a tailored competency matrix with 5-7 dimensions. All matrices share a common 4-level proficiency scale:

| Level | Label        | Definition                                                                                |
| ----- | ------------ | ----------------------------------------------------------------------------------------- |
| 1     | Foundational | Understands concepts; requires guidance and review for all work products                  |
| 2     | Developing   | Applies concepts independently on small-to-medium tasks; occasional guidance needed       |
| 3     | Proficient   | Handles complex tasks autonomously; contributes to team decisions; mentors Level 1-2      |
| 4     | Expert       | Sets standards for the role family; architects solutions; recognized cross-team authority |

#### Android Development Track

| Dimension               | Level 1                                                         | Level 2                                                                         | Level 3                                                                                | Level 4                                                                     |
| ----------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Kotlin/Java Proficiency | Writes basic Activities, Fragments; needs review for coroutines | Uses coroutines, Flow, ViewModel correctly; writes unit tests                   | Designs reactive architectures; optimizes performance; leads code reviews              | Sets team Kotlin standards; authors ADRs on architectural patterns          |
| Android SDK & Lifecycle | Understands Activity/Fragment lifecycle; basic Jetpack          | Uses Navigation, Room, WorkManager independently; handles configuration changes | Designs multi-module architecture; implements custom views; optimizes battery/memory   | Contributes to Android Open Source Project; speaks at DroidCon              |
| Platform Security       | Follows SRD checklist; uses Keychain for basic auth             | Implements OWASP MASVS controls; handles biometric auth, certificate pinning    | Designs security architecture for Android-specific threats; leads pen-test remediation | Publishes Android security guidance; advises CSO on mobile threat landscape |
| CI/CD & Testing         | Runs local tests; understands CI pipeline output                | Writes unit + integration tests; configures Fastlane lanes                      | Designs test architecture; achieves ≥80% code coverage; maintains CI stability         | Sets team testing standards; authors testing skill files                    |
| Code Review Quality     | Identifies surface-level issues (style, naming)                 | Catches logic errors, missing edge cases; provides constructive feedback        | Reviews for architecture, security, performance; approves PRs independently            | Sets code review standards; calibrates review quality across team           |

#### iOS Development Track

| Dimension            | Level 1                                                       | Level 2                                                                             | Level 3                                                                                | Level 4                                                                    |
| -------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Swift & SwiftUI      | Builds basic views; understands Optionals, structs, protocols | Uses Combine, SwiftData, SwiftUI lifecycle; writes XCTest                           | Architects MVVM/TCA patterns; optimizes SwiftUI performance; leads reviews             | Sets Swift standards; contributes to Swift Evolution discussions           |
| iOS SDK & Frameworks | Uses UIKit or SwiftUI basics; understands app lifecycle       | Implements Core Data, CloudKit, UserNotifications; handles App Lifecycle            | Designs complex navigation stacks; implements custom animations; optimizes launch time | Architects iOS platform strategy; advises CTO on Apple ecosystem direction |
| Platform Security    | Follows SRD checklist; uses Keychain for credentials          | Implements ATS, certificate pinning, biometric auth; handles App Transport Security | Designs security architecture for iOS-specific threats; leads pen-test remediation     | Publishes iOS security guidance; advises CSO on mobile threat landscape    |
| CI/CD & Testing      | Runs Xcode tests; understands CI pipeline output              | Writes unit + UI tests; configures Fastlane + xcodebuild                            | Designs test architecture; achieves ≥80% code coverage; maintains CI stability         | Sets team testing standards; authors testing skill files                   |
| Code Review Quality  | Identifies surface-level issues (style, naming)               | Catches logic errors, memory leaks; provides constructive feedback                  | Reviews for architecture, security, performance; approves PRs independently            | Sets code review standards; calibrates review quality across team          |

#### Cross-Platform Development Track (Flutter / KMP)

| Dimension                       | Level 1                                                              | Level 2                                                       | Level 3                                                                                 | Level 4                                                                         |
| ------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Framework Proficiency (Flutter) | Builds basic widgets; understands Stateful/Stateless lifecycle       | Uses Provider/Riverpod, navigates routes, writes widget tests | Architects scalable state management; implements platform channels; optimizes rendering | Sets Flutter standards; contributes to Flutter framework; speaks at FlutterConf |
| Framework Proficiency (KMP)     | Writes basic shared modules; understands Kotlin Multiplatform basics | Implements expect/actual patterns; writes shared unit tests   | Designs KMP architecture for complex business logic; manages platform-specific interop  | Sets KMP standards; advises CTO on cross-platform strategy                      |
| Platform Integration            | Uses basic platform channels or expect/actual                        | Implements native interop for camera, location, storage       | Designs plugin architecture; handles native SDK integration patterns                    | Architects cross-platform plugin ecosystem                                      |
| Performance Optimization        | Identifies obvious performance issues (jank, memory)                 | Profiles with DevTools/Instruments; optimizes widget rebuilds | Implements advanced optimizations (isolate, compose recomposition bounds)               | Sets performance benchmarks; leads cross-platform perf initiatives              |
| Code Review Quality             | Identifies surface-level issues                                      | Catches logic errors, platform-specific bugs                  | Reviews for architecture, cross-platform consistency, performance                       | Sets code review standards for cross-platform track                             |

#### Software Architecture Track

| Dimension             | Level 1                                          | Level 2                                                              | Level 3                                                                       | Level 4                                                                       |
| --------------------- | ------------------------------------------------ | -------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| UML Modeling          | Creates basic class and sequence diagrams        | Produces complete UML package (class, sequence, component, activity) | Architects UML for complex systems; validates diagrams against implementation | Sets UML standards; trains engineers on modeling best practices               |
| ADR Authoring         | Contributes to existing ADRs; understands format | Authors ADRs independently; facilitates decision discussions         | Leads architecture decision processes; maintains ADR catalog integrity        | Sets ADR standards; advises CTO on critical technology decisions              |
| System Design         | Understands modular architecture basics          | Designs multi-module systems; evaluates trade-offs                   | Architects system-wide solutions; leads design reviews                        | Sets architectural vision; evaluates emerging technologies for strategic fit  |
| Technology Evaluation | Researches technologies per CIO/TSD criteria     | Conducts structured evaluations with TCO analysis                    | Leads vendor/technology evaluations; presents recommendations to CTO+CIO      | Sets technology evaluation standards; advises executive team on tech strategy |

#### Test Lead Track

| Dimension              | Level 1                                    | Level 2                                                             | Level 3                                                                          | Level 4                                                                         |
| ---------------------- | ------------------------------------------ | ------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Test Architecture      | Writes unit and integration tests          | Designs test suites across unit, integration, E2E, regression       | Architects test strategy for full pipeline; achieves 100% automated pass rate    | Sets testing standards across all platforms; advises CTO on test infrastructure |
| Defect Analysis        | Classifies defects per P0-P3 system        | Analyzes defect trends; identifies systemic quality issues          | Leads root-cause analysis; implements preventive quality measures                | Sets defect classification standards; advises on quality gate criteria          |
| CI/CD Test Integration | Configures test execution in CI pipeline   | Implements parallel test execution; manages flaky test quarantine   | Designs test pipeline architecture; optimizes execution time and reliability     | Sets CI/CD testing standards; integrates advanced testing (chaos, mutation)     |
| Quality Metrics        | Collects and reports basic quality metrics | Builds quality dashboards; correlates metrics with release outcomes | Predicts release risk based on quality signals; implements early warning systems | Sets quality measurement standards; advises executive team on quality posture   |

### Assessment Framework

#### Multi-Rater Evaluation Model

Each competency dimension is assessed through 3 lenses:

| Rater                 | Method                                                  | Frequency     | Weight |
| --------------------- | ------------------------------------------------------- | ------------- | ------ |
| Self-Assessment       | Engineer rates own proficiency with evidence examples   | Quarterly     | 20%    |
| Peer Assessment       | 2-3 peers rate engineer via calibrated rubric           | Semi-annually | 30%    |
| Supervisor Assessment | Direct supervisor rates based on observed work products | Quarterly     | 50%    |

**Composite Score Calculation:**

```
Composite = (Self × 0.20) + (Peer × 0.30) + (Supervisor × 0.50)
```

#### Assessment Instruments

- **Behavioral Anchors:** Each proficiency level includes 3-5 observable behaviors (e.g., "Level 3: Designs reactive architectures; optimizes performance; leads code reviews")
- **Evidence Requirements:** Assessors must cite specific work products (PRs, ADRs, shipped features) to justify ratings
- **Calibration Sessions:** Quarterly calibration across supervisors to reduce rater bias; CHRO facilitates
- **Inter-Rater Reliability:** Measured via Cronbach's alpha; target ≥0.75. If below threshold, recalibrate rubrics and retrain assessors

### Progress Dashboards

#### Dashboard Architecture

- **Tool:** Internal competency dashboard (built on internal analytics platform; data sourced from HRIS, Git, CI/CD, and assessment surveys)
- **Views:**
  - **Individual View:** Engineer sees own competency trajectory across all dimensions, with historical trend lines
  - **Team View:** Supervisor sees team competency heatmap, identifying gaps and over-concentration risks
  - **Executive View:** CHRO and CTO see department-level competency distribution, promotion readiness pipeline, and skill gap alerts
- **Update Frequency:** Automated metrics (PR count, review participation, test coverage) updated daily; assessment scores updated quarterly
- **Alerts:**
  - Skill gap alert: Any dimension where ≥3 team members score ≤Level 1
  - Stagnation alert: Any engineer with no proficiency increase across any dimension in 2 consecutive quarters
  - Promotion readiness: Any engineer scoring Level 3+ on all dimensions for 2 consecutive quarters

#### Key Dashboard Metrics

| Metric                           | Definition                                                  | Target       |
| -------------------------------- | ----------------------------------------------------------- | ------------ |
| Competency Coverage              | % of engineers with up-to-date assessments (within 90 days) | ≥95%         |
| Skill Gap Density                | Avg. number of dimensions per team where avg. score <2.0    | ≤1 per team  |
| Promotion Readiness Pipeline     | # of engineers scoring Level 3+ across all dimensions       | ≥15% of FTEs |
| Assessment Completion Rate       | % of assessments completed by deadline                      | ≥95%         |
| Rater Reliability (Cronbach's α) | Inter-rater agreement across all dimensions                 | ≥0.75        |

### Probationary Period Evaluation

#### Timeline & Process

| Milestone           | Timing    | Activity                                                                                         | Owner                                           |
| ------------------- | --------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| Baseline Assessment | Day 1-5   | Supervisor documents starting competency levels based on interview evidence and portfolio review | Supervisor                                      |
| Week 1 Check-in     | Day 5     | Verify environment readiness, first PR quality, buddy relationship health                        | Onboarding Lead + Buddy                         |
| Month 1 Review      | Day 30    | Competency assessment update; goal adjustment; buddy feedback                                    | Supervisor + Onboarding Lead                    |
| Month 2 Check-in    | Day 60    | Mid-probation progress review; remediation plan if gaps identified                               | Supervisor                                      |
| Probationary Review | Day 85-90 | Final evaluation against competency matrix; pass/fail decision                                   | CHRO + Supervisor + CTO (for engineering roles) |

#### Pass/Fail Criteria

| Outcome              | Criteria                                                                                                | Action                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Pass — Strong**    | Composite score ≥3.0 on all dimensions; evidence of autonomous contribution                             | Confirm employment; eligibility for promotion track                 |
| **Pass — Meets**     | Composite score ≥2.5 on all dimensions; no dimension ≤2.0                                               | Confirm employment; targeted development plan for weaker dimensions |
| **Extend Probation** | 1-2 dimensions scoring 1.5-2.0; overall trajectory positive                                             | Extend probation by 30 days; specific remediation goals documented  |
| **Fail**             | ≥2 dimensions scoring <1.5; or any dimension scoring <1.0; or P0/P1 defect introduced due to negligence | Termination per HR policy; exit interview conducted by CHRO         |

#### Documentation Requirements

- All probationary assessments documented in HRIS with specific evidence citations
- Extension decisions require CHRO approval and documented remediation plan with measurable goals
- Fail decisions require CHRO + CTO co-signature; legal review if tenure >60 days
- New hire receives written summary of assessment within 3 business days of review

### Performance Baselining

#### Baseline Establishment Process

1. **Pre-Hire Baseline:** Interview panel documents expected starting level per dimension based on interview performance and portfolio evidence
2. **Day 1 Confirmation:** Supervisor validates (or adjusts) pre-hire baseline after reviewing new hire's actual work sample (coding exercise or portfolio piece)
3. **Week 1 Calibration:** After first PR merge, supervisor adjusts baseline if observed performance differs significantly from pre-hire estimate
4. **Baseline Sign-off:** New hire and supervisor both sign the baseline document; serves as reference point for all future assessments

#### Baseline Documentation Template

```markdown
# Performance Baseline — [Engineer Name]

**Role:** [Role Family] — [Level]
**Start Date:** [YYYY-MM-DD]
**Baseline Date:** [YYYY-MM-DD]
**Supervisor:** [Name]

## Dimension Baselines

| Dimension | Expected Level | Confirmed Level | Evidence / Notes    |
| --------- | -------------- | --------------- | ------------------- |
| [Dim 1]   | [1-4]          | [1-4]           | [Specific evidence] |
| [Dim 2]   | [1-4]          | [1-4]           | [Specific evidence] |
| ...       | ...            | ...             | ...                 |

## Signatures

- Supervisor: **\*\*\*\***\_**\*\*\*\*** Date: **\_\_\_**
- Engineer: **\*\*\*\***\_**\*\*\*\*** Date: **\_\_\_**
```

### Onboarding ROI Measurement

#### ROI Calculation Model

```
Onboarding Cost = (Buddy Hours × Buddy Hourly Rate) +
                  (Supervisor Hours × Supervisor Hourly Rate) +
                  (Onboarding Lead Hours × Lead Rate) +
                  (Training Materials & Tools Cost) +
                  (New Hire Non-Productive Salary for Ramp Period)

Productivity Value = (New Hire Output Value from Day 1 to Day 90) —
                     (Expected Output of Equivalent Experienced Hire for Same Period)

ROI = (Productivity Value — Onboarding Cost) / Onboarding Cost × 100%
```

#### Measurement Cadence

| Metric                      | Frequency                   | Owner                  |
| --------------------------- | --------------------------- | ---------------------- |
| Onboarding Cost per Hire    | Per cohort                  | Onboarding Lead        |
| Time-to-Productivity (Days) | Per hire                    | Supervisor             |
| First-Year Retention Rate   | Annually                    | CHRO                   |
| Onboarding NPS              | Per cohort (Day 30, Day 90) | Onboarding Lead        |
| ROI per Role Family         | Quarterly                   | Onboarding Lead + CHRO |

#### ROI Reporting

- Quarterly ROI report presented to CHRO with breakdown by role family, cohort, and individual hire
- Recommendations for program optimization based on ROI signals (e.g., if buddy time is high but ramp time is low, increase buddy investment)
- Year-over-year ROI trend tracked; target: positive ROI within first 6 months of hire

## Pipeline Integration

| Pipeline Stage                   | Competency Tracking Relevance                                                                                                                         |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 1-4                        | Not directly applicable — new hires in early onboarding do not contribute to these stages                                                             |
| Stage 5 (Development)            | **Primary measurement stage** — PR count, code review participation, defect introduction rate, and feature ownership tracked as competency indicators |
| Stage 6 (Code Review)            | Code review quality dimension assessed via PR review participation and feedback quality                                                               |
| Stage 7 (Testing)                | Test architecture dimension assessed via test contribution volume and quality                                                                         |
| Stage 8 (Integrity Verification) | Panel participation tracked as leadership signal for senior engineers                                                                                 |
| Stage 9-10                       | Not directly applicable — specialized to Localization and Release teams                                                                               |

## Quality Standards

- **Assessment Currency:** 100% of engineers have competency assessments updated within 90 days; zero engineers with stale assessments (>120 days)
- **Calibration Compliance:** Quarterly calibration sessions held for all role families; 100% of supervisors participate
- **Probationary Review Timeliness:** 100% of probationary reviews completed by Day 90 (±5 days); zero reviews completed late without documented exception
- **Dashboard Accuracy:** Dashboard data matches source systems (HRIS, Git, CI/CD) within 24-hour lag; data integrity audit conducted monthly
- **ROI Reporting:** Quarterly ROI reports delivered to CHRO by 15th business day of quarter; includes actionable recommendations
- **Promotion Pipeline Accuracy:** ≥80% of engineers flagged as "promotion ready" in dashboard actually promoted within 6 months (validates model accuracy)
- **Legal Compliance:** All probationary evaluations documented per employment law; zero legal challenges due to procedural deficiencies
