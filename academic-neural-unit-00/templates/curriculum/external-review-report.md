# External Curriculum Review — [Evaluation Lens]

<!-- FILING NOTE (for whoever deploys this template, not for the reviewer):
     Copy to academic-neural-unit-00/curriculum/reviews/YYYY-MM-DD-<round-slug>/external/<lens>-review.md
     — one dated round folder per review cycle, per curriculum/reviews/README.md. Never fill one
     in inside templates/ itself.

     Point-in-time record (academic-neural-unit-00/templates/README.md § Available Templates) — a
     re-review is a new file with a cross-reference, never an edit to this one.

     This review is BLIND BY DESIGN (curriculum-development-plan.md §5, Phase 4). The reviewer is
     given the finished curriculum documents and this template, and no organizational context: no
     roster, no author names, no internal conventions, no knowledge of who commissioned the work.
     That is the entire point — internal review cannot catch material that reads as correct to
     people who share the author's assumptions. Do not brief the reviewer beyond the documents
     themselves, and do not add internal identifiers to the sections below. -->

**Reviewer designation:** [A / B — anonymous; no real identity is recorded for a blind review]
**Evaluation lens:** [Technical accuracy & citation audit / Interview readiness]
**Documents reviewed:** [Relative paths, listed individually — every document received]
**Review date:** [YYYY-MM-DD]

---

## 1. Assumed Persona and Evaluation Lens

<!-- Required first, because every judgment below is only interpretable against the standard the
     reviewer is holding. A verdict of "not deep enough" from a research scientist and from a
     hiring manager mean different things and imply different fixes. State the persona plainly and
     commit to it for the whole review. -->

