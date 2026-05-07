# Casual Games Pipeline Power

**Version:** 1.0.0  
**Status:** Active  
**Authority:** AGENTS.md § Part II — The Three Systems § 5. The Casual Games Studio

---

## Overview

The **Casual Games Pipeline Power** provides comprehensive support for the Casual Games Studio's 11-stage game development pipeline using Unity 6.3 LTS.

This Power packages:

- **Pipeline Documentation**: Complete 11-stage game development pipeline
- **Unity Templates**: Unity 6.3 LTS project templates and patterns
- **Steering Files**: Conditional activation for game development guidance
- **Crew Roster**: Access to 39 FTE across 7 divisions

---

## What This Power Provides

### 1. Pipeline Documentation

Access to the complete 11-stage game development pipeline:

| Stage | Name                        | Key Deliverables               | User Approval? |
| ----- | --------------------------- | ------------------------------ | -------------- |
| 0     | Art Direction + Style Guide | Style guide, art direction doc | ❌             |
| 1     | Concept (GDD + PRD + SRD)   | GDD, PRD, SRD                  | ✅             |
| 2     | Prototype (Playable + GDS)  | Playable prototype, GDS        | ✅             |
| 3     | Vertical Slice              | Vertical slice build           | ✅             |
| 4     | Production Planning         | Production plan, Gantt         | ✅             |
| 5     | Full Production             | Complete game build            | ❌             |
| 6     | Automated Testing           | Test suite, QA report          | ✅             |
| 7     | Soft Launch Prep            | Soft launch build, marketing   | ✅             |
| 8     | Soft Launch                 | Soft launch metrics, feedback  | ✅             |
| 9     | Global Launch Readiness     | Global launch build, locales   | ✅             |
| 10    | Live Ops (continuous)       | Events, updates, analytics     | QBR review     |

### 2. Studio Profile

| Field               | Detail                                                        |
| ------------------- | ------------------------------------------------------------- |
| **Engine**          | Unity 6.3 LTS                                                 |
| **Status**          | All 39 crew hired · Stage 0-ready · No projects initiated     |
| **Crew**            | 39 FTE (38 FTE + 1 Contract) across 7 divisions               |
| **Library**         | `studio/casual-games/library/`                                |
| **Strategic Brief** | `studio/casual-games/library/overview/casual-games-studio.md` |

### 3. Crew Divisions

Seven divisions support the pipeline:

| Division            | Count | Key Roles                                         |
| ------------------- | ----- | ------------------------------------------------- |
| **Leadership**      | 3     | Studio Director, Creative Director, Exec Producer |
| **Production**      | 4     | Producers, Production Coordinators                |
| **Creative-Design** | 6     | Game Designers, Level Designers                   |
| **Art**             | 9     | Art Director, Artists, Animators                  |
| **Audio**           | 3     | Composer/Sound Director, Sound Designers          |
| **Engineering**     | 10    | Game Engineers, Tools Engineers                   |
| **Live-Ops**        | 4     | Live Ops Lead, Analysts, Community Manager        |

### 4. Steering Files

Conditional steering files auto-activate when working in studio directories:

- `casual-games-pipeline.md` — 11-stage game development pipeline
- `unity-development.md` — Unity 6.3 LTS development patterns
- `game-design.md` — Game design document patterns

---

## How to Use This Power

### Activate the Power

```typescript
kiroPowers({
  action: "activate",
  powerName: "casual-games-pipeline",
});
```

### Start a New Game Project

1. **Read the strategic brief**: `studio/casual-games/library/overview/casual-games-studio.md`
2. **Review the pipeline**: `studio/casual-games/pipeline/casual-games-pipeline.md`
3. **Create project folder**: `studio/casual-games/projects/<game-slug>/`
4. **Begin at Stage 0**: Art Direction + Style Guide
5. **Follow stage gates**: Respect user approval requirements (✅)

### Key Pipeline Rules

