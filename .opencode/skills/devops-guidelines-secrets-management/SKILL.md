---
name: devops-guidelines-secrets-management
description: "Devops skill: Secrets Management"
---

# Secrets Management

**Category:** DevOps Security — Credential Management
**Owner:** DevOps Engineer — Leila Khoury

## Overview

Design, implement, and manage enterprise-grade secrets management infrastructure using HashiCorp Vault, covering dynamic credential generation, automated secret rotation, fine-grained access policies, comprehensive audit logging, Kubernetes secrets management, and CI/CD integration. This skill ensures that all secrets — API keys, database credentials, TLS certificates, signing keys, and service account tokens — are securely stored, accessed, rotated, and audited throughout their lifecycle. Secrets management is a critical control across all compliance frameworks (SOC 2, PCI DSS, ISO 27001, GDPR) and a frequent audit focus area.

## Competency Dimensions

| Dimension                     | Description                                                      | Proficiency Indicators                                                                                                                     |
| ----------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| HashiCorp Vault Architecture  | Designing and operating Vault clusters for production workloads  | Deploys Vault in HA mode with auto-unseal; achieves 99.99% uptime; implements disaster recovery replication; manages Raft storage backend  |
| Dynamic Credentials           | Configuring Vault to generate short-lived, on-demand credentials | Dynamic credentials for 100% of database and cloud service access; credentials expire within 1 hour; zero static credentials in production |
| Secret Rotation               | Automated rotation of all managed secrets                        | 100% of secrets rotated on defined schedule (≤90 days for static, ≤1 hour for dynamic); rotation failures alert within 5 minutes           |
| Access Policies               | Fine-grained ACL and RBAC policies for secret access             | Every secret access governed by least-privilege policy; policies version-controlled; access reviewed quarterly                             |
| Audit Logging                 | Comprehensive, tamper-proof audit trail for all Vault operations | 100% of Vault operations logged (auth, access, policy changes); logs shipped to SIEM; log integrity verified                               |
| Kubernetes Secrets Management | Integrating Vault with Kubernetes for pod-level secret injection | Vault Agent Injector deployed; secrets injected as environment variables or volumes; no Kubernetes Secrets for sensitive data              |
| CI/CD Integration             | Securely providing secrets to CI/CD pipelines                    | CI/CD pipelines authenticate via OIDC (no static tokens); secrets scoped to specific workflows; secret access logged and monitored         |

## Execution Guidance

### 1. HashiCorp Vault Architecture

**Production Vault Deployment — High Availability:**

```hcl
# vault-ha-config.hcl — Vault server configuration
storage "raft" {
  path    = "/opt/vault/data"
  node_id = "vault-1"

  retry_join {
    leader_api_addr = "https://vault-1.vault.internal:8200"
  }
  retry_join {
    leader_api_addr = "https://vault-2.vault.internal:8200"
  }
  retry_join {
    leader_api_addr = "https://vault-3.vault.internal:8200"
  }
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file  = "/opt/vault/tls/vault.key"
  tls_min_version = "tls12"
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "alias/vault-auto-unseal"
}

api_addr     = "https://vault-1.vault.internal:8200"
cluster_addr = "https://vault-1.vault.internal:8201"

ui = true

log_level = "info"

# Telemetry
telemetry {
  prometheus_retention_time = "24h"
  disable_hostname = true
}
```

**Terraform — Vault HA on EKS:**

```hcl
# vault-infrastructure/vault-ha.tf

module "vault" {
  source  = "hashicorp/vault-helm/kubernetes"
  version = "0.28.0"

  set {
    name  = "server.ha.enabled"
    value = "true"
  }

  set {
    name  = "server.ha.raft.enabled"
    value = "true"
  }

  set {
    name  = "server.ha.raft.setNodeId"
    value = "true"
  }

  set {
    name  = "server.replicas"
    value = "3"
  }

  set {
    name  = "server.dataStorage.enabled"
    value = "true"
  }

  set {
    name  = "server.dataStorage.size"
    value = "50Gi"
  }

  # Auto-unseal with AWS KMS
  set {
    name  = "server.ha.raft.config"
    value = file("${path.module}/vault-raft-config.hcl")
  }

  # Vault Agent Injector for Kubernetes
  set {
    name  = "injector.enabled"
    value = "true"
  }

  set {
    name  = "injector.externalVaultAddr"
    value = "https://vault.company.internal:8200"
  }
}

# AWS KMS key for auto-unseal
resource "aws_kms_key" "vault_unseal" {
  description             = "Vault auto-unseal key"
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
        Sid    = "Allow Vault EKS Nodes"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.vault_eks_nodes.arn
        }
        Action = [
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

**Vault Initialization & Unseal (Automated with AWS KMS):**

```bash
# With AWS KMS auto-unseal, no manual unseal needed
# Vault automatically unseals using KMS key on startup

