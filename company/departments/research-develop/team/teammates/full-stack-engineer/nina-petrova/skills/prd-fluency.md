---
version: "1.0.0"
---

| Competency                      | Description                                                                                 | Quality Criteria                                                                                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Requirements Translation        | PRD user story to technical task mapping, acceptance criteria derivation, effort estimation | Decomposes every PRD requirement into implementable tasks; writes acceptance criteria that are testable; provides effort estimates with confidence levels |
| Technical Specification Writing | Architecture diagrams, API contracts, data models, migration plans                          | Authors SPEC documents that cover all implementation aspects; includes sequence diagrams for complex flows; defines error handling for every API          |
| Edge Case Identification        | Boundary condition analysis, failure mode exploration, concurrent access patterns           | Identifies edge cases through systematic frameworks (boundary values, state transitions, concurrency); documents edge cases in SPEC before implementation |
| Trade-off Analysis              | Build vs buy evaluation, consistency vs availability decisions, performance vs complexity   | Evaluates alternatives with decision matrices; documents trade-offs with quantitative data; presents recommendations with clear rationale                 |

## Execution Guidance

### PRD to Technical Task Translation

**Translation process:**

```
PRD Requirement → Technical Analysis → Implementation Tasks → Acceptance Criteria
```

**Example: PRD requirement → technical tasks**

```
PRD Requirement:
"As a user, I want to upload profile photos so that other users can see my avatar."

Technical Analysis:
- Storage: S3 for image storage, CloudFront for CDN
- Processing: Resize to multiple sizes (thumbnail 64x64, medium 256x256, large 512x512)
- Validation: Image format (JPEG, PNG, WebP), size limit (5MB), content type check
- Security: Virus scanning, EXIF data stripping
- Database: Store S3 key, not URL; generate signed URLs for access

Implementation Tasks:
1. [S3] Configure upload bucket with lifecycle policy
2. [API] POST /users/{id}/avatar endpoint with multipart upload
3. [API] GET /users/{id}/avatar endpoint with signed URL generation
4. [Processing] Image resize pipeline (sharp library)
5. [Security] Input validation (format, size, content type)
6. [Frontend] Upload component with preview and progress
7. [Frontend] Avatar display component with fallback
8. [Testing] Integration tests for upload/download pipeline
9. [Docs] Update OpenAPI spec with avatar endpoints

Acceptance Criteria:
- [ ] User can upload JPEG/PNG/WebP up to 5MB
- [ ] Upload rejects non-image files with clear error message
- [ ] Thumbnails generated within 2 seconds of upload
- [ ] Avatar visible to other users within 5 seconds
- [ ] Old avatar deleted when new one uploaded
- [ ] EXIF data stripped from stored images
- [ ] Signed URLs expire after 1 hour
```

### Technical Specification Template

```markdown
# SPEC: User Avatar Upload

## Business Context

Users need profile photos for identification in the platform. This feature supports
user engagement and trust by providing visual identity.

## Technical Approach

Store avatars in S3 with CloudFront CDN distribution. Process uploads server-side
to generate multiple sizes. Use signed URLs for access control.

## Architecture Diagram

[PlantUML component diagram showing upload flow]

## API Contracts

### POST /users/{userId}/avatar

- Content-Type: multipart/form-data
- Body: file (image/jpeg|png|webp, max 5MB)
- Response: 200 { avatarUrl, sizes }
- Errors: 400 (invalid file), 413 (too large), 404 (user not found)

### GET /users/{userId}/avatar

- Response: 302 redirect to signed S3 URL
- Errors: 404 (no avatar)

## Data Model

ALTER TABLE users ADD COLUMN avatar_s3_key VARCHAR(255);
ALTER TABLE users ADD COLUMN avatar_updated_at TIMESTAMP;

## Migration Strategy

- Expand/contract: Add columns as nullable
- Backfill: NULL for existing users (show default avatar)
- Contract: After 30 days, make NOT NULL with default

## Rollout Phases

Phase 1: Backend API only (feature flag: avatar-upload-backend)
Phase 2: Frontend upload component (feature flag: avatar-upload-frontend)
Phase 3: Enable for 10% of users
Phase 4: Full rollout

## Success Metrics

- Upload success rate > 99%
- Average upload time < 3 seconds
- Avatar adoption rate > 40% within 30 days

## Rollback Procedure

1. Disable feature flag avatar-upload-frontend
2. Users see default avatar (no data loss)
3. Backend continues accepting uploads (for retry)
```

### Edge Case Identification Framework

**Systematic edge case categories:**

| Category              | Questions                                  | Examples                                 |
| --------------------- | ------------------------------------------ | ---------------------------------------- |
| **Boundary Values**   | What are the min/max/empty/null cases?     | Empty upload, 5MB file, 5.001MB file     |
| **State Transitions** | What happens during state changes?         | Upload interrupted, concurrent uploads   |
| **Concurrency**       | What happens with simultaneous operations? | Two uploads at once, upload + delete     |
| **Failure Modes**     | What happens when dependencies fail?       | S3 unavailable, image processing timeout |
| **Data Consistency**  | What if partial updates occur?             | DB updated but S3 upload failed          |
| **Security**          | What if malicious input?                   | Malicious image file, path traversal     |
| **Scale**             | What happens at 10x/100x volume?           | 10,000 simultaneous uploads              |
| **Localization**      | What about different regions/languages?    | File names with Unicode characters       |

