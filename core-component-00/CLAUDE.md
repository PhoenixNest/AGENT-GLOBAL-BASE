# core-component-00/ — CC-00 LLM Engineering Laboratory

Entry point for the Core Component 00 applied research laboratory. Read this before any CC-00 work.

---

## What This Is

CC-00 is the organisation's centralised LLM engineering laboratory and the foundational dependency
for every agent-powered system built here. It houses five engineering modules plus a governing
meta-layer (ASGF), production-grade Python implementations, and active research programmes.

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
| 1 — What to write         | `framework/01-prompt-engineering/`          | Knowledge base        | No         |
| 2 — How to structure it   | `framework/02-context-engineering/`         | Knowledge + Framework | Yes        |
| 3 — How to execute safely | `framework/03-harness-engineering/`         | Production Framework  | Yes        |
| 4 — Where to get content  | `framework/04-retrieval-augmented-generation/` | Production Framework  | Yes        |
| 5 — How agents cooperate  | `framework/05-multi-agent-engineering/`     | Production Framework  | Yes        |

ASGF (Agent Systems Governance Framework) is the **meta-layer above all five** — not a sixth module. See
`framework/00-agent-systems-governance-framework/`.

---

## Key Production Implementations

All paths relative to `core-component-00/`:

| File                                                                                  | Module | Purpose                                                |
| -------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------ |
| `framework/02-context-engineering/implementations/context_assembler.py`                | CE     | Four-slot context window assembly                      |
| `framework/02-context-engineering/implementations/memory_store.py`                     | CE     | Episodic, semantic, procedural, working memory         |
| `framework/02-context-engineering/implementations/context_compressor.py`               | CE     | Long-session compression                               |
| `framework/03-harness-engineering/implementations/error_boundary.py`                   | HE     | Timeout, rate-limit, validation recovery               |
| `framework/03-harness-engineering/implementations/context_monitor.py`                  | HE     | Token budget enforcement                               |
| `framework/03-harness-engineering/implementations/tool_registry.py`                    | HE     | Tool whitelists, call limits, dangerous task detection |
| `framework/05-multi-agent-engineering/implementations/swarm_orchestrator.py`           | MAE    | Swarm topology orchestration                           |
| `framework/05-multi-agent-engineering/implementations/handoff_packet.py`               | MAE    | Context Handoff Protocol                               |

---

## Running Tests (PowerShell)

Run tests **per-module from the module folder** to avoid duplicate-package import collisions:

```powershell
# From core-component-00/
pytest framework/02-context-engineering/testing/ -v
pytest framework/03-harness-engineering/testing/ -v
pytest framework/04-retrieval-augmented-generation/testing/ -v
pytest framework/05-multi-agent-engineering/testing/ -v
```

Do NOT run all modules together with a single root-level `pytest .` — this causes import conflicts.

Parallel workers: `pytest -n <N>` — keep N ≤ 10 on this machine (i9-13900H, 14 cores).

---

## Environment Notes (Windows)

- **RAG dependencies are heavy** — install only when needed:
  ```powershell
  pip install -r framework/04-retrieval-augmented-generation/requirements.txt
  python -m spacy download en_core_web_sm
  ```
- **GPU:** RTX 4060 (8 GB GDDR6) supports CUDA — always verify
  `torch.cuda.is_available()` before assuming GPU is available.
- **Import path:** Tests use `from implementations.<module>` after inserting the module root on
  `sys.path`. Run from the module folder, not the workspace root.

---

## ASGF Governance (Mandatory)

All LLM-powered systems built in this workspace are bound by the ASGF framework — ratified via
`ADR-ASGF-001`. Build new systems on CC-00 patterns; do not invent ad-hoc approaches.

Governing documents: `framework/00-agent-systems-governance-framework/governance/`

> **Layout note:** All five engineering modules plus ASGF now live under `framework/`, numbered
> `00`–`05` (`00-agent-systems-governance-framework/` through `05-multi-agent-engineering/`). MCP
> servers, maintenance records, benchmarks, and remediation live under `platform/` (unnumbered).

---

## Where to Look

| I need…                                                         | Go to                                                       |
| --------------------------------------------------------------- | ------------------------------------------------------------ |
| Full lab overview + researcher profile                          | `README.md`                                                  |
| Governing framework + compliance                                | `framework/00-agent-systems-governance-framework/`            |
| Synthesis of all five layers                                    | `framework/00-agent-systems-governance-framework/CONCEPTS.md` |
| Prompt patterns                                                 | `framework/01-prompt-engineering/`                            |
| Context window architecture                                     | `framework/02-context-engineering/`                           |
| Safe model execution                                            | `framework/03-harness-engineering/`                           |
| RAG pipelines                                                   | `framework/04-retrieval-augmented-generation/`                |
| Multi-agent / swarm systems                                     | `framework/05-multi-agent-engineering/`                       |
| MCP server implementations (deployment surface)                 | `platform/model-context-protocol-servers/`                    |
| Lab Director persona + crew roster                              | `crew/`                                                       |
| Research reports (CC-00 engineering + LLM research)             | `telescope/`                                                  |
| Maintenance operations log (servers, dependencies, MCP infra)   | `platform/maintenance-records/`                                |
| Enterprise benchmark assessments (module vs. industry practice) | `platform/benchmarks/`                                        |
| Remediation execution log (P0/P1 benchmark findings)            | `platform/remediation/`                                       |
| Cross-cutting / workspace-wide research                         | workspace-root `telescope/`                                   |
