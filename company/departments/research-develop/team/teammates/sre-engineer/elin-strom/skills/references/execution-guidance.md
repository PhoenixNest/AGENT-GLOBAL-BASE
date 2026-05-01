# Execution Guidance

## Execution Guidance

### Falco Runtime Security

**Falco Architecture:**

```
Container Runtime → Falco (kernel module/eBPF) → Rule Engine → Output → Alerting
                                                      ↓
                                                Security Events
                                                (JSON format)
                                                      ↓
                                        SIEM / Elasticsearch / Slack
```

**Custom Falco Rules:**

```yaml
# rules/order-service-rules.yaml
- rule: Unexpected Process in Order Service Container
  desc: Detects unexpected process execution in order service container
  condition: >
    container and
    container.image.repository contains "order-service" and
    proc.name not in (order-service, sh, bash, cat, ls, grep, sleep, env)
  output: >
    Unexpected process in order service container 
    (user=%user.name container=%container.name image=%container.image.repository 
    process=%proc.name cmd=%proc.cmdline)
  priority: CRITICAL
  tags: [container, process, order-service]

- rule: Sensitive File Access in Container
  desc: Detects access to sensitive files inside containers
  condition: >
    open_read and
    container and
    fd.name startswith /etc/shadow or
    fd.name startswith /etc/passwd or
    fd.name startswith /proc/ or
    fd.name startswith /var/run/secrets
  output: >
    Sensitive file access in container
    (user=%user.name container=%container.name file=%fd.name)
  priority: WARNING
  tags: [filesystem, container]

- rule: Outbound Connection to Non-Standard Port
  desc: Detects outbound connections to unusual ports
  condition: >
    outbound and
    container and
    fd.sport not in (80, 443, 5432, 6379, 53, 9090, 8080)
  output: >
    Outbound connection to non-standard port
    (user=%user.name container=%container.name connection=%fd.name)
  priority: WARNING
  tags: [network, container]

- rule: Privilege Escalation Attempt
  desc: Detects privilege escalation attempts in containers
  condition: >
    spawned_process and
    container and
    (proc.name = "sudo" or proc.name = "su" or proc.name = "chmod" or proc.name = "chown") and
    not proc.cmdline contains "/usr/local/bin/health-check"
  output: >
    Potential privilege escalation in container
    (user=%user.name container=%container.name process=%proc.name cmd=%proc.cmdline)
  priority: CRITICAL
  tags: [privilege, container]

- rule: Kubernetes API Access from Container
  desc: Detects attempts to access Kubernetes API from within containers
  condition: >
    outbound and
    container and
    fd.sip contains "kubernetes.default" or
    fd.sip contains "10.96.0.1"
  output: >
    Kubernetes API access from container
    (user=%user.name container=%container.name connection=%fd.name)
  priority: WARNING
  tags: [kubernetes, network]

- rule: Crypto Mining Detection
  desc: Detects known crypto mining processes
  condition: >
    spawned_process and
    (proc.name in (xmrig, minerd, cpuminer, cgminer, bfgminer, nicehash) or
     proc.cmdline contains "stratum+tcp" or
     proc.cmdline contains "mining" or
     proc.cmdline contains "coinhive")
  output: >
    Crypto mining detected
    (user=%user.name container=%container.name process=%proc.name cmd=%proc.cmdline)
  priority: CRITICAL
  tags: [crypto, mining, container]
```

**Falco Configuration:**

```yaml
# falco.yaml
program_output:
  enabled: true
  keep_alive: true
  program: "jq '{text: .output}' | curl -X POST -H 'Content-Type: application/json' -d @- https://slack-webhook.company.com/alerts"

http_output:
  enabled: true
  url: "http://falco-sidecar:8765/"
  keep_alive: true

json_output: true
json_include_output_property: true
json_include_tags_property: true

file_output:
  enabled: true
  keep_alive: false
  filename: /var/log/falco/events.json
```

### OSQuery Host Investigation

**OSQuery Configuration:**

