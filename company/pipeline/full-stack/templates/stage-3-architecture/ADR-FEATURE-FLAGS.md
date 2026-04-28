# ADR: Feature Flag Strategy (Cross-Platform)

| Field         | Value                                                                   |
| ------------- | ----------------------------------------------------------------------- |
| **Status**    | Proposed                                                                |
| **Context**   | Stage 3 — Full-Stack Cross-Platform Pipeline (P3)                       |
| **Decision**  | LaunchDarkly with cross-platform flag taxonomy and kill switch protocol |
| **Date**      | YYYY-MM-DD                                                              |
| **Authors**   | CIO (primary), CTO, All Platform Leads                                  |
| **Reviewers** | CSO, CPO                                                                |

---

## Decision

We will use **LaunchDarkly** as the primary feature flag service with Unleash as backup. Flags will support real-time propagation (<1 second), staggered rollouts per platform, and emergency kill switches (<1 minute disable time).

## Rationale

Full-stack cross-platform products require coordinated feature releases across web, iOS, Android, and backend. Feature flags enable gradual rollouts, A/B testing, kill switches for problematic features, and platform-specific release timing. Without unified feature flag governance, inconsistencies arise: a feature enabled on web but broken on iOS, or a kill switch activated on backend but not propagated to mobile clients. This ADR establishes cross-platform feature flag standards.

### 1. Feature Flag Platform: LaunchDarkly (Primary) with Unleash (Backup)

**Primary Platform:** LaunchDarkly

**Rationale:**

- **Cross-platform SDKs** — Native SDKs for JavaScript (web), Swift (iOS), Kotlin (Android), Go/Node.js/Java (backend)
- **Real-time updates** — Flags propagate to all platforms within seconds (no app update required)
- **Targeting rules** — Enable flags for specific user segments (beta testers, EU users, premium tier)
- **Audit trail** — Complete history of flag changes (who changed what, when, why)
- **Kill switch** — Instantly disable feature across all platforms if critical bug discovered

**Backup Platform:** Unleash (open-source alternative)

**Use Case:** Disaster recovery if LaunchDarkly experiences outage; self-hosted option for data sovereignty requirements.

---

### 2. Flag Taxonomy & Naming Convention

**Naming Format:** `{platform}.{feature}.{variant}`

**Examples:**

- `web.checkout.new-payment-flow` — Web-only checkout feature
- `mobile.ios.home-screen.redesign` — iOS-specific home screen
- `mobile.android.offline-mode.v2` — Android offline mode improvement
- `backend.api.rate-limiting.strict` — Backend API rate limiting adjustment
- `all.recommendations.ml-v2` — Cross-platform ML recommendation engine

**Flag Types:**

| Type            | Scope      | Use Case                                             | Rollout Strategy           |
| --------------- | ---------- | ---------------------------------------------------- | -------------------------- |
| Release flag    | Short-term | Gradual rollout of new feature                       | 1% → 5% → 25% → 50% → 100% |
| Experiment flag | Short-term | A/B test (control vs. variant)                       | 50% control, 50% variant   |
| Ops flag        | Long-term  | Operational controls (rate limits, maintenance mode) | Manual toggle as needed    |
| Permission flag | Long-term  | Feature gating by user tier (free vs. premium)       | Based on user attribute    |

---

### 3. Cross-Platform Flag Synchronization

**Challenge:** Backend enables flag, but mobile clients cache old flag state → inconsistent behavior.

**Solution:** Real-time flag propagation with fallback strategies.

**Propagation Mechanism:**

#### Web: Server-Side Rendering (SSR) + Client-Side SDK

```javascript
// SSR: Inject initial flag state into HTML
const flags = await launchdarkly.allFlagsState(user);
res.render('page', { flags });

// Client-side: Subscribe to real-time updates
ldClient.on('change', (updates) => {
  if (updates['web.checkout.new-payment-flow']) {
    // Re-render checkout component with new flag state
    refreshCheckoutUI();
  }
});
```

#### Mobile: Background Sync + Local Cache

```swift
// iOS: Fetch flags on app launch + periodic background refresh
LDConfig *config = [[LDConfig alloc] initWithMobileKey:@"mobile-key"];
config.backgroundUpdatesEnabled = YES;
config.flagPollingInterval = 300; // 5 minutes

[LDClient startWithConfiguration:config user:user];

// Listen for flag changes
[[NSNotificationCenter defaultCenter] addObserver:self
                                         selector:@selector(flagsChanged:)
                                             name:kLDFlagsChangeNotification
                                           object:nil];
```

