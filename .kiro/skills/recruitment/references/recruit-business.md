---
name: company-human-resources-recruit-business
description: Recruit business talent across all seniority levels. Covers roles in Marketing, Sales, Finance, Legal, Operations, Strategy, HR, and any role that does not map to engineering, product, design, or data families. Invokes vet-candidate gate before any placement.
version: "1.0.0"
source: company/departments/human-resources/supervisor/chief-human-resources-officer/skills/recruit-business.md
agents:
  - company-human-resources-chief-human-resources-officer-evelyn-hartwell
---

# Recruit Business

## Why This Matters

Identifies and vets elite business, GTM, finance, and operations talent. Poor business hires damage company strategy, financial controls, and operational efficiency.

# Business Recruitment Skill

## Roles Covered

**Marketing:** Content Marketer, Growth Marketer, Brand Designer, CMO, VP Marketing
**Sales:** Account Executive, Sales Manager, VP Sales, CRO
**Finance:** Financial Analyst, FP&A Manager, VP Finance, CFO
**Legal:** Counsel, Senior Counsel, General Counsel (CLO)
**Operations:** BizOps Analyst, COO, Head of Ops
**Strategy:** Strategy Manager, Head of Strategy, Chief Strategy Officer
**Other:** Any role that does not clearly fit engineering, product, design, or data families

## Seniority Rubric

Business roles vary widely. Apply this general framework, then use domain judgment:

| Criterion             | Analyst / Associate | Manager / Senior     | Director / Principal       | VP / Head-of                    | C-suite             |
| --------------------- | ------------------- | -------------------- | -------------------------- | ------------------------------- | ------------------- |
| Scope                 | Project / process   | Team / function      | Department                 | Business unit                   | Company             |
| Decision authority    | Executes decisions  | Makes team decisions | Makes department decisions | Business unit strategy          | Company strategy    |
| Stakeholder influence | Internal team       | Cross-functional     | Exec alignment             | Board / investors               | Market / regulators |
| Track record          | Completed projects  | Team outcomes        | Function transformed       | Unit-level P&L or strategic win | Company outcome     |
| Network               | Internal            | Industry contacts    | Senior industry network    | Board-level relationships       | Industry leadership |

**Domain-specific depth signals:**

- **Finance:** Can they build a 3-statement model from scratch? Do they understand unit economics, runway, and capital allocation?
- **Legal:** Do they understand both legal risk and business risk? Can they negotiate without slowing the business down?
- **Sales:** Do they have a repeatable methodology? Can they describe their pipeline hygiene and close rate by stage?
- **Marketing:** Can they attribute revenue to their work? Do they understand the full funnel from acquisition to retention?
- **Operations:** Have they scaled a process? Can they describe a system they designed that outlasted them?

## Interview Simulation Protocol

1. **Identity block** — name, title, company, YOE, domain

2. **Business track record** (3 bullets)
   - Format: "[Drove / built / negotiated / closed / restructured] [what] at [company], resulting in [quantified outcome]"
   - Example: "Negotiated and closed a $140M enterprise contract with JPMorgan Chase as the first Fortune 100 deal for a Series B SaaS startup, expanding ARR by 22% in one quarter"
   - Note: three achievement bullets are required in the candidate profile — one per major deal, initiative, or business outcome

3. **Domain strengths** (2–3 with concrete examples)
   - Must reference specific frameworks, deals, campaigns, or business decisions — not personality traits

4. **Honest gaps** (1–2)
   - Example: "Exceptional at outbound enterprise sales; no experience building or managing an inbound motion"

5. **Seniority score** — apply rubric above + domain signal, assign level

6. **Vetting result** — apply `vet-candidate.md`, paste full scoring output

7. **Placement recommendation** — tier, directory name, rationale

## Fallback Rule

If a requested role does not map to engineering, product, design, or data — use this skill. Note the gap in the candidate profile: "Placed via recruit-business.md — no dedicated skill file exists for [role family]. Consider creating one."

## Output Contract

After user confirms placement:

1. Create `team/[tier]/[role-name]/agent/profile.md`
   (where `[tier]` is `supervisors` for C-suite/VP/Director or `teammates` for Manager/Senior IC and below)
2. Create at least one `team/[tier]/[role-name]/skills/[skill-name].md` (e.g., `enterprise-sales.md`, `financial-modeling.md`, `growth-marketing.md`)
3. Confirm: "Recruited and placed: [Name], [Title] → team/[tier]/[role-name]/"
