# Casual Games Studio — Asset Strategy Addendum

**Document Type:** Asset Sourcing & Compliance Strategy  
**Status:** C-Suite Review Complete  
**Date:** April 9, 2026  
**Parent Document:** `casual-games-studio.md`  
**Directive:** All game assets must be "legal, compliant, free of charge, and licensed for commercial use"

---

## 1. Executive Summary

The CEO has confirmed that **budget is not a constraint** for personnel or infrastructure costs. The studio directive is to use only free, commercially-licensed game assets to maximize revenue. Three officers — CTO, CDO, and CSO — have assessed this directive from their respective domains.

**Consensus verdict:** Viable for hyper-casual and casual segments, with three non-negotiable conditions:

1. A rigorous **asset license registry and attribution automation system** (CTO + CSO)
2. A **security review pipeline** for every asset before production use (CSO)
3. A **visual unification pipeline** (post-processing, VFX, custom UI) to achieve premium feel (CDO)

**Key tension identified:** "Free assets" are free in acquisition cost but carry significant engineering and design labor costs. The relevant metric is **Total Cost of Asset (TCA)** — not the purchase price, but the sum of acquisition + integration time + maintenance time + risk premium.

---

## 2. Approved Asset Sources (Tier List)

### Tier 1 — Primary Sources (High Reliability)

| Source                               | Asset Types                             | License                           | Attribution Required?               |
| ------------------------------------ | --------------------------------------- | --------------------------------- | ----------------------------------- |
| **Kenney.nl**                        | 2D sprites, 3D models, UI, audio, fonts | CC0                               | No                                  |
| **Unity Asset Store (Free Section)** | Complete packages, systems, art         | Unity Asset Store EULA            | Per-asset (must check individually) |
| **OpenGameArt.org**                  | 2D, 3D, audio, tilesets, UI             | Mixed (CC0, CC-BY, CC-BY-SA, GPL) | Per-asset (must check individually) |
| **Itch.io (Free Assets)**            | Sprites, tilesets, audio, fonts, UI     | Mixed (creator-defined)           | Per-asset (must check individually) |

### Tier 2 — Supplementary Sources (Good Quality, Niche Focus)

| Source            | Asset Types                   | License                      | Attribution Required?              |
| ----------------- | ----------------------------- | ---------------------------- | ---------------------------------- |
| **Poly Pizza**    | Low-poly 3D models            | CC0                          | No                                 |
| **Poly Haven**    | HDRI, textures, 3D models     | CC0                          | No                                 |
| **AmbientCG**     | PBR textures, 3D scans        | CC0                          | No                                 |
| **Freesound.org** | Audio effects, ambient, music | Mixed (CC0, CC-BY, CC-BY-NC) | Per-asset; **filter out CC-BY-NC** |

### Tier 3 — Use with Caution

| Source                                                          | Notes                                                                     |
| --------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Public domain repositories** (Wikimedia, Library of Congress) | Useful for historical/educational themes; quality varies wildly           |
| **GitHub open-source game projects**                            | Code assets well-licensed (MIT/Apache); art asset licensing often unclear |

### Excluded by Policy

| License                       | Reason for Exclusion                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| **CC-BY-NC (Non-Commercial)** | Prohibited by our commercial mandate                                                 |
| **CC-BY-SA (ShareAlike)**     | Viral licensing — derivatives must carry same license, compromising our IP ownership |
| **GPL-licensed code**         | Copyleft could require open-sourcing our entire game codebase                        |
| **Unclear/unstated license**  | If the license is not explicitly stated, the asset is not usable                     |

---

## 3. Asset License Classification Framework

