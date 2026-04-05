# Infrastructure as Code (IaC) Security

**Category:** DevOps — Infrastructure Architecture & Policy
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

Design, implement, and maintain secure Infrastructure as Code (IaC) using Terraform, implementing module architecture best practices, state management security, drift detection, policy-as-code with OPA/Sentinel, and GitOps workflows. This skill ensures that all cloud infrastructure supporting mobile applications (API backends, databases, CI/CD runners, monitoring systems) is defined, versioned, reviewed, and deployed through a secure, auditable infrastructure pipeline. Infrastructure security is foundational — no amount of application-level security can compensate for misconfigured cloud infrastructure.

## Competency Dimensions

| Dimension | Description | Proficiency Indicators |
|-----------|-------------|----------------------|
| Terraform Module Architecture | Designing reusable, composable, secure Terraform modules | Creates modules with input validation, output documentation, version pinning, and security defaults; modules used across 3+ projects without modification |
| State Management | Secure handling of Terraform state files containing sensitive data | State stored in encrypted remote backend with access controls; state file never committed to repository; state locking prevents concurrent modifications |
| Drift Detection | Identifying and remediating configuration drift between IaC and live infrastructure | Automated drift detection runs daily; drift alerts within 1 hour; 100% of drift incidents investigated and remediated within 24 hours |
| Policy-as-Code (OPA/Sentinel) | Enforcing infrastructure security policies through automated checks | Writes Sentinel/OPA policies that prevent 100% of common misconfigurations (open S3, unencrypted RDS, public-facing databases); policies tested against known-bad configurations |
| GitOps Workflows | Managing infrastructure changes through Git-based approval workflows | All infrastructure changes via PR; requires 2+ approvals; automated plan preview in PR comments; zero manual infrastructure changes |
| IaC Security Scanning | Automated security analysis of Terraform configurations | Integrates tfsec/checkov into CI pipeline; blocks deployment of non-compliant infrastructure; maintains custom rules for company-specific security requirements |

## Execution Guidance

### 1. Terraform Module Architecture

**Module Design Principles:**
1. **Single Responsibility**: Each module manages one logical infrastructure component
2. **Security Defaults**: Secure configuration is the default; insecurity requires explicit override
3. **Input Validation**: Validate all inputs with `validation` blocks
4. **Version Pinning**: All module versions pinned; no `latest` references
5. **Documentation**: Every module has README with inputs, outputs, examples, and security considerations

**Module Directory Structure:**

```
terraform-modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
├── ecs-service/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
├── rds-instance/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
├── s3-bucket/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── README.md
└── github-oidc-role/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── versions.tf
    └── README.md
```

**Example: Secure S3 Bucket Module:**

```hcl
# terraform-modules/s3-bucket/main.tf

# Security-first S3 bucket module
# All security controls are enabled by default

resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  tags = merge(var.tags, {
    ManagedBy   = "terraform"
    SecurityTier = var.security_tier
  })
}

# Block all public access by default
resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = var.sse_algorithm  # Default: aws:kms
      kms_master_key_id = var.kms_key_id
    }
    bucket_key_enabled = true
  }
}

# Enable versioning for data recovery
resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable access logging
resource "aws_s3_bucket_logging" "this" {
  bucket        = aws_s3_bucket.this.id
  target_bucket = var.logging_bucket
  target_prefix = "${var.bucket_name}/"
}

# Enable lifecycle policies for cost management
resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  dynamic "rule" {
    for_each = var.lifecycle_rules
    content {
      id     = rule.value.id
      status = rule.value.status

      expiration {
        days = rule.value.expiration_days
      }

      transition {
        days          = rule.value.transition_days
        storage_class = rule.value.transition_storage_class
      }
    }
  }
}

# Enable object lock for compliance (optional)
resource "aws_s3_bucket_object_lock_configuration" "this" {
  count = var.enable_object_lock ? 1 : 0
  bucket = aws_s3_bucket.this.id

  rule {
    default_retention {
      mode  = var.object_lock_mode
      days  = var.object_lock_days
    }
  }
}

# Bucket policy — enforce TLS in transit
resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.this.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceTLS"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.this.arn,
          "${aws_s3_bucket.this.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}
```

**Module Variables with Validation:**

