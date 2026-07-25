# [Research Report Title]

<!-- Copy this file to academic-neural-unit-00/knowledge-base/YYYY-MM-DD-<slug>/research-report.md.
     The folder and this file are opened at CHARTER time, before findings exist
     (research-programme-chartering.md §6) — an opened report with empty findings sections is the
     correct state for a programme in progress, not an unfinished document.

     Point-in-time record. A materially different finding is a new dated entry with a cross-
     reference, not an edit to this one (root templates/README.md § Usage). -->

**Programme slug:** [`YYYY-MM-DD-<slug>`]
**Charter:** [`./charter.md`]
**Primary owner:** [Name, ANU-00 role]
**Contributors:** [Names and what each covered, or "None"]
**Status:** [Opened at charter / In progress / Complete]
**Report date:** [YYYY-MM-DD]

---

## 0. Ingestion Metadata

<!-- Filled at ingestion by the author, checked by Tobias Lindqvist
     (knowledge-base-ingestion-architecture.md). Cross-references are recorded BIDIRECTIONALLY at
     ingestion time, not as a later cleanup pass (§3 of that skill) — when you add a row to
     "Cites / extends" below, add the reciprocal row to the cited entry in the same sitting. -->

| Field               | Value                                                                                                                                                                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Taxonomy category   | [Category. If this entry does not fit cleanly, resolve the taxonomy gap with the Knowledge Systems Engineer BEFORE ingesting — never force-fit.]                                                                                               |
| Charter field tags  | [Tag **every** charter field this entry touches, not only the primary one, so it surfaces under any relevant taxonomy lookup — `cross-domain-literature-synthesis.md` §5]                                                                      |
| Claim types present | [Theoretical / Empirical / Both]                                                                                                                                                                                                               |
| Finding polarity    | [Positive / Negative / Mixed / Inconclusive — a negative finding is a complete finding, see §6]                                                                                                                                                |
| Observation records | [Count and IDs of records in `./observations/`, or "None" — e.g. "4 (OBS-01–04)". These are the raw reproducible incidents behind the claims in §4; an observation is not itself a finding until it clears that register's evidence standard.] |

**Cross-references:**

| Direction    | Entry                 | Relationship                         |
| ------------ | --------------------- | ------------------------------------ |
| This cites → | [`YYYY-MM-DD-<slug>`] | [Extends / Replicates / Contradicts] |
| ← Cited by   | [`YYYY-MM-DD-<slug>`] | [Reciprocal row added there? Yes/No] |

---

## 1. Plain-Language Summary

<!-- REQUIRED on every entry, not only technical-domain ones. neural-systems-research-design.md §4
     is explicit: every finding must include a plain-language summary accessible to a reader outside
     the specialty, IN ADDITION to the full technical treatment — do not publish technical-only.
     Write this section for a colleague in a different charter field. -->

[Three to six sentences. What was asked, what was found, and what it means — no notation, no
undefined jargon.]

---

## 2. Research Question and Charter Reference

**Question:** [Restate verbatim from the charter, §2.]

**Falsifiability condition as chartered:** [Restate verbatim from the charter, §3.]

**Was it met?** [Was the disproof condition triggered, not triggered, or was the study unable to
test it? Answer this plainly before presenting any evidence.]

---

## 3. Prior Literature

<!-- Grounding in existing literature comes BEFORE original work — neural-systems §2, learning-
     theory §4, software-engineering-research-design §3. Replication and extension are valued
     outcomes here, not lesser ones; say plainly if that is what this is. -->

**Was this question already answered, in whole or in part?** [Yes / Partially / No — and what that
implies for this programme's contribution.]

**This entry's contribution type:** [Original investigation / Extension / Independent replication /
Synthesis]

### 3.1 Source Ledger

<!-- One block per charter field involved. cross-domain-literature-synthesis.md §2 is binding here:
     each field's claims are sourced at THAT field's own rigor bar. Do not lower the bar for the
     field outside your primary depth — route the depth gap to the specialist instead (§3 of that
     skill), and name them in the charter's §6. -->

| Charter field | Key sources | Rigor bar applied                       | Depth gap? Routed to |
| ------------- | ----------- | --------------------------------------- | -------------------- |
| [Field]       | [Citations] | [What standard was held for this field] | [Name, or "None"]    |

---

## 4. Claim Register

<!-- The evidence-standard firewall. Baek §3 and Okonkwo §3 both require stating WHICH KIND of
     claim is being made before presenting supporting evidence — a generalization-bound argument and
     an empirical result are not interchangeable evidence types. Dubois §2 adds a second axis for
     LLM work: emergent-capability claims and engineered-behavior claims are different research
     objects and must be kept apart explicitly in every write-up. -->

| #   | Claim       | Type                                                                                | Evidence offered                                              |
| --- | ----------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| C1  | [The claim] | [Theoretical / proof-style · Empirical · Emergent-capability · Engineered-behavior] | [Formal bound / systematic evaluation set / observed pattern] |

**Assumption set and regime of applicability** (required for any theoretical claim —
`learning-theory-research-design.md` §1):

[State the assumptions and the regime in which the claim holds. A claim stated without these is not
falsifiable and should not have been chartered.]

**Metric, population, effect size and confidence** (required for any empirical
software-engineering claim — `software-engineering-research-design.md` §1, §4):

| Claim | Metric              | Population  | Effect size (magnitude)         | Confidence         |
| ----- | ------------------- | ----------- | ------------------------------- | ------------------ |
| [C#]  | [What was measured] | [Over what] | [Magnitude, not just direction] | [Interval / level] |

<!-- "Significant / not significant" alone does not satisfy §4. Report magnitude and confidence. -->

---

## 5. Method

<!-- Fill in the subsections relevant to this programme's domain; delete the rest. Each carries a
     named requirement from a crew skill file — these are not generic methods boilerplate. -->

### 5.1 Evaluation design

[**Design against anecdote, not for it** (`llm-behavior-evaluation-design.md` §3): describe the
systematic evaluation set. A handful of impressive examples is not evidence.]

### 5.2 Conditions and non-conditions

[**Report emergence conditions, not just the phenomenon** (`agent-coordination-theory-research.md`
§4): state the agent population, environment, and observation criteria — and explicitly, under what
conditions the phenomenon does **not** occur. "It emerges" without that is an incomplete finding.]

### 5.3 Feasibility bar

[**State the bar before evaluating** (`applied-ai-feasibility-research.md` §1): the cost/benefit
threshold against which "worth pursuing" is judged. Concluding "promising" without a stated
threshold is not a finding.]

### 5.4 Domain coverage

[**Test across more than one application domain where possible**
(`applied-ai-feasibility-research.md` §3): if the result holds in only one narrow domain, say so
explicitly here rather than letting the summary generalize past its evidence.]

### 5.5 Cross-field decomposition

[**Decompose before synthesizing** (`cross-domain-literature-synthesis.md` §1): list the per-field
sub-claims and confirm each was found independently sound before any combined claim was stated in
§6. A merged claim that silently conflates two fields' evidence standards is the named failure mode
this section exists to prevent.]

---

## 6. Findings

### 6.1 What was found

[The result, stated against the claim register in §4 — one subsection or paragraph per claim.]

### 6.2 Failure modes and negative results

<!-- REQUIRED, not optional, and not a weakness section. dubois §3 requires failure modes reported
     alongside successes. tan §4 is explicit that "this technique is not worth pursuing given the
     current bar" is a COMPLETE, valuable finding — do not present it as an incomplete programme,
     and do not pad it to look like more. -->

[Where it did not hold, what failed, and — for a negative or null result — a plain statement that
this is the programme's finding, not a shortfall in it.]

### 6.3 Cross-field implication

[Only for cross-field programmes, and only after §5.5 confirms each field's sub-claims are
independently sound: state the combined finding and its cross-field implication explicitly. This is
the value a generalist adds that a single-field specialist cannot —
`cross-domain-literature-synthesis.md` §4.]

---

## 7. Boundary Restatement and Referrals

<!-- Re-checked at publication, not only at charter. Roldán §2, Fujimori §2, and Dubois §4 all
     require the boundary check at the point the finding is written up, because that is where scope
     creep actually happens: a finding that leads naturally to "so we should build a reusable
     pattern for this" is a REFERRAL, never ANU-00 implementing it. -->

**Stage of inquiry, restated:** [One sentence — this entry reports pre-implementation findings; it
does not deliver a production pattern, module, or reusable framework.]

**Referrals raised by this finding:**

| #   | What is being referred | Why it is out of ANU-00 charter       | Referral note path   |
| --- | ---------------------- | ------------------------------------- | -------------------- |
| 1   | [Tooling / pattern]    | [Post-validation implementation work] | [`../referrals/...`] |

<!-- A referral is a record that a need exists. It is not an assignment, a commitment, or a
     handshake — ANU-00 does not take delivery dates from it and does not track it to completion. -->

---

## 8. Open Questions Raised

[Questions this programme surfaced but did not answer. Each one that lacks a falsifiability
condition goes to `knowledge-base/open-question-log.md` — add it there in the same sitting, and
reference the OQ number here.]

| Question | Logged as | Falsifiable yet?                               |
| -------- | --------- | ---------------------------------------------- |
| [Text]   | [OQ-NN]   | [Yes → candidate for chartering / No → parked] |
