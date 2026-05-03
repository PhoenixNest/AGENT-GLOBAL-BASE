---
name: network-security-fundamentals
description: Apply network security fundamentals to AWS VPC design — security group rules, NACLs, VPC Flow Log analysis, and private subnet architecture — ensuring backend services are not directly reachable from the internet and all traffic flows are audited.
version: "1.0.0"
---

# Network Security Fundamentals

| Competency      | Description                                                         | Quality Criteria                                                                                                                    |
| --------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| VPC Design      | Design VPC with public/private subnet segregation                   | All application and database services in private subnets; only ALB and NAT Gateway in public subnets; no direct internet-facing EC2 |
| Security Groups | Configure least-privilege security group rules                      | No 0.0.0.0/0 ingress rules except on ALB port 443; inter-service rules scoped to source security group ID, not CIDR                 |
| VPC Flow Logs   | Analyze VPC Flow Logs for anomalous traffic patterns                | Flow logs retained ≥ 90 days; CloudWatch Insights queries detect port scanning, unexpected cross-AZ traffic, and rejected flows     |
| Network ACLs    | Implement stateless NACLs as defence-in-depth for subnet boundaries | NACLs deny known-bad source CIDRs at the subnet level; rules reviewed quarterly; stateless rule ordering documented                 |

## Execution Guidance

### VPC Architecture Checklist

- [ ] Public subnets: ALB, NAT Gateway only
- [ ] Private subnets: ECS tasks, RDS, ElastiCache, Lambda (VPC-attached)
- [ ] No resources with public IP assignment except explicitly required
- [ ] VPC endpoints for S3, ECR, CloudWatch (eliminates NAT Gateway cost for AWS service traffic)
- [ ] PrivateLink for cross-account service access

### Security Group Audit

```bash
# Find overly permissive rules
aws ec2 describe-security-groups \
  --filters "Name=ip-permission.cidr,Values=0.0.0.0/0" \
  --query 'SecurityGroups[*].[GroupId,GroupName,IpPermissions]'
```

Any result with port 22 (SSH) or port 3389 (RDP) open to 0.0.0.0/0 is a Critical finding. All SSH access should go through AWS Systems Manager Session Manager — no direct SSH exposure.
