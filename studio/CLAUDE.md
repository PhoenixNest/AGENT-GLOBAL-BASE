# studio/ — The Studio

Entry point for the Studio system. Contains all active and future creative game development studios.

---

## What Lives Here

```
studio/
├── README.md          ← Studio index + naming conventions for future studios
└── casual-games/      ← Only active studio
```

---

## Active Studios

| Studio              | Path            | Status                 | Engine        |
| ------------------- | --------------- | ---------------------- | ------------- |
| Casual Games Studio | `casual-games/` | Active — Stage 0-ready | Unity 6.3 LTS |

No other studios have been instantiated yet. Future studios will be added as sibling folders to
`casual-games/` following the conventions below.

---

## Future Studio Conventions

New studios follow this structure:

```
studio/<studio-name>/
├── library/       ← Studio knowledge hub
├── pipeline/      ← Studio-specific pipeline definition
├── projects/      ← Per-game project folders (kebab-case slugs)
└── team/crew/     ← Studio crew by division
```

**Each studio defines its own pipeline independently.** Do not assume future studios will inherit
the Casual Games Studio's 11-stage pipeline. Studio identity, pipeline, and crew structure are
entirely self-contained per studio.

**Studio folder names use kebab-case** (e.g., `casual-games`, `narrative-studio`, `puzzle-lab`).

---

## Architecture Principle

Studios are architecturally independent of The Company. They share governance through the ASE
framework and report through the authority hierarchy, but their pipelines, crew structures, and
project conventions are self-contained. Do not import company pipeline stage numbers or department
structures into studio work.

---

## Where to Start

For the Casual Games Studio — the only active studio — start at:

```
studio/casual-games/library/overview/casual-games-studio.md
```

For studio-level conventions and the index of all studios:

```
studio/README.md
```
