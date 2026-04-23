# AWS Security Monitoring & Incident Response

**Category:** Cloud Security — Monitoring & Detection
**Owner:** DevOps Engineer — Leila Khoury

## Overview

Design, implement, and manage comprehensive AWS security monitoring infrastructure covering CloudWatch, GuardDuty, Security Hub, VPC Flow Logs, S3 access logging, CloudTrail, alerting configuration, and incident response integration. This skill ensures continuous visibility into the security posture of all AWS infrastructure supporting mobile applications, with automated detection of threats, anomalous behavior, and compliance violations. The monitoring infrastructure feeds into the company's Security Operations Center (SOC) processes and enables rapid incident response with mean time to detect (MTTD) targets of under 5 minutes for critical threats.

## Competency Dimensions

| Dimension                      | Description                                                             | Proficiency Indicators                                                                                                                                    |
| ------------------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CloudWatch Security Monitoring | Configuring CloudWatch for security event detection and alerting        | Creates custom metrics and alarms for security-relevant events; achieves MTTD <5 minutes for critical threats; integrates with SNS/PagerDuty for alerting |
| GuardDuty Management           | Configuring and tuning Amazon GuardDuty threat detection                | GuardDuty enabled across all accounts and regions; finding false positive rate <10%; automated response to critical findings via EventBridge              |
| Security Hub Orchestration     | Managing AWS Security Hub for centralized security posture management   | Security Hub enabled with all available standards (CIS, PCI DSS, AWS Foundational); findings aggregated and prioritized; compliance score ≥95%            |
| VPC Flow Log Analysis          | Configuring and analyzing VPC Flow Logs for network security monitoring | Flow logs enabled on all VPCs; analysis detects unauthorized network access, data exfiltration patterns, and lateral movement; retention ≥365 days        |
| CloudTrail & Audit Logging     | Ensuring comprehensive API audit logging                                | CloudTrail enabled in all regions with log file validation; management and data events logged; logs shipped to SIEM; integrity verified                   |
| Incident Response Integration  | Connecting monitoring alerts to incident response workflows             | Automated alerting with runbook attachment; mean time to respond (MTTR) <15 minutes for critical alerts; post-incident documentation                      |

## Execution Guidance

### 1. CloudWatch Security Monitoring

**Security-Relevant CloudWatch Alarms:**

```yaml
# cloudwatch-security-alarms.yml
# All alarms trigger SNS notifications to security team

alarms:
  # IAM & Authentication
  - name: UnauthorizedAPICalls
    metric: CloudWatchMetrics/UnauthorizedAPI
    threshold: 5
    period: 300 # 5 minutes
    evaluation_periods: 1
    comparison: GreaterThanThreshold
    actions:
      - sns-topic: arn:aws:sns:us-east-1:123456789012:security-alerts
      - pagerduty-service: security-p1
    runbook: 'https://wiki.company.internal/runbooks/unauthorized-api-calls'

  - name: RootAccountUsage
    metric: CloudWatchMetrics/RootAccountUsage
    threshold: 0
    period: 60
    evaluation_periods: 1
    comparison: GreaterThanThreshold
    actions:
      - sns-topic: arn:aws:sns:us-east-1:123456789012:security-alerts
      - pagerduty-service: security-p1
    runbook: 'https://wiki.company.internal/runbooks/root-account-usage'

  - name: IAMPolicyChange
    metric: CloudWatchMetrics/IAMPolicyChange
    threshold: 1
    period: 60
    evaluation_periods: 1
    comparison: GreaterThanThreshold
    actions:
      - sns-topic: arn:aws:sns:us-east-1:123456789012:security-alerts
    runbook: 'https://wiki.company.internal/runbooks/iam-policy-change'

  # Network Security
  - name: SGChange
    metric: CloudWatchMetrics/SecurityGroupChange
    threshold: 1
    period: 60
    evaluation_periods: 1
    comparison: GreaterThanThreshold
    actions:
      - sns-topic: arn:aws:sns:us-east-1:123456789012:security-alerts
    runbook: 'https://wiki.company.internal/runbooks/security-group-change'

  - name: NACLChange
    metric: CloudWatchMetrics/NACLChange
    threshold: 1
    period: 60
    evaluation_periods: 1
    comparison: GreaterThanThreshold
    actions:
      - sns-topic: arn:aws:sns:us-east-1:123456789012:security-alerts

  # Data Security
  - name: S3BucketPolicyChange
    metric: CloudWatchMetrics/S3BucketPolicyChange
    threshold: 1
    period: 60
    evaluation_periods: 1
    comparison: GreaterThanThreshold
    actions:
      - sns-topic: arn:aws:sns:us-east-1:123456789012:security-alerts
      - pagerduty-service: security-p1
    runbook: 'https://wiki.company.internal/runbooks/s3-bucket-policy-change'

  - name: KMSKeyDeletion
    metric: CloudWatchMetrics/KMSKeyDeletion
    threshold: 1
    period: 60
    evaluation_periods: 1
    comparison: GreaterThanThreshold
    actions:
      - sns-topic: arn:aws:sns:us-east-1:123456789012:security-alerts
      - pagerduty-service: security-p1
    runbook: 'https://wiki.company.internal/runbooks/kms-key-deletion'

  # Compute Security
  - name: EC2PublicIPAssigned
    metric: CloudWatchMetrics/EC2PublicIPAssigned
    threshold: 1
    period: 300
    evaluation_periods: 1
    comparison: GreaterThanThreshold
    actions:
      - sns-topic: arn:aws:sns:us-east-1:123456789012:security-alerts
    runbook: 'https://wiki.company.internal/runbooks/ec2-public-ip'
```