**Edge case documentation in SPEC:**

```markdown
## Edge Cases

| Scenario                           | Expected Behavior                                 | Implementation                             |
| ---------------------------------- | ------------------------------------------------- | ------------------------------------------ |
| File exactly 5MB                   | Accepted                                          | Validation: `file.size <= 5 * 1024 * 1024` |
| File 5MB + 1 byte                  | Rejected with "File too large (max 5MB)"          | Same validation                            |
| Network interruption during upload | Client retries, server supports resume            | Multipart upload with part tracking        |
| Concurrent uploads for same user   | Latest upload wins, previous marked as superseded | Optimistic locking with version            |
| S3 unavailable                     | Queue upload for retry, notify user               | SQS dead letter queue                      |
| Image processing timeout (> 30s)   | Fail gracefully, store original                   | Circuit breaker on processing service      |
| User deleted during upload         | Abort upload, clean up S3 object                  | Cascade delete handler                     |
| Unicode filename                   | Sanitize and store safely                         | `sanitize-filename` library                |
| SVG file (not in allowed list)     | Rejected with "Unsupported format"                | Content-Type + magic number check          |
```

### Trade-off Analysis Framework

**Build vs Buy Decision Matrix:**

| Criterion           | Weight   | Build (Custom)           | Buy (Third-Party) |
| ------------------- | -------- | ------------------------ | ----------------- |
| Time to market      | 30%      | 3 weeks                  | 1 day             |
| Cost (3-year TCO)   | 25%      | $150K (engineering)      | $36K (licensing)  |
| Customization       | 20%      | Full control             | Limited to API    |
| Maintenance burden  | 15%      | Ongoing engineering cost | Vendor manages    |
| Vendor lock-in risk | 10%      | None                     | Medium            |
| **Weighted Score**  | **100%** | **6.2**                  | **7.8**           |

**Decision: Buy** — Third-party solution wins on speed and cost. Customization needs are within vendor API capabilities.

**Consistency vs Availability Decision:**

| Scenario              | CP (Consistency)                        | AP (Availability)                      | Decision |
| --------------------- | --------------------------------------- | -------------------------------------- | -------- |
| User profile update   | CP — user expects immediate consistency | —                                      | CP       |
| Product catalog view  | —                                       | AP — stale data acceptable for minutes | AP       |
| Payment processing    | CP — financial accuracy required        | —                                      | CP       |
| Notification delivery | —                                       | AP — delayed notification acceptable   | AP       |
| Shopping cart         | CP — user expects accurate cart state   | —                                      | CP       |
| Search results        | —                                       | AP — slightly stale index acceptable   | AP       |

**Performance vs Complexity Decision:**

```
Scenario: Real-time notification delivery

Option A: WebSocket connections to every client
  Performance: Excellent (< 100ms delivery)
  Complexity: High (connection management, horizontal scaling)
  Cost: High (persistent connections, server resources)

Option B: Short-polling every 30 seconds
  Performance: Poor (up to 30s delay)
  Complexity: Low (simple HTTP requests)
  Cost: Low (stateless, scales easily)

Option C: Server-Sent Events with reconnect
  Performance: Good (< 1s delivery)
  Complexity: Medium (event stream management)
  Cost: Medium (persistent connections, but simpler than WS)

Decision: Option C — SSE provides good performance with manageable complexity.
Auto-reconnect handles network issues. Single-direction is sufficient for notifications.
```

## Pipeline Integration

**Stage 1 (Requirements):** Full-stack engineer reviews PRD for technical feasibility. Identifies edge cases and trade-offs during requirements analysis.

**Stage 4 (Implementation Plan):** SPEC documents authored for each feature area. Technical tasks derived from PRD with acceptance criteria. Trade-off decisions documented with rationale.

**Stage 5 (Development):** Implementation follows SPEC. Edge cases handled per specification. Feature flags implemented per rollout plan.

**Stage 6 (Code Review):** Review validates implementation matches SPEC. Edge case handling verified. Acceptance criteria met.

## Quality Standards

| Metric                          | Target                                       | Measurement                 |
| ------------------------------- | -------------------------------------------- | --------------------------- |
| PRD requirement coverage        | 100% of requirements mapped to tasks         | Traceability matrix         |
| SPEC completeness               | All sections populated before implementation | SPEC review checklist       |
| Edge case coverage              | All identified edge cases handled            | Test coverage of edge cases |
| Trade-off documentation         | All significant decisions documented         | ADR/SPEC audit              |
| Acceptance criteria testability | 100% criteria are testable                   | QA review                   |
| Technical debt from MVP scope   | All deferred items documented                | Technical debt register     |