```hcl
# terraform-modules/s3-bucket/variables.tf

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{2,62}$", var.bucket_name))
    error_message = "Bucket name must be lowercase alphanumeric with dots and hyphens, 3-63 characters."
  }
}

variable "security_tier" {
  description = "Security classification of data stored in this bucket"
  type        = string
  default     = "confidential"

  validation {
    condition     = contains(["public", "internal", "confidential", "restricted"], var.security_tier)
    error_message = "Security tier must be one of: public, internal, confidential, restricted."
  }
}

variable "enable_object_lock" {
  description = "Enable S3 Object Lock for compliance (immutability)"
  type        = bool
  default     = false
}

variable "lifecycle_rules" {
  description = "Lifecycle rules for the bucket"
  type = list(object({
    id                        = string
    status                    = string
    expiration_days           = number
    transition_days           = number
    transition_storage_class  = string
  }))
  default = []
}

variable "sse_algorithm" {
  description = "Server-side encryption algorithm"
  type        = string
  default     = "aws:kms"

  validation {
    condition     = contains(["aws:kms", "aws:kms:dsse"], var.sse_algorithm)
    error_message = "Only KMS-based encryption is allowed. AES256 is not permitted for company data."
  }
}

variable "kms_key_id" {
  description = "KMS key ID for server-side encryption"
  type        = string
}

variable "logging_bucket" {
  description = "Target bucket for access logging"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

### 2. State Management Security

**Remote Backend Configuration:**

```hcl
# backend.tf — Remote state with encryption and access controls

terraform {
  backend "s3" {
    bucket         = "terraform-state-prod-us-east-1"
    key            = "mobile-app-backend/production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "alias/terraform-state-key"
    dynamodb_table = "terraform-state-lock"
    acl            = "private"

    # Prevent accidental state deletion
    # Note: These are provider-level settings, not backend settings
  }
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  # Enable point-in-time recovery
  point_in_time_recovery {
    enabled = true
  }

  # Enable server-side encryption
  server_side_encryption {
    enabled = true
  }

  tags = {
    ManagedBy = "terraform"
    Purpose   = "Terraform state locking"
  }
}

# State bucket with maximum security
module "state_bucket" {
  source = "../terraform-modules/s3-bucket"

  bucket_name        = "terraform-state-prod-us-east-1"
  security_tier      = "restricted"
  enable_object_lock = true
  object_lock_mode   = "GOVERNANCE"
  object_lock_days   = 365
  sse_algorithm      = "aws:kms"
  kms_key_id         = aws_kms_key.state_key.id
  logging_bucket     = module.logging_bucket.id
  lifecycle_rules = [{
    id                      = "old-versions"
    status                  = "Enabled"
    expiration_days         = 365
    transition_days         = 90
    transition_storage_class = "GLACIER"
  }]
}

# KMS key for state encryption with strict access
resource "aws_kms_key" "state_key" {
  description             = "KMS key for Terraform state encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow CI/CD Pipeline Access"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/github-actions-deploy"
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })
}
```

**State File Security Rules:**
1. State files **never** stored locally on developer machines in production
2. State access restricted to CI/CD pipeline role only (no human access)
3. State bucket has Object Lock enabled (prevents deletion/modification for retention period)
4. State encryption uses dedicated KMS key with strict IAM policy
5. State file changes logged via CloudTrail (S3 data events)
6. Weekly state file integrity verification (compare hash with known-good hash)

### 3. Drift Detection

**Automated Drift Detection Pipeline:**

```yaml
# .github/workflows/terraform-drift-detection.yml
name: Infrastructure — Drift Detection
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-drift-detection
          aws-region: us-east-1

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        id: plan
        run: |
          terraform plan -no-color -detailed-exitcode -out=tfplan
        continue-on-error: true

      - name: Check for Drift
        run: |
          EXIT_CODE=$?
          if [ $EXIT_CODE -eq 2 ]; then
            echo "🚨 DRIFT DETECTED — infrastructure does not match Terraform configuration"
            terraform show -no-color tfplan > drift-report.txt
            echo "=== DRIFT REPORT ===" >> $GITHUB_STEP_SUMMARY
            cat drift-report.txt >> $GITHUB_STEP_SUMMARY

            # Post to Slack
            curl -X POST -H 'Content-type: application/json' \
              --data "{\"text\": \"🚨 Infrastructure drift detected in production. See: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}\"}" \
              ${{ secrets.SLACK_WEBHOOK_URL }}

            # Create GitHub issue
            gh issue create \
              --title "🚨 Infrastructure Drift Detected — $(date +%Y-%m-%d)" \
              --body "$(cat drift-report.txt)" \
              --label "infrastructure,drift,urgent"
          else
            echo "✅ No drift detected — infrastructure matches Terraform configuration"
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Drift Response Procedure:**

