---
name: container-runtime-security
description: Harden container runtime environments — ECS Fargate task security, Docker image scanning, runtime threat detection with Falco, and network policy enforcement — ensuring containers run with minimal privilege and any anomalous behavior is detected within minutes.
version: "1.0.0"
---

# Container Runtime Security

| Competency               | Description                                                        | Quality Criteria                                                                                                          |
| ------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| ECS Task Hardening       | Configure ECS Fargate tasks with least-privilege security          | No root containers; read-only root filesystem where possible; no privileged mode; task role scoped to minimum permissions |
| Image Scanning           | Scan container images for CVEs in CI and registry                  | `trivy` or ECR Enhanced Scanning runs on every build; Critical CVEs block deployment; images rescanned weekly in registry |
| Runtime Threat Detection | Deploy Falco for runtime anomaly detection                         | Falco rules cover: unexpected process execution, file writes to `/etc`, shell spawning in containers; alerts to PagerDuty |
| Secrets Management       | Ensure container secrets injected via AWS Secrets Manager, not env | No plaintext secrets in task definition environment variables; all secrets via `secrets` block in ECS task definition     |

## Execution Guidance

### ECS Task Hardening Checklist

```json
{
  "containerDefinitions": [
    {
      "user": "1000:1000",
      "readonlyRootFilesystem": true,
      "linuxParameters": {
        "capabilities": {
          "drop": ["ALL"],
          "add": []
        }
      },
      "privileged": false
    }
  ]
}
```

All ECS tasks must drop ALL Linux capabilities unless a specific capability is explicitly required and documented in the ADR.

### Falco Rule Example

```yaml
- rule: Shell spawned in container
  desc: Detect a shell being spawned in a container (potential intrusion)
  condition: >
    spawned_process and container and
    proc.name in (shell_binaries) and
    not proc.pname in (allowed_shell_progenitors)
  output: >
    Shell spawned in container (user=%user.name container=%container.name
    image=%container.image.repository proc=%proc.name)
  priority: WARNING
```

Alert every Falco WARNING to the on-call engineer. Alert every Falco ERROR (e.g., container escape attempt) as a P0 incident.