| License Category           | Commercial Use            | Attribution                                     | Derivative Works                           | Viral Risk                                         | Our Policy                              |
| -------------------------- | ------------------------- | ----------------------------------------------- | ------------------------------------------ | -------------------------------------------------- | --------------------------------------- |
| **CC0 (Public Domain)**    | Yes                       | No                                              | Unrestricted                               | None                                               | ✅ **Primary target**                   |
| **CC-BY 4.0**              | Yes                       | Yes (credit + license link + modification note) | Allowed (inherits CC-BY)                   | None                                               | ✅ Acceptable with attribution tracking |
| **Unity Asset Store EULA** | Yes (Unity projects only) | Per-asset                                       | Allowed within Unity                       | Medium                                             | ✅ Acceptable with per-asset tracking   |
| **MIT License (code)**     | Yes                       | Yes (copyright notice)                          | Allowed (separate licensing for additions) | None                                               | ✅ Low risk                             |
| **Apache 2.0 (code)**      | Yes                       | Yes (notice + changes documented)               | Allowed (separate licensing for additions) | None (patent grant included)                       | ✅ Low risk                             |
| **CC-BY-SA 4.0**           | Yes                       | Yes                                             | Must carry same license                    | **High** — entire derivative work must be CC-BY-SA | 🚫 **Excluded**                         |
| **GPL v3 (code)**          | Yes                       | Yes                                             | Must release source under GPL              | **Extreme** — entire project may need to be GPL    | 🚫 **Excluded**                         |

---

## 4. Asset Security Review Pipeline

**Mandatory for ALL third-party assets, regardless of source reputation.** (CSO)

```
Download → Quarantine → Static Analysis → Import (test project) → Runtime Verification → Approval → Production
```

### Phase 1 — Quarantine (Before Import)

- Download to isolated staging directory (NOT directly into Unity `Assets/`)
- Catalog all files: extensions, sizes, directory structure
- Flag any `.dll`, `.exe`, `.bat`, `.sh`, or script files for manual review

### Phase 2 — Static Analysis

- **DLLs**: Decompile with ILSpy/dnSpy. Verify no unexpected network calls, file system access, or reflection
- **Prefabs**: Open in text mode (Unity YAML). Search for unexpected `m_Script` references, suspicious serialized data
- **Editor scripts**: Review ALL code in `Editor/` folders — these execute with full Unity editor permissions
- **Shaders**: Review for unusual compute patterns that could perform unauthorized computation

### Phase 3 — Import & Runtime Verification

- Import into a **clean test project** first — not production
- Monitor network traffic (Fiddler/Charles Proxy/Wireshark) during execution
- Profile CPU/GPU for unexpected computational load (crypto mining detection)
- Check `Application.persistentDataPath` for unexpected file writes
- Verify no unexpected `PlayerPrefs` keys are written

### Phase 4 — Approval

- Only after all phases pass does the asset move to the production library
- Record review outcome in SBOM (reviewer, date, findings, verdict)

---

## 5. Software Bill of Materials (SBOM)

**Non-negotiable.** Every asset must be registered in a structured asset registry before entering production. (CTO + CSO)

### SBOM Schema

| Field                      | Purpose                                 |
| -------------------------- | --------------------------------------- |
| `asset-id`                 | Unique identifier (UUID or hash)        |
| `asset-name`               | Human-readable name                     |
| `version`                  | Asset version                           |
| `source-url`               | Download URL                            |
| `creator`                  | Original creator                        |
| `license-type`             | CC0, CC-BY-4.0, Unity EULA, etc.        |
| `license-url`              | Link to full license text               |
| `license-snapshot-date`    | Date license terms were captured        |
| `attribution-required`     | Boolean                                 |
| `attribution-text`         | Exact attribution string for credits    |
| `commercial-use-confirmed` | Boolean                                 |
| `security-review-status`   | Passed / Failed / Pending               |
| `security-reviewer`        | Name of reviewer                        |
| `security-review-date`     | Date of review                          |
| `games-used-in`            | List of game projects                   |
| `intake-date`              | Date asset entered library              |
| `modified`                 | Boolean — whether we modified the asset |
| `modification-summary`     | Description of changes made             |

### Attribution Automation Pipeline

```
Asset Registry (YAML/Markdown source)
    ↓  [Build-time script: Python/Node]
credits.txt (formatted attribution text)
    ↓
Unity Resources/credits.txt (runtime-readable)
    ↓
In-game CreditsScreen UI (auto-populated)
```

**In-game credits display:** Grouped by asset type ("Art by...", "Music by...", "Sound Effects by..."), sorted alphabetically. Auto-generated from registry — **never manually maintained**.

