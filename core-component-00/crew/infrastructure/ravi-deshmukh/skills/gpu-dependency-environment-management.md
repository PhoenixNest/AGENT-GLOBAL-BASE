---
name: cc00-gpu-dependency-environment-management
description: Reproducible GPU/dependency environment provisioning for the CC-00 lab's local RTX 4060 dev environment. Owned by Ravi Deshmukh (Infrastructure Engineer). Trigger: dev environment setup, GPU dependency, CUDA configuration, spaCy install.
version: "1.0.0"
---

# GPU & Dependency Environment Management

**Skill ID:** gpu-dependency-environment-management
**Role:** Infrastructure Engineer
**Seniority:** L3 — Senior

## Overview

Provisions and maintains reproducible GPU and dependency environments for CC-00's local
development setup (RTX 4060, Windows), with primary focus on the RAG module's heavy dependency
footprint (`requirements.txt`, spaCy models, vector index libraries).

## Tools & Frameworks

| Tool                         | Proficiency | Use Case                                                           |
| ---------------------------- | ----------- | ------------------------------------------------------------------ |
| CUDA/Windows GPU tooling     | Expert      | `torch.cuda.is_available()` verification, driver/toolkit alignment |
| Python dependency management | Expert      | Reproducible `requirements.txt` installs across module boundaries  |
| spaCy model management       | Advanced    | `en_core_web_sm` and related model installs/updates                |

## Module Ownership

- Owns the RAG module's dependency install process (`pip install -r retrieval-augmented-generation/requirements.txt`,
  `python -m spacy download en_core_web_sm`) and documents any environment drift
- Verifies GPU availability assumptions across the crew rather than letting each engineer
  independently rediscover `torch.cuda.is_available()` failures
- Coordinates onboarding environment setup for all new hires, not just RAG-specific ones

## Scenarios & Trade-offs

### Scenario 1: A New Dependency Conflicts with an Existing Module's Pinned Versions

- **Approach:** Isolate per-module environments where genuinely necessary rather than forcing one
  global environment that can't satisfy all four modules simultaneously
- **Trade-off:** Per-module isolation adds setup complexity vs. one shared environment
- **Quality Bar:** Any version conflict is documented with the specific modules affected, not
  silently resolved by picking one module's version and hoping the other still works

### Scenario 2: GPU Unavailable in a Given Session

- **Approach:** Every workflow that assumes GPU has a documented, tested CPU fallback path
- **Trade-off:** Maintaining both paths doubles some testing surface
- **Quality Bar:** No module's core functionality silently fails when GPU is unavailable — it
  degrades to a documented, working CPU path

## Quality Standards

- Environment setup is reproducible from a clean machine, documented step by step
- Every dependency addition is verified against all four modules' existing requirements, not just
  the module that needed it
- GPU availability is verified, never assumed, per `core-component-00/CLAUDE.md`'s existing rule

## References

- `core-component-00/CLAUDE.md` § Environment Notes (Windows)
- `core-component-00/retrieval-augmented-generation/requirements.txt`
