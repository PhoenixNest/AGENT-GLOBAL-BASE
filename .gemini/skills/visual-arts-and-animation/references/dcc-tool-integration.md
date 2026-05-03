---
name: studio-art-dcc-tool-integration
description: DCC tool integration and pipeline standardization for Maya, Blender, and Substance Painter/Designer into a Unity-based casual game art pipeline — export settings, naming conventions, plugin setup, and round-trip workflows. Owned by Lena Kovac (Technical Artist). Use during Studio Pipeline Stages 2–6 (Automated Testing). Trigger: DCC, Maya, Blender, Substance Painter, DCC pipeline, asset export, tool integration, 3D software.
version: "1.0.0"
---

# DCC Tool Integration

**Skill Owner:** Lena Kovac (Technical Artist)
**Applies To:** Maya, Blender, Substance Painter/Designer, Houdini (FX), Unity Integration

## Studio DCC Stack

| Tool               | Version | Usage                                               |
| ------------------ | ------- | --------------------------------------------------- |
| Maya               | 2024    | Character and prop modeling, rigging, animation     |
| Blender            | 4.x     | Environment art, supplemental modeling              |
| Substance Painter  | 9.x     | Texture authoring for characters and props          |
| Substance Designer | 13.x    | Tileable material creation for environments         |
| Photoshop          | CC 2024 | UI texture authoring, sprite sheets                 |
| Houdini            | 20.x    | Procedural VFX (used by Javier Moreno — VFX Artist) |
| Unity              | 6 LTS   | Engine host; receives all DCC output                |

## Export Standards by Asset Type

### Character Meshes (Maya → Unity)

| Setting          | Value                                                                  |
| ---------------- | ---------------------------------------------------------------------- |
| Export format    | FBX 2020                                                               |
| Scale            | 1 Unity unit = 1 meter (apply scale before export: `Ctrl+A` → `Scale`) |
| Forward axis     | Z-forward                                                              |
| Up axis          | Y-up                                                                   |
| Smoothing groups | Export from Maya (per-face normals baked)                              |
| Rig              | Include skeleton; bind pose at frame 0                                 |
| Animations       | Export as separate FBX per animation clip                              |
| Naming           | `CHR_<CharacterName>_<variant>_v<version>.fbx`                         |

### Environment Assets (Maya/Blender → Unity)

| Setting      | Value                                      |
| ------------ | ------------------------------------------ |
| Pivot point  | Base of asset (Y=0)                        |
| Scale        | Real-world scale; 1 unit = 1 meter         |
| UV channel 0 | Diffuse/albedo UV (0–1 space, no overlaps) |
| UV channel 1 | Lightmap UV (if baked lighting used)       |
| Naming       | `ENV_<SetName>_<AssetName>_v<version>.fbx` |

### Textures (Substance Painter → Unity via Substance export preset)

| Channel      | File Name Suffix | Format | Notes                                 |
| ------------ | ---------------- | ------ | ------------------------------------- |
| Albedo/Color | `_A`             | PNG    | sRGB color space                      |
| Normal Map   | `_N`             | PNG    | Linear; DirectX-style (flip G)        |
| Mask (MAOR)  | `_M`             | PNG    | Linear; R=Metallic, G=AO, B=Roughness |
| Emissive     | `_E`             | PNG    | Linear; only if needed                |

**Substance Painter export preset:** Lena maintains a Unity URP-compatible export preset in the studio's shared Substance Painter project settings. All artists use this preset — manual channel configuration is not permitted.

## Round-Trip Workflow (Unity ↔ DCC)

For assets requiring iteration between DCC and Unity:

1. Artist works in DCC; exports to `Assets/Art/[Category]/[AssetName]/` using the batch export script (see `art-pipeline-optimization.md`)
2. Unity auto-reimports via `AssetPostprocessor`; compression and import settings applied automatically
3. Artist views the asset in Unity's Scene view within ~30 seconds of export
4. If adjustments needed, artist modifies in DCC and re-exports — no manual Unity reimport needed

## Real-World Production Scenario

### Scenario: Onboarding a New 3D Artist to the DCC Pipeline

**Context:** Anya Petrova joins as a 3D Artist; needs to be productive on day 3.
**Process:**

1. Lena shares the Studio Art Bible and DCC Integration Guide (this document, plus naming conventions reference)
2. Lena walks Anya through the batch export script for Maya (30-minute demo)
3. Anya exports a test asset; Lena reviews it in Unity and provides feedback on anything that deviates from the standard
4. Anya completes a small "integration exercise" — model a prop, texture in Substance, integrate in Unity — before touching production assets
5. First production asset is reviewed by Lena before submission to the weekly art review

## Measurable Quality Standards

| Standard                     | Target                             | Measurement Method             |
| ---------------------------- | ---------------------------------- | ------------------------------ |
| DCC-to-engine iteration time | ≤2 minutes per export cycle        | Manual measurement             |
| Export standard compliance   | 100% of assets on first submission | Validation tool report         |
| Onboarding to productive     | ≤3 days for a new artist           | Time-to-first-production-asset |