| Rule                       | Applies At | Detail                                                              |
| -------------------------- | ---------- | ------------------------------------------------------------------- |
| **Stage 0 First**          | Always     | Every game begins with art direction and style guide                |
| **GDD + PRD + SRD Trio**   | Stage 1    | These three documents travel together through all subsequent stages |
| **Vertical Slice Quality** | Stage 3    | Must represent final game quality, not prototype quality            |
| **Soft Launch Required**   | Stage 8    | No game skips soft launch — data-driven iteration is mandatory      |
| **Live Ops Continuous**    | Stage 10   | Ongoing content, events, and community management                   |

---

## Unity 6.3 LTS Patterns

### Project Structure

```
studio/casual-games/projects/<game-slug>/
├── Assets/
│   ├── Scripts/
│   ├── Prefabs/
│   ├── Scenes/
│   ├── Materials/
│   ├── Textures/
│   └── Audio/
├── ProjectSettings/
├── Packages/
└── Documentation/
    ├── gdd.md
    ├── prd.md
    ├── srd.md
    └── style-guide.md
```

### Unity Best Practices

- **Addressables**: For asset management and memory optimization
- **DOTween**: For animation and tweening
- **TextMeshPro**: For all text rendering
- **Unity Analytics**: For player behavior tracking
- **Unity IAP**: For in-app purchases
- **Unity Ads**: For monetization

---

## Game Design Documents

### GDD (Game Design Document)

Core game design specification:

- **Core Loop**: What players do repeatedly
- **Progression**: How players advance
- **Monetization**: How the game generates revenue
- **Retention**: What brings players back
- **Social**: How players interact

### PRD (Product Requirements Document)

Product requirements from CPO perspective:

- **Target Audience**: Who plays this game
- **Market Positioning**: How it competes
- **Success Metrics**: KPIs and targets
- **Launch Strategy**: Soft launch → Global launch
- **Live Ops Plan**: Post-launch content roadmap

### SRD (Security Requirements Document)

Security requirements from CSO perspective:

- **Data Protection**: Player data security
- **Payment Security**: IAP and transaction security
- **Cheat Prevention**: Anti-cheat measures
- **Privacy Compliance**: GDPR, COPPA, etc.
- **Incident Response**: Security incident handling

---

## Related Powers

- **Company Pipeline**: Company's 13-stage development pipeline
- **CC-00 Engineering**: LLM engineering patterns for agent-powered systems
- **Organizational Agents**: Type A agent activation and management

---

## Quick Start Examples

### Example 1: Start New Game Project

```typescript
// 1. Activate the power
kiroPowers({ action: "activate", powerName: "casual-games-pipeline" });

// 2. Create project folder
// mkdir studio/casual-games/projects/puzzle-rush

// 3. Stage 0: Art Direction + Style Guide
invokeSubAgent({
  name: "studio-casual-games-art-director-renaud-leclercq",
  prompt: "Create art direction and style guide for Puzzle Rush",
  explanation: "Stage 0 deliverable creation",
});

// 4. Stage 1: GDD + PRD + SRD
invokeSubAgent({
  name: "studio-casual-games-lead-game-designer-mei-watanabe",
  prompt: "Create GDD for Puzzle Rush",
  explanation: "Stage 1 GDD creation",
});

// 5. Get user approval for Stage 1 ✅
```

### Example 2: Execute Vertical Slice (Stage 3)

```typescript
// Use pipeline-stage-executor
invokeSubAgent({
  name: "pipeline-stage-executor",
  prompt: "Execute Stage 3 (Vertical Slice) for Puzzle Rush",
  explanation: "Delegating Stage 3 execution",
  contextFiles: [
    "studio/casual-games/pipeline/casual-games-pipeline.md",
    "studio/casual-games/projects/puzzle-rush/gdd.md",
  ],
});
```

### Example 3: Soft Launch Analysis (Stage 8)

