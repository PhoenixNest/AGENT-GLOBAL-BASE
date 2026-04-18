---
name: monitoring-audit
description: Infrastructure monitoring, cost optimization, and centralized audit logging for cloud platforms, covering CloudWatch, Datadog integration, and CloudTrail-based audit pipelines.
---

# Monitoring & Audit

## Overview

This skill covers infrastructure monitoring, cost optimization, and centralized audit logging for cloud platforms. It includes CloudWatch and Datadog integration, anomaly detection, cost anomaly alerting, capacity forecasting, and CloudTrail-based audit logging with Athena querying. It is used by DevOps engineers during Stage 5 (Development) and Stage 8 (Integrity Verification).

## Infrastructure Monitoring Stack

**CloudWatch + Datadog integration**:

- CloudWatch for AWS-native metrics (EC2, RDS, ELB, Lambda, ECS).
- Datadog for application-level metrics, APM tracing, and custom dashboards.
- Custom CloudWatch metrics for business KPIs not covered by default metrics.
- Unified alerting: CloudWatch Alarms → SNS → Datadog → PagerDuty.

**Key metric categories**:

| Category    | Metrics                                          | Alert Threshold          |
| ----------- | ------------------------------------------------ | ------------------------ |
| Compute     | CPU utilization, memory pressure, disk I/O       | >80% for 5 min           |
| Database    | Connections, read/write latency, replication lag | >1s latency, >10s lag    |
| Network     | Bandwidth, error rate, connection count          | >1% error rate           |
| Application | Response time, error rate, throughput            | P99 >500ms, >0.1% errors |

## Cost Anomaly Detection

- AWS Cost Anomaly Detection with daily monitoring and alerting.
- Right-sizing recommendations based on 30-day utilization data.
- Reserved Instance coverage target: >70% of eligible compute.
- Automated resource scheduling: non-production environments shut down outside business hours.

## Centralized Audit Logging

**CloudTrail + S3 + Athena pipeline**:

```
CloudTrail (all accounts) → S3 (centralized bucket) → Athena (ad-hoc queries)
                                              → EventBridge (real-time alerts)
                                              → GuardDuty (threat detection)
```

**Audit query patterns**:

- IAM changes in last 24 hours.
- Console sign-in failures.
- S3 bucket policy changes.

## Capacity Planning

- Automated capacity forecasting using CloudWatch metric math and linear prediction.
- Auto-scaling policies with target tracking (CPU target 60%, memory target 75%).
- Quarterly capacity review: compare forecasted growth against current reservation commitments.
