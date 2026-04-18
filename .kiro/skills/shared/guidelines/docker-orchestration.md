---
name: docker-orchestration
description: Docker container orchestration, multi-container deployment patterns, and container lifecycle management for application deployment.
---

# Docker Orchestration

## Overview

This skill covers Docker container orchestration, multi-container deployment patterns, and container lifecycle management for application deployment. It is used by full-stack engineers during Stage 5 (Development) for containerized application deployment and Stage 7 (Testing) for test environment provisioning.

## Docker Compose for Development

```yaml
version: "3.8"
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://app:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]

volumes:
  pgdata:
```

## Multi-Stage Dockerfile

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=true --ignore-scripts
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

## Container Security

- **Non-root user**: Always run containers as non-root (`USER node`).
- **Minimal base image**: Use `-alpine` or `-slim` variants; avoid `latest` tag.
- **Image scanning**: Trivy or Snyk scan in CI pipeline — fail on CRITICAL/HIGH CVEs.
- **Read-only filesystem**: Mount writable volumes only where needed.
- **Resource limits**: Set CPU and memory limits to prevent resource starvation.
- **No secrets in images**: Use Docker secrets, environment variables from secret manager, or mounted volumes.

## Container Lifecycle Management

- **Health checks**: Every service must define a health check endpoint.
- **Graceful shutdown**: Handle SIGTERM, drain connections, flush buffers, exit within 30 seconds.
- **Log management**: Structured logging (JSON), log rotation, centralized log aggregation.
- **Image tagging**: `major.minor.patch` for releases, `git-sha` for CI builds.
