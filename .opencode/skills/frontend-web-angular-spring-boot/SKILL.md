---
name: frontend-web-angular-spring-boot
description: Angular + Spring Boot full-stack development — Angular standalone components with signals, Spring Boot REST controllers, JPA/Hibernate entity mapping, Spring Security OAuth2/JWT, and Docker multi-stage builds. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 5 (Development) for enterprise full-stack implementation. Trigger: angular spring boot, java angular, spring security, jpa hibernate, oauth2 angular, docker spring boot.
prerequisites:
  - frontend-web-angular-signals

version: "1.0.0"
---

# Angular + Spring Boot

**Category:** Full-Stack Engineering (Java/Angular)
**Owner:** Full-Stack Engineer (Diego Morales)

## Overview

Delivers enterprise full-stack applications using Angular frontend with Spring Boot backend, covering Angular component architecture with signals and standalone components, Spring Boot REST controllers with exception handling, JPA/Hibernate entity mapping with relationships, Spring Security with OAuth2 and JWT authentication, and Docker deployment with multi-stage builds.

## Competency Dimensions

| Dimension                      | Description                                                                     | Proficiency Indicators                                                                                                                                                       |
| ------------------------------ | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Angular Component Architecture | Standalone components, signals, input/output, lifecycle, change detection       | Uses standalone components (no NgModules); leverages signals for reactive state; implements OnPush change detection; designs component hierarchy with clear responsibilities |
| Spring Boot REST Controllers   | Request mapping, path variables, request bodies, validation, exception handling | Designs RESTful controllers with proper HTTP semantics; uses Bean Validation; implements global exception handling with @ControllerAdvice                                    |
| JPA/Hibernate Entity Mapping   | Entity relationships, fetch strategies, cascade types, optimistic locking       | Designs entity graphs with correct fetch types (LAZY vs EAGER); implements optimistic locking with @Version; avoids N+1 queries with @EntityGraph                            |
| Spring Security                | OAuth2 resource server, JWT validation, method security, CORS configuration     | Configures Spring Security for JWT-based auth; implements @PreAuthorize method security; configures CORS for Angular frontend                                                |
| Docker Deployment              | Multi-stage builds, layer optimization, health checks, non-root user            | Writes production Dockerfiles with multi-stage builds; optimizes image layers; configures health checks; runs as non-root user                                               |

## Pipeline Integration

**Stage 5 (Development):** Angular components use standalone architecture with signals. Spring Boot controllers follow RESTful conventions. JPA entities configured with correct fetch strategies. Security configured with JWT validation.

**Stage 6 (Code Review):** Review component architecture for proper separation. Validate entity fetch strategies (no EAGER on collections). Check security configuration. Verify DTO mapping completeness.

**Stage 7 (Testing):** Angular component tests with signals. Spring Boot integration tests with @DataJpaTest and @WebMvcTest. Security tests for authorization rules.

## Quality Standards

| Metric               | Target                                         | Measurement             |
| -------------------- | ---------------------------------------------- | ----------------------- |
| Component standalone | 100% new components are standalone             | Code review             |
| Signal usage         | 100% reactive state uses signals               | Code review             |
| JPA fetch strategy   | 0 EAGER collections                            | Static analysis         |
| N+1 query prevention | All list queries use EntityGraph or JOIN FETCH | Query count monitoring  |
| Security coverage    | All endpoints have authorization               | Security audit          |
| Docker image size    | < 200MB for backend, < 50MB for frontend       | Image size check        |
| Health check         | All services have health endpoints             | Health check monitoring |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
