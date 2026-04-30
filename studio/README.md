# Creative Studios

Independent creative studios operating under the organization. Each studio has its own crew, workflow, pipeline, and reference library — but reports to the parent company's Chief Officers.

Studios are not limited to game development. Future additions may include art studios, interactive media studios, or other creative disciplines.

## Active Studios

| Studio                          | Discipline        | Status          |
| ------------------------------- | ----------------- | --------------- |
| [Casual Games](./casual-games/) | Casual mini-games | Stage 0 — Ready |

## Directory Convention

Each studio lives at `studio/<studio-name>/` and follows this standard structure:

```
studio/<studio-name>/
├── README.md          ← Studio overview and navigation
├── library/           ← Reference documentation
│   ├── overview/      ← Studio charter, strategic brief, C-suite assessments
│   ├── topics/        ← Cross-cutting strategies (assets, security, etc.)
│   └── reference/     ← External resources and link collections
├── pipeline/          ← Studio-specific development workflow
├── projects/          ← Individual project folders (kebab-case slugs)
└── team/
    └── crew/          ← Agent profiles, skills, pipeline artifacts
```

Studio names use **kebab-case**. Pipeline stages, crew structure, and tooling are defined per-studio and may differ between studios.
