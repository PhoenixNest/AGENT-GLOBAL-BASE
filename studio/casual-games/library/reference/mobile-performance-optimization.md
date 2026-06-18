# Mobile Performance Optimization

**Last Updated:** April 9, 2026

---

## 1. Performance Budgets for Casual Mobile Games

| Metric                          | Target (High-End) | Target (Mid-Range) | Target (Low-End) |
| ------------------------------- | ----------------- | ------------------ | ---------------- |
| **Frame Rate**                  | 60 FPS            | 60 FPS             | 30 FPS (stable)  |
| **Frame Time Budget**           | 16.67ms total     | 16.67ms total      | 33.33ms total    |
| └ CPU Budget                    | 8ms               | 10ms               | 15ms             |
| └ GPU Budget                    | 8ms               | 6ms                | 18ms             |
| **Draw Calls**                  | < 150             | < 100              | < 60             |
| **Triangles**                   | < 200K            | < 100K             | < 50K            |
| **Memory (RAM)**                | < 300 MB          | < 200 MB           | < 150 MB         |
| **App Size (initial download)** | < 100 MB          | < 80 MB            | < 50 MB          |
| **Load Time (cold start)**      | < 5s              | < 8s               | < 12s            |
| **Scene Transition**            | < 2s              | < 3s               | < 5s             |

---

## 2. GPU Optimization (Rendering)

### 2.1 Draw Call Reduction

Draw calls are the #1 GPU bottleneck on mobile. Each draw call requires CPU-to-GPU communication.

| Technique            | Impact | Effort                                                    |
| -------------------- | ------ | --------------------------------------------------------- |
| **Sprite Atlasing**  | ★★★★★  | Low — Unity's Sprite Packer auto-atlas                    |
| **Static Batching**  | ★★★★☆  | Low — mark static objects as "Static"                     |
| **Dynamic Batching** | ★★★☆☆  | Low — automatic for < 300 vertex meshes                   |
| **GPU Instancing**   | ★★★★★  | Medium — use `MaterialPropertyBlock` for varied instances |
| **Combine meshes**   | ★★★★☆  | Medium — merge static geometry into single mesh           |

### 2.2 Texture Optimization

| Setting                | Recommendation                                       | Rationale                                  |
| ---------------------- | ---------------------------------------------------- | ------------------------------------------ |
| **Compression**        | ASTC 6x6 or 8x8 for mobile                           | Universal support, good quality/size ratio |
| **Max Size**           | 1024 for UI, 2048 for backgrounds                    | Higher sizes waste memory on mobile        |
| **Generate Mip Maps**  | Disabled for 2D/UI; Enabled for 3D                   | Mip maps add 33% memory overhead           |
| **sRGB**               | Enabled for color textures; Disabled for normal maps | Correct color space                        |
| **Read/Write Enabled** | Disabled in production                               | Doubles texture memory usage               |

### 2.3 Shader Optimization

| Rule                                               | Rationale                                              |
| -------------------------------------------------- | ------------------------------------------------------ |
| Use **Mobile/Diffuse** or **Mobile/Unlit** shaders | Built-in mobile shaders are highly optimized           |
| Avoid **transparent shaders** when opaque works    | Transparent shaders disable early-Z optimization       |
| Minimize **texture samples** in shaders            | Each `tex2D` costs GPU cycles                          |
| Avoid **branching** (`if/else`) in shaders         | GPUs execute both branches and discard results         |
| Use **Shader Graph** with "Mobile" target          | Ensures shader is optimized for mobile GPUs            |
| Limit **post-processing effects**                  | Each effect is a full-screen pass (millions of pixels) |

### 2.4 Lighting

| Technique                                            | Recommendation                                 |
| ---------------------------------------------------- | ---------------------------------------------- |
| **Baked lighting** for static geometry               | Use Lightmaps — zero runtime cost              |
| **Real-time lights** only for dynamic objects        | Limit to 1–2 real-time lights per scene        |
| **Light probes** for dynamic objects in baked scenes | Interpolates baked lighting for moving objects |
| **Disable real-time shadows** on mobile              | Use baked shadows or fake shadow sprites       |

---

## 3. CPU Optimization (Game Logic)

### 3.1 Update Loop Optimization

| Anti-Pattern                       | Problem                           | Fix                                          |
| ---------------------------------- | --------------------------------- | -------------------------------------------- |
| `FindObjectOfType()` in `Update()` | O(n) search every frame           | Cache in `Awake()` or `Start()`              |
| `GetComponent<T>()` in `Update()`  | Reflection overhead every frame   | Cache in `Awake()` or `[SerializeField]`     |
| `SendMessage()`                    | Slow reflection-based dispatch    | Use C# events or direct method calls         |
| String concatenation in `Update()` | Allocates memory → GC spikes      | Use string builders or pre-formatted strings |
| `new` keyword in `Update()`        | Allocates heap memory → GC spikes | Pre-allocate or use object pools             |
| `Debug.Log()` in production        | String formatting + I/O overhead  | Wrap in `#if UNITY_EDITOR` blocks            |

