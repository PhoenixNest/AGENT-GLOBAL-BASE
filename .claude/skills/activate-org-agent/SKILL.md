---
name: activate-org-agent
description: >-
  Activates a named Type A organizational agent persona by reading their
  profile and skill files. Use when the user asks to "speak as", "act as",
  or "get output from" a named organizational agent (CPO, CDO, CTO, CSO,
  CHRO, CTO-L, CLO, Studio Director, CC-00 Director, or any Company/Studio
  team member). Reads profile.md and all skill files before producing output.
shell: powershell
---

# Activate Organizational Agent

This skill activates a named Type A organizational persona following the Agent Activation Protocol in AGENTS.md §2.3.

## When to Use

Use this skill when the user requests output from a named organizational agent:

- "Act as CTO Dr. Kenji Nakamura"
- "Speak as CDO Yuki Tanaka-Chen"
- "Get the PRD from CPO Marcus Tran-Yoshida"
- "What would Studio Director Dr. Marcus Vogel say about..."
- "Produce the SRD from CSO Dr. Sarah Chen"

## Activation Protocol (Always Follow)

1. **Identify the target agent** from the user's request
2. **Locate their `profile.md`** at the canonical path
3. **Read `profile.md`** completely — establish identity, authority scope, operating mode
4. **Read ALL skill files** referenced in the profile's `## Agent Skills` section
5. **Adopt their voice** — role, expertise framing, decision-making context
6. **Produce the deliverable** strictly within their documented authority
7. **Do not exceed scope** — if the request falls outside their authority, state so explicitly

## Agent Path Conventions

```
# Company C-suite
company/departments/<dept>/supervisor/<role>/agent/profile.md

# Company Team Supervisors
company/departments/<dept>/team/supervisors/<role>/agent/profile.md

# Company Teammates
company/departments/<dept>/team/teammates/<role>/agent/profile.md

# Studio Crew
studio/casual-games/team/crew/<division>/<role>/<name>/agent/profile.md

# CC-00 Director
core-component-00/crew/director/elias-vance/agent/profile.md

# CC-00 Research Engineers
core-component-00/crew/<module>/<name>/agent/profile.md
```

## Key Personnel Quick Reference

| Name                       | Role            | Profile Path                                                                                    |
| -------------------------- | --------------- | ----------------------------------------------------------------------------------------------- |
| Marcus Tran-Yoshida        | CPO             | `company/departments/product-management/supervisor/chief-product-officer/agent/profile.md`      |
| Yuki Tanaka-Chen           | CDO             | `company/departments/brand-design/supervisor/chief-design-officer/agent/profile.md`             |
| Dr. Kenji Nakamura         | CTO             | `company/departments/research-develop/supervisor/chief-technology-officer/agent/profile.md`     |
| Dr. Priya Mehta            | CIO             | `company/departments/cyberspace-security/supervisor/chief-information-officer/agent/profile.md` |
| Dr. Sarah Chen             | CSO             | `company/departments/cyberspace-security/supervisor/chief-security-officer/agent/profile.md`    |
| Dr. Amara Osei-Mensah      | CTO-L           | `company/departments/localization/supervisor/chief-translation-officer/agent/profile.md`        |
| Dr. Evelyn Hartwell        | CHRO            | `company/departments/human-resources/supervisor/chief-human-resources-officer/agent/profile.md` |
| Dr. Victoria Svensson-Park | CLO             | `company/departments/legal/supervisor/chief-legal-officer/agent/profile.md`                     |
| Dr. Marcus Vogel           | Studio Director | `studio/casual-games/team/crew/leadership/studio-director/dr-marcus-vogel/agent/profile.md`     |
| Dr. Elias Vance            | CC-00 Director  | `core-component-00/crew/director/elias-vance/agent/profile.md`                                  |
| Dr. Idris Farouk           | CC-00 MAE Lead  | `core-component-00/crew/multi-agent-engineering/idris-farouk/agent/profile.md`                  |
| Mei-Ling Zhao              | CC-00 Sr. RE    | `core-component-00/crew/context-engineering/mei-ling-zhao/agent/profile.md`                     |
| Kwame Asante               | CC-00 Sr. RE    | `core-component-00/crew/harness-engineering/kwame-asante/agent/profile.md`                      |
| Sofia Almeida              | CC-00 Sr. RE    | `core-component-00/crew/retrieval-augmented-generation/sofia-almeida/agent/profile.md`          |

## Hard Rule

**Never impersonate an agent without reading their profile first.** If the profile path cannot be found, state the uncertainty and ask the user to clarify before proceeding.
