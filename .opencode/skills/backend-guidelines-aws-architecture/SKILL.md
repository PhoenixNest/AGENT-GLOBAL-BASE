---
name: backend-guidelines-aws-architecture
description: 'Backend skill: Aws Architecture'
---

# AWS Architecture

## Overview

This skill covers AWS cloud architecture patterns for backend services, enabling engineers to select the right services, design for high availability, implement secure networking, and optimize costs. It applies to Stage 3 (Architecture) where cloud infrastructure is designed, Stage 4 (Implementation Plan) where service selections are documented, and Stage 5 (Development) where cloud resources are provisioned.

## Compute Service Selection

| Pattern                 | Service    | Best When                                                     |
| ----------------------- | ---------- | ------------------------------------------------------------- |
| Serverless functions    | Lambda     | Event-driven, sporadic traffic, <15 min execution             |
| Container orchestration | ECS/EKS    | Microservices, predictable traffic, need container control    |
| Virtual machines        | EC2        | Legacy apps, specific OS requirements, sustained high compute |
| Managed runtime         | App Runner | Simple web services, minimal ops overhead                     |

**Selection criteria**: traffic pattern (sporadic vs. sustained), cold start tolerance, execution duration, team ops capacity, cost at projected scale.

## Storage Architecture

**Data store selection matrix**:

| Data Type           | Service                | Characteristics                        |
| ------------------- | ---------------------- | -------------------------------------- |
| Relational (OLTP)   | RDS (PostgreSQL/MySQL) | ACID transactions, complex queries     |
| Key-value / Session | DynamoDB / ElastiCache | Sub-millisecond reads, high throughput |
| Document            | DocumentDB / MongoDB   | Flexible schema, hierarchical data     |
| Object              | S3                     | Files, images, backups, data lake      |
| Search              | OpenSearch             | Full-text search, log analytics        |

## High Availability Design

**Multi-AZ architecture**:

- Application: Deploy across minimum 2 AZs, behind Application Load Balancer.
- Database: RDS Multi-AZ (automatic failover, <60 second RTO).
- Cache: ElastiCache with Multi-AZ enabled (automatic failover to replica).
- Queue: SQS (inherently multi-AZ, no additional configuration needed).

**DR strategy**:

- RPO: 15 minutes (continuous replication to secondary region).
- RTO: 1 hour (warm standby in secondary region).
- Route 53 health checks with failover routing policy.

## Networking Architecture

**VPC design for applications**:

- 3-tier architecture: public (ALB), private (app servers), isolated (databases).
- VPC endpoints for AWS services (no NAT for S3, DynamoDB, Secrets Manager).
- Transit Gateway for multi-VPC connectivity.
- PrivateLink for cross-account service access.

## Cost Optimization

- Right-sizing: use Compute Optimizer recommendations.
- Reserved Instances: 1-year standard for baseline compute (40-50% savings).
- Spot Instances: fault-tolerant workloads (70-90% savings).
- S3 lifecycle: transition to Intelligent-Tiering, then Glacier.
- CloudFront for static content (60-80% cheaper than S3 direct for high-traffic assets).
