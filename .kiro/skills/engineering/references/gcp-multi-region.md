---
name: gcp-multi-region
description: Design and operate multi-region deployments on Google Cloud Platform — Cloud Run services, Cloud SQL with cross-region replication, global load balancing, and failover automation — for disaster recovery and latency reduction across APAC and EU markets.
version: "1.0.0"
---

# GCP Multi Region

| Competency             | Description                                                           | Quality Criteria                                                                                                            |
| ---------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Cloud Run Multi-Region | Deploy Cloud Run services to multiple regions behind Global LB        | Services deployed to ≥ 2 regions; Global HTTP(S) Load Balancer routes to nearest region; health check configured per region |
| Cloud SQL HA           | Configure Cloud SQL High Availability with cross-region read replicas | Primary in primary region with HA failover; read replica in secondary region; failover tested quarterly                     |
| Global Load Balancing  | Configure GCP Global HTTP(S) Load Balancer with SSL and health checks | SSL certificate managed via Google-managed cert; backend health checks tuned to service startup time; anycast IPs used      |
| Disaster Recovery      | Implement and test DR runbooks for region failover                    | RTO ≤ 30 minutes; RPO ≤ 5 minutes for database; DR runbook tested bi-annually; failover automated with Cloud Monitoring     |

## Execution Guidance

### Multi-Region Architecture

```
Global LB (anycast IP)
    ├── us-central1: Cloud Run service + Cloud SQL primary
    └── asia-southeast1: Cloud Run service + Cloud SQL read replica

Failover scenario:
  us-central1 unhealthy → Global LB routes all traffic to asia-southeast1
  Cloud SQL failover: promote replica to primary (< 60s automated)
```

### Terraform Multi-Region Pattern

```hcl
locals {
  regions = ["us-central1", "asia-southeast1"]
}

resource "google_cloud_run_service" "app" {
  for_each = toset(local.regions)
  name     = "app-${each.key}"
  location = each.key
  # ...
}

resource "google_compute_backend_service" "app" {
  dynamic "backend" {
    for_each = toset(local.regions)
    content {
      group = google_compute_region_network_endpoint_group.app[backend.key].id
    }
  }
}
```

### Disaster Recovery Test Schedule

| Test Type         | Frequency   | Success Criteria                          |
| ----------------- | ----------- | ----------------------------------------- |
| Failover drill    | Quarterly   | Traffic rerouted within RTO; no data loss |
| DR runbook review | Bi-annually | All steps current; contacts updated       |
| Backup restore    | Monthly     | Restore from backup verified in < 1 hour  |
