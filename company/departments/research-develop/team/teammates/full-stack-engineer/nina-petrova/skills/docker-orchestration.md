---
name: docker-orchestration
description: Build optimized Docker images and orchestrate multi-container workloads for development and staging environments — using multi-stage builds, Docker Compose for local development, and preparing images for ECS Fargate deployment.
version: "1.0.0"
---

# Docker Orchestration

| Competency         | Description                                                            | Quality Criteria                                                                                                               |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Multi-Stage Builds | Write multi-stage Dockerfiles for minimal production images            | Final image uses distroless or slim base; no build tools in production image; image size ≤ 200 MB for API services             |
| Docker Compose     | Design Docker Compose configurations for complete local dev stacks     | `docker compose up` starts a complete development environment with all dependencies; hot reload configured for all services    |
| Image Security     | Scan Docker images for CVEs and apply least-privilege container config | `trivy image` runs in CI; Critical CVEs block deployment; container runs as non-root user; read-only filesystem where possible |
| ECS-Ready Images   | Produce images configured for ECS Fargate deployment                   | Health check defined in Dockerfile; environment config via env vars (12-factor); logging to stdout/stderr only                 |

## Execution Guidance

### Multi-Stage Dockerfile Pattern

```dockerfile
# Build stage — includes build tools
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server ./cmd/server

# Production stage — minimal runtime
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/server /server
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Docker Compose Local Stack

```yaml
services:
  api:
    build: .
    ports: ["8080:8080"]
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user"]
      interval: 5s
      retries: 5
```
