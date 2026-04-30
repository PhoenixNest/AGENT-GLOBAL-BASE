# Pattern: Paired Artifacts

| Field        | Value                               |
| ------------ | ----------------------------------- |
| **Category** | Pipeline Governance · Quality Gates |
| **Layer**    | Cross-cutting (Layers 1 + 3)        |
| **Status**   | Ratified — ADR-ASE-001              |

---

## Problem

Critical concerns — security, compliance, accessibility, performance — are consistently
treated as afterthoughts when they have independent artifact lifecycles from the features
they govern. A Product Requirements Document (PRD) that proceeds through a pipeline
without its Security Requirements Document (SRD) produces a feature that is functionally
complete but security-unreviewed. Security is then bolted on at the end, at high cost,
or skipped entirely.

The root cause is **artifact independence**: if related documents can exist separately,
they will exist separately, and the coupling between them degrades over time.

---

## Solution

**Pair critical artifacts** so that they always travel together through the pipeline.
A gate cannot pass a primary artifact unless its paired artifact exists, is current,
and is consistent with it.

A **Paired Artifact** is a document that is:

- Always created alongside its primary artifact
- Always updated when its primary artifact changes
- Always reviewed together in the same gate
- Non-separable — passing one without the other is a gate violation

---

## Standard Pairings in This Organisation

| Primary Artifact  | Paired Artifact                     | Governs                                      |
| ----------------- | ----------------------------------- | -------------------------------------------- |
| PRD               | SRD (Security Requirements Doc)     | Security posture of every feature in the PRD |
| Architecture Doc  | Threat Model                        | Attack surface of the proposed architecture  |
| API Specification | Authentication & Authorisation Spec | Access control for every API endpoint        |
| Agent Identity    | Forbidden Behaviours List           | Anti-pattern firewall for every agent role   |
| Release Candidate | Compliance Audit Report             | ASE compliance status before production      |

---

## How to Apply

### Step 1: Identify the pairing at artifact creation

When a primary artifact is created, immediately create its pair. The pair does not need
to be complete on Day 1 — a stub with defined structure is sufficient — but it must
exist. A primary artifact with no pair is immediately flagged as a P1 gap.

### Step 2: Enforce joint gating

Pipeline gates check both artifacts. Gate criteria:

```
Gate passes if:
  primary_artifact.status == "approved"
  AND paired_artifact.status == "approved"
  AND paired_artifact.last_updated >= primary_artifact.last_updated
```

If the primary artifact was updated after the pair's last review, the gate holds until
the pair is updated and re-reviewed.

### Step 3: Co-author, not sequential

Paired artifacts should be developed in parallel, not sequentially. The security
engineer and the product manager draft their respective documents simultaneously —
not the security engineer waiting for the PRD to be "done." This surfaces conflicts
early, when they are cheap to resolve.

### Step 4: Version-lock pairings

When one artifact in a pair is versioned (e.g., PRD v1.2), the paired artifact carries
the same version marker. A PRD v1.2 paired with an SRD v1.0 is a mismatch — the SRD
must be updated to v1.2 before the gate.

---

## In Multi-Agent Pipelines

In a multi-agent pipeline, each agent that produces a primary artifact must also update
its paired artifact before passing the gate. This is enforced via the Harness Layer's
quality gate mechanism.

Example: The CPO Agent produces a PRD update. Before the gate agent approves passage
to the next stage, it checks:

1. PRD version exists and is approved ✓
2. SRD exists and version-matches the PRD ✓
3. Both are consistent (no unaddressed security requirements in PRD without SRD entry) ✓

---

## Consequences

**Benefits:**

- Security and compliance are woven into the delivery process, not appended at the end
- Gate failures are caught early — a missing SRD at Stage 2 is far cheaper than a
  security review failure at Stage 8
- Every critical artifact has a traceable companion document through the full pipeline

**Trade-offs:**

- Increases documentation burden — every primary artifact requires a maintained pair
- Requires author discipline to keep pairs in sync after updates
- May slow early-stage exploration where pairing overhead is high relative to value

---

## Related Patterns

- [`canonical-source-of-truth.md`](./canonical-source-of-truth.md) — Each artifact in
  a pair derives its authority structure from the canonical source
- [`defect-severity-vocabulary.md`](./defect-severity-vocabulary.md) — Used to classify
  gaps found when pairing is violated
- [`progress-sync-protocol.md`](./progress-sync-protocol.md) — Detects when a pair
  falls out of sync during long-running pipeline execution

## CC-00 References

- `core-component-00/harness-engineering/` — Quality gate implementation patterns
- `core-component-00/multi-agent-engineering/patterns/orchestration-patterns.md` —
  Pipeline pattern governs artifact gating between stages
