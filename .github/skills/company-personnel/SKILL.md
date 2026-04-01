---
name: company-personnel
description: Complete personnel roster and agent definitions for the simulated mobile product company. Use when identifying which agent owns a task, understanding agent capabilities, or coordinating between agents. Trigger when user mentions agent names, roles, departments, or asks who owns a particular responsibility.
---

# Company Personnel Roster

This skill provides the complete personnel reference for the simulated mobile product company.

## Full Personnel Reference

The complete personnel roster is defined in this workspace's agent files and skills.

## C-Suite Agents

| Agent                 | Role                              | Pipeline Stages      | Agent File                   |
| --------------------- | --------------------------------- | -------------------- | ---------------------------- |
| Marcus Tran-Yoshida   | Chief Product Officer (CPO)       | 1, 6, 8, 10          | `marcus-tran-yoshida-cpo`    |
| Yuki Tanaka-Chen      | Chief Design Officer (CDO)        | 2, 6, 8, 10          | `yuki-tanaka-chen-cdo`       |
| Dr. Kenji Nakamura    | Chief Technology Officer (CTO)    | 3, 4, 5, 6, 7, 8, 10 | `dr-kenji-nakamura-cto`      |
| Dr. Priya Mehta       | Chief Information Officer (CIO)   | 3, 6, 8, 10          | `dr-priya-mehta-cio`         |
| Dr. Sarah Chen        | Chief Security Officer (CSO)      | 1, 6, 8, 10          | `dr-sarah-chen-cso`          |
| Dr. Evelyn Hartwell   | Chief HR Officer (CHRO)           | Recruitment only     | `dr-evelyn-hartwell-chro`    |
| Dr. Amara Osei-Mensah | Chief Translation Officer (CTO-L) | 9, 10                | `dr-amara-osei-mensah-cto-l` |

## Team Supervisors

| Agent              | Role                | Pipeline Stages | Agent File                               |
| ------------------ | ------------------- | --------------- | ---------------------------------------- |
| Rafael Okonkwo     | Software Architect  | 3, 6            | `rafael-okonkwo-software-architect`      |
| Priscilla Oduya    | Test Lead           | 7, 8            | `priscilla-oduya-test-lead`              |
| Kofi Asante-Mensah | Android Lead        | 5, 8            | `kofi-asante-mensah-android-lead`        |
| Seo-Yeon Park      | iOS Lead            | 5, 8            | `seo-yeon-park-ios-lead`                 |
| Mei-Ling Johansson | Cross-Platform Lead | 5, 8            | `mei-ling-johansson-cross-platform-lead` |

## Department → C-Suite Mapping

| Department             | Supervisor(s)                               | Key Pipeline Stages  |
| ---------------------- | ------------------------------------------- | -------------------- |
| Brand Design           | CDO (Yuki Tanaka-Chen)                      | 2, 6, 8, 10          |
| Cyberspace Security    | CIO (Dr. Priya Mehta), CSO (Dr. Sarah Chen) | 1, 3, 6, 8, 10       |
| Human Resources        | CHRO (Dr. Evelyn Hartwell)                  | Recruitment only     |
| Localization           | CTO-L (Dr. Amara Osei-Mensah)               | 9, 10                |
| Product Management     | CPO (Marcus Tran-Yoshida)                   | 1, 6, 8, 10          |
| Research & Development | CTO (Dr. Kenji Nakamura)                    | 3, 4, 5, 6, 7, 8, 10 |

## Reporting Lines

```
User
 ├── CPO  (Product Management)
 ├── CDO  (Brand Design)        → reports to CIO
 ├── CTO  (R&D)                 → reports to CIO, CSO
 ├── CIO  (Cyberspace Security) → oversees Brand Design, Product Management, R&D
 ├── CSO  (Cyberspace Security) → oversees R&D
 ├── CHRO (Human Resources)
 └── CTO-L (Localization)
```

## Agent Profiles

Full agent profiles are available via the custom agents in `.github/agents/`.
