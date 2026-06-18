# Asset Pipeline & Management

**Last Updated:** April 9, 2026

---

## 1. Asset Import Settings

### 2D Textures (Sprites, UI, Backgrounds)

| Setting                | Value                                                 | Rationale                                              |
| ---------------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| **Texture Type**       | Sprite (2D and UI)                                    | Enables sprite packing, 2D-specific options            |
| **Sprite Mode**        | Single (per-file sprites) or Multiple (sprite sheets) | Match source asset format                              |
| **Pixels Per Unit**    | 100 (default) or match art spec                       | Controls sprite-to-world scale                         |
| **Filter Mode**        | Bilinear (3D), Point (pixel art)                      | Bilinear for smooth scaling; Point for crisp pixel art |
| **Compression**        | ASTC 6x6 (mobile)                                     | Best quality/size ratio for mobile GPUs                |
| **Max Size**           | 1024 (UI/icons), 2048 (backgrounds)                   | Higher sizes waste memory                              |
| **Generate Mip Maps**  | Disabled (2D/UI), Enabled (3D backgrounds)            | Mip maps add 33% memory                                |
| **sRGB**               | Enabled for color; Disabled for normal maps           | Correct color space for rendering                      |
| **Read/Write Enabled** | Disabled in production                                | Doubles texture memory if enabled                      |

### 3D Models

| Setting                | Value                                          | Rationale                                    |
| ---------------------- | ---------------------------------------------- | -------------------------------------------- |
| **Scale Factor**       | 1 (or match DCC tool export scale)             | Prevents scale mismatches between assets     |
| **Mesh Compression**   | Medium or High                                 | Reduces mesh size with minimal visual impact |
| **Read/Write Enabled** | Disabled                                       | Doubles mesh memory if enabled               |
| **Normals**            | Import (or Calculate if source lacks normals)  | Required for lighting                        |
| **Tangents**           | Import (or Calculate if source lacks tangents) | Required for normal mapping                  |
| **Blend Shapes**       | Disabled (unless using facial animation)       | Adds significant memory overhead             |
| **Animation**          | Import (if model contains animations)          | Enable only if needed                        |

### Audio

| Setting           | Value                                                                             | Rationale                                    |
| ----------------- | --------------------------------------------------------------------------------- | -------------------------------------------- |
| **Force To Mono** | Enabled for SFX; Disabled for music                                               | Mono SFX uses half the memory                |
| **Load Type**     | Decompress On Load (short SFX), Streaming (music), Compressed In Memory (ambient) | Match to asset usage pattern                 |
| **Compression**   | Vorbis (mobile)                                                                   | Best quality/size ratio for mobile           |
| **Quality**       | 0.5–0.7 (SFX), 0.7–0.9 (music)                                                    | Lower quality for short SFX is imperceptible |
| **Sample Rate**   | 22050 Hz (SFX), 44100 Hz (music)                                                  | Lower rates save memory for non-music audio  |

---

## 2. Addressables System

### 2.1 Setup

1. **Install package:** Window → Package Manager → Addressables → Install
2. **Open Addressables window:** Window → Asset Management → Addressables → Groups
3. **Create default profile:** Creates default addressable group

### 2.2 Group Strategy

```
Default Local Group (built into app)
├── Core/                 # Essential startup assets
│   ├── MainMenu scene
│   ├── Loading scene
│   └── Essential UI sprites
├── Gameplay/             # Core gameplay assets
│   ├── Gameplay scene
│   ├── Core mechanic prefabs
│   └── Common VFX
└── Audio/                # Core audio
    ├── UI SFX
    └── Core game SFX

On-Demand Groups (loaded at runtime)
├── Levels/               # Per-level assets
│   ├── Level_01
│   ├── Level_02
│   └── ...
├── Seasonal/             # Remote content (downloaded from CDN)
│   ├── Season_01
│   └── Season_02
└── Cosmetics/            # Unlockable content
    ├── Skins_Pack_01
    └── Skins_Pack_02
```

### 2.3 Loading Assets with Addressables

```csharp
// Load a single asset
var handle = Addressables.LoadAssetAsync<GameObject>("level_01_prefab");
await handle.Task;
GameObject level = handle.Result;

// Load a group of assets
var groupHandle = Addressables.LoadResourceLocationsAsync("Levels/Level_01");
foreach (var location in groupHandle.Result)
{
    var assetHandle = Addressables.LoadAssetAsync<GameObject>(location);
    await assetHandle.Task;
    // Use asset...
}

// Release when done (CRITICAL — prevents memory leaks)
Addressables.Release(handle);
Addressables.Release(groupHandle);
```

### 2.4 Addressables Best Practices

| Rule                                                       | Rationale                                                                  |
| ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Address early, not retroactively**                       | Adding Addressables to an existing project requires major refactoring      |
| **Group by load/unload pattern**                           | Assets loaded and unloaded together should be in the same group            |
| **Release every handle**                                   | Unreleased handles keep assets in memory → memory leaks                    |
| **Profile with Addressables Event Viewer**                 | Identifies redundant loads, memory leaks, and loading bottlenecks          |
| **Use labels for flexible grouping**                       | Labels allow querying assets across groups (e.g., "season_01", "cosmetic") |
| **Enable "Build Remote Catalog"** for downloadable content | Enables CDN-based asset delivery                                           |

