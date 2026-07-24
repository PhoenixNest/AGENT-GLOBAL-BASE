# Skill: Research Programme Chartering

**Owner:** Dr. Naledi Mokoena, ANU-00 Lead
**Purpose:** Define how Academic Neural Unit 00 originates, scopes, and ratifies a new research
programme independent of any external agenda — the capability that distinguishes ANU-00 from a
team executing someone else's research plan.

---

## When to Use

Any time a new research question is proposed — by Dr. Mokoena, by one of the 3 Research
Scientists, or surfaced from the knowledge base's own literature synthesis — before it is treated
as an active ANU-00 programme.

## Process

1. **Origination.** State the research question in one sentence. It must be answerable by primary
   academic research (literature synthesis, theoretical analysis, or original investigation) in
   one of ANU-00's four charter fields: computer science, artificial intelligence, neural
   networks, software engineering.
2. **Falsifiability check.** State what result would prove the question's working hypothesis
   wrong. A programme without a falsifiable failure condition is not chartered — it is logged as
   an open question for later refinement instead.
3. **Boundary check — apply the stage-of-inquiry test.** Per the CEO-approved charter refinement
   (`formation-report.md` §3.1), ask whether the question is pre-implementation ("does this work /
   is it worth building" — ANU-00's charter) or post-validation ("given that it works, how do we
   build it reliably" — CC-00's charter). Judge by stage of inquiry, not by which field's
   vocabulary the question uses — "investigate emergent multi-agent coordination behavior" is
   ANU-00 under this test even though it shares vocabulary with CC-00's
   `multi-agent-engineering/`; "harden a coordination pattern into a reusable orchestration module"
   is CC-00, for the same reason. If a question requires building production tooling to answer,
   scope only the research component as ANU-00's programme and note the tooling need separately as
   a referral, not as ANU-00 scope.
   - **Migrate-vs-task distinction, binding:** a finding migrating from an ANU-00 programme into a
     future CC-00 initiative is ordinary research uptake and does not require ratification beyond
     normal chartering. ANU-00 being tasked by CC-00, Dr. Vance, or the CEO to de-risk a specific
     item already on CC-00's roadmap, on request, recreates the "direct link" the CEO's original
     ruling (`formation-report.md` §2) prohibits — decline or escalate to the CEO rather than
     chartering it as an ordinary ANU-00 programme.
4. **Ownership assignment.** Assign a lead researcher from the 3 Research Scientists (or Dr.
   Mokoena herself) based on domain fit. Cross-field programmes may have a primary owner plus a
   named contributor from an adjacent specialty.
5. **Ratification.** Dr. Mokoena signs off on every chartered programme — this is not delegable,
   since programme direction is the Lead's core mandate per her Assigned Role.
6. **Archive entry.** Once chartered, the programme gets a dated knowledge-base entry following the
   workspace's `YYYY-MM-DD-<slug>/research-report.md` convention, opened at charter time even
   before findings exist, so the programme is discoverable from the moment it starts.

## What This Skill Does Not Cover

- Evaluating whether a specific literature synthesis meets quality bar — that is the individual
  Research Scientist's own research-design skill (see their respective `skills/*.md`).
- Knowledge-base ingestion tooling — that is the Knowledge Systems Engineer's mandate
  (`skills/knowledge-base-ingestion-architecture.md`).
- ASE compliance for any LLM-powered tooling a programme might require — ASE governance applies
  workspace-wide regardless of this chartering process; consult
  `core-component-00/agent-systems-engineering/governance/` for the standard itself (a technical
  reference, not a CC-00 organizational dependency).