# Verify Vault status
vault status

# Expected output:
# Key             Value
# ---             -----
# Seal Type       awskms
# Initialized     true
# Sealed          false        # ← Auto-unsealed
# Total Shares    0            # ← No Shamir keys needed
# Threshold       0
# Version         1.16.0
# Storage Type    raft
# Cluster Name    vault-cluster
# Cluster ID      xxxxxxxx
# HA Enabled      true
# HA Cluster      https://vault-1:8201
# HA Mode         active
```

### 2. Dynamic Credentials

**Database Dynamic Credentials — PostgreSQL:**

```hcl
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/mobile-app-db \
  plugin_name=postgresql-database-plugin \
  allowed_roles="mobile-app-readonly,mobile-app-readwrite" \
  connection_url="postgresql://{{username}}:{{password}}@mobile-app-db.example.com:5432/mobile_app?sslmode=verify-full" \
  username="vault-admin" \
  password="vault-admin-password" \
  root_rotation_statements="ALTER USER \"vault-admin\" WITH PASSWORD '{{password}}';"

# Create readonly role (1-hour TTL)
vault write database/roles/mobile-app-readonly \
  db_name=mobile-app-db \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  revocation_statements="ALTER ROLE \"{{name}}\" NOLOGIN;" \
  default_ttl="1h" \
  max_ttl="24h"

# Create readwrite role (30-min TTL)
vault write database/roles/mobile-app-readwrite \
  db_name=mobile-app-db \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  revocation_statements="ALTER ROLE \"{{name}}\" NOLOGIN;" \
  default_ttl="30m" \
  max_ttl="4h"
```

**AWS Dynamic Credentials:**

```hcl
# Enable AWS secrets engine
vault secrets enable aws

# Configure AWS root credentials (for generating IAM users/roles)
vault write aws/config/root \
  access_key="AKIA..." \
  secret_key="..." \
  region="us-east-1"

# Create IAM role for CI/CD pipeline (short-lived)
vault write aws/roles/github-actions-deploy \
  credential_type=assumed_role \
  role_arns="arn:aws:iam::123456789012:role/github-actions-deploy" \
  default_ttl="1h" \
  max_ttl="4h"

