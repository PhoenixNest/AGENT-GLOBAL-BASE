# Level Definitions: L1 vs L2

## Level Definitions: L1 vs L2

### When L1 is Sufficient

| Application Type                 | Rationale                                                            |
| -------------------------------- | -------------------------------------------------------------------- |
| Content/consumer apps            | No sensitive user data, no financial transactions                    |
| Utility apps (calculator, notes) | Minimal attack surface, no network communication with sensitive data |
| Entertainment/gaming apps        | Low regulatory exposure, no PII handling                             |
| Internal tools (non-sensitive)   | Limited data sensitivity, controlled user population                 |

**L1 control set:** All V1 through V7 controls. V8 is not required.

### When L2 is Mandatory

| Application Type       | Rationale                                        | Mandatory Controls              |
| ---------------------- | ------------------------------------------------ | ------------------------------- |
| Banking/financial apps | Regulatory compliance, financial data protection | All V1-V8 + MASVS-R recommended |
| Healthcare apps        | HIPAA, sensitive health data                     | All V1-V8                       |
| Government services    | Official data handling, public trust             | All V1-V8                       |
| Enterprise SSO         | Corporate credential handling                    | All V1-V8 + MASVS-R recommended |
| Payment processing     | PCI-DSS compliance                               | All V1-V8 + MASVS-R recommended |
| PII at scale           | GDPR, CCPA compliance                            | All V1-V8                       |

**L2 control set:** All V1 through V8 controls. MASVS-R is recommended but determined by CSO during Stage 1.

### L2-Selected Controls for Sensitive Applications

For applications that exceed standard L2 requirements, the CSO may select additional controls:

| Additional Control                | Applicability                                     |
| --------------------------------- | ------------------------------------------------- |
| MASVS-R.1 (RASP)                  | High-value target applications                    |
| MASVS-R.2 (Anti-dynamic-analysis) | Applications with proprietary algorithms          |
| MASVS-R.3 (Anti-repackaging)      | Applications targeting regions with high piracy   |
| MASVS-R.4 (Anti-emulator)         | Applications with location-based fraud prevention |

---