**Persona I am reviewing as:** [e.g. "PhD-level researcher in machine learning, publishing in the
area, no affiliation with the authors" / "Technical interviewer and hiring manager at a frontier AI
lab, currently running an agent-engineering loop"]

**What I am therefore optimizing the review for:** [One paragraph. What would make me reject this
material, and what would make me recommend it.]

**What I am explicitly NOT judging:** [Name it — house style, formatting preferences, the material's
fit to any internal convention I have not been shown. A blind reviewer who invents the commissioning
body's expectations and then grades against them is reviewing a document they were not given.]

**Context I was given:** [State exactly what I received. If the answer is "the document files and
nothing else", say so — it is the condition that makes this review worth having.]

---

## 2. External Standards Benchmarked Against

<!-- Required, named, and linked. A review that says "below the standard of a good graduate course"
     without naming the course is an opinion; a review that names the course and the specific unit
     is a check someone else can repeat. Every row must be a real, currently-reachable source that
     the reviewer actually opened. -->

| #   | Standard (course / textbook / paper)    | Link            | What I benchmarked against it                              |
| --- | --------------------------------------- | --------------- | ---------------------------------------------------------- |
| 1   | [Full title, authors/institution, year] | [Markdown link] | [Which curriculum documents, and against which unit of it] |

**Why these standards and not others:** [One paragraph. Coverage matters — a curriculum spanning
foundations through multi-agent evaluation cannot be benchmarked against a single source without
leaving a level or a cluster unjudged. Say which parts of the curriculum each standard covers, and
name any part of the curriculum you had no external standard for.]

---

## 3. Claim Spot-Check

<!-- Sample deliberately, not conveniently. Choose claims where an error would matter and where an
     author working from memory would plausibly get it wrong: named results, quantitative
     statements, attributions of an idea to a paper, and anything stated with more confidence than
     the literature actually supports. Include at least one claim per level and per topic cluster,
     and state the sampling rule you used so a reader can judge the coverage. -->

**Sampling rule I used:** [How the claims below were selected. "Whatever I noticed" is a valid
answer only if stated as one.]

| #   | Claim as stated in the curriculum | Document / location | Verified against (with link) | Verdict                                                                    |
| --- | --------------------------------- | ------------------- | ---------------------------- | -------------------------------------------------------------------------- |
| 1   | [Quote or close paraphrase]       | [`path` § heading]  | [Source I opened myself]     | [Correct / Overstated / Wrong / Unverifiable from any source I could find] |

**Errors that would mislead a beginner, specifically:** [The reader has no prior background and
cannot catch an error by intuition. Which of the above would they carry forward as a
misunderstanding into later material?]

---

## 4. Citation Audit

<!-- Every formula, named result, and paper citation found in the material — checked for two
     separate things that are commonly conflated: (a) does the source EXIST, and (b) does it say
     what the document claims it says. A real paper cited for a claim it does not make is a
     failure, not a pass, and must be recorded as one. Do not audit only the References sections:
     a formula or named result stated in the body with no citation at all is itself an audit
     finding and belongs in this table. -->

| #   | Citation / formula as given                       | Document / location | Source exists? | Correctly represented?                     | Verdict       |
| --- | ------------------------------------------------- | ------------------- | -------------- | ------------------------------------------ | ------------- |
| 1   | [Title, authors, year, or the formula as written] | [`path` § heading]  | [Yes / No]     | [Yes / No — what the source actually says] | [Pass / Fail] |

**Audit totals:**

| Metric                                                       | Count |
| ------------------------------------------------------------ | ----- |
| Citations found                                              | [N]   |
| Links that resolve                                           | [N]   |
| Sources that exist                                           | [N]   |
| Sources correctly represented                                | [N]   |
| **Fabricated or non-existent sources**                       | [N]   |
| **Real sources cited for a claim they do not support**       | [N]   |
| Formulas / named results stated in the body with no citation | [N]   |

**If either bolded row is non-zero, list every instance here, individually:** [Nothing in this
report matters more than this list. If both rows are zero, write that plainly — "No fabricated or
misrepresented citations found across N citations audited" — rather than leaving this empty. An
empty section and a clean audit must not look the same.]

---

## 5. Level-by-Level Assessment

<!-- The lens applies differently per level and a single overall grade hides that. An introductory
     module that assumes prior coursework and an advanced module that stays shallow are opposite
     failures; both are invisible in an averaged verdict. -->

| Level          | Does it do its job? | The strongest thing about it | The weakest thing about it |
| -------------- | ------------------- | ---------------------------- | -------------------------- |
| `introductory` | [Yes / Partly / No] | [Specific]                   | [Specific]                 |
| `intermediate` | [Yes / Partly / No] | [Specific]                   | [Specific]                 |
| `advanced`     | [Yes / Partly / No] | [Specific]                   | [Specific]                 |

**Gaps against my named standards in §2:** [Topics a reader would be expected to know that this
curriculum never covers, or covers too thinly to be useful. Name the standard the expectation
comes from.]

**Material present here that my standards do not cover:** [Say so — a curriculum that goes beyond
the benchmark in a defensible direction is not a defect, and a review that only measures shortfall
mismeasures the work.]

---

## 6. Overall Verdict — Would This Get a Reader Through a Real Technical Interview?

<!-- The question the review exists to answer, stated as a question about a person and an outcome
     rather than a grade on a document. Answer it directly in the first sentence, then give the
     reasoning. Reasoning that does not commit to an answer is not a verdict. -->

**Answer:** [Yes / Yes, with named caveats / No — stated in one sentence, first, before the
reasoning.]

**Reasoning:**

[Several paragraphs. Ground each judgment in something specific from §3, §4, or §5 — a claim that
was wrong, a standard that was met or missed, a level that under-delivers. An assessment that could
have been written without reading the documents is not evidence of anything.]

**What kind of interview, specifically:** [Interviews differ. Say which bar you are answering
against — a research-scientist screen, an applied agent-engineering loop, a new-graduate interview —
and whether the answer changes across them.]

**What a reader would still be unable to do after finishing this curriculum:** [Name it plainly.
Every curriculum has a boundary; an honest one is more useful to the commissioning body than a
generous verdict.]

**The three changes that would most improve interview readiness, in order:**

1. [Change — and what it would fix]
2. [Change — and what it would fix]
3. [Change — and what it would fix]

---

## 7. Reviewer's Confidence and Limits

<!-- Required. A blind reviewer works without the ability to ask the authors a question, and that
     limitation shapes the findings. Stating where confidence is low prevents a soft judgment from
     being read downstream as a firm one. -->

| Area                                    | My confidence         | Why                                                                                                     |
| --------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------- |
| [Topic area / level / specific finding] | [High / Medium / Low] | [Outside my depth, could not access a source, ambiguity in the text I could not resolve without asking] |

**Anything I could not evaluate at all:** [Named, or "None". Including the Chinese-language content
if that is outside your competence — say so rather than passing it silently.]

---

**Reviewer [designation], [assumed persona] — [YYYY-MM-DD]**
