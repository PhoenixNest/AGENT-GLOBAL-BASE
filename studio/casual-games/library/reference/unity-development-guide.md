# Unity 6 Development Guide

**Version:** Unity 6.3 LTS (current production)  
**Last Updated:** April 9, 2026

---

## 1. Current Unity Version Landscape

| Version           | Type              | Support Until     | Status                                    |
| ----------------- | ----------------- | ----------------- | ----------------------------------------- |
| Unity 6.0 LTS     | LTS               | October 2026      | End of life approaching                   |
| **Unity 6.3 LTS** | **LTS**           | **December 2027** | **Current recommended LTS**               |
| Unity 6.4         | Supported release | Until 6.5 LTS     | Production-ready (LTS-equivalent support) |
| Unity 6.5         | Beta              | —                 | Not for production                        |
| Unity 6.7 LTS     | Planned LTS       | Q4 2026           | Evaluate when released                    |

**Recommendation:** Lock to **Unity 6.3 LTS** for all new projects. It has the longest remaining support window and is the most stable production release.

---

## 2. Project Structure Best Practices

### Recommended Folder Layout for Mobile Games

```
Assets/
├── _Project/                    # All project-specific content (underscore for sorting)
│   ├── Scripts/                 # C# source code
│   │   ├── Core/                # Game loop, managers, systems
│   │   ├── Gameplay/            # Mechanics, controllers, behaviors
│   │   ├── UI/                  # All UI-related scripts
│   │   ├── Audio/               # Audio managers and controllers
│   │   └── Data/                # ScriptableObjects, data models
│   ├── Prefabs/                 # Prefab files
│   │   ├── Characters/
│   │   ├── Environment/
│   │   ├── UI/
│   │   └── VFX/
│   ├── Scenes/                  # Unity scenes
│   │   ├── Core/                # Core scenes (MainMenu, Loading)
│   │   ├── Gameplay/            # Gameplay scenes (levels)
│   │   └── Test/                # Test and debugging scenes
│   ├── Art/                     # Art assets
│   │   ├── 2D/
│   │   │   ├── Sprites/
│   │   │   ├── UI/
│   │   │   └── Textures/
│   │   └── 3D/
│   │       ├── Models/
│   │       ├── Materials/
│   │       └── Animations/
│   ├── Audio/
│   │   ├── SFX/
│   │   ├── Music/
│   │   └── Voice/
│   ├── ScriptableObjects/       # Configuration data
│   │   ├── GameSettings/
│   │   ├── Levels/
│   │   └── Economy/
│   └── Resources/               # Runtime-loaded resources (minimize usage)
├── Plugins/                     # Third-party plugins and SDKs
│   ├── Android/
│   └── iOS/
├── AddressableAssetsData/       # Addressables configuration
├── Settings/                    # URP settings, input system config
├── StreamingAssets/             # Read-only assets bundled with build
└── ThirdParty/                  # Third-party assets (unmodified originals)
    └── <AssetName>/
        ├── Original/            # Unmodified download (for provenance)
        └── Modified/            # Our modifications
```

### Key Principles

| Principle                                             | Rationale                                                                 |
| ----------------------------------------------------- | ------------------------------------------------------------------------- |
| `_Project/` prefix                                    | Ensures project content sorts to top of Asset folder                      |
| Separate `ThirdParty/` with `Original/` + `Modified/` | Clear audit trail for asset licensing and security review                 |
| Minimize `Resources/`                                 | Unity loads everything in Resources/ at startup; use Addressables instead |
| `StreamingAssets/` for read-only bundled content      | Bundled as-is, accessible at runtime via path                             |
| `ScriptableObjects/` for configuration                | Data-driven design, easy to tune without code changes                     |

---

## 3. Universal Render Pipeline (URP) Setup

For casual mobile games, **URP is the recommended rendering pipeline**. HDRP is overkill and too heavy for mobile targets.

### URP Configuration for Mobile

| Setting               | Recommended Value                                                  | Rationale                                                    |
| --------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------ |
| **Render Pipeline**   | URP (Mobile tier)                                                  | Best balance of quality and performance                      |
| **MSAA**              | 2x (or disabled for lowest-end targets)                            | Balance between quality and GPU cost                         |
| **Depth Texture**     | Disabled (unless needed for specific effects)                      | Adds render pass overhead                                    |
| **Opaque Texture**    | Disabled                                                           | Only needed for specific post-processing effects             |
| **Shadow Cascades**   | 1 cascade (or disabled for 2D games)                               | Shadow quality vs. performance trade-off                     |
| **Shadow Resolution** | 512–1024 for mobile                                                | Higher resolutions are GPU-heavy                             |
| **Additional Lights** | Disabled or limited to 2–4 per object                              | Each light adds a render pass                                |
| **Pixel Light Count** | 1–2                                                                | Most mobile games can get away with minimal dynamic lighting |
| **Post-processing**   | Enabled, but limit to 2–3 effects (color grading, bloom, vignette) | Each effect adds a full-screen pass                          |