```typescript
// Activate Live Ops Lead
invokeSubAgent({
  name: "studio-casual-games-live-ops-lead-aisha-nkemelu",
  prompt: "Analyze soft launch metrics and recommend optimizations",
  explanation: "Stage 8 soft launch analysis",
  contextFiles: [
    "studio/casual-games/projects/puzzle-rush/soft-launch-metrics.md",
  ],
});
```

---

## Stage-by-Stage Guide

### Stage 0: Art Direction + Style Guide

**Owner:** Art Director (Renaud Leclercq)  
**Duration:** 1-2 weeks  
**Deliverables:**

- Art direction document
- Style guide with color palette, typography, visual language
- Reference mood boards
- Technical art constraints

**Success Criteria:**

- Clear visual identity established
- Style guide comprehensive enough for production
- Technical feasibility validated

### Stage 1: Concept (GDD + PRD + SRD)

**Owners:** Lead Game Designer, CPO, CSO  
**Duration:** 2-4 weeks  
**Deliverables:**

- Game Design Document (GDD)
- Product Requirements Document (PRD)
- Security Requirements Document (SRD)

**Success Criteria:**

- Core loop clearly defined
- Monetization strategy validated
- Security requirements documented
- User approval obtained ✅

### Stage 2: Prototype (Playable + GDS)

**Owner:** Lead Game Designer + Engineering  
**Duration:** 4-6 weeks  
**Deliverables:**

- Playable prototype (Unity build)
- Game Design Specification (GDS)
- Prototype playtest report

**Success Criteria:**

- Core loop is fun and engaging
- Technical feasibility proven
- GDS documents all systems
- User approval obtained ✅

### Stage 3: Vertical Slice

**Owner:** Full team  
**Duration:** 8-12 weeks  
**Deliverables:**

- Vertical slice build (final quality)
- All systems integrated
- Polish pass completed

**Success Criteria:**

- Represents final game quality
- All core systems working
- Performance targets met
- User approval obtained ✅

### Stage 4: Production Planning

**Owner:** Executive Producer  
**Duration:** 2-3 weeks  
**Deliverables:**

- Production plan
- Gantt chart with milestones
- Resource allocation plan
- Risk assessment

**Success Criteria:**

- Realistic timeline established
- Resources allocated
- Risks identified and mitigated
- User approval obtained ✅

### Stage 5: Full Production

**Owner:** Full team  
**Duration:** 12-24 weeks  
**Deliverables:**

- Complete game build
- All content implemented
- All features complete

**Success Criteria:**

- Feature complete
- Content complete
- Performance optimized
- Ready for testing

### Stage 6: Automated Testing

**Owner:** Lead QA Engineer  
**Duration:** 2-4 weeks  
**Deliverables:**

- Automated test suite
- QA report
- Bug database

**Success Criteria:**

- All P0/P1 bugs fixed
- Test coverage ≥ 80%
- Performance benchmarks met
- User approval obtained ✅

### Stage 7: Soft Launch Prep

**Owner:** Executive Producer + Marketing  
**Duration:** 2-3 weeks  
**Deliverables:**

- Soft launch build
- Marketing materials
- App store listings
- Analytics integration

**Success Criteria:**

- Build submitted to stores
- Analytics tracking verified
- Marketing materials ready
- User approval obtained ✅

### Stage 8: Soft Launch

**Owner:** Live Ops Lead  
**Duration:** 4-8 weeks  
**Deliverables:**

- Soft launch metrics
- Player feedback analysis
- Optimization recommendations

**Success Criteria:**

- Key metrics tracked (retention, monetization, engagement)
- Player feedback collected
- Optimization plan created
- User approval obtained ✅

### Stage 9: Global Launch Readiness

**Owner:** Executive Producer + CTO-L  
**Duration:** 2-4 weeks  
**Deliverables:**

- Global launch build
- All localizations complete
- Marketing campaign ready
- Launch plan finalized

**Success Criteria:**

- All optimizations implemented
- All locales complete
- Marketing ready
- User approval obtained ✅

### Stage 10: Live Ops (Continuous)

**Owner:** Live Ops Lead  
**Duration:** Ongoing  
**Deliverables:**

