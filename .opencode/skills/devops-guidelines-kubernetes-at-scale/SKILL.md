---
name: devops-guidelines-kubernetes-at-scale
description: Kubernetes at scale for mobile backend services — cluster autoscaling, horizontal pod autoscaling, service mesh (Istio/Linkerd), multi-cluster federation, and GitOps-driven deployments for mobile API infrastructure handling 10K+ RPS. Owned by Thomas Zhang (DevOps Lead). Use during Stage 3 (UML Engineering) for backend architecture design and Stage 5 (Development) for Kubernetes cluster provisioning. Trigger: Kubernetes at scale, cluster autoscaling, HPA, service mesh, Istio, Linkerd, multi-cluster, mobile API scaling, high throughput backend.
prerequisites:
  - devops-guidelines-cloud-infrastructure

version: "1.0.0"
---

# Kubernetes at Scale

## Overview

This skill covers Kubernetes cluster management at scale, operator patterns, cluster autoscaling, and multi-cluster governance. It is used by DevOps engineers during Stage 5 (Development) for container orchestration and Stage 8 (Integrity Verification) for infrastructure conformance.

## Cluster Architecture at Scale

**Multi-cluster topology**:

| Cluster  | Purpose                           | Node Count | Scaling                 |
| -------- | --------------------------------- | ---------- | ----------------------- |
| Platform | Ingress, service mesh, monitoring | 10-30      | Static                  |
| Workload | Application microservices         | 20-200     | Cluster autoscaler      |
| CI/CD    | Build runners, test environments  | 5-50       | Dynamic (scale to zero) |

**Node group strategy**:

- General purpose: stateless application pods.
- Memory optimized: in-memory caches, data processing.
- GPU enabled: ML inference, video processing.
- Spot node group: fault-tolerant workloads (batch jobs, CI runners).

## Operator Patterns

**Common operators**:

| Operator           | Purpose                   | Configuration                           |
| ------------------ | ------------------------- | --------------------------------------- |
| cert-manager       | TLS certificate lifecycle | ClusterIssuer (Let's Encrypt)           |
| external-secrets   | Secret synchronization    | SecretStore → AWS SM / Vault            |
| metrics-server     | HPA metrics               | Deployed by default on EKS              |
| cluster-autoscaler | Node scaling              | ASG integration, scale-up/down policies |

## Cluster Autoscaling

**HPA configuration**:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 3
  maxReplicas: 50
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Security Hardening

- Pod Security Standards: `restricted` profile for all namespaces.
- Network Policies: deny-all default, explicit allow for required communication paths.
- RBAC: least-privilege service accounts, no default SA with cluster-admin.
- Image admission: only images from approved registries with signed attestations.
- Runtime security: Falco for anomaly detection, automatic alerting on policy violations.