```ini
# osquery.conf
{
  "options": {
    "config_plugin": "filesystem",
    "logger_plugin": "filesystem",
    "logger_path": "/var/log/osquery",
    "disable_logging": "false",
    "log_result_events": "true",
    "schedule_splay_percent": 10,
    "events_max": 50000,
    "events_expiry": 360,
    "disable_events": "false",
    "host_identifier": "hostname"
  },
  "schedule": {
    "system_info": {
      "query": "SELECT hostname, cpu_brand, physical_memory FROM system_info;",
      "interval": 3600
    },
    "running_processes": {
      "query": "SELECT pid, name, path, cmdline, uid FROM processes;",
      "interval": 300
    },
    "listening_ports": {
      "query": "SELECT address, port, pid FROM listening_ports;",
      "interval": 60
    },
    "cron_jobs": {
      "query": "SELECT * FROM crontab;",
      "interval": 3600
    },
    "installed_packages": {
      "query": "SELECT name, version, source FROM packages;",
      "interval": 86400
    },
    "file_integrity": {
      "query": "SELECT path, hash.sha256, size, uid, gid, mode FROM file WHERE path IN ('/etc/passwd', '/etc/shadow', '/etc/sudoers');",
      "interval": 300
    }
  },
  "packs": {
    "incident-response": "/usr/share/osquery/packs/incident-response.conf",
    "it-compliance": "/usr/share/osquery/packs/it-compliance.conf",
    "ossec-rootkit": "/usr/share/osquery/packs/ossec-rootkit.conf"
  }
}
```

**Security Investigation Queries:**

```sql
-- Find all processes with network connections
SELECT p.pid, p.name, p.path, p.cmdline, s.local_address, s.local_port, s.remote_address, s.remote_port
FROM processes p
JOIN process_open_sockets s ON p.pid = s.pid
WHERE s.family = 2;  -- IPv4

-- Check for unauthorized SUID binaries
SELECT path, uid, gid, mode, size, sha256
FROM file
WHERE path LIKE '/usr/%' AND (mode & 04000) = 04000;

-- Find recently modified system files
SELECT path, mtime, uid, gid, mode
FROM file
WHERE path IN ('/etc/passwd', '/etc/shadow', '/etc/sudoers', '/etc/ssh/sshd_config')
  AND mtime > (unix_time() - 86400);  -- Last 24 hours

-- Check for unauthorized SSH keys
SELECT path, uid, gid, mode
FROM file
WHERE path LIKE '/home/%/.ssh/authorized_keys';

-- Find processes running as root that shouldn't be
SELECT pid, name, cmdline, uid, gid, cwd
FROM processes
WHERE uid = 0 AND name NOT IN ('systemd', 'sshd', 'cron', 'dockerd', 'containerd', 'kubelet');

-- Check for anomalous DNS queries
SELECT datetime, query, query_type, answer
FROM dns_responses
WHERE query_type = 'A' AND answer LIKE '169.254.%';  -- Metadata endpoint queries

-- Find containers running as privileged
SELECT id, name, image, privileged, pid
FROM docker_container_labels
WHERE privileged = 'true';
```

**OSQuery Fleet Management:**

```python
# fleet_monitor.py
import requests
import json
from datetime import datetime

class OSQueryFleetMonitor:
    def __init__(self, kolide_api_url, api_token):
        self.api_url = kolide_api_url
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def check_host_compliance(self):
        """Check all hosts for security compliance."""
        queries = [
            {
                "name": "password_policy",
                "query": "SELECT * FROM users WHERE password_status = 'normal' AND uid >= 1000;"
            },
            {
                "name": "firewall_status",
                "query": "SELECT status FROM iptables WHERE chain = 'INPUT' AND policy = 'DROP';"
            },
            {
                "name": "ssh_config",
                "query": "SELECT * FROM ssh_configs WHERE key = 'PermitRootLogin' AND value = 'yes';"
            },
        ]

        results = {}
        for query in queries:
            response = requests.post(
                f"{self.api_url}/api/v1/osquery/distributed/read",
                headers=self.headers,
                json={"queries": {query["name"]: query["query"]}}
            )
            results[query["name"]] = response.json()

        return self.analyze_compliance(results)

    def analyze_compliance(self, results):
        """Analyze compliance results and flag violations."""
        violations = []

        # Check for users without password expiration
        for host, data in results.get("password_policy", {}).items():
            for row in data:
                violations.append({
                    "host": host,
                    "type": "password_policy",
                    "detail": f"User {row.get('username')} has no password expiration",
                    "severity": "medium",
                })

        # Check for root SSH access
        for host, data in results.get("ssh_config", {}).items():
            for row in data:
                violations.append({
                    "host": host,
                    "type": "ssh_root_login",
                    "detail": "Root SSH login is enabled",
                    "severity": "high",
                })

        return violations
```

