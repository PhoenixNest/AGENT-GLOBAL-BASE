---
version: "1.0.0"
---

| Competency                                  | Description                                                                                                                          | Quality Criteria                                                                                                                                              |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Class Diagrams                              | Classes, interfaces, relationships (association, aggregation, composition, inheritance), multiplicities, visibility, design patterns | Models domain entities with correct relationships; represents design patterns (Factory, Strategy, Observer) in UML; indicates multiplicities and navigability |
| Sequence Diagrams                           | Lifelines, activation bars, synchronous/asynchronous messages, return messages, alt/opt/loop fragments, self-messages                | Models complex interaction flows; represents async messaging correctly; uses combined fragments for conditional logic; shows error/exception paths            |
| Component Diagrams                          | Components, ports, interfaces (provided/required), dependencies, deployment nodes                                                    | Models system architecture with clear component boundaries; shows inter-component contracts; represents deployment topology                                   |
| PlantUML & Mermaid                          | Syntax mastery, styling, theming, macros, include files                                                                              | Writes production-quality diagrams; uses consistent styling; organizes complex diagrams with includes and macros; generates SVG/PNG output                    |
| Architecture-to-Implementation Traceability | UML element → code mapping, change propagation, validation                                                                           | Every UML element maps to a code artifact; changes in code trigger UML review; UML validated against implementation during code review                        |

## Class Diagram → Code

| UML Element                    | Code Location                                | Verified |
| ------------------------------ | -------------------------------------------- | -------- |
| `User` class                   | `server/src/models/user.ts`                  | ✅       |
| `Order` class                  | `server/src/models/order.ts`                 | ✅       |
| `OrderItem` class              | `server/src/models/order-item.ts`            | ✅       |
| `IRepository<T>` interface     | `server/src/repositories/base.ts`            | ✅       |
| `UserRepository`               | `server/src/repositories/user-repository.ts` | ✅       |
| `OrderService`                 | `server/src/services/order-service.ts`       | ✅       |
| Composition: Order → OrderItem | `Order.items` cascade: all                   | ✅       |

## Sequence Diagram → Code

| Interaction                | Code Location                                 | Verified |
| -------------------------- | --------------------------------------------- | -------- |
| `POST /api/orders`         | `server/src/routes/orders.ts:42`              | ✅       |
| `Inventory.reserveStock()` | `server/src/services/inventory-service.ts:88` | ✅       |
| `Payment.processPayment()` | `server/src/services/payment-service.ts:156`  | ✅       |
| Kafka: OrderCreated event  | `server/src/events/order-events.ts:23`        | ✅       |

## Component Diagram → Infrastructure

| Component           | Infrastructure              | Verified |
| ------------------- | --------------------------- | -------- |
| API Gateway (Envoy) | `infra/gateway/envoy.yaml`  | ✅       |
| PostgreSQL Primary  | `infra/database/primary.tf` | ✅       |
| Redis Cache         | `infra/cache/redis.tf`      | ✅       |
| Kafka Cluster       | `infra/messaging/kafka.tf`  | ✅       |

```

**Validation process:**

```

1. UML diagrams authored during Stage 3
2. Implementation begins in Stage 4/5
3. Code review (Stage 6) validates:
   a. All UML classes have corresponding code artifacts
   b. Relationships match implementation (composition vs aggregation)
   c. Sequence flows match actual service interactions
   d. Component boundaries match deployment units
4. Discrepancies logged and resolved:
   a. If code differs from UML → Update UML or code
   b. If UML has elements not in code → Remove from UML or implement
   c. If code has elements not in UML → Add to UML
5. Integrity verification (Stage 8) final validation

```

## Pipeline Integration

**Stage 3 (UML Engineering Package):** UML diagrams are primary deliverable. Class diagrams show domain model and architecture. Sequence diagrams show critical flows. Component diagrams show system topology. All diagrams in PlantUML or Mermaid format.

**Stage 4 (Implementation Plan):** Implementation tasks trace back to UML elements. Each class, service, and component mapped to implementation tasks.

**Stage 6 (Code Review):** Code review validates implementation against UML. Discrepancies documented and resolved. UML updated if implementation diverges.

**Stage 8 (Integrity Verification):** Final traceability validation. All UML elements have corresponding implementation. All implementation elements documented in UML.

## Quality Standards

| Metric                        | Target                                    | Measurement            |
| ----------------------------- | ----------------------------------------- | ---------------------- |
| Diagram coverage              | 100% of domain entities in class diagrams | UML audit              |
| Sequence diagram completeness | All critical flows documented             | Flow audit             |
| Component diagram accuracy    | Matches production topology               | Infrastructure audit   |
| Traceability completeness     | 100% UML elements mapped to code          | Traceability matrix    |
| Diagram syntax validity       | 0 PlantUML/Mermaid compilation errors     | CI validation          |
| UML-code consistency          | 0 discrepancies at Stage 8                | Integrity verification |


---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
```
