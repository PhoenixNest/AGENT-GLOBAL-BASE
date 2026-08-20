# core-component-00/mcp-servers/ — CC-00 MCP Server Implementations

Production MCP server implementations exposed to Claude Code. This is the lab's deployment
surface — architecturally distinct from the five-module research stack under `engineering/` and
`retrieval-augmented-generation/`, though it depends on them.

---

## What Lives Here

Two live MCP servers, a shared model-provisioning convention, and a shared internal embedding
process (`embedder-service`) both servers depend on but which is not itself registered in
`.mcp.json`:

```
mcp-servers/
├── workspace-knowledge/     ← Document knowledge base (BM25 + semantic search over qdrant-workspace)
├── agent-memory/            ← Persistent agent memory (episodic/semantic/procedural/reflection over qdrant-memory)
└── _shared/
    ├── provision_model.py    ← Shared embedding-model provisioning (writes to _shared/models/<slug>/)
    └── embedder-service/     ← Persistent localhost-only HTTP embedding process; both servers route
                                 embed calls through it when available, each falling back to its own
                                 private in-process model load if it isn't. Not an MCP server itself —
                                 see .claude/rules/mcp-governance.md "Shared Infrastructure" section.
```

Each server carries its own `README.md` — read that first for the server's tool contract,
configuration, and setup. This file is a thin index, not a duplicate; do not let facts drift
between here and either README.

---

## Python Environment — Per-Server Venvs

**Each server runs from its own virtual environment** — `workspace-knowledge/.venv/` and
`agent-memory/.venv/`, each with its own `pyproject.toml`/`uv.lock` — not a single shared venv.

```
mcp-servers/
├── workspace-knowledge/.venv/   ← workspace-knowledge's own environment (gitignored)
└── agent-memory/.venv/          ← agent-memory's own environment (gitignored)
```

`embedder-service` does not get its own venv — `embedder_client.py` spawns it with
`sys.executable`, so it always runs under whichever server's venv started it.

**The one invariant per-server venvs depend on:** `torch` and `sentence-transformers` version
pins in `workspace-knowledge/pyproject.toml` and `agent-memory/pyproject.toml` **must stay
identical**. This is what actually makes `embedder-service`'s behavior deterministic regardless of
which server starts it first — not which venv layout is in use. Check both files whenever either
pin is bumped; a silent drift here is the one failure mode a shared venv would have prevented for
free.

**How the interpreter is selected — three places must agree:**

| Location                                      | Mechanism                                                                                                                                                                                                                                     |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.mcp.json`                                   | `"command"` points directly at each server's own venv interpreter — `<server>/.venv/Scripts/python.exe` on Windows, `<server>/.venv/bin/python` on Linux/macOS (not bare `"python"`, and not `"uv"` — see the 2026-08-13 incident note below) |
| `embedder_client.py`                          | Inherits automatically via `sys.executable` — no configuration needed                                                                                                                                                                         |
| `embedder-service/manage_embedder_service.py` | Resolves whichever server's venv spawned it, via the inherited interpreter — no separate venv of its own; `EMBEDDER_SERVICE_PYTHON` overrides if ever needed                                                                                  |

> **A bare `"python"` — or `"uv"` — anywhere in this chain is a defect.** Both resolve via `PATH`
> to whatever the spawning process's own environment happens to contain. `"python"` risks a
> system-wide, possibly CPU-only interpreter. `"uv"` failed for a different reason on 2026-08-13:
> the Claude Code host process spawns MCP servers using its own long-lived process environment,
> which does not necessarily match a freshly-opened shell's `PATH` — a `uv` install added to the
> user `PATH` after the host process started is invisible to it until the host itself restarts,
> not just on `/mcp reconnect`. `.mcp.json`'s `"command"` must therefore be an absolute or
> `${CLAUDE_PROJECT_DIR:-.}`-relative path to a concrete interpreter, never a bare command name
> resolved via `PATH`. Full incident record:
> `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
>
> **Cross-platform consequence:** because `.mcp.json` cannot branch on OS, a single checked-in
> file cannot auto-resolve both `Scripts/python.exe` (Windows) and `bin/python` (Linux/macOS)
> without either a `PATH`-resolved indirection (proven unreliable above) or a hardcoded,
> OS-specific literal (the current state). A Linux/macOS deployment of this workspace must edit
> both `.mcp.json` entries' `"command"` to
> `${CLAUDE_PROJECT_DIR:-.}/core-component-00/mcp-servers/<server>/.venv/bin/python` — a one-line,
> documented change per server, not an automatic one. Full record:
> `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.

**`sys.path` and `sys.executable` are not interchangeable.** Inserting a `site-packages` directory
at `sys.path[0]` affects _imports in the current process only_ — it does not change
`sys.executable`, so it cannot redirect a spawned subprocess. A server doing that would import one
torch installation while the `embedder-service` it spawns imports a different one. Only the
`"command"` in `.mcp.json` governs what a subprocess inherits, which is why the interpreter is
pinned there rather than bootstrapped in code.

Each `server.py` still inserts two paths — the `context-engineering` module root and the
`_shared` root — so cross-module imports resolve. Those are import-path plumbing for first-party
code, not environment selection; neither points at a `site-packages` directory.

**CUDA is required, not optional.** Each venv holds `torch==2.13.0+cu130`. A CPU-only build costs
roughly **16–21× on batch embedding** and **~6.5× on the live query path** — measured on this
machine against 512 real workspace chunks, with CPU and GPU output numerically identical (mean
cosine similarity 1.000000), so the CUDA build carries no retrieval-quality risk. The two resident
models occupy ~570 MB of VRAM. `pip install torch==2.13.0` is a
**silent no-op** against an installed `+cpu` build because pip ignores the local version tag when
base versions match; the local version must be pinned explicitly, per server:

```bash
# Linux/macOS — repeat for each server directory
core-component-00/mcp-servers/<server>/.venv/bin/python -m pip install "torch==2.13.0+cu130" --index-url https://download.pytorch.org/whl/cu130
```

```powershell
# Windows — repeat for each server directory
core-component-00\mcp-servers\<server>\.venv\Scripts\python.exe -m pip install "torch==2.13.0+cu130" --index-url https://download.pytorch.org/whl/cu130
```

Each server's `pyproject.toml` declares its real imports and carries `[tool.uv.sources]` so `uv`
selects the CUDA index automatically — running `uv sync` from within `<server>/` is the normal
path; the manual `pip install` above is only needed if a venv's torch build needs correcting
after the fact.

---

## Governance

Every server registered here must pass the Three-Gate Inclusion Test (Capability, Governance,
Completeness) before being added to root `.mcp.json`. Full gate definitions, the Registered
Servers status table — including open caveats and incident history — and the retirement
procedure are the authoritative source of truth at `.claude/rules/mcp-governance.md`. Treat that
file, not this one or either server's README, as canonical if they ever disagree.

---

## Where to Look

| I need…                                      | Go to                                |
| -------------------------------------------- | ------------------------------------ |
| A server's tools, contract, setup            | `<server>/README.md`                 |
| Gate status, caveats, incident history       | `.claude/rules/mcp-governance.md`    |
| Shared embedding-model provisioning          | `_shared/provision_model.py`         |
| Shared embedding process (not an MCP server) | `_shared/embedder-service/server.py` |

---

## Ownership

Owned by **CC-00 Lab**, reporting to **Dr. Elias Vance** (Lab Director). Per-server executing
engineers are listed in each server's own README.