```
Drift Detected (automated alert)
    │
    ▼
Yuki Matsuda investigates drift cause
    ├── Intentional change (manual fix for emergency)?
    │   └── Update Terraform configuration to match desired state
    ├── Unauthorized change?
    │   └── Investigate who/what made the change via CloudTrail
    │       └── If malicious: initiate incident response
    │       └── If accidental: revert via terraform apply
    └── Terraform configuration bug?
        └── Fix configuration and apply
    │
    ▼
Apply Terraform to restore desired state
    │
    ▼
Document drift incident
    ├── Root cause
    ├── Remediation steps
    ├── Preventive measures
    └── Update drift detection rules if needed
    │
    ▼
Close drift incident
```

### 4. Policy-as-Code — OPA/Sentinel

**Sentinel Policies — HashiCorp Terraform Cloud/Enterprise:**

```sentinel
# policies/sentinel/enforce-encryption.sentinel
# Require encryption for all S3 buckets, RDS instances, and EBS volumes

import "tfplan/v2" as tfplan

# S3 buckets must have server-side encryption
s3_encryption = rule {
  all tfplan.resource.changes as _, resources {
    all resources as _, r {
      r.type is "aws_s3_bucket_server_side_encryption_configuration" or
      r.type is not "aws_s3_bucket" or
      r.change.actions contains "delete"
    }
  }
}

# RDS instances must have storage_encrypted = true
rds_encryption = rule {
  all tfplan.resource.changes as _, resources {
    all resources as _, r {
      r.type is not "aws_db_instance" or
      r.change.actions contains "delete" or
      r.change.after.storage_encrypted is true
    }
  }
}

# EBS volumes must be encrypted
ebs_encryption = rule {
  all tfplan.resource.changes as _, resources {
    all resources as _, r {
      r.type is not "aws_ebs_volume" or
      r.change.actions contains "delete" or
      r.change.after.encrypted is true
    }
  }
}

# Security groups must not allow inbound 0.0.0.0/0 on sensitive ports
no_open_sensitive_ports = rule {
  all tfplan.resource.changes as _, resources {
    all resources as _, r {
      r.type is not "aws_security_group" or
      r.change.actions contains "delete" or
      all r.change.after.ingress as _, ingress {
        ingress.cidr_blocks is null or
        all ingress.cidr_blocks as _, cidr {
          cidr is not "0.0.0.0/0"
        } or
        all ingress.from_port as _, port {
          port is not 22 and port is not 3306 and port is not 5432 and port is not 6379
        }
      }
    }
  }
}

# Main policy
main = rule {
  s3_encryption and
  rds_encryption and
  ebs_encryption and
  no_open_sensitive_ports
}
```

**OPA Policies — Check with Conftest:**

```rego
# policy/opa/terraform.rego
package terraform

import rego.v1

# Deny S3 buckets without versioning
deny_contains msg if {
    some resource in input.resource.changes
    resource.type == "aws_s3_bucket_versioning"
    resource.change.after.versioning_configuration.status != "Enabled"
    msg := "S3 bucket versioning must be enabled"
}

# Deny security groups with unrestricted SSH
deny_contains msg if {
    some resource in input.resource.changes
    resource.type == "aws_security_group"
    some ingress in resource.change.after.ingress
    ingress.from_port == 22
    "0.0.0.0/0" in ingress.cidr_blocks
    msg := "Security group allows SSH from 0.0.0.0/0"
}

# Deny RDS instances without multi-AZ (production only)
deny_contains msg if {
    some resource in input.resource.changes
    resource.type == "aws_db_instance"
    resource.change.after.multi_az == false
    resource.change.after.tags.Environment == "production"
    msg := "Production RDS instances must be multi-AZ"
}

# Deny Lambda functions without VPC configuration
deny_contains msg if {
    some resource in input.resource.changes
    resource.type == "aws_lambda_function"
    resource.change.after.vpc_config == {}
    msg := "Lambda functions must be deployed within a VPC"
}

# Require tags on all resources
deny_contains msg if {
    some resource in input.resource.changes
    resource.change.actions == ["create"]
    not resource.change.after.tags
    msg := sprintf("Resource %s must have tags", [resource.address])
}
```

**CI/CD Policy Enforcement:**

