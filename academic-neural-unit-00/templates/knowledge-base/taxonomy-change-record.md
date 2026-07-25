# ANU-00 Knowledge Base — Taxonomy Change Record

<!-- Copy this file once to academic-neural-unit-00/knowledge-base/taxonomy-change-record.md. There
     is exactly ONE instance for the whole knowledge base.

     APPEND-ONLY. Every taxonomy revision gets a new numbered section at the bottom; prior sections
     are never edited or removed. This is the durable answer to
     knowledge-base-ingestion-architecture.md §5 — "no silent taxonomy drift": if the taxonomy
     changes, existing entries are re-tagged EXPLICITLY and the change is logged. Old and new
     taxonomy versions must never coexist silently. -->

**Owner:** Tobias Lindqvist, Knowledge Systems Engineer
**Ratified by:** Dr. Naledi Mokoena, ANU-00 Lead (taxonomy is part of knowledge-base structure)
**Opened:** [YYYY-MM-DD]
**Convention:** Append-only

---

## 1. Current Taxonomy

<!-- The one authoritative statement of the taxonomy as it stands right now. This section IS
     rewritten on each change — it is the current-state view — but every rewrite must be accompanied
     by a new §2 entry recording what changed. A §1 edit with no matching §2 entry is exactly the
     silent drift this document exists to prevent. -->

**Version:** [vN]
**In force since:** [YYYY-MM-DD]

| Category | Definition                             | Example entry         |
| -------- | -------------------------------------- | --------------------- |
| [Name]   | [What belongs here, and what does not] | [`YYYY-MM-DD-<slug>`] |

---

## 2. Change Log

<!-- Newest at the bottom. One section per revision. -->

### TX-[NN] — [Short description of the change]

**Date:** [YYYY-MM-DD]
**Version:** [v(N-1) → vN]
**Proposed by:** [Name] — **Ratified by:** Dr. Naledi Mokoena, [YYYY-MM-DD]

**Trigger:** [Usually: a new entry did not fit the current taxonomy cleanly. Per
`knowledge-base-ingestion-architecture.md` §1, taxonomy gaps are resolved BEFORE the entry is
ingested — never by force-fitting it into an existing category. Name the entry that triggered this.]

**What changed:**

| Change type                                           | Detail      |
| ----------------------------------------------------- | ----------- |
| [Added / Renamed / Split / Merged / Removed category] | [From → to] |

**Re-tagging performed** — mandatory, explicit, and completed before this record is closed:

| Entry                 | Old category | New category | Re-tagged on |
| --------------------- | ------------ | ------------ | ------------ |
| [`YYYY-MM-DD-<slug>`] | [Old]        | [New]        | [YYYY-MM-DD] |

- [ ] Every affected entry above has been re-tagged. No entry remains on the previous taxonomy
      version.

**Tooling note:** [If any ingestion automation reads the taxonomy, state whether it was updated in
the same change. Per `knowledge-base-ingestion-architecture.md` §1, automation is never built
against a taxonomy that has not stabilized — if the taxonomy is still moving, say so and leave the
automation unbuilt rather than chasing it.]
