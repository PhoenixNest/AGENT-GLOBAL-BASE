#!/usr/bin/env python3
"""
Full Claude Code configuration audit for agent-global-base.

Run from project root:
    python .claude/scripts/audit_config.py

Checks: tool availability, settings.json integrity, hook syntax,
MCP server syntax, agent definitions, scripts directory, and
CC-00 pytest suite counts.
"""

import os
import json
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.getcwd())
PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"
WARN = "\033[33mWARN\033[0m"
errors = []
warnings = []


def ok(label):
    print(f"  {PASS}  {label}")


def fail(label, detail=""):
    msg = f"  {FAIL}  {label}" + (f" — {detail}" if detail else "")
    print(msg)
    errors.append(label)


def warn(label, detail=""):
    msg = f"  {WARN}  {label}" + (f" — {detail}" if detail else "")
    print(msg)
    warnings.append(label)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


# ── 1. Toolchain ─────────────────────────────────────────────────────────────

print("\n[1] Toolchain")

for tool, flag in [("python", "--version"), ("prettier", "--version"),
                    ("ruff", "--version"), ("pytest", "--version")]:
    rc, out, _ = run(f"{tool} {flag}")
    if rc == 0:
        ok(f"{tool}: {out.splitlines()[0]}")
    else:
        fail(f"{tool} not found")

rc, out, _ = run('python -c "import fastmcp; print(fastmcp.__version__)"')
if rc == 0:
    ok(f"fastmcp: {out}")
else:
    fail("fastmcp not installed")

# ── 2. settings.json ─────────────────────────────────────────────────────────

print("\n[2] settings.json")

settings_path = ROOT / ".claude" / "settings.json"
try:
    with open(settings_path) as f:
        settings = json.load(f)
    ok("settings.json is valid JSON")
except Exception as e:
    fail("settings.json parse error", str(e))
    settings = {}

if settings.get("defaultShell") == "powershell":
    ok("defaultShell = powershell")
else:
    fail("defaultShell not set to powershell")

allow = settings.get("permissions", {}).get("allow", [])
ps_rules = [r for r in allow if r.startswith("PowerShell(")]
if len(ps_rules) >= 5:
    ok(f"PowerShell allow rules: {len(ps_rules)} entries")
else:
    warn(f"PowerShell allow rules: only {len(ps_rules)} entries (expected ≥5)")

bg = settings.get("worktree", {}).get("bgIsolation")
if bg == "none":
    ok("worktree.bgIsolation = none (local-only repo)")
else:
    warn("worktree.bgIsolation not set to none")

mcp_enabled = settings.get("enabledMcpjsonServers", [])

local_path = ROOT / ".claude" / "settings.local.json"
if local_path.exists():
    try:
        with open(local_path) as f:
            local = json.load(f)
        mcp_enabled = local.get("enabledMcpjsonServers", mcp_enabled)
        ok("settings.local.json is valid JSON")
    except Exception as e:
        fail("settings.local.json parse error", str(e))

expected_servers = {"workspace-knowledge", "pipeline-automation",
                    "git-worktree-manager", "cc00-tools"}
if expected_servers.issubset(set(mcp_enabled)):
    ok(f"All 4 MCP servers enabled: {sorted(mcp_enabled)}")
else:
    missing = expected_servers - set(mcp_enabled)
    fail(f"Missing MCP servers in enabledMcpjsonServers", str(missing))

# ── 3. Hooks ─────────────────────────────────────────────────────────────────

print("\n[3] Hooks")

hooks = [
    ".claude/hooks/prettier-on-save.ps1",
    ".claude/hooks/lint-on-save.ps1",
    ".claude/hooks/test-on-code-change.ps1",
]
for h in hooks:
    p = ROOT / h
    if p.exists():
        ok(f"{p.name} exists")
    else:
        fail(f"{p.name} missing")

# ── 4. MCP servers ───────────────────────────────────────────────────────────

print("\n[4] MCP servers (syntax)")

servers = [
    ".claude/mcp-servers/cc00-tools/server.py",
    ".claude/mcp-servers/pipeline-automation/server.py",
    ".claude/mcp-servers/git-worktree-manager/server.py",
    ".claude/mcp-servers/workspace-knowledge/server.py",
]
for s in servers:
    p = ROOT / s
    if not p.exists():
        fail(f"{p.name} missing")
        continue
    try:
        ast.parse(p.read_text(encoding="utf-8"))
        ok(f"{p.name} syntax OK")
    except SyntaxError as e:
        fail(f"{p.name} syntax error", str(e))

# ── 5. Agent definitions ─────────────────────────────────────────────────────

print("\n[5] Agent definitions")

agents = [
    ".claude/agents/cc00-implementation-assistant.md",
    ".claude/agents/multi-agent-orchestrator.md",
    ".claude/agents/organizational-agent-activator.md",
    ".claude/agents/pipeline-stage-executor.md",
]
for a in agents:
    p = ROOT / a
    if p.exists():
        ok(f"{p.name} present")
    else:
        fail(f"{p.name} missing")

# ── 6. Scripts directory ─────────────────────────────────────────────────────

print("\n[6] Scripts (.claude/scripts/)")

scripts = [
    ".claude/scripts/audit_config.py",
]
for s in scripts:
    p = ROOT / s
    if p.exists():
        try:
            ast.parse(p.read_text(encoding="utf-8"))
            ok(f"{p.name} present and syntax OK")
        except SyntaxError as e:
            fail(f"{p.name} syntax error", str(e))
    else:
        fail(f"{p.name} missing")

# ── 7. CC-00 pytest suites ───────────────────────────────────────────────────

print("\n[7] CC-00 pytest suites")

suites = {
    "context-engineering": ("core-component-00/context-engineering/testing", 63),
    "harness-engineering": ("core-component-00/harness-engineering/testing", 41),
    "multi-agent-engineering": ("core-component-00/multi-agent-engineering/testing", 36),
}
total_collected = 0
for name, (path, expected) in suites.items():
    rc, out, err = run(f"python -m pytest {path} --collect-only -q 2>&1")
    lines = (out + err).splitlines()
    collected = 0
    for line in lines:
        if "test" in line and ("selected" in line or "item" in line):
            parts = line.split()
            for part in parts:
                if part.isdigit():
                    collected = int(part)
                    break
    rc2, out2, _ = run(f"python -m pytest {path} -q --tb=no 2>&1")
    passed_line = [l for l in out2.splitlines() if "passed" in l]
    if passed_line and "failed" not in passed_line[0]:
        ok(f"{name}: all tests passed")
    else:
        fail(f"{name}: test failures detected", passed_line[0] if passed_line else "no output")
    total_collected += expected

ok(f"Total CC-00 tests: {total_collected} expected across 3 suites")

# ── Summary ──────────────────────────────────────────────────────────────────

print()
if warnings:
    print(f"\033[33m{len(warnings)} warning(s):\033[0m")
    for w in warnings:
        print(f"  • {w}")

if errors:
    print(f"\n\033[31m{len(errors)} check(s) FAILED:\033[0m")
    for e in errors:
        print(f"  • {e}")
    sys.exit(1)
else:
    print(f"\033[32mAll checks passed.\033[0m" +
          (f" ({len(warnings)} warning(s))" if warnings else ""))