### URP Renderer Features (Enable Only What You Need)

| Feature           | Use Case                      | Mobile Cost |
| ----------------- | ----------------------------- | ----------- |
| Forward Renderer  | Default for most games        | Baseline    |
| 2D Renderer       | 2D games with custom lighting | Low         |
| Deferred Renderer | NOT recommended for mobile    | High        |
| Tile Renderer     | 2D tilemap-based games        | Low         |

---

## 4. Input System

**Use the new Input System package**, not the legacy Input Manager.

| Feature                  | Recommendation                                                                   |
| ------------------------ | -------------------------------------------------------------------------------- |
| **Input System Package** | Unity Input System (com.unity.inputsystem) — install via Package Manager         |
| **Input Actions**        | Define in `.inputactions` asset; map to touch, swipe, hold gestures              |
| **Touch Handling**       | Use Input System's touch phase events (Started, Performed, Cancelled)            |
| **Multi-touch**          | Configure in Input Actions if game requires (most casual games are single-touch) |

---

## 5. Build Pipeline Configuration

### Android Build Settings

| Setting                      | Value                                                                    |
| ---------------------------- | ------------------------------------------------------------------------ |
| **Scripting Backend**        | IL2CPP (required by Google Play, better performance than Mono)           |
| **Target Architecture**      | ARM64 (required by Google Play); add ARMv7 if targeting very old devices |
| **Texture Compression**      | ASTC (universal support on Android 5.0+); ETC2 as fallback               |
| **Minimum API Level**        | Android 8.0 (API 26) — covers 95%+ of Android devices                    |
| **Target API Level**         | Latest (required by Google Play)                                         |
| **Split Application Binary** | Enabled if APK exceeds 150 MB (splits into APK + OBB)                    |
| **Strip Engine Code**        | Enabled                                                                  |
| **Managed Stripping Level**  | High (with link.xml for preserved types)                                 |

### iOS Build Settings

| Setting                       | Value                                 |
| ----------------------------- | ------------------------------------- |
| **Scripting Backend**         | IL2CPP (required by Apple)            |
| **Target Architecture**       | ARM64                                 |
| **Texture Compression**       | ASTC (universal on iOS)               |
| **Minimum iOS Version**       | iOS 14.0 (covers 95%+ of iOS devices) |
| **Strip Engine Code**         | Enabled                               |
| **Managed Stripping Level**   | High                                  |
| **Xcode Build Configuration** | Release (for App Store submission)    |

---

## 6. Unity Packages (Essential for Mobile Games)

| Package                         | Purpose                                        | Package ID                             |
| ------------------------------- | ---------------------------------------------- | -------------------------------------- |
| **Input System**                | Modern touch/gesture input                     | `com.unity.inputsystem`                |
| **Addressables**                | Dynamic asset loading, app size reduction      | `com.unity.addressables`               |
| **Mobile Notifications**        | Push notifications for retention               | `com.unity.mobile.notifications`       |
| **Device Simulator**            | Test on virtual devices in Editor              | `com.unity.device-simulator`           |
| **Profiler**                    | Performance profiling                          | Built-in                               |
| **Memory Profiler**             | Memory leak detection                          | `com.unity.memoryprofiler`             |
| **Post Processing**             | Visual polish (color grading, bloom, vignette) | `com.unity.postprocessing`             |
| **DOTween** (third-party, free) | Animation tweens                               | Asset Store                            |
| **TextMeshPro**                 | High-quality text rendering                    | `com.unity.textmeshpro`                |
| **2D Sprite**                   | 2D sprite rendering                            | `com.unity.2d.sprite`                  |
| **2D Tilemap**                  | Tile-based level design                        | `com.unity.2d.tilemap`                 |
| **URP**                         | Universal Render Pipeline                      | `com.unity.render-pipelines.universal` |

---

## 7. Code Organization Patterns

### Recommended Architecture for Casual Mobile Games

