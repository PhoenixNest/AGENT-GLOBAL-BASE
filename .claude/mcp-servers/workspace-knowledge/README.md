# Workspace Knowledge MCP Server

RAG server for workspace documentation search and retrieval.

## Features

- **Semantic Search**: Search across all workspace documentation
- **Full Context Retrieval**: Retrieve complete file contents
- **Index Management**: List and rebuild the document index
- **Fast Performance**: Simple keyword-based search for quick results

## Installation

```bash
# Install with uv
uv pip install -e .

# Or install from package
uvx workspace-rag-server@latest
```

## Configuration

Registered for Claude Code in the project-root `.mcp.json`:

```json
{
  "mcpServers": {
    "workspace-knowledge": {
      "command": "python",
      "args": [
        "${CLAUDE_PROJECT_DIR:-.}/.claude/mcp-servers/workspace-knowledge/server.py"
      ],
      "env": {
        "WORKSPACE_ROOT": "${CLAUDE_PROJECT_DIR:-.}",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

Tool permissions are granted in `.claude/settings.json` under `permissions.allow` (e.g. `mcp__workspace-knowledge__search_docs`).

## Tools

### `search_docs`

Search workspace documentation using keyword search.

**Parameters:**

- `query` (string): Search query
- `top_k` (int, optional): Number of results (default: 5)

**Returns:** JSON with search results

### `retrieve_context`

Retrieve full content for a specific file.

**Parameters:**

- `file_path` (string): Relative path from workspace root

**Returns:** JSON with file content

### `list_indexed_files`

List all files in the RAG index.

**Returns:** JSON with list of indexed files

### `rebuild_index`

Rebuild the RAG index from workspace files.

**Returns:** JSON with rebuild status

## Indexed Directories

- `company/library`
- `company/pipeline`
- `company/departments`
- `studio/casual-games/library`
- `studio/casual-games/pipeline`
- `core-component-00`
- `.claude/rules`
- `.claude/skills`

## Usage Examples

### Search Documentation

```typescript
// In Claude Code
"Search for pipeline stage gates";
// Tool: search_docs(query="pipeline stage gates", top_k=5)
```

### Retrieve File Content

```typescript
// In Claude Code
"Get the content of company/library/overview/pipeline.md";
// Tool: retrieve_context(file_path="company/library/overview/pipeline.md")
```

### List Indexed Files

```typescript
// In Claude Code
"Show me all indexed documentation files";
// Tool: list_indexed_files()
```

## Development

```bash
# Install dependencies
uv pip install -e .

# Run server locally
python server.py

# Test tools
# (Use Claude Code to test tool invocations)
```

## License

MIT