### Archive Requirements

| Artifact                                  | Retention | Purpose                              |
| ----------------------------------------- | --------- | ------------------------------------ |
| Original asset file (unmodified)          | Permanent | Provenance evidence if challenged    |
| License snapshot (screenshot/Wayback URL) | Permanent | License terms at time of acquisition |
| SBOM entry                                | Permanent | Single source of truth               |
| Security review record                    | Permanent | Audit trail                          |
| Shipped game credits screenshots          | Permanent | Proof of attribution compliance      |

---

## 6. Visual Coherence Strategy

The CDO's assessment: free assets from different sources will **not** look cohesive without a unification layer. Three strategies are recommended:

### Strategy A: Runtime Unification (Highest Impact)

| Technique                                                                        | Impact | Effort     |
| -------------------------------------------------------------------------------- | ------ | ---------- |
| **Post-processing stack** (color grading LUT, bloom, vignette)                   | ★★★★★  | Low        |
| **Custom Unity shader** (consistent outlines, cel-shading, texture filtering)    | ★★★★★  | Medium     |
| **Global lighting design** (shared HDRI, rim lighting, baked lightmaps)          | ★★★★☆  | Medium     |
| **Master color palette** (6–8 core colors + 2 accents, batch-recolor all assets) | ★★★★☆  | Low–Medium |

### Strategy B: The "Juice Layer" (Premium Feel)

Every player action triggers a minimum of **3 feedback responses** (visual + animation + audio + haptic):

| Technique                                                                              | Impact | Effort |
| -------------------------------------------------------------------------------------- | ------ | ------ |
| **Particle VFX** on every interaction (clicks, scores, transitions, victories/defeats) | ★★★★★  | Medium |
| **Animation curves** (easing, anticipation, overshoot — replace linear motion)         | ★★★★☆  | Low    |
| **Screen feedback** (shake on impact, flash on hit, slow-mo on critical moments)       | ★★★★☆  | Low    |
| **Custom typography & UI** (animated transitions, micro-interactions on every button)  | ★★★★★  | Medium |
| **Transition design** (no hard cuts — use wipes, fades, camera moves)                  | ★★★★☆  | Medium |

### Strategy C: Brand Differentiation

| Strategy                                                                            | Effectiveness | Investment |
| ----------------------------------------------------------------------------------- | ------------- | ---------- |
| **Custom UI/UX shell** — distinctive UI framework wrapping all gameplay             | High          | Medium     |
| **2–3 custom hero assets** — mascot character, signature environment, unique weapon | Very High     | Medium     |
| **Signature VFX style** — unique particle effects that become brand identity        | High          | Medium     |
| **Branded framing** — custom logos, animated intros, consistent typography          | Medium        | Low        |
| **Gameplay-driven identity** — let mechanics, not visuals, be the differentiator    | Very High     | High       |

**CDO's recommendation:** Invest in custom UI design + 2–3 hero assets as brand anchors. Everything else can be free/modified. Players remember the mascot and the menu — they don't remember background tiles.

---

## 7. Quality Gate Pipeline

All sourced assets pass through three quality gates before production use:

```
Asset Ingestion
    ↓
[QC Gate 1] Visual/Audio Audit
    ├── Resolution/texture quality ≥ 1024px
    ├── Polygon count appropriate for mobile
    ├── Art style consistency check
    └── Audio quality ≥ 44.1kHz, 16-bit minimum
    ↓ (Pass → Proceed | Fail → Reject or Flag for Modification)
[QC Gate 2] Technical Audit + Security Review
    ├── Rigging/skinning integrity (3D)
    ├── Animation state machine compatibility
    ├── Import warnings/errors in Unity
    ├── Performance profiling (draw calls, memory footprint)
    ├── Static analysis (DLL decompilation, prefab YAML review)
    └── Runtime verification (network monitoring, CPU/GPU profiling)
    ↓ (Pass → Proceed | Fail → Reject)
[QC Gate 3] Style Cohesion Review
    ├── Does this asset match the established art direction?
    ├── Can we modify it to match? (CC-BY/CC0 allow modification)
    └── If not, reject regardless of individual quality
    ↓ (Pass → Approved for Production | Fail → Reject)
```

