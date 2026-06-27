# Full-Stack RAG Deployment — Local LLM + Retrieval + Observability

> **Core Component 00 — Retrieval Augmented Generation Module**
> **Scope:** Self-contained RAG application — embedding service, vector store, reranker, local LLM
> inference, Redis cache, and Prometheus/Grafana observability.
> **Audience:** Engineers deploying a standalone RAG system on local or on-premises hardware.
> **Laboratory Director:** Dr. Elias Vance
> **Last Updated:** 2026-05-05

---

## Overview

This guide covers production-ready deployment of a **full-stack RAG application** — a
self-contained system that handles every layer of the RAG pipeline: document ingestion,
embedding, vector search, reranking, context assembly, LLM inference, caching, and
observability. No external agent host is required; the system is the complete application.

For the lightweight retrieval-only variant (retrieval component integrated into an agent
runtime), see **[lightweight-rag-deployment.md](./lightweight-rag-deployment.md)**.

## Directory Structure

```
deployment/
├── README.md                              # Deployment overview and navigation index
├── full-stack-rag-deployment.md           # This file — full-stack application deployment
├── lightweight-rag-deployment.md          # Lightweight retrieval-only deployment
├── full-stack/                            # Full-stack system guides, reference, and config
│   ├── guides/
│   │   ├── quick-start-guide.md          # Complete RAG deployment walkthrough
│   │   └── lm-studio-optimization-guide.md # LM Studio configuration and thermal management
│   ├── reference/
│   │   ├── QUICK-REFERENCE.md            # One-page configuration summary
│   │   └── model-comparison-2026.md      # Comprehensive model benchmarks
│   └── config/
│       ├── lm-studio-config.json         # LM Studio server configuration
│       ├── rag-config.yaml               # RAG system configuration
│       └── .env.example                  # Environment variables template
└── lightweight/                           # Lightweight system guides and reference
    ├── guides/
    │   ├── mcp-server-setup.md           # Qdrant container setup, seeding, health check
    │   └── hook-configuration.md         # H-RAG02 operator guide
    └── reference/
        └── rag-sync-state-schema.md      # State file contract quick reference
```

## Available Documentation

### Deployment Guides

| Document                                                                                | Purpose                                                              | Target Audience                                         |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------- |
| **[Quick Start Guide](./full-stack/guides/quick-start-guide.md)**                       | Complete deployment walkthrough with hardware-specific configuration | Engineers deploying RAG on ASUS Zenbook Pro 14 Duo OLED |
| **[LM Studio Optimization Guide](./full-stack/guides/lm-studio-optimization-guide.md)** | Hardware-specific LM Studio configuration with thermal management    | Engineers configuring local LLM inference               |

### Reference Materials

| Document                                                                     | Purpose                                                             | Target Audience                            |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------ |
| **[Quick Reference](./full-stack/reference/QUICK-REFERENCE.md)**             | One-page configuration summary with quick start commands            | All users (quick lookup)                   |
| **[Model Comparison 2026](./full-stack/reference/model-comparison-2026.md)** | Comprehensive comparison of open-source coding LLMs with benchmarks | Technical decision-makers selecting models |

### Configuration Templates

| File                                        | Purpose                                     |
| ------------------------------------------- | ------------------------------------------- |
| **full-stack/config/lm-studio-config.json** | LM Studio server configuration template     |
| **full-stack/config/rag-config.yaml**       | RAG system configuration (production-ready) |
| **full-stack/config/.env.example**          | Environment variables for deployment        |

---

## Quick Start Guide Highlights

### What's Included

- ✅ **Hardware-optimized configuration** for RTX 4060 (8GB VRAM) + 32GB RAM
- ✅ **Step-by-step installation** for LM Studio, Qdrant, Redis, and Python dependencies
- ✅ **Model recommendation:** Qwen 3.6 35B-A3B (Q4_K_M) — best balance of accuracy and efficiency
- ✅ **CC-00 integration patterns** for Context Engineering and Harness Engineering
- ✅ **Production-ready configuration files** with YAML templates
- ✅ **Monitoring and evaluation** setup with Prometheus/Grafana
- ✅ **Troubleshooting guide** for common issues

### Key Configuration

```yaml
# Optimized for ASUS Zenbook Pro 14 Duo OLED
llm:
  model: "Qwen3.6-35B-A3B-Q4_K_M"
  context_length: 32768
  max_tokens: 4096

embedding:
  model: "BAAI/bge-small-en-v1.5"
  device: "cuda"

vector_db:
  provider: "qdrant"
  collection_name: "coding_knowledge_base"

performance:
  max_concurrent_requests: 4
  request_timeout: 180
```

---

## Model Comparison 2026 Highlights

### Top Recommendations

