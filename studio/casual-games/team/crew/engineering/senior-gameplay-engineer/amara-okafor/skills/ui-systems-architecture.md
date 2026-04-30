---
name: studio-engineering-ui-systems-architecture
description: Mobile game UI framework architecture — Unity UI Toolkit, data-binding patterns, batched rendering optimization, and unified UI system design for casual games at scale. Owned by Amara Okafor (Senior Gameplay Engineer). Use during Studio Pipeline Stages 2–5 for UI system development and Stage 6 (Automated Testing) for UI regression testing. Trigger: UI systems architecture, UI framework, Unity UI Toolkit, data-binding, draw call optimization, retained mode UI.
version: "1.0.0"
---

# UI Systems Architecture

## Purpose

Own the UI systems architecture for the studio's casual games — designing the component model, data-binding strategy, rendering approach, and asset pipeline that every UI screen in the game will use. Amara Okafor built King's unified UI framework (250M+ MAU) and brings that production-scale experience to the studio's Unity 6 LTS stack.

## Tools & Frameworks

| Tool              | Version              | Context                               |
| ----------------- | -------------------- | ------------------------------------- |
| Unity UI Toolkit  | Unity 6 LTS built-in | Primary UI framework for new projects |
| UXML / USS        | Unity 6 LTS          | Declarative UI layout and styling     |
| C# 11             | .NET 8               | UI logic, data binding, view models   |
| Addressables      | 2.0+                 | Dynamic UI asset loading              |
| ScriptableObjects | Unity 6 LTS          | Runtime data containers for UI state  |

## Architecture Decision: UI Toolkit vs. UGUI

For new casual game projects, Amara recommends **Unity UI Toolkit** over legacy UGUI:

| Dimension        | UI Toolkit                                      | UGUI                                                |
| ---------------- | ----------------------------------------------- | --------------------------------------------------- |
| **Rendering**    | Retained mode; batches draw calls automatically | Immediate mode; draw call spikes on complex screens |
| **Styling**      | USS (CSS-like); centrally managed               | Per-component, per-scene; hard to maintain at scale |
| **Data binding** | Built-in runtime binding                        | Manual; requires custom solutions                   |
| **Tooling**      | UI Builder (visual designer)                    | Scene-based; harder to version control              |
| **Mobile perf**  | Better at scale; validated in Unity 6 LTS       | Fine for simple UIs; degrades on complex screens    |

**Exception:** If the project requires third-party UI assets or has existing UGUI investment, Amara evaluates hybrid approaches. This decision is documented in a Stage 3 ADR.

## UI System Design — Component Model

```
UIManager (singleton)
├── ScreenStack (handles push/pop navigation)
│   ├── MainMenuScreen
│   ├── GameplayHUDScreen
│   └── ShopScreen
├── OverlayLayer (toasts, modals, tooltips)
│   ├── ToastController
│   └── ModalController
└── UIDataBus (ScriptableObject event channels)
    ├── PlayerDataChannel
    ├── EconomyChannel
    └── GameStateChannel
```

**Design principles:**

- Screens are **data-driven**: UI components observe `UIDataBus` channels; no direct coupling between screens and game logic
- **Push/pop navigation**: Modal patterns use the ScreenStack to maintain correct back-navigation on mobile
- **No scene transitions for UI**: All UI transitions are within the same scene; Addressables load/unload UI prefabs on demand

## Data Binding Strategy

Amara uses Unity UI Toolkit's runtime data binding with an MVVM-lite pattern:

```csharp
// ViewModel: exposes UI state from game systems
public class PlayerHUDViewModel : INotifyBindablePropertyChanged {
    [CreateProperty]
    public int CoinBalance {
        get => _coinBalance;
        set {
            if (SetProperty(ref _coinBalance, value))
                Notify(nameof(CoinBalance));
        }
    }

    // Called by EconomySystem when player coins change
    public void OnCoinsChanged(int newBalance) => CoinBalance = newBalance;
}

// UXML binding (USS binds to property name)
// <Label binding-path="CoinBalance" />
```

**Benefits:** UI components never call game code directly; data flows one-way through the ViewModel; unit-testable without rendering.

## Rendering Optimization

Key optimizations applied to all UI screens:

```csharp
// 1. Prevent unnecessary re-renders: use version stamps
public class UIOptimizer : MonoBehaviour {
    private int _lastCoinVersion = -1;

    void LateUpdate() {
        int currentVersion = EconomySystem.Instance.CoinVersion;
        if (currentVersion != _lastCoinVersion) {
            _lastCoinVersion = currentVersion;
            coinLabel.text = EconomySystem.Instance.Coins.ToString();
        }
    }
}

// 2. Batch draw calls: group elements in same atlas
// Ensure all UI sprites use a shared texture atlas (max 2048×2048)
// Use UI Toolkit's atlasing in the Panel Settings asset

// 3. Avoid dynamic text that causes re-layout every frame
// Pre-format text that doesn't change; update only what changes
```

### Draw Call Budget

| Screen Type       | Max Draw Calls | Notes                              |
| ----------------- | -------------- | ---------------------------------- |
| Gameplay HUD      | ≤ 8            | Minimal; game is the focus         |
| Main menu         | ≤ 20           | Rich UI but not real-time critical |
| Shop / IAP screen | ≤ 35           | Complex layout; use sprite atlases |
| Modal / overlay   | ≤ 5            | Small, focused surface             |

## Production Scenario: Building the Shop Screen

**Context:** Shop screen requires 40+ IAP cards with dynamic pricing, countdown timers, and personalized offer highlighting. Initial prototype had 80 draw calls.

**Analysis:** Each card was rendering its own background, icon, and price label in separate draw calls. No atlas; no batching.

**Solution:**

1. Moved all card art to a single texture atlas (Sprite Atlas, max 16 cards per atlas; shop has 3 atlases)
2. Replaced per-card price update with a single `OfferViewModel` list bound to a `ListView` (UI Toolkit handles virtualization — only visible cards are rendered)
3. Countdown timers pooled via `UITimerPool` — one update loop drives all timers instead of per-card `Update()`

**Result:** 80 draw calls → 22 draw calls. Frame time for shop screen: 14ms → 4ms on mid-tier Android.

## Stage 6 — UI Regression Testing

At Stage 6 (Automated Testing), Amara owns the UI regression suite:

| Test Type            | Tool                           | What It Catches                      |
| -------------------- | ------------------------------ | ------------------------------------ |
| Snapshot tests       | Unity Test Runner + UISnapshot | Layout changes, missing elements     |
| Draw call regression | UIBenchmark CI script          | Draw call count increase vs baseline |
| Input latency test   | Unity Input Simulation         | Touch-to-response time regression    |
| Accessibility (WCAG) | axe-core mobile (via Maestro)  | AA violations introduced by new UI   |

Any snapshot or draw call regression blocks Stage 6 advancement until Amara reviews and either accepts (documents reason) or fixes.

## Quality Standards

- UI frame budget: ≤ 8ms on mid-tier Android (Pixel 4a equivalent)
- Draw calls per screen: within defined budgets above
- 60fps maintained on target device matrix during all UI transitions
- Zero direct coupling between UI screens and game logic — all data flows via `UIDataBus`
- UI regression suite passes before Stage 6 gate
- All new UI screens reviewed by Amara before Stage 5 implementation begins
