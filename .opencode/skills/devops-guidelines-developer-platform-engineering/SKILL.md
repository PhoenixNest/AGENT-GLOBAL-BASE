---
name: devops-guidelines-developer-platform-engineering
description: 'Devops skill: Developer Platform Engineering'
---

# Developer Platform Engineering

## Purpose

Build and operate the internal developer platform that enables 50+ engineers across 5 divisions to ship code safely and quickly. The platform is a product — the engineering teams are the customers. Platform success is measured by adoption rate, deployment frequency, and developer satisfaction, not by feature count.

## Platform Philosophy: Golden Paths, Not Guardrails

**Golden path:** A well-documented, pre-approved, fully-supported way to build, test, and deploy a service. Teams may deviate if they have a compelling reason, but the golden path must be so good that deviation feels like a step backward.

**Guardrails (rejected approach):** Restrictive policies that block engineers from deploying. This creates shadow IT, manual workarounds, and resentment.

```
Golden Path = 80% of teams should use it because it's the easiest option
Guardrails  = 100% of teams must use it because everything else is blocked
```

## Internal Developer Portal (Backstage)

### Service Catalog Schema

Every service registered in the catalog must include:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: orders-service
  description: Order management service — handles order creation, cancellation, and status tracking
  tags: [backend, orders, production, tier-1]
  annotations:
    github.com/project-slug: company/orders-service
    backstage.io/techdocs-ref: dir:docs
    sonarqube.org/project-key: orders-service
spec:
  type: service
  lifecycle: production
  owner: team-orders-backend
  system: order-management
  dependsOn: [api-gateway, payment-service, inventory-service]
```

**Ownership model:** Every service has a single owning team. No orphaned services. If a team is disbanded, services must be reassigned before the team's Jira/Slack accounts are deactivated.

### Software Templates (Cookiecutter/Jinja2)

| Template        | Purpose                         | Tech Stack                               | SLO Tier        |
| --------------- | ------------------------------- | ---------------------------------------- | --------------- |
| `rest-api`      | Standard CRUD service           | Go + PostgreSQL + gRPC + OpenTelemetry   | Tier 2 (99.9%)  |
| `graphql-api`   | GraphQL API with federation     | Node.js + Apollo Federation + PostgreSQL | Tier 2 (99.9%)  |
| `worker`        | Background job processor        | Go + Kafka consumer + Redis locks        | Tier 3 (99%)    |
| `cron-job`      | Scheduled batch processing      | Python + Airflow DAG                     | Tier 3 (99%)    |
| `web-app`       | React frontend application      | Next.js + Vercel deployment              | Tier 1 (99.95%) |
| `mobile-bff`    | Backend-for-Frontend for mobile | Go + GraphQL gateway                     | Tier 1 (99.95%) |
| `data-pipeline` | ETL/streaming pipeline          | Python + Spark + Kafka                   | Tier 2 (99.9%)  |
| `ml-service`    | ML model serving                | Python + FastAPI + ONNX runtime          | Tier 2 (99.9%)  |

**What templates generate:**

- Full project scaffolding (source tree, config files, Dockerfile, helm charts)
- CI/CD pipeline (GitHub Actions with lint → test → build → scan → deploy)
- Monitoring (pre-built Grafana dashboards, PagerDuty routing)
- Documentation (TechDocs skeleton, runbook template, architecture decision log)
- Security (Semgrep rules, Trivy scanning, SBOM generation, Dependabot config)
- Testing (testcontainers setup, Pact contract testing skeleton, k6 load test template)

### Scorecard: Automated Quality Gates

Every service gets a quarterly scorecard (0–100):

| Metric                     | Weight | Gold Standard         | Minimum                   |
| -------------------------- | ------ | --------------------- | ------------------------- |
| Test coverage              | 25%    | ≥90%                  | ≥75%                      |
| SLO compliance             | 25%    | ≥99.9% uptime         | No SLO breach in quarter  |
| Security scan status       | 20%    | Zero findings         | No critical/high findings |
| Documentation completeness | 15%    | All sections complete | Owner + runbook present   |
| Deployment frequency       | 10%    | ≥10 deploys/week      | ≥1 deploy/week            |
| Incident rate              | 5%     | Zero P0/P1            | ≤1 P1 per quarter         |

**Scorecard usage:** Teams below 60 are flagged for platform intervention. VP of Platform meets with team lead to identify friction points. This is not punitive — it's diagnostic.

## CI/CD Pipeline Architecture

### Pipeline Stages (15-Minute Target)

```
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────┐   ┌──────────┐
│  Lint   │──▶│  Unit    │──▶│Integration│──▶│ SAST │──▶│ Container│
│  (30s)  │   │  Test    │   │  Test     │   │(60s) │   │  Build   │
│         │   │  (3 min) │   │  (5 min)  │   │      │   │  (2 min) │
└─────────┘   └──────────┘   └──────────┘   └──────┘   └────┬─────┘
                                                            │
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────┐   ┌────▼─────┐
│ E2E     │◀──│ Deploy   │◀──│ Container│◀──│ IaC  │◀──│ Canary   │
│ (nightly│   │ Staging  │   │ Scan     │   │Scan  │   │ Analysis │
│  only)  │   │ (2 min)  │   │ (60s)    │   │(30s) │   │ (2 min)  │
└─────────┘   └──────────┘   └──────────┘   └──────┘   └──────────┘
```

### Build Optimization

| Technique                    | Impact                                      | Implementation                                                        |
| ---------------------------- | ------------------------------------------- | --------------------------------------------------------------------- |
| Remote build caching (Bazel) | 60–80% cache hit rate on incremental builds | Bazel remote cache server; cache key = hash of inputs                 |
| Docker layer caching         | 40–60% faster image builds                  | BuildKit cache mount; multi-stage builds with dependency layers first |
| Dynamic test sharding        | 40% faster test execution                   | Run only tests affected by changed files (coverage mapping)           |
| Parallel stage execution     | 50% faster pipeline                         | Independent stages (SAST, lint, unit test) run in parallel            |

### GitOps Deployment with ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: orders-service-prod
spec:
  project: default
  source:
    repoURL: https://github.com/company/k8s-manifests.git
    targetRevision: main
    path: clusters/production/orders-service
  destination:
    server: https://kubernetes.default.svc
    namespace: orders
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
  healthCheck:
    script: |
      hs = {}
      if obj.status.phase == "Running" then
        hs.status = "Healthy"
      end
      return hs
```