```
Core/
├── GameManager.cs           # Singleton, game state (playing, paused, game over)
├── AudioManager.cs          # Music, SFX, volume management
├── SaveManager.cs           # Player data persistence (PlayerPrefs or encrypted save)
├── SceneManager.cs          # Scene loading, transitions
└── AnalyticsManager.cs      # Event tracking, funnel instrumentation

Gameplay/
├── <MechanicName>Controller.cs   # Core game mechanic
├── <MechanicName>View.cs         # Visual representation
└── <MechanicName>Model.cs        # Data/state for the mechanic

UI/
├── UIScreen.cs                   # Base class for all screens
├── MainMenuScreen.cs
├── GameHUD.cs
├── SettingsScreen.cs
└── StoreScreen.cs

Data/
├── GameSettings.asset            # ScriptableObject: global game configuration
├── LevelData/                    # ScriptableObjects: per-level configuration
└── EconomyConfig.asset           # ScriptableObject: currency, pricing, rewards
```

---

## 8. Version Control for Unity Projects

| Tool                                    | Recommendation                                                                               |
| --------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Git + Git LFS**                       | Sufficient for small teams. Git LFS required for binary assets (textures, models, audio).    |
| **Unity Version Control (Plastic SCM)** | Purpose-built for game development. Better handling of large binary assets and scene merges. |
| **Unity Collaborate**                   | Deprecated — do not use.                                                                     |

### Essential `.gitignore` for Unity

```
# Unity generated
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
[Uu]ser[Ss]ettings/

# OS generated
.DS_Store
Thumbs.db

# IDE
.vs/
.idea/
*.csproj
*.sln

# Unity-specific
*.pidb.meta
*.pdb.meta
*.mdb.meta
sysinfo.txt
*.apk
*.aab
*.ipa
*.unitypackage

# Addressables (generated)
AddressableAssetsData/AddressableAssetSettings.asset.backup
```

### Essential `.gitattributes` for Unity

```
# Unity meta files
*.meta text eol=lf
*.cs text eol=lf
*.shader text eol=lf

# Binary assets (force LFS)
*.png filter=lfs diff=lfs merge=lfs
*.jpg filter=lfs diff=lfs merge=lfs
*.fbx filter=lfs diff=lfs merge=lfs
*.mp3 filter=lfs diff=lfs merge=lfs
*.wav filter=lfs diff=lfs merge=lfs
*.unity filter=lfs diff=lfs merge=lfs
```

---

## 9. Unity Editor Settings for Team Consistency

| Setting                       | Recommended Value                                       |
| ----------------------------- | ------------------------------------------------------- |
| **Asset Serialization**       | Force Text (not Binary) — enables version control diffs |
| **Version Control Mode**      | Visible Meta Files                                      |
| **Sprite Packer**             | Enabled (Always Enabled)                                |
| **Color Space**               | Linear (better color accuracy for post-processing)      |
| **Virtual Reality Supported** | Disabled (unless game is VR)                            |
| **Auto Graphics API**         | Disabled for iOS (Metal only); Enabled for Android      |

---

## 10. Development Workflow Tips

| Practice                                | Description                                                                                |
| --------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Use Assembly Definitions (.asmdef)**  | Split code into logical assemblies for faster compilation and better dependency management |
| **Enable Domain Reload profiling**      | Identify slow domain reload times; target <5 seconds                                       |
| **Use Play Mode tinting**               | Prevents accidental edits during Play Mode (Edit → Preferences → Colors → Playmode tint)   |
| **ScriptableObjects for configuration** | All tunable values (speeds, prices, rewards) should be in ScriptableObjects, not hardcoded |
| **Event-driven architecture**           | Use C# events or UnityEvents for loose coupling between systems                            |
| **Object pooling**                      | Never instantiate/destroy objects at runtime in mobile games — always pool                 |

---

## 11. Recommended Learning Resources

| Resource                                              | Type                    | Link                                                                                                  |
| ----------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------- |
| Unity 6 Optimization Guides                           | Official                | https://unity.com/blog/games/optimize-your-mobile-game-performance-expert-tips-on-graphics-and-assets |
| Unity Learn — Mobile Game Dev                         | Official course         | https://learn.unity.com/                                                                              |
| "A Practical Guide to Unity Game Development in 2026" | Article                 | https://www.juegostudio.com/blog/unity-game-development-guide                                         |
| Code Monkey (YouTube)                                 | Video tutorials         | https://www.youtube.com/c/CodeMonkeyUnity                                                             |
| Jason Weimann (YouTube)                               | Architecture patterns   | https://www.youtube.com/c/JasonWeimann                                                                |
| Tarodev (YouTube)                                     | Beginner-friendly Unity | https://www.youtube.com/c/Tarodev                                                                     |

---

_End of Unity 6 Development Guide_