---

## 8. COPPA/GDPR-K Compliance Screening

Free assets may bundle third-party SDKs that introduce unauthorized data collection. Controls:

| Control                                                                                                       | Description |
| ------------------------------------------------------------------------------------------------------------- | ----------- |
| **SDK inventory** — inventory all network-capable components in every third-party asset                       |
| **Network usage screening** — flag any `UnityWebRequest`, `HttpClient`, `WWW`, or ad/analytics SDK references |
| **Default "no tracking" posture** — disable all analytics/advertising SDKs for games that may attract minors  |
| **Legal review** — any asset bundling an SDK requires legal counsel review before inclusion                   |
| **Data collection inventory** — document every data flow per game, mapped to privacy policy                   |

---

## 9. The Total Cost of Asset (TCA) Framework

The CTO's key insight: **free in acquisition does not mean free in total cost.**

```
TCA = Acquisition Cost + (Integration Time × Hourly Rate) + (Maintenance Time × Hourly Rate) + Risk Premium
```

### Concrete Example

| Scenario                                                         | Asset Cost | Engineering Time             | Total Cost             |
| ---------------------------------------------------------------- | ---------- | ---------------------------- | ---------------------- |
| Free inventory system (4 stars, 200 downloads, buggy)            | $0         | 3 days debugging and fixing  | **3 engineering days** |
| Paid inventory system (5 stars, 2,000 downloads, active support) | $25        | 2 hours import and configure | **$25 + 2 hours**      |

**The "free" asset is 12× more expensive** when engineering time is the valued resource.

### CTO's Modified Policy Recommendation

Given that budget is not a constraint:

| Policy                                                                                                                                           | Priority |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| **Default to CC0 assets** (Kenney.nl, Poly Pizza, Poly Haven) — genuinely free, zero obligations                                                 | **P0**   |
| **Exclude CC-BY-SA and GPL assets** by policy — viral licensing risk                                                                             | **P0**   |
| **Allow paid assets when TCA analysis shows they are cheaper** — if a $20 asset saves 2+ engineering days, it is the economically correct choice | **P1**   |
| **Never invest >4 hours fixing a free asset** — if it needs more work, it has already exceeded the cost of a quality paid alternative            | **P1**   |
| **Invest engineering time in custom tooling, not custom asset fixes** — automation creates genuine competitive advantage                         | **P1**   |

---

## 10. Immediate Action Items

| #   | Action                                                                           | Owner     | Priority |
| --- | -------------------------------------------------------------------------------- | --------- | -------- |
| 1   | Establish Asset SBOM registry before acquiring any third-party assets            | CTO + CSO | **P0**   |
| 2   | Implement security review pipeline (Section 4) as mandatory gate                 | CSO       | **P0**   |
| 3   | Adopt CC0-first sourcing policy (Kenney.nl, Poly Pizza, Poly Haven as primary)   | CTO       | **P0**   |
| 4   | Exclude CC-BY-SA and GPL assets by policy                                        | CSO + CTO | **P0**   |
| 5   | Create style guide and art direction brief BEFORE sourcing any assets            | CDO       | **P0**   |
| 6   | Build attribution automation pipeline (registry → auto-generated credits screen) | CTO       | **P1**   |
| 7   | Design and implement post-processing + VFX "juice layer" system                  | CDO + CTO | **P1**   |
| 8   | Commission 2–3 custom hero assets (mascot, signature environment)                | CDO       | **P1**   |
| 9   | Archive original downloads with SHA-256 hashes from Day 1                        | CSO       | **P1**   |
| 10  | Engage IP legal counsel for license framework validation + COPPA posture         | CSO + CIO | **P1**   |

---

## 11. Document Version History

| Version | Date          | Author          | Changes                                                                       |
| ------- | ------------- | --------------- | ----------------------------------------------------------------------------- |
| v1      | April 9, 2026 | CTO + CDO + CSO | Initial asset strategy addendum — technical, design, and security assessments |

---

_End of Asset Strategy Addendum_
