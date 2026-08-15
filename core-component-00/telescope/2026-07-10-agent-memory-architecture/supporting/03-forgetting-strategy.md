# Forgetting Strategy — Human-Brain-Emulating Memory Decay for Qdrant-Backed Agent Memory

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md)
> **Audience:** Written for a general audience, not just the engineers implementing this. If you
> only want the short version, read § 1 and § 6.
> **Last Updated:** 2026-08-10
> **Knowledge basis:** every human-memory-science citation below was retrieved via live web search
> on 2026-07-10 for this investigation, not from training-data recall. Source URLs are inline; the
> full list is also in [00-sources-and-references.md](00-sources-and-references.md) § 3.

---

## 1. Why a Forgetting Strategy Is a Design Requirement, Not an Afterthought

Imagine a note-taking app that never let you delete or archive anything — every scrap you'd ever
jotted down stayed pinned to the top, forever, with no way to tell important notes from clutter.
Eventually you couldn't find anything, not because the notes were gone, but because there were too
many of them competing for attention. A memory system for an AI agent has exactly the same
problem: if it just accumulates everything forever with no sense of what matters more, search
quality quietly gets worse over time even though nothing is technically "full." Anthropic's own
engineering research calls this "context rot," and their own memory-tool guidance is blunt about
the fix: developers should periodically expire memory that isn't being used. A memory system
without an explicit forgetting policy would, by construction, ignore that advice.

The original brief for this system also asked for something more specific than "add an expiry
timer": it asked for a forgetting strategy that **emulates how a human brain actually works** —
not because that's the only correct engineering choice, but because it was the explicit design
goal. So every mechanism below is grounded in a specific, cited piece of human memory science, and
cross-checked against how other well-known AI memory systems already implement something similar
(the full comparison lives in `research-report.md` § Findings).

---

## 2. The Governing Model: Memory Fades, But Reviewing It Slows the Fade

**The human-memory basis:** psychology's classic "multi-store model" of memory (Atkinson &
Shiffrin) describes information moving from a fleeting sensory impression, through short-term
working memory, into long-term memory — and what actually makes that transfer happen is
_attention_ and _rehearsal_ (repeated exposure). Separately, the well-known "Ebbinghaus forgetting
curve" shows that unreinforced memories fade exponentially fast at first — roughly half of what
you learn is gone within 30 minutes if you never revisit it, and 70–80% is gone within a day. But
"spaced repetition" — reviewing something again at increasing intervals — dramatically slows that
fade; a large body of research (a 254-study analysis) found spaced review outperforms cramming by
10–30%.

**How this maps onto the memory system:**

| Human Memory Concept                                    | This System's Equivalent                                                                                                                                          |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A fleeting sensory impression                           | Not modeled — anything shorter than a full agent turn has no lasting value                                                                                        |
| Short-term / working memory                             | `WorkingMemory` — exists only during the current turn, then is discarded                                                                                          |
| Long-term memory (built through attention + repetition) | The durable memory collections, entered by an explicit write (the "attention" step) and reinforced every time they're retrieved again (the "rehearsal" step, § 3) |
| Ebbinghaus's exponential fade                           | A record's "decay weight" is recalculated on an exponential curve (§ 3), not a straight-line countdown                                                            |
| Spaced repetition slowing the fade                      | Every time a memory is retrieved, its resistance to future fading increases (§ 3) — directly modeled on how other AI memory systems already do this               |

---

## 3. The Decay Formula — How "Fading" Is Actually Calculated

Once a day (by default — see [02-deployment-guidelines.md](02-deployment-guidelines.md) § 5), a scheduled job recalculates a
"decay weight" for every memory record — a number from roughly 0 to 1 representing how strongly it
should still count in search results:

```
decay_weight(t) = importance × e^(-Δt / strength)

where:
  Δt       = time since the memory was last accessed (or created, if never accessed)
  strength = a base value that grows the more often the memory has been retrieved
```

