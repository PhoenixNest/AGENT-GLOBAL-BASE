# Knowledge Transfer Protocol — Casual Games Studio

> **ASE Layer:** 2 — Context Engineering (institutional memory) + Layer 4 — RAG (static knowledge base)
> **Authority:** Studio Director Dr. Marcus Vogel
> **Reference:** `core-component-00/context-engineering/patterns/multi-agent-handoff.md`
> **Related:** `rag-integration-blueprint.md` (explains why no live retrieval pipeline is used)

This protocol defines how **institutional knowledge is captured, structured, and transferred** across stages, crew agents, and future projects within the Casual Games Studio.

---

## 1. Knowledge Tiers

The studio operates a three-tier knowledge model, from most ephemeral to most permanent:

| Tier | Name                        | Scope                     | Storage                                     | Retention          |
| :--: | :-------------------------- | :------------------------ | :------------------------------------------ | :----------------- |
|  1   | **Session Knowledge**       | Single work session       | `session-log.md`                            | Until stage closes |
|  2   | **Project Knowledge**       | Full project lifecycle    | `checkpoint.json`, stage artifacts          | Project lifetime   |
|  3   | **Institutional Knowledge** | Cross-project, cross-crew | Crew profiles, pipeline spec, this protocol | Permanent          |

---

## 2. Tier 1 — Session Knowledge

**What to capture per session:**

- Decisions made (with rationale)
- Playtest data observed
- Kill gate metric readings
- Risks surfaced
- Blockers encountered and resolved
- Next session objectives

**Format:** Append to `session-log.md` using the session template.

**Transfer rule:** At session end, the active crew member must update `progress.md` and `checkpoint.json` before closing. No session ends without these three files updated.

---

## 3. Tier 2 — Project Knowledge

**What to capture per stage gate:**

- Stage Transition Summary (human-readable)
- Stage Transition Schema JSON (machine-readable)
- All produced artifacts (GDD chapters, ADRs, build reports, playtest data)
- Kill gate decision and rationale (kill-gate-report.md)
- Constraints carried forward into next stage

**Format:** Filed under the project folder: `studio/casual-games/projects/<project-slug>/`

**Transfer rule:** Before any stage transition, the Stage owner must verify `checkpoint.json` reflects all kill gate outcomes and that `stage-transition-schemas.md` schema is complete. The schema JSON is the handoff packet.

---

## 4. Tier 3 — Institutional Knowledge

**What qualifies as institutional knowledge:**

- Lessons learned from kill gate failures (what signals predict failure)
- Playtesting heuristics (what question formats yield reliable D1/D7 data)
- Engine-specific patterns (Unity 6.3 performance gotchas, shader budgets)
- Market tier calibration adjustments (what MAU thresholds proved reliable)
- Crew capability discoveries (which roles can flex across divisions)

**How to capture:**

After each project reaches Stage 10 (Live Ops) or is killed, Studio Director produces a **Project Retrospective** appended to `studio/casual-games/library/` as `retrospectives/<project-slug>-retrospective.md`.

**Transfer to new crew:** When a new crew member joins, they receive:

1. Their `profile.md` and `skills/*.md`
2. The relevant pipeline stage specification
3. The last 2 Project Retrospectives (Tier 3 knowledge)

---

## 5. Cross-Stage Handoff Checklist

At every stage transition (kill gate or user approval gate), verify:

- [ ] `session-log.md` updated with current session output
- [ ] `progress.md` reflects current stage and next stage objective
- [ ] `checkpoint.json` updated with gate outcome and all metric values
- [ ] `stage-transition-summary.md` completed with full handoff context
- [ ] Stage Transition Schema JSON produced and validated
- [ ] Constraints from this stage explicitly listed in `constraints_forward`
- [ ] Lessons learned (if any) documented for Tier 3 capture
- [ ] Receiving crew member's MVC Profile consulted (only ✅ items sent)
- [ ] Handoff tier selected (Full / Scoped / Minimal) per `inter-agent-communication-protocol.md` §4

---

## 6. Knowledge Decay Prevention

| Risk                                                | Mitigation                                                                     |
| :-------------------------------------------------- | :----------------------------------------------------------------------------- |
| Stale GDD sections referenced by engineering agents | GDD owner tags all superseded sections with `[SUPERSEDED — see §X.Y]`          |
| Kill gate thresholds drift from pipeline spec       | Thresholds only change via pipeline amendment signed by Studio Director + User |
| Session logs lost on context reset                  | `checkpoint.json` is the single source of truth; session logs are secondary    |
| Crew departure mid-project                          | Departing crew produces a **Handoff Summary** (Scoped tier) for successor      |
| Institutional memory only in individual crew heads  | Tier 3 retrospective is mandatory after each project regardless of outcome     |