**Progressive delivery:** Canary analysis runs for 30 minutes post-deploy. Metrics: error rate, P99 latency, CPU/memory utilization. If any metric deviates >2σ from baseline, ArgoCD auto-rolls back to previous revision.

## Self-Service Infrastructure

### Environment Provisioning

| Resource               | Provisioning Time | Method                                                               |
| ---------------------- | ----------------- | -------------------------------------------------------------------- |
| Dev environment        | <5 minutes        | `platform create-env --env=dev --service=orders-service`             |
| Staging environment    | <5 minutes        | Automated from PR targeting `main`                                   |
| Production environment | One-time setup    | Terraform module + manual VP Platform approval                       |
| PostgreSQL database    | <3 minutes        | `platform create-db --engine=postgres --tier=standard`               |
| Redis cache            | <2 minutes        | `platform create-cache --engine=redis --tier=standard`               |
| Kafka topic            | <1 minute         | `platform create-topic --topic=orders.order.created --partitions=12` |

### Terraform Module Standards

Every Terraform module must include:

- `variables.tf` with type constraints, descriptions, and validation rules
- `outputs.tf` with descriptions
- `examples/` directory with working usage examples
- `tests/` directory with Terratest integration tests
- `README.md` with usage instructions and architecture diagram

## Developer Experience Metrics

### DORA Metrics (Weekly Reporting)

| Metric                | Elite Benchmark              | Current Target            |
| --------------------- | ---------------------------- | ------------------------- |
| Deployment Frequency  | On-demand (multiple per day) | ≥10 deploys/week per team |
| Lead Time for Changes | <1 hour                      | <4 hours                  |
| Change Failure Rate   | 0–15%                        | <10%                      |
| Mean Time to Recovery | <1 hour                      | <30 minutes               |

### SPACE Framework (Quarterly Survey)

| Dimension         | Survey Questions (5-point Likert)                                        |
| ----------------- | ------------------------------------------------------------------------ |
| **Satisfaction**  | "I am satisfied with the developer tools available to me"                |
| **Performance**   | "I can accomplish my work without unnecessary friction"                  |
| **Activity**      | Number of PRs opened, reviews completed, services deployed               |
| **Communication** | "Cross-team collaboration is effective"                                  |
| **Efficiency**    | "I spend >60% of my time on deep work (not meetings, context switching)" |

**Target:** Average SPACE score ≥4.0/5.0. Any team scoring <3.5 triggers a platform intervention (VP Platform meets with team lead to identify and resolve friction).

## Quality Standards

- Pipeline execution time must not exceed 15 minutes from commit to staging deployment
- Self-service environment provisioning must complete in <10 minutes
- Platform uptime target: 99.95% (platform downtime blocks all engineering teams)
- All golden-path templates must pass security scanning with zero critical/high findings
- Onboarding time for new engineer: <5 days from first commit to first production deployment
- Platform adoption target: >90% of teams using IDP for service provisioning and deployment
- DORA metrics must trend toward elite benchmarks quarterly (no regression)
