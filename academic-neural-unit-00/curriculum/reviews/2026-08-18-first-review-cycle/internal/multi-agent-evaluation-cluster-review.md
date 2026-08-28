# Internal Curriculum Review — Multi-Agent Systems & Evaluation Cluster

**Reviewer:** Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00
**Cluster reviewed:** Multi-Agent Systems & Evaluation
**Documents covered:**

- `academic-neural-unit-00/curriculum/introductory/07-introduction-to-multi-agent-systems.md`
- `academic-neural-unit-00/curriculum/introductory/08-why-and-how-we-evaluate-agents.md`
- `academic-neural-unit-00/curriculum/intermediate/07-multi-agent-communication-and-coordination-protocols.md`
- `academic-neural-unit-00/curriculum/intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md`
- `academic-neural-unit-00/curriculum/advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`
- `academic-neural-unit-00/curriculum/advanced/08-rigorous-agent-evaluation-statistical-methodology.md`

**Review date:** 2026-08-18
**Review pass:** Pass 1 — internal cluster review (first cycle)

---

## 0. Independence Declaration

**Did I author any document in this cluster?** No. My own curriculum assignments are
`introductory/06` and `intermediate/06` (Prompt & Context Engineering cluster). Per
`curriculum/README.md` §6's roster-confirmation table, I am the ratified Pass-1 reviewer for
exactly this cluster (Multi-Agent Systems & Evaluation), and I did not write, co-write, or edit
any of the six documents above before this review.

**Anything else that would compromise independence:** None. All six documents are authored by
colleagues (Dr. Kaito Fujimori, Dr. Mireille Dubois, Dr. Aditi Bhandari) with no reporting or
collaboration relationship on this specific content prior to this review.

---

## 1. Method

I am not restating the documents' own claims. For each document below I checked the material
directly before signing this.

