# Referral Note — [Short Title of the Referred Need]

<!-- Copy to academic-neural-unit-00/knowledge-base/YYYY-MM-DD-<slug>/referrals/<short-slug>.md,
     alongside the report that raised it.

     WHAT THIS DOCUMENT IS: a record that a production-engineering need was discovered during
     ANU-00 research and is being scoped OUT, so it does not silently become ANU-00 work.

     WHAT IT IS NOT: a task, a request, a ticket, or a commitment from anyone. ANU-00 does not
     assign this, does not track it to completion, and does not accept a delivery date against it.
     Filing this note discharges ANU-00's obligation entirely. If a referral note is ever used to
     negotiate scope or schedule with CC-00, it has been misused — escalate to Dr. Mokoena. -->

**Filed:** [YYYY-MM-DD]
**Filed by:** [Name, ANU-00 role]
**Raised during:** [`YYYY-MM-DD-<slug>`] — [charter §7 / report §7]
**Countersigned:** Dr. Naledi Mokoena, ANU-00 Lead — [YYYY-MM-DD]

---

## 1. The Need

[One paragraph. What capability, tooling, or pattern would be required — described as a need, not
as a specification. Writing a specification here would itself be doing the post-validation work
this note exists to decline.]

---

## 2. Why It Is Out of ANU-00's Charter

<!-- software-engineering-research-design.md § What This Skill Does Not Cover: building tooling
     described in a finding as a reusable pattern is a production-engineering deliverable, out of
     ANU-00's charter ENTIRELY — noted as a referral, not as ANU-00 output. -->

**Stage-of-inquiry placement:** [Post-validation — "given that it works, how do we build it
reliably." State it plainly.]

**Reusable-vs-one-off test** (`agent-coordination-theory-research.md` §3):

- [ ] A one-off instrumentation harness would suffice → **not a referral**; build it inside the
      programme and delete this note.
- [ ] A reusable framework, module, or maintained tool is required → **referral**, continue below.

**Named boundary:** [Which CC-00 module or mandate this would fall under, by name — e.g.
`core-component-00/framework/05-multi-agent-engineering/`. Name it; do not write "production
engineering" generically.]

---

## 3. What ANU-00 Did Instead

[How the research question was answered — or bounded — without building the referred thing. If the
question could not be fully answered without it, say so: a partially-answered question with an
honest boundary is a better record than an answer obtained by quietly stepping over the charter.]

---

## 4. Disposition

| Field                           | Value                                                                      |
| ------------------------------- | -------------------------------------------------------------------------- |
| Recorded in the research report | [Yes — §7, row #N]                                                         |
| Communicated to anyone?         | [No — filed as a record only / Yes — state to whom and on whose authority] |

<!-- The default is "No." A referral note is a record in ANU-00's own knowledge base. Routing one to
     CC-00 as a work item is a decision only the CEO or Dr. Mokoena makes, explicitly, and it must
     be recorded above with the reasoning — never done as routine housekeeping. -->