**Terraform — CloudWatch Alarm Configuration:**

```hcl
# monitoring/cloudwatch-security-alarms.tf

# SNS Topic for security alerts
resource "aws_sns_topic" "security_alerts" {
  name = "security-alerts"

  kms_master_key_id = aws_kms_key.sns_key.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudWatchAlarms"
        Effect = "Allow"
        Principal = {
          Service = "cloudwatch.amazonaws.com"
        }
        Action   = "sns:Publish"
        Resource = aws_sns_topic.security_alerts.arn
      }
    ]
  })
}

# Root account usage alarm — CRITICAL
resource "aws_cloudwatch_metric_alarm" "root_account_usage" {
  alarm_name          = "RootAccountUsage"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "RootAccountUsage"
  namespace           = "CloudTrailMetrics"
  period              = "60"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "Root account was used to make API calls"
  treat_missing_data  = "notBreaching"

  alarm_actions = [
    aws_sns_topic.security_alerts.arn,
    "arn:aws:sns:us-east-1:123456789012:pagerduty-security-p1"
  ]

  tags = {
    Severity = "critical"
    Runbook  = "https://wiki.company.internal/runbooks/root-account-usage"
  }
}

# Unauthorized API calls alarm
resource "aws_cloudwatch_metric_alarm" "unauthorized_api_calls" {
  alarm_name          = "UnauthorizedAPICalls"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "UnauthorizedAPI"
  namespace           = "CloudTrailMetrics"
  period              = "300"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "More than 5 unauthorized API calls in 5 minutes"
  treat_missing_data  = "notBreaching"

  alarm_actions = [
    aws_sns_topic.security_alerts.arn,
    "arn:aws:sns:us-east-1:123456789012:pagerduty-security-p1"
  ]

  tags = {
    Severity = "high"
    Runbook  = "https://wiki.company.internal/runbooks/unauthorized-api-calls"
  }
}

# S3 bucket policy change alarm
resource "aws_cloudwatch_metric_alarm" "s3_bucket_policy_change" {
  alarm_name          = "S3BucketPolicyChange"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "S3BucketPolicyChange"
  namespace           = "CloudTrailMetrics"
  period              = "60"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "S3 bucket policy was modified"
  treat_missing_data  = "notBreaching"

  alarm_actions = [
    aws_sns_topic.security_alerts.arn,
    "arn:aws:sns:us-east-1:123456789012:pagerduty-security-p1"
  ]

  tags = {
    Severity = "critical"
    Runbook  = "https://wiki.company.internal/runbooks/s3-bucket-policy-change"
  }
}
```

**CloudTrail Metric Filters for Custom Metrics:**

