# Architecture Decision Record (ADR) — Template

| Field             | Value                                                                  |
| ----------------- | ---------------------------------------------------------------------- |
| **Document Type** | Authoritative ADR template                                             |
| **Scope**         | All Stage 3 architecture decisions across all product pipelines        |
| **Owner**         | Software Architect (template); per-ADR owner is the authoring engineer |
| **Effective**     | First Stage 3 entry post-publication                                   |
| **Cross-Refs**    | Base pipeline Stage 3 · `_base/independent-challenge-template.md`      |

---

## 1. Purpose

An ADR captures **one architecturally significant decision**, the context that forced the decision, the alternatives considered, the choice made, and the consequences accepted. ADRs travel with the codebase; they are the durable record of why the system looks the way it does.

This template replaces the legacy "ADRs are locked at Stage 3 and not revisable" rule with a **versionable + supersedable** model: ADRs are mutable in the sense that a new ADR can supersede an old one, with full provenance, but the old ADR is never deleted. The ledger of decisions remains intact.

---

## 2. When to Author an ADR

Author one ADR per decision that meets **any** of the criteria below:

| Criterion                                                   | Examples                                                                         |
| :---------------------------------------------------------- | :------------------------------------------------------------------------------- |
| Hard to reverse later                                       | Database engine choice, primary programming language, deployment topology        |
| Affects multiple teams                                      | API protocol (REST vs GraphQL vs gRPC), shared design system, cross-surface auth |
| Sets a precedent for future decisions                       | First use of a new pattern (e.g., first event-sourced service)                   |
| Locks in a third-party dependency for ≥ 1 year              | Cloud provider, payments processor, CDN, observability stack                     |
| Encodes a security or compliance position                   | Encryption suite, key management, data residency, biometric storage              |
| Trades a clear non-functional axis (perf, cost, complexity) | Caching strategy, cold-start optimisation, replication topology                  |

Decisions that do **not** meet any of these criteria do not require an ADR; they belong in code comments or in the Stage 4 Implementation Plan.

---

## 3. Mandatory ADRs at Stage 3

These ADRs are produced for every project at Stage 3, in addition to project-specific ones:

1. **String Key Taxonomy ADR** — locks the naming convention for all localised strings.
2. **Security Architecture ADR(s)** — crypto, secure storage, certificate pinning, surface-specific security patterns.
3. **Strategy ADR** (one of, depending on product type):
   - Mobile: **Platform Strategy ADR**
   - Web: **Web Rendering ADR**
   - Backend: **API Protocol ADR**
   - Full-stack: **Composition Strategy ADR**

