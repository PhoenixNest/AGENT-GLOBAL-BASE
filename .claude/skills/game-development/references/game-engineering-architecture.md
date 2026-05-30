---
name: studio-engineering-game-engineering-architecture
description: Game system architecture and cross-platform design — offline-first sync, memory optimization, networking models, engine selection (Unity/Unreal) for casual games. Owned by Dmitri Volkov (Senior Game Engineer). Use during Studio Pipeline Stages 1–4 for architecture decisions and Stage 5 (Full Production) for system implementation. Trigger: game architecture, system design, offline-first sync, networking, engine selection, cross-platform.
version: "1.0.0"
---

# Game Engineering Architecture

**Skill Owner:** Dmitri Volkov (Senior Game Engineer)
**Applies To:** System Architecture, Networking, Cross-Platform Design, Engine Architecture

## Tools & Frameworks

| Tool/Framework  | Version Context | Usage                                    |
| --------------- | --------------- | ---------------------------------------- |
| Unity           | Unity 6 LTS     | Primary game engine                      |
| Unreal Engine   | 5.4+            | Alternative engine for specific projects |
| C#              | .NET 8+         | Primary gameplay language                |
| C++             | C++20           | Engine-level code, performance-critical  |
| Photon / Mirror | Latest          | Multiplayer networking                   |
| PlayFab         | Latest          | Backend services (abstraction layer)     |
| RenderDoc       | 1.33+           | GPU debugging and profiling              |

## Real-World Production Scenarios

### Scenario 1: Designing Offline-First Sync Architecture

**Context:** Mobile casual game needs reliable offline play with cloud sync.
**Process:**

1. Design local-first data model: all game state stored locally first, synced to cloud when online
2. Implement conflict resolution: last-write-wins for simple data, operational transforms for complex state
3. Build sync queue: pending changes queued locally, synced in order when connection restored
4. Design fallback: graceful degradation when sync fails, user notified but gameplay continues
5. Test under network conditions: 3G, high latency, intermittent connectivity using network simulation tools
6. Results: 99.9% data consistency, seamless offline experience

### Scenario 2: Reducing Memory Footprint by 35%

**Context:** Game crashes on mid-tier Android devices with 2GB RAM.
**Process:**

1. Profile memory usage: Unity Profiler + Android Memory Profiler
2. Identify top consumers: textures (40%), audio (20%), UI (15%), game objects (15%), overhead (10%)
3. Optimize textures: ASTC compression, reduce resolution for distant objects, texture atlasing
4. Optimize audio: compress to Vorbis, stream large audio files, reduce sample rate for SFX
5. Optimize UI: pool UI elements, reduce overdraw, use canvas batching
6. Results: 35% memory reduction, game runs smoothly on 2GB devices

## Trade-Off Analysis

