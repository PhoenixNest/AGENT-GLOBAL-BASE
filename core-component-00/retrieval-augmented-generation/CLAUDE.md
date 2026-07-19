# core-component-00/retrieval-augmented-generation/ — Layer 4: RAG

CC-00 Layer 4 — "Where to get content." This module provides the production framework for building
retrieval-augmented generation pipelines that ground LLM responses in institutional knowledge.

---

## What Lives Here

This module contains knowledge documentation, production Python reference implementations, and a
lightweight pytest test suite. The test suite uses mock dependencies and requires no GPU, CUDA,
spaCy, or a live Qdrant instance.

---

## Directory Structure

```
retrieval-augmented-generation/
├── fundamentals/          ← Concepts: retrieval strategies, chunking, embedding, reranking
├── patterns/              ← Pipeline patterns (naive RAG, advanced RAG, modular RAG)
├── implementations/       ← Reference Python implementations (pure Python, injectable deps)
│   ├── chunker.py         ← FixedSizeChunker, SemanticChunker, HybridChunker
│   ├── retrieval.py       ← BM25 scoring, RRF fusion, ACL filtering
│   └── pipeline.py        ← RAGPipeline — end-to-end orchestration
├── testing/               ← Lightweight pytest suite (no heavy deps required)
│   ├── conftest.py        ← Mock embedder, mock Qdrant client, sample corpus
│   ├── test_chunking.py   ← Chunking strategy tests
│   ├── test_retrieval.py  ← BM25, RRF fusion, ACL filter tests
│   └── test_pipeline.py   ← End-to-end pipeline + Layer 2 contract tests
├── tools/                 ← Operational scripts (initialize.py, thermal_guardian.py)
└── requirements.txt       ← Heavy dependencies (install only when needed)
```

---

## Dependencies Warning

**RAG dependencies are heavy — install only when actually needed.**

```powershell
pip install -r retrieval-augmented-generation/requirements.txt
```

The spaCy language model is a separate install step:

```powershell
python -m spacy download en_core_web_sm
```

Do not install these dependencies as part of a general environment setup. Install them only when
actively working on RAG-related tasks.

---

## GPU Note

Some RAG workloads (embedding generation, reranking) benefit from GPU acceleration:

```python
import torch
print(torch.cuda.is_available())  # Must be True before assuming GPU
```

The RTX 4060 (8 GB GDDR6) supports CUDA. Always verify availability before running GPU-dependent
code — do not assume the GPU is accessible.

---

## Active Research Programme

| Programme                      | Status                    | Resolution / Open Question                                                                                                                                                                                                |
| ------------------------------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Retrieval Freshness Guarantees | **Resolved** (2026-06-26) | Staleness in agent-native deployments is a policy variable — the debounce threshold of a post-write hook — not an architectural invariant. See `patterns/index-sync-hooks.md` for the full resolution and generalisation. |

---

## Running the Test Suite

The test suite requires only standard library + pytest + unittest.mock — no heavy RAG dependencies:

```powershell
# From core-component-00/
pytest retrieval-augmented-generation/testing/ -v
```

All heavy dependencies (embedding models, Qdrant, spaCy) are replaced by deterministic stubs
defined in `testing/conftest.py`. The suite validates chunking invariants, BM25 scoring
correctness, RRF fusion deduplication, ACL enforcement, and the Layer 2 slot-assembly contract.

---

## User Reference Deployment

The production RAG deployment for this workspace is the **workspace-knowledge MCP server**:

```
core-component-00/mcp-servers/workspace-knowledge/
```

It uses BM25 + Qdrant hybrid retrieval and serves as the official reference example for
deploying a Layer 4 RAG pipeline in an agent-native environment.

---

## Relationship to Other Modules

RAG is the knowledge retrieval layer. It integrates with:

- **Context Engineering (Layer 2):** Retrieved chunks are injected into the context window
- **Harness Engineering (Layer 3):** Retrieval calls are wrapped in error boundaries
- **Multi-Agent Engineering (Layer 5):** RAG pipelines feed knowledge into swarm agent contexts

---

## Rules

- Install dependencies only when actively needed — `requirements.txt` is a heavy payload.
- Verify `torch.cuda.is_available()` before any GPU-dependent code path.
- No CC-00 implementation change merges until `pytest retrieval-augmented-generation/testing/ -v`
  passes. The lightweight suite requires no heavy deps and must always be green.
- New RAG patterns must conform to ASE compliance standards in
  `agent-systems-engineering/governance/compliance-standard.md`.
- Test files live in `testing/` — do not place them alongside implementation files.