- **`importance`** (a number from 0 to 1) is assigned the moment a memory is written, by a cheap,
  rule-based check — not an AI judgment call, because that would add unwanted delay to every
  single write. The starting rules: a decision or firm commitment → 1.0 (and, as § 3.1 explains,
  exempt from fading entirely); an explicit correction or stated preference → 0.7; an ordinary
  observation or tool result → 0.2–0.3. This borrows the _idea_ from a well-known AI-agent-memory
  research project (Generative Agents, which scores importance with an AI call per memory) without
  borrowing the _cost_ — a rule-based check adds essentially no delay, where an AI call per write
  would. A richer, AI-judged reassessment of importance is possible in principle during the batch
  maintenance pass, which already makes AI calls for other reasons (§ 4) and isn't time-sensitive
  the way a live write is — see § 3.2 for why that hasn't been pursued yet.
- **`strength`** grows every time a memory is retrieved — this is the literal implementation of
  "reviewing something makes it stick," the spaced-repetition finding from § 2. A frequently-used
  fact therefore fades slower than the population average, rather than everything fading at one
  fixed, global rate.
- The exact numbers (`reinforcement_factor`, `base_strength`) are deployment-tunable settings, not
  fixed truths — there's no single "correct" value in the research literature; picking one is a
  policy decision the workspace makes for itself, the same way it already treats similar tuning
  choices elsewhere.

**Implementation status (audited 2026-08-10): this formula and every one of its default constants
are implemented exactly as designed** — confirmed directly against the running code. Nothing in
this section describes aspirational behavior; this is what actually runs today.

### 3.1 The Exception: Some Memories Never Fade

