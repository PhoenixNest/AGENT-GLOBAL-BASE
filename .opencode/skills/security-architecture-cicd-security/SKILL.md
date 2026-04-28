---
name: security-architecture-cicd-security
description: CI/CD pipeline security — meta-skill aggregating secrets scanning, supply chain attestation, and pipeline access control. See sub-skills for implementation details. Owned by Yuki Matsuda (Security Engineer). Use during Stage 4 (Implementation Plan) for pipeline security design and Stage 6 (Code Review) for security gate validation. Trigger: CI/CD security overview, pipeline security architecture, supply chain security.
prerequisites:
  - security-overview

version: "2.0.0"
---

# CI/CD Pipeline Security (Meta-Skill)

**Category:** DevOps Security — Pipeline Hardening
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

This meta-skill aggregates three focused sub-skills covering CI/CD security from a security architecture perspective. Use this skill for high-level security architecture; use sub-skills for implementation.

## Sub-Skills

| Sub-Skill                                    | Focus                   | Key Topics                                                        |
| -------------------------------------------- | ----------------------- | ----------------------------------------------------------------- |
| `security-architecture-cicd-secrets-scan`    | Secrets scanning        | git-secrets, truffleHog, pre-commit hooks, secret detection       |
| `security-architecture-cicd-supply-chain`    | Supply chain security   | SLSA provenance, signed commits, SBOM, dependency allowlisting    |
| `security-architecture-cicd-pipeline-access` | Pipeline access control | RBAC, environment protection, branch protection, artifact storage |

## Pipeline Integration

| Stage                                | Application                                                                                                                         |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 4** (Implementation Plan)    | CI/CD pipeline architecture designed with security controls; secrets management strategy documented; security gate criteria defined |
| **Stage 5** (Development)            | CI/CD pipeline operational with security gates; SAST/DAST/dependency scanning running on every PR; secrets managed via Vault        |
| **Stage 6** (Code Review)            | Pipeline security configuration reviewed; secrets management verified; gate effectiveness validated                                 |
| **Stage 8** (Integrity Verification) | Pipeline provenance verified; artifact signatures validated; SBOM completeness confirmed                                            |
| **Stage 10** (Release Readiness)     | CI/CD security gate results provided to CTO panel; confirms all security checks passed before release                               |

## Quality Standards

| Metric               | Standard                                                                              |
| -------------------- | ------------------------------------------------------------------------------------- |
| **Secrets Scanning** | Zero hardcoded secrets detected in any commit or pipeline configuration               |
| **Supply Chain**     | SLSA Level 3 provenance for all release builds; 100% commits signed                   |
| **Access Control**   | Production deployments require 2+ approvals; runners have minimal permissions         |
| **Audit Trail**      | 100% of pipeline executions logged with artifact hashes, signatures, and gate results |
