# CC-00 — Laboratory Crew

Personnel roster for the Core Component 00 applied research laboratory.

| Directory                                                            | Purpose                                                                                          |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [director/](./director/)                                             | Dr. Elias Vance — Laboratory Director                                                            |
| [research-science/](./research-science/)                             | Dr. Amara Nwosu-Chen — Staff Research Scientist                                                  |
| [safety-evaluation/](./safety-evaluation/)                           | Dr. Tomasz Wieczorek — Staff Safety & Evaluation Engineer                                        |
| [infrastructure/](./infrastructure/)                                 | Ravi Deshmukh — Infrastructure Engineer                                                          |
| [context-engineering/](./context-engineering/)                       | Mei-Ling Zhao — Senior Research Engineer · Hana Kobayashi — Senior Research Engineer II          |
| [harness-engineering/](./harness-engineering/)                       | Kwame Asante — Senior Research Engineer · Connor O'Malley — Senior Research Engineer II          |
| [retrieval-augmented-generation/](./retrieval-augmented-generation/) | Sofia Almeida — Senior Research Engineer · Diego Fontán — Senior Research Engineer II            |
| [multi-agent-engineering/](./multi-agent-engineering/)               | Dr. Idris Farouk — Staff Research Engineer, MAE Lead · Amina Yusuf — Senior Research Engineer II |

**Recruitment is complete — Phases 1–3.** All 11 Research crew FTEs have been hired through the
full 9-stage pipeline (`company/pipeline/recruitment/pipeline.md`), cycle
`company/recruitment/core-component-00-fy2026-q3/`. The lab now has bus factor 2 on all four
production-grade modules (Context, Harness, RAG, Multi-Agent), an independent Research Scientist
and Safety & Evaluation function, and dedicated Infrastructure support. Prompt Engineering remains
directly held by Dr. Vance as a documentation-only module with no test infrastructure. Total lab
headcount: 12 (Director + 11 hires).

---

## Composition Assessment — Dr. Elias Vance (2026-07-03)

> **Superseded (2026-07-03, same day).** The Verdict below concluded the lab should not expand
> further this quarter. The CEO reviewed this assessment, disagreed with "postpone" as the answer
> to real structural gaps, and directed a Phase 3 expansion that closes all four gaps identified
> below — bus factor, Research Scientist tier, safety/eval function, infra support — within the
> current cycle. That decision and its rationale are recorded in
> `company/recruitment/core-component-00-fy2026-q3/recruitment-plan.md` (v1.1–v1.3). The original
> reasoning below is left intact as the honest record of what I actually assessed at the time —
> superseding it is not the same as it having been wrong on the facts; the CEO weighed the same
> facts and set a different bar for urgency than I did.

Reviewed against the standard I'd apply to any lab I'd call top-tier: Anthropic, DeepMind,
OpenAI. I read each profile and skills index in this crew before writing this, not just the
headcount table.

### What holds up

| Dimension                  | Finding                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Module coverage**        | All four coded modules (Context, Harness, RAG, Multi-Agent) now have a named implementation owner with a production track record in that exact problem — Zhao shipped a 4-tier memory store at Cohere, Asante built Stripe's recovery layer, Almeida led Elastic's fusion ranking, Farouk built Anthropic's own swarm orchestration. This is hire-for-precedent, not hire-for-potential. |
| **Vetting integrity**      | All four cleared their tier floor with margin (18–19/20 against 17–18/20 floors), zero conditional approvals, zero red flags. The bar was not softened to hit a headcount target.                                                                                                                                                                                                        |
| **Leadership sequencing**  | Staggering Farouk (L4) first so he could bar-raise the three IC hires is the correct pattern — it's how Amazon and Anthropic actually run senior-first hiring, not an invented formality.                                                                                                                                                                                                |
| **Honest-gaps discipline** | Every profile documents what its owner is _not_ — Zhao defers to Asante on harness, Almeida defers to Farouk on orchestration, and so on. That's the difference between a team and four soloists sharing a floor plan.                                                                                                                                                                   |

### What does not yet hold up

| Gap                                                     | Why it matters at top-tier standard                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bus factor of 1 per module, still**                   | We went from bus factor 1 (me, across five modules) to bus factor 1 per module, four times over. No module has a second engineer who could cover an absence, a departure, or a surge in scope. Top-tier labs pair every critical system with at least a primary and a secondary. This is a real regression risk, not a solved problem.                                                                                                                                                          |
| **No Research Scientist tier, only Research Engineers** | Every hire is credentialed for production implementation (and in Almeida's and Farouk's cases, has genuine PhD research depth) but is leveled and scoped as an engineer executing against my research programmes, not as an independent PI. A lab I'd call top-tier eventually needs at least one Research Scientist who can originate a research question, not just execute one I hand them. Today that's fine — the programmes are mine and early-stage — but it won't scale past this cycle. |
| **No dedicated safety/eval function**                   | ASE compliance execution now sits with Farouk (correctly, as a delegated _execution_ role), but there is no crew member whose sole mandate is red-teaming, adversarial evaluation, or safety regression testing across all four modules. Right now that's still entirely on me.                                                                                                                                                                                                                 |
| **No infra/MLOps support**                              | Almeida's RAG module carries the lab's heaviest dependency footprint (GPU, spaCy, vector indices) with no dedicated infrastructure engineer. She'll absorb that overhead herself, which is a tax on a Senior IC's actual research time.                                                                                                                                                                                                                                                         |

### Verdict

**The composition is sufficient for this quarter and should not be expanded further right now.**
Four hires in one cycle already took the lab from 1 to 5 — adding more headcount before this crew
has shipped anything together would be premature scaling, not rigor. The gaps above (bus factor,
research-scientist tier, safety function, infra support) are real and I am logging them, but none
of them block current operations: every module has an owner today, and I retain ASE ratification,
cross-module architecture, and Prompt Engineering directly.

**Recommendation, not a request:** revisit bus-factor and a Research Scientist hire at the next
quarterly configuration cycle (`company/pipeline/recruitment/pipeline.md` § Quarterly
Configuration Cycle) once this crew has a shipped track record to hire against — hiring a second
engineer per module now, before we know where the actual load concentrates, would be guessing.