### 3.2 Physics Optimization

| Rule                                                                | Rationale                                           |
| ------------------------------------------------------------------- | --------------------------------------------------- |
| Use **2D physics** for 2D games (`Physics2D`, not `Physics`)        | 3D physics on 2D objects wastes CPU                 |
| Set **Sleep Mode** to "Start Awake" for static objects              | Sleeping objects don't consume physics CPU          |
| Use **simplified colliders** (Box, Circle) over Mesh Colliders      | Mesh Colliders are expensive                        |
| **Disable physics** on objects that don't need it                   | Remove `Rigidbody2D` from static decorative objects |
| Use **Layer Collision Matrix** to skip unnecessary collision checks | Edit → Project Settings → Physics 2D                |

### 3.3 Coroutines vs. Update

| Scenario                          | Use                        |
| --------------------------------- | -------------------------- |
| Continuous input checking         | `Update()`                 |
| Timed sequences (wait, then do X) | Coroutines                 |
| Complex state machines over time  | Coroutines or async/await  |
| High-frequency polling            | Avoid — use events instead |

---

## 4. Memory Management

### 4.1 Garbage Collection (GC)

Unity's Mono runtime uses Boehm GC — it pauses the game to clean up unused memory. **GC spikes are the #1 cause of stuttering on mobile.**

| Rule                                                     | Rationale                                           |
| -------------------------------------------------------- | --------------------------------------------------- |
| **Never allocate in Update()**                           | Every allocation eventually triggers GC             |
| **Pre-allocate collections** (`new List<T>(capacity)`)   | Prevents internal array resizing (which allocates)  |
| **Use `StringBuilder`** for dynamic text                 | String concatenation creates garbage                |
| **Avoid LINQ** in runtime code                           | LINQ allocates enumerators                          |
| **Cache IEnumerator** for repeated coroutines            | `StartCoroutine(MyCoroutine())` allocates each call |
| **Use `struct` instead of `class`** for small data types | Structs are stack-allocated (no GC)                 |
| **Object pool everything**                               | Eliminates allocation/deallocation cycles           |

### 4.2 Memory Profiling

| Tool                                                     | Purpose                                             |
| -------------------------------------------------------- | --------------------------------------------------- |
| **Unity Profiler** (Window → Analysis → Profiler)        | Real-time CPU, GPU, memory, rendering stats         |
| **Memory Profiler Package** (`com.unity.memoryprofiler`) | Memory snapshot comparison, leak detection          |
| **Deep Profile**                                         | Identifies specific method-level performance issues |
| **Xcode Instruments (iOS)**                              | Native memory profiling on iOS devices              |
| **Android Studio Profiler**                              | Native memory profiling on Android devices          |

### 4.3 Memory Budget by Category

| Category         | Budget              |
| ---------------- | ------------------- |
| Textures         | 40–50% of total RAM |
| Audio            | 10–15% of total RAM |
| Meshes           | 5–10% of total RAM  |
| Code + Mono heap | 15–20% of total RAM |
| Unity engine     | 10–15% of total RAM |
| Overhead         | 5–10% of total RAM  |

---

## 5. Addressables System

### 5.1 Why Addressables

| Problem         | Without Addressables                        | With Addressables                              |
| --------------- | ------------------------------------------- | ---------------------------------------------- |
| **App size**    | All assets bundled → large initial download | Core assets bundled, rest downloaded on-demand |
| **Memory**      | All assets loaded at startup                | Load only what's needed, unload when done      |
| **Updates**     | Full app re-download                        | Download only changed asset bundles            |
| **A/B testing** | Requires code changes                       | Swap asset groups remotely                     |

### 5.2 Addressables Grouping Strategy

| Group              | Content                                      | Load Strategy                               |
| ------------------ | -------------------------------------------- | ------------------------------------------- |
| **Core**           | MainMenu scene, essential UI, startup assets | Packaged with app, loaded at startup        |
| **Gameplay**       | Gameplay scene, core mechanic prefabs        | Loaded on-demand when entering gameplay     |
| **Levels**         | Per-level assets (configs, art)              | Loaded per level, unloaded after completion |
| **UI**             | Settings, store, leaderboards screens        | Loaded on-demand, kept in memory            |
| **Audio**          | Music tracks, SFX                            | Streamed (music) or preloaded (SFX)         |
| **Remote Content** | Seasonal events, cosmetics                   | Downloaded from CDN, cached locally         |

