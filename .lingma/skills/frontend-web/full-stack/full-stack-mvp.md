---
name: full-stack-mvp
description: Delivers minimum viable products rapidly using React + Node.js + PostgreSQL stack with Docker Compose for local development, feature flag strategies for controlled rollouts.
---

# Full-Stack MVP Development

**Category:** Full-Stack Engineering
**Owner:** Full-Stack Engineer (Nina Petrova)

## Overview

Delivers minimum viable products rapidly using React + Node.js + PostgreSQL stack with Docker Compose for local development, feature flag strategies for controlled rollouts, MVP scoping frameworks for requirement prioritization, and end-to-end delivery pipelines from prototype to production. Balances speed with production-readiness.

## Competency Dimensions

| Dimension               | Description                                                                           | Proficiency Indicators                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Rapid Prototyping       | React + Node.js + PostgreSQL stack, scaffold generation, boilerplate patterns         | Sets up full-stack project in < 1 hour; implements CRUD operations end-to-end; deploys to staging environment                 |
| Docker Compose          | Multi-service orchestration, volume management, network configuration, health checks  | Writes docker-compose.yml for local development with app, database, and cache services; configures hot-reload for development |
| Feature Flag Strategies | LaunchDarkly, OpenFeature, rollout percentages, user targeting, kill switches         | Implements feature flags for gradual rollout; designs kill switches for emergency disable; tracks flag usage and cleanup      |
| MVP Scoping             | MoSCoW prioritization, user story mapping, scope negotiation, technical debt tracking | Distills PRD into MVP scope; identifies must-have vs nice-to-have; documents deferred items for future iterations             |
| End-to-End Delivery     | CI/CD pipeline, staging deployment, smoke testing, production promotion               | Configures CI/CD from commit to production; implements automated smoke tests; manages deployment rollbacks                    |

## Execution Guidance

### Rapid Full-Stack Scaffold

```
my-mvp/
├── docker-compose.yml          # Local development
├── .env.example
├── client/                     # React frontend
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/               # API client layer
│   │   │   ├── client.ts      # Axios/fetch wrapper
│   │   │   └── users.ts       # Resource-specific API
│   │   ├── components/        # Reusable UI
│   │   ├── pages/             # Route-level components
│   │   └── hooks/             # Custom React hooks
├── server/                     # Node.js backend
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── index.ts           # Express app entry
│   │   ├── routes/            # API routes
│   │   ├── services/          # Business logic
│   │   ├── repositories/      # Data access
│   │   └── middleware/        # Auth, validation, error handling
├── database/
│   ├── migrations/            # SQL migrations
│   └── seeds/                 # Seed data for development
└── infra/
    └── Dockerfile             # Production Dockerfiles
```

### Docker Compose for Local Development

```yaml
version: "3.8"

services:
  client:
    build:
      context: ./client
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./client:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://server:4000
    depends_on:
      server:
        condition: service_healthy
    command: npm run dev

  server:
    build:
      context: ./server
      dockerfile: Dockerfile.dev
    ports:
      - "4000:4000"
    volumes:
      - ./server:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://postgres:password@database:5432/mvp_dev
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=dev-secret-change-in-production
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: npm run dev
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4000/healthz"]
      interval: 10s
      timeout: 5s
      retries: 5

  database:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mvp_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  postgres_data:
```

### Feature Flag Implementation

```typescript
// Feature flag service (OpenFeature-compatible)
interface FeatureFlags {
  newDashboard: boolean;
  experimentalCheckout: boolean;
  darkModeBeta: boolean;
  maxUploadSizeMB: number;
}

class FeatureFlagService {
  private flags: Partial<FeatureFlags> = {};
  private userFlags: Map<string, Partial<FeatureFlags>> = new Map();

  // Initialize from remote config
  async initialize(userId?: string): Promise<void> {
    const response = await fetch('/api/flags', {
      headers: userId ? { 'X-User-ID': userId } : {},
    });
    this.flags = await response.json();
  }

  isEnabled(flag: keyof FeatureFlags, defaultValue: boolean = false): boolean {
    return this.flags[flag] ?? defaultValue;
  }

  getValue<T>(flag: keyof FeatureFlags, defaultValue: T): T {
    return (this.flags[flag] as T) ?? defaultValue;
  }

  // User-targeted flags
  isEnabledForUser(flag: keyof FeatureFlags, userId: string): boolean {
    const userFlag = this.userFlags.get(userId)?.[flag];
    return userFlag ?? this.isEnabled(flag);
  }
}

// Usage in React
const FeatureFlag: React.FC<{
  flag: keyof FeatureFlags;
  fallback?: React.ReactNode;
  children: React.ReactNode;
}> = ({ flag, fallback, children }) => {
  const flags = useFeatureFlags();

  if (!flags.isEnabled(flag)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
};

// Usage in component
function Dashboard() {
  const flags = useFeatureFlags();

  if (flags.isEnabled('newDashboard')) {
    return <NewDashboard />;
  }

  return <LegacyDashboard />;
}

// Server-side feature flag evaluation
// POST /api/flags/evaluate
// Body: { flag: 'experimentalCheckout', userId: 'user-123' }
// Response: { enabled: true, variant: 'B', rollout: 0.25 }

// Kill switch pattern
async function handleCheckout(req: Request, res: Response) {
  if (!featureFlags.isEnabled('experimentalCheckout')) {
    return res.redirect('/legacy-checkout');
  }

  try {
    // Experimental checkout logic
  } catch (error) {
    // Kill switch: disable flag on critical error
    await featureFlags.disable('experimentalCheckout');
    logger.error('Kill switch activated for experimentalCheckout', { error });
    return res.redirect('/legacy-checkout');
  }
}
```

