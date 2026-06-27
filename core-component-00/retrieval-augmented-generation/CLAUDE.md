# core-component-00/retrieval-augmented-generation/ — Layer 4: RAG

CC-00 Layer 4 — "Where to get content." This module provides the production framework for building
retrieval-augmented generation pipelines that ground LLM responses in institutional knowledge.

---

## What Lives Here

This module contains knowledge documentation and a production Python implementation. Unlike Layers 2,
3, and 5, **there is no pytest test suite** for this module.

---

## Directory Structure

```
retrieval-augmented-generation/
├── fundamentals/          ← Concepts: retrieval strategies, chunking, embedding, reranking
├── patterns/              ← Pipeline patterns (naive RAG, advanced RAG, modular RAG)
├── implementations/       ← Production Python code
│   └── <rag-modules>      ← RAG pipeline components
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

## No Test Suite

Unlike Layers 2, 3, and 5, this module ships an implementation but **no pytest test suite**. There
are no automated tests to run. Validation of RAG pipeline behaviour happens through integration
testing in downstream systems.

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
- There is no test suite — validate RAG components through integration tests in consuming systems.
- New RAG patterns must conform to ASE compliance standards in
  `agent-systems-engineering/governance/compliance-standard.md`.
- Do not place test files here — if a test suite is added in the future, it belongs in a `testing/`
  subfolder following the pattern of the other CC-00 modules.