```hcl
# CloudTrail → CloudWatch Logs → Metric Filters

# Unauthorized API calls
resource "aws_cloudwatch_log_metric_filter" "unauthorized_api" {
  name           = "UnauthorizedAPI"
  pattern        = "{ ($.errorCode = \"*UnauthorizedAccess\") || ($.errorCode = \"AccessDenied*\") }"
  log_group_name = aws_cloudwatch_log_group.cloudtrail_logs.name

  metric_transformation {
    name          = "UnauthorizedAPI"
    namespace     = "CloudTrailMetrics"
    value         = "1"
    default_value = "0"
  }
}

# Root account usage
resource "aws_cloudwatch_log_metric_filter" "root_account_usage" {
  name           = "RootAccountUsage"
  pattern        = "{ $.userIdentity.type = \"Root\" && $.userIdentity.invokedBy NOT EXISTS && $.eventType != \"AwsServiceEvent\" }"
  log_group_name = aws_cloudwatch_log_group.cloudtrail_logs.name

  metric_transformation {
    name          = "RootAccountUsage"
    namespace     = "CloudTrailMetrics"
    value         = "1"
    default_value = "0"
  }
}

# IAM policy changes
resource "aws_cloudwatch_log_metric_filter" "iam_policy_change" {
  name           = "IAMPolicyChange"
  pattern        = "{ ($.eventName = DeleteGroupPolicy) || ($.eventName = DeleteRolePolicy) || ($.eventName = DeleteUserPolicy) || ($.eventName = PutGroupPolicy) || ($.eventName = PutRolePolicy) || ($.eventName = PutUserPolicy) || ($.eventName = CreatePolicy) || ($.eventName = DeletePolicy) || ($.eventName = CreatePolicyVersion) || ($.eventName = DeletePolicyVersion) || ($.eventName = AttachRolePolicy) || ($.eventName = DetachRolePolicy) || ($.eventName = AttachUserPolicy) || ($.eventName = DetachUserPolicy) || ($.eventName = AttachGroupPolicy) || ($.eventName = DetachGroupPolicy) }"
  log_group_name = aws_cloudwatch_log_group.cloudtrail_logs.name

  metric_transformation {
    name          = "IAMPolicyChange"
    namespace     = "CloudTrailMetrics"
    value         = "1"
    default_value = "0"
  }
}
```

### 2. GuardDuty Configuration & Management

**GuardDuty Multi-Account Setup:**

```hcl
# Enable GuardDuty in all accounts and regions
# Delegated administrator pattern for Organizations

# Master account
resource "aws_guardduty_detector" "master" {
  enable = true

  finding_publishing_frequency = "FIFTEEN_MINUTES"

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          enable = true
        }
      }
    }
  }
}

# Organization-wide GuardDuty
resource "aws_guardduty_organization_admin_account" "this" {
  admin_account_id = var.master_account_id
}

# Auto-enable for new accounts
resource "aws_guardduty_organization_configuration" "this" {
  detector_id = aws_guardduty_detector.master.id
  auto_enable = true

  datasources {
    s3_logs {
      auto_enable = true
    }
    kubernetes {
      audit_logs {
        auto_enable = true
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          auto_enable = true
        }
      }
    }
  }
}
```

**GuardDuty Finding Response — EventBridge Automation:**

```json
{
  "source": ["aws.guardduty"],
  "detail-type": ["GuardDuty Finding"],
  "detail": {
    "severity": [
      {
        "numeric": [">=", 7.0]
      }
    ]
  }
}
```

**Automated Response to Critical GuardDuty Findings:**

```python
# lambda/guardduty-auto-response.py
import json
import boto3
import os

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
    finding = event['detail']
    finding_id = finding['id']
    severity = finding['severity']
    finding_type = finding['type']
    region = finding['region']

    # Critical findings (7.0-10.0) trigger automated response
    if severity >= 7.0:
        affected_resource = finding.get('resource', {})

        # Auto-isolate compromised EC2 instance
        if affected_resource.get('instanceDetails'):
            instance_id = affected_resource['instanceDetails']['instanceId']

            # Remove instance from all security groups (isolate)
            ec2.modify_instance_attribute(
                InstanceId=instance_id,
                Groups=[os.environ['ISOLATION_SECURITY_GROUP']]
            )

            # Create snapshot of EBS volumes for forensics
            for volume in affected_resource['instanceDetails'].get('blockDeviceMapping', []):
                ec2.create_snapshot(
                    VolumeId=volume['ebs']['volumeId'],
                    Description=f"Forensic snapshot for GuardDuty finding {finding_id}",
                    TagSpecifications=[{
                        'ResourceType': 'snapshot',
                        'Tags': [
                            {'Key': 'GuardDutyFinding', 'Value': finding_id},
                            {'Key': 'Purpose', 'Value': 'Forensics'}
                        ]
                    }]
                )

        # Notify security team via PagerDuty
        sns.publish(
            TopicArn=os.environ['PAGERDUTY_SNS_ARN'],
            Subject=f"🚨 GuardDuty CRITICAL: {finding_type}",
            Message=json.dumps({
                'finding_id': finding_id,
                'severity': severity,
                'type': finding_type,
                'region': region,
                'description': finding.get('description', ''),
                'action_taken': 'Instance isolated, EBS snapshots created',
                'console_url': f"https://console.aws.amazon.com/guardduty/home?region={region}#/findings?search=id%3D{finding_id}"
            }, indent=2)
        )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed finding {finding_id}')
    }
```