### MVP Scoping Framework

**MoSCoW Prioritization:**

| Category        | Criteria                                      | MVP Inclusion              | Example                      |
| --------------- | --------------------------------------------- | -------------------------- | ---------------------------- |
| **Must Have**   | Core value proposition, cannot launch without | ✅ Included in MVP         | User registration, core CRUD |
| **Should Have** | Important but workaround exists               | ⚠️ Include if time permits | Email notifications          |
| **Could Have**  | Nice-to-have, no workarounds needed           | ❌ Deferred to v2          | Dark mode, animations        |
| **Won't Have**  | Out of scope for this iteration               | ❌ Explicitly excluded     | Multi-language support       |

**User Story Mapping for MVP:**

```
User Journey: Discover → Register → Browse → Purchase → Track
┌─────────────────────────────────────────────────────────────┐
│ Backbone (Activities)                                       │
├─────────────────────────────────────────────────────────────┤
│ Discover    │ Register      │ Browse    │ Purchase │ Track  │
├─────────────┼───────────────┼───────────┼──────────┼────────┤
│ Search      │ Email signup  │ List view │ Checkout │ Order  │
│ products    │ Password set  │ Detail    │ Payment  │ status │
├─────────────┼───────────────┼───────────┼──────────┼────────┤
│ Categories  │ Social login  │ Filters   │ Coupon   │ Email  │
│             │ SSO           │ Sort      │ codes    │ notify │
├─────────────┼───────────────┼───────────┼──────────┼────────┤
│ Recommend.  │ Phone verify  │ Wishlist  │ Split    │ SMS    │
│             │ 2FA setup     │ Compare   │ payment  │ notify │
└─────────────┴───────────────┴───────────┴──────────┴────────┘
  ← MVP slice ←  (first horizontal row only)
```

**Technical Debt Tracking for MVP:**

```markdown
# Technical Debt Register

| ID    | Debt Item                          | Reason    | Risk                             | Planned Fix     |
| ----- | ---------------------------------- | --------- | -------------------------------- | --------------- |
| TD-01 | No pagination on list endpoints    | MVP speed | Medium (degrades at >1K records) | Sprint 3        |
| TD-02 | Hardcoded email templates          | MVP speed | Low                              | Sprint 4        |
| TD-03 | No rate limiting on auth endpoints | MVP speed | High (security)                  | Sprint 2        |
| TD-04 | Single database instance           | Cost      | Medium                           | When >10K users |
```

### End-to-End Delivery Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy MVP
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: cd server && npm ci && npm test
      - run: cd client && npm ci && npm test && npm run build

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: docker compose -f docker-compose.staging.yml up -d
      - name: Smoke Test
        run: |
          curl -f https://staging.company.com/healthz
          curl -f https://staging.company.com/api/health

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          # Blue-green deployment
          docker compose -f docker-compose.prod.yml up -d --no-deps --scale app=2 app
          # Wait for health check
          sleep 30
          # Switch traffic
          docker compose -f docker-compose.prod.yml up -d --no-deps app
          # Smoke test
          curl -f https://api.company.com/healthz

  rollback:
    runs-on: ubuntu-latest
    if: failure()
    needs: [deploy-production]
    steps:
      - name: Rollback
        run: |
          # Rollback to previous image
          docker compose -f docker-compose.prod.yml up -d --no-deps app:${{ github.event.before }}
```

## Pipeline Integration

**Stage 4 (Implementation Plan):** MVP scope defined with MoSCoW prioritization. Technical debt items documented with planned fix timeline. Feature flag strategy defined for each major feature.

**Stage 5 (Development):** Docker Compose environment functional. All Must-Have features implemented. Feature flags wrap Should-Have features. CI/CD pipeline configured.

**Stage 6 (Code Review):** Review MVP scope completeness. Validate feature flag implementation. Check technical debt register accuracy. Verify Docker Compose reproducibility.

**Stage 10 (Release Readiness):** Panel confirms all Must-Have features implemented. Feature flags configured for controlled rollout. Rollback procedure tested.

## Quality Standards

| Metric                       | Target                              | Measurement            |
| ---------------------------- | ----------------------------------- | ---------------------- |
| MVP delivery time            | < 4 weeks from PRD to staging       | Project timeline       |
| Docker Compose setup         | < 5 minutes for new developer       | Onboarding measurement |
| Feature flag coverage        | 100% of experimental features       | Code review            |
| CI/CD pipeline               | < 10 minutes from commit to staging | Pipeline duration      |
| Smoke test pass rate         | 100% on deployment                  | Deployment logs        |
| Technical debt items tracked | 100% of known debt documented       | Debt register          |
