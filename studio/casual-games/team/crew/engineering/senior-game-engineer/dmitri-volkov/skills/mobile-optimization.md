---
name: studio-engineering-mobile-optimization
description: Mobile performance optimization for casual games on Android and iOS — GPU profiling, CPU bottleneck resolution, memory footprint reduction, draw call batching, and platform-specific tuning. Owned by Dmitri Volkov (Senior Game Engineer). Trigger: performance optimization, FPS drop, memory issue, draw calls, profiling, battery drain, mobile performance.
version: "1.0.0"
---

# Mobile Optimization

**Skill Owner:** Dmitri Volkov (Senior Game Engineer)
**Applies To:** Android/iOS Performance, GPU/CPU Profiling, Memory Management, Build Optimization

## Tools & Frameworks

| Tool/Framework          | Version Context | Usage                                            |
| ----------------------- | --------------- | ------------------------------------------------ |
| Unity Profiler          | Built-in        | CPU/GPU/memory frame analysis                    |
| Android GPU Inspector   | Latest          | Frame capture and GPU workload analysis          |
| Xcode Instruments       | Latest          | iOS CPU, memory, and battery profiling           |
| RenderDoc               | 1.33+           | GPU frame capture and overdraw analysis          |
| Unity Memory Profiler   | Built-in        | Managed and native memory snapshots              |
| Android Studio Profiler | Latest          | APK size, native memory, and thread analysis     |
| Firebase Performance    | Latest          | Real-device performance monitoring in production |

## Real-World Production Scenarios

### Scenario 1: Reducing Memory Footprint by 35% on Mid-Tier Android

**Context:** Game crashes on mid-tier Android devices (2GB RAM), causing high crash rates in SEA markets.
**Process:**

1. Capture memory snapshot with Unity Memory Profiler; identify top consumers
2. Textures (40%): apply ASTC compression on Android, PVRTC/ASTC on iOS; reduce mip bias; implement texture atlasing for UI
3. Audio (20%): compress to Vorbis at 44kHz for music, 22kHz for SFX; stream audio >10s instead of loading into memory
4. UI (15%): pool and recycle UI elements using Unity's Object Pooling; disable canvases not currently visible
5. Game objects (15%): implement spatial partitioning (grid-based); only activate objects within camera frustum + buffer zone
6. Overhead (10%): profile the managed heap; eliminate frequent GC allocations in hot paths (use struct-based events, avoid boxing)
7. Profile on real devices every sprint; set a memory budget per system and enforce it via automated tests

**Result target:** ≤50% of available RAM consumed on the minimum spec device.

### Scenario 2: Diagnosing and Resolving a Frame Rate Drop

**Context:** Game hits 45fps on target device (iPhone 12) in a level-complete screen despite 60fps target.
**Process:**

1. Open Unity Profiler; capture 5 seconds on device. Identify whether bottleneck is CPU or GPU
2. If **CPU-bound:** examine main thread; look for GC.Collect spikes, large Update() loops, physics calculations, or layout rebuilds
3. If **GPU-bound:** check draw call count (target ≤150 for mobile); identify overdraw hotspots with Scene View overdraw mode
4. Resolution for GPU overdraw in UI: merge static UI elements into atlases; set UI canvas to "Screen Space - Camera" only when 3D interaction needed
5. Enable SRP Batcher; check for broken batches (materials with different keywords)
6. Verify target frame rate is locked: `Application.targetFrameRate = 60`; check `QualitySettings.vSyncCount = 0` on Android

**Result target:** ≥60fps sustained on iPhone 12 and Pixel 6a at high quality settings.

### Scenario 3: Reducing APK/IPA Build Size

**Context:** APK is 120MB; store guidelines and user research show drop-off above 100MB on mobile data.
**Process:**

1. Run Android Studio's APK Analyser; identify largest resources
2. Strip unused Unity engine modules via Build Settings (remove audio if using FMOD, physics if using custom)
3. Enable IL2CPP + Managed Code Stripping (High); verify no reflection-based code breaks
4. Use Addressable Assets for content that can be downloaded post-install
5. Compress all textures with Build Target–specific formats; remove duplicate assets
6. Target: APK ≤80MB base install, remaining content downloadable on first launch

## Trade-Off Analysis

| Decision            | Option A                  | Option B                     | Trade-Off                                                                                 |
| ------------------- | ------------------------- | ---------------------------- | ----------------------------------------------------------------------------------------- |
| Texture Quality     | Higher resolution         | Lower resolution + ASTC      | Visual quality vs. memory; ASTC at 4bpp delivers 75% savings with negligible visual delta |
| Physics Computation | Unity PhysX (per frame)   | Simplified custom logic      | Accuracy vs. cost; casual games rarely need full PhysX; custom AABB is 10× faster         |
| Object Activation   | Always active             | Pool + activate on demand    | Simplicity vs. memory + CPU; pooling is mandatory for particle effects and projectiles    |
| Shader Complexity   | High-fidelity PBR shaders | Mobile-optimized URP shaders | Visual parity vs. GPU cost; URP mobile shaders save 30–50% fragment shader cycles         |

## Measurable Quality Standards

| Standard          | Target                       | Measurement Method              |
| ----------------- | ---------------------------- | ------------------------------- |
| Frame rate        | ≥60fps sustained             | Unity Profiler + device testing |
| Memory headroom   | ≤50% RAM on minimum spec     | Unity Memory Profiler           |
| Draw calls        | ≤150 per frame               | Unity Frame Debugger            |
| Build size (base) | ≤80MB APK / ≤100MB IPA       | Android Studio / Xcode          |
| Crash rate        | ≤0.1% of sessions            | Firebase Crashlytics            |
| Battery drain     | ≤15% per hour of active play | Android Battery Historian       |

## Industry Best Practice References

- **Google Play Android Vitals** — ANR, crash, and performance benchmarks for Play Store
- **Apple App Store Review Guidelines** — Performance requirements for iOS App Store
- **Unity Mobile Performance Best Practices** — Official Unity documentation
- **GDC 2023: "Real-Time Multiplayer Architecture at Scale"** — Dmitri Volkov (speaker)
