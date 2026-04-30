---
name: studio-engineering-code-review-standards
description: Code review standards and process for the Casual Games Studio engineering team — PR template, review checklist, severity classification, and culture norms that reduced production bugs by 30%. Owned by Dmitri Volkov (Senior Game Engineer). Trigger: code review, PR review, pull request, review process, review standards.
version: "1.0.0"
---

# Code Review Standards

**Skill Owner:** Dmitri Volkov (Senior Game Engineer)
**Applies To:** All Engineering PRs, Stage 5 (Full Production) continuous PR reviews feeding into the Stage 6 (Automated Testing) quality gate

## PR Template (Required for All Engineering PRs)

Every pull request must include:

```markdown
## Summary

[1–3 sentences: what does this PR do and why?]

## Type

[ ] Feature [ ] Bug Fix [ ] Performance [ ] Refactor [ ] Test [ ] Tooling

## Test Evidence

[Screenshot, profiler capture, or test output demonstrating the change works]

## Performance Impact

[Before/after frame time, memory delta, or "N/A — no performance-sensitive code"]

## Checklist

- [ ] Self-reviewed (read every line before requesting review)
- [ ] No debug code, commented-out blocks, or TODO left in
- [ ] Unit tests added/updated for new logic
- [ ] No new compiler warnings
- [ ] Profiled on target device if touching a hot path
```

## Reviewer Checklist

| Category           | What to Check                                                                                             |
| ------------------ | --------------------------------------------------------------------------------------------------------- |
| Correctness        | Does the code do what the PR description says? Does it handle edge cases and null inputs?                 |
| Performance        | Are there allocations in hot paths (Update, FixedUpdate)? Does it introduce unnecessary draw calls?       |
| Architecture       | Does the change respect the established system design? Does it introduce unintended coupling?             |
| Readability        | Can a new team member understand this code in 10 minutes? Are variable and method names self-documenting? |
| Testability        | Is the new logic unit-testable? Are tests included?                                                       |
| Security           | Are there any hardcoded credentials, exposed API keys, or unsafe deserialization patterns?                |
| Studio Conventions | Does the code follow the studio's naming conventions, folder structure, and Unity component patterns?     |

## Finding Severity Classification

| Severity | Definition                                                                  | Required Action                                  |
| -------- | --------------------------------------------------------------------------- | ------------------------------------------------ |
| **P0**   | Crash, data loss, security vulnerability, or game-breaking bug              | PR must not merge; author fixes before re-review |
| **P1**   | Core feature broken, performance regression >15%, or architecture violation | PR must not merge; author fixes before re-review |
| **P2**   | Suboptimal but functional; clear improvement available                      | Author addresses or documents accepted debt      |
| **P3**   | Nit / style / minor readability issue                                       | Author decides; no merge gate                    |
| **Note** | Informational — no action required                                          | Optional discussion                              |

P0 and P1 findings block merge. Dmitri makes the final call on borderline P1/P2 classifications.

## Review Culture Norms

1. **Be specific, not vague.** "This allocates in Update" beats "this might be slow."
2. **Separate opinions from standards.** P3 nits are preferences. Only P0/P1 are non-negotiable.
3. **Praise good work explicitly.** Recognition in code review builds a learning culture.
4. **No drive-by approvals.** A ✅ approval means the reviewer read every changed line.
5. **Turnaround SLA:** Reviews must be completed within 24 hours of request. If a reviewer cannot meet this, they notify the author immediately.

## Measurable Quality Standards

| Standard                 | Target               | Measurement Method                      |
| ------------------------ | -------------------- | --------------------------------------- |
| Review turnaround        | ≤24 hours            | GitHub PR open → first review timestamp |
| P0/P1 escape rate        | 0 post-Stage 5 (before Stage 6 automated testing gate)       | Stage 6 defect log                      |
| Production bug reduction | ≥30% vs. baseline    | Post-launch defect count comparison     |
| PR size (lines changed)  | ≤400 lines preferred | GitHub PR diff stats                    |