- Regular content updates
- Events and promotions
- Community management
- Analytics reports

**Success Criteria:**

- Player retention maintained
- Revenue targets met
- Community engaged
- QBR reviews conducted

---

## Unity 6.3 LTS Technical Patterns

### Architecture

```csharp
// Use dependency injection
public class GameManager : MonoBehaviour
{
    [Inject] private IPlayerService _playerService;
    [Inject] private ILevelService _levelService;

    private void Start()
    {
        // Initialize game systems
    }
}
```

### Addressables

```csharp
// Load assets asynchronously
public async Task<GameObject> LoadPrefabAsync(string key)
{
    var handle = Addressables.LoadAssetAsync<GameObject>(key);
    await handle.Task;
    return handle.Result;
}
```

### DOTween

```csharp
// Animate UI elements
public void AnimateButton(Button button)
{
    button.transform.DOScale(1.2f, 0.3f)
        .SetEase(Ease.OutBack)
        .SetLoops(2, LoopType.Yoyo);
}
```

### Unity Analytics

```csharp
// Track custom events
public void TrackLevelComplete(int level, float time)
{
    Analytics.CustomEvent("level_complete", new Dictionary<string, object>
    {
        { "level", level },
        { "time", time }
    });
}
```

---

## Monetization Patterns

### In-App Purchases (IAP)

```csharp
// Unity IAP integration
public void PurchaseProduct(string productId)
{
    IAPManager.Instance.BuyProductID(productId);
}
```

### Ad Integration

```csharp
// Unity Ads integration
public void ShowRewardedAd(Action<bool> onComplete)
{
    Advertisement.Show("rewardedVideo", new ShowOptions
    {
        resultCallback = result =>
        {
            onComplete(result == ShowResult.Finished);
        }
    });
}
```

### Subscription Model

```csharp
// Subscription management
public class SubscriptionManager
{
    public bool IsSubscribed { get; private set; }
    public DateTime ExpirationDate { get; private set; }

    public void ValidateSubscription()
    {
        // Check subscription status with backend
    }
}
```

---

## Live Ops Best Practices

### Content Updates

- **Weekly Events**: New challenges, limited-time offers
- **Seasonal Content**: Holiday themes, special events
- **Balance Updates**: Adjust difficulty, rewards
- **Bug Fixes**: Regular maintenance releases

### Player Engagement

- **Daily Rewards**: Login bonuses
- **Achievements**: Milestone rewards
- **Leaderboards**: Competitive rankings
- **Social Features**: Friend invites, gifting

### Analytics Tracking

- **Retention**: D1, D7, D30 retention rates
- **Monetization**: ARPU, ARPPU, conversion rate
- **Engagement**: Session length, sessions per day
- **Funnel**: Tutorial completion, level progression

---

## Troubleshooting

### Issue: Vertical slice doesn't represent final quality

**Solution:**

- Vertical slice must be final quality, not prototype quality
- Polish all aspects: art, audio, gameplay, UI
- Get user approval before proceeding to Stage 4

### Issue: Soft launch metrics below targets

**Solution:**

- Analyze player feedback and metrics
- Create optimization plan
- Implement changes
- Extend soft launch if needed
- Do not proceed to global launch until metrics improve

### Issue: Live ops content pipeline slow

**Solution:**

- Use Addressables for hot content updates
- Implement A/B testing framework
- Automate content deployment
- Build content creation tools

---

## References

- **Pipeline Specification**: `studio/casual-games/pipeline/casual-games-pipeline.md`
- **Studio Overview**: `studio/casual-games/library/overview/casual-games-studio.md`
- **Crew Roster**: `studio/casual-games/team/README.md`
- **AGENTS.md**: § Part II — The Three Systems § 5. The Casual Games Studio
- **Unity Documentation**: https://docs.unity3d.com/

---

**Power Maintained By:** Studio Leadership (Studio Director, Creative Director, Executive Producer)  
**Last Updated:** 2026-05-06
