---
name: recruit-engineering
description: Recruit engineering talent across all seniority levels. Covers Software Engineers, Staff/Principal Engineers, Engineering Managers, Directors of Engineering, VP Engineering, and CTO. Invokes vet-candidate gate before any placement.
---

# Engineering Recruitment Skill

## Roles Covered

Software Engineer (SE), Senior SE, Staff SE, Principal SE,
Engineering Manager (EM), Director of Engineering, VP Engineering, CTO.

## Seniority Rubric

Score the candidate against each criterion. Use this to assign seniority level.

| Criterion       | SE                       | Senior SE             | Staff SE                    | Principal SE                      | EM                           | Director Eng           | VP Eng               | CTO               |
| --------------- | ------------------------ | --------------------- | --------------------------- | --------------------------------- | ---------------------------- | ---------------------- | -------------------- | ----------------- |
| Scope of impact | Feature                  | Service/component     | Team/cross-team             | Org-wide                          | Team delivery                | Multi-team             | Org-wide             | Company-wide      |
| Technical depth | Implements assigned work | Designs solutions     | Defines technical direction | Shapes engineering culture        | Understands codebase broadly | Architecture standards | Engineering strategy | Technology vision |
| Leadership      | Self                     | Mentors 1–2           | Informal tech lead          | Recognized authority              | Manages 4–8                  | Manages managers       | Builds org 20–100    | C-suite exec      |
| Track record    | 1+ shipped features      | 2+ impactful projects | Cross-team technical wins   | Org-wide technical transformation | Team health + delivery       | Multi-team execution   | Org scaling          | Company outcomes  |

## Interview Simulation Protocol

When recruiting an engineering role, the CHRO must generate a candidate profile covering:

1. **Identity block**
   - Full name (realistic, diverse)
   - Current title and company
   - Years of experience
   - Education (institution, degree — only if relevant to seniority signal)

2. **Track record** (3 bullet points, each with a specific outcome)
   - Format: "[Action verb] [what] at [company], resulting in [quantified outcome]"
   - Example: "Reduced P95 API latency from 800ms to 120ms at Stripe by redesigning the fanout query pattern, cutting infrastructure costs by $2.4M annually"

3. **Technical strengths** (2–3, each with a concrete example)
   - Must name specific technologies, patterns, or systems — no vague claims

4. **Honest gaps** (1–2)
   - Be direct. Example: "Has not led an organization larger than 12 engineers. Scaling from 12 to 50 would be an open question."

5. **Seniority score** — apply the rubric table above, assign a level

6. **Vetting result** — apply `vet-candidate.md` and paste the full scoring output

7. **Placement recommendation**
   - Recommended tier: `team/supervisors/` or `team/teammates/` (as determined by the CHRO seniority map)
   - Recommended directory name (kebab-case)
   - Rationale (2 sentences)

## Output Contract

After user confirms placement:

1. Create `team/[tier]/[role-name]/agent/profile.md` — where `[tier]` is either `supervisors` or `teammates` based on seniority. Use the Recruited Agent Profile Template defined in `team/supervisor/chief-human-resources-officer/agent/profile.md`
2. Create at least one `team/[tier]/[role-name]/skills/[skill-name].md` covering their primary technical capability
3. Confirm to the user: "Recruited and placed: [Name], [Title] → team/[tier]/[role-name]/"
