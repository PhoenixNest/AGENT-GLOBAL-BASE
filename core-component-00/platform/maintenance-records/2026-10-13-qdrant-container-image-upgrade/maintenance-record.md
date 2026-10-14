# Maintenance Record — Qdrant Containers (`qdrant-memory`, `qdrant-workspace`)

| Field                          | Detail                                                                                                                                                                                                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owner**                      | Dr. Elias Vance, CC-00 Laboratory Director (coordinating). Operational owner: Ravi Deshmukh, Infrastructure Engineer                                                                                                                                                                              |
| **Authorized / reviewed by**   | CEO — approved removing both containers and recreating them on the latest `qdrant/qdrant` image, and approved documenting the operation here                                                                                                                                                      |
| **System / resource affected** | The two local Docker containers behind the registered MCP servers: `qdrant-memory` (`agent-memory`, host port 6335, volume `qdrant_memory_store`) and `qdrant-workspace` (`workspace-knowledge`, host port 6333, volume `qdrant_workspace_knowledge`). No server code, venv or `.mcp.json` change |
| **Severity**                   | P3 — routine image upgrade, one minor version                                                                                                                                                                                                                                                     |
| **Status**                     | Completed with follow-up open — both containers on Qdrant 1.19.2, all records intact, live search full quality on both servers; version-management policy awaiting CEO decision                                                                                                                   |

---

## Pipeline Stage Log

| Stage                               | Entry                                                                                                                               | Summary                                                                                                                                                                        |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1–4 — Investigation to Verification | `core-component-00/platform/maintenance-records/2026-10-13-qdrant-container-image-upgrade/log/01-container-recreation-on-1-19-2.md` | Both containers ran 1.18.2 from an untagged image. Stores copied out, containers recreated on 1.19.2 with the same volumes and ports. Point counts and live searches unchanged |

---

## Open Follow-Up Items

| Item                                                                                                                                                                                                                                     | Owner                             | Target                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | --------------------- |
| Version-management proposals: pin an exact image version, upgrade one minor version at a time on a schedule, copy both stores before each upgrade, keep the container setup as one saved definition, restart both containers with Docker | Ravi Deshmukh; Dr. Vance approves | On CEO decision       |
| Retention of the pre-upgrade copy in `C:\Users\ASUS\qdrant-backups\2026-10-13-pre-1.19.2\`                                                                                                                                               | Ravi Deshmukh                     | With the policy above |

---

## Related Records

- `core-component-00/platform/maintenance-records/2026-10-12-shared-embedding-model-cache-loss/maintenance-record.md` —
  the search-system repair verified on these containers immediately before the upgrade
- `.claude/rules/mcp-governance.md` — Registered Servers entries for `agent-memory` and
  `workspace-knowledge`
