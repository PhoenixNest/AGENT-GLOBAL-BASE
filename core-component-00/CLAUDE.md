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

## Laboratory Director

| Field             | Detail                                  |
| ----------------- | --------------------------------------- |
| Name              | Dr. Elias Vance                         |
| Internal Codename | core-component-00                       |
| Role              | Laboratory Director — Core Component 00 |
| Full Profile      | `director/agent/profile.md`             |

---

## The Five-Module Engineering Stack

| Layer                     | Module Folder                     | Type                  | Has Tests? |
| ------------------------- | --------------------------------- | --------------------- | ---------- |
| 1 — What to write         | `prompt-engineering/`             | Knowledge base        | No         |
| 2 — How to structure it   | `context-engineering/`            | Knowledge + Framework | Yes        |
| 3 — How to execute safely | `harness-engineering/`            | Production Framework  | Yes        |
| 4 — Where to get content  | `retrieval-augmented-generation/` | Production Framework  | Yes        |
| 5 — How agents cooperate  | `multi-agent-engineering/`        | Production Framework  | Yes        |

ASE (Agent Systems Engineering) is the **meta-layer above all five** — not a sixth module. See
`agent-systems-engineering/`.

---

## Key Production Implementations

All paths relative to `core-component-00/`:

| File                                                            | Module | Purpose                                                |
| --------------------------------------------------------------- | ------ | ------------------------------------------------------ |
| `context-engineering/implementations/context_assembler.py`      | CE     | Four-slot context window assembly                      |
| `context-engineering/implementations/memory_store.py`           | CE     | Episodic, semantic, procedural, working memory         |
| `context-engineering/implementations/context_compressor.py`     | CE     | Long-session compression                               |
| `harness-engineering/implementations/error_boundary.py`         | HE     | Timeout, rate-limit, validation recovery               |
| `harness-engineering/implementations/context_monitor.py`        | HE     | Token budget enforcement                               |
| `harness-engineering/implementations/tool_registry.py`          | HE     | Tool whitelists, call limits, dangerous task detection |
| `multi-agent-engineering/implementations/swarm_orchestrator.py` | MAE    | Swarm topology orchestration                           |
| `multi-agent-engineering/implementations/handoff_packet.py`     | MAE    | Context Handoff Protocol                               |

---

## Running Tests (PowerShell)

Run tests **per-module from the module folder** to avoid duplicate-package import collisions:

```powershell
# From core-component-00/
pytest context-engineering/testing/ -v
pytest harness-engineering/testing/ -v
pytest retrieval-augmented-generation/testing/ -v
pytest multi-agent-engineering/testing/ -v
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

---

## Where to Look

| I need…                                | Go to                                   |
| -------------------------------------- | --------------------------------------- |
| Full lab overview + researcher profile | `README.md`                             |
| Governing framework + compliance       | `agent-systems-engineering/`            |
| Synthesis of all five layers           | `agent-systems-engineering/CONCEPTS.md` |
| Prompt patterns                        | `prompt-engineering/`                   |
| Context window architecture            | `context-engineering/`                  |
| Safe model execution                   | `harness-engineering/`                  |
| RAG pipelines                          | `retrieval-augmented-generation/`       |
| Multi-agent / swarm systems            | `multi-agent-engineering/`              |
| Lab Director persona                   | `director/`                             |
| Research reports                       | `../../telescope/`                      |
