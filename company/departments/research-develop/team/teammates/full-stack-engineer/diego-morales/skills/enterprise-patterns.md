---
version: "1.0.0"
---

# Enterprise Patterns

-------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repository Pattern | Spring Data JPA repositories, custom queries, specification pattern, pagination | Designs repository interfaces with type-safe queries; uses Specification for dynamic queries; implements custom repository fragments for complex operations |
| Service Layer Architecture | Transaction management, business logic organization, dependency injection, facade pattern | Designs services with clear transaction boundaries; uses @Transactional appropriately; implements facade pattern for complex workflows |
| DTO/Entity Mapping | MapStruct configuration, nested mapping, collection mapping, custom mappers | Configures MapStruct with compile-time code generation; handles bidirectional relationships; implements custom type mappers |
| Validation Chains | Hibernate Validator, custom validators, group validation, cross-field validation | Builds validation chains with group sequences; implements custom constraint validators; validates cross-field dependencies |
| Audit Logging | Entity listeners, @CreatedDate/@LastModifiedDate, audit trail tables, soft deletes | Implements audit fields automatically via entity listeners; maintains separate audit trail for sensitive operations; implements soft delete pattern |

## Pipeline Integration

**Stage 5 (Development):** Repository interfaces use Specification for dynamic queries. Service layer has clear transaction boundaries. MapStruct mappers compile-time generated. Validation chains cover all request DTOs. Audit logging automatic via entity listeners.

**Stage 6 (Code Review):** Review transaction boundary correctness (no long-running transactions). Validate MapStruct mapper completeness. Check validation chain coverage. Verify audit logging on sensitive entities.

**Stage 7 (Testing):** Repository tests with @DataJpaTest. Service tests with @Transactional. Validation tests for all constraint violations. Audit log verification tests.

## Quality Standards

| Metric                       | Target                                 | Measurement                   |
| ---------------------------- | -------------------------------------- | ----------------------------- |
| Repository pattern usage     | 100% data access through repositories  | Code review                   |
| Transaction boundary clarity | All write methods have @Transactional  | Code review + static analysis |
| MapStruct mapping coverage   | 100% DTO/Entity mapping via MapStruct  | Code review                   |
| Validation coverage          | 100% request DTOs validated            | Validation test coverage      |
| Audit trail coverage         | 100% sensitive entities audited        | Entity listener audit         |
| N+1 query prevention         | 0 N+1 queries in production            | Query count monitoring        |
| Soft delete implementation   | All deletable entities use soft delete | Code review                   |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
