---
name: code-review-participation
description: Participate effectively in code reviews as both reviewer and reviewee. This skill covers how to conduct thorough.
---

# Code Review Participation Process

**Category:** Engineering Process
**Owner:** All Engineers

## Purpose

Participate effectively in code reviews as both reviewer and reviewee. This skill covers how to conduct thorough, constructive code reviews; how to receive and respond to review feedback; turnaround time expectations; escalation paths for disagreements; and the role of code review within the 10-stage pipeline (Stage 6).

## Execution Guidance

### As a Reviewer — What to Check

**Review checklist ordered by priority:**

| Priority | Check                        | How to Verify                                |
| -------- | ---------------------------- | -------------------------------------------- |
| P0       | Security vulnerabilities     | OWASP Top 10, input validation, auth checks  |
| P0       | Data loss or corruption risk | Migration safety, destructive operations     |
| P1       | Business logic correctness   | Does it match the PRD/spec?                  |
| P1       | Error handling completeness  | All error paths handled, no swallowed errors |
| P2       | Code clarity and readability | Naming, comments, function length            |
| P2       | Test coverage                | Unit tests for new logic, edge cases         |
| P2       | Performance implications     | N+1 queries, missing indexes, large payloads |
| P3       | Style consistency            | Formatting, naming conventions               |
| P3       | Documentation updates        | README, API docs, inline comments            |

**Effective review comment format:**

```
[Severity] Location
Observation: What you see
Impact: Why it matters
Suggestion: How to fix (optional but preferred)

Example:
[P1] src/services/order_service.go:47
Observation: The database transaction is started but never committed or rolled back on the error path.
Impact: This will leave the database in a partially committed state and lock rows indefinitely.
Suggestion: Use defer tx.Rollback() and tx.Commit() after all operations succeed.
```

### Code Review Process in the Pipeline

**Stage 6 — Code Review Gate:**

```
1. CTO assembles review panel (minimum 2 engineers)
2. Each reviewer independently reviews the full diff
3. Reviewers classify defects using P0-P3 system
4. Panel consolidates findings into Defect Report
5. Report presented to user for P2/P3 decisions
6. User approves/rejects based on defect classification
```

**Turnaround expectations:**

| Review Type         | Max Turnaround | Reviewers Required |
| ------------------- | -------------- | ------------------ |
| Hotfix (P0)         | 2 hours        | 1 senior engineer  |
| Bug fix (P1/P2)     | 24 hours       | 1 engineer         |
| Feature (new code)  | 48 hours       | 2 engineers        |
| Architecture change | 48 hours       | CTO + 1 engineer   |
| Security change     | 24 hours       | CSO + 1 engineer   |

### As a Reviewee — Responding to Feedback

**Response protocol:**

1. **Acknowledge** each comment — "Fixed", "Addressed in commit abc123", or "Can you clarify?"
2. **Classify** — Is it a valid defect? Does the severity match?
3. **Fix** — Address P0/P1 defects immediately. Discuss P2/P3 with reviewer.
4. **Re-request review** — After fixes, explicitly request re-review.
5. **Escalate** — If you disagree with a P0/P1 classification, escalate to CTO.

**Disagreement resolution:**

```
Reviewer flags P1 → Reviewee believes it's P2
  → Reviewee explains rationale
  → If unresolved → CTO makes final call
  → CTO's classification is final

Reviewer flags P0 → Reviewee disagrees
  → CTO and CSO jointly assess
  → If either confirms P0 → It is P0 (non-negotiable)
```

### Review Anti-Patterns to Avoid

| Anti-Pattern         | What It Looks Like                    | Better Approach                    |
| -------------------- | ------------------------------------- | ---------------------------------- |
| Rubber-stamping      | "LGTM" with no substantive comments   | At least 2 meaningful observations |
| Nit-picking          | 80% style comments, 0% logic comments | Focus on P0/P1 first, style last   |
| Drive-by refactoring | Reviewer rewrites unrelated code      | Suggest as separate PR             |
| Wall of text         | Single paragraph with 20 issues       | One comment per issue, numbered    |
| Silent rejection     | Rejecting without explanation         | Always explain rejection reason    |
| Approval pressure    | "Just approve it, we're in a hurry"   | Pipeline gates exist for a reason  |

### Review Template (for review tools)

```markdown
## Code Review: {PR Title}

**Reviewer:** {name}
**Date:** {date}
**Scope:** {files changed, lines added/removed}

### Summary

{2-3 sentence overview of what this change does and overall quality}

### Critical Issues (P0/P1)

1. **[P0/P1]** {description} — {file:line}
   - Impact: {why this blocks merge}
   - Suggestion: {how to fix}

### Non-Critical Issues (P2/P3)

1. **[P2]** {description} — {file:line}
   - Impact: {why this should be addressed}
   - Suggestion: {how to fix}

### Positive Observations

- {what was done well}
- {patterns worth replicating}

### Recommendation

- [ ] Approve (no issues or P3 only)
- [ ] Approve with fixes (P2 issues addressed before merge)
- [ ] Request changes (P0/P1 issues must be fixed)
```

## Pipeline Integration

**Stage 6 (Code Review):** This IS the code review process. Panel members use this skill to conduct reviews. Defects classified here feed into the Defect Report.

**Stage 8 (Integrity Verification):** Previous code review sign-off is validated. Any regressions from Stage 6 are flagged.

**Stage 10 (Release):** Code review sign-off is one of 7 release checklist items (owned by CTO panel).

## Quality Standards

| Metric                 | Target                                | Measurement                |
| ---------------------- | ------------------------------------- | -------------------------- |
| Review turnaround      | < 48 hours for features               | PR analytics               |
| Defect detection rate  | > 80% of defects caught in review     | Post-merge defect tracking |
| Review coverage        | 100% of changes reviewed before merge | CI pipeline gate           |
| Comment quality        | > 70% substantive (non-style)         | Manual audit               |
| Reviewer participation | Minimum 2 reviewers per feature PR    | PR metadata                |
| Fix rate on P0/P1      | 100% fixed before merge               | PR merge criteria          |

## Reference Materials

- [Google Code Review Guidelines](https://google.github.io/eng-practices/review/)
- [Conventional Comments Specification](https://conventionalcomments.org/)
- [Code Review Pyramid](https://www.morling.dev/blog/the-code-review-pyramid/)
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
- `company/pipeline/mobile-development/pipeline.md` — Stage 6 specification
