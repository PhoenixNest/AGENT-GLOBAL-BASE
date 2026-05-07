# Kiro Steering Files Index

**Last Updated:** 2026-05-07  
**Total Files:** 26  
**Purpose:** Comprehensive index of all steering files, their inclusion strategies, and activation patterns

---

## What Are Steering Files?

Steering files provide additional context and instructions to Kiro during agent sessions. They can be:

- **Auto-included:** Always active in every session
- **FileMatch-included:** Automatically activated when working with matching file patterns
- **Manual-included:** Activated explicitly by the user via `#filename` context key

---

## Quick Reference

| Inclusion Type | Count | Use Case                                         |
| -------------- | ----- | ------------------------------------------------ |
| **auto**       | 2     | Universal rules needed in all sessions           |
| **fileMatch**  | 24    | Domain-specific guidance activated automatically |
| **manual**     | 0     | Explicit activation (none currently)             |

---

## Auto-Inclusion (Always Active)

These files are automatically included in every Kiro session:

### 1. `git-workflow.md`

**Purpose:** Git safety rules and multi-agent worktree patterns  
**Coverage:**

- Repository information and conventions
- Git safety rules (commit policy, destructive operations)
- Multi-agent worktree workflow (5-phase lifecycle)
- Agent roles (Orchestrator, Worker, Integration, Review)
- Branch and commit naming conventions
- Command reference

**Why Auto:** Critical safety rules to prevent destructive git operations and ensure proper multi-agent coordination.

### 2. `workspace-conventions.md`

**Purpose:** Core workspace conventions and foundational rules  
**Coverage:**

- File and folder naming conventions
- Document authority hierarchy
- Company personnel tier system
- Progress monitoring requirements
- Context and session management
- Agent types (Type A vs Type B)
- Agent activation protocol
- Authority hierarchy and user approval gates

**Why Auto:** Foundational knowledge needed in every session for proper workspace navigation and agent behavior.

---

## FileMatch Inclusion (Automatic Activation)

These files are automatically activated when working with files matching their patterns:

### CC-00 Engineering Modules (7 files)

#### `ase-framework.md`

**Pattern:** `**/agent-systems-engineering/**`  
**Purpose:** Agent Systems Engineering (ASE) governance framework  
**Activates When:** Working in ASE directories  
**Coverage:**

- ASE compliance requirements
- Five-layer integration model
- Cross-cutting design patterns
- Compliance workflow and audit process

#### `cc00-overview.md`

**Pattern:** `**/core-component-00/**`  
**Purpose:** CC-00 Laboratory overview and module navigation  
**Activates When:** Working in any CC-00 directory  
**Coverage:**

- Laboratory identity and mission
- Five-module engineering stack overview
- Key production implementations
- Active research programmes
- Quick navigation guide

#### `context-engineering.md`

**Pattern:** `**/context-engineering/**,**/*context*.py`  
**Purpose:** Context Engineering (Layer 2) patterns  
**Activates When:** Working in context-engineering directories or context-related Python files  
**Coverage:**

- Four-slot context window anatomy
- Four memory types (episodic, semantic, procedural, working)
- Context assembly patterns
- Multi-agent handoff protocol
- Token budget management

#### `harness-engineering.md`

**Pattern:** `**/harness-engineering/**,**/*harness*.py`  
**Purpose:** Harness Engineering (Layer 3) patterns  
**Activates When:** Working in harness-engineering directories or harness-related Python files  
**Coverage:**

- Error boundary patterns
- Context monitoring and budget enforcement
- Tool registry and whitelisting
- Rate limiting and timeout handling
- Safe model execution patterns

#### `multi-agent-engineering.md`

**Pattern:** `**/multi-agent-engineering/**,**/*agent*.py`  
**Purpose:** Multi-Agent Engineering (Layer 5) patterns  
**Activates When:** Working in multi-agent directories or agent-related Python files  
**Coverage:**