```kotlin
// Android: WorkManager for background sync
val config = LDConfig.Builder()
    .backgroundPollingIntervalMillis(300_000) // 5 minutes
    .build()

LDClient.init(applicationContext, config, user)

// Observe flag changes
ldClient.observe("mobile.ios.home-screen.redesign") { newValue ->
    if (newValue.asBool() == true) {
        // Reload home screen with new design
        reloadHomeScreen()
    }
}
```

#### Backend: In-Memory Cache + Webhook Notifications

```go
// Go: Initialize LD client with streaming mode
client, _ := ld.MakeClient("sdk-key", 5*time.Second)

// Check flag value
showNewFeature, _ := client.BoolVariation("backend.api.new-endpoint", user, false)

if showNewFeature {
    // Enable new endpoint logic
}

// Webhook: Receive real-time flag change notifications
http.HandleFunc("/ld-webhook", func(w http.ResponseWriter, r *http.Request) {
    // Parse webhook payload, invalidate local cache
    invalidateFlagCache()
})
```

**Fallback Strategy:**
If LaunchDarkly SDK fails to initialize or network unreachable:

1. Use locally cached flag state (last known good values)
2. If no cache exists, use default values (feature disabled)
3. Log error to observability system (OpenTelemetry trace)
4. Retry connection every 30 seconds

---

### 4. Kill Switch Protocol

**Scenario:** Critical bug discovered in production (e.g., payment processing failure affecting 10% of users).

**Kill Switch Procedure:**

1. **Immediate action (<1 minute):**
   - CTO or designated on-call engineer disables flag in LaunchDarkly dashboard
   - Flag propagates to all platforms within 5-30 seconds (real-time update)
   - Monitoring alerts confirm flag change propagated (Grafana dashboard)

