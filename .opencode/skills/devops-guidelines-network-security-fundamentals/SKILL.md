---
name: devops-guidelines-network-security-fundamentals
description: "Devops skill: Network Security Fundamentals"
---

# Network Security Fundamentals

## Overview

This skill covers network security fundamentals for cloud infrastructure, including VPC design, security group configuration, Network ACL management, and traffic inspection. It is used by DevOps engineers during Stage 5 (Development) and Stage 8 (Integrity Verification) for network security conformance.

## VPC Architecture

**VPC design principles**:

- CIDR block planning: /16 for production VPCs, /20 for non-production.
- Subnet strategy: public subnets for load balancers, private subnets for application servers, isolated subnets for databases.
- NAT Gateway in each AZ for outbound internet access from private subnets.
- VPC endpoints (Gateway and Interface) for AWS services — no traffic through internet.

**Reference architecture**:

```
VPC (10.0.0.0/16)
├── Public Subnets (10.0.1.0/24, 10.0.2.0/24)
│   └── Application Load Balancer
├── Private Subnets (10.0.10.0/24, 10.0.20.0/24)
│   └── ECS Tasks / EC2 Instances
└── Isolated Subnets (10.0.100.0/24, 10.0.200.0/24)
    └── RDS, ElastiCache
```

## Security Groups

- Default deny all inbound, allow all outbound.
- Explicit inbound rules: only required ports from specific sources (ALB → App: 443, App → DB: 5432).
- Reference security groups rather than CIDR blocks for inter-service communication.
- No 0.0.0.0/0 inbound rules except for public-facing ALBs (443 only).

## Network ACLs

- Stateless layer — must define both inbound and outbound rules.
- Default NACL: allow all (as safety net).
- Custom NACLs: deny known-bad IP ranges, restrict outbound to required destinations only.
- Rule numbering with gaps (100, 200, 300) to allow insertion of emergency deny rules.

## Traffic Inspection

- VPC Flow Logs on all subnets, delivered to CloudWatch Logs and S3.
- GuardDuty VPC flow log analysis for threat detection.
- Network firewall for deep packet inspection at perimeter.
- WAF on public-facing ALBs and CloudFront distributions.
