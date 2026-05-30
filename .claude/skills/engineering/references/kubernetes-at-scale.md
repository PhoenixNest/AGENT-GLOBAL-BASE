---
name: kubernetes-at-scale
description: Operate and scale Kubernetes clusters for production workloads — covering Horizontal Pod Autoscaler tuning, resource quotas, namespace isolation, and cluster upgrade strategies — as a migration target when ECS/Fargate reaches operational limits.
version: "1.0.0"
---

# Kubernetes At Scale

| Competency          | Description                                                   | Quality Criteria                                                                                                      |
| ------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| HPA Tuning          | Configure Horizontal Pod Autoscaler with custom metrics       | HPA targets 60–70% CPU/memory utilization; scale-up triggers before saturation; scale-down has stabilization window   |
| Resource Management | Set requests/limits and namespace resource quotas             | Every pod has CPU and memory requests+limits set; namespace quotas prevent resource starvation between teams          |
| Cluster Upgrades    | Execute Kubernetes version upgrades with zero downtime        | Uses managed node group rolling update; tests on staging cluster first; upgrade window communicated 1 week in advance |
| Network Policies    | Implement Kubernetes network policies for namespace isolation | Default-deny policy applied to all namespaces; explicit allow rules for service-to-service communication              |

## Execution Guidance

### Resource Right-Sizing

```bash
# Analyze actual resource usage vs. requests
kubectl top pods --all-namespaces --sort-by=cpu
kubectl resource-capacity --pods --util

# VPA recommendation (Vertical Pod Autoscaler in recommendation mode)
kubectl get vpa --all-namespaces
```

Set `requests` to the p75 actual usage and `limits` to p95 + 20% buffer. Never set `limits` CPU to the same value as `requests` — this causes CPU throttling even at normal load.

### Cluster Upgrade Playbook

1. Upgrade staging cluster → validate for 48 hours
2. Communicate upgrade window to all teams (1 week notice)
3. Drain and cordon one node group at a time
4. Upgrade control plane first, then node groups (sequential, never parallel)
5. Post-upgrade: verify all Deployments, StatefulSets, and DaemonSets are healthy
