# RAG Deployment Documentation

> **Core Component 00 — Retrieval Augmented Generation Module**  
> **Laboratory Director:** Dr. Elias Vance  
> **Last Updated:** 2026-06-27

---

## Overview

This directory contains deployment documentation for two architecturally distinct RAG system
designs. Both share the same retrieval engineering foundations documented in this module; they
differ in deployment scope and the role of the host environment.

| Design Philosophy   | Document                                                         | When to Use                                                                                    |
| ------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Full-Stack RAG**  | [full-stack-rag-deployment.md](./full-stack-rag-deployment.md)   | Self-contained application: local LLM inference, Redis cache, Prometheus/Grafana observability |
| **Lightweight RAG** | [lightweight-rag-deployment.md](./lightweight-rag-deployment.md) | Retrieval component integrated into an agent runtime via MCP; no local LLM                     |

---

## Directory Structure

```
deployment/
├── README.md                              # This file — navigation index
├── full-stack-rag-deployment.md           # Full-stack RAG application deployment
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

---

## Deployment Guides and Reference Materials

The guides, reference materials, and configuration templates in this directory apply to the
**full-stack RAG deployment** and are cross-referenced from
[full-stack-rag-deployment.md](./full-stack-rag-deployment.md).

| Document                                                                            | Purpose                                                              |
| ----------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [Quick Start Guide](./full-stack/guides/quick-start-guide.md)                       | Complete deployment walkthrough with hardware-specific configuration |
| [LM Studio Optimization Guide](./full-stack/guides/lm-studio-optimization-guide.md) | Hardware-specific LM Studio configuration with thermal management    |
| [Quick Reference](./full-stack/reference/QUICK-REFERENCE.md)                        | One-page configuration summary with quick start commands             |
| [Model Comparison 2026](./full-stack/reference/model-comparison-2026.md)            | Comprehensive comparison of open-source coding LLMs with benchmarks  |

---

## Related Module References

| Reference                    | Location                              |
| ---------------------------- | ------------------------------------- |
| CC-00 RAG Architecture       | `../architecture/overview.md`         |
| Index Sync Hook Pattern      | `../patterns/index-sync-hooks.md`     |
| Evaluation and MRR Baselines | `../evaluation/reference-table.md`    |
| CC-00 Context Engineering    | `../../context-engineering/README.md` |
| CC-00 Harness Engineering    | `../../harness-engineering/README.md` |

---

**Maintained by:** Core Component 00 Laboratory  
**Laboratory Director:** Dr. Elias Vance  
**Contact:** Via workspace agent activation protocol (AGENTS.md § 2.3)
