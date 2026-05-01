---
version: "1.0.0"
---

# Infrastructure Security

| Competency                 | Description                                                                                                         | Quality Criteria                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Falco Runtime Security     | Rule creation, syscall monitoring, container runtime visibility, alert integration, response automation             | Detects runtime anomalies within seconds; custom rules for application-specific threats |
| OSQuery Investigation      | Host-based queries, file integrity monitoring, process monitoring, network connection auditing, compliance checking | Queries across fleet of 100+ hosts; detects configuration drift within 5 minutes        |
| Container Scanning         | Image vulnerability scanning, SBOM generation, policy enforcement, registry integration, CI/CD gating               | 0 critical CVEs in production images; all images scanned before deployment              |
| Network Anomaly Detection  | Traffic baseline analysis, east-west monitoring, lateral movement detection, DNS monitoring, egress filtering       | Detects unauthorized network activity; blocks anomalous egress traffic                  |
| Security Event Correlation | SIEM integration, event enrichment, threat intelligence feeds, automated response playbooks                         | Correlates events across layers; automated response for known attack patterns           |

## Pipeline Integration

| Pipeline Stage                   | Application                                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------------------------ |
| Stage 3 (Architecture)           | Security architecture decisions; runtime security strategy; container scanning policy            |
| Stage 5 (Development)            | Falco rule implementation; OSQuery pack configuration; network policy setup                      |
| Stage 6 (Code Review)            | Security configuration review; container image scan results; network policy audit                |
| Stage 7 (Testing)                | Security scan integration testing; Falco rule validation; network policy testing                 |
| Stage 8 (Integrity Verification) | Runtime security audit; container scanning completeness; network policy enforcement verification |
| Stage 10 (Release Readiness)     | Infrastructure security sign-off; Falco/OSQuery operational verification; scan results review    |

## Quality Standards

| Metric                                | Target                                   | Measurement                          |
| ------------------------------------- | ---------------------------------------- | ------------------------------------ |
| Container scan coverage               | 100% of images scanned before deployment | CI/CD pipeline scan results          |
| Critical CVEs in production           | 0                                        | Trivy/Grype scan results             |
| Falco rule coverage                   | All critical runtime threats covered     | Rule audit against threat model      |
| OSQuery fleet coverage                | 100% of hosts running OSQuery            | Host inventory vs OSQuery deployment |
| Network policy coverage               | 100% of services have network policies   | Kubernetes NetworkPolicy audit       |
| Anomaly detection false positive rate | <5%                                      | Alert accuracy analysis              |
| Security event correlation accuracy   | >90% true positive rate                  | Incident correlation analysis        |
| SBOM completeness                     | 100% of images have SBOMs                | Registry SBOM inventory              |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
