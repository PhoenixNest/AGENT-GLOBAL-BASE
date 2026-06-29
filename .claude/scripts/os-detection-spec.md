# OS Detection Specification — Cross-Platform Hook and Script Primitives

This document defines the canonical OS detection primitives used across
`.claude/scripts/` (Python) and `.claude/hooks/` (PowerShell). All new scripts and
hooks **must** draw from these primitives rather than inventing ad-hoc detection logic.

---

## Section 1 — Python Context

Use `platform.system()` from the standard library. No third-party dependency required.

```python
import platform

os_name = platform.system()  # "Windows" | "Darwin" | "Linux"

if os_name == "Windows":
    ...
elif os_name == "Darwin":
    ...
elif os_name == "Linux":
    ...
```

**Return values are exact strings — case-sensitive. Never compare with `.lower()`.**

### Extended Detection

```python
import platform, sys

os_name   = platform.system()        # "Windows" | "Darwin" | "Linux"
arch      = platform.machine()       # "AMD64" | "x86_64" | "arm64" | "aarch64"
py_ver    = sys.version_info         # (3, 11, 2, ...)
is_wsl    = "microsoft" in platform.uname().release.lower()  # True inside WSL
```

---

## Section 2 — PowerShell Context

PowerShell 7+ (pwsh) exposes three automatic boolean variables set at session start.
These variables are **not available in Windows PowerShell 5.1** — use only in `pwsh`
hooks and scripts.

```powershell
if ($IsWindows) {
    # Windows (any edition)
} elseif ($IsMacOS) {
    # macOS
} elseif ($IsLinux) {
    # Linux (including WSL)
}
```

**Fallback for Windows PowerShell 5.1:**

```powershell
$os = [System.Environment]::OSVersion.Platform  # "Win32NT" on Windows
```

---

## Section 3 — OS Reference Table

| OS      | `platform.system()` | PowerShell variable | `uname -s`  |
| ------- | ------------------- | ------------------- | ----------- |
| Windows | `"Windows"`         | `$IsWindows`        | n/a (MINGW) |
| macOS   | `"Darwin"`          | `$IsMacOS`          | `Darwin`    |
| Linux   | `"Linux"`           | `$IsLinux`          | `Linux`     |
| WSL     | `"Linux"`           | `$IsLinux`          | `Linux`     |

> WSL reports as Linux in both contexts. Use `platform.uname().release` (Python) or
> `$(uname -r)` (shell) and check for `"microsoft"` to distinguish WSL from native
> Linux when the distinction matters.

---

## Section 4 — Usage Note: Which Primitive Goes Where

| Script / Hook family   | Runtime           | Use                                    |
| ---------------------- | ----------------- | -------------------------------------- |
| `.claude/scripts/*.py` | Python            | `platform.system()`                    |
| `.claude/hooks/*.ps1`  | PowerShell (pwsh) | `$IsWindows` / `$IsMacOS` / `$IsLinux` |

**Q1 init script** (`init.py`) uses the Python primitive — `platform.system()` —
because it runs before PowerShell availability is confirmed.

**Q2 Syntax Guard** (`system-powershell-syntax-guard.ps1`) uses PowerShell automatic
variables because it runs inside a confirmed `pwsh` session as a hook.

---

## Section 5 — Example: Python Guard Block

```python
import platform, shutil, sys

def require_posix_tool(tool: str) -> str:
    """Return the full path to `tool`, or exit with a clear message."""
    os_name = platform.system()
    if os_name == "Windows":
        sys.exit(f"[init] '{tool}' is not available on Windows natively. "
                 "Use WSL or install the Windows equivalent.")
    path = shutil.which(tool)
    if path is None:
        sys.exit(f"[init] '{tool}' not found on PATH.")
    return path
```

---

## Section 6 — Example: PowerShell Guard Block

```powershell
# Portable path separator — works on all three OSes
$sep = [System.IO.Path]::DirectorySeparatorChar

if ($IsWindows) {
    $configRoot = "$env:APPDATA\claude"
} elseif ($IsMacOS -or $IsLinux) {
    $configRoot = "$HOME/.claude"
}
```
