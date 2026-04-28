# Game Architecture Patterns

**Last Updated:** April 9, 2026

---

## 1. Overview

Game architecture patterns solve recurring structural challenges in game development. Unlike application patterns (MVC, MVVM), game patterns must handle real-time loops, physics, input polling, and state-driven behavior. This document catalogs the patterns most relevant to casual mobile game development.

---

## 2. Core Patterns

### 2.1 Game Loop

**Purpose:** The heartbeat of every game. Drives update, rendering, and input processing in a continuous cycle.

```
while (game is running) {
    ProcessInput()
    Update()        // Game logic, physics, AI
    Render()        // Draw frame
    WaitForNextFrame()
}
```

**Unity Implementation:**

```csharp
// Unity abstracts the game loop into lifecycle methods:
void Update()       // Called once per frame — game logic goes here
void FixedUpdate()  // Called at fixed intervals — physics goes here
void LateUpdate()   // Called after Update — camera follow, final positioning
```

**Best Practices:**

| Rule                                                     | Rationale                                               |
| -------------------------------------------------------- | ------------------------------------------------------- |
| Keep `Update()` under 16.67ms (60fps budget)             | Exceeding budget causes frame drops                     |
| Put physics in `FixedUpdate()`, not `Update()`           | Physics requires deterministic timing                   |
| Use `Time.deltaTime` for frame-rate-independent movement | Ensures consistent gameplay across devices              |
| Avoid `FindObjectOfType()` in `Update()`                 | O(n) search every frame — cache references in `Awake()` |

---

### 2.2 Component Pattern

**Purpose:** Game objects are composed of independent, interchangeable parts rather than inheriting from deep class hierarchies.

```
Player GameObject
├── Transform (built-in)
├── SpriteRenderer (built-in)
├── Rigidbody2D (built-in)
├── Collider2D (built-in)
├── PlayerController.cs (custom)
├── HealthComponent.cs (custom)
├── AnimationController.cs (custom)
└── AudioSource (built-in)
```

**Best Practices:**

| Rule                                                                   | Rationale                                                          |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------ |
| One responsibility per component                                       | `PlayerController` handles input; `HealthComponent` handles damage |
| Components communicate via events or interfaces, not direct references | Loose coupling enables reuse                                       |
| Use ScriptableObjects for shared configuration data                    | Multiple enemies can reference the same `EnemyConfig` asset        |

---

### 2.3 Object Pooling

**Purpose:** Pre-allocate and reuse objects instead of creating/destroying at runtime. Critical for mobile performance.

```csharp
public class ObjectPool<T> where T : Component
{
    private Queue<T> _pool = new Queue<T>();
    private T _prefab;

    public T Get()
    {
        if (_pool.Count > 0) return _pool.Dequeue();
        return Object.Instantiate(_prefab);
    }

    public void Return(T obj)
    {
        obj.gameObject.SetActive(false);
        _pool.Enqueue(obj);
    }
}
```

**When to Use:**

| Use Case                           | Priority                              |
| ---------------------------------- | ------------------------------------- |
| Projectiles, bullets, particles    | **Critical** — spawned frequently     |
| Enemy spawns                       | **Critical** — frequent instantiation |
| UI elements (popups, score popups) | **High** — frequent but low-cost      |
| Level chunks (endless runners)     | **High** — large objects, frequent    |
| Audio sources                      | **Medium** — moderate cost            |
| Menu screens                       | **Low** — created once, long-lived    |

---

### 2.4 State Machine

**Purpose:** Game entities transition between discrete states with defined entry/exit behaviors.

```csharp
public abstract class GameState
{
    public abstract void Enter();
    public abstract void Update();
    public abstract void Exit();
}

public class PlayerStateMachine
{
    private GameState _currentState;

    public void ChangeState(GameState newState)
    {
        _currentState?.Exit();
        _currentState = newState;
        _currentState.Enter();
    }

    public void Update() => _currentState?.Update();
}
```

**Common Use Cases in Casual Games:**

| Entity           | States                                                      |
| ---------------- | ----------------------------------------------------------- |
| **Player**       | Idle → Running → Jumping → Falling → Dead                   |
| **Game Manager** | Loading → Menu → Playing → Paused → GameOver → ResultScreen |
| **Enemy**        | Patrol → Alert → Chase → Attack → Dead                      |
| **UI Screen**    | Hidden → Entering → Visible → Exiting → Hidden              |

