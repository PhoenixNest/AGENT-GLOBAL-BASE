---
version: "1.0.0"
---

# Cloud Infrastructure

| Competency             | Description                                                                    | Quality Criteria                                                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| GCP Architecture       | GKE, Cloud SQL, Cloud Load Balancing, Cloud Storage, VPC networking            | Designs secure multi-tier GCP architecture; configures VPC with private subnets; sets up Cloud NAT for egress; manages IAM with least privilege |
| Terraform Modules      | Module design, variables, outputs, state management, workspace isolation       | Writes reusable Terraform modules with versioned interfaces; manages state with remote backend; implements workspace per environment            |
| Kubernetes Deployments | Deployment strategies (blue-green, canary, rolling), HPA, PDB, resource quotas | Configures zero-downtime deployments; implements horizontal pod autoscaling; sets pod disruption budgets for availability                       |
| Multi-Region Setup     | Regional traffic routing, data replication, latency-based routing, failover    | Designs active-active or active-passive multi-region architecture; configures global load balancer with health-based failover                   |
| Disaster Recovery      | RPO/RTO definition, backup strategies, failover runbooks, DR drills            | Designs DR strategy aligned with RPO/RTO targets; automates backup and recovery; conducts regular DR drills                                     |

## RPO/RTO Targets

| System       | RPO           | RTO        | Strategy                                |
| ------------ | ------------- | ---------- | --------------------------------------- |
| API Services | 0 (stateless) | 15 minutes | Multi-region active-active              |
| PostgreSQL   | 5 minutes     | 30 minutes | Cross-region read replica + promotion   |
| Redis        | 1 hour        | 1 hour     | Rebuild from database                   |
| S3 Storage   | 0             | 15 minutes | Cross-region replication                |
| Kafka        | 1 hour        | 2 hours    | MirrorMaker 2 cross-cluster replication |

## Regional Failure Recovery

### Scenario: us-central1 region unavailable

1. **Detection** (0-5 min)
   - Cloud monitoring alerts trigger
   - Global load balancer detects unhealthy backend

2. **Automatic failover** (5-15 min)
   - Load balancer shifts traffic to europe-west1
   - DNS TTL expires, new traffic routed to EU

3. **Database promotion** (15-30 min)
   - Promote Cloud SQL read replica to primary
   - Update application configuration
   - Verify data consistency

4. **Verification** (30-45 min)
   - Run smoke tests against EU region
   - Verify all services operational
   - Confirm data integrity

5. **Communication**
   - Update status page
   - Notify stakeholders
   - Begin post-incident review

### Recovery Commands

# Promote Cloud SQL read replica

gcloud sql instances promote-read-replica api-database-replica

# Update application to use new primary

kubectl set env deployment/api DATABASE_HOST=<new-primary-ip>

# Verify replication

gcloud sql instances describe api-database-replica | grep -A5 replicaConfiguration

```

## Pipeline Integration

**Stage 3 (Architecture):** GCP architecture diagrams show all services, networking, and security boundaries. ADR required for GKE vs alternatives, multi-region strategy.

**Stage 4 (Implementation Plan):** Terraform modules authored as infrastructure dependencies. Deployment strategy selected per service. DR runbooks drafted.

**Stage 5 (Development):** Infrastructure provisioned via Terraform. GKE clusters deployed. Cloud SQL configured with read replicas. Load balancer configured.

**Stage 6 (Code Review):** Review Terraform module correctness. Validate Kubernetes resource configurations. Check security settings (workload identity, shielded nodes).

**Stage 7 (Testing):** Load tests validate auto-scaling. Failover tests validate DR procedures. Chaos tests validate pod disruption budgets.

**Stage 10 (Release Readiness):** Panel confirms infrastructure matches architecture, multi-region failover tested, DR runbooks validated, monitoring operational.

## Quality Standards

| Metric                          | Target                                        | Measurement                |
| ------------------------------- | --------------------------------------------- | -------------------------- |
| Infrastructure as Code coverage | 100% of infrastructure via Terraform          | Infrastructure audit       |
| Terraform module reusability    | All modules parameterized, versioned          | Module review              |
| Deployment zero-downtime        | 100% of deployments without downtime          | Deployment metrics         |
| Auto-scaling responsiveness     | Scale up within 2 minutes of threshold breach | HPA metrics                |
| Multi-region failover time      | < 15 minutes                                  | DR drill results           |
| Database RPO compliance         | < 5 minutes data loss                         | Replication lag monitoring |
| Resource utilization            | 60-80% average CPU/memory                     | GKE metrics                |
| Cost efficiency                 | Within 10% of estimate                        | GCP billing                |


---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
```
