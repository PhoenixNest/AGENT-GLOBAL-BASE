# Execution Guidance

## Execution Guidance

### GCP Architecture

```
GCP Production Architecture:

                    ┌─────────────────────────────────────┐
                    │        Cloud Load Balancing          │
                    │  (Global HTTP(S) Load Balancer)      │
                    └────────────┬──────────────┬──────────┘
                                 │              │
                    ┌────────────▼────┐  ┌──────▼────────────┐
                    │   Region 1      │  │   Region 2        │
                    │   (us-central1) │  │   (europe-west1)  │
                    │                 │  │                   │
                    │  ┌───────────┐  │  │  ┌─────────────┐  │
                    │  │   GKE     │  │  │  │   GKE       │  │
                    │  │  Cluster  │  │  │  │  Cluster    │  │
                    │  │           │  │  │  │             │  │
                    │  │ ┌───────┐ │  │  │  │ ┌─────────┐ │  │
                    │  │ │ API   │ │  │  │  │ │ API     │ │  │
                    │  │ │ Pods  │ │  │  │  │ │ Pods    │ │  │
                    │  │ └───────┘ │  │  │  │ └─────────┘ │  │
                    │  │ ┌───────┐ │  │  │  │ ┌─────────┐ │  │
                    │  │ │Worker │ │  │  │  │ │ Worker  │ │  │
                    │  │ │ Pods  │ │  │  │  │ │ Pods    │ │  │
                    │  │ └───────┘ │  │  │  │ └─────────┘ │  │
                    │  └─────┬─────┘  │  │  └──────┬──────┘  │
                    │        │        │  │         │         │
                    │  ┌─────▼─────┐  │  │  ┌──────▼──────┐  │
                    │  │Cloud SQL  │  │  │  │ Cloud SQL   │  │
                    │  │(Primary)  │◄─┼──┼──┤(Read Replica)│  │
                    │  └───────────┘  │  │  └─────────────┘  │
                    │  ┌───────────┐  │  │  ┌─────────────┐  │
                    │  │  Redis    │  │  │  │   Redis     │  │
                    │  │ (Memorystore)│ │  │ (Memorystore) │  │
                    │  └───────────┘  │  │  └─────────────┘  │
                    └─────────────────┘  └───────────────────┘
```

### Terraform Module Design

```hcl
# modules/gke-cluster/main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "GCP region"
}

variable "cluster_name" {
  type        = string
  description = "GKE cluster name"
}

variable "machine_type" {
  type        = string
  description = "Machine type for node pool"
  default     = "e2-standard-4"
}

variable "min_node_count" {
  type        = number
  description = "Minimum number of nodes"
  default     = 3
}

variable "max_node_count" {
  type        = number
  description = "Maximum number of nodes for autoscaling"
  default     = 20
}

variable "network" {
  type        = string
  description = "VPC network name"
}

variable "subnetwork" {
  type        = string
  description = "VPC subnetwork name"
}

variable "enable_autopilot" {
  type        = bool
  description = "Enable GKE Autopilot mode"
  default     = false
}

resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.region

  # Use VPC-native (alias IPs) for better networking
  network    = var.network
  subnetwork = var.subnetwork
  ip_allocation_policy {}

  # Remove default node pool (we create our own)
  remove_default_node_pool = true
  initial_node_count       = 1

  # Master authorized networks
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block   = "10.0.0.0/8"
      display_name = "Internal networks"
    }
  }

  # Security settings
  resource_labels = {
    environment = var.environment
    managed_by  = "terraform"
  }

  # Enable workload identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  # Logging and monitoring
  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = true
    }
  }

  lifecycle {
    ignore_changes = [
      node_pool,        # We manage node pools separately
      initial_node_count,
    ]
  }
}

resource "google_container_node_pool" "primary" {
  name       = "${var.cluster_name}-primary-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name

  initial_node_count = var.min_node_count

  autoscaling {
    min_node_count = var.min_node_count
    max_node_count = var.max_node_count
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type = var.machine_type
    disk_size_gb = 100
    disk_type    = "pd-balanced"

    # Use workload identity (no service account keys)
    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    # Shielded nodes
    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    # OAuth scopes (minimal)
    oauth_scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]

    metadata = {
      disable-legacy-endpoints = "true"
    }

    labels = {
      pool = "primary"
    }

    taint {
      key    = "dedicated"
      value  = "primary"
      effect = "NO_SCHEDULE"
    }
  }
}

output "cluster_endpoint" {
  description = "GKE cluster endpoint"
  value       = google_container_cluster.primary.endpoint
}

output "cluster_ca_certificate" {
  description = "Cluster CA certificate"
  value       = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
}

output "cluster_name" {
  description = "Cluster name"
  value       = google_container_cluster.primary.name
}
```

**Root module with workspace isolation:**