- Swarm orchestration patterns
- Git worktree isolation
- Context handoff protocol (Full/Scoped/Minimal)
- Agent coordination and conflict resolution

#### `prompt-engineering.md`

**Pattern:** `**/prompt-engineering/**`  
**Purpose:** Prompt Engineering (Layer 1) patterns  
**Activates When:** Working in prompt-engineering directories  
**Coverage:**

- Zero-shot, few-shot, chain-of-thought patterns
- Advanced prompt patterns (Socratic, Devil's Advocate)
- Workspace integration strategy
- Prompt stability and testing

#### `rag-engineering.md`

**Pattern:** `**/retrieval-augmented-generation/**,**/*rag*.py`  
**Purpose:** RAG Engineering (Layer 4) patterns  
**Activates When:** Working in RAG directories or RAG-related Python files  
**Coverage:**

- RAG pipeline architecture
- Retrieval strategies and reranking
- ACL filtering and PII masking
- Vector store integration
- Freshness guarantees

---

### Company Pipelines (6 files)

#### `company-pipeline-overview.md`

**Pattern:** `**/company/pipeline/**`  
**Purpose:** 13-stage company development pipeline overview  
**Activates When:** Working in any company pipeline directory  
**Coverage:**

- Complete 13-stage pipeline (Stages 0-11)
- Non-negotiable pipeline rules
- Technology decision lock (Stage 3)
- Trim-to-pass forbidden (Stage 8)
- Defect severity classification (P0-P3)
- Stage 6 remediation loop
- PRD + SRD pairing requirement

#### `mobile-pipeline.md`

**Pattern:** `**/mobile-development/**`  
**Purpose:** Mobile development pipeline (Android/iOS)  
**Activates When:** Working in mobile development directories  
**Coverage:**

- Platform coverage (Android, iOS, KMP)
- Stage-specific mobile requirements
- Mobile architecture decisions
- Mobile testing requirements
- OWASP MASVS compliance
- Mobile localization
- App store release checklist

#### `web-pipeline.md`

**Pattern:** `**/web-development/**`  
**Purpose:** Web development pipeline  
**Activates When:** Working in web development directories  
**Coverage:**

- Web-specific pipeline requirements
- Frontend framework decisions
- Browser compatibility requirements
- Web performance standards
- SEO and accessibility requirements

#### `backend-pipeline.md`

**Pattern:** `**/backend-api/**`  
**Purpose:** Backend API development pipeline  
**Activates When:** Working in backend API directories  
**Coverage:**

- API architecture patterns
- Database design requirements
- API security standards
- Performance and scalability requirements
- API documentation standards

#### `full-stack-pipeline.md`

**Pattern:** `**/full-stack/**`  
**Purpose:** Full-stack development pipeline  
**Activates When:** Working in full-stack directories  
**Coverage:**

- Full-stack architecture patterns
- Frontend-backend integration
- End-to-end testing requirements
- Deployment and DevOps standards

#### `recruitment-pipeline.md`

**Pattern:** `**/recruitment/**`  
**Purpose:** 9-stage recruitment pipeline  
**Activates When:** Working in recruitment directories  
**Coverage:**

- Complete 9-stage recruitment process
- Hiring plan authorship
- Candidate vetting and assessment
- Interview and evaluation standards
- Offer and onboarding process

---

### Studio Pipelines (1 file)

#### `casual-games-pipeline.md`

**Pattern:** `**/studio/casual-games/**`  
**Purpose:** 11-stage game development pipeline  
**Activates When:** Working in Casual Games Studio directories  
**Coverage:**

- Complete 11-stage game pipeline (Stages 0-10)
- Unity 6.3 LTS standards
- Stage-specific game development requirements
- Soft launch and global launch process
- Live ops and game metrics
- Game-specific defect severity

---

### Platform-Specific Development (3 files)

#### `android-development.md`

**Pattern:** `**/*.kt,**/*.java,**/android/**,**/build.gradle.kts,**/build.gradle`  
**Purpose:** Android/Kotlin development patterns  
**Activates When:** Working with Kotlin/Java files or Android project files  
**Coverage:**

- Kotlin best practices
- Android architecture patterns (MVVM, Clean Architecture)
- Material Design 3 guidelines
- Android testing (JUnit, Espresso)
- OWASP MASVS security standards
- Performance optimization

#### `ios-development.md`

**Pattern:** `**/*.swift,**/ios/**,**/Podfile,**/Package.swift,**/project.pbxproj`  
**Purpose:** iOS/Swift development patterns  
**Activates When:** Working with Swift files or iOS project files  
**Coverage:**

- Swift best practices
- iOS architecture patterns (MVVM, TCA)
- Human Interface Guidelines
- iOS testing (XCTest, XCUITest)
- iOS security standards
- Performance optimization

#### `cross-platform-development.md`

**Pattern:** `**/cross-platform/**`  
**Purpose:** KMP and Flutter development patterns  
**Activates When:** Working in cross-platform directories  
**Coverage:**

- Kotlin Multiplatform (KMP) patterns
- Flutter development standards
- Shared code architecture
- Platform-specific implementations
- Cross-platform testing

---

### Architecture & Engineering (4 files)

#### `frontend-architecture.md`

**Pattern:** `**/frontend/**`  
**Purpose:** Frontend architecture patterns  
**Activates When:** Working in frontend directories  
**Coverage:**

- Frontend framework patterns (React, Vue, Angular)
- State management
- Component architecture
- Frontend testing
- Performance optimization

#### `backend-architecture.md`

**Pattern:** `**/backend/**`  
**Purpose:** Backend architecture patterns  
**Activates When:** Working in backend directories  
**Coverage:**

- Backend framework patterns (Node.js, Python, Go)
- API design patterns
- Database architecture
- Microservices patterns
- Backend testing

#### `localization-engineering.md`

**Pattern:** `**/localization/**`  
**Purpose:** i18n and localization engineering  
**Activates When:** Working in localization directories  
**Coverage:**

- i18n pipeline and workflow
- Translation management systems (TMS)
- String externalization
- RTL support
- Locale-specific formatting

#### `security-architecture.md`

**Pattern:** `**/security/**,**/*security*.md,**/*auth*.ts,**/*auth*.py,**/*auth*.kt,**/*auth*.swift`  
**Purpose:** Security architecture and OWASP best practices  
**Activates When:** Working with security-related files or authentication code  
**Coverage:**

- OWASP Top 10 (2021)
- OWASP MASVS (Mobile)
- OWASP ASVS (Web)
- Authentication and authorization patterns
- Cryptography best practices
- Security testing (SAST, DAST)

---

### Quality & Testing (1 file)

#### `quality-assurance.md`

**Pattern:** `**/testing/**,**/qa/**`  
**Purpose:** Testing standards and QA processes  
**Activates When:** Working in testing or QA directories  
**Coverage:**

- Testing pyramid (unit, integration, E2E)
- Test coverage requirements
- Automated testing standards
- Manual testing processes
- Defect tracking and severity classification

---

### Game Development (2 files)

#### `unity-development.md`

**Pattern:** `**/unity-project/**,**/*.unity,**/*.prefab,**/*.asset,**/*.cs`  
**Purpose:** Unity 6.3 LTS development patterns  
**Activates When:** Working with Unity project files or C# scripts  
**Coverage:**

- Unity project structure
- C# coding standards
- Performance best practices (object pooling, optimization)
- Addressables system
- Dependency injection (Zenject, VContainer)
- UI best practices
- Mobile optimization
- Unity testing

#### `game-design.md`

**Pattern:** `**/gdd.md,**/gds.md,**/game-design/**`  
**Purpose:** Game design document patterns  
**Activates When:** Working with game design documents  
**Coverage:**

- GDD (Game Design Document) structure
- GDS (Game Design Specification) structure
- Core loop design patterns
- Progression and monetization design
- Balancing guidelines
- Playtesting and metrics

---

## Manual Inclusion (Explicit Activation)

**Current Count:** 0

All steering files now use auto or fileMatch inclusion for better user experience.

---

## Usage Guide

### For Users

**Automatic Activation:**

- Most steering files activate automatically when you work with relevant files
- No action needed — Kiro will load the appropriate context

**Checking Active Steering:**

- Kiro will mention which steering files are active when relevant
- Look for "Steering File:" headers in responses

**Manual Activation (if needed):**

- Use `#filename.md` in chat to explicitly activate a steering file
- Example: `#security-architecture.md` to activate security guidance

### For Agents

**Reading Steering Files:**

1. Check which steering files are active based on current file context
2. Follow the guidance provided in active steering files
3. Reference authority sources (AGENTS.md sections) when needed
4. Cross-reference related steering files for comprehensive coverage

**Steering File Priority:**

1. Auto-inclusion files (always active)
2. FileMatch files (active when pattern matches)
3. Manual files (active when explicitly requested)
4. AGENTS.md (ultimate authority)

---

## Maintenance

### Adding New Steering Files

1. Create the file in `.kiro/steering/`
2. Add proper frontmatter with inclusion strategy
3. Update this README.md index
4. Run Prettier: `prettier --write .kiro/steering/README.md`
5. Commit with message: `kiro: add <filename> steering file`

### Updating Existing Steering Files

1. Make changes to the steering file
2. Update version number if significant changes
3. Update this README if inclusion strategy changes
4. Run Prettier on modified files
5. Commit with descriptive message

### Reviewing Steering Files

- Run analysis: Review `.kiro/steering/ANALYSIS.md`
- Check for schema compliance
- Verify inclusion strategies are appropriate
- Ensure no contradictions with AGENTS.md

---

## Related Documentation

- **AGENTS.md** — Workspace agent orientation guide (ultimate authority)
- **ANALYSIS.md** — Steering files compliance analysis report
- **Company Library** — `company/library/` for company-specific documentation
- **Studio Library** — `studio/casual-games/library/` for studio documentation
- **CC-00 Documentation** — `core-component-00/` for LLM engineering patterns

---

## Statistics

| Category                   | Count  |
| -------------------------- | ------ |
| Auto-Inclusion             | 2      |
| CC-00 Modules              | 7      |
| Company Pipelines          | 6      |
| Studio Pipelines           | 1      |
| Platform-Specific          | 3      |
| Architecture & Engineering | 4      |
| Quality & Testing          | 1      |
| Game Development           | 2      |
| **Total**                  | **26** |

---

---

## Recent Updates

### 2026-05-07: Steering File Optimization Project

**Status:** ✅ Complete

**Improvements Made:**

1. ✅ **Converted 3 manual files to fileMatch** — `android-development.md`, `ios-development.md`, `security-architecture.md` now activate automatically
2. ✅ **Added version numbers to all files** — 100% coverage (26/26 files now versioned)
3. ✅ **Enhanced pattern coverage** — Unity patterns now include prefabs/assets; Game design includes GDS files
4. ✅ **Added cross-references** — CC-00 modules now have bidirectional navigation
5. ✅ **Created comprehensive documentation** — This index, implementation summary, and enhancements report

**Impact:**

- Manual inclusion files: 3 → 0 (100% reduction)
- Version coverage: 81% → 100% (+19%)
- Cross-references: Partial → Complete
- Auto-activation: 88% → 100% (+12%)

**Documentation:**

- `ANALYSIS.md` — Initial compliance analysis
- `IMPLEMENTATION-SUMMARY.md` — Core recommendations implementation
- `ENHANCEMENTS-COMPLETE.md` — Future enhancements implementation

---

**Index Maintained By:** Kiro AI Assistant  
**Last Updated:** 2026-05-07  
**Next Update:** When new steering files are added or inclusion strategies change