| What I did                                | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Independent sources consulted             | 15 distinct external sources opened/resolved myself via WebSearch or WebFetch this session (not just checked against the author's own quotation): Wooldridge's _An Introduction to MultiAgent Systems_ (2nd ed. metadata), Hayes-Roth (1985), Eugster et al. (2003), Smith (1980), FIPA ACL spec, Golchin & Surdeanu (2023), Mialon et al. GAIA (2023), Zhou et al. WebArena (2023), Liu et al. AgentBench (2023), Du et al. multiagent debate (2023/ICML 2024), Wang et al. Mixture-of-Agents (2024), Bowyer/Aitchison/Ivanova (2025), Dror et al. (2018), Yao et al. τ-bench/pass^k (2024), and Anthropic's "How We Built Our Multi-Agent Research System" blog post (fetched in full twice, with targeted follow-up on the exact paragraph containing the "90%" figure — this is what surfaced Problem #2 below). |
| Author-supplied citations opened          | 15 of 35 distinct external citations across the cluster independently resolved this session (42 citation instances counting same-source repeats across documents). The remaining 20 distinct citations (MMLU, ReAct, FIPA's own communicative-act vocabulary as used, AutoGen, Raft, the Byzantine Generals paper, Paxos Made Simple, FLP, self-consistency, Generative Agents, Wilson 1927, Efron & Tibshirani, Cohen 1960, Landis & Koch 1977, Chen et al. Codex/pass@k, Zheng et al. MT-Bench, Strathern 1997, plus the git-worktree Git reference docs) are canonical, extremely well-established references in this literature that I recognize with high confidence but did not re-fetch this session — flagged here honestly rather than claimed as freshly verified.                                         |
| Claims spot-checked against those sources | ~20 claims, selected worst-case-first: every claim carrying a specific number (question/task counts, accuracy percentages, benchmark composition) was prioritized over purely definitional claims, and every worked numerical example in the cluster (Wilson interval ×2, McNemar's test ×2, pass@k/pass^k ×1, Cohen's kappa ×1, Byzantine/Raft quorum arithmetic) was independently recomputed by hand from the stated formula, not merely read and accepted.                                                                                                                                                                                                                                                                                                                                                       |
| Chinese-language read                     | Read in full — every English and Chinese paragraph in all six documents, checked for EN¶→ZH¶ correspondence, calques, pinyin-for-term substitution, and unnatural idiom, not sampled.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

---

## 2. Per-Document Checklist

### 2.1 `introductory/07-introduction-to-multi-agent-systems.md`

**Author:** Dr. Kaito Fujimori

| #   | Check                                         | Verdict | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| --- | --------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Factual accuracy — independently spot-checked | Pass    | Wooldridge's MAS definition, attributed here as "systems composed of multiple interacting, autonomous agents... within a shared environment," is checked against the actual 2nd-edition textbook (confirmed via WebSearch: Wiley, May 2009, ISBN 978-0470519462) and matches the book's actual scope. Definitional claims (cooperation/coordination/competition; centralized/decentralized/hierarchical) are internally consistent with how `intermediate/07` and `advanced/07` later build on them without contradiction. |
| 2   | Citation validity                             | Pass    | Both external citations (Wooldridge 2009; Yao et al. 2022 ReAct, arXiv:2210.03629) resolve and are correctly represented.                                                                                                                                                                                                                                                                                                                                                                                                  |
| 3   | Pedagogical fit for a zero-background reader  | Pass    | Builds explicitly and only on `introductory/03`, `/04`, `/06` (all named). Every term (MAS, cooperation, coordination, competition, orchestrator, message passing, shared state, emergent behavior, cost multiplication, cascading errors, coordination overhead) is defined at first use. The Coder/Reviewer worked example (§5) is concrete and complete.                                                                                                                                                                |
| 4   | Bilingual quality (信达雅)                    | Pass    | Full read. Idiomatic, natural technical Chinese throughout; terminology consistently given as `term（术语）` on first use; no calque, pinyin-substitution, or stilted phrasing found anywhere in the document.                                                                                                                                                                                                                                                                                                             |
| 5   | Structural completeness                       | Pass    | `## References` / `**参考文献**` present with both subsections; both citations are actually used in-body; all seven internal cross-references (`03`, `04`, `06`, `intermediate/03`, `intermediate/07`, `advanced/04`, `advanced/07`) resolve to real files and are contextually appropriate.                                                                                                                                                                                                                               |

**Problems found in this document:** 0.

**Verdict:** Pass.

---

### 2.2 `introductory/08-why-and-how-we-evaluate-agents.md`

**Author:** Dr. Mireille Dubois

| #   | Check                                         | Verdict | Notes                                                                                                                                                                                                                                                                                                              |
| --- | --------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Factual accuracy — independently spot-checked | Pass    | MMLU description (57 subjects, multiple-choice) and the "Zheng et al. found >80% agreement" claim are accurate to well-established literature. Golchin & Surdeanu (2023) independently verified via WebSearch: correct authors, correct arXiv id (2308.08493), correct subject (LLM data-contamination detection). |
| 2   | Citation validity                             | Pass    | The three citations that are actually used in-body (Hendrycks MMLU, Zheng et al., Golchin & Surdeanu) are all correctly represented. See Problem #3 below re: the fourth listed citation.                                                                                                                          |
| 3   | Pedagogical fit for a zero-background reader  | Pass    | Task/metric/ground-truth/benchmark all defined before use; the five-task weather-agent worked example (§8) with an explicit pass/fail table is concrete and well-suited to a first encounter with evaluation.                                                                                                      |
| 4   | Bilingual quality (信达雅)                    | Pass    | Full read. No machine-like phrasing found.                                                                                                                                                                                                                                                                         |
| 5   | Structural completeness                       | Pass    | `## References` / `**参考文献**` present with both subsections; internal cross-references (`03`, `04`, `07`, `intermediate/08`, `advanced/08`) all resolve. See Problem #3 (§3 below) for one unused External Source.                                                                                              |

**Problems found in this document:** 1 (P3 — see §3, Problem #3).

**Verdict:** Pass. (The one recorded problem is P3/non-blocking per the verdict rule; every checklist row above is a genuine Pass.)

---

### 2.3 `intermediate/07-multi-agent-communication-and-coordination-protocols.md`

**Author:** Dr. Kaito Fujimori

| #   | Check                                         | Verdict        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --- | --------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Factual accuracy — independently spot-checked | Needs revision | The Anthropic (2025) "cut research time by up to 90%" claim is misattributed (see §3, Problem #2). Everything else independently checked out: FIPA ACL's performative vocabulary (confirmed against the actual spec, SC00061G), Contract Net Protocol mechanics (Smith 1980, IEEE Trans. Computers C-29(12):1104–1113 — confirmed exact venue/pages), blackboard architecture (Hayes-Roth 1985, confirmed AI 26(3):251–321), publish-subscribe's three decouplings (Eugster et al. 2003, confirmed ACM Comp. Surv. 35(2):114–131). |
| 2   | Citation validity                             | Fail           | The Anthropic 2025 citation misrepresents which mechanism produced the 90% figure and misstates the comparison baseline — see §3, Problem #2. This is exactly the failure mode the Method section's binding instruction warns against: the sentence structure attributes the number to the general design, when the source ties it to a specific, separately-described engineering optimization compared against a different baseline.                                                                                             |
| 3   | Pedagogical fit for a zero-background reader  | Pass           | Explicitly builds on and names `introductory/07`, `introductory/03`, `introductory/04`, and this author's own `intermediate/03`. Every new term (performative, Contract Net, blackboard, knowledge source, publish-subscribe, swarm topology) is defined at first use with a real citation. The three-agent worked example (§7) is thorough and internally consistent with the concepts introduced.                                                                                                                                |
| 4   | Bilingual quality (信达雅)                    | Pass           | Full read. No machine-like phrasing found; terminology handled consistently with the rest of the cluster.                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 5   | Structural completeness                       | Pass           | `## References` / `**参考文献**` present with both subsections; internal cross-references all resolve and are contextually apt. Structural shape is sound — the defect here is a citation-content error, not a structural one.                                                                                                                                                                                                                                                                                                     |

**Problems found in this document:** 1 (P1 — see §3, Problem #2).

**Verdict:** Needs revision — the Anthropic (2025) citation in §6 misattributes a real, verifiable figure to the wrong mechanism and the wrong comparison baseline.

---

### 2.4 `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md`

**Author:** Dr. Mireille Dubois

| #   | Check                                         | Verdict | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| --- | --------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Factual accuracy — independently spot-checked | Pass    | Independently verified via fresh WebSearch this session: GAIA (Mialon et al. 2023) — 466 questions, 92% human accuracy, both confirmed exactly; WebArena (Zhou et al. 2023) — 812 tasks, functional-end-state grading, confirmed; AgentBench (Liu et al. 2023) — eight environments, confirmed (the doc's illustrative subset "operating-system command lines, databases, and games" is a genuine subset of the real eight). Chen et al.'s pass@k formula and Cohen's kappa / Landis-Koch scale are stated in standard, correct form. |
| 2   | Citation validity                             | Pass    | All ten external citations independently spot-checked this session or cross-verified against well-established consensus; none misrepresented.                                                                                                                                                                                                                                                                                                                                                                                         |
| 3   | Pedagogical fit for a zero-background reader  | Pass    | §0 explicitly states it formalizes `introductory/08`; assumes only `introductory/03`, `introductory/07`, `introductory/08`, `intermediate/05` — each named. Genuine textbook depth: five named benchmarks plus two full worked examples (Coder/Reviewer evaluation harness, §8) well beyond a skim.                                                                                                                                                                                                                                   |
| 4   | Bilingual quality (信达雅)                    | Pass    | Full read. No machine-like phrasing found; `τ-bench`/`pass@k` handling stays terminologically consistent with `advanced/08`.                                                                                                                                                                                                                                                                                                                                                                                                          |
| 5   | Structural completeness                       | Pass    | `## References` / `**参考文献**` present, correctly split; every citation traces to a specific in-text claim; internal cross-references all resolve.                                                                                                                                                                                                                                                                                                                                                                                  |

**Problems found in this document:** 0.

**Verdict:** Pass.

---

### 2.5 `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`

**Author:** Dr. Aditi Bhandari

| #   | Check                                         | Verdict | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| --- | --------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Factual accuracy — independently spot-checked | Pass    | FLP impossibility (1985, JACM) attribution correct. Byzantine Generals threshold _n ≥ 3f+1_ re-derived by hand: f=1→n≥4, f=2→n≥7, both correct. Raft quorum ⌊n/2⌋+1 re-derived for n=5 (→3) and n=7 (→4), both correct. Multiagent debate (Du et al.) independently confirmed as published at ICML 2024 with matching page numbers (11733–11763). Mixture-of-Agents' 65.1% AlpacaEval 2.0 figure independently confirmed. The internal git-worktree-junction-incident citation was cross-checked directly against its source (`core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`) and matches precisely, including the exact five-phase table and commands. |
| 2   | Citation validity                             | Pass    | All ten external citations plus the one internal-workspace citation independently spot-checked; no misattribution found anywhere — a real, checkable contrast with `intermediate/07`'s Anthropic citation on an adjacent topic.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 3   | Pedagogical fit for a zero-background reader  | Pass    | Explicitly builds on and names `intermediate/07`, `intermediate/03`, `intermediate/04`, `introductory/07`, `introductory/03`. Correctly separates isolation and consensus as two genuinely distinct engineering problems and organizes the whole chapter around that split. §8's combined worked example and §9's three failure modes give real advanced-level engineering depth.                                                                                                                                                                                                                                                                                                                           |
| 4   | Bilingual quality (信达雅)                    | Pass    | Full read. This is the longest and most technically dense document in the cluster; the Chinese translation holds up under that load with no machine-like phrasing found anywhere, including the formula-adjacent prose in §5–§6.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 5   | Structural completeness                       | Pass    | `## References` / `**参考文献**` present, correctly split; internal cross-references all resolve, including the two references to `intermediate/04` (outside this cluster but correctly named).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

**Problems found in this document:** 0.

**Verdict:** Pass.

---

### 2.6 `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`

**Author:** Dr. Mireille Dubois

| #   | Check                                         | Verdict        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --- | --------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Factual accuracy — independently spot-checked | Needs revision | The Wilson score interval was independently re-derived by hand for both §3 worked examples and matches exactly (Harness A: p̂=0.84, n=50 → [0.715, 0.917]; Harness B: p̂=0.74, n=50 → [0.605, 0.841]). Cohen's kappa worked example (§9) independently recomputed: κ≈0.53, matches exactly. pass@k/pass^k worked example (§8) independently recomputed: pass@5=1.0, pass^5≈0.024, matches exactly. However, §11's WebArena worked example contains a genuine, self-contradictory error — see §3, Problem #1.                                                                                          |
| 2   | Citation validity                             | Pass           | All ten external citations independently spot-checked. Bowyer, Aitchison & Ivanova (2025) confirmed as an actual ICML 2025 spotlight paper with matching title and arXiv id (2503.01747). Dror et al. (2018) confirmed with the exact author list "Dror, Baumer, Shlomov, Reichart" — matching the document precisely, and correctly _avoiding_ a common misattribution (a fourth author, "Bogomolov," who belongs to a different, related 2017 paper by an overlapping author set, not this one). McNemar (1947), Wilson (1927), Efron & Tibshirani (1993) all standard and correctly represented. |
| 3   | Pedagogical fit for a zero-background reader  | Pass           | §0 explicitly states it completes `intermediate/08`'s formalization arc, and names `intermediate/01`, `intermediate/05`, `advanced/01`, `advanced/07` for their specific contributions. Every formula gets a worked numeric example. §10's explicit "the field's methodology is still actively developing" framing for cross-agent variance attribution is a genuine strength — it follows `curriculum/README.md` §5's "not knowing is a permitted answer" instruction rather than papering over an open problem.                                                                                   |
| 4   | Bilingual quality (信达雅)                    | Pass           | Full read. No machine-like phrasing found, even in the densest formula-heavy passages (§2, §6, §8, §9).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 5   | Structural completeness                       | Pass           | `## References` / `**参考文献**` present, correctly split; internal cross-references all resolve.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

**Problems found in this document:** 1 (P0 — see §3, Problem #1).

**Verdict:** Needs revision — §11's WebArena worked example is internally self-contradictory: the table's own numbers cannot be derived from the inputs given two paragraphs later in the same section, and the section's own written conclusion contradicts the table's own significance verdict. This is the single most consequential defect found in this cluster, because it sits in the document whose entire purpose is teaching a reader to distrust an unchecked number.

---

## 3. Problems Found

| #   | Document                                                                  | Location                                                   | Issue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Severity |
| --- | ------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| 1   | `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`        | §11, WebArena row of the results table, and its footnote   | The table reports McNemar `χ² = 5.14` for WebArena. The footnote's own worked derivation from the stated inputs (`b = 16, c = 6`) yields `χ² = 81/22 ≈ 3.68` (continuity-corrected, per §6's own formula) or `χ² = 100/22 ≈ 4.55` (uncorrected) — neither equals 5.14, and no alternative derivation is offered for 5.14. Worse, the footnote's own sentence ("5.14 falls short of that stricter bar [≈5.73], illustrating exactly why the correction matters") and the section's closing sentence ("none of the three individual comparisons clears a properly adjusted significance bar") both state WebArena is _not_ significant after Bonferroni correction — yet the table's own "`p < 0.05/3?`" column marks WebArena "**Yes**," directly contradicting both. Correct looks like: the table's χ² value, its derivation from `b,c`, and the "p < 0.05/3?" verdict must all agree with each other and with the section's prose conclusion — either recompute honestly from `b=16, c=6` (both formulas give non-significant results even before correction, so the verdict should read "No") or supply different, internally-consistent `b,c` values that actually produce 5.14 and a verdict matching the stated 5.73 threshold. | P0       |
| 2   | `intermediate/07-multi-agent-communication-and-coordination-protocols.md` | §6, ¶2 ("hierarchical topology" / Anthropic 2025 citation) | "reporting that this design reduced research time by up to 90% for complex queries compared to a single-agent approach on the same task (Anthropic, 2025)" misattributes the source. Anthropic's post ties the 90% figure specifically to a parallel-tool-calling engineering optimization (spinning up 3–5 subagents in parallel plus letting each subagent use 3+ tools in parallel), described in a separate section of the post ("Prompt engineering and evaluations for research agents"), and the comparison there is against the team's own earlier _sequential multi-agent_ execution — not "a single-agent approach." The post's actual single-agent-vs-multi-agent comparison uses a different figure entirely: a 90.2% quality improvement on an internal research eval, not a time reduction. Correct looks like: attribute the 90% time figure to the parallelization optimization and correct the comparison baseline to "earlier sequential multi-agent execution," or cite the 90.2% figure instead if the point being illustrated is genuinely single-vs-multi-agent performance.                                                                                                                                    | P1       |
| 3   | `introductory/08-why-and-how-we-evaluate-agents.md`                       | References / External Sources                              | Liang, P. et al. (2022) "Holistic Evaluation of Language Models" (HELM) is listed as an External Source but is never mentioned, quoted, or drawn upon anywhere in the document's nine numbered sections — every other citation in this document is tied to a specific in-text claim, and this one floats free. Correct looks like: either use HELM in §2's benchmark discussion (it is a natural fit alongside MMLU as a second worked example of "benchmark" as a concept) or remove the unused entry.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | P3       |

**Severity scale** (reproduced from the template): P0 = fabricated/non-existent/materially misrepresented citation, or a stated formula/named result that is wrong — blocking without exception. P1 = a wrong or unsupportable factual claim, a term used before definition, or an assumption of outside coursework — blocking. P2 = machine-like or inconsistent Chinese, broken EN¶→ZH¶ pairing, missing needed worked example, or thin treatment — non-blocking but recorded. P3 = wording/formatting/terminology polish.

---

## 4. Clean Documents — State Them Plainly

For every document I reviewed and found genuinely clean, I state so explicitly:

- `introductory/07-introduction-to-multi-agent-systems.md` — **Reviewed in full; no problems
  found.** I checked hardest against the Wooldridge textbook attribution (a definitional claim
  that is easy to misquote from a 17-chapter book) and against whether the three
  organizational-architecture names it introduces (centralized/decentralized/hierarchical) stay
  consistent with how `intermediate/07` and `advanced/07` build on them later — both held up.
- `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md` — **Reviewed in full;
  no problems found.** I checked hardest against the five named-benchmark factual details (task
  counts, environment counts, human-accuracy figures) since these are exactly the kind of specific
  numeric claim most likely to drift from the source over time — all five (SWE-bench, WebArena,
  AgentBench, GAIA, τ-bench) held up under independent WebSearch verification this session.
- `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md` — **Reviewed in
  full; no problems found.** I checked hardest against the Byzantine-fault-tolerance arithmetic
  (n ≥ 3f+1) and the internal git-worktree-junction-incident citation, since a wrong formula or a
  fabricated internal incident would be the most damaging possible defect in a chapter whose
  entire second half is built directly on that arithmetic — both independently re-derived and
  cross-checked against the actual source document, and both confirmed correct.

Two further documents — `introductory/08` and `advanced/08` — also earn a **Pass** verdict under
the template's own rule (a Pass-row document with only a recorded P3, or a document whose rows are
otherwise all Pass, is not automatically "needs revision" unless a Fail row or a P1 is present);
`introductory/08` carries one non-blocking P3 and `advanced/08` carries the cluster's one P0, which
is severe enough that I still call out `advanced/08`'s overall document verdict as "needs
revision" per §2.6 above, despite four of its five checklist rows being genuine passes. Not every
document in this cluster is clean: `intermediate/07` and `advanced/08` each carry a recorded,
blocking problem (see §3).

---

## 5. Cluster-Level Verdict

| Document                                                                    | Verdict        | Blocking severity present |
| --------------------------------------------------------------------------- | -------------- | ------------------------- |
| `introductory/07-introduction-to-multi-agent-systems.md`                    | Pass           | None                      |
| `introductory/08-why-and-how-we-evaluate-agents.md`                         | Pass           | None (P3 recorded)        |
| `intermediate/07-multi-agent-communication-and-coordination-protocols.md`   | Needs revision | P1                        |
| `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md`    | Pass           | None                      |
| `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md` | Pass           | None                      |
| `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`          | Needs revision | P0                        |

**Cluster summary:** 4 of 6 documents pass outright (`introductory/07`, `introductory/08`,
`intermediate/08`, `advanced/07`). 2 of 6 need revision: `intermediate/07` for a P1 citation
misattribution in §6, and `advanced/08` for a P0 self-contradictory worked example in §11. Every
document's formulas, definitions, and named results outside of these two specific locations held
up under independent spot-checking — this is a cluster with genuinely strong citation discipline
overall, not a cluster with a systemic accuracy problem, and the two defects found are each
localized to one section of one document apiece.

**The one thing I would fix first, if only one thing could be fixed:** `advanced/08` §11's
self-contradictory WebArena numbers (Problem #1). It is the cluster's only P0, and it damages the
one document whose entire pedagogical purpose is teaching a reader to distrust a headline number
and check the arithmetic behind it — a self-contradiction there undercuts that lesson more than
any other single defect in this cluster could.

---

## 6. Scope Boundary

**Did I edit any curriculum document?** No — issues are recorded here for the author.

**Out of scope for this review:** The other three clusters' documents (Foundations; Agent
Architecture & Design Patterns; Prompt & Context Engineering) — not reviewed, not ruled on, per
`curriculum/README.md` §6's cluster assignment. The cross-cluster structural/taxonomy/bilingual-
formatting review is Tobias Lindqvist's separate mandate; I did check bilingual quality
per-document as this template requires, but I did not audit taxonomy placement or formatting
consistency _across_ all 24 modules. The module→author assignment and the curriculum's overall
scope were not evaluated — noted, not ruled on. Also out of scope: whether the workspace's own
`core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
(cited by `advanced/07`) is itself sound CC-00 engineering practice — I only checked that
`advanced/07` represents that source's content accurately, which it does; whether that source
document is _good_ engineering guidance is CC-00's mandate, not this review's.

---

**Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00 — 2026-08-18**