### Container Image Scanning

**CI/CD Integration:**

```yaml
# .github/workflows/security-scan.yml
- name: Scan Container Image
  run: |
    # Build image
    docker build -t order-service:${{ github.sha }} .

    # Scan with Trivy
```

    trivy image --severity CRITICAL,HIGH --exit-code 1 order-service:${{ github.sha }}

    # Generate SBOM
    syft order-service:${{ github.sha }} -o spdx-json > sbom-${{ github.sha }}.json

    # Scan with Grype
    grype sbom:sbom-${{ github.sha }}.json --fail-on high

    # Push SBOM to artifact registry
    gcloud artifacts docker images add --sbom sbom-${{ github.sha }}.json \
      gcr.io/company-prod/order-service:${{ github.sha }}

- name: Gate on Security Scan Results
  if: failure()
  run: |
  echo "❌ Security scan failed. Critical/High CVEs detected."
  echo "Review the scan results and remediate before merging."
  exit 1

````

**Trivy Configuration:**

```yaml
# .trivy.yaml
severity:
  - CRITICAL
  - HIGH
  - MEDIUM

scan:
  security-checks:
    - vuln
    - config
    - secret

vulnerability:
  type:
    - os
    - library

ignore-unfixed: true

cache:
  backend: fs
  dir: /tmp/trivy-cache

# Allowed CVEs (with justification)
ignorefile: .trivyignore

# .trivyignore
# False positive — library not used in our code path
CVE-2024-1234

# Fix available but requires major version upgrade (planned for Q2)
CVE-2024-5678

# No fix available; mitigated by network policies
CVE-2024-9012
````

**Container Registry Policy:**

```yaml
container_registry_policy:
  scanning:
    on_push: true
    schedule: "daily"
    severity_threshold: "HIGH" # Block on HIGH and above

  signing:
    enabled: true
    tool: "cosign"
    key_management: "Cloud KMS"

  admission_control:
    enabled: true
    policy:
      - "Image must be scanned within last 24 hours"
      - "No CRITICAL CVEs"
      - "Image must be signed"
      - "Image must be from approved registry"

  retention:
    untagged_images: "7 days"
    tagged_images: "90 days"
    sbom_artifacts: "1 year"
```

### Network Anomaly Detection

**Network Baseline:**

```yaml
# network-baseline.yaml
baseline_period: 30_days
update_frequency: weekly

services:
  order-service:
    expected_egress:
      - destination: "cloud-sql-proxy:5432"
        protocol: TCP
        description: "Database connection"
      - destination: "memorystore:6379"
        protocol: TCP
        description: "Redis cache"
      - destination: "kafka:9092"
        protocol: TCP
        description: "Event publishing"
      - destination: "dns:53"
        protocol: UDP
        description: "DNS resolution"

    expected_ingress:
      - source: "api-gateway:8080"
        protocol: TCP
        description: "API requests"

    anomaly_thresholds:
      new_destination_alert: true
      volume_spike_threshold: 3x_baseline
      protocol_violation_alert: true
      after_hours_traffic_alert: true
```

**Network Policy Enforcement:**

```yaml
# Kubernetes NetworkPolicy with anomaly detection
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: order-service-network-policy
  namespace: production
  annotations:
    network-monitoring: "enabled"
    baseline-hash: "abc123..."
