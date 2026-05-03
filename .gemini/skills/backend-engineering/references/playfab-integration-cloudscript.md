---
name: studio-engineering-playfab-integration-cloudscript
description: PlayFab SDK integration and Cloud Script development — authentication, economy, API wrapper design, and PlayFab Events to Kafka data export pipeline. Also covers Stage 7 (Soft Launch Prep) backend readiness checks and Stage 10 (Live Ops) monitoring and incident response. Owned by Aisha Bello (Backend Engineer). Use during Stage 5 for integration development, Stage 7 for soft launch backend validation, and Stage 10 for live operations support. Trigger: PlayFab integration, Cloud Script, PlayFab SDK, Kafka pipeline, API wrapper, Azure Functions, live ops backend, soft launch readiness.
version: "1.0.0"
---

# PlayFab Integration & Cloud Script

## Purpose

Implement and maintain the PlayFab backend stack for the studio's casual games — SDK integration, Cloud Script functions, API wrapper design, and the data export pipeline. Aisha Bello owns PlayFab integration from Stage 5 (Full Production) through Stage 7 (Soft Launch Prep) and Stage 10 (Live Ops). She works under direction from Priya Nair (Senior Backend Engineer) who owns architecture and anti-cheat design.

## Tools & Frameworks

| Tool            | Version | Context                                       |
| --------------- | ------- | --------------------------------------------- |
| PlayFab SDK     | v2.17   | Authentication, Economy, Cloud Script, Events |
| C#              | 11.0    | Cloud Script functions; API wrappers          |
| Azure Functions | v4      | Serverless Cloud Script execution             |
| Apache Kafka    | 3.5     | Event streaming for analytics pipeline        |
| NUnit           | 3.13    | Unit testing for Cloud Script functions       |

## Stage 5 — PlayFab Integration Development

### SDK Integration Pattern

Aisha implements PlayFab SDK integration behind an interface contract designed by Priya Nair. The wrapper ensures PlayFab-specific calls are never in gameplay code:

```csharp
// Interface designed by Priya Nair; Aisha implements
public interface IBackendAdapter {
    Task<PlayerProfile> GetProfileAsync(string playerId);
    Task UpdateCurrencyAsync(string playerId, CurrencyOperation op);
    Task<CloudScriptResult> InvokeCloudScriptAsync(string functionName, object args);
}

// Aisha's implementation
public class PlayFabAdapter : IBackendAdapter {
    public async Task<PlayerProfile> GetProfileAsync(string playerId) {
        var result = await PlayFabClientAPI.GetPlayerProfileAsync(
            new GetPlayerProfileRequest { PlayFabId = playerId }
        );
        return MapToProfile(result.Result.PlayerProfile);
    }
    // ... remaining methods
}
```

**Benefits:** Interface lets unit tests mock the backend; future migration away from PlayFab requires only a new adapter class.

### Cloud Script Development

Aisha writes C# Cloud Script functions for economy transactions and player progression:

```csharp
// Example: Currency grant with validation
public static async Task<CloudScriptResult> GrantCurrency(dynamic args) {
    var playerId = currentPlayerId;
    var amount = (int)args.amount;
    var reason = (string)args.reason;

    // Server-side validation (Priya designs these rules; Aisha implements)
    if (amount <= 0 || amount > 10000) {
        return new CloudScriptResult { Error = "InvalidAmount" };
    }

    await PlayFabServerAPI.AddUserVirtualCurrencyAsync(new AddUserVirtualCurrencyRequest {
        PlayFabId = playerId,
        Amount = amount,
        VirtualCurrency = "GC" // Gold Coins
    });

    // Log to analytics pipeline
    await LogEvent("currency_grant", new { amount, reason });

    return new CloudScriptResult { Success = true };
}
```

**Quality gate (Stage 5):** All Cloud Script functions have NUnit tests. Coverage ≥ 80% before Stage 6 entry.

### PlayFab Events → Kafka Pipeline

```
PlayFab Events → Azure Function (Aisha's code) → Kafka Topic → Analytics Team
```

