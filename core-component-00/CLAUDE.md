# core-component-00/ — CC-00 LLM Engineering Laboratory

Entry point for the Core Component 00 applied research laboratory. Read this before any CC-00 work.

---

## What This Is

CC-00 is the organisation's centralised LLM engineering laboratory and the foundational dependency
for every agent-powered system built here. It houses five engineering modules plus a governing
meta-layer (ASE), production-grade Python implementations, and active research programmes.

The **only runnable code in this entire workspace** lives under `core-component-00/`. Everything
else in the repository is Markdown documentation.

---

## Laboratory Director & Crew

| Field             | Detail                                       |
| ----------------- | -------------------------------------------- |
| Name              | Dr. Elias Vance                              |
| Internal Codename | core-component-00                            |
| Role              | Laboratory Director — Core Component 00      |
| Full Profile      | `crew/director/elias-vance/agent/profile.md` |

As of FY2026 Q3, the lab is staffed beyond the Director: 4 Research Engineer FTEs cover the four
production-grade modules (Context, Harness, RAG, Multi-Agent). Full roster and activation
protocol: `crew/README.md` and `crew/CLAUDE.md`.

---

## The Five-Module Engineering Stack

| Layer                     | Module Folder                              | Type                  | Has Tests? |
| ------------------------- | ------------------------------------------- | --------------------- | ---------- |
| 1 — What to write         | `engineering/prompt-engineering/`           | Knowledge base        | No         |
| 2 — How to structure it   | `engineering/context-engineering/`          | Knowledge + Framework | Yes        |
| 3 — How to execute safely | `engineering/harness-engineering/`          | Production Framework  | Yes        |
| 4 — Where to get content  | `retrieval-augmented-generation/`           | Production Framework  | Yes        |
| 5 — How agents cooperate  | `engineering/multi-agent-engineering/`      | Production Framework  | Yes        |

ASE (Agent Systems Engineering) is the **meta-layer above all five** — not a sixth module. See
`agent-systems-engineering/`.

---

## Key Production Implementations

All paths relative to `core-component-00/`:

| File                                                                         | Module | Purpose                                                |
| ---------------------------------------------------------------------------- | ------ | ------------------------------------------------------ |
| `engineering/context-engineering/implementations/context_assembler.py`      | CE     | Four-slot context window assembly                      |
| `engineering/context-engineering/implementations/memory_store.py`           | CE     | Episodic, semantic, procedural, working memory         |
| `engineering/context-engineering/implementations/context_compressor.py`     | CE     | Long-session compression                               |
| `engineering/harness-engineering/implementations/error_boundary.py`         | HE     | Timeout, rate-limit, validation recovery               |
| `engineering/harness-engineering/implementations/context_monitor.py`        | HE     | Token budget enforcement                               |
| `engineering/harness-engineering/implementations/tool_registry.py`          | HE     | Tool whitelists, call limits, dangerous task detection |
| `engineering/multi-agent-engineering/implementations/swarm_orchestrator.py` | MAE    | Swarm topology orchestration                           |
| `engineering/multi-agent-engineering/implementations/handoff_packet.py`     | MAE    | Context Handoff Protocol                               |

---

## Running Tests (PowerShell)

Run tests **per-module from the module folder** to avoid duplicate-package import collisions:

```powershell
# From core-component-00/
pytest engineering/context-engineering/testing/ -v
pytest engineering/harness-engineering/testing/ -v
pytest retrieval-augmented-generation/testing/ -v
pytest engineering/multi-agent-engineering/testing/ -v
```

Do NOT run all modules together with a single root-level `pytest .` — this causes import conflicts.

Parallel workers: `pytest -n <N>` — keep N ≤ 10 on this machine (i9-13900H, 14 cores).

---

## Environment Notes (Windows)

- **RAG dependencies are heavy** — install only when needed:
  ```powershell
  pip install -r retrieval-augmented-generation/requirements.txt
  python -m spacy download en_core_web_sm
  ```
- **GPU:** RTX 4060 (8 GB GDDR6) supports CUDA — always verify
  `torch.cuda.is_available()` before assuming GPU is available.
- **Import path:** Tests use `from implementations.<module>` after inserting the module root on
  `sys.path`. Run from the module folder, not the workspace root.

---

## ASE Governance (Mandatory)

All LLM-powered systems built in this workspace are bound by the ASE framework — ratified via
`ADR-ASE-001`. Build new systems on CC-00 patterns; do not invent ad-hoc approaches.

Governing documents: `agent-systems-engineering/governance/`

> **Note (2026-07-16):** `prompt-engineering/`, `context-engineering/`, `harness-engineering/`, and
> `multi-agent-engineering/` were relocated under `engineering/` on this date.
> `retrieval-augmented-generation/` and `agent-systems-engineering/` were not moved.

---

## Where to Look

| I need…                                             | Go to                                   |
| --------------------------------------------------- | --------------------------------------- |
| Full lab overview + researcher profile              | `README.md`                             |
| Governing framework + compliance                    | `agent-systems-engineering/`            |
| Synthesis of all five layers                        | `agent-systems-engineering/CONCEPTS.md` |
| Prompt patterns                                     | `engineering/prompt-engineering/`       |
| Context window architecture                         | `engineering/context-engineering/`      |
| Safe model execution                                | `engineering/harness-engineering/`      |
| RAG pipelines                                       | `retrieval-augmented-generation/`       |
| Multi-agent / swarm systems                         | `engineering/multi-agent-engineering/`  |
| Lab Director persona + crew roster                  | `crew/`                                 |
| Research reports (CC-00 engineering + LLM research) | `telescope/`                            |
| Cross-cutting / workspace-wide research             | `../telescope/` (workspace root)        |
