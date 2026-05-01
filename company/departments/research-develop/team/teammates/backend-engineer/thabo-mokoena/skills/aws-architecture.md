---
name: aws-architecture
description: Design and implement AWS cloud architectures for the company's backend workloads — including ECS/Fargate container orchestration, RDS database tiers, S3 lifecycle management, and IAM least-privilege policies — aligned with the Stage 3 Deployment ADR.
version: "1.0.0"
---

# AWS Architecture

| Competency          | Description                                                         | Quality Criteria                                                                                                                |
| ------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| ECS/Fargate         | Container deployment and service scaling on ECS Fargate             | Services defined as IaC (Terraform/CDK); auto-scaling configured with CPU/memory targets; health checks on all task definitions |
| RDS & Aurora        | Relational database tier design — multi-AZ, read replicas, failover | Multi-AZ enabled for production; automated backups with 30-day retention; parameter group tuned for workload type               |
| S3 Lifecycle        | Object storage design with lifecycle policies and encryption        | Lifecycle rules move objects to Intelligent-Tiering or Glacier after defined periods; SSE-S3 or SSE-KMS encryption enforced     |
| IAM Least Privilege | Design IAM roles and policies with minimum required permissions     | No wildcards in resource ARNs; roles scoped to specific services; periodic access review with AWS IAM Access Analyzer           |

## Execution Guidance

### AWS Architecture Tiers

| Tier       | Services                                            | Sizing Guidance                          |
| ---------- | --------------------------------------------------- | ---------------------------------------- |
| Compute    | ECS Fargate, Lambda (async)                         | CPU: 0.5–4 vCPU; Memory: 1–8 GB per task |
| Database   | RDS Aurora PostgreSQL (multi-AZ), ElastiCache Redis | db.r6g.large minimum for production      |
| Storage    | S3 Standard → Intelligent-Tiering → Glacier         | Lifecycle transition at 30/90/365 days   |
| Networking | VPC with private subnets, NAT Gateway, ALB          | ALB idle timeout 60s for mobile clients  |

### IaC Standards

All AWS resources must be defined as Infrastructure as Code (Terraform or AWS CDK). No manual console creation for production resources. IaC changes go through the same PR review process as application code.
