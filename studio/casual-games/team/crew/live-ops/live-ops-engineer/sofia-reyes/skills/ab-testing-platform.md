---
name: ab-testing-platform
description: A/B testing infrastructure design, experiment management, statistical analysis, and feature flag integration for live games.
version: "1.0.0"
---

# A/B Testing Platform

## Overview

This skill covers the design, implementation, and operation of A/B testing infrastructure for live mobile games, including randomization, experiment management, statistical analysis, and feature flag integration.

## Core Architecture

```
Game Client → Event SDK → Kafka → Flink (stream processing) → ClickHouse (real-time)
                                                      → S3 (batch analysis)
                                                      → Experiment Dashboard
```

### Randomization Service

| Method            | Use Case                      | Implementation                       |
| ----------------- | ----------------------------- | ------------------------------------ |
| Consistent Hash   | Stable bucket assignment      | MurmurHash3(player_id) % num_buckets |
| Server-side eval  | Experiment-aware flag values  | Redis cache for bucket → variant map |
| Client-side cache | Offline experiment enrollment | Local bucket assignment with TTL     |

### Statistical Analysis Engine

| Test Type            | Method                  | Guardrails                       |
| -------------------- | ----------------------- | -------------------------------- |
| Binary metrics       | Proportion Z-test       | Min sample size: 50K per variant |
| Continuous metrics   | Welch's t-test          | Normality check (Shapiro-Wilk)   |
| Multiple comparisons | Bonferroni correction   | Family-wise error rate ≤ 0.05    |
| Sequential testing   | Alpha spending function | O'Brien-Fleming boundaries       |

### Feature Flag Integration

- Flags can be scoped to experiment variants (e.g., `new_ui` flag evaluates differently for control vs. treatment)
- Experiment-aware evaluation prevents flag conflicts when multiple experiments run simultaneously
- Gradual rollout integrated with experiment enrollment (ramp up both simultaneously)
