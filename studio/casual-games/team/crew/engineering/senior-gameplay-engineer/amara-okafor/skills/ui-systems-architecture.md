# Skills — Amara Okafor

## UI Systems Architecture

**Tools:** Unity UI Toolkit 2023, C# 11, Addressables, ScriptableObjects
**Production:** Built King's unified UI framework (250M+ MAU); 40% frame time reduction via batched rendering
**Trade-offs:** Immediate mode vs retained mode → retained for performance; data-binding vs manual → data-binding for maintainability
**Standards:** ≤ 8ms UI frame budget; ≤ 35 draw calls per screen; 60fps maintained on mid-tier devices
**References:** GDC 2023 "UI Architecture at Scale" (King); Unity UI Toolkit documentation

## Input & Animation Integration

**Tools:** Unity Input System, Spine 2D, Animation Rigging, Cinemachine
**Production:** Unified touch/keyboard/gamepad input across 4 King titles; Spine integration for character animations
**Trade-offs:** Polling vs event-driven input → event-driven for responsiveness; baked vs runtime animation → runtime for flexibility
**Standards:** ≤ 16ms input latency; animation state transitions ≤ 2 frames; input buffering 120ms window
**References:** "Game Input Systems" (GDC 2022); Spine documentation; Unity Input System guide
