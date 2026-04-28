---
name: gcp-multi-region
description: This skill guides the design and implementation of multi-region deployments on Google Cloud Platform for mobile backend services. It covers regional topology, traffic management.
---

# GCP Multi-Region Architecture

## Purpose

This skill guides the design and implementation of multi-region deployments on Google Cloud Platform for mobile backend services. It covers regional topology, traffic management, data replication, failover procedures, and disaster recovery planning. It is used by the CTO, Software Architect, and CIO during Stage 3 (Architecture) and Stage 5 (Development).

## Execution Guidance

### 1. Multi-Region Architecture Patterns

**Active-Active (preferred for mobile backends)**:

```
                  Global HTTPS Load Balancer
                   /           |           \
          us-central1    europe-west4    asia-northeast1
          (primary)      (secondary)     (secondary)
          /       \      /       \      /       \
        GKE      GKE  GKE      GKE  GKE      GKE
        Cloud SQL  ←─── Cloud SQL  ←─── Cloud SQL
         (primary)   (read replica)  (read replica)
```

**Active-Passive (cost-optimized)**:

- Primary region handles all traffic under normal conditions.
- Secondary region on standby with warm infrastructure.
- Failover triggered by health check failures or manual intervention.
- RTO (Recovery Time Objective): <15 minutes.
- RPO (Recovery Point Objective): <5 minutes.

### 2. Regional Service Selection

| Service              | Multi-Region Capability    | Notes                                                |
| -------------------- | -------------------------- | ---------------------------------------------------- |
| Cloud Load Balancing | Global Anycast             | Single anycast IP, routes to nearest healthy backend |
| Cloud Run            | Multi-region deployment    | Deploy same container to multiple regions            |
| GKE                  | Multi-cluster federation   | Use Anthos or manual cluster federation              |
| Cloud SQL            | Cross-region read replicas | Failover requires manual promotion                   |
| Cloud Spanner        | Natively multi-region      | Strong consistency across regions — higher latency   |
| Firestore            | Multi-region (default)     | Automatic replication, eventual consistency          |
| Cloud Storage        | Dual-region / Multi-region | 99.999999999% durability                             |
| Memorystore (Redis)  | Single region only         | Requires custom replication for multi-region         |

### 3. Traffic Management

**Global HTTPS Load Balancer configuration**:

- **Backend services**: One per region with health checks.
- **Health check path**: `/health` returning 200 with region identifier.
- **Failover policy**: Traffic shifts away from unhealthy regions automatically.
- **Affinity**: Use generated cookie or header affinity for stateful sessions.

**Traffic splitting strategies**:
| Strategy | Use Case | Implementation |
|----------|----------|----------------|
| Geographic routing | Serve users from nearest region | Load balancer default behavior |
| Weighted routing | Canary deployments, capacity testing | Cloud Load Balancing with backend weights |
| Failover routing | Disaster recovery | Primary backend with failover to backup |
| Latency-based routing | Optimize response time | Cloud CDN with edge caching |

### 4. Data Replication Strategy

**Cloud SQL cross-region replication**:

```
Primary (us-central1)
  ├── Read Replica (europe-west4) — 50-100ms replication lag
  ├── Read Replica (asia-northeast1) — 150-250ms replication lag
  └── Binary logs retained for 7 days (point-in-time recovery)
```

**Failover procedure**:

1. Detect primary region failure (health check timeout >60 seconds).
2. Promote read replica to primary (`gcloud sql instances promote-replica`).
3. Update DNS/load balancer backend to new primary.
4. Verify write operations succeed in new primary.
5. Rebuild former primary as new read replica when recovered.

**Cloud Spanner for strong consistency**:

- Use when ACID compliance across regions is non-negotiable.
- Multi-region instance: `nam3` (US multi-region), `eur3` (EU multi-region).
- Trade-off: Higher write latency (10-50ms) for strong consistency.

### 5. Disaster Recovery Planning

**DR runbook structure**:

```
disaster-recovery/
├── runbooks/
│   ├── region-failure.md       # Full region outage response
│   ├── database-failure.md     # Database failover procedure
│   ├── network-partition.md    # Network connectivity loss
│   └── data-corruption.md      # Point-in-time recovery
├── test-results/
│   ├── dr-test-2026-q1.md      # Quarterly DR test results
│   └── dr-test-2026-q2.md
└── recovery-metrics/
    ├── rto-tracking.md         # Recovery time objective history
    └── rpo-tracking.md         # Recovery point objective history
```

**Quarterly DR testing**:

- Simulate primary region failure during maintenance window.
- Measure actual RTO and RPO against targets.
- Document gaps and update runbooks.
- Report results to CTO and CIO.

### 6. Cost Optimization

**Multi-region cost factors**:
| Component | Single Region | Multi-Region (Active-Active) | Multi-Region (Active-Passive) |
|-----------|--------------|------------------------------|-------------------------------|
| Compute | 1x | 2-3x | 1.5x (warm standby) |
| Database | 1x | 1.5x (replicas) | 1.3x (replica) |
| Network egress | Baseline | +20-40% (cross-region) | +10-20% |
| Load balancer | Baseline | +50% (multiple backends) | +25% |

**Cost reduction strategies**:

- Use committed use discounts for baseline capacity in all active regions.
- Scale passive region to minimum viable capacity — auto-scale on failover.
- Use Cloud CDN aggressively to reduce cross-region traffic.
- Schedule non-production multi-region testing windows (not 24/7).

### 7. Monitoring and Alerting

**Multi-region dashboards**:

- Per-region health: CPU, memory, request latency, error rate.
- Cross-region replication lag: monitor slave SQL thread delay.
- Load balancer traffic distribution: requests per region over time.
- Cost per region: monthly spend breakdown by region and service.

**Critical alerts**:

- Region health check failure (immediate page).
- Replication lag exceeds RPO threshold (page if >5 minutes).
- Cross-region network latency spike (alert if p99 >200ms).
- Cost anomaly detection (alert if daily spend exceeds baseline by >20%).

## Reference Materials

- Google Cloud multi-region architecture guide
- Cloud SQL cross-region replication documentation
- Cloud Spanner instance configuration guide
- Cloud Load Balancing traffic management
- Company disaster recovery runbook template
- Company cloud infrastructure skill