# Create IAM user for legacy systems (rotate automatically)
vault write aws/roles/legacy-app-access \
  credential_type=iam_user \
  policy_document=-<<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::mobile-app-assets/*"
    }
  ]
}
EOF
  default_ttl="1h"
  max_ttl="4h"
```

**Application Usage — Dynamic Credentials:**

```python
# Python — Retrieve dynamic database credentials from Vault
import hvac
import psycopg2

def get_db_connection():
    client = hvac.Client(
        url='https://vault.company.internal:8200',
        namespace='mobile-app'
    )

    # Authenticate using Kubernetes service account
    client.auth.kubernetes.login(
        role='mobile-app-backend',
        jwt=open('/var/run/secrets/kubernetes.io/serviceaccount/token').read()
    )

    # Get dynamic database credentials
    creds = client.secrets.database.generate_credentials(
        name='mobile-app-readonly',
        mount_point='database'
    )

    username = creds['data']['username']
    password = creds['data']['password']

    # Connect with dynamic credentials
    return psycopg2.connect(
        host='mobile-app-db.example.com',
        dbname='mobile_app',
        user=username,
        password=password,
        sslmode='verify-full'
    )

# Credentials automatically expire after 1 hour
# Application must re-authenticate to get new credentials
```

### 3. Secret Rotation

**Automatic Rotation Configuration:**

```hcl
# Root credential rotation for database
vault write -force database/rotate-root/mobile-app-db

# Configure automatic rotation for static secrets
vault write secret/data/mobile/api-keys \
  rotation_period=7776000 \  # 90 days in seconds
  data='{"stripe-key": "sk_live_...", "sendgrid-key": "SG...."}'

# Rotation via API
curl --header "X-Vault-Token: $VAULT_TOKEN" \
  --request POST \
  --data '{"rotation_period": "7776000"}' \
  https://vault.company.internal:8200/v1/secret/data/mobile/api-keys
```

**Rotation Monitoring:**

```bash
# Check rotation status for all secrets
vault list secret/metadata/mobile/

# Check lease status for dynamic credentials
vault list sys/leases/lookup/database/creds/

# Monitor upcoming expirations
vault list sys/leases/lookup/aws/creds/ | while read lease_id; do
    vault read sys/leases/lookup/$lease_id
done

# Alert on rotation failures
vault read sys/internal/counters/requests
```

**Rotation Failure Alerting:**

```python
# lambda/vault-rotation-monitor.py
import boto3
import hvac
import os
from datetime import datetime, timedelta

def check_rotation_status():
    client = hvac.Client(
        url=os.environ['VAULT_ADDR'],
        token=os.environ['VAULT_TOKEN']
    )

    # Check database credentials
    db_roles = ['mobile-app-readonly', 'mobile-app-readwrite']
    for role in db_roles:
        try:
            lease_list = client.sys.list_leases(
                f'database/creds/{role}/'
            )
            for lease in lease_list.get('data', {}).get('keys', []):
                lease_info = client.sys.read_lease(f'database/creds/{role}/{lease}')
                expire_time = datetime.fromisoformat(lease_info['data']['expire_time'])
                if expire_time < datetime.now() + timedelta(minutes=30):
                    send_alert(f"Lease expiring soon: {role}/{lease}")
        except Exception as e:
            send_alert(f"Error checking rotation for {role}: {e}")

def send_alert(message):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=os.environ['ALERT_SNS_ARN'],
        Subject="⚠️ Vault Rotation Alert",
        Message=message
    )
```

### 4. Access Policies

**ACL Policy — Mobile App Backend:**

```hcl
# policies/mobile-app-backend.hcl
path "secret/data/mobile/api-keys" {
  capabilities = ["read"]
}

path "database/creds/mobile-app-readonly" {
  capabilities = ["read"]
  description  = "Generate readonly database credentials"
}

path "database/creds/mobile-app-readwrite" {
  capabilities = ["read"]
  description  = "Generate readwrite database credentials"
  min_wrapping_ttl = "1s"
}

# Allow token renewal
path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}

# Deny everything else (implicit deny)
```

**ACL Policy — CI/CD Pipeline:**

```hcl
# policies/github-actions-deploy.hcl
path "secret/data/mobile/android/*" {
  capabilities = ["read"]
  description  = "Android build secrets"
}

path "secret/data/mobile/ios/*" {
  capabilities = ["read"]
  description  = "iOS build secrets"
}

path "secret/data/mobile/firebase/*" {
  capabilities = ["read"]
  description  = "Firebase service account"
}

path "aws/creds/github-actions-deploy" {
  capabilities = ["read"]
  description  = "Assume AWS role for deployment"
}

# No access to production secrets
path "secret/data/mobile/production/*" {
  capabilities = ["deny"]
}
```

**ACL Policy — Kubernetes Service Account:**

```hcl
# policies/mobile-app-k8s.hcl
path "secret/data/mobile/config" {
  capabilities = ["read"]
}

path "database/creds/mobile-app-readonly" {
  capabilities = ["read"]
}

path "database/creds/mobile-app-readwrite" {
  capabilities = ["read"]
}

path "transit/encrypt/mobile-app-key" {
  capabilities = ["update"]
}

path "transit/decrypt/mobile-app-key" {
  capabilities = ["update"]
}
```

**Policy Assignment via Kubernetes Auth:**

```hcl
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth
vault write auth/kubernetes/config \
  token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  kubernetes_host="https://kubernetes.default.svc:443" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# Create role mapping
vault write auth/kubernetes/role/mobile-app-backend \
  bound_service_account_names="mobile-app-backend" \
  bound_service_account_namespaces="mobile-app" \
  policies="mobile-app-k8s" \
  ttl="24h" \
  max_ttl="72h"
```

### 5. Audit Logging

**Enable Audit Devices:**

```bash
# File audit device — detailed logs to file
vault audit enable file file_path=/var/log/vault/audit.log

# Syslog audit device — logs to syslog
vault audit enable syslog tag="vault" log_raw=false

# Socket audit device — logs to remote SIEM
vault audit enable socket log_raw=false socket_type=tcp address="siem.company.internal:5140"

# Verify audit devices
vault audit list
```

**Audit Log Configuration:**

```hcl
# Vault audit configuration
# All audit devices log the following:
# - Authentication attempts (success and failure)
# - Secret access (read, write, delete)
# - Policy changes
# - Secret engine changes
# - Auth method changes
# - Token operations

# Audit logs include:
# - Timestamp
# - Request ID
# - Client token (hashed)
# - Client IP
# - Operation (read, write, delete, list)
# - Path accessed
# - Response (success/failure)
# - Error message (if applicable)

# Raw secret values are NEVER logged (log_raw=false)
```

**Audit Log Shipping to SIEM:**

```yaml
# fluentd configuration for Vault audit logs
<source>
@type tail
path /var/log/vault/audit.log
pos_file /var/log/fluentd/vault-audit.log.pos
tag vault.audit
format json
time_key time
time_format %iso8601
</source>

<match vault.audit>
@type splunk_hec
host splunk.company.internal
port 8088
token ${SPLUNK_HEC_TOKEN}
index vault-audit
source vault
sourcetype vault:audit
flush_interval 5s
</match>
```

**Audit Log Monitoring — Key Alerts:**

| Alert Condition                                 | Severity | Response                                       |
| ----------------------------------------------- | -------- | ---------------------------------------------- |
| Failed authentication attempt (5+ in 5 minutes) | High     | Investigate potential brute force              |
| Policy modification                             | Critical | Verify authorized; investigate if not          |
| Secret engine disabled/enabled                  | Critical | Verify authorized; investigate if not          |
| Root token usage                                | Critical | Root tokens should never be used in production |
| Audit device disabled                           | Critical | Immediately re-enable; investigate             |
| Access from unauthorized IP                     | High     | Block IP; investigate access pattern           |

### 6. Kubernetes Secrets Management

**Vault Agent Injector — Sidecar Pattern:**

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mobile-app-backend
  namespace: mobile-app
  annotations:
    vault.hashicorp.com/agent-inject: "true"
    vault.hashicorp.com/role: "mobile-app-backend"
    vault.hashicorp.com/agent-inject-secret-db-creds: "database/creds/mobile-app-readwrite"
    vault.hashicorp.com/agent-inject-template-db-creds: |
      {{- with secret "database/creds/mobile-app-readwrite" -}}
      DATABASE_HOST=mobile-app-db.example.com
      DATABASE_PORT=5432
      DATABASE_NAME=mobile_app
      DATABASE_USER={{ .Data.username }}
      DATABASE_PASSWORD={{ .Data.password }}
      DATABASE_SSL_MODE=verify-full
      {{- end }}
    vault.hashicorp.com/agent-inject-secret-api-keys: "secret/data/mobile/api-keys"
    vault.hashicorp.com/agent-inject-template-api-keys: |
      {{- with secret "secret/data/mobile/api-keys" -}}
      STRIPE_API_KEY={{ .Data.data.stripe-key }}
      SENDGRID_API_KEY={{ .Data.data.sendgrid-key }}
      {{- end }}
    vault.hashicorp.com/agent-pre-populate-only: "false"
    vault.hashicorp.com/agent-run-as-user: "1000"
    vault.hashicorp.com/agent-run-as-group: "1000"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mobile-app-backend
  template:
    metadata:
      labels:
        app: mobile-app-backend
    spec:
      serviceAccountName: mobile-app-backend
      containers:
        - name: backend
          image: ghcr.io/our-org/mobile-api-backend:latest
          env:
            - name: DATABASE_HOST
              value: "mobile-app-db.example.com"
            - name: DATABASE_PORT
              value: "5432"
            - name: DATABASE_NAME
              value: "mobile_app"
          envFrom:
            - secretRef:
                name: mobile-app-env-secrets # Populated by Vault Agent
```

**Kubernetes Service Account for Vault Auth:**

```yaml
# k8s/service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mobile-app-backend
  namespace: mobile-app
  annotations:
    vault.hashicorp.com/agent-inject: "true"
    vault.hashicorp.com/role: "mobile-app-backend"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: mobile-app-backend-role
  namespace: mobile-app
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: mobile-app-backend-binding
  namespace: mobile-app
subjects:
  - kind: ServiceAccount
    name: mobile-app-backend
roleRef:
  kind: Role
  name: mobile-app-backend-role
  apiGroup: rbac.authorization.k8s.io
```

### 7. CI/CD Integration

**GitHub Actions — OIDC Authentication to Vault:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    tags: ["v*"]

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      # Authenticate to Vault using GitHub OIDC
      - name: Authenticate to Vault
        uses: hashicorp/vault-action@v2.8.0
        with:
          url: https://vault.company.internal
          method: jwt
          role: github-actions-deploy
          jwtGithubAudience: https://vault.company.internal
          exportToken: true
          secrets: |
            secret/data/mobile/android signing-keystore-password | KEYSTORE_PASSWORD ;
            secret/data/mobile/firebase service-account-key | FIREBASE_SA_KEY ;
            aws/creds/github-actions-deploy | AWS_CREDS ;

      # Use retrieved secrets
      - name: Deploy
        run: |
          aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
          aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
          aws configure set aws_session_token $AWS_SESSION_TOKEN
          # Deploy using temporary AWS credentials
          ./scripts/deploy.sh
```

**Vault JWT/OIDC Auth Method for GitHub Actions:**

```hcl
# Enable JWT auth
vault auth enable jwt

# Configure OIDC for GitHub Actions
vault write auth/jwt/config \
  oidc_discovery_url="https://token.actions.githubusercontent.com" \
  bound_issuer="https://token.actions.githubusercontent.com"

# Create role for mobile app deployment
vault write auth/jwt/role/github-actions-deploy \
  role_type="jwt" \
  bound_audiences="https://vault.company.internal" \
  bound_subject="repo:our-org/mobile-app:ref:refs/heads/main" \
  bound_claims_type="glob" \
  bound_claims='{"repository": "our-org/mobile-app", "workflow_ref": "our-org/mobile-app/.github/workflows/deploy.yml@refs/heads/main"}' \
  user_claim="repository" \
  token_policies="github-actions-deploy" \
  ttl="1h" \
  max_ttl="4h"
```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                                  |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 3** (Architecture)           | Secrets management architecture designed; Vault integration points identified; dynamic credential strategy defined                           |
| **Stage 4** (Implementation Plan)    | Vault deployment plan included; secret rotation schedule defined; CI/CD integration approach documented                                      |
| **Stage 5** (Development)            | Vault operational; all application secrets managed via Vault; dynamic credentials for database access; CI/CD pipelines authenticate via OIDC |
| **Stage 6** (Code Review)            | Secrets management reviewed; no hardcoded secrets in codebase; Vault access policies verified                                                |
| **Stage 8** (Integrity Verification) | Vault audit logs reviewed; secret rotation verified; all credentials confirmed as dynamic or properly rotated                                |
| **Stage 10** (Release Readiness)     | Secrets management posture confirmed; zero static secrets in production; audit trail complete                                                |

## Quality Standards

| Metric                     | Standard                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Secret Coverage**        | 100% of production secrets managed via Vault; zero hardcoded secrets in codebase or configurations     |
| **Dynamic Credentials**    | 100% of database and cloud service credentials are dynamic; TTL ≤1 hour for database, ≤4 hours for AWS |
| **Secret Rotation**        | 100% of static secrets rotated ≤90 days; 100% of dynamic credentials rotated on TTL expiry             |
| **Access Control**         | Every secret access governed by least-privilege ACL policy; policies reviewed quarterly                |
| **Audit Logging**          | 100% of Vault operations logged; logs shipped to SIEM within 5 minutes; log integrity verified         |
| **Vault Availability**     | 99.99% uptime for Vault cluster; HA with 3 nodes; automated disaster recovery                          |
| **CI/CD Integration**      | 100% of CI/CD pipelines authenticate via OIDC; no static tokens for Vault access                       |
| **Kubernetes Integration** | 100% of Kubernetes secrets injected via Vault Agent; no Kubernetes Secret objects for sensitive data   |
