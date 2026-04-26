---
name: devops-guidelines-aws-management
description: AWS multi-account cloud governance for mobile backend infrastructure — AWS Organizations setup, Control Tower landing zones, service control policies (SCPs), cross-account IAM role design, centralized CloudTrail logging, and cost management with budget alerting. Owned by Thomas Zhang (DevOps Lead). Use during Stage 5 (Development) for cloud infrastructure provisioning and Stage 8 (Integrity Verification) for compliance conformance. Trigger: aws management, multi-account, control tower, SCP, cross-account IAM, CloudTrail, cloud governance, AWS Organizations, cost management.
prerequisites:
  - devops-overview

version: "1.0.0"
---

# AWS Management

## Overview

This skill covers AWS cloud platform management for a multi-account organization. It includes AWS Organizations setup, Control Tower governance, service control policies (SCPs), cross-account IAM role design, and centralized CloudTrail logging. It is used by DevOps engineers during Stage 5 (Development) for cloud infrastructure provisioning and Stage 8 (Integrity Verification) for compliance conformance.

## Multi-Account AWS Organization

**AWS Organizations + Control Tower**:

- Landing zone with centralized identity (SSO), logging, and security accounts.
- SCPs to prevent privileged actions (root usage, disabling CloudTrail, leaving the organization).
- Account vending machine for automated account creation with baseline guardrails.

**Account structure**:

| Account         | Purpose                                       | Guardrails                            |
| --------------- | --------------------------------------------- | ------------------------------------- |
| Management      | Organization root, billing                    | SCP: no resource creation             |
| Logging         | Centralized CloudTrail, Config, VPC Flow Logs | SCP: read-only for non-security       |
| Security        | GuardDuty, Security Hub, IAM Access Analyzer  | SCP: no internet-facing resources     |
| Shared Services | Shared infrastructure (ECS, RDS, ElastiCache) | SCP: no direct internet access        |
| Dev/Stage/Prod  | Application environments                      | SCP: environment-specific constraints |

## Cross-Account IAM Design

- Cross-account roles with trust policies limiting assume-role to specific accounts.
- Least-privilege permissions with permission boundaries for developer roles.
- Session duration limits (1 hour for humans, 15 minutes for CI/CD).
- No long-lived access keys — use IAM Roles Anywhere or OIDC federation.

## Centralized CloudTrail Logging

- Single management account trail delivering logs to centralized S3 bucket in Logging account.
- All regions, global service events, multi-region trail enabled.
- S3 lifecycle: transition to Glacier after 90 days, delete after 7 years.
- CloudWatch Logs subscription for real-time alerting on specific API actions.

## Cost Management

- AWS Budgets with alerting at 50%, 80%, and 100% of budget.
- Reserved Instance and Savings Plan optimization (quarterly review).
- Resource tagging policy: environment, team, cost-center, application.
