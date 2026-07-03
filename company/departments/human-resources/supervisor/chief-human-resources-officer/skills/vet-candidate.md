---
name: vet-candidate
description: Shared elite-standards gate. Apply to every candidate before placement regardless of role family. Reject without compromise if they do not meet the bar.
version: "1.0.0"
---

# Elite Candidate Vetting Gate

## Purpose

Every candidate — regardless of role, seniority, or role family — must pass this gate before the CHRO places them. This is non-negotiable. The CHRO does not place mediocre candidates.

## Why This Matters

Applies the 20-point elite candidate vetting gate. Without rigorous vetting, sub-bar candidates enter the organization, creating long-term performance and culture costs.

## Five Vetting Dimensions

Score each dimension 1–5. A candidate must score ≥ 4 on at least 4 of 5 dimensions to pass.

### 1. Impact at Scale (1–5)

- 1: Impact limited to self or immediate team
- 2: Team-level impact, few measurable outcomes
- 3: Cross-team impact, some quantified results
- 4: Org-wide or product-wide impact, clear before/after metrics
- 5: Industry-level impact — shipped products used by millions, built orgs of 50+, or produced work cited beyond their company

**Signal questions:**

- What is the biggest thing they shipped? How many users did it reach?
- What metric moved because of their specific work?
- Would their departure leave a visible hole?

### 2. Craft Depth (1–5)

- 1: Surface-level knowledge, relies on others for depth
- 2: Competent practitioner, no distinguishing expertise
- 3: Strong in primary domain, limited in adjacent areas
- 4: Deep expert in primary domain, credible in two or more adjacent areas
- 5: Recognized authority — others in the industry seek their opinion

**Signal questions:**

- Ask them to go three levels deep on their core skill. Do they still have answers?
- Can they explain the trade-offs in their most important architectural or strategic decision?
- Have they invented, published, or contributed to the field beyond their job?

### 3. Leadership Signal (1–5)

- 1: Individual contributor only, no evidence of multiplying others
- 2: Mentored one or two junior colleagues informally
- 3: Led a small project or team, others grew under them
- 4: Built or transformed a team; people they mentored are now senior elsewhere
- 5: Org-builder — created culture, hiring bars, or practices adopted company-wide

**Signal questions:**

- Name someone they grew. Where is that person now?
- How did the team operate differently because of them?
- What did they give away that made someone else look good?

### 4. Standards Signal (1–5)

- 1: Accepts the status quo, does not raise the bar
- 2: Complains about quality but doesn't fix it
- 3: Raises issues and fixes them within their scope
- 4: Raises the bar for the whole team — code reviews, design crits, writing standards
- 5: Changed what "good" means at their company or in their field

**Signal questions:**

- What was broken when they arrived? What did they do about it?
- What standard did they introduce that outlasted them?
- Did peers voluntarily follow their lead?

### 5. Red Flag Scan (pass/fail)

Automatic fail on any of:

- [ ] Job tenure < 12 months at more than two consecutive roles without a compelling explanation
- [ ] Claims of impact that cannot be attributed to their specific contribution
- [ ] Title inflation: "Head of" with a team of zero, "Principal" with no evidence of scope
- [ ] Vague answers to specific technical or strategic questions
- [ ] Speaks only about what the team did, never what they personally drove

## Evidence Requirement (mandatory as of 2026-07-03)

**No numeric dimension score is valid without the specific signal-question evidence written next
to it.** A number with no cited evidence is not a score — it is a placeholder, and placeholders do
not pass this gate.

For each of the four numeric dimensions, the scorer must answer the dimension's own signal
question in one sentence, naming a concrete fact from the candidate's record — not a restatement
of their title or seniority level. For Leadership Signal specifically, that means naming who the
candidate grew and where that person is now, or explicitly writing "not established" if the
record contains no such evidence.

**"Not established" is an acceptable answer. A default 4/5 backed by nothing is not.** A candidate
whose Leadership Signal is genuinely unestablished should be scored on what the record actually
shows — if that means 1 or 2, that is the honest score, not a problem to paper over. Scoring
generously to avoid an awkward number, or defaulting a score from seniority level rather than from
cited evidence, is exactly the failure mode this requirement exists to close.

**Stage 7 Secondary Officer Review must check for this evidence explicitly** — not just that a
number between 1 and 5 exists, but that the cited evidence actually supports that number against
the dimension's own rubric level. A score with no evidence, or evidence that belongs to a
different dimension (e.g., a craft achievement cited as leadership evidence), is a Stage 7 defect
and is sent back for correction before the candidate can proceed.

## Scoring Output

After scoring, the CHRO must write:

```
VETTING RESULT: [PASS / FAIL]

Scores (each with cited evidence — see Evidence Requirement above):
- Impact at Scale: X/5 — [evidence: one sentence naming the concrete fact]
- Craft Depth: X/5 — [evidence: one sentence naming the concrete fact]
- Leadership Signal: X/5 — [evidence: who did they grow, and where are they now — or "not established"]
- Standards Signal: X/5 — [evidence: one sentence naming the concrete fact]
- Red Flag Scan: [PASS / FAIL]

Total: X/20

Summary: [2–3 sentences on why this candidate passes or fails. Be specific. Name the evidence.]
```

If FAIL: State the exact reason. Do not soften it. Offer to recruit a stronger candidate.

If any dimension has no cited evidence, or evidence that belongs to a different dimension: **do
not finalize the score.** Either find the actual evidence, score it honestly at whatever level the
record supports, or mark it "not established" and score accordingly.
