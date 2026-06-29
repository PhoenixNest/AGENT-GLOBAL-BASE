# Solution Evaluation — Q1: Cross-Platform Initialization Script

**Related Report:** `telescope/2026-06-29-cross-platform-compatibility-audit/research-report.md`  
**Date:** 2026-06-29  
**Evaluator:** Dr. Elias Vance, Laboratory Director — Core Component 00  
**Status:** Complete

---

## Summary

The CEO's proposed initialization script is technically feasible and is the correct
architectural approach to the P0 hook-executor problem. The solution has two branches:
Branch A (install `pwsh`, recommended path) delivers full hook fidelity and is
straightforward on macOS and most Linux distributions. Branch B (alternative config, no
`pwsh`) is viable as a graceful degradation path but necessarily results in silent loss of
all harness engineering behaviors unless the hooks are ported to bash — which is the
recommended Branch B implementation. The script should be a single Python file at repo root
(`init.py`), as Python is already a required dependency of this workspace and runs natively
on all three platforms without a package manager prerequisite. OS detection logic is a
direct shared primitive with Q2 (Syntax Guard upgrade) and should be extracted into a
common utility at `.claude/scripts/detect_os.py`.

---

## CEO Solution Overview

The workspace currently hardcodes `C:/PROGRA~1/PowerShell/7/pwsh.exe` as the hook executor
in all 12 hook entries of `.claude/settings.json`. This path does not exist on macOS or
Linux, silently disabling all 14 hook behaviors on non-Windows machines. The CEO's solution:

1. An initialization script runs on first workspace setup
2. It detects the current OS
3. It asks the user whether to install PowerShell (`pwsh`)
4. **Branch A (yes):** installs the latest `pwsh` for the user's platform
5. **Branch B (no):** generates an alternative `.claude/settings.json` (or
   `settings.local.json`) that works without `pwsh`
6. After either branch: workspace is ready for `claude` CLI use

---

## Feasibility Assessment

**Overall verdict: High feasibility.** All three components — OS detection, conditional
`pwsh` installation, and settings.json patching — are well-solved problems with standard
tooling. The primary complexity is Linux distro fragmentation in Branch A.

| Component                        | Feasibility | Notes                                                                                                       |
| -------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------- |
| OS detection                     | ✅ High     | `platform.system()` in Python; `uname -s` in bash                                                           |
| First-run detection              | ✅ High     | Sentinel file approach is reliable and transparent                                                          |
| Branch A: macOS pwsh install     | ✅ High     | `brew install --cask powershell` — one command, low risk                                                    |
| Branch A: Linux pwsh install     | ⚠️ Medium   | Distro fragmentation; snap is most universal but not always present                                         |
| Branch A: Windows pwsh install   | ✅ High     | `winget install Microsoft.PowerShell` — standard tooling                                                    |
| Branch B: settings.json patch    | ✅ High     | JSON manipulation is trivial in Python                                                                      |
| Branch B: bash hook translations | ✅ High     | Port all 14 `.ps1` hooks to `.sh` using bash + Python (already a prereq); no external dependencies required |

---

## Branch A: Install PowerShell

### macOS

```bash
# Check if Homebrew is installed
if command -v brew &>/dev/null; then
    brew install --cask powershell
else
    # Fallback: direct .pkg download from GitHub releases
    PWSH_URL="https://github.com/PowerShell/PowerShell/releases/latest/download/powershell-lts-osx-x64.pkg"
    curl -L "$PWSH_URL" -o /tmp/pwsh.pkg && sudo installer -pkg /tmp/pwsh.pkg -target /
fi
```

**Installed path:** `/usr/local/bin/pwsh` (Intel) or `/opt/homebrew/bin/pwsh` (Apple Silicon)

**Privilege requirement:** Homebrew cask installs are user-level. Direct `.pkg` install
requires `sudo`. Homebrew is strongly preferred.

**Edge cases:**

- Apple Silicon Macs with Homebrew installed at `/opt/homebrew` — `brew` is available but
  the PATH may differ in non-interactive shells. Verify PATH includes `/opt/homebrew/bin`.
- Corporate MDM environments may block package installs — provide a manual fallback URL.

