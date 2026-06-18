# core-component-00/harness-engineering/ — Layer 3: Harness Engineering

CC-00 Layer 3 — "How to execute safely." This module provides production-grade safety infrastructure
for executing LLM model calls: error boundaries, token budget enforcement, and tool governance.

---

## What Lives Here

This module combines knowledge documentation with production-grade Python implementations and a
pytest test suite. It is one of three CC-00 modules with runnable code.

---

## Directory Structure

```
harness-engineering/
├── fundamentals/          ← Conceptual docs: execution safety, error taxonomy, budget theory
├── patterns/              ← Reusable safety patterns
├── implementations/       ← Production Python code (import from here)
│   ├── error_boundary.py       ← Timeout, rate-limit, and validation recovery
│   ├── context_monitor.py      ← Token budget enforcement
│   └── tool_registry.py        ← Tool whitelists, call limits, dangerous task detection
└── testing/               ← pytest test suite
```

---

## Key Implementations

| File                                 | Class / Entry Point | Purpose                                                                       |
| ------------------------------------ | ------------------- | ----------------------------------------------------------------------------- |
| `implementations/error_boundary.py`  | `ErrorBoundary`     | Wraps model calls with retry logic, timeout handling, and rate-limit recovery |
| `implementations/context_monitor.py` | `ContextMonitor`    | Tracks and enforces token budget limits across a session                      |
| `implementations/tool_registry.py`   | `ToolRegistry`      | Manages tool whitelists, per-tool call limits, and dangerous task detection   |

---

## Running Tests

Run from `core-component-00/` (not workspace root) to avoid import conflicts:

```powershell
pytest harness-engineering/testing/ -v
```

Tests import via `from implementations.<module>` — the module root must be on `sys.path`. The test
suite handles this automatically when run from the correct directory.

---

## Import Pattern

```python
import sys
sys.path.insert(0, "path/to/core-component-00/harness-engineering")
from implementations.error_boundary import ErrorBoundary
from implementations.context_monitor import ContextMonitor
from implementations.tool_registry import ToolRegistry
```

---

## Safety Patterns

| Pattern                  | Purpose                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------- |
| Error Boundary           | Wraps all model calls; catches and recovers from timeout, rate-limit, and validation failures |
| Token Budget Enforcement | `ContextMonitor` tracks token spend and blocks calls that would exceed the budget             |
| Tool Whitelisting        | `ToolRegistry` allows only approved tools; rejects calls outside the whitelist                |
| Dangerous Task Detection | `ToolRegistry` detects and blocks categorically dangerous tool call patterns                  |

---

## Active Research Programme

| Programme                        | Open Question                                        |
| -------------------------------- | ---------------------------------------------------- |
| Harness Performance Benchmarking | Latency cost of the full error boundary stack at p99 |

---

## Rules

- Every LLM model call in a production CC-00 system must be wrapped in an `ErrorBoundary`.
- Token budgets must be enforced via `ContextMonitor` — do not rely on ad-hoc token counting.
- Tool access must be governed by `ToolRegistry` — do not allow unrestricted tool access.
- Run tests from `core-component-00/` or the module folder, not the workspace root.
- Any implementation change must pass `pytest harness-engineering/testing/ -v` before committing.
- Never bypass safety enforcement to advance a task — this is equivalent to Trim-to-Pass and is a
  P0 defect in any ASE-governed system.
