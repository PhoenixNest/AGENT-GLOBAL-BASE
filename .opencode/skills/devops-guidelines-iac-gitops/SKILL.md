---
name: devops-guidelines-iac-gitops
description: 'Devops skill: Iac Gitops'
---

# IaC & GitOps

## Overview

This skill covers Infrastructure as Code (IaC) using GitOps workflows, including Terraform module architecture, Terragrunt for DRY configurations, Atlantis for automated plan/apply pipelines, state management with locking, and pull request-based infrastructure change governance. It is used by DevOps engineers during Stage 5 (Development) for infrastructure provisioning and Stage 8 (Integrity Verification) for infrastructure conformance.

## Terraform Architecture

**Module design principles**:

- Reusable modules with input validation, output documentation, and version constraints.
- Environment-specific configurations via Terragrunt `terragrunt.hcl` inheritance.
- Remote state sharing between modules using `terraform_remote_state` data sources.

**Best practices**:

```hcl
# Version pinning
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "prod/networking/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-table"
    encrypt        = true
  }
}
```

## Terragrunt DRY Patterns

**Directory structure**:

```
infrastructure/
├── live/
│   ├── prod/
│   │   ├── terragrunt.hcl      # Environment-level config
│   │   ├── networking/
│   │   │   └── terragrunt.hcl  # Module instance config
│   │   └── compute/
│   │       └── terragrunt.hcl
│   └── staging/
│       └── ...
└── modules/
    ├── networking/
    │   └── main.tf
    └── compute/
        └── main.tf
```

**Terragrunt inheritance**:

```hcl
# live/prod/terragrunt.hcl
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = "prod-terraform-state"
    region = "us-east-1"
  }
}

# live/prod/networking/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "${get_terragrunt_dir()}/../../modules//networking"
}

inputs = {
  vpc_cidr = "10.0.0.0/16"
  environment = "prod"
}
```

## Atlantis Workflow

**Atlantics server configuration**:

- Webhook receiver for GitHub/GitLab PR events.
- Automatic `terraform plan` on PR creation/update.
- Manual `atlantis apply` comment for controlled apply.
- State locking via DynamoDB during plan/apply.

**PR-based change governance**:

1. Developer creates branch with IaC changes.
2. PR triggers Atlantis → runs `terraform plan`.
3. Plan output posted as PR comment.
4. Peer review + approval required.
5. `atlantis apply` comment triggers apply.
6. 100% audit trail: every change linked to PR, plan, and approval.

## State Management

**Locking strategy**:

- DynamoDB table for state locking (prevents concurrent modifications).
- S3 bucket with versioning enabled (enables rollback to previous state).
- State file encryption at rest (S3 server-side encryption).

**State separation**:

- One state file per module per environment.
- No shared state files across environments.
- Remote state references for cross-module dependencies.

## Security Controls

- No secrets in Terraform variables — use AWS Secrets Manager references.
- IAM policies for state access (least-privilege per environment).
- Sentinel/OPA policies for IaC compliance (e.g., no public S3 buckets, no unencrypted RDS).
- Pre-commit hooks: `terraform fmt`, `terraform validate`, `checkov`, `tfsec`.
