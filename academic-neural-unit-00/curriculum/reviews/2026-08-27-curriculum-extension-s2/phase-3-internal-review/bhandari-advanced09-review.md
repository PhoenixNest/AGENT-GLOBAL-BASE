# Internal Curriculum Review — Post-Training (S2, Amendment 5) Cluster, `advanced/09` Only

**Reviewer:** Dr. Aditi Bhandari, Staff Research Scientist — Foundational AI Lead, ANU-00
**Cluster reviewed:** Post-Training (S2, Amendment 5) — `advanced/09` only, per CEO-corrected Phase 3
scope
**Documents covered:**
`academic-neural-unit-00/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md`
**Review date:** 2026-08-27
**Review pass:** Pass 1 (S2 extension) — internal cluster review

---

## 0. Independence Declaration

**Did I author any document in this cluster?** No document in my reviewed scope. I am the author
of `advanced/10-modern-post-training-methods-dpo-grpo-and-reward-modeling.md` — the other half of
the Post-Training (S2, Amendment 5) cluster — but `advanced/10` is **not** in my Phase 3 scope for
this review, and I have not reviewed it here.

This is worth stating plainly rather than leaving to inference. The S2 plan's original Phase 3
wording (`plans/2026-08-19-curriculum-coding-and-post-training-extension/curriculum-extension-plan.md`
§4) assigned me "the post-training pair she didn't write plus spot-checks Okonkwo's" — which was
self-contradictory, since §2.2 of that same plan assigns me as author of `advanced/10`. Reviewing
`advanced/10` under that original wording would have put me in direct violation of
`curriculum/README.md` §6's no-self-review rule ("no reviewer reviews a cluster they authored
into"). The CEO resolved this on 2026-08-27 by reassigning `advanced/10`'s review to Dr. Baek and
narrowing my Phase 3 scope to `advanced/09` only — Dr. Okonkwo's module, which I did not author and
have no conflict reviewing. That correction is the entire reason this report's scope is one
document rather than two, and is recorded here, not left silent.

**Anything else that would compromise independence:** None. I have no authorship stake, prior
review stake, or other conflict in `advanced/09`. Dr. Okonkwo (author) is a peer I coordinate with
only at the stage-of-inquiry-test layer for research-question triage
(`skills/foundational-ai-research-coordination.md`), not in a chartering or approval capacity over
his authored curriculum work.

---

## 1. Method

I am not restating the document's own claims. I checked the material directly, myself, before
signing this — including opening every one of the module's 8 external citations at their source
and independently re-deriving or cross-checking every named formula against the paper it is
attributed to, not merely confirming the module's own citation superficially supports its own
text.