---

### Linux

Linux has significant distro fragmentation. Recommended priority order:

```bash
if command -v snap &>/dev/null; then
    sudo snap install powershell --classic
elif command -v apt-get &>/dev/null; then
    # Debian/Ubuntu — add Microsoft repo
    wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb"
    sudo dpkg -i packages-microsoft-prod.deb
    sudo apt-get update && sudo apt-get install -y powershell
elif command -v dnf &>/dev/null; then
    # RHEL/Fedora
    sudo dnf install -y powershell
elif command -v zypper &>/dev/null; then
    # openSUSE
    sudo zypper install powershell
else
    echo "No supported package manager found. Install pwsh manually:"
    echo "https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-linux"
    exit 1
fi
```

**Installed path:** `/usr/bin/pwsh` (apt/dnf/zypper) or `/snap/bin/pwsh` (snap)

**Privilege requirement:** `sudo` required for all Linux install methods.

**Edge cases:**

- Snap requires `snapd` daemon — not present on all distros (notably Debian by default,
  minimal container images, some enterprise Linux)
- `lsb_release` may not be installed on minimal systems
- Container or cloud environments may lack sudo — document as unsupported for Branch A
- NixOS and Arch Linux are not covered — provide manual fallback URL

---

### Windows

```powershell
# Check if winget is available (Windows 10 1709+ / Windows 11)
if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install Microsoft.PowerShell --accept-source-agreements --accept-package-agreements
} else {
    # Fallback: MSI installer
    $url = "https://github.com/PowerShell/PowerShell/releases/latest/download/PowerShell-win-x64.msi"
    $dest = "$env:TEMP\PowerShell.msi"
    Invoke-WebRequest -Uri $url -OutFile $dest
    Start-Process msiexec.exe -Wait -ArgumentList "/I $dest /quiet"
}
```

**Note:** Windows users likely already have `pwsh` if they are running a modern dev
environment. The init script should check for existing installation before proceeding:
`if (Get-Command pwsh -ErrorAction SilentlyContinue) { Write-Host "pwsh already installed." }`

**Privilege requirement:** `winget` installs are user-level. MSI fallback may request UAC
elevation depending on install scope.

---

### After Branch A: Update `settings.json`

After successful `pwsh` install, the init script must update `.claude/settings.json` to
replace all 12 occurrences of `C:/PROGRA~1/PowerShell/7/pwsh.exe` with `pwsh`. This is the
same change recommended in the base audit — Branch A simply automates it.

```python
import json, re
with open(".claude/settings.json", "r") as f:
    content = f.read()
content = content.replace("C:/PROGRA~1/PowerShell/7/pwsh.exe", "pwsh")
with open(".claude/settings.json", "w") as f:
    f.write(content)
```

---

## Branch B: Alternative Configuration

> **CEO Direction (2026-06-29):** Branch B must provide offline, out-of-the-box bash
> translations of all 14 PowerShell hook scripts. Disabling hooks is not an acceptable
> fallback. PowerShell is the preferred tool; if the user declines installation, full hook
> fidelity must still be delivered via bash equivalents.

Branch B applies when the user declines `pwsh` installation. The init script generates a
POSIX-compatible `settings.json` override and ensures all 14 `.sh` hook translations are
present in `.claude/hooks/`.

### Design Constraints

- **No external dependencies** beyond `bash` and `python3` — both pre-installed on macOS
  and Linux, and Python is already a mandatory workspace prerequisite
- `jq` is **not** required — hooks that need JSON parsing use inline `python3 -c` calls
  (pure stdlib, no pip install)
- Each `.ps1` hook maps 1-to-1 to a `.sh` equivalent at `.claude/hooks/<name>.sh`
- The translated hooks are functionally identical to their PowerShell counterparts

### Translation Approach by Hook Category