| Rank | Model                 | HumanEval | SWE-bench | VRAM (Q4_K_M) | License     |
| ---- | --------------------- | --------- | --------- | ------------- | ----------- |
| 🥇   | **Qwen 3.6 35B-A3B**  | 92.7%     | 73.4%     | 6.5GB         | Apache 2.0  |
| 🥈   | **GLM-5.1 32B**       | 94.2%     | 71.8%     | 7.2GB         | GLM License |
| 🥉   | **DeepSeek V4 Coder** | 90.5%     | 80.1%     | 14.0GB        | MIT         |

### Hardware Compatibility

**For RTX 4060 (8GB VRAM):**

- ✅ **Qwen 3.6 35B-A3B** — Perfect fit (6.5GB)
- ✅ **GLM-5.1 32B** — Tight fit (7.2GB)
- ✅ **Llama 4 27B** — Comfortable (5.8GB)
- ✅ **Gemma 4 27B** — Comfortable (5.9GB)
- ✅ **Kimi K2.6 14B** — Very comfortable (3.8GB)
- ❌ **DeepSeek V4** — Too large (14.0GB)

---

## Integration with CC-00 Engineering Stack

Both guides integrate with the Core Component 00 engineering modules:

### Context Engineering Integration

```python
from core_component_00.context_engineering.implementations.context_assembler import ContextAssembler

# 4-slot context window assembly
context_assembler = ContextAssembler(max_tokens=32768)
context_assembler.add_system(system_prompt)
context_assembler.add_retrieved(chunks)
context_assembler.add_history(conversation)
assembled_context = context_assembler.assemble()
```

### Harness Engineering Integration

```python
from core_component_00.harness_engineering.implementations.error_boundary import ErrorBoundary

# Safe execution with error boundaries
error_boundary = ErrorBoundary(timeout=180, max_retries=3)
result = await error_boundary.execute(llm_call, context=assembled_context)
```

---

## Performance Targets

| Metric                        | Target  | Measurement          |
| ----------------------------- | ------- | -------------------- |
| **Query Latency (p50)**       | <500ms  | Prometheus histogram |
| **Query Latency (p95)**       | <1200ms | Prometheus histogram |
| **Retrieval Accuracy (EM@5)** | >0.70   | Automated eval suite |
| **Cache Hit Rate**            | >40%    | Redis INFO stats     |
| **GPU Memory Usage**          | <7GB    | nvidia-smi           |

---

## Architecture Overview

```
User Query
    ↓
RAG Orchestrator
    ↓
[Cache Check] → Redis (5-min TTL)
    ↓
Embedding Service (bge-small-en-v1.5)
    ↓
Vector Database (Qdrant)
    ↓
Reranking Service (bge-reranker-large)
    ↓
Context Assembler (CC-00)
    ↓
LM Studio (Qwen 3.6 35B-A3B)
    ↓
Response + Citations
```

---

## Support and Troubleshooting

### Common Issues

| Issue          | Solution                              | Reference             |
| -------------- | ------------------------------------- | --------------------- |
| Out of VRAM    | Switch to Q5_K_M or use Kimi K2.6 14B | Quick Start Guide § 8 |
| Slow inference | Verify GPU acceleration enabled       | Quick Start Guide § 8 |
| Poor retrieval | Enable hybrid search, increase top_k  | Quick Start Guide § 8 |
| Cache misses   | Increase TTL, normalize queries       | Quick Start Guide § 8 |

### Diagnostic Commands

```powershell
# Check GPU utilization
nvidia-smi -l 1

# Monitor Redis cache
redis-cli INFO stats

# Check Qdrant collection
curl http://localhost:6333/collections/coding_knowledge_base

# Test LM Studio endpoint
curl http://localhost:1234/v1/models
```

---

## References

| Resource                      | Location                                    |
| ----------------------------- | ------------------------------------------- |
| **CC-00 RAG Architecture**    | `../architecture/overview.md`               |
| **CC-00 Context Engineering** | `../../context-engineering/README.md`       |
| **CC-00 Harness Engineering** | `../../harness-engineering/README.md`       |
| **LM Studio Documentation**   | https://lmstudio.ai/docs                    |
| **Qdrant Documentation**      | https://qdrant.tech/documentation/          |
| **Qwen 3.6 Model Card**       | https://huggingface.co/Qwen/Qwen3.6-35B-A3B |

---

## Document Status

| Document                     | Status           | Last Updated | Next Review |
| ---------------------------- | ---------------- | ------------ | ----------- |
| Quick Start Guide            | Production-ready | 2026-05-05   | 2026-06-05  |
| Model Comparison 2026        | Production-ready | 2026-05-05   | 2026-06-05  |
| LM Studio Optimization Guide | Production-ready | 2026-05-05   | 2026-06-05  |
| Quick Reference              | Production-ready | 2026-05-05   | 2026-06-05  |
| full-stack-rag-deployment.md | Current          | 2026-06-27   | As needed   |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Contact:** Via workspace agent activation protocol (AGENTS.md § 2.3)
