# telescope/ — Research Archive Hub

Centralized research documentation repository, maintained by Core Component 00. Read this before
documenting any research investigation in this workspace.

---

## What This Is

`telescope/` is the workspace's research archive — a structured repository for documenting
investigations, experiments, literature reviews, and research reports. It is physically at the
workspace root but is owned and maintained by the CC-00 laboratory under Dr. Elias Vance's
direction.

---

## Directory Structure

```
telescope/
├── README.md              ← Archive index — list of all research reports
└── template/              ← Report template (use this for every new report)
    └── research-report.md ← The canonical template file
```

---

## Creating a New Research Report

1. Create a new folder: `YYYY-MM-DD-<slug>/`
2. Copy the template: `template/research-report.md` → `YYYY-MM-DD-<slug>/research-report.md`
3. Complete the report in the new folder
4. Add an entry to `README.md` (the archive index)

---

## Folder Naming Convention

```
YYYY-MM-DD-<slug>/
```

Where:

- `YYYY-MM-DD` is the date the investigation was initiated
- `<slug>` is a kebab-case descriptive label for the research topic

Examples:

```
2026-05-15-context-compression-bounds/
2026-06-01-retrieval-freshness-study/
2026-06-18-multi-agent-memory-coherence/
```

---

## Who Can Write Here

Any team or agent in the workspace may document research here — not only CC-00. The telescope is
a shared resource. However:

- CC-00 research programmes are the primary contributors
- Company and studio teams may document technology investigations, competitive research, or
  architectural studies
- All reports must follow the template format from `template/research-report.md`
- All reports must be indexed in `README.md`

---

## Report Template Fields

The canonical template (`template/research-report.md`) includes:

| Section           | Purpose                                 |
| ----------------- | --------------------------------------- |
| Title & Metadata  | Date, author, research question, status |
| Executive Summary | 2–3 sentence summary of findings        |
| Background        | Context and motivation                  |
| Methodology       | How the investigation was conducted     |
| Findings          | What was discovered                     |
| Analysis          | Interpretation of findings              |
| Conclusions       | Answers to the research question        |
| Recommendations   | Actionable next steps                   |
| References        | Sources cited                           |

Do not deviate from this structure without a documented reason in the report itself.

---

## Rules

- Every new report must live in a `YYYY-MM-DD-<slug>/` folder containing `research-report.md`.
- Every new report must be indexed in `telescope/README.md`.
- Use the template from `template/research-report.md` — do not invent alternative formats.
- This archive is append-oriented. Do not edit published reports except to correct factual errors
  (note the correction with a date in the report's metadata).
