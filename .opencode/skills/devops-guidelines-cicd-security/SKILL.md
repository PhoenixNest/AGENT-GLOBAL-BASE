---
name: devops-guidelines-cicd-security
description: CI/CD security for mobile pipelines — meta-skill aggregating secrets management, runner hardening, artifact signing, and security gate enforcement. See sub-skills for implementation details. Owned by Thomas Zhang (DevOps Lead). Use during Stage 4 (Implementation Plan) for security gate design and Stage 6 (Code Review) for pipeline security audit. Trigger: CI/CD security overview, pipeline security, devops security.
prerequisites:
  - devops-guidelines-ci-cd-optimization

version: "2.0.0"
---

# CI/CD Pipeline Security (Meta-Skill)

**Category:** DevOps Security — Pipeline Hardening
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

This meta-skill aggregates four focused sub-skills covering the complete CI/CD security lifecycle. Use this skill for high-level pipeline security architecture; use sub-skills for implementation.

## Sub-Skills

| Sub-Skill                                 | Focus                     | Key Topics                                                        |
| ----------------------------------------- | ------------------------- | ----------------------------------------------------------------- |
| `devops-guidelines-cicd-secrets-mgmt`     | Secrets management        | Vault OIDC, dynamic credentials, secret rotation, audit logging   |
| `devops-guidelines-cicd-runner-hardening` | Pipeline hardening        | Ephemeral runners, OPA policies, action pinning, runner isolation |
| `devops-guidelines-cicd-artifact-signing` | Artifact signing          | Cosign keyless signing, Sigstore, Rekor transparency log          |
| `devops-guidelines-cicd-gate-enforcement` | Security gate enforcement | Multi-stage gates (SAST/DAST/Dependency/SBOM/Signing)             |

## Pipeline Integration

| Stage                                | Application                                                                                                                         |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 4** (Implementation Plan)    | CI/CD pipeline architecture designed with security controls; secrets management strategy documented; security gate criteria defined |
| **Stage 5** (Development)            | CI/CD pipeline operational with security gates; SAST/DAST/dependency scanning running on every PR; secrets managed via Vault        |
| **Stage 6** (Code Review)            | Pipeline security configuration reviewed; secrets management verified; gate effectiveness validated                                 |
| **Stage 8** (Integrity Verification) | Pipeline provenance verified; artifact signatures validated; SBOM completeness confirmed                                            |
| **Stage 10** (Release Readiness)     | CI/CD security gate results provided to CTO panel; confirms all security checks passed before release                               |

## Quality Standards

| Metric                 | Standard                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| **Secrets Management** | Zero hardcoded secrets in any repository or pipeline configuration                        |
| **Pipeline Isolation** | All CI/CD jobs run in ephemeral, isolated environments                                    |
| **Artifact Signing**   | 100% of release artifacts signed with cosign/Sigstore; signatures verifiable by any party |
| **Security Gates**     | All 5 gates (SAST, DAST, Dependency, SBOM, Signing) must pass before deployment           |
| **Action Pinning**     | 100% of CI/CD actions pinned to commit SHA                                                |
| **Secret Rotation**    | All CI/CD secrets rotated on ≤90-day schedule                                             |
| **Audit Trail**        | 100% of pipeline executions logged with artifact hashes, signatures, and gate results     |
| **Gate Reliability**   | Zero instances of security gate bypass in production                                      |
