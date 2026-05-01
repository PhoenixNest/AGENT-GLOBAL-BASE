---
version: "1.0.0"
---

### Changelog Workflow

| Step | Action                                                                      | Actor                      | Timing                             |
| ---- | --------------------------------------------------------------------------- | -------------------------- | ---------------------------------- |
| 1    | Developer submits changelog entry via PR with code changes                  | Developer                  | At time of code change             |
| 2    | Technical Writer reviews entry for clarity, completeness, and format        | Technical Writer           | Within 2 business days             |
| 3    | Entry added to `Unreleased` section                                         | Technical Writer           | After review approval              |
| 4    | On release day, `Unreleased` section is versioned and dated                 | Technical Writer           | Day of release                     |
| 5    | Deprecation notices communicated via email, dashboard banner, and changelog | Technical Writer + Product | ≥90 days before sunset             |
| 6    | Migration guide published for any breaking changes                          | Technical Writer           | Concurrent with deprecation notice |
| 7    | Changelog published to developer portal                                     | Technical Writer           | Day of release                     |

#### Changelog Writing Standards

| Standard                         | Requirement                                                                                                                               |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Human-readable**               | Entries describe what changed and why, not just what commit was merged. "Added pagination support to list endpoints" not "Merge PR #142." |
| **Categorized**                  | Every entry is categorized: Added, Changed, Deprecated, Removed, Fixed, Security.                                                         |
| **Linked**                       | Every entry links to relevant documentation, migration guides, or issue trackers.                                                         |
| **Versioned**                    | Every release has a version number (SemVer) and release date.                                                                             |
| **Breaking changes highlighted** | Breaking changes are explicitly marked and include migration guidance.                                                                    |
| **Deprecation timeline**         | Deprecated features include a specific sunset date (≥90 days from deprecation notice).                                                    |
| **Security entries**             | Security-relevant changes are in a dedicated "Security" section with CVE references where applicable.                                     |

### Developer Experience Writing

#### DX Writing Principles

| Principle                            | Application                                                                                                               |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| **Respect developer time**           | Get to the point. No marketing language, no filler. Developers scan; they don't read novels.                              |
| **Show, don't tell**                 | Code examples > prose descriptions. A working example teaches more than three paragraphs of explanation.                  |
| **Assume intelligence, not context** | Developers are smart but don't know your system. Explain concepts; don't dumb them down.                                  |
| **Error-first mindset**              | Developers encounter errors before they encounter success. Document errors before happy paths in troubleshooting content. |
| **Consistent terminology**           | Use the same term for the same concept everywhere. If it's an "API key" on page 1, it's not an "access token" on page 5.  |
| **Progressive complexity**           | Start simple. Add complexity in layers. The quick start has no optional parameters. The API reference has all of them.    |
| **Action-oriented headings**         | "Make Your First Request" not "Request Execution." "Handle Errors" not "Error Management."                                |
| **Visual hierarchy**                 | Use headings, lists, tables, and code blocks to create scannable content. No walls of text.                               |

#### Readability Standards

| Metric                     | Target                   | Measurement                    |
| -------------------------- | ------------------------ | ------------------------------ |
| Flesch-Kincaid Grade Level | 8-10                     | Automated readability analysis |
| Average sentence length    | ≤20 words                | Automated analysis             |
| Code-to-prose ratio        | ≥40% code                | Content audit                  |
| Heading density            | 1 heading per ≤150 words | Content audit                  |
| Link density               | 1-3 links per 500 words  | Content audit                  |

#### Voice & Tone Guidelines

| Context         | Tone                              | Example                                                                            |
| --------------- | --------------------------------- | ---------------------------------------------------------------------------------- |
| Quick Start     | Direct, encouraging, concise      | "Copy your API key. You'll need it in the next step."                              |
| API Reference   | Precise, technical, neutral       | "Returns a paginated list of resources. Requires `resources:read` scope."          |
| Troubleshooting | Diagnostic, actionable, calm      | "A 401 error means the server couldn't verify your identity. Check your token."    |
| Migration Guide | Clear, structured, cautious       | "Before migrating, review the breaking changes below. Test in staging first."      |
| Changelog       | Factual, categorized, linked      | "Added `fields` query parameter for sparse fieldset support. ([Docs](#))"          |
| Error Messages  | Specific, actionable, non-blaming | "The request body is missing the required `name` field. Include `name` and retry." |