---

### 2.5 Observer Pattern (Event System)

**Purpose:** Decoupled communication between systems. Publishers emit events; subscribers react without knowing the publisher.

```csharp
// C# event-based approach (recommended over UnityEvents for complex systems)
public static class GameEvents
{
    public static event Action<int> OnScoreChanged;
    public static event Action OnPlayerDied;
    public static event Action<string> OnAchievementUnlocked;

    public static void ScoreChanged(int newScore) => OnScoreChanged?.Invoke(newScore);
    public static void PlayerDied() => OnPlayerDied?.Invoke();
}

// Subscriber:
void OnEnable() => GameEvents.OnScoreChanged += UpdateScoreUI;
void OnDisable() => GameEvents.OnScoreChanged -= UpdateScoreUI;
```

**Best Practices:**

| Rule                                                | Rationale                                             |
| --------------------------------------------------- | ----------------------------------------------------- |
| Always unsubscribe in `OnDisable()`                 | Prevents memory leaks and null reference exceptions   |
| Use `Action<T>` over `UnityEvent` for performance   | `UnityEvent` has reflection overhead                  |
| Keep event payloads minimal                         | Pass only what subscribers need                       |
| Document all events in a central `GameEvents` class | Single source of truth for inter-system communication |

---

### 2.6 Entity Component System (ECS)

**Purpose:** Data-oriented architecture for high-performance games with thousands of entities. Separates data (Components) from behavior (Systems).

**When to Use:**

| Scenario                                 | Recommendation                                                            |
| ---------------------------------------- | ------------------------------------------------------------------------- |
| Casual game with < 100 objects on screen | **Do NOT use ECS** — standard Component pattern is simpler and sufficient |
| Endless runner with 500+ obstacles       | Consider ECS (Unity DOTS) for performance                                 |
| Bullet-hell with 1000+ projectiles       | **Use ECS** — data-oriented approach is necessary                         |
| Puzzle game with static board            | **Do NOT use ECS** — overkill for static content                          |

**Unity DOTS Packages:**

| Package              | Purpose                                    |
| -------------------- | ------------------------------------------ |
| `com.unity.entities` | Core ECS framework                         |
| `com.unity.jobs`     | C# Job System for multi-threading          |
| `com.unity.burst`    | Burst compiler for native code performance |

**Note:** DOTS has a steep learning curve. For a casual mini-game studio, **start with the Component pattern** and only migrate to ECS if profiling shows it's necessary.

---

### 2.7 Service Locator

**Purpose:** Centralized access to singleton services (Audio, Analytics, Save, etc.) without tight coupling.

```csharp
public static class Services
{
    private static IAudioService _audio;
    private static IAnalyticsService _analytics;
    private static ISaveService _save;

    public static IAudioService Audio => _audio ??= new AudioService();
    public static IAnalyticsService Analytics => _analytics ??= new AnalyticsService();
    public static ISaveService Save => _save ??= new SaveService();
}

// Usage:
Services.Analytics.TrackEvent("level_complete", new Dictionary<string, object> {
    { "level", 5 },
    { "score", 1500 }
});
```

**Best Practices:**

| Rule                                                                             | Rationale                                     |
| -------------------------------------------------------------------------------- | --------------------------------------------- |
| Use interfaces, not concrete types                                               | Enables mocking for testing                   |
| Lazy initialization                                                              | Services are created only when first accessed |
| Do NOT overuse — prefer dependency injection (Hilt/Zenject) for complex projects | Service Locator can hide dependencies         |

---

### 2.8 Command Pattern

**Purpose:** Encapsulate user actions as objects. Enables undo/redo, replay systems, and input buffering.

```csharp
public interface ICommand
{
    void Execute();
    void Undo();
}

public class MoveCommand : ICommand
{
    private Player _player;
    private Vector2 _from;
    private Vector2 _to;

    public void Execute() => _player.MoveTo(_to);
    public void Undo() => _player.MoveTo(_from);
}
```

**Use Cases in Casual Games:**

| Use Case                       | Benefit                                |
| ------------------------------ | -------------------------------------- |
| Undo button (puzzle games)     | Store command history, call `Undo()`   |
| Input buffering (rhythm games) | Queue commands, execute on beat        |
| Replay system                  | Re-execute command sequence for replay |
| Tutorial step-through          | Replay tutorial commands on demand     |