### 5.3 Addressables Best Practices

| Rule                                                       | Rationale                                              |
| ---------------------------------------------------------- | ------------------------------------------------------ |
| **Group by load pattern** (not by type)                    | Group assets that load/unload together                 |
| **Use "Pack Separately"** for large unique assets          | Prevents one large asset from bloating the whole group |
| **Enable "Build Remote Catalog"** for downloadable content | Enables CDN-based asset delivery                       |
| **Use content update restriction**                         | Only changed assets need re-download                   |
| **Profile with Addressables Event Viewer**                 | Identifies redundant loads and memory leaks            |

---

## 6. Profiling Workflow

### 6.1 When to Profile

| Milestone                                      | Action                                     |
| ---------------------------------------------- | ------------------------------------------ |
| After **Mechanic Sprint #1**                   | Baseline performance measurement           |
| At **50% completion** (Game Feel Checkpoint)   | Full profiling pass — identify bottlenecks |
| At **75% completion** (Visual Coherence Check) | Re-profile after art integration           |
| At **90% completion** (Tier 3 Playtest)        | Final optimization pass                    |
| Before **Soft Launch**                         | Performance sign-off on device matrix      |

### 6.2 Device Testing Matrix

| Tier           | Devices                              | Purpose                                                   |
| -------------- | ------------------------------------ | --------------------------------------------------------- |
| **High-End**   | iPhone 15+, Samsung Galaxy S24+      | Baseline for "best case" performance                      |
| **Mid-Range**  | iPhone 13, Samsung Galaxy A54        | Target performance tier (majority of users)               |
| **Low-End**    | iPhone SE (2022), Samsung Galaxy A14 | Minimum viable performance (30fps target)                 |
| **Android Go** | Devices with < 2GB RAM               | Graceful degradation test (if targeting emerging markets) |

### 6.3 Profiling Checklist

| Check                | Tool                 | Pass Criteria                                            |
| -------------------- | -------------------- | -------------------------------------------------------- |
| Frame rate stability | Unity Profiler       | No drops below target FPS for > 3 consecutive frames     |
| Memory usage         | Memory Profiler      | Total RAM < target budget; no memory growth over 30 min  |
| Draw call count      | Frame Debugger       | < target budget for device tier                          |
| CPU time per system  | Profiler (CPU Usage) | No single system > 5ms per frame                         |
| GC allocations       | Profiler (GC Alloc)  | Zero allocations during gameplay (not during scene load) |
| Load time            | Custom timer         | < target for device tier                                 |
| App binary size      | Build report         | < 50 MB initial download (or < 150 MB with OBB)          |

---

## 7. Quick Reference: Optimization Cheat Sheet

### "Do This First" — Highest Impact, Lowest Effort

| Action                                                     | Expected Improvement                   |
| ---------------------------------------------------------- | -------------------------------------- |
| Enable **Sprite Atlasing**                                 | 30–50% draw call reduction for 2D      |
| Use **IL2CPP** (not Mono)                                  | 20–40% CPU improvement, smaller binary |
| **Object pool** frequently spawned objects                 | Eliminate GC spikes                    |
| Set **Max Size** on textures                               | 30–50% memory reduction                |
| Disable **Read/Write** on textures not modified at runtime | 50% texture memory reduction           |
| Use **unlit shaders** for 2D/UI elements                   | 2–3x rendering performance             |
| **Static batch** non-moving objects                        | 20–40% draw call reduction             |
| Remove **Debug.Log()** from production build               | 5–10% CPU improvement                  |

---

## 8. External Resources

| Resource                                        | Link                                                                                                  | Focus                            |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------- |
| Unity Mobile Optimization Guide                 | https://uhiyama-lab.com/en/notes/unity/unity-mobile-game-optimization-guide/                          | GPU, CPU, memory optimization    |
| Unity Blog: Graphics & Asset Optimization       | https://unity.com/blog/games/optimize-your-mobile-game-performance-expert-tips-on-graphics-and-assets | Official Unity optimization tips |
| Unity Profiler Manual                           | https://docs.unity3d.com/Manual/Profiler.html                                                         | Official documentation           |
| "Optimizing Unity Games for Mobile Performance" | https://elaris.software/blog/unity-mobile-optimization-2025/                                          | Practical optimization guide     |
| Unity Addressables Documentation                | https://docs.unity3d.com/Manual/class-addressableassetsettings.html                                   | Official Addressables guide      |

---

_End of Mobile Performance Optimization_
