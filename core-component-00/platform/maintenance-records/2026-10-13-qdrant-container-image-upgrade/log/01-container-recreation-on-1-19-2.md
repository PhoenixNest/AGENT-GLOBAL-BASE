# Log Entry 01 — Container Recreation on Qdrant 1.19.2 — 2026-10-13

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-10-13-qdrant-container-image-upgrade/maintenance-record.md`, pipeline stages 1–4 — Investigation to Verification (`core-component-00/platform/maintenance-records/pipeline.md`)                                                                                                                                                           |
| **Trigger**      | CEO approval to remove the containers running on an outdated image and recreate them on the latest `qdrant/qdrant` image, which the CEO had already pulled                                                                                                                                                                                                                                     |
| **State before** | `qdrant-memory` (host 6335→6333, 6336→6334, volume `qdrant_memory_store`) and `qdrant-workspace` (host 6333–6334, volume `qdrant_workspace_knowledge`), both on untagged image `75eab8c4ba42`, Qdrant 1.18.2, restart policy `no`, data in named volumes mounted at `/qdrant/storage`. `qdrant/qdrant:latest` present locally as image `b7b0444c4c35`, Qdrant 1.19.2 — one minor version later |

**Actions taken:**

1. Executed by the lead orchestrator under CEO authorization. No change to either server's code,
   configuration or `.mcp.json`; no write to either store.
2. Stopped both containers: `docker stop qdrant-memory qdrant-workspace`.
3. Copied both stores out of the stopped containers into
   `C:\Users\ASUS\qdrant-backups\2026-10-13-pre-1.19.2\` with `docker cp <container>:/qdrant/storage`:
   `qdrant_memory_store` (371 files) and `qdrant_workspace_knowledge` (133 files). The folder is
   outside the repository.
4. Removed both containers with `docker rm`, without `-v`, so both named volumes were kept.
5. Recreated both containers on `qdrant/qdrant:latest` with the same names, ports and volumes:
   - `docker run -d --name qdrant-workspace -p 6333:6333 -p 6334:6334 -v qdrant_workspace_knowledge:/qdrant/storage qdrant/qdrant:latest`
   - `docker run -d --name qdrant-memory -p 6335:6333 -p 6336:6334 -v qdrant_memory_store:/qdrant/storage qdrant/qdrant:latest`

**Verification:**

| Check performed                                 | Result                                                                                                               |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Version reported by each container              | Pass — both report 1.19.2                                                                                            |
| `qdrant-memory` point counts                    | Pass — `memory_episodic` 1, `memory_semantic` 0, `memory_procedural` 0, `memory_reflection` 4, identical to before   |
| `qdrant-workspace` point count                  | Pass — `workspace_knowledge` 3,957, identical to before                                                              |
| Collection status after start                   | `memory_episodic` green; the others grey (optimization not yet triggered after restart), which does not affect reads |
| Live `search_memory` through the MCP connection | Pass — returned REFLECT-002, `degraded: false`, tier 1                                                               |
| Live `search_docs` through the MCP connection   | Pass — `hybrid_qdrant`, no degradation reason; with `top_k=2` the same two results and scores as before the upgrade  |
| Containers still running after about 50 minutes | Pass — both up, same port bindings                                                                                   |

| Field                     | Detail                                                                                                                                                                                                                                                                                                         |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | Both stores run on Qdrant 1.19.2 with all records intact and full-quality search. The 1.18.2 image is no longer present on the machine, so a rollback requires pulling `qdrant/qdrant:v1.18.2` and restoring the copy from step 3. Both containers still use the floating `latest` tag and restart policy `no` |
| **Handoff to next stage** | Close. The version-management proposals and the retention of the backup copy are listed in this topic's `maintenance-record.md` Open Follow-Up Items                                                                                                                                                           |
