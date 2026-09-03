# Maintenance Record — workspace-knowledge Embedding-Model Cache Retrofit

| Field                          | Detail                                                                                                                                                                       |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owner**                      | Dr. Elias Vance (CC-00 Laboratory Director)                                                                                                                                  |
| **Authorized / reviewed by**   | Self-authorized — within the Director's documented authority scope                                                                                                           |
| **System / resource affected** | `workspace-knowledge` MCP server's embedding-model fallback loader (`SearchEngine._MODEL_DIR`, `workspace-knowledge/server.py`); the shared model cache at `_shared/models/` |
| **Severity**                   | P3 (routine — no live service impact; a cache-location cleanup)                                                                                                              |
| **Status**                     | Completed                                                                                                                                                                    |

---

## Pipeline Stage Log

| Stage             | Entry                                | Summary                                                                                                                                                                                                                   |
| ----------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 — Investigation | `log/01-embedding-cache-retrofit.md` | `workspace-knowledge` held a private `embedding/model/` cache duplicating a model already provisioned in the shared cache; retrofitted the fallback loader onto the shared-cache convention and removed the private copy. |

---

## Open Follow-Up Items

None.

---

## Related Records

- `.claude/rules/mcp-governance.md` — Registered Servers section, `workspace-knowledge` entry; points here for this migration's history instead of narrating it inline.
- `core-component-00/platform/model-context-protocol-servers/_shared/models/` — the shared embedding-model cache this retrofit moved `workspace-knowledge` onto.