---

## 3. Third-Party Asset Management

### 3.1 Import Workflow

```
Download → Quarantine → Security Review → Import → Modification → Register in SBOM
```

### 3.2 Asset Registration (per Asset Strategy)

Every third-party asset must be registered in the SBOM before production use:

| Field                    | Description                      |
| ------------------------ | -------------------------------- |
| `asset-id`               | Unique identifier (UUID)         |
| `asset-name`             | Human-readable name              |
| `source-url`             | Download URL                     |
| `creator`                | Original creator                 |
| `license-type`           | CC0, CC-BY-4.0, Unity EULA, etc. |
| `attribution-required`   | Boolean                          |
| `attribution-text`       | Exact attribution string         |
| `security-review-status` | Passed / Failed / Pending        |
| `games-used-in`          | List of game projects            |

### 3.3 Storage Convention

```
Assets/ThirdParty/<AssetName>/
├── Original/           # Unmodified download (provenance)
│   └── <original files>
├── Modified/           # Our modifications
│   └── <modified files>
├── LICENSE.txt         # License snapshot
├── README.md           # Asset metadata, source, version
└── security-review.md  # Security review record
```

---

## 4. Sprite Atlas (2D Games)

### 4.1 What is Sprite Atlas?

Sprite Atlas packs multiple sprites into a single texture, reducing draw calls. Unity's Sprite Packer auto-generates atlases at build time.

### 4.2 Atlas Strategy

| Atlas                 | Contents                        | Purpose                                 |
| --------------------- | ------------------------------- | --------------------------------------- |
| **UI Atlas**          | All UI elements, buttons, icons | Single draw call for entire UI          |
| **Gameplay Atlas**    | Characters, obstacles, pickups  | Single draw call for gameplay objects   |
| **VFX Atlas**         | Particles, explosions, sparkles | Single draw call for all VFX            |
| **Environment Atlas** | Backgrounds, decorations        | Single draw call for static environment |

### 4.3 Creating a Sprite Atlas

1. Create → 2D → Sprite Atlas
2. Add objects to "Objects for Packing" (folders, individual sprites, or other atlases)
3. Set "Include in Build" = True
4. Configure packing settings (tight packing, padding, platform settings)
5. Pack (automatic at build time, or manual via "Pack Preview" button)

---

## 5. Texture Atlasing for 3D

| Technique                      | Tool                       | Use Case                                                          |
| ------------------------------ | -------------------------- | ----------------------------------------------------------------- |
| **Unity Sprite Atlas**         | Built-in                   | 2D games                                                          |
| **Texture Packing** (external) | TexturePacker, ShaderForge | Combine multiple textures into one atlas                          |
| **Material Property Blocks**   | Unity API                  | Vary color/texture on instanced objects without breaking batching |
| **Terrain Texture Splatting**  | Unity Terrain              | Large environment textures                                        |

---

## 6. Asset Quality Control Checklist

### Before Import

| Check                  | Criteria                                          |
| ---------------------- | ------------------------------------------------- |
| License verified       | CC0, CC-BY, or Unity EULA with commercial rights  |
| Security review passed | No malicious scripts, no unexpected network calls |
| Resolution appropriate | ≥ target resolution (not upscaled from lower res) |
| Topology clean (3D)    | No n-gons, proper UV unwrapping, consistent scale |
| Naming consistent      | Descriptive, lowercase, no spaces                 |

### After Import

| Check                   | Criteria                                              |
| ----------------------- | ----------------------------------------------------- |
| Import settings correct | Compression, max size, read/write per asset type      |
| Pivot point correct     | Center for characters, bottom for environment objects |
| Scale matches project   | 1 unit = 1 meter convention (or project-specific)     |
| Material assigned       | Correct shader (Mobile/Diffuse, Mobile/Unlit)         |
| Prefab variant created  | If modifying third-party prefabs                      |
| SBOM entry created      | All fields populated                                  |

---

## 7. External Resources

| Resource                           | Link                                                                                                  | Focus                                |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Unity Addressables Guide           | https://www.wayline.io/blog/unity-addressables-system-complete-guide                                  | Complete Addressables walkthrough    |
| Unity Mobile Optimization (Assets) | https://unity.com/blog/games/optimize-your-mobile-game-performance-expert-tips-on-graphics-and-assets | Official Unity asset optimization    |
| Kenney Assets                      | https://kenney.nl/assets                                                                              | CC0 game assets                      |
| Poly Pizza                         | https://poly.pizza/                                                                                   | CC0 low-poly 3D models               |
| Poly Haven                         | https://polyhaven.com/                                                                                | CC0 textures, HDRI, 3D models        |
| OpenGameArt                        | https://opengameart.org/                                                                              | Free game assets (check licenses)    |
| Game Asset Guidelines (licensing)  | https://gameaccessibilityguidelines.com/full-list/                                                    | Accessibility + asset considerations |

---

_End of Asset Pipeline & Management_