A memory marked as "sacred" (a decision or firm commitment — the exact same rule already used
elsewhere in this workspace's memory code) is **completely exempt** from the formula above: its
decay weight is permanently pinned at 1.0 and it's always treated as fully active.

This isn't just a convenience carve-out — it has a genuine basis in how human memory actually
works. Emotionally significant events get a kind of VIP treatment in the brain: the amygdala (the
brain's salience-detector) biases the hippocampus toward prioritizing that specific memory for
long-term storage, and suppresses competing processing while it does — the mechanism behind
so-called "flashbulb memories," the vivid, unusually durable memories people form of significant
personal or historic moments. A user's explicit decision is this system's version of a
high-salience event: not just _high_ importance, but _maximal and permanent_ importance, by
design.

### 3.2 A Possible Future Upgrade — Not Adopted, Recorded for Later

§ 3 mentions that a richer, AI-judged importance reassessment (beyond the cheap write-time rule)
was considered. This is where that discussion, and the decision that came out of it, is recorded.

**Decision: not pursued for now.** Given this workspace's current hardware (a single consumer GPU,
shared with the embedding model and the document-search pipeline), the CEO decided against adding
a local-AI-model-based importance scorer for the time being. The write-time rule in § 3 remains
the actual, current design — this subsection exists purely as a reference in case the decision is
ever revisited, not as a plan or a promise.

**What was actually discussed, for reference:** a small locally-run language model already vetted
for this hardware in a different context (coding tasks) was considered, but is sized and tuned for
code generation, not the very different job of classifying or scoring text. A smaller,
general-purpose model would likely fit the job better but hasn't been evaluated in this workspace
at all. Either way, this was a "someday, maybe" discussion, not a commitment.

**What this doesn't affect:** the contradiction check (§ 5) and the consolidation step (§ 4) below
already make AI calls as part of the batch maintenance pass — that was decided independently and
has nothing to do with this subsection.

---

## 4. Consolidation — Turning Repeated Experience Into a Durable Fact

**The human-memory basis:** according to systems-consolidation theory, detailed episodic memories
(the kind that remember a specific moment) gradually get transformed into more general,
fact-like semantic memories (the kind that just remember "this is true," without the surrounding
detail) — a transfer believed to happen substantially during sleep, through a specific
neural replay process between the hippocampus and the cortex. Critically, this transfer
**strips away the specific contextual detail and keeps only the generalizable gist.**

**How this maps onto the memory system:**

1. The maintenance job scans a session's episodic memories for ones whose combined
   "importance times how-often-retrieved" score crosses a threshold (150, by default) — a number
   borrowed directly from the same Generative Agents research cited in § 3, where it triggers
   roughly two to three times per simulated day.
2. When that threshold is crossed, an AI summarization call condenses the qualifying cluster of
   episodic memories into one new, distilled semantic fact — discarding session-specific detail
   and keeping the generalizable conclusion. This is the direct software equivalent of the
   detail-stripping, gist-forming transfer described above.
3. The new fact records exactly which original episodic memories it was built from, so the
   provenance is never lost — mirroring both the cited research (which does the same) and this
   workspace's own general habit of preserving history rather than overwriting it.
4. **The original episodic memories are not deleted** when this happens. They keep fading on their
   own separate decay schedule (§ 3), independently of the new fact that was distilled from them.
   Consolidation adds a new record; it never removes the old ones — this matches the observation
   that some detailed episodic memory can remain independently recallable even after the gist has
   been consolidated into semantic memory.

**Implementation status (audited 2026-08-10): implemented exactly as designed**, including the
150-point trigger threshold — confirmed directly against the running code.

---

## 5. Forgetting — A Change in Status, Not an Instant Deletion

**The human-memory basis:** the best-supported explanation for everyday forgetting isn't simply
"time passed" — it's **interference**: specifically, _retroactive_ interference, where new,
related information makes it harder to recall something older. In other words, people tend to
forget things _because something new came along and conflicted with it_, not just because a clock
ran out.

**How this maps onto the memory system — two separate mechanisms:**

### 5.1 Contradiction Checking (Built, Currently Switched Off)

The idea: when a new durable fact is written, check whether it conflicts with something already
stored, and if so, mark the older one as superseded rather than just letting two contradictory
facts sit side by side. This is checked in a periodic batch pass, not at the moment of writing —
a new fact is saved immediately and only classified against older facts later, because that
classification needs an AI judgment call, and putting an AI call on the fast write path would slow
down every single write for a check that doesn't need to happen instantly.

The classification step sorts each new fact against similar existing ones into: genuinely new
(no conflict), an update (it supersedes an existing fact), or a duplicate (no action needed) — the
same three-way decision a well-known AI memory framework (Mem0) makes over its own retrieved
candidates. When something is classified as an update, the older, superseded fact is marked
**archived — never deleted.** It's simply excluded from normal search results going forward, while
the record itself is kept, exactly the same "close the validity window, don't erase the fact"
pattern another well-known system (Zep/Graphiti) uses for its own knowledge graph. This is
retroactive interference, implemented as a visible, reviewable state change instead of a silent,
untraceable overwrite.

**Implementation status (audited 2026-08-10): built, but deliberately not active.** The
classification code exists and works correctly in isolation. But a 2026-07-12 adversarial safety
test found a serious problem: it flagged genuinely new, unrelated facts as "contradicting" existing
ones **100% of the time** in testing — and confirmed two concrete ways someone could exploit that
flaw to feed false information into memory (a "memory poisoning" attack) or exploit a timing race
between two near-simultaneous writes. Because of that finding, the maintenance job's code requires
a human to explicitly confirm "I have reviewed and accepted this mechanism is safe" before it will
ever run this step — and that confirmation has deliberately not been given. In practice: **no
contradiction checking happens in production today.** New facts are written and simply coexist,
without automatic conflict detection, until this is remediated and re-tested. Full detail:
[research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md) § Contradiction-Check Adversarial Evaluation.

### 5.2 Decay-Driven Status Changes (Built and Active)

Separately from contradiction checking, every record moves through a status ladder purely based on
how much it's faded (§ 3) — this part **is** live:

- **Active → Dormant**, once decay weight drops below 0.5 — excluded from normal search, but still
  directly retrievable if something specifically asks for it by ID. Think of it as "a weakened
  connection, not yet pruned."
- **Dormant → Archived**, once decay weight drops below 0.15 **and** the record hasn't been
  accessed for a grace period (30 days by default) — now excluded from every search tier, though
  it's still sitting in the underlying log file and could still be recovered.
- **Archived → actually deleted**, is a step that **never happens automatically**, at any decay
  level. Physically removing a record from the log file requires a human to explicitly confirm it.

This is a deliberate, disclosed departure from strict biological realism — actual synaptic pruning
in a real brain isn't reversible, but this system chooses safety and reversibility over a perfectly
faithful analogy, because accidentally, permanently losing data is a much worse outcome here than
being slightly less brain-like.

---

## 6. Tunable Constants (Deployment Defaults)

| Setting                  | Default                                                    | Why This Value                                                                                                                                                              |
| ------------------------ | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Base strength            | 7 days                                                     | A rough middle ground between the Ebbinghaus curve's hours-scale initial fade and how long a persistent fact is meant to stay useful across sessions                        |
| Reinforcement per access | +50% strength each time retrieved                          | Tunable — there's no single canonical value in the cited research; this is a deployment policy choice                                                                       |
| Dormant threshold        | Decay weight below 0.5                                     | Matches the "weakened, not gone" framing rather than a hard cutoff                                                                                                          |
| Archive threshold        | Decay weight below 0.15, and unused for 30+ days           | Deliberately conservative — errs toward keeping borderline records rather than losing them                                                                                  |
| Consolidation trigger    | Combined importance × access-count reaches 150 per session | Reused directly from the Generative Agents research as a starting point; worth recalibrating against this workspace's own real session lengths once enough real data exists |

**These are starting defaults, not validated thresholds.** Confirming they behave well against real
usage data remains an open question tracked in `research-report.md` § Open Questions — this rewrite
doesn't change that status, it just makes the numbers themselves easier to find and verify against
the live code (§ 3, § 4).

---

## References

| Resource                                                                                                                                               | Role                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `research-report.md` § Findings                                                                                                                        | Full architecture-by-architecture comparison against other AI memory systems                              |
| [01-technical-options.md](01-technical-options.md) §§ 2–3                                                                                              | The record fields this document changes over time (`decay_weight`, `status`, `consolidated_from`)         |
| [00-sources-and-references.md](00-sources-and-references.md) § 6                                                                                       | Full implementation-status audit for every mechanism in this document                                     |
| [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md) § Contradiction-Check Adversarial Evaluation | The safety test that found the contradiction-check flaw described in § 5.1                                |
| `context-engineering/implementations/memory_store.py`, `memory_maintenance.py`                                                                         | The actual code implementing everything in §§ 3–5                                                         |
| `context-engineering/implementations/context_compressor.py`                                                                                            | The summarization tool reused for consolidation (§ 4)                                                     |
| Anthropic Engineering, "Effective context engineering for AI agents" (2025-09-29)                                                                      | "Context rot" framing (§ 1) — retrieved 2026-07-10                                                        |
| Claude Developer Platform, Memory tool docs                                                                                                            | "Periodically expire unaccessed memory files" guidance (§ 1) — retrieved 2026-07-10                       |
| Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (2023, ar5iv)                                                                | Importance scoring, recency decay, the reflection/consolidation mechanism (§§ 3–4) — retrieved 2026-07-10 |
| Mem0 architecture breakdown (Dwarves Memo)                                                                                                             | The new/update/duplicate consolidation decision (§ 5) — retrieved 2026-07-10                              |
| Zep temporal knowledge graph paper (arXiv:2501.13956) / Neo4j Graphiti blog                                                                            | Mark-don't-delete fact invalidation (§ 5) — retrieved 2026-07-10                                          |
| Wikipedia, "Atkinson–Shiffrin memory model"; SimplyPsychology                                                                                          | The multi-store model (§ 2) — retrieved 2026-07-10                                                        |
| Whatfix; OmniSets — Ebbinghaus curve / spaced repetition                                                                                               | Exponential decay, rehearsal strengthening (§§ 2–3) — retrieved 2026-07-10                                |
| PMC, "Sleep-dependent consolidation model"; "Memory Consolidation"; Springer                                                                           | Episodic-to-semantic consolidation (§ 4) — retrieved 2026-07-10                                           |
| Wikipedia, "Interference theory"; SimplyPsychology                                                                                                     | Retroactive / proactive interference (§ 5) — retrieved 2026-07-10                                         |
| PNAS, "Making lasting memories"; PMC, amygdala prioritization                                                                                          | Salience-weighted, non-fading retention (§ 3.1) — retrieved 2026-07-10                                    |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Executing Engineers:** Mei-Ling Zhao (Context Engineering), Sofia Almeida & Diego Fontán (RAG)