### 3. Security Hub Orchestration

**Security Hub Configuration:**

```hcl
# Enable Security Hub with all standards
resource "aws_securityhub_account" "this" {}

# Enable CIS AWS Foundations Benchmark
resource "aws_securityhub_standards_subscription" "cis" {
  standards_arn = "arn:aws:securityhub:${var.region}::standards/cis-aws-foundations-benchmark/v/1.2.0"
}

# Enable AWS Foundational Security Best Practices
resource "aws_securityhub_standards_subscription" "aws_foundational" {
  standards_arn = "arn:aws:securityhub:${var.region}::standards/aws-foundational-security-best-practices/v/1.0.0"
}

# Enable PCI DSS v4.0 (if applicable)
resource "aws_securityhub_standards_subscription" "pci_dss" {
  standards_arn = "arn:aws:securityhub:${var.region}::standards/pci-dss/v/4.0.0"
  count         = var.enable_pci_dss ? 1 : 0
}

# Enable NIST SP 800-53 Rev 5
resource "aws_securityhub_standards_subscription" "nist" {
  standards_arn = "arn:aws:securityhub:${var.region}::standards/nist-800-53/v/5.0.0"
  count         = var.enable_nist ? 1 : 0
}

# Cross-region aggregation
resource "aws_securityhub_finding_aggregator" "this" {
  linking_mode = "ALL_REGIONS"
}
```

**Security Hub Compliance Dashboard — Key Metrics:**

| Standard                  | Total Controls | Passed | Failed | Compliance % |
| ------------------------- | -------------- | ------ | ------ | ------------ |
| CIS AWS Foundations 1.2.0 | 46             | 44     | 2      | 95.7%        |
| AWS Foundational BP       | 123            | 118    | 5      | 95.9%        |
| PCI DSS v4.0              | 287            | 280    | 7      | 97.6%        |
| NIST 800-53 Rev 5         | 325            | 315    | 10     | 96.9%        |

**Failed Controls — Remediation Priority:**

| Control    | Standard  | Severity | Description                                | Remediation                | Owner           |
| ---------- | --------- | -------- | ------------------------------------------ | -------------------------- | --------------- |
| CIS 2.1.1  | CIS 1.2.0 | Medium   | CloudTrail log file validation not enabled | Enable log file validation | Leila Khoury    |
| CIS 2.1.2  | CIS 1.2.0 | Medium   | CloudTrail not enabled in all regions      | Enable multi-region trail  | Leila Khoury    |
| FSBP.IAM.4 | AWS FSBP  | Low      | IAM root access key exists                 | Delete root access keys    | Dr. Priya Mehta |

### 4. VPC Flow Logs Analysis

**VPC Flow Log Configuration:**

```hcl
# Enable VPC Flow Logs for all VPCs
resource "aws_flow_log" "this" {
  for_each = var.vpc_ids

  vpc_id       = each.value
  traffic_type = "ALL"  # ACCEPT, REJECT, and ALL

  log_destination      = aws_cloudwatch_log_group.vpc_flow_logs[each.key].arn
  log_destination_type = "cloud-watch-logs"

  iam_role_arn = aws_iam_role.vpc_flow_logs.arn

  # Optional: Also send to S3 for long-term storage
  # log_destination = aws_s3_bucket.vpc_flow_logs.arn
  # log_destination_type = "s3"

  tags = {
    Name    = "vpc-flow-log-${each.key}"
    Purpose = "security-monitoring"
  }
}

# CloudWatch Logs Group for Flow Logs
resource "aws_cloudwatch_log_group" "vpc_flow_logs" {
  for_each = var.vpc_ids

  name              = "/aws/vpc/flow-logs/${each.key}"
  retention_in_days = 365  # Retain for 1 year

  kms_key_id = aws_kms_key.vpc_flow_logs.arn

  tags = {
    Purpose = "security-monitoring"
  }
}

# IAM Role for Flow Logs
resource "aws_iam_role" "vpc_flow_logs" {
  name = "vpc-flow-logs-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "vpc_flow_logs" {
  name = "vpc-flow-logs-policy"
  role = aws_iam_role.vpc_flow_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}
```

