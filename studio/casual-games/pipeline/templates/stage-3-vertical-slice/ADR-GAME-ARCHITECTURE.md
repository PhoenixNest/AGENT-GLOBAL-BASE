# ADR: Game Architecture — Template

> **Stage:** 3 — Vertical Slice
> **Producer:** Lead Engineer + Studio Director (Dr. Marcus Vogel)
> **Kill Gate:** KG-3 — Vertical Slice
> **User Approval:** ✅ Required — technology decisions lock on approval
> **Warning:** Architecture decisions made here are **immutable** after User approval. Any change
> requires a new ADR and full Stage 3 re-entry.

---

## ADR: [Title — e.g. "Platform Architecture and Rendering Strategy"]

**Date:** YYYY-MM-DD
**Status:** Proposed / Accepted / Superseded
**Author:** [Lead Engineer]

---

## Context

[2–3 sentences describing the technical problem or design question that this decision addresses. What forces are at play? What constraints exist from the PRD, GDS, or SRD?]

---

## Decision

**[State the decision clearly and directly in one sentence]**

[Expand with 2–3 sentences explaining what exactly was decided and what it means in practice]

---

## Platform Strategy

| Dimension               | Decision                                               |
| :---------------------- | :----------------------------------------------------- |
| **Engine**              | Unity 6.3 LTS (studio standard)                        |
| **Target platforms**    | [iOS / Android / Both]                                 |
| **Minimum OS versions** | iOS [X] / Android [X]                                  |
| **Rendering pipeline**  | [URP / HDRP / Built-in]                                |
| **Scripting backend**   | IL2CPP                                                 |
| **Graphics API**        | [Metal (iOS) / Vulkan (Android) / OpenGL ES3 fallback] |

---

## Architecture Decisions

### [Sub-decision 1: e.g. State Management]

| Option     | Pros   | Cons   |
| :--------- | :----- | :----- |
| [Option A] | [Pros] | [Cons] |
| [Option B] | [Pros] | [Cons] |

**Chosen:** [Option A/B]
**Rationale:** [2 sentences]

### [Sub-decision 2: e.g. Data Persistence]

| Option     | Pros   | Cons   |
| :--------- | :----- | :----- |
| [Option A] | [Pros] | [Cons] |
| [Option B] | [Pros] | [Cons] |

**Chosen:** [Option A/B]
**Rationale:** [2 sentences]

### [Sub-decision 3: e.g. Networking / Backend]

| Dimension           | Decision                                |
| :------------------ | :-------------------------------------- |
| **Backend service** | [e.g. PlayFab / Firebase / Custom]      |
| **Protocol**        | [e.g. HTTPS REST / WebSocket]           |
| **Offline mode**    | [Required / Not required]               |
| **Anti-cheat**      | [Server-authoritative / Client-trusted] |

---

## Dependency Map

| Dependency        | Version | Licence       | Risk Level |
| :---------------- | :------ | :------------ | :--------: |
| Unity 6.3 LTS     | 6.3.x   | Unity Licence |    Low     |
| [Third-party SDK] | [X.X]   | [Licence]     |   [Risk]   |
| [Ad network SDK]  | [X.X]   | [Licence]     |   [Risk]   |
| [Analytics SDK]   | [X.X]   | [Licence]     |   [Risk]   |

---

## Consequences

### Positive

1. [Consequence 1]
2. [Consequence 2]

### Negative / Trade-offs

1. [Trade-off 1]
2. [Trade-off 2]

### Risks

| Risk     | Likelihood | Impact  | Mitigation   |
| :------- | :--------: | :-----: | :----------- |
| [Risk 1] |  [H/M/L]   | [H/M/L] | [Mitigation] |
| [Risk 2] |  [H/M/L]   | [H/M/L] | [Mitigation] |

---

## Sign-Off

> Technology decisions are **locked** on User approval. No changes without a new ADR and Stage 3 re-entry.

| Role            | Agent            |      Decision       | Date       |
| :-------------- | :--------------- | :-----------------: | :--------- |
| Lead Engineer   | [Name]           |     ☐ Proposed      | YYYY-MM-DD |
| Studio Director | Dr. Marcus Vogel |     ☐ Accepted      | YYYY-MM-DD |
| CEO             | User             | ☐ Approved (locked) | YYYY-MM-DD |
