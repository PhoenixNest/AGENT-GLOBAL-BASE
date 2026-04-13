# Mobile Gameplay Optimization

**Skill Owner:** Kaelen Reeves  
**Version:** 1.0 | **Date:** 2026-04-20

---

## Description

Performance optimization techniques specific to mobile gameplay systems: CPU/GPU profiling, memory management, GC avoidance, battery optimization, and thermal throttling mitigation.

## Tools & Frameworks

| Tool/Framework        | Version  | Context                                                      |
| --------------------- | -------- | ------------------------------------------------------------ |
| Unity Profiler        | 2023 LTS | Frame-level CPU/GPU analysis; memory allocation tracking     |
| Xcode Instruments     | 15.x     | iOS profiling: Time Profiler, Allocations, Leaks, Energy Log |
| Android GPU Inspector | 1.4      | GPU bottleneck identification; shader analysis               |
| Unity Burst Compiler  | 1.8      | SIMD optimization for gameplay calculations                  |
| Unity Jobs System     | 2023 LTS | Multi-threaded gameplay logic                                |

## Production Scenarios

### Scenario 1: GC Elimination (Supercell 2023)

**Problem:** GC spikes caused 120ms frame drops every 8-12 seconds during combat.  
**Solution:** Replaced all per-frame allocations with object pools; used struct-based data for hot paths; pre-allocated collections.  
**Result:** GC allocations reduced from 2.4MB/frame to 0.04MB/frame; frame drops eliminated; 60fps maintained consistently.

### Scenario 2: Thermal Throttling Mitigation (Supercell 2024)

**Problem:** Devices throttled after 20 minutes of gameplay, dropping from 60fps to 30fps.  
**Solution:** Implemented dynamic quality scaling; reduced particle count and shadow distance when thermal state detected; capped max CPU usage per frame.  
**Result:** Sustained 55+ fps for 60+ minute sessions on mid-tier devices; player session length increased 15%.

## Trade-off Analysis

| Decision          | Option A                 | Option B               | Chosen                      | Rationale                                    |
| ----------------- | ------------------------ | ---------------------- | --------------------------- | -------------------------------------------- |
| Memory Management | GC-tolerant with pooling | Full manual management | Pooling + struct hot paths  | Good balance of safety and performance       |
| Threading         | Single-threaded gameplay | Full Jobs System       | Jobs System for heavy tasks | Complexity justified for pathfinding/physics |
| Quality Scaling   | Fixed settings           | Dynamic thermal-aware  | Dynamic thermal-aware       | Better player experience across device range |

## Quality Standards

- Frame budget: 16.67ms total (60fps target)
- GC allocation: ≤ 0.1MB/frame on gameplay hot path
- Thermal throttling: Sustain 55+ fps for 60 min on mid-tier devices
- Battery consumption: ≤ 15%/hour on iPhone 14

## Industry Best Practice References

- GDC 2023: "Mobile Game Optimization at Supercell"
- "Optimizing Unity for Mobile" (Unity Learn, 2024)
- ARM Mobile Studio documentation
- "Game Engine Architecture" by Jason Gregory — performance chapter