**Flow Log Analysis — Security Detection Patterns:**

```sql
-- Athena Query: Detect potential data exfiltration (large outbound transfers)
SELECT
    srcaddr,
    dstaddr,
    SUM(bytes) as total_bytes,
    COUNT(*) as packet_count,
    MIN(start) as first_seen,
    MAX(end) as last_seen
FROM vpc_flow_logs
WHERE action = 'ACCEPT'
    AND srcaddr LIKE '10.%'  -- Internal IP
    AND dstaddr NOT LIKE '10.%'  -- External destination
    AND bytes > 1000000  -- > 1MB
GROUP BY srcaddr, dstaddr
HAVING SUM(bytes) > 100000000  -- > 100MB total
ORDER BY total_bytes DESC
LIMIT 50;

-- Athena Query: Detect port scanning
SELECT
    srcaddr,
    COUNT(DISTINCT dstport) as unique_ports,
    COUNT(DISTINCT dstaddr) as unique_destinations,
    COUNT(*) as total_connections
FROM vpc_flow_logs
WHERE action = 'REJECT'
    AND dstport > 0
GROUP BY srcaddr
HAVING COUNT(DISTINCT dstport) > 20
ORDER BY unique_ports DESC
LIMIT 20;

-- Athena Query: Detect unauthorized SSH access attempts
SELECT
    srcaddr,
    dstaddr,
    COUNT(*) as connection_attempts,
    MIN(start) as first_attempt,
    MAX(end) as last_attempt
FROM vpc_flow_logs
WHERE dstport = 22
    AND action = 'REJECT'
GROUP BY srcaddr, dstaddr
HAVING COUNT(*) > 5
ORDER BY connection_attempts DESC;
```

### 5. CloudTrail Configuration

**Comprehensive CloudTrail Setup:**

```hcl
# Organization-wide CloudTrail
resource "aws_cloudtrail" "org_trail" {
  name                          = "org-security-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_logs.id
  s3_key_prefix                 = "cloudtrail"
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
  kms_key_id                    = aws_kms_key.cloudtrail.arn

  # Event selectors for data events
  event_selector {
    read_write_type           = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::S3::Object"
      values = ["arn:aws:s3:::*"]
    }

    data_resource {
      type   = "AWS::Lambda::Function"
      values = ["arn:aws:lambda:*:*:function:*"]
    }
  }

  insight_selector {
    insight_type = "ApiCallRateInsight"
  }

  insight_selector {
    insight_type = "ApiErrorRateInsight"
  }

  tags = {
    Purpose = "security-audit"
  }
}

# CloudTrail log bucket with maximum security
resource "aws_s3_bucket" "cloudtrail_logs" {
  bucket = "cloudtrail-logs-org-${var.account_id}"

  tags = {
    Purpose     = "security-audit"
    Compliance  = "SOC2,PCI-DSS,ISO27001"
  }
}

resource "aws_s3_bucket_policy" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AWSCloudTrailAclCheck"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.cloudtrail_logs.arn
      },
      {
        Sid    = "AWSCloudTrailWrite"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.cloudtrail_logs.arn}/AWSLogs/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      },
      {
        Sid    = "DenyUnencryptedUploads"
        Effect = "Deny"
        Principal = "*"
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.cloudtrail_logs.arn}/*"
        Condition = {
          StringNotEquals = {
            "s3:x-amz-server-side-encryption" = "aws:kms"
          }
        }
      },
      {
        Sid    = "DenyInsecureTransport"
        Effect = "Deny"
        Principal = "*"
        Action   = "s3:*"
        Resource = aws_s3_bucket.cloudtrail_logs.arn
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}

# Object Lock for CloudTrail logs (compliance)
resource "aws_s3_bucket_object_lock_configuration" "cloudtrail" {
  bucket = aws_s3_bucket.cloudtrail_logs.id

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 365  # 1-year retention for compliance
    }
  }
}
```

### 6. Incident Response Integration

**Alert Routing Matrix:**

