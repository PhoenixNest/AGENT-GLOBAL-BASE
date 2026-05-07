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

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "workspace-knowledge": {
      "command": "uvx",
      "args": ["workspace-rag-server@latest"],
      "env": {
        "WORKSPACE_ROOT": "c:\\Users\\ASUS\\Documents\\Code\\Local\\agent-global-base",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": ["search_docs", "retrieve_context", "list_indexed_files"]
    }
  }
}
```

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
- `.kiro/steering`
- `.kiro/skills`

## Usage Examples

### Search Documentation

```typescript
// In Kiro IDE
"Search for pipeline stage gates";
// Tool: search_docs(query="pipeline stage gates", top_k=5)
```

### Retrieve File Content

```typescript
// In Kiro IDE
"Get the content of company/library/overview/pipeline.md";
// Tool: retrieve_context(file_path="company/library/overview/pipeline.md")
```

### List Indexed Files

```typescript
// In Kiro IDE
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
# (Use Kiro IDE to test tool invocations)
```

## License

MIT
