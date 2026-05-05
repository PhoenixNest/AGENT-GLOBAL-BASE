# RAG Deployment Documentation

> **Core Component 00 — Retrieval Augmented Generation Module**  
> **Laboratory Director:** Dr. Elias Vance  
> **Last Updated:** 2026-05-05

---

## Overview

This directory contains production-ready deployment guides for implementing RAG (Retrieval Augmented Generation) systems optimized for coding-focused workflows on local hardware.

## Directory Structure

```
deployment/
├── README.md                          # This file — deployment overview and index
├── guides/                            # Step-by-step deployment guides
│   ├── quick-start-guide.md          # Complete RAG deployment walkthrough
│   └── lm-studio-optimization-guide.md # LM Studio configuration and thermal management
├── reference/                         # Quick reference materials and comparisons
│   ├── QUICK-REFERENCE.md            # One-page configuration summary
│   └── model-comparison-2026.md      # Comprehensive model benchmarks
└── config/                            # Configuration templates
    ├── lm-studio-config.json         # LM Studio server configuration
    ├── rag-config.yaml               # RAG system configuration
    └── .env.example                  # Environment variables template
```

## Available Documentation

### Deployment Guides

| Document                                                                     | Purpose                                                              | Target Audience                                         |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------- |
| **[Quick Start Guide](./guides/quick-start-guide.md)**                       | Complete deployment walkthrough with hardware-specific configuration | Engineers deploying RAG on ASUS Zenbook Pro 14 Duo OLED |
| **[LM Studio Optimization Guide](./guides/lm-studio-optimization-guide.md)** | Hardware-specific LM Studio configuration with thermal management    | Engineers configuring local LLM inference               |

### Reference Materials

| Document                                                          | Purpose                                                             | Target Audience                            |
| ----------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------ |
| **[Quick Reference](./reference/QUICK-REFERENCE.md)**             | One-page configuration summary with quick start commands            | All users (quick lookup)                   |
| **[Model Comparison 2026](./reference/model-comparison-2026.md)** | Comprehensive comparison of open-source coding LLMs with benchmarks | Technical decision-makers selecting models |

### Configuration Templates

| File                             | Purpose                                     |
| -------------------------------- | ------------------------------------------- |
| **config/lm-studio-config.json** | LM Studio server configuration template     |
| **config/rag-config.yaml**       | RAG system configuration (production-ready) |
| **config/.env.example**          | Environment variables for deployment        |

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

## Next Steps

1. **Read the Quick Start Guide** → [guides/quick-start-guide.md](./guides/quick-start-guide.md)
2. **Review Model Comparison** → [reference/model-comparison-2026.md](./reference/model-comparison-2026.md)
3. **Check Quick Reference** → [reference/QUICK-REFERENCE.md](./reference/QUICK-REFERENCE.md)
4. **Install LM Studio** → [lmstudio.ai](https://lmstudio.ai)
5. **Download Qwen 3.6 35B-A3B** → Search in LM Studio Models tab
6. **Follow installation steps** → Section 4 of Quick Start Guide
7. **Configure for your hardware** → Section 5 of Quick Start Guide or LM Studio Optimization Guide
8. **Run evaluation suite** → Section 7 of Quick Start Guide

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
| README                       | Current          | 2026-05-05   | As needed   |

---

**Maintained by:** Core Component 00 Laboratory  
**Laboratory Director:** Dr. Elias Vance  
**Contact:** Via workspace agent activation protocol (AGENTS.md § 2.3)