---

## 3. Architecture for Casual Mobile Games

### Recommended Architecture: Layered Component + Event-Driven

```
┌──────────────────────────────────────────────────────────────┐
│                      Presentation Layer                      │
│  UI Screens ─── Game Views ─── VFX/Audio ─── Animations      │
├──────────────────────────────────────────────────────────────┤
│                      Game Logic Layer                        │
│  GameMechanics ─── AI ─── Physics ─── Level Management       │
├──────────────────────────────────────────────────────────────┤
│                      Service Layer                           │
│  Audio ─── Analytics ─── Save ─── IAP ─── Ads ─── Network    │
├──────────────────────────────────────────────────────────────┤
│                      Data Layer                              │
│  ScriptableObjects ─── PlayerPrefs ─── Encrypted Save Files  │
└──────────────────────────────────────────────────────────────┘

Communication: Events (GameEvents static class) between layers.
Data flow: Top-down for commands, bottom-up for events.
```

### Anti-Patterns to Avoid

| Anti-Pattern                                                                 | Problem                                               | Solution                                                |
| ---------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------- |
| **God Manager** (one `GameManager` doing everything)                         | Unmaintainable, tightly coupled                       | Split into focused managers (Audio, Save, Analytics)    |
| **Spaghetti dependencies** (A references B references C references A)        | Impossible to test or refactor                        | Use events or interfaces for cross-system communication |
| **Hardcoded values** (speeds, prices, cooldowns in code)                     | Requires code changes and rebuilds to tune            | Move all tunables to ScriptableObjects                  |
| **Direct scene loading** (`SceneManager.LoadScene()` called from UI buttons) | No loading screen, no data passing, no error handling | Centralize scene management in a `SceneController`      |
| **Static singletons everywhere**                                             | Hidden dependencies, hard to test                     | Use Service Locator with interfaces, or DI container    |

---

## 4. Unity-Specific Architecture Patterns

### 4.1 ScriptableObject Architecture

**Purpose:** Data-driven configuration. All game tunables live in asset files, not code.

```csharp
[CreateAssetMenu(fileName = "LevelConfig", menuName = "Game/Level Config")]
public class LevelConfig : ScriptableObject
{
    public int levelNumber;
    public float timeLimit;
    public int targetScore;
    public EnemyData[] enemyWaves;
    public float rewardCoins;
}
```

**Benefits:**

- Designers tune levels without touching code
- Version-controlled (assets are text files)
- Hot-swappable (change values, re-enter Play Mode, see results)
- Reusable across multiple levels

### 4.2 Scene Management Pattern

```
BootScene          → Load services, show splash, transition to MainMenu
MainMenuScene      → Hub: play, settings, store, leaderboards
LoadingScene       → Progress bar, tips, async scene loading
GameplayScene      → Core game loop
ResultScene        → Score, rewards, share, retry, home
```

**Never** call `SceneManager.LoadScene()` directly from UI. Route through a `SceneController`:

```csharp
public class SceneController : MonoBehaviour
{
    public async Task LoadSceneAsync(SceneName scene, float minLoadTime = 1.0f)
    {
        await LoadSceneAsync("LoadingScene");
        var asyncOp = SceneManager.LoadSceneAsync(scene.ToString(), LoadSceneMode.Single);
        asyncOp.allowSceneActivation = false;

        // Show loading UI...
        await Task.Delay((int)(minLoadTime * 1000));

        asyncOp.allowSceneActivation = true;
    }
}
```

---

## 5. Reference Resources

| Resource                                         | Link                                                                   | Focus                                       |
| ------------------------------------------------ | ---------------------------------------------------------------------- | ------------------------------------------- |
| Game Programming Patterns (book)                 | https://gameprogrammingpatterns.com/                                   | Comprehensive pattern catalog (free online) |
| Unity Design Patterns                            | https://learn.unity.com/project/design-patterns                        | Official Unity Learn course                 |
| "Design Patterns That Shaped the World of Games" | https://kokkugames.com/design-patterns-that-shaped-the-world-of-games/ | Historical context + practical application  |
| Entity Component System Guide                    | https://www.theknowledgeacademy.com/blog/entity-component-system/      | ECS deep dive                               |

---

_End of Game Architecture Patterns_
