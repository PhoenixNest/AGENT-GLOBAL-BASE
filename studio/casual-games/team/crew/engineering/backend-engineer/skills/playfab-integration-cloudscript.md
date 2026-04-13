# PlayFab Integration & Cloud Script

**Skill Owner:** Aisha Bello | **Version:** 1.0 | **Date:** 2026-04-20

## Description

PlayFab SDK integration, Cloud Script development in C#, API wrapper design conforming to interface contracts, and PlayFab Events → Kafka data export pipeline.

## Tools & Frameworks

| Tool            | Version | Context                                       |
| --------------- | ------- | --------------------------------------------- |
| PlayFab SDK     | v2.17   | Authentication, Economy, Cloud Script, Events |
| C#              | 11.0    | Cloud Script functions; API wrappers          |
| Azure Functions | v4      | Serverless Cloud Script execution             |
| Apache Kafka    | 3.5     | Event streaming for analytics pipeline        |
| NUnit           | 3.13    | Unit testing for Cloud Script functions       |

## Production Scenarios

**Scenario 1: PlayFab SDK Integration (Space Ape 2024)** — Integrated PlayFab SDK for 3 live titles including authentication, economy, and cloud script. Result: All titles shipped on schedule; zero critical PlayFab-related bugs.
**Scenario 2: Events → Kafka Pipeline (Space Ape 2024)** — Built real-time data export from PlayFab Events to Kafka for analytics team. Result: Analytics data latency reduced from hours to seconds; enabled real-time dashboards.

## Trade-offs

- Cloud Script vs dedicated backend → Cloud Script for speed; dedicated for complex logic
- Direct SDK calls vs wrapper → wrapper for testability and future migration

## Quality Standards

- Cloud Script execution: ≤ 5s per invocation
- API wrapper test coverage: ≥ 80%
- Data pipeline latency: ≤ 30s from event to Kafka
- Interface contract compliance: 100% of defined methods

## References

PlayFab documentation; Azure Functions best practices; Kafka consumer guidelines
