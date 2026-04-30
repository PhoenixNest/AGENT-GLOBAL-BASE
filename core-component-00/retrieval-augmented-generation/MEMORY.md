# RAG System Documentation Index

## Overview

This directory contains enterprise-level documentation for implementing Retrieval Augmented Generation (RAG) systems in production environments. All documentation follows Prettier formatting standards.

---

## Quick Navigation

| Category         | Documents                                                                                                                                                 | Purpose                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Architecture** | [overview.md](./architecture/overview.md), [diagrams.md](./architecture/diagrams.md)                                                                      | System design patterns and architecture diagrams  |
| **Components**   | [reference-table.md](./components/reference-table.md), [quick-reference.md](./components/quick-reference.md)                                              | Component specifications and integration patterns |
| **Evaluation**   | [reference-table.md](./evaluation/reference-table.md), [edge-cases.md](./evaluation/edge-cases.md), [quick-reference.md](./evaluation/quick-reference.md) | Metrics, benchmarks, and testing frameworks       |
| **Integrations** | [overview.md](./integrations/overview.md), [reference.md](./integrations/reference.md)                                                                    | Data source connectors and ingestion patterns     |
| **Security**     | [guide.md](./security/guide.md), [reference.md](./security/reference.md)                                                                                  | Security controls, compliance, and audit logging  |
| **Templates**    | [deployment-template.yaml](./templates/deployment-template.yaml), [quick-reference.md](./templates/quick-reference.md)                                    | Production deployment configurations              |
| **Tools**        | [initialize.py](./tools/initialize.py), [utility-guide.md](./tools/utility-guide.md)                                                                      | Utility scripts and monitoring tools              |

---

## Core Documentation Files

- [`README.md`](./README.md) - Project overview and quickstart guide
- [`architecture/overview.md`](./architecture/overview.md) - High-level system architecture
- [`architecture/diagrams.md`](./architecture/diagrams.md) - Visual architecture diagrams (Mermaid)
- [`components/reference-table.md`](./components/reference-table.md) - Component specifications matrix
- [`components/quick-reference.md`](./components/quick-reference.md) - Component quick reference guide
- [`evaluation/reference-table.md`](./evaluation/reference-table.md) - Evaluation metrics and benchmarks
- [`evaluation/edge-cases.md`](./evaluation/edge-cases.md) - Edge case handling strategies
- [`evaluation/quick-reference.md`](./evaluation/quick-reference.md) - Evaluation quick reference
- [`integrations/overview.md`](./integrations/overview.md) - Data source integration guide
- [`integrations/reference.md`](./integrations/reference.md) - Integration specifications
- [`security/guide.md`](./security/guide.md) - Security controls and compliance
- [`security/reference.md`](./security/reference.md) - Security reference documentation
- [`templates/deployment-template.yaml`](./templates/deployment-template.yaml) - Production deployment config
- [`templates/quick-reference.md`](./templates/quick-reference.md) - Deployment templates guide
- [`tools/initialize.py`](./tools/initialize.py) - Initialization script
- [`tools/utility-guide.md`](./tools/utility-guide.md) - Utility tools documentation
- [`requirements.txt`](./requirements.txt) - Python dependencies

---

## Quick Reference Documents

| Need                      | Document                   | Link                                                                       |
| ------------------------- | -------------------------- | -------------------------------------------------------------------------- |
| **Architecture patterns** | Architecture overview      | [architecture/overview.md](./architecture/overview.md)                     |
| **Component specs**       | Components reference table | [components/reference-table.md](./components/reference-table.md)           |
| **Evaluation metrics**    | Evaluation guide           | [evaluation/quick-reference.md](./evaluation/quick-reference.md)           |
| **Security checklist**    | Security guide             | [security/guide.md](./security/guide.md)                                   |
| **Deployment setup**      | Templates                  | [templates/deployment-template.yaml](./templates/deployment-template.yaml) |
| **Integration patterns**  | Integrations overview      | [integrations/overview.md](./integrations/overview.md)                     |

---

## File Status

All files created and formatted with Prettier per `.prettierrc.json` configuration.

### Total Files Created: 21 files across 7 directories

- Root: README.md, MEMORY.md, requirements.txt, .prettierrc.json (4)
- Architecture: overview.md, diagrams.md (2)
- Components: reference-table.md, quick-reference.md (2)
- Evaluation: reference-table.md, edge-cases.md, quick-reference.md (3)
- Integrations: overview.md, reference.md (2)
- Security: guide.md, reference.md (2)
- Templates: deployment-template.yaml, quick-reference.md (2)
- Tools: initialize.py, utility-guide.md (2)

---

## Quick Start Guide

1. **Read the README**: [`README.md`](./README.md) for project overview
2. **Understand architecture**: [`architecture/overview.md`](./architecture/overview.md) and [`architecture/diagrams.md`](./architecture/diagrams.md)
3. **Check components**: [`components/reference-table.md`](./components/reference-table.md)
4. **Review security**: [`security/guide.md`](./security/guide.md)
5. **Configure deployment**: [`templates/deployment-template.yaml`](./templates/deployment-template.yaml)
6. **Run evaluation**: [`evaluation/quick-reference.md`](./evaluation/quick-reference.md)

---

## Parent Project References

- [Harness Engineering Documentation](../../harness-engineering/README.md) - Core engineering patterns
- [Prompt Engineering Guide](../../prompt-engineering/README.md) - Prompt design patterns
