---
name: container-runtime-security
description: Container runtime security covering Falco rules, eBPF-based monitoring, kernel syscall auditing, image vulnerability scanning, and runtime policy enforcement for production Kubernetes and Docker environments.
---

# Container Runtime Security

## Overview

This skill covers container runtime security, including Falco rules, eBPF-based monitoring, kernel syscall auditing, image vulnerability scanning, and runtime policy enforcement for production Kubernetes and Docker environments. It is used by SRE engineers during Stage 5 (Development) for infrastructure security hardening and Stage 8 (Integrity Verification) for runtime security conformance.

## Falco Rules Engine

**How Falco works**: Falco hooks into the Linux kernel via eBPF or a kernel module, intercepting system calls at runtime. It evaluates each syscall against a ruleset to detect anomalous behavior.

**Core rule structure**:

```yaml
- rule: Unexpected K8s API Server Access
  desc: Detects unexpected access to the K8s API server from a pod
  condition: spawned_process and proc.name contains "kubectl" and not k8s.ns.name = "kube-system"
  output: "Unexpected K8s API access (user=%user.name command=%proc.cmdline namespace=%k8s.ns.name)"
  priority: WARNING
  tags: [k8s, runtime]
```

**Rule categories**:

| Category             | Examples                                     | Priority |
| -------------------- | -------------------------------------------- | -------- |
| Privilege escalation | `setuid`, `setgid`, `mount`                  | CRITICAL |
| Container escape     | `ptrace`, `unshare`, `nsenter`               | CRITICAL |
| Unexpected network   | Outbound to unexpected IPs, DNS exfiltration | HIGH     |
| File integrity       | Writes to `/etc`, `/usr/bin`, `/root/.ssh`   | HIGH     |
| Process execution    | Unexpected binaries, reverse shells          | CRITICAL |

## eBPF-Based Monitoring

**Advantages over kernel modules**:

- No kernel recompilation required.
- Lower overhead (<1% CPU typically).
- Safer — eBPF verifier prevents kernel panics.

**Key monitoring targets**:

- Network connections: unexpected outbound, lateral movement.
- File system: writes to sensitive paths, config tampering.
- Process execution: unexpected child processes, cryptominers.
- Kernel calls: privilege escalation attempts, syscall anomalies.

## Runtime Policy Enforcement

**Policy-as-code approach**:

- Define allowed syscalls per container image (seccomp profiles).
- Block privileged containers in production namespaces.
- Enforce read-only root filesystems.
- Deny host namespace and host network access.

**Kubernetes security contexts**:

```yaml
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

## Image Scanning Integration

- Scan images at build time (Trivy, Snyk, Grype).
- Gate deployments on critical/high CVE count.
- Continuous monitoring for newly discovered CVEs in running images.
- SBOM generation and tracking for all deployed images.
