---
name: backend-engineering
description: Super-Skill router for Backend Engineering. Dynamically loads specific sub-skills from its references/ directory.
---

# Backend Engineering

This is the router skill for the `backend-engineering` domain. It serves as an entry point for the agent to access a library of specific sub-skills located in the `references/` subdirectory.

## How to use

When you need expertise in Backend Engineering, explore the `references/` directory and read the highly specific sub-skill markdown files.

## Available Sub-Skills

| Skill File                                                                     | Location                          | Description                                                                                                            |
| ------------------------------------------------------------------------------ | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `api-gateway-design.md`                                                        | `backend-engineering/references/` | Gateway Patterns; Rate Limiting; mTLS & Security; Load Balancing; Health Checks                                        |
| `api-testing.md`                                                               | `backend-engineering/references/` | Contract Testing; Integration Testing; Performance Benchmarking; API Documentation Validation; Negative Testing        |
| `apollo-server,-schema-stitching,-dataloader,-subscriptions.md`                | `backend-engineering/references/` | Schema Design; Resolver Optimization; DataLoader Pattern; Apollo Federation; Subscriptions                             |
| `aws-architecture-foundations,-service-selection,-multi-service-deployment.md` | `backend-engineering/references/` | ECS/Fargate; RDS & Aurora; S3 Lifecycle; IAM Least Privilege                                                           |
| `backend-chapter-leadership.md`                                                | `backend-engineering/references/` | Implementation patterns for backend chapter leadership                                                                 |
| `backend-observability.md`                                                     | `backend-engineering/references/` | **Instrumentation**; **Log Management**; **Metrics Engineering**; **Distributed Tracing**; **Alerting & SLOs**         |
| `cicd-infrastructure-engineering.md`                                           | `backend-engineering/references/` | CI/CD Architecture; Build Pipeline Optimization; Multi-Platform Builds; Pipeline Security; i18n Pipeline Engineering   |
| `circuit-breakers,-retry-logic,-fallback-handling,-third-party-integration.md` | `backend-engineering/references/` | SQL Fundamentals; Indexing; Query Optimization; Transaction Isolation; Alembic Migrations                              |
| `database-sharding.md`                                                         | `backend-engineering/references/` | Horizontal Partitioning; Sharding Strategies; Distributed Query Execution; Eventual Consistency; Failover Handling     |
| `event-sourcing.md`                                                            | `backend-engineering/references/` | Event Sourcing Patterns; CQRS Implementation; Kafka Integration; Event Schema Versioning; Replay Strategies            |
| `fastapi,-async-python,-pydantic,-postgresql.md`                               | `backend-engineering/references/` | Dependency Injection; Pydantic v2 Models; Async Endpoints; Background Tasks; Middleware Configuration                  |
| `go-concurrency,-postgresql,-microservices,-error-handling.md`                 | `backend-engineering/references/` | HTTP Handlers; Middleware Chains; Error Handling; Context Propagation; Structured Logging                              |
| `go-microservices-development,-production-patterns.md`                         | `backend-engineering/references/` | Idiomatic Go; gRPC Service Design; Concurrency Safety; Observability                                                   |
| `postgresql-query-optimization,-indexing,-execution-plans.md`                  | `backend-engineering/references/` | Query Plan Analysis; Index Design; Connection Pooling; Partitioning                                                    |
| `real-time-architecture.md`                                                    | `backend-engineering/references/` | WebSocket Architecture; SSE vs WebSockets; GraphQL Subscriptions; Message Queuing; Connection Pool Management          |
| `rest-api-design,-openapi-3.0,-request-validation,-pagination.md`              | `backend-engineering/references/` | Table-Driven Tests; Interface Mocking; Integration Testing; HTTP Handler Testing; Test Coverage                        |
| `security-patterns.md`                                                         | `backend-engineering/references/` | OWASP Top 10 (2021); API Security (OWASP API Top 10); Input Validation Pipelines; JWT Best Practices; Security Headers |
| `terraform,-ecs,-rds,-auto-scaling,-blue-green-deployments.md`                 | `backend-engineering/references/` | EC2 Instance Types; ECS Task Definitions; RDS Configuration; S3 Lifecycle Policies; IAM Roles & Policies               |

**Total Skills:** 18

### OWASP Top 10 (2021) — Implementation Controls; Primary Control; Broken Access Control |

| `terraform,-ecs,-rds,-auto-scaling,-blue-green-deployments.md` | `backend-engineering/references/` | Instance families (compute, memory, general), sizing, EBS volumes; ECS Task Definitions; Storage classes, lifecycle transitions, versioning, encryption; IAM Roles & Policies; Stack management, parameters, outputs, nested stacks, drift detection |

**Total Skills:** 18