Per-product `delta.md` files may add additional mandatory ADRs (see each delta's Stage 3 section).

---

## 4. Template

Author one Markdown file per ADR at `company/project/<project>/architecture/adr-NNN-<slug>.md` (or the studio equivalent).

```markdown
# ADR-NNN — <decision title>

| Field            | Value                                                             |
| :--------------- | :---------------------------------------------------------------- |
| ADR ID           | ADR-NNN (zero-padded; monotonically increasing per project)       |
| Status           | Proposed / Accepted / Superseded / Deprecated                     |
| Date             | YYYY-MM-DD (date this status was set)                             |
| Author(s)        | <names + roles>                                                   |
| Reviewers        | CTO / CIO / CSO / surface lead — all reviewers who signed         |
| Supersedes       | <ADR-IDs this record supersedes, or "none">                       |
| Superseded by    | <ADR-ID, set when this record is later superseded; otherwise "—"> |
| Linked artifacts | PRD section / SRD section / UML diagram(s) / TSD comparison       |
| Project          | <project name + path>                                             |
| Surface          | mobile / web / backend / full-stack / studio                      |

## 1. Context

What forced the decision. What was happening in the project that demanded a choice. Cite the relevant PRD requirement (REQ-NNN) or SRD requirement (SEC-NNN) or quality attribute that the decision must serve.

## 2. Decision

The single decision, stated in one declarative sentence. ("We will use PostgreSQL 16 as the primary OLTP datastore for the order service.")

## 3. Alternatives considered

At least two real alternatives were evaluated. For each:

| Alternative | Pros | Cons | Why not chosen |
| :---------- | :--- | :--- | :------------- |

Listing only one alternative ("we considered doing nothing") is not acceptable.

## 4. Consequences

The outcomes the team accepts by making this decision. Include both positive and negative; an ADR with no negative consequences is incomplete.

| Type     | Consequence                                                                                 |
| :------- | :------------------------------------------------------------------------------------------ |
| Positive | <e.g. "single source of truth for order data; well-understood operational profile">         |
| Positive | ...                                                                                         |
| Negative | <e.g. "limited horizontal scale beyond ~50K TPS; will require sharding strategy by Year 2"> |
| Negative | ...                                                                                         |
| Neutral  | <e.g. "engineering team gains expertise in pgvector for future ML feature work">            |

## 5. Success criteria

Measurable conditions under which this decision is considered to have worked. Reviewed at the next QBR after the deciding system goes live.

| Criterion                             | Threshold | Measurement source        |
| :------------------------------------ | :-------- | :------------------------ |
| <e.g. "P99 query latency under load"> | ≤ 50 ms   | <observability dashboard> |

## 6. Failure criteria

Measurable conditions under which this decision must be revisited (i.e., a successor ADR drafted).

| Criterion                            | Threshold             | Measurement source        |
| :----------------------------------- | :-------------------- | :------------------------ |
| <e.g. "P99 query latency sustained"> | > 200 ms over 14 days | <observability dashboard> |

## 7. Rollback plan (mandatory if Status transitions to Superseded)

The successor ADR cites this section. Includes:

1. **Pre-conditions for rollback** (data migration completeness, dual-write window, etc.)
2. **Rollback steps** (ordered, with owner per step)
3. **Validation** (how we know rollback succeeded)
4. **Cost** (engineering effort, customer-visible impact, financial)

If no rollback plan can be authored, the decision is by definition irreversible; the ADR §4 Negative Consequences must say so explicitly.

## 8. References

External standards, RFCs, vendor docs, internal precedents.

## 9. Document version history

Per-ADR change log. Required even if there is only the initial entry.
```

---

## 5. Lifecycle and Statuses

```text
                    ┌────────────┐
              ┌────►│  Proposed  │  draft under review by CTO + CIO + CSO
              │     └─────┬──────┘
              │           │ approved
              │     ┌─────▼──────┐
              │     │  Accepted  │  in force; codebase implements this
              │     └─────┬──────┘
              │           │ superseded by ADR-MMM
              │     ┌─────▼──────┐
              │     │ Superseded │  durable record; codebase no longer follows
              │     └────────────┘
              │
              │     ┌────────────┐
              └─────│ Deprecated │  Accepted record withdrawn without successor
                    └────────────┘   (rare; explicit declaration that the
                                      decision no longer applies and no new
                                      decision is made)
```

**Supersession rules.**

1. A new ADR (ADR-MMM) supersedes an old one (ADR-NNN) by stating `Supersedes: ADR-NNN` in its header.
2. ADR-NNN's `Status` is updated to `Superseded` and `Superseded by: ADR-MMM` is set. The body of ADR-NNN is **not edited** beyond these header fields; the historical record is preserved.
3. ADR-NNN's §7 Rollback plan must exist before supersession is filed; if it doesn't, the supersession itself triggers the §7 authoring as a P0 prerequisite.
4. Supersession is a Stage 3 re-entry **minimum** — the new ADR follows the same review path as a new decision, including reviewers and any required Independent Challenge round.
5. **Implementation-Plan re-baseline is required** after supersession (Stage 4 re-entry), because the implementation plan was built against the old decision.

**Cross-pipeline cascade.** A superseded ADR may invalidate downstream artifacts (UML diagrams, IDS sections, test cases). The supersession PR must enumerate the affected downstream artifacts and create tracking issues for each. The supersession is not Accepted until the downstream tracking is in place.

---

## 6. Independent Challenge Requirement

An Independent Challenge round per `_base/independent-challenge-template.md` is **mandatory** before transition to `Accepted` for any ADR that meets **any** of the criteria:

- Locks in a third-party dependency with cost > $X / year (project-defined; never $0)
- Encodes a security position (any Security Architecture ADR)
- Affects more than one surface (cross-pipeline ADR)
- Supersedes a prior Accepted ADR

For other ADRs, the Independent Challenge is recommended but not required; the CTO sign-off on `Status: Accepted` substitutes.

---

## 7. Storage and Indexing

| Where                                                         | What                                                                  |
| :------------------------------------------------------------ | :-------------------------------------------------------------------- |
| `company/project/<project>/architecture/adr-NNN-<slug>.md`    | Per-project ADR                                                       |
| `company/project/<project>/architecture/INDEX.md`             | Index of ADRs in the project (auto-generated from filenames + status) |
| `studio/<studio>/projects/<project>/architecture/adr-NNN-...` | Studio-scoped ADR                                                     |
| `_base/adr-template.md` (this file)                           | Universal template; revisions follow the freeze rule for base files   |

---

## 8. Document Version History

| Version | Date           | Author             | Changes                                                                                                                                                                                                                                                                                                       |
| :------ | :------------- | :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | April 21, 2026 | Software Architect | Initial publication. Replaces the legacy "ADRs locked at Stage 3" rule. ADRs are versionable: a new ADR may supersede an old one. `Supersedes` and `Superseded by` header fields are mandatory. §7 Rollback plan is mandatory before supersession. Independent Challenge required for high-blast-radius ADRs. |
