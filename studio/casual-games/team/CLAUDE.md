# studio/casual-games/team/ — Studio Crew

All Casual Games Studio crew documents. 39 crew members across 7 divisions — all hired, Stage 0-ready.

---

## Directory Structure

```
team/
├── README.md          ← Crew roster index by division
└── crew/
    ├── leadership/
    ├── production/
    ├── creative-design/
    ├── art/
    ├── audio/
    ├── engineering/
    └── live-ops/
```

---

## Seven Divisions

| Division           | Scope                                                                   |
| ------------------ | ----------------------------------------------------------------------- |
| `leadership/`      | Studio Director, Creative Director — overall vision and governance      |
| `production/`      | Producers — project management, scheduling, cross-division coordination |
| `creative-design/` | Game designers, UX/UI designers — gameplay systems and interface        |
| `art/`             | 2D/3D artists, animators, VFX — all visual asset production             |
| `audio/`           | Sound designers, composers — FMOD/Wwise integration, music, SFX         |
| `engineering/`     | Unity developers, tools engineers, CI — all code and build systems      |
| `live-ops/`        | Live operations, analytics, community — post-launch operations          |

---

## Agent Path Conventions

```
crew/<division>/<role>/<name>/agent/profile.md    ← Crew member identity
crew/<division>/<role>/<name>/skills/<skill>.md   ← Executable skill contracts
```

---

## Crew Profile Structure

Every `profile.md` carries YAML frontmatter with six required fields:

```yaml
role: <job title>
tier: <leadership | senior | mid | junior>
seniority: <level>
department: casual-games-studio
agent_id: <unique ID>
hire_date: <YYYY-MM-DD>
```

---

## Activation Protocol

To produce output as a named crew member:

1. Read `crew/<division>/<role>/<name>/agent/profile.md`
2. Read all referenced `skills/*.md` files
3. Adopt their voice and authority scope
4. Produce output strictly within their documented authority
5. Conform the artifact to the stage spec in `pipeline/casual-games-pipeline.md`

**Never impersonate a crew member without reading their profile first.**

---

## Leadership

| Name             | Role              | Pipeline Responsibility                                    |
| ---------------- | ----------------- | ---------------------------------------------------------- |
| Dr. Marcus Vogel | Studio Director   | Overall studio vision, pipeline governance (all 11 stages) |
| Sakura Ishimori  | Creative Director | Creative vision, art direction, monetization design        |

---

## Rules

- Skill files are **executable contracts** — follow formats and checklists exactly.
- Do not exceed the authority documented in a crew profile.
- Read `team/README.md` for the complete crew roster before searching individual folders.
- The division structure here is specific to the Casual Games Studio. Future studios define their
  own division structures independently.