| Alert Source     | Severity            | Notification Channel                     | Response SLA      | Runbook                      |
| ---------------- | ------------------- | ---------------------------------------- | ----------------- | ---------------------------- |
| GuardDuty        | Critical (7.0-10.0) | PagerDuty P1 + Slack #security-incidents | 5 minutes         | runbooks/guardduty-critical  |
| GuardDuty        | High (4.0-6.9)      | Slack #security-alerts                   | 30 minutes        | runbooks/guardduty-high      |
| CloudWatch Alarm | Critical            | PagerDuty P1 + Slack #security-incidents | 5 minutes         | runbooks/cloudwatch-critical |
| CloudWatch Alarm | High                | Slack #security-alerts                   | 15 minutes        | runbooks/cloudwatch-high     |
| Security Hub     | Failed Control      | Slack #compliance-alerts                 | Next business day | runbooks/securityhub-failed  |
| VPC Flow Logs    | Anomaly             | Slack #security-alerts                   | 30 minutes        | runbooks/vpc-anomaly         |

**Incident Response Runbook — GuardDuty Critical Finding:**

```markdown
# Runbook: GuardDuty Critical Finding Response

## Trigger

GuardDuty finding with severity ≥ 7.0

## Initial Response (0-5 minutes)

1. [ ] Acknowledge PagerDuty alert
2. [ ] Open GuardDuty console → navigate to finding
3. [ ] Record finding ID, type, severity, and description
4. [ ] Post initial notification to #security-incidents Slack channel

## Triage (5-15 minutes)

5. [ ] Identify affected resource (EC2 instance, IAM user, etc.)
6. [ ] Check if resource is production or non-production
7. [ ] Review recent API activity for affected resource (CloudTrail)
8. [ ] Determine if finding is true positive or false positive

## Containment (15-30 minutes) — True Positive

9. [ ] **EC2 compromise**: Isolate instance (move to quarantine security group)
10. [ ] **IAM compromise**: Disable IAM user/role, rotate credentials
11. [ ] **S3 exposure**: Block public access, review bucket policy
12. [ ] Create EBS snapshot for forensics (if EC2)
13. [ ] Preserve CloudTrail logs for investigation

## Investigation (30 minutes - 2 hours)

14. [ ] Determine attack vector and timeline
15. [ ] Identify all affected resources
16. [ ] Check for lateral movement
17. [ ] Determine data exposure (if any)

## Eradication & Recovery (2-4 hours)

18. [ ] Remove attacker access (delete unauthorized resources, keys)
19. [ ] Patch vulnerability that enabled compromise
20. [ ] Restore affected services from clean state
21. [ ] Verify eradication (re-scan with GuardDuty)

## Post-Incident (24-48 hours)

22. [ ] Write incident report
23. [ ] Conduct blameless post-mortem
24. [ ] Update runbook with lessons learned
25. [ ] Implement preventive controls
26. [ ] Update risk register
```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Stage 3** (Architecture)           | Infrastructure monitoring architecture designed; CloudWatch, GuardDuty, Security Hub, and CloudTrail integration specified |
| **Stage 5** (Development)            | Monitoring infrastructure provisioned via Terraform; all logging and alerting configured and tested                        |
| **Stage 6** (Code Review)            | Monitoring configuration reviewed; alert thresholds validated; runbooks verified                                           |
| **Stage 8** (Integrity Verification) | Monitoring systems verified operational; test alerts confirm end-to-end alerting pipeline                                  |
| **Stage 10** (Release Readiness)     | Monitoring coverage confirmed for all production infrastructure; incident response runbooks validated                      |

## Quality Standards

| Metric                      | Standard                                                                                           |
| --------------------------- | -------------------------------------------------------------------------------------------------- |
| **GuardDuty Coverage**      | GuardDuty enabled in 100% of AWS accounts and regions; all datasources (S3, EKS, EBS) enabled      |
| **CloudTrail Coverage**     | Multi-region trail with management and data events; log file validation enabled; 365-day retention |
| **VPC Flow Logs**           | Flow logs enabled on 100% of VPCs; ALL traffic type; 365-day retention                             |
| **Security Hub Compliance** | Security Hub enabled with CIS, AWS FSBP, and PCI DSS standards; compliance score ≥95%              |
| **MTTD (Critical)**         | Mean time to detect critical threats <5 minutes                                                    |
| **MTTR (Critical)**         | Mean time to respond to critical alerts <15 minutes                                                |
| **Alert Accuracy**          | <10% false positive rate on security alerts                                                        |
| **Runbook Coverage**        | 100% of alert types have documented runbooks; runbooks tested quarterly                            |
| **S3 Access Logging**       | 100% of S3 buckets have access logging enabled; logs retained for 365 days                         |