2. **Verification (1-5 minutes):**
   - Check error rate drops back to baseline
   - Verify no residual impact (cached flag states on mobile devices)
   - Communicate status to stakeholders (Slack #incident channel)

3. **Post-mortem (within 24 hours):**
   - Root cause analysis
   - Determine if flag can be re-enabled (after fix) or must remain disabled
   - Update runbook with lessons learned

**Kill Switch Authority:**

- **P0 incidents:** CTO, VP Engineering, or on-call engineer (immediate action)
- **P1 incidents:** Platform lead + CTO approval (within 15 minutes)
- **P2/P3 incidents:** Platform lead discretion (within 1 hour)

---

### 5. Staggered Rollout Coordination

**Scenario:** New checkout flow launches across web, iOS, Android simultaneously.

**Rollout Strategy:**

| Day    | Web Rollout | iOS Rollout | Android Rollout | Backend API | Notes                             |
| ------ | ----------- | ----------- | --------------- | ----------- | --------------------------------- |
| Day 1  | 1%          | 0%          | 0%              | 100%        | Test web first (easiest rollback) |
| Day 2  | 5%          | 1%          | 0%              | 100%        | Monitor web metrics               |
| Day 3  | 25%         | 5%          | 1%              | 100%        | Expand web, start iOS             |
| Day 5  | 50%         | 25%         | 5%              | 100%        | All platforms at 50%+             |
| Day 7  | 100%        | 50%         | 25%             | 100%        | Web complete, continue mobile     |
| Day 10 | 100%        | 100%        | 50%             | 100%        | iOS complete                      |
| Day 14 | 100%        | 100%        | 100%            | 100%        | All platforms complete            |

**Per-Platform Go/No-Go Authority:**

- **Web:** Frontend Lead (Amira Voss)
- **iOS:** iOS Lead (Seo-Yeon Park)
- **Android:** Android Lead (Kofi Asante-Mensah)
- **Backend:** Backend Lead (Dev Malhotra)
- **Overall coordination:** CTO (Dr. Kenji Nakamura)

**Rollback Criteria:**

- Error rate increases >2x baseline
- P99 latency exceeds SLA by >50%
- User complaints spike (>10 support tickets/hour)
- Revenue impact detected (conversion rate drops >5%)

---

### 6. Environment Parity

**Rule:** Dev, staging, and production environments must have matching flag configurations (except for rollout percentages).

**Enforcement:**

- CI gate: Compare flag configurations across environments before deployment
- Alert: Slack notification if production flag differs from staging by >10%
- Exception: Production rollout percentages intentionally differ (staging = 100% for testing)

**Example Violation:**

```
Staging: web.checkout.new-payment-flow = 100%
Production: web.checkout.new-payment-flow = 5%
→ ALERT: Production rollout <10%, verify intentional
```

---

## Alternatives Considered

### Alternative 1: Custom-Built Feature Flag System

**Pros:** Full control, no vendor dependency, lower cost at small scale  
**Cons:** Months of development effort, ongoing maintenance burden, lack of advanced features (targeting, audit trail)  
**Rejected because:** LaunchDarkly provides enterprise-grade features out-of-the-box; build-vs-buy analysis favors SaaS solution.

### Alternative 2: Configuration Files (No Dynamic Flags)

**Pros:** Simple, no external dependencies  
**Cons:** Requires app update to change flag state (days/weeks for mobile), no real-time control, no targeting rules  
**Rejected because:** Violates requirement for "instant kill switch capability"; mobile app store review process makes configuration files impractical for urgent fixes.

### Alternative 3: Database-Backed Flags

**Pros:** Full control, no vendor lock-in  
**Cons:** Polling overhead (mobile battery drain), complex synchronization logic, no real-time updates  
**Rejected because:** LaunchDarkly's streaming SDKs provide real-time updates with minimal overhead; reinventing this wheel is unjustified.

---

## Consequences

### Positive

- **Instant kill switch** — Disable problematic feature across all platforms in <1 minute
- **Gradual rollouts** — Reduce blast radius of bugs by limiting initial exposure to 1% of users
- **A/B testing** — Data-driven feature decisions with statistical significance
- **Platform-specific control** — Enable feature on web while keeping it disabled on iOS (if iOS-specific bug exists)

### Negative

- **Vendor dependency** — LaunchDarkly outage impacts ability to toggle flags (mitigated by local cache fallback)
- **Cost** — $15/user/month × 50 engineers = $750/month (acceptable within engineering budget)
- **Complexity** — Engineers must understand flag lifecycle (create, test, rollout, retire); training required

### Risks & Mitigations

| Risk                               | Likelihood | Impact   | Mitigation                                                                                             |
| ---------------------------------- | ---------- | -------- | ------------------------------------------------------------------------------------------------------ |
| Flag sprawl (too many flags)       | High       | Medium   | Quarterly flag audit, auto-expire flags after 90 days, max 50 active flags per service                 |
| Stale cached flags on mobile       | Medium     | High     | Force flag refresh on app launch, background sync every 5 minutes, clear cache on major version update |
| Kill switch causes cascade failure | Low        | Critical | Test kill switch in staging before production, ensure graceful degradation (not hard crash)            |
| Flag misconfiguration              | Medium     | High     | Require peer review for flag changes, automated tests verify flag behavior in staging                  |

---

## Implementation Plan

**Phase 1 (Week 1-2):** LaunchDarkly setup

- Create LaunchDarkly account, configure projects (web, iOS, Android, backend)
- Set up SDK integrations for all platforms
- Define initial flag taxonomy (naming convention, types)

**Phase 2 (Week 3-4):** First feature flag rollout

- Select low-risk feature for pilot (e.g., UI color change)
- Implement gradual rollout (1% → 5% → 25% → 100%)
- Monitor metrics, verify flag propagation across platforms

**Phase 3 (Week 5-6):** Kill switch drill

- Simulate P0 incident, execute kill switch procedure
- Measure time-to-disable (target <1 minute)
- Verify all platforms received flag update (target <30 seconds)

**Phase 4 (Week 7-8):** Governance policies

- Establish quarterly flag audit process
- Document flag lifecycle (creation, testing, rollout, retirement)
- Train all engineers on flag best practices

---

## Compliance Alignment

- **SOC 2 Type II:** Audit trail of all flag changes (who, what, when, why)
- **GDPR Article 30:** Flag-based user segmentation logged for processing activity records
- **SRD Section 8.1:** "Feature flag governance with kill switch capability across all platforms"

---

## References

- [LaunchDarkly Documentation](https://docs.launchdarkly.com/)
- [Feature Flag Best Practices](https://launchdarkly.com/blog/feature-flag-best-practices/)
- [Martin Fowler: Feature Toggles](https://martinfowler.com/articles/feature-toggles.html)
- SRD.md Section 8.1 (Feature Flag Governance)

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching between strategies requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