| Decision         | Option A                  | Option B                      | Trade-Off                                                                                                        |
| ---------------- | ------------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Engine Choice    | Unity (C#)                | Unreal (C++)                  | Unity = faster development, larger mobile community; Unreal = better graphics out-of-box, steeper learning curve |
| Networking Model | Client-authoritative      | Server-authoritative          | Client = lower latency but cheatable; Server = secure but higher latency and server cost                         |
| Data Persistence | Local SQLite + cloud sync | Cloud-only with offline cache | Local = reliable offline but sync complexity; Cloud-only = simpler but requires connectivity                     |

## Measurable Quality Standards

| Standard                      | Target                    | Measurement Method                 |
| ----------------------------- | ------------------------- | ---------------------------------- |
| Frame Rate                    | ≥ 60fps on target devices | Unity Profiler, device testing     |
| Memory Usage                  | ≤ 50% of available RAM    | Android/iOS memory profiling       |
| Load Time                     | ≤ 10 seconds cold start   | Automated load time testing        |
| Crash Rate                    | ≤ 0.1% of sessions        | Crash reporting (Firebase, Sentry) |
| Network Latency (multiplayer) | ≤ 200ms p95               | Network profiling                  |

## Scenario: Client-Server Real-Time Multiplayer Architecture

Dmitri's career highlight is a 30M-player mobile game with real-time PvP. This scenario documents the architecture patterns for scaling a casual game from single-player to real-time multiplayer.

### Problem Statement

A casual match-3 game is adding a real-time PvP mode where two players race to clear a board simultaneously. Requirements:

- Real-time board sync with ≤200ms p95 latency
- Anti-cheat: server must be authoritative over board state
- Scale to 50,000 concurrent matches at launch

### Architecture Decision: Server-Authoritative with Client Prediction

```
Client A                    Game Server (Photon)               Client B
  |                               |                               |
  |── Input event ──────────────>|                               |
  |<─ State update (ACK) ────────|── State broadcast ──────────>|
  |                               |                               |
  |  [Client predicts locally]    |  [Server is truth]            |
  |<─ Correction if diverged ────|                               |
```

**Why server-authoritative:**

- Prevents score manipulation (Client A cannot report a win the server did not authorize)
- Enables replay verification and anti-cheat audit
- Cost: ~15ms additional latency vs. client-authoritative; acceptable for casual PvP

### Rollback Netcode for Latency Masking

For players with 100–150ms round-trip latency, input lag is noticeable. Dmitri implements rollback netcode:

```csharp
public class RollbackManager : MonoBehaviour {
    private const int ROLLBACK_FRAMES = 8; // ~133ms at 60fps
    private GameState[] stateBuffer = new GameState[ROLLBACK_FRAMES];

    public void OnServerCorrection(GameState authorityState, int serverFrame) {
        int localFrame = networkManager.LocalFrame;
        int frameDelta = localFrame - serverFrame;

        if (frameDelta > 0 && frameDelta <= ROLLBACK_FRAMES) {
            // Roll back to server frame
            RestoreState(stateBuffer[serverFrame % ROLLBACK_FRAMES]);

            // Re-simulate frames from server frame to current
            for (int f = serverFrame; f < localFrame; f++) {
                ApplyInput(inputBuffer[f % INPUT_BUFFER_SIZE]);
                SimulateFrame();
                stateBuffer[f % ROLLBACK_FRAMES] = CaptureState();
            }
        }
    }
}
```

### Scaling to 50K Concurrent Matches

| Layer             | Solution                                                    | Why                                                          |
| ----------------- | ----------------------------------------------------------- | ------------------------------------------------------------ |
| Match server      | Photon Realtime (managed)                                   | Auto-scales; no server management at launch                  |
| Match assignment  | Custom matchmaking service (Go)                             | Photon's default matchmaking too slow for MMR-based matching |
| State persistence | Redis (per-match state)                                     | Sub-millisecond read; evicted on match end                   |
| Long-term storage | PostgreSQL (match history, results)                         | ACID for final score recording                               |
| Anti-cheat        | Server-side move validation + statistical anomaly detection | Detect 99th percentile speed runners and flag for review     |

### When to Use This Pattern

This pattern is appropriate for:

- Turn-based async PvP (lower stakes, works fine for casual games with ≤500ms latency tolerance)
- Real-time casual PvP with 2-8 players and ≤15 minutes per session
- Leaderboard-driven competitive features

Do NOT use Photon Realtime for:

- Large-scale MMO-style battles (>64 concurrent players in one room) — use dedicated server topology
- Cross-platform LAN play — consider Steam Networking or peer-to-peer fallback

## Industry Best Practice References

- **GDC 2023: "Real-Time Multiplayer Architecture at Scale"** — Dmitri's own talk
- **Unity Performance Optimization Guide** — Official Unity best practices
- **Google Play Android Vitals** — Platform-specific performance standards
- **Apple App Store Review Guidelines** — Platform-specific requirements
- **Photon Realtime Documentation** — Dmitri's preferred multiplayer framework for casual games