| What I did                                | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Independent sources consulted             | Opened, myself, via WebFetch/WebSearch against the primary sources (not the module's framing of them): Ouyang et al. (2022, InstructGPT, full text + abstract), Schulman et al. (2017, PPO, abstract + secondary corroboration of the clipped objective and ε=0.2 via OpenAI Spinning Up's PPO reference page), Schulman et al. (2015, GAE, full text), Christiano et al. (2017, abstract), Ziegler et al. (2019, abstract + targeted search on its own summarization comparison count), Stiennon et al. (2020, full text + independent corroborating searches), Gao/Schulman/Hilton (2022, abstract), and Bradley & Terry (1952, bibliographic record via Oxford Academic/JSTOR/Semantic Scholar) — none taken from memory or from the module's own representation of them. |
| Author-supplied citations opened          | 8 of 8 External Sources links resolved and opened at the source.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Claims spot-checked against those sources | Exhaustive on the formula-bearing and numeric-claim material, which is the load-bearing content of an advanced module: all 8 named formulas (Bradley-Terry probability model, RM loss, PPO probability ratio, PPO clipped objective, combined `L^CLIP+VF+S` objective, GAE advantage estimator, KL-penalized reward, PPO-ptx objective), every author list on every citation, and every quantitative claim tied to a specific paper (InstructGPT's 13k SFT prompts/16 epochs/cosine decay/6B RM/33k RM prompts/175B-unstable claim; Christiano et al.'s <1% human-labeling claim; PPO's ε=0.2; the §5 worked-example arithmetic, recomputed by hand; and the §4 comparison-count claim attributed to Stiennon et al. 2020).                                                  |
| Chinese-language read                     | Read in full, paragraph by paragraph against its English counterpart, for both meaning-fidelity and 信达雅 quality — not sampled.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

---

## 2. Per-Document Checklist

### 2.1 `academic-neural-unit-00/curriculum/advanced/09-reinforcement-learning-from-human-feedback.md`

**Author:** Dr. Samuel Okonkwo

| #   | Check                                         | Verdict  | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| --- | --------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Factual accuracy — independently spot-checked | **Fail** | Every named formula I re-derived independently against its source paper matches exactly: the Bradley-Terry probability model (§4, confirmed equivalent to the σ(λᵢ−λⱼ) log-parametrization used across the modern RLHF literature), the InstructGPT RM loss (§4, verified verbatim against the paper's own equation), the PPO ratio and clipped objective (§6, verified against the paper's clip-and-min construction, corroborated via OpenAI Spinning Up's canonical restatement), the GAE advantage estimator (§7, verified verbatim — δₜ and the (γλ)ˡ-weighted sum both match Schulman et al. 2015's own equations exactly), the KL-penalized reward and PPO-ptx objective (§7, verified verbatim against Ouyang et al. 2022's own equations), and the §5/§8 worked-example arithmetic (recomputed by hand; correct to normal rounding tolerance). Christiano et al.'s "<1%" claim, InstructGPT's 13k/16-epoch/6B-RM/33k/175B-unstable details, and PPO's ε=0.2 all check out against the primary sources. **One claim does not check out** — see Check 2, which is the same underlying defect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 2   | Citation validity                             | **Fail** | All 8 links resolve to the correct, real papers, with author lists matching exactly in every case (I checked every author list against the paper's own listing, not the module's transcription of it) — including the Bradley & Terry (1952) Biometrika citation, which I confirmed independently (vol. 39, issue 3–4, pp. 324–345, matching exactly). **One citation misrepresents its source:** §4 states "Stiennon et al. (2020) report that this comparison-based labeling scaled to 60,000 human comparisons for their summarization work at a labeling cost the demonstration-only approach of Ziegler et al. (2019) could not match at the same budget." I opened Stiennon et al. (2020) directly and found their own released TL;DR comparison dataset is reported at 64,832 comparisons (a different figure, and independently corroborated by multiple secondary citations, not 60,000). I then searched independently and found the 60,000-comparison figure actually belongs to **Ziegler et al. (2019)'s own** summarization experiments ("models trained with 60,000 comparisons copy whole sentences from the input..." is Ziegler et al.'s own reported result). The module has swapped which paper the number belongs to, and — more consequentially — mischaracterizes Ziegler et al. (2019) as a "demonstration-only approach": Ziegler et al. (2019) is titled "Fine-Tuning Language Models from Human Preferences" and is itself a comparison-based reward-modeling paper, the direct methodological predecessor Stiennon et al. (2020) scales up from, not a contrasting demonstration-writing baseline. See Problem #1. |
| 3   | Pedagogical fit for a zero-background reader  | **Pass** | Every use of prior material names the specific earlier module (`intermediate/01` for gradient descent/optimizers, `advanced/01` for scaling-law reasoning), never "as is well known." Two full worked examples (§5: RM loss on a hand-computed 4-way ranking; §8: PPO's clip asymmetry across two concrete cases) at genuine textbook depth, not a skim. §10 correctly states reward-model overoptimization as an open problem rather than papering over it, per README §5's standing rule on unsettled claims.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 4   | Bilingual quality (信达雅)                    | **Fail** | See the mandatory instruction below this table.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 5   | Structural completeness                       | **Fail** | EN¶→ZH¶ pairing holds throughout; bold ZH subtitle present under every heading; `## References` + `**参考文献**` present with both required subsections; no `$$...$$` block sits inside a code fence, none carries leading/trailing content on its own line, and no `$...$` span sits inside a single-backtick span (checked mechanically across the whole document — all clean on these three specific patterns). But a fourth, related rendering defect exists: see Problem #3. §4.4's Chinese range-citation notation is also not followed consistently — see Problem #4.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

**MANDATORY CHECK 4 DETAIL.** Two duplicate-gloss defects in §10, both machine-like in the sense
the review template means — a native technical editor would never produce a parenthetical that
repeats the term it is glossing:

- **English paragraph, line 421:** `**Goodhart's Law**（古德哈特定律，Goodhart's Law）` — the
  parenthetical repeats "Goodhart's Law" in English a second time, immediately after the bolded
  English term it is supposedly glossing. Correct form (matching the README §4 pattern used
  correctly elsewhere in this same document for RLHF/PPO/GAE, which pair a Chinese gloss with a
  **new** piece of information, the acronym — this case adds no new information, so it should just
  be): `**Goodhart's Law**（古德哈特定律）`.
- **Chinese paragraph, line 424:** `**古德哈特定律**（古德哈特定律，Goodhart's Law）` — same
  defect, mirrored: the parenthetical repeats "古德哈特定律" a second time before adding the
  English original. Correct form: `**古德哈特定律**（Goodhart's Law）` — and since Goodhart's Law
  is first glossed in the English paragraph immediately above (line 421), per README §4 "gloss
  such a name once, at its first appearance in the document," the Chinese paragraph does not
  strictly need a second gloss at all once line 421 is fixed; if kept for symmetry, only the
  English original belongs in the parenthetical, not a repeat of 古德哈特定律 itself.
- **Chinese paragraph, line 424 (second instance):** `被称为**奖励黑客**（奖励黑客）` — this is not
  a translation gloss at all, it is the identical two-character-for-two-character Chinese term
  repeated inside its own parenthetical, which conveys zero information and reads as a mechanical
  copy-paste artifact rather than anything a human editor would write. Correct form, given
  "reward hacking" is a named phenomenon already introduced with its English name and Chinese
  gloss in the immediately preceding English paragraph (line 422: `**reward hacking**（奖励黑客）`,
  itself a legitimate first-use gloss): drop the parenthetical entirely here —
  `被称为**奖励黑客**。` — the term was already glossed once, at its first appearance.

**Problems found in this document:** 4 (1 × P0, 1 × P2 bilingual-quality, 1 × P2
structural/rendering, 1 × P3 formatting).

**Verdict:** Needs revision — blocking reason: §4's citation of "Stiennon et al. (2020) ... 60,000
human comparisons" misattributes a figure and a methodological characterization that actually
belong to Ziegler et al. (2019), a materially misrepresented citation per `curriculum/README.md`
§5 and the review template's P0 definition.

---

## 3. Problems Found

| #   | Document                                                    | Location                                                                                                                       | Issue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Severity |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| 1   | `advanced/09-reinforcement-learning-from-human-feedback.md` | §4 ("Stage 2: Reward Modeling"), the sentence beginning "Stiennon et al. (2020) report that this comparison-based labeling..." | Misattributed citation: the "60,000 human comparisons for their summarization work" figure belongs to **Ziegler et al. (2019)'s own** summarization experiments (independently confirmed), not Stiennon et al. (2020), whose own released TL;DR comparison dataset is 64,832 comparisons — a different number. The same sentence also mischaracterizes Ziegler et al. (2019) as a "demonstration-only approach," when it is itself a comparison-based reward-modeling paper (title: "Fine-Tuning Language Models from Human Preferences") and the direct methodological predecessor of Stiennon et al. (2020), not a contrasting baseline. Fix: attribute the 60,000-comparison figure to Ziegler et al. (2019) directly, cite Stiennon et al. (2020)'s own (larger, ~64,832+) dataset separately if the scaling point is still wanted, and remove "demonstration-only" from the Ziegler characterization. | P0       |
| 2   | `advanced/09-reinforcement-learning-from-human-feedback.md` | §10 ("Reward Hacking and Overoptimization"), lines 421 and 424                                                                 | Machine-like duplicate glosses: `Goodhart's Law（古德哈特定律，Goodhart's Law）` (line 421, English paragraph) and `古德哈特定律（古德哈特定律，Goodhart's Law）` plus `奖励黑客（奖励黑客）` (line 424, Chinese paragraph) — each parenthetical repeats the term it is glossing instead of supplying the other language's rendering. See Check 4 detail above for the exact corrected wording for each of the three instances.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | P2       |
| 3   | `advanced/09-reinforcement-learning-from-human-feedback.md` | §6 ("Stage 3: From Policy Gradients to PPO's Clipped Objective"), lines 268–270, English paragraph only                        | Broken markdown rendering: the inline `$L^{\text{CLIP+VF+S}}(\theta) = ...$` formula is split across a blank line (paragraph break), and the continuation line begins with `- c_1 \left(...`, which markdown renders as a bullet-list item — this breaks both the math rendering and the sentence. The underlying LaTeX is correct (the Chinese paragraph immediately below has the identical formula, correctly kept on one line, and I verified it matches Schulman et al. 2017's own combined objective exactly) — this is purely an accidental line-wrap artifact confined to the English paragraph. Fix: join lines 268–270 into one unbroken paragraph, exactly as the Chinese paragraph already does.                                                                                                                                                                                               | P2       |
| 4   | `advanced/09-reinforcement-learning-from-human-feedback.md` | §9 and §11 (Internal Cross-References range citations), 3 instances: "第 3 至 8 节", "第 4 至 5 节", "第 6 至 9 节"            | README §4.4's ratified range-citation notation is `[第 X–Y 节]` (en-dash), but this module consistently uses `第 X 至 Y 节` (the character 至) instead. All 27 of the module's section citations correctly carry markdown anchor links, and English-side `§§X–Y` notation is followed correctly throughout — only the Chinese-side character choice for ranges deviates from §4.4's literal ratified form.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | P3       |

**Severity scale:** as defined in `templates/curriculum/internal-review-report.md` (P0 = fabricated
or materially misrepresented citation, or a wrong stated formula/named result, blocking without
exception; P1 = a wrong/unsupportable factual claim, an undefined term, or an assumed-outside-
coursework section, blocking; P2 = machine-like/inconsistent Chinese, broken pairing, or thin
treatment, non-blocking but must be recorded; P3 = wording/formatting/terminology polish).

---

## 4. Clean Documents — State Them Plainly

No document in this review's scope was found genuinely clean end-to-end.
`advanced/09-reinforcement-learning-from-human-feedback.md` is a strong module overall — every one
of its 8 named formulas independently re-verified correct against the primary source, every
citation's authors/venue correct, genuine textbook depth with two full worked examples, and correct
handling of the one genuinely open research question (§10) — but it carries one P0 (a misattributed
citation), two P2s, and one P3, so it does not earn a clean bill under this review's own rule that a
verdict must be supported by what the checklist rows actually found.

---

## 5. Cluster-Level Verdict

| Document                                                    | Verdict        | Blocking severity present |
| ----------------------------------------------------------- | -------------- | ------------------------- |
| `advanced/09-reinforcement-learning-from-human-feedback.md` | Needs revision | P0                        |

**Cluster summary:** 1 of 1 document in this scope needs revision. The document's mathematical and
methodological content is otherwise sound — this is a citation-attribution defect plus two
formatting/rendering defects, not a wrong-formula or fabricated-source defect, and none of it
requires re-deriving or re-checking any of the module's actual technical claims once fixed.

**The one thing I would fix first, if only one thing could be fixed:** Problem #1 — the Ziegler/
Stiennon citation misattribution in §4. It is the only P0, it is the module's blocking defect, and
because it also mischaracterizes what Ziegler et al. (2019) actually did methodologically, leaving
it uncorrected would teach a zero-background reader something false about the field's own history,
not just get a number wrong.

---

## 6. Scope Boundary

**Did I edit any curriculum document?** No — issues are recorded here for the author (Dr.
Okonkwo) and for Dr. Mokoena's Phase 5 synthesis; I made no changes to
`advanced/09-reinforcement-learning-from-human-feedback.md` or to any other curriculum file.

**Out of scope for this review:** `advanced/10-modern-post-training-methods-dpo-grpo-and-reward-modeling.md`
— my own authored module, reassigned to Dr. Baek's review under the CEO's 2026-08-27 correction (see
§0). I have not read it with a reviewer's eye as part of this report and take no position on its
content here. The 6 practicum modules and Dr. Lindqvist's structural/taxonomy/bilingual-formatting
pass across the full S2 extension are likewise out of scope — this report covers `advanced/09`
alone, per the corrected Phase 3 assignment. The module→author assignment itself and the curriculum's
overall S2 scope are noted as given, not re-litigated here.

---

**Dr. Aditi Bhandari, Staff Research Scientist — Foundational AI Lead, ANU-00 — 2026-08-27**
