# Skill Changelog Template

> Copy this file to each skill's directory as `CHANGELOG.md`. Update on every modification.

## Format

Use [Semantic Versioning](https://semver.org/) for the `version:` field in `SKILL.md` frontmatter.
Each changelog entry must include: version, date, author, change type, and description.

### Change Types

| Type         | When to Use                                                                          |
| ------------ | ------------------------------------------------------------------------------------ |
| `ADDED`      | New sections, references, scripts, or capabilities added to the skill                |
| `CHANGED`    | Existing content modified, restructured, or updated                                  |
| `DEPRECATED` | Feature or section marked for future removal                                         |
| `REMOVED`    | Feature or section deleted                                                           |
| `FIXED`      | Bug fix, typo correction, broken link repair, factual error correction               |
| `SECURITY`   | Security-related change (e.g., updated crypto standards, removed vulnerable pattern) |

## Changelog

<!-- Format each entry as: -->
<!-- ## [version] — YYYY-MM-DD — [Author] — [TYPE] -->
<!-- - [Description of change] -->

## [1.0.0] — YYYY-MM-DD — [Author] — ADDED

- Initial skill creation

---

_When incrementing version:_

- _**Patch** (1.0.0 → 1.0.1): Typos, formatting, minor clarifications, broken link fixes_
- _**Minor** (1.0.0 → 1.1.0): New sections, reference files, trigger context updates, owner changes_
- _**Major** (1.0.0 → 2.0.0): Breaking changes to skill behavior, removed sections, rewritten structure_