```yaml
# .github/workflows/terraform-policy-check.yml
name: Infrastructure — Policy Check
on:
  pull_request:
    paths: ['terraform/**']

jobs:
  tfsec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run tfsec
        uses: aquasecurity/tfsec-action@v1.0.3
        with:
          working_directory: terraform/
          soft_fail: false
          format: sarif

  conftest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Conftest (OPA)
        run: |
          terraform init
          terraform plan -out=tfplan
          terraform show -json tfplan > tfplan.json
          conftest test tfplan.json \
            --policy policy/opa/ \
            --namespace terraform \
            --all-namespaces

  sentinel:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Run Sentinel Policies
        run: |
          # Sentinel requires Terraform Cloud/Enterprise
          # For GitHub Actions, use conftest as primary policy engine
          echo "Sentinel policies run in Terraform Cloud"
```

### 5. GitOps Workflows

**Infrastructure Change Workflow:**

```
Developer identifies infrastructure change need
    │
    ▼
Create feature branch from main
    │
    ▼
Make Terraform changes (new resources, configuration updates)
    │
    ▼
Run terraform fmt + terraform validate locally
    │
    ▼
Commit changes and open PR
    │
    ▼
Automated CI Pipeline:
    ├── terraform fmt -check
    ├── terraform validate
    ├── tfsec (security scan)
    ├── conftest (policy check)
    ├── terraform plan (posted as PR comment)
    └── All checks must pass
    │
    ▼
Peer Review (2+ approvals required)
    ├── Infrastructure team member review
    ├── Security team review (for security-impacting changes)
    └── CSO review (for production environment changes)
    │
    ▼
Merge to main
    │
    ▼
Automated Deployment:
    ├── terraform plan (final)
    ├── Manual approval gate (production only)
    └── terraform apply
    │
    ▼
Post-deployment verification
    ├── terraform plan (should show no changes)
    └── Drift detection confirms applied state
```

**PR Template for Infrastructure Changes:**

```markdown
## Infrastructure Change Request

### Description
[What is changing and why?]

### Affected Resources
- [ ] VPC/Networking
- [ ] Compute (EC2/ECS/Lambda)
- [ ] Database (RDS/DynamoDB)
- [ ] Storage (S3/EFS)
- [ ] IAM/Roles/Policies
- [ ] CI/CD Pipeline
- [ ] Monitoring/Logging
- [ ] Other: [specify]

### Environment
- [ ] Development
- [ ] Staging
- [ ] Production

### Security Impact
- [ ] New IAM permissions
- [ ] Network changes (security groups, NACLs)
- [ ] Encryption changes
- [ ] Public exposure changes
- [ ] Secrets/credentials changes
- [ ] No security impact

### Terraform Plan Summary
```
# Paste terraform plan output here (resources to add/change/destroy)
```

### Rollback Plan
[How to revert this change if needed?]

### Testing
- [ ] terraform fmt -check passes
- [ ] terraform validate passes
- [ ] tfsec scan passes
- [ ] conftest policy check passes
- [ ] Manual review of plan output
```

## Pipeline Integration

| Pipeline Stage | Application |
|----------------|-------------|
| **Stage 3** (Architecture) | Infrastructure architecture designed; Terraform module structure defined; security requirements for infrastructure documented |
| **Stage 4** (Implementation Plan) | IaC implementation plan includes module development, policy-as-code creation, and GitOps workflow setup |
| **Stage 5** (Development) | Infrastructure provisioned via Terraform; drift detection active; policy checks enforced on all changes |
| **Stage 6** (Code Review) | Terraform configuration reviewed for security; policy check results included in review |
| **Stage 10** (Release Readiness) | Infrastructure security posture confirmed; drift detection current; all policy checks passing |

## Quality Standards

| Metric | Standard |
|--------|----------|
| **IaC Coverage** | 100% of infrastructure defined in Terraform; no manual infrastructure changes |
| **Policy Enforcement** | 100% of Terraform changes pass policy checks before merge |
| **State Security** | Zero state file exposure incidents; state access limited to CI/CD pipeline role |
| **Drift Detection** | Drift detected within 6 hours; 100% of drift incidents investigated within 24 hours |
| **Module Quality** | All modules pass tfsec with zero critical/high findings; all modules documented |
| **GitOps Compliance** | 100% of infrastructure changes via Git PR workflow; zero manual `terraform apply` |
| **Encryption** | 100% of storage resources encrypted at rest; 100% of network traffic encrypted in transit |
| **Access Control** | All infrastructure access via IAM roles; no long-lived access keys |
