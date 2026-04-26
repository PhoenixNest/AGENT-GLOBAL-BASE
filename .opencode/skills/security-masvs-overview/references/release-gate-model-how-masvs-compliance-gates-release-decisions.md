# Release Gate Model: How MASVS Compliance Gates Release Decisions

## Release Gate Model: How MASVS Compliance Gates Release Decisions

### P0 Defects for MASVS Non-Compliance

The following conditions are classified as **P0 defects** (non-negotiable release blockers):

| Condition                                                    | MASVS Reference | Rationale                            |
| ------------------------------------------------------------ | --------------- | ------------------------------------ |
| Any mandatory L1 control fails verification                  | V1-V7           | Baseline security is not met         |
| Any mandatory L2 control fails verification                  | V1-V8           | Defense-in-depth is not met          |
| Cleartext transmission of sensitive data                     | V5.1, V5.4      | Data interception risk               |
| Hardcoded credentials or cryptographic keys                  | V4.5, V3.2      | Immediate compromise vector          |
| Custom TLS certificate validation accepting all certificates | V5.2            | Man-in-the-middle vulnerability      |
| Sensitive data in application logs (release build)           | V2.4            | Data exfiltration via logcat/Console |
| No biometric fallback security                               | V4.3            | Authentication bypass                |
| Missing root/jailbreak detection for L2 app                  | V8.5            | Defense-in-depth failure             |

### Release Blocking Criteria

A release is **blocked** if any of the following are true:

| Criterion                                                                             | Description                    |
| ------------------------------------------------------------------------------------- | ------------------------------ |
| Any P0 MASVS defect exists                                                            | Non-negotiable — must be fixed |
| Any P1 MASVS defect exists                                                            | Non-negotiable — must be fixed |
| MASVS compliance matrix has any "Fail" on mandatory controls                          | Equivalent to P0               |
| MASVS compliance matrix has unresolved "Partial" on mandatory controls (user decides) | P2 — user may defer            |
| External assessor (if engaged) issues non-compliant determination                     | P0 — must be remediated        |

### Exception Process

MASVS exceptions follow this process:

| Step | Action                                                                          | Authority              |
| ---- | ------------------------------------------------------------------------------- | ---------------------- |
| 1    | CSO identifies a control that cannot be implemented due to technical constraint | CSO                    |
| 2    | CSO documents exception request with risk assessment and compensating controls  | CSO                    |
| 3    | CTO + CPO review exception request                                              | CTO + CPO              |
| 4    | User approves or rejects exception                                              | User (final authority) |
| 5    | If approved, exception is documented in SRD addendum                            | CSO                    |
| 6    | Exception is re-reviewed at each release cycle                                  | CSO                    |

**Important:** Exceptions are **rare and temporary**. An exception for one release does not grant a permanent waiver. The CSO must re-evaluate at each release cycle.

---
