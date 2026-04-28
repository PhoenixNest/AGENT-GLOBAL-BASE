---
name: user-research-driven-design
description: Make research-backed design decisions through usability testing, A/B experiments, qualitative research, and data-informed iteration
version: "1.0.0"
---

# User Research-Driven Design

## Purpose

Ground design decisions in user evidence rather than intuition, using mixed-methods research to validate assumptions and iterate toward better outcomes.

## When to Use

- Validating new design concepts before implementation
- Choosing between multiple design alternatives
- Understanding why users struggle with current designs
- Measuring impact of design changes
- Challenging product assumptions with user evidence

## Why This Matters

Replaces opinion-based design decisions with evidence. Research-backed iterations improve D1 retention by 15-25% and reduce the risk of shipping features that users don't understand or value.

## Research Methods

### 1. Usability Testing

**When:** Validate interaction flows, identify friction points

**Protocol:**

- Recruit 5-8 participants per platform (iOS/Android)
- Create task scenarios (e.g., "Find and purchase item X")
- Observe without leading ("What would you do next?" not "Would you tap here?")
- Record screen + audio, note friction points
- Measure: task completion rate, time on task, error rate

**Output:** Friction report with severity ratings and recommended fixes

### 2. A/B Experiments

**When:** Measure impact of design changes on key metrics

**Protocol:**

- Define hypothesis: "Changing X will improve Y by Z%"
- Identify primary metric (e.g., conversion rate, retention)
- Set sample size for statistical power (typically 80% power, 95% confidence)
- Run for full week cycles to account for day-of-week effects
- Analyze with proper statistical tests (t-test, chi-square)

**Output:** Experiment report with decision (ship/kill/iterate)

### 3. Qualitative Interviews

**When:** Understand user mental models, motivations, pain points

**Protocol:**

- Recruit 8-12 participants representing target segments
- Semi-structured interviews (30-45 min)
- Ask open-ended questions ("Tell me about the last time you...")
- Probe for specifics ("What did you do next? How did that feel?")
- Record and transcribe, code for themes

**Output:** Insight synthesis with user quotes and design implications

### 4. Diary Studies

**When:** Understand behavior over time in natural context

**Protocol:**

- Recruit 10-15 participants
- Ask participants to log experiences over 1-2 weeks
- Provide prompts (e.g., "When did you use the app today? What were you trying to do?")
- Follow up with interviews to clarify entries

**Output:** Longitudinal behavior patterns and unmet needs

## Decision Framework

### When to Trust Data vs. Intuition

**Trust quantitative data when:**

- Sample size is sufficient (n > 100 per variant for A/B tests)
- Metric directly measures user value (retention, task success)
- Result is statistically significant (p < 0.05)

**Trust qualitative research when:**

- Understanding WHY behind quantitative results
- Exploring new problem spaces
- Identifying unmet needs

**Trust design intuition when:**

- Violating platform conventions (users expect iOS/Android patterns)
- Accessibility requirements (non-negotiable)
- Ethical concerns (dark patterns may test well but harm users)

## Research-to-Design Process

1. **Identify assumption** — "We believe users want X"
2. **Choose method** — Usability test? A/B experiment? Interviews?
3. **Run research** — Execute with rigor
4. **Synthesize findings** — What did we learn? What surprised us?
5. **Make decision** — Ship, kill, or iterate?
6. **Document rationale** — Why did we choose this path?

## Quality Standards

**Usability Testing:**

- [ ] Recruited representative users (not internal employees)
- [ ] Tested on actual devices (not desktop simulators)
- [ ] Observed without leading participants
- [ ] Identified severity of issues (critical/major/minor)

**A/B Experiments:**

- [ ] Defined hypothesis upfront
- [ ] Calculated required sample size
- [ ] Ran for sufficient duration (minimum 1 week)
- [ ] Checked for statistical significance
- [ ] Considered secondary metrics (no unintended harm)

**Qualitative Research:**

- [ ] Asked open-ended questions
- [ ] Probed for specifics (not accepting vague answers)
- [ ] Recorded and transcribed
- [ ] Coded for themes across participants
- [ ] Included user quotes in synthesis

## Anti-Patterns

- **Research theater** — Running studies but ignoring results that contradict preferences
- **Sample size of 1** — "My mom said..." is not research
- **Leading questions** — "Don't you think this button is too small?" biases responses
- **Vanity metrics** — Optimizing for clicks when retention matters more
- **Analysis paralysis** — Endless research without shipping
