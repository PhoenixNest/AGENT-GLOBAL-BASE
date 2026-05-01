---
name: aws-management
description: Manage day-to-day AWS infrastructure operations — including ECS service deployments, RDS maintenance windows, cost optimization reviews, and incident response for infrastructure alerts — ensuring production reliability and cost efficiency.
version: "1.0.0"
---

# AWS Management

| Competency        | Description                                                            | Quality Criteria                                                                                                       |
| ----------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| ECS Operations    | Deploy, scale, and troubleshoot ECS Fargate services                   | Blue/green deployments with rollback; service health checks verified after each deploy; runbook maintained per service |
| RDS Maintenance   | Manage RDS parameter groups, maintenance windows, and failover testing | Maintenance windows scheduled during low-traffic periods; failover tested quarterly; PITR verified annually            |
| Cost Management   | Monitor and optimize AWS spend with Cost Explorer and Trusted Advisor  | Monthly cost review; savings plans reviewed quarterly; unused resources (unattached EBS, idle ELBs) eliminated         |
| Incident Response | Respond to CloudWatch alerts with defined runbooks                     | P1 infrastructure incidents acknowledged in < 5 minutes; runbook exists for every monitored alert; MTTR < 30 minutes   |

## Execution Guidance

### ECS Deployment Runbook

1. Build and tag Docker image: `docker build -t app:$GIT_SHA .`
2. Push to ECR: `docker push $ECR_URI:$GIT_SHA`
3. Update ECS task definition with new image tag
4. Deploy: `aws ecs update-service --cluster prod --service app --force-new-deployment`
5. Monitor: Watch CloudWatch logs + ALB 5xx error rate for 10 minutes
6. Rollback trigger: If 5xx rate > 1% or task launch failure rate > 0 — execute rollback immediately

### Monthly Cost Review Checklist

- [ ] Reserved Instance / Savings Plan utilization > 85%
- [ ] Unattached EBS volumes = 0
- [ ] Idle load balancers (< 100 req/day) reviewed and decommissioned
- [ ] RDS storage auto-scaling thresholds appropriate for growth rate
- [ ] CloudWatch log retention set to ≤ 90 days (no infinite retention)
