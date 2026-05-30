---
name: data-protection-compliance
description: Conduct Data Protection Impact Assessments (DPIA), select and implement cross-border data transfer mechanisms, analyse data residency obligations, and maintain the organisation's privacy compliance documentation.
version: "1.0.0"
---

# Data Protection Compliance

| Competency                   | Description                                                                | Quality Criteria                                                                                   |
| ---------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| DPIA Methodology             | Conduct full DPIAs for new products, features, and data processing changes | DPIA completed before processing begins for high-risk activities; Dutch DPA-compatible methodology |
| Transfer Mechanism Selection | Select and implement the appropriate cross-border transfer mechanism       | Mechanism selected is legally valid in both source and destination jurisdictions                   |
| Data Residency Analysis      | Map data flows and identify residency obligations for each data category   | All personal data flows mapped; residency obligations documented per jurisdiction                  |
| Compliance Documentation     | Maintain Records of Processing Activities (RoPA), privacy notices, DPAs    | RoPA current; privacy notices reviewed after any material processing change                        |

## Execution Guidance

### DPIA Trigger Assessment

A DPIA is required when processing is **likely to result in high risk**. Always conduct a DPIA for:

- [ ] Systematic surveillance of public spaces (e.g., transit monitoring systems)
- [ ] Large-scale processing of sensitive personal data
- [ ] Automated decision-making with legal or similarly significant effects
- [ ] Profiling of individuals at scale
- [ ] Innovative technology with novel privacy risks
- [ ] Any processing that combines datasets in ways that could reveal additional information

### DPIA Structure

```
1. Description of Processing
   ├── Purpose and legal basis
   ├── Data categories and subjects
   ├── Data flows (collection → storage → processing → transfer → deletion)
   └── Retention periods

2. Necessity and Proportionality Assessment
   ├── Is the purpose achievable with less data?
   ├── Is the retention period proportionate?
   └── Is processing limited to what is necessary?

3. Risk Assessment
   ├── Risk 1: [Description] → Likelihood × Severity → Residual Risk after mitigation
   ├── Risk 2: ...
   └── Risk N: ...

4. Mitigation Measures
   ├── Technical controls (encryption, pseudonymisation, access controls)
   ├── Organisational controls (policies, training, DPA with processors)
   └── Legal controls (SCCs, adequacy, DPIA re-review trigger)

5. Consultation
   ├── Data subjects consulted? Y/N
   ├── DPA consultation required? Y/N (required if residual risk remains high)
   └── Approval: CLO sign-off required before high-risk processing begins
```

### Data Residency Decision Matrix

| Data Category               | Jurisdiction | Localisation Required? | Permitted Transfer Mechanism        |
| --------------------------- | ------------ | ---------------------- | ----------------------------------- |
| Transit passenger flow data | Indonesia    | Yes (GR 71 / GR 80)    | None — must be processed in-country |
| Financial transaction data  | China        | Yes (PIPL)             | Security Assessment or SCCs + PIPL  |
| General personal data       | EU           | No                     | SCCs or adequacy decision           |
| Biometric data              | Thailand     | Consent required       | Consent + contractual safeguards    |