| Category           | PS Construct Used          | Bash Translation                                            |
| ------------------ | -------------------------- | ----------------------------------------------------------- |
| JSON input parsing | `ConvertFrom-Json`         | `python3 -c "import sys,json; d=json.load(sys.stdin); ..."` |
| JSON output        | `ConvertTo-Json`           | `python3 -c "import json; print(json.dumps(...))"`          |
| Regex matching     | `-match '...'`             | `echo "$var" \| grep -qP '...'`                             |
| String ops         | `-replace`, `-join`        | `sed`, `printf`, parameter expansion                        |
| Date/time          | `[DateTimeOffset]::UtcNow` | `date +%s`                                                  |
| File read          | `Get-Content`              | `cat`                                                       |
| Path ops           | `Join-Path`, `Split-Path`  | `dirname`, `basename`, string concat                        |

### Effort Estimate

~8–12 hours total (14 hooks × 35–50 min each). Hooks with complex JSON I/O
(`prompt-optimizer.sh`, `pipeline-context-injector.sh`, `harness-tool-rate-limiter.sh`)
are at the higher end; simple guards (`git-line-encoding-validator.sh`,
`multi-agent-branch-naming-guard.sh`) are at the lower end.

### Branch B settings.json (hooks use bash + .sh scripts)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "defaultShell": "bash",
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(python *)",
      "Bash(prettier *)",
      "Bash(ruff *)",
      "Bash(pytest *)"
    ],
    "deny": ["Read(./GEMINI.md)", "Read(./.gemini/**)"]
  },
  "includeCoAuthoredBy": false,
  "statusLine": {
    "type": "command",
    "command": "python -u ~/.claude/statusline.py"
  },
  "subagentStatusLine": {
    "type": "command",
    "command": "python -u ~/.claude/statusline.py"
  },
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash",
            "args": [
              "-c",
              "r=$(git rev-parse --show-toplevel 2>/dev/null) && bash \"$r/.claude/hooks/prompt-quality-gate.sh\""
            ]
          },
          {
            "type": "command",
            "command": "bash",
            "args": [
              "-c",
              "r=$(git rev-parse --show-toplevel 2>/dev/null) && bash \"$r/.claude/hooks/prompt-optimizer.sh\""
            ]
          }
        ]
      }
    ]
  },
  "worktree": { "bgIsolation": "none" },
  "enabledMcpjsonServers": ["workspace-knowledge"]
}
```

Note: `defaultShell` is `bash`; the init script detects the OS and writes this file only on
POSIX platforms. The full hook list mirrors the Windows `settings.json` with `.sh`
substituted for `.ps1` throughout.

---

## Implementation Recommendation

### Script Language: Python

Use a single Python init script (`init.py`) at the repository root.

**Rationale:**

- Python is already a mandatory dependency of this workspace (MCP server requires it)
- Python's `platform` module provides reliable, cross-platform OS detection with a single
  API — no bash/PS branching at the script level
- A single file is simpler to document, test, and maintain than an `init.sh` + `init.ps1`
  pair
- Python runs natively on macOS, Linux, and Windows without a prerequisite shell

**Execution:**

```bash
# macOS / Linux
python3 init.py

# Windows PowerShell
python init.py
```

---

### Script Location: Repository Root

Place `init.py` at the repository root alongside `CLAUDE.md` and `AGENTS.md`. Add a
prominent "First-time setup" section to `AGENTS.md` or a new `SETUP.md`:

```
AGENT-GLOBAL-BASE/
├── init.py          ← Run this once after cloning
├── AGENTS.md
├── CLAUDE.md
├── ...
```

---

### First-Run Detection: Sentinel File

Create `.claude/.workspace-initialized` after successful init. Check for its existence at
script start:

```python
import os
SENTINEL = ".claude/.workspace-initialized"
if os.path.exists(SENTINEL):
    print("Workspace already initialized. Run with --force to re-run.")
    exit(0)
```

Add `.claude/.workspace-initialized` to `.gitignore` so each cloned instance starts fresh.

---

### High-Level Script Flow

```python
import platform, json, subprocess, os, sys

OS = platform.system()  # "Windows", "Darwin", "Linux"