Key design decisions:

- **Idempotency key:** Each event carries `eventId`; Kafka consumer deduplicates on re-delivery
- **Schema:** Events converted to Avro before Kafka publish; schema registry maintained in `backend/schemas/`
- **Latency target:** ≤ 30s from PlayFab event to Kafka partition

## Stage 7 — Soft Launch Prep Backend Readiness

Before the game enters Stage 7 (Soft Launch), Aisha completes a backend readiness checklist for each test region:

| Check                             | Owner         | Pass Criteria                                              |
| --------------------------------- | ------------- | ---------------------------------------------------------- |
| Cloud Script function smoke tests | Aisha         | All 100% pass in staging env                               |
| Economy integrity baseline        | Priya + Aisha | Starting balances correct; no negative currency            |
| Data pipeline live verification   | Aisha         | Events visible in Kafka ≤ 30s                              |
| Error rate baseline               | Aisha         | Cloud Script error rate < 0.1% across 100 test invocations |
| Rollback procedures documented    | Priya         | Rollback runbook reviewed and accessible                   |
| PlayFab dashboard access          | Aisha         | Monitoring dashboards live for all soft launch regions     |

**Deliverable:** Aisha produces a _Backend Soft Launch Sign-off_ document listing all checks and their pass status. This is reviewed by Priya Nair before Stage 7 advancement.

### Monitoring Setup for Soft Launch

Aisha configures PlayFab monitoring dashboards before soft launch:

```
Dashboard: Soft Launch Monitoring
├── Real-time: Active players, concurrent sessions
├── Economy: Currency granted/spent per hour; shop purchase rate
├── Errors: Cloud Script error rate; SDK call failure rate
├── Data Pipeline: Kafka lag, event throughput, retry count
└── Alerts: Pager-level alert if Cloud Script error rate > 1%
```

Alert contacts: Priya Nair (primary), Aisha Bello (secondary), Executive Producer James Okonkwo (for player-visible issues).

## Stage 10 — Live Ops Backend Support

Aisha remains active during Stage 10 (Live Ops) to maintain and evolve the PlayFab backend as the live game grows.

### Routine Live Ops Tasks

| Task                           | Frequency          | Description                                                           |
| ------------------------------ | ------------------ | --------------------------------------------------------------------- |
| Cloud Script function updates  | Per live ops event | New economy functions for seasonal events, offers, limited-time modes |
| Data pipeline health check     | Weekly             | Verify Kafka lag, retry rates, schema compatibility                   |
| Economy anomaly review         | Weekly             | Review currency grant/spend ratios for inflation signals              |
| PlayFab SDK version assessment | Quarterly          | Review PlayFab changelogs; plan upgrades with Priya                   |
| Incident response              | On-alert           | Follow runbook; escalate to Priya within 15 minutes if unresolved     |

### Incident Response Protocol

When a backend alert fires during Stage 10:

```
1. Acknowledge alert (within 5 minutes)
2. Check PlayFab status page → if PlayFab outage, contact Priya and broadcast to #live-ops channel
3. Check Cloud Script error logs → identify failing function
4. If error is new Cloud Script function: roll back to previous version via PlayFab dashboard
5. If error is data pipeline: check Kafka consumer lag; restart Azure Function if lag > 10,000 events
6. Escalate to Priya if not resolved within 15 minutes
7. Write incident report within 24 hours of resolution
```

**Escalation path:** Aisha → Priya Nair (Senior Backend) → James Okonkwo (Executive Producer)

## Quality Standards

| Metric                         | Target                              |
| ------------------------------ | ----------------------------------- |
| Cloud Script execution time    | ≤ 5s per invocation                 |
| API wrapper test coverage      | ≥ 80%                               |
| Data pipeline latency          | ≤ 30s from PlayFab event to Kafka   |
| Interface contract compliance  | 100% of defined methods             |
| Cloud Script error rate (live) | < 0.1%                              |
| Soft launch readiness sign-off | Required before Stage 7 advancement |