spec:
  podSelector:
    matchLabels:
      app: order-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: cloud-sql-proxy
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: memorystore
      ports:
        - protocol: TCP
          port: 6379
    - to:
        - podSelector:
            matchLabels:
              app: kafka
      ports:
        - protocol: TCP
          port: 9092
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
        - podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

**Egress Filtering:**

```yaml
# Allowed egress destinations (default deny all others)
egress_allowlist:
  - "*.googleapis.com:443" # GCP APIs
  - "*.gcr.io:443" # Container registry
  - "*.cloudsql.com:5432" # Cloud SQL
  - "auth.company.com:443" # Authentication service
  - "slack-webhook.company.com:443" # Alerting

egress_deny:
  - "0.0.0.0/0" # Default deny all

egress_logging:
  - log_all_denied: true
  - log_all_new_destinations: true
  - alert_on_new_destination: true
```

### Security Event Correlation

**SIEM Integration:**

```python
# siem_correlator.py
from datetime import datetime, timedelta
from collections import defaultdict

class SecurityEventCorrelator:
    """Correlate security events across Falco, OSQuery, and container scanning."""

    def __init__(self, lookback_hours=24):
        self.lookback = timedelta(hours=lookback_hours)

    def correlate_events(self, events):
        """Correlate events to identify attack patterns."""
        correlated = []

        # Group events by host/container
        by_target = defaultdict(list)
        for event in events:
            target = event.get('container', {}).get('id') or event.get('host', {}).get('name')
            if target:
                by_target[target].append(event)

        for target, target_events in by_target.items():
            # Sort by timestamp
            target_events.sort(key=lambda e: e['timestamp'])

            # Check for attack patterns
            patterns = self.detect_patterns(target_events)
            if patterns:
                correlated.append({
                    'target': target,
                    'patterns': patterns,
                    'severity': max(p['severity'] for p in patterns),
                    'events': target_events,
                    'recommendation': self.generate_recommendation(patterns),
                })

        return correlated

    def detect_patterns(self, events):
        """Detect known attack patterns."""
        patterns = []

        # Pattern: Reconnaissance → Exploitation → Lateral Movement
        recon_events = [e for e in events if e.get('type') in ['network_scan', 'port_scan']]
        exploit_events = [e for e in events if e.get('type') in ['privilege_escalation', 'exploit_attempt']]
        lateral_events = [e for e in events if e.get('type') in ['lateral_movement', 'unauthorized_access']]

        if recon_events and exploit_events:
            patterns.append({
                'name': 'Reconnaissance + Exploitation',
                'severity': 'critical',
                'description': 'Reconnaissance activity followed by exploitation attempt',
            })

        if exploit_events and lateral_events:
            patterns.append({
                'name': 'Exploitation + Lateral Movement',
                'severity': 'critical',
                'description': 'Successful exploitation followed by lateral movement',
            })

        # Pattern: Crypto mining indicators
        mining_events = [e for e in events if e.get('type') == 'crypto_mining']
        if mining_events:
            patterns.append({
                'name': 'Crypto Mining',
                'severity': 'high',
                'description': f'{len(mining_events)} crypto mining indicators detected',
            })

        # Pattern: Data exfiltration indicators
        egress_events = [e for e in events if e.get('type') == 'unusual_egress']
        if len(egress_events) > 5:
            patterns.append({
                'name': 'Potential Data Exfiltration',
                'severity': 'critical',
                'description': 'Unusual egress volume detected',
            })

        return patterns

    def generate_recommendation(self, patterns):
        """Generate remediation recommendations."""
        recommendations = []

        for pattern in patterns:
            if pattern['name'] == 'Crypto Mining':
                recommendations.append("Isolate affected container; check for vulnerable entry points")
            elif pattern['name'] == 'Potential Data Exfiltration':
                recommendations.append("Block egress to suspicious destinations; investigate data access logs")
            elif pattern['severity'] == 'critical':
                recommendations.append("Isolate affected host; initiate incident response procedure")

        return recommendations
```
