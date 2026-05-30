# Pipeline Automation MCP Server

Tools for executing and validating pipeline stages across company and studio pipelines.

## Features

- **Stage Validation**: Validate pipeline stage gate requirements
- **Stage Advancement**: Advance projects to next pipeline stage
- **Stage Information**: Get details about specific stages
- **Project Status**: Check current status of projects
- **Multi-Pipeline Support**: Company (13 stages) and Studio (11 stages)

## Installation

```bash
# Install with uv
uv pip install -e .

# Or install from package
uvx pipeline-automation-server@latest
```

## Configuration

Registered for Claude Code in the project-root `.mcp.json`:

```json
{
  "mcpServers": {
    "pipeline-automation": {
      "command": "python",
      "args": [
        "${CLAUDE_PROJECT_DIR:-.}/.claude/mcp-servers/pipeline-automation/server.py"
      ],
      "env": {
        "WORKSPACE_ROOT": "${CLAUDE_PROJECT_DIR:-.}",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

## Tools

### `validate_stage_gate`

Validate pipeline stage gate requirements.

**Parameters:**

- `stage` (int): Stage number to validate
- `project_path` (string): Relative path to project
- `pipeline_type` (string, optional): "company" or "studio" (default: "company")

**Returns:** JSON with validation results

### `advance_stage`

Advance project to next pipeline stage.

**Parameters:**

- `stage` (int): Current stage number
- `project_path` (string): Relative path to project
- `pipeline_type` (string, optional): "company" or "studio" (default: "company")

**Returns:** JSON with advancement results

### `get_stage_info`

Get information about a specific pipeline stage.

**Parameters:**

- `stage` (int): Stage number
- `pipeline_type` (string, optional): "company" or "studio" (default: "company")

**Returns:** JSON with stage information

### `list_pipeline_stages`

List all stages in a pipeline.

**Parameters:**

- `pipeline_type` (string, optional): "company" or "studio" (default: "company")

**Returns:** JSON with list of stages

### `check_project_status`

Check current status of a project.

**Parameters:**

- `project_path` (string): Relative path to project

**Returns:** JSON with project status

## Supported Pipelines

### Company Pipeline (13 Stages)

- Stage 0: Problem Validation
- Stage 1: Requirements → PRD + SRD ✅ User Approval
- Stage 2: PRD → Web Prototype + IDS ✅ User Approval
- Stage 3: Prototype → UML Engineering Package ✅ User Approval
- Stage 4: UML → Implementation Plan + Gantt ✅ User Approval
- Stage 5: Plan → Software Development
- Stage 6: Development → Arch. & Conformance Review ✅ User Approval
- Stage 7: Arch. Review → Automated Testing ✅ User Approval
- Stage 8: Testing → Integrity Verification
- Stage 9: Integrity Verification → Translation Production
- Stage 10: Translation Production → Release Readiness ✅ User Approval
- Stage 11: Live Operations

### Studio Pipeline (11 Stages)

- Stage 0: Art Direction + Style Guide
- Stage 1: Concept (GDD + PRD + SRD) ✅ User Approval
- Stage 2: Prototype (Playable + GDS) ✅ User Approval
- Stage 3: Vertical Slice ✅ User Approval
- Stage 4: Production Planning ✅ User Approval
- Stage 5: Full Production
- Stage 6: Automated Testing ✅ User Approval
- Stage 7: Soft Launch Prep ✅ User Approval
- Stage 8: Soft Launch ✅ User Approval
- Stage 9: Global Launch Readiness ✅ User Approval
- Stage 10: Live Ops

## Usage Examples

### Validate Stage Gate

```typescript
// In Claude Code
"Validate Stage 1 requirements for the dark-mode project";
// Tool: validate_stage_gate(stage=1, project_path="projects/dark-mode", pipeline_type="company")
```

### Advance to Next Stage

```typescript
// In Claude Code
"Advance dark-mode project to Stage 2";
// Tool: advance_stage(stage=1, project_path="projects/dark-mode", pipeline_type="company")
```

### Get Stage Information

```typescript
// In Claude Code
"What are the requirements for Stage 3?";
// Tool: get_stage_info(stage=3, pipeline_type="company")
```

### List All Stages

```typescript
// In Claude Code
"Show me all stages in the company pipeline";
// Tool: list_pipeline_stages(pipeline_type="company")
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
