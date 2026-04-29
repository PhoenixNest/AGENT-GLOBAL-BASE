---
name: shared
description: Use for cross-cutting capabilities that span multiple domains — general performance optimization, WCAG mobile compliance roadmap, developer documentation, and test-driven development practices.
---

# Shared

## Overview

Cross-cutting capabilities and shared practices that apply across multiple functional domains. These guidelines are referenced by multiple category skills and cover general performance optimization, mobile accessibility compliance, developer documentation, and development methodology.

## Sub-Guidelines

| Guideline                 | File                                                                                                   | When to Use                                                        |
| ------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Performance Optimization  | [`guidelines/performance-optimization.md`](guidelines/performance-optimization.md)                     | General performance                                                |
| WCAG Mobile Roadmap       | [`guidelines/wcag-mobile-roadmap.md`](guidelines/wcag-mobile-roadmap.md)                               | WCAG 2.1 AA mobile                                                 |
| Developer Documentation   | [`guidelines/developer-documentation.md`](guidelines/developer-documentation.md)                       | Developer docs                                                     |
| Test-Driven Development   | [`guidelines/test-driven-development.md`](guidelines/test-driven-development.md)                       | TDD practices                                                      |
| WebAuthn & Biometric Auth | [`guidelines/webauthn-biometric-auth.md`](guidelines/webauthn-biometric-auth.md)                       | Passkeys, biometrics                                               |
| Multi-Tenant Isolation    | [`guidelines/multi-tenant-isolation.md`](guidelines/multi-tenant-isolation.md)                         | SaaS data isolation                                                |
| Docker Orchestration      | [`guidelines/docker-orchestration.md`](guidelines/docker-orchestration.md)                             | Container deployment                                               |
| Context Engineering       | [`guidelines/context-engineering.md`](guidelines/context-engineering.md)                               | Agent context assembly, positional optimization, MVC enforcement   |
| Inter-Agent Communication | [`guidelines/inter-agent-communication-protocol.md`](guidelines/inter-agent-communication-protocol.md) | Message formats, routing, escalation, SLAs for agent communication |
| Stage Transition Schemas  | [`guidelines/stage-transition-schemas.md`](guidelines/stage-transition-schemas.md)                     | JSON contracts for all 10 pipeline stage transitions               |
| Knowledge Transfer        | [`guidelines/knowledge-transfer-protocol.md`](guidelines/knowledge-transfer-protocol.md)               | 3-tier learning loop: session → project → institutional memory     |
| RAG Integration           | [`guidelines/rag-integration-blueprint.md`](guidelines/rag-integration-blueprint.md)                   | Semantic retrieval architecture and evolution roadmap              |
| Schema Validation         | [`guidelines/schema-validation-spec.md`](guidelines/schema-validation-spec.md)                         | Automated gate enforcement rules and error escalation              |
| ASE Adoption ADR          | [`guidelines/adr-ase-001.md`](guidelines/adr-ase-001.md)                                               | Formal ADR codifying ASE as permanent enterprise methodology       |