# 1. First-run check
# 2. Detect OS
# 3. Check if pwsh is already installed
# 4. If not: prompt user for Branch A or B
# 5. Branch A: install pwsh (OS-specific commands)
# 6. Branch B: write platform-appropriate settings.json (no hooks)
# 7. Both branches: patch settings.json hook executor path → "pwsh" (Branch A only)
# 8. Both branches: patch statusLine path → "~/.claude/statusline.py"
# 9. Write sentinel file
# 10. Print summary of changes made
```

---

## Shared Primitives with Q2

Both Q1 (init script) and Q2 (Syntax Guard OS detection) require OS detection. The shared
primitive differs by runtime:

| Context         | Runtime    | Detection Method                                         |
| --------------- | ---------- | -------------------------------------------------------- |
| Q1 init script  | Python     | `platform.system()` → `"Windows"`, `"Darwin"`, `"Linux"` |
| Q2 syntax guard | PowerShell | `$IsWindows`, `$IsLinux`, `$IsMacOS` (built-in vars)     |

**These do not share code** — they run in different runtimes at different times. However,
the _logic_ is equivalent and should be documented in a shared spec.

**Recommendation:** Create `.claude/scripts/os-detection-spec.md` documenting the canonical
OS detection approach for both contexts. This ensures future hook authors and script writers
use the same detection primitives consistently.

---

## Risks and Edge Cases

| Risk                                                     | Severity | Mitigation                                                        |
| -------------------------------------------------------- | -------- | ----------------------------------------------------------------- |
| Corporate firewall blocks package manager URLs           | P1       | Document manual install fallback URLs for all platforms           |
| User has existing `.claude/settings.json` customizations | P1       | Read-modify-write JSON rather than overwriting; backup original   |
| Apple Silicon path differs from Intel                    | P2       | Detect Homebrew prefix via `brew --prefix` rather than hardcoding |
| Linux distro not in supported list                       | P2       | Provide manual URL and graceful exit with clear instructions      |
| Python 2 on legacy systems (unlikely)                    | P2       | Add `#!/usr/bin/env python3` shebang; check `sys.version_info`    |
| User runs init.py from wrong directory                   | P2       | Detect working directory; error if `CLAUDE.md` not found nearby   |
| Sentinel file committed accidentally                     | P3       | Add to `.gitignore`                                               |

---

## Open Implementation Questions (for CEO/User)

1. **Branch B depth:** ~~Should Branch B ship as B1 (disable hooks) or B2 (bash port)?~~
   **Resolved — 2026-06-29 (CEO).** Branch B must deliver full bash translations of all 14
   hooks (no hook-disabling fallback). Bash translations must use only `bash` + `python3`
   (no `jq` or other external tools). Effort: ~8–12h.

2. **Re-run behavior:** If a user runs `init.py` again after initial setup (e.g., after
   pulling changes), should it re-check and re-apply, or exit early? Recommendation:
   `--force` flag for re-run; default to exit-early with a status summary.

3. **settings.json vs. settings.local.json:** Should init.py modify `settings.json`
   (tracked in git) or write a `settings.local.json` override (untracked)? Modifying
   `settings.json` simplifies the flow but creates git noise on each setup. A
   `settings.local.json` override is cleaner but requires confirming Claude Code's merge
   semantics for this file.

4. **SETUP.md:** Should a new `SETUP.md` be created at repo root, or should the first-time
   setup instructions be added to the existing `AGENTS.md`?

---

## Next Steps

1. **CEO reviews** `q1-init-script-evaluation.md` and `q2-syntax-guard-upgrade-evaluation.md`
   before implementation begins (RQ-04 gate)
2. **Implement `init.py`** in `.claude/scripts/` with Branch A (pwsh install) and Branch B
   (bash-translated hooks) paths
3. **Write all 14 `.sh` hook translations** in `.claude/hooks/` — bash + python3 only, no
   external dependencies
4. **Extract OS detection spec** into `.claude/scripts/os-detection-spec.md` (shared
   reference with Q2 Syntax Guard upgrade)
5. **Apply P0 fixes** independently of init script: hook executor path (`pwsh`) and
   status-line path (`~/.claude/statusline.py`) in `settings.json`
6. **Apply P1 fix**: `server.py` venv bootstrap platform branch

---

**Document Version:** 1.0  
**Date:** 2026-06-29  
**Authority:** Core Component 00 Laboratory — Dr. Elias Vance