```hcl
# environments/production/main.tf
terraform {
  backend "gcs" {
    bucket = "company-terraform-state"
    prefix = "production"
  }
}

module "vpc" {
  source = "../../modules/vpc"

  project_id  = var.project_id
  region      = var.region
  environment = "production"
}

module "gke_primary" {
  source = "../../modules/gke-cluster"

  project_id     = var.project_id
  region         = var.region
  cluster_name   = "api-cluster-primary"
  machine_type   = "e2-standard-8"
  min_node_count = 3
  max_node_count = 30
  network        = module.vpc.network_name
  subnetwork     = module.vpc.subnetwork_name
  environment    = "production"
}

module "cloud_sql" {
  source = "../../modules/cloud-sql"

  project_id       = var.project_id
  region           = var.region
  instance_name    = "api-database"
  database_version = "POSTGRES_16"
  tier             = "db-custom-4-16384"  # 4 vCPU, 16GB RAM
  disk_size        = 100
  enable_ha        = true
  network          = module.vpc.network_name
}
```

### Kubernetes Deployment Strategies

**Canary deployment with Istio:**

```yaml
# Kubernetes Deployment (stable version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: api
      track: stable
  template:
    metadata:
      labels:
        app: api
        track: stable
    spec:
```

      containers:
        - name: api
          image: gcr.io/company/api:v1.2.3
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: "1"
              memory: 1Gi
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10

# Kubernetes Deployment (canary version)

apiVersion: apps/v1
kind: Deployment
metadata:
name: api-canary
spec:
replicas: 1
selector:
matchLabels:
app: api
track: canary
template:
metadata:
labels:
app: api
track: canary
spec:
containers: - name: api
image: gcr.io/company/api:v1.3.0-rc1
resources:
requests:
cpu: 500m
memory: 512Mi
limits:
cpu: "1"
memory: 1Gi

# Istio VirtualService — route 10% to canary

apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
name: api-routing
spec:
hosts: - api.company.com
http: - route: - destination:
host: api-service
subset: stable
weight: 90 - destination:
host: api-service
subset: canary
weight: 10

# Canary promotion (increase to 50%)

# kubectl patch virtualservice api-routing --type=json -p='[

# {"op": "replace", "path": "/spec/http/0/route/0/weight", "value": 50},

# {"op": "replace", "path": "/spec/http/0/route/1/weight", "value": 50}

# ]'

````

**Blue-green deployment:**

```yaml
# Service points to "blue" (current production)
apiVersion: v1
kind: Service
metadata:
  name: api-production
spec:
  selector:
    app: api
    track: blue  # Switch to "green" for cutover
  ports:
    - port: 80
      targetPort: 8080

# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-blue
spec:
  replicas: 10
  selector:
    matchLabels:
      app: api
      track: blue
  template:
    metadata:
      labels:
        app: api
        track: blue
    spec:
      containers:
        - name: api
          image: gcr.io/company/api:v1.2.3

# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-green
spec:
  replicas: 10
  selector:
    matchLabels:
      app: api
      track: green
  template:
    metadata:
      labels:
        app: api
        track: green
    spec:
      containers:
        - name: api
          image: gcr.io/company/api:v1.3.0

# Cutover: switch service selector
# kubectl patch service api-production -p '{"spec":{"selector":{"track":"green"}}}'

# Rollback: switch back
# kubectl patch service api-production -p '{"spec":{"selector":{"track":"blue"}}}'
````

**Horizontal Pod Autoscaler:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-stable
  minReplicas: 3
  maxReplicas: 30
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 5
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300 # Wait 5 min before scaling down
      policies:
        - type: Pods
          value: 2
          periodSeconds: 120
```

### Multi-Region Traffic Management

```yaml
# Cloud DNS with latency-based routing
# Traffic directed to nearest healthy region

# Global load balancer configuration
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: api-certificate
spec:
  domains:
    - api.company.com
---
# Backend services per region
apiVersion: cloud.google.com/v1
kind: BackendService
metadata:
  name: api-backend-us
spec:
  protocol: HTTP
  healthChecks:
    - api-health-check
  localityLbPolicy: ROUND_ROBIN
  connectionDraining:
    drainingTimeoutSec: 300
---
apiVersion: cloud.google.com/v1
kind: BackendService
metadata:
  name: api-backend-eu
spec:
  protocol: HTTP
  healthChecks:
    - api-health-check
  localityLbPolicy: ROUND_ROBIN
---
# URL map with failover
apiVersion: cloud.google.com/v1
kind: URLMap
metadata:
  name: api-urlmap
spec:
  defaultService: api-backend-us
  hostRules:
    - hosts:
        - api.company.com
      pathMatcher: api-paths
  pathMatchers:
    - name: api-paths
      defaultService: api-backend-us
      pathRules:
        - paths:
            - /api/*
          service: api-backend-us

# Failover: if US region unhealthy, route to EU
# Configured via health check thresholds
apiVersion: cloud.google.com/v1
kind: HealthCheck
metadata:
  name: api-health-check
spec:
  httpHealthCheck:
    requestPath: /healthz
    port: 8080
    checkIntervalSec: 10
    timeoutSec: 5
    unhealthyThreshold: 3   # 30 seconds to detect failure
    healthyThreshold: 2     # 20 seconds to confirm recovery
```

### Disaster Recovery Runbook

```markdown
# Disaster Recovery Runbook
```
