# studio/casual-games/telescope/ — Studio Research Archive

Research archive for the Casual Games Studio. Read this before documenting any competitive,
market, or technical research investigation.

---

## What This Is

The Studio's dedicated instance of the workspace's research-archive pattern — a structured
repository for dated game/market/technical research investigations. Established 2026-07-02 as
part of the CEO-directed decentralization of the former unified workspace-root `telescope/`,
which had been exclusively CC-00-flavored and never covered the Studio. See workspace-root
`telescope/README.md` for the cross-department index and rationale.

---

## Scope

**In scope:** competitive game analysis (mechanics, monetization loops, retention hooks),
live-ops/economy experiments (sink/faucet/velocity analysis), engine and tooling evaluations,
and market/UA trend studies feeding Stage 7–9 launch decisions.

**Out of scope:** engineering/LLM research (→ `core-component-00/telescope/`), company-wide
product research (→ `company/telescope/`), and workspace-wide governance research (stays at
workspace-root `telescope/`).

---

## Relationship to `studio/casual-games/library/topics/` — Important

`library/topics/` already contains research-shaped documents filed by subject rather than by
date (e.g. an SDK vetting report, a pen-testing plan, a UA strategy review framework). **The CEO
decided (2026-07-02) to leave those documents in place — they are NOT migrated into this
archive.** `telescope/` starts empty and is used only for _future_ investigations going forward.

This means, until a future reconciliation decision is made:

- Do not move or duplicate existing `library/topics/` documents into `telescope/`
- New dated investigations belong in `telescope/`, not `library/topics/`
- If in doubt whether an existing finding lives in one place or the other, check `library/topics/`
  first — it is the older, established location

---

## Directory Structure

```
studio/casual-games/telescope/
├── README.md              ← Archive index (currently empty)
└── template/               ← Report template (use this for every new report)
    ├── research-report.md
    └── qa-document.md
```

---

## Creating a New Research Report

1. Create a new folder: `YYYY-MM-DD-<slug>/`
2. Copy the template: `template/research-report.md` → `YYYY-MM-DD-<slug>/research-report.md`
3. Complete the report
4. Add an entry to `README.md`, tagged by discipline (competitive / monetization / tech / market)
   so different crew members' research doesn't get lost in one flat list

Naming, lifecycle, append-only policy, versioning, and quality standards follow the same shared
conventions as every other telescope instance — see workspace-root `telescope/CLAUDE.md`.

---

## Ownership

- **Governance sign-off:** Marcus Vogel, Studio Director — retains sign-off on anything reaching
  ADR-equivalent weight for the Studio
- **Day-to-day steward:** James Okonkwo, Executive Producer
- **Creative/monetization co-owner:** Sakura Ishimori, Creative Director
- **Profiles:** `studio/casual-games/team/crew/leadership/`
