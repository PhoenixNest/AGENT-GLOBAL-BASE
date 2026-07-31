#!/usr/bin/env python3
"""
init.py — Cross-Platform Workspace Initialization Script
.claude/scripts/init.py

Phases 4a/4b of the cross-platform compatibility hardening plan.
Run once to configure the Claude Code workspace for the current OS.

Usage:
    python .claude/scripts/init.py           # normal run (skips if already initialized)
    python .claude/scripts/init.py --force   # re-run even if sentinel exists

settings.json is a single, OS-agnostic file since the Phase 3 cutover: every hook
runs via "uv run ${CLAUDE_PROJECT_DIR}/.claude/hooks/<name>.py" (exec form, no
shell), so there is no per-OS settings.json variant to select or copy anymore.
This script's remaining OS-specific work is orthogonal to hook execution:
    Windows            — pwsh path: normalizes any absolute pwsh path left in
                          settings.json, and installs pwsh if needed, for the
                          INTERACTIVE PowerShell tool (CLAUDE.md §1), not hooks.
    macOS/Linux/WSL     — sets the machine-local interactive defaultShell to bash.

Both paths conclude with patch_statusline() and sentinel file creation.

PowerShell detection order on Windows:
    1. pwsh       — PowerShell 7+ cross-platform edition (must be installed separately)
    2. powershell — Windows PowerShell 5.x (built-in; always present on Windows)
    Settings.json hooks require pwsh; PS 5.x alone is insufficient.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).resolve().parent          # .claude/scripts/
_CLAUDE_DIR = _SCRIPT_DIR.parent                       # .claude/
_SETTINGS   = _CLAUDE_DIR / "settings.json"
_LOCAL_SETTINGS = _CLAUDE_DIR / "settings.local.json"
_SENTINEL      = _CLAUDE_DIR / ".workspace-initialized"

# Regex matching any absolute path to pwsh/pwsh.exe (any drive, any install dir).
_PWSH_PATH_PATTERN = re.compile(r'[A-Za-z]:[/\\][^\s",]+[/\\]pwsh(?:\.exe)?', re.IGNORECASE)
_PORTABLE_PWSH     = "pwsh"

# Pattern matching any absolute statusline path; patch_statusline() replaces with ~-form.
_STATUSLINE_PATTERN  = re.compile(r'python -u [^\s"\\]+statusline\.py')
_PORTABLE_STATUSLINE = "python -u ~/.claude/statusline.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _log(msg: str) -> None:
    print(f"[init] {msg}", flush=True)


def _read_settings() -> dict:
    """Load settings.json and return the parsed dict."""
    if not _SETTINGS.exists():
        _log(f"ERROR: {_SETTINGS} not found — cannot continue.")
        sys.exit(1)
    with _SETTINGS.open(encoding="utf-8") as fh:
        return json.load(fh)


def _write_settings(data: dict) -> None:
    """Write data back to settings.json with 2-space indent."""
    with _SETTINGS.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")



# ---------------------------------------------------------------------------
# pwsh path — normalise absolute pwsh paths in settings.json
# ---------------------------------------------------------------------------

def normalise_pwsh_path() -> None:
    """Replace any absolute pwsh path in settings.json with the portable 'pwsh' command."""
    _log("Normalising settings.json: replacing absolute pwsh paths with 'pwsh'...")

    with _SETTINGS.open(encoding="utf-8") as fh:
        raw = fh.read()

    updated = _PWSH_PATH_PATTERN.sub(_PORTABLE_PWSH, raw)

    if updated == raw:
        _log("  settings.json is already clean — no absolute pwsh path found.")
        return

    try:
        json.loads(updated)
    except json.JSONDecodeError as exc:
        _log(f"  ERROR: post-substitution JSON is invalid ({exc}). Aborting.")
        sys.exit(1)

    with _SETTINGS.open("w", encoding="utf-8") as fh:
        fh.write(updated)

    _log(f"  Replaced absolute pwsh path(s) with '{_PORTABLE_PWSH}'.")


def ensure_local_default_shell(shell: str) -> None:
    """Ensure settings.local.json has defaultShell = <shell> (machine-specific, gitignored)."""
    data = {}
    if _LOCAL_SETTINGS.exists():
        with _LOCAL_SETTINGS.open(encoding="utf-8") as fh:
            data = json.load(fh)
    if data.get("defaultShell") == shell:
        _log(f"settings.local.json already has defaultShell = {shell}.")
        return
    data["defaultShell"] = shell
    with _LOCAL_SETTINGS.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    _log(f"settings.local.json: set defaultShell = {shell}.")


# ---------------------------------------------------------------------------
# pwsh installation helpers
# ---------------------------------------------------------------------------

def install_pwsh(os_name: str) -> None:
    """Attempt to install PowerShell 7 for the current OS."""
    _log(f"Attempting to install pwsh on {os_name}...")

    if os_name == "Darwin":
        _install_pwsh_macos()
    elif os_name == "Linux":
        _install_pwsh_linux()
    elif os_name == "Windows":
        _install_pwsh_windows()
    else:
        _log(f"  Unsupported OS '{os_name}' for automatic install.")
        _print_manual_install_url()


def _install_pwsh_macos() -> None:
    brew = shutil.which("brew")
    if brew is None:
        _log("  Homebrew not found — cannot install automatically.")
        _print_manual_install_url()
        return

    _log("  Running: brew install --cask powershell")
    result = subprocess.run(
        ["brew", "install", "--cask", "powershell"],
        check=False,
    )
    if result.returncode != 0:
        _log("  brew install failed.")
        _print_manual_install_url()
    else:
        _log("  pwsh installed via Homebrew.")


def _install_pwsh_linux() -> None:
    """Try snap, then apt-get, then dnf; fall back to manual URL."""
    installers = [
        (["snap", "install", "powershell", "--classic"],  "snap"),
        (["apt-get", "install", "-y", "powershell"],      "apt-get"),
        (["dnf",     "install", "-y", "powershell"],      "dnf"),
    ]

    for cmd, label in installers:
        binary = shutil.which(cmd[0])
        if binary is None:
            _log(f"  '{label}' not found — skipping.")
            continue

        _log(f"  Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            _log(f"  pwsh installed via {label}.")
            return
        _log(f"  {label} install failed (exit {result.returncode}).")

    _log("  All package managers failed or absent.")
    _print_manual_install_url()


def _install_pwsh_windows() -> None:
    winget = shutil.which("winget")
    if winget is None:
        _log("  winget not found on PATH.")
        _print_manual_install_url()
        return

    cmd = [
        "winget", "install",
        "--id", "Microsoft.PowerShell",
        "--source", "winget",
        "--accept-package-agreements",
        "--accept-source-agreements",
    ]
    _log(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        _log(f"  winget install failed (exit {result.returncode}).")
        _print_manual_install_url()
    else:
        _log("  pwsh installed via winget.")


def _print_manual_install_url() -> None:
    _log(
        "  Manual install: https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell"
    )


# ---------------------------------------------------------------------------
# uv installation helpers
# ---------------------------------------------------------------------------
#
# .mcp.json launches the workspace-knowledge/agent-memory MCP servers via the
# bare, portable command "uv" (mirrors "pwsh" in settings.json — no absolute
# paths, relies on PATH). uv itself is what makes that command identical
# across Windows/macOS/Linux/WSL, since "uv run --project <dir> python
# <script>" abstracts the venv layout (.venv/bin vs .venv/Scripts) internally.
# This section closes the one remaining gap: making sure uv is actually on
# PATH on a fresh device, the same way install_pwsh() does for pwsh.

def install_uv(os_name: str) -> None:
    """Attempt to install uv for the current OS."""
    _log(f"Attempting to install uv on {os_name}...")

    if os_name in ("Darwin", "Linux"):
        _install_uv_posix()
    elif os_name == "Windows":
        _install_uv_windows()
    else:
        _log(f"  Unsupported OS '{os_name}' for automatic install.")
        _print_manual_uv_install_url()


def _install_uv_posix() -> None:
    """Official uv install script — works identically on Linux, macOS, and WSL."""
    fetcher = shutil.which("curl") or shutil.which("wget")
    if fetcher is None:
        _log("  Neither 'curl' nor 'wget' found — cannot install automatically.")
        _print_manual_uv_install_url()
        return

    if fetcher.endswith("wget"):
        cmd = "wget -qO- https://astral.sh/uv/install.sh | sh"
    else:
        cmd = "curl -LsSf https://astral.sh/uv/install.sh | sh"

    _log(f"  Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=False)
    if result.returncode != 0:
        _log("  uv install script failed.")
        _print_manual_uv_install_url()
        return

    _log("  uv installed via the official install script.")
    _refresh_path_for_uv_install_dirs()


def _refresh_path_for_uv_install_dirs() -> None:
    """Prepend uv's known install dirs to this process's PATH.

    The official install script writes PATH updates to shell rc files for
    *future* shells — it cannot mutate the PATH already loaded into this
    running process. Without this, a same-process 'shutil.which("uv")'
    re-check right after a successful install can report a false negative
    on a machine where ~/.local/bin (or ~/.cargo/bin, used by older uv
    versions) wasn't already on PATH.
    """
    candidates = [Path.home() / ".local" / "bin", Path.home() / ".cargo" / "bin"]
    existing = os.environ.get("PATH", "")
    existing_parts = existing.split(os.pathsep) if existing else []
    to_prepend = [str(p) for p in candidates if p.is_dir() and str(p) not in existing_parts]
    if to_prepend:
        os.environ["PATH"] = os.pathsep.join(to_prepend + existing_parts)


def _install_uv_windows() -> None:
    winget = shutil.which("winget")
    if winget is None:
        _log("  winget not found on PATH.")
        _print_manual_uv_install_url()
        return

    cmd = [
        "winget", "install",
        "--id", "astral-sh.uv",
        "--source", "winget",
        "--accept-package-agreements",
        "--accept-source-agreements",
    ]
    _log(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        _log(f"  winget install failed (exit {result.returncode}).")
        _print_manual_uv_install_url()
    else:
        _log("  uv installed via winget.")


def _print_manual_uv_install_url() -> None:
    _log(
        "  Manual install: https://docs.astral.sh/uv/getting-started/installation/"
    )


def prime_mcp_venvs() -> None:
    """Pre-sync each MCP server's uv-managed environment.

    Without this, the first real Claude Code launch pays uv's dependency
    download/build cost inside the MCP connection handshake, which can time
    out. Skipped silently if uv still isn't available.
    """
    if shutil.which("uv") is None:
        return

    mcp_servers_dir = _CLAUDE_DIR.parent / "core-component-00" / "mcp-servers"
    for name in ("workspace-knowledge", "agent-memory"):
        server_dir = mcp_servers_dir / name
        if not (server_dir / "pyproject.toml").exists():
            continue
        _log(f"Priming uv environment for {name}...")
        result = subprocess.run(
            ["uv", "sync", "--project", str(server_dir)],
            check=False,
        )
        if result.returncode != 0:
            _log(f"  WARNING: 'uv sync' failed for {name} (exit {result.returncode}).")


# ---------------------------------------------------------------------------
# statusLine path patch
# ---------------------------------------------------------------------------

def patch_statusline() -> None:
    """Replace any absolute statusline path in settings.json with the portable ~ form."""
    with _SETTINGS.open(encoding="utf-8") as fh:
        raw = fh.read()

    updated = _STATUSLINE_PATTERN.sub(_PORTABLE_STATUSLINE, raw)

    if updated == raw:
        _log("patch_statusline: statusLine path already portable — no change needed.")
        return

    try:
        json.loads(updated)
    except json.JSONDecodeError as exc:
        _log(f"patch_statusline: ERROR — post-patch JSON invalid ({exc}). Skipping.")
        return

    with _SETTINGS.open("w", encoding="utf-8") as fh:
        fh.write(updated)

    _log("patch_statusline: replaced absolute statusline path with portable form.")


# ---------------------------------------------------------------------------
# Sentinel
# ---------------------------------------------------------------------------

def _write_sentinel() -> None:
    _SENTINEL.write_text(
        "Workspace initialized by .claude/scripts/init.py\n"
        f"OS: {platform.system()}\n"
        f"Date: {__import__('datetime').date.today()}\n",
        encoding="utf-8",
    )
    _log(f"Sentinel written: {_SENTINEL}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-platform Claude Code workspace initializer."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-run initialization even if the sentinel file already exists.",
    )
    args = parser.parse_args()

    # --- Sentinel check ---
    if _SENTINEL.exists() and not args.force:
        _log(
            f"Workspace already initialized ({_SENTINEL}).\n"
            "  Pass --force to re-run."
        )
        sys.exit(0)

    # --- OS detection (Python primitive per os-detection-spec.md §1) ---
    os_name = platform.system()  # "Windows" | "Darwin" | "Linux"
    is_wsl = os_name == "Linux" and "microsoft" in platform.uname().release.lower()
    _log(f"Detected OS: {'WSL (Linux)' if is_wsl else os_name}")

    # --- Settings selection: OS-first, not merely pwsh-presence-first ---
    # Per CLAUDE.md §1, Windows's interactive shell is PowerShell, while macOS's
    # and Linux's (including WSL, which reports as "Linux" per
    # os-detection-spec.md §3) is bash. The settings.json variant selected here
    # follows that OS split — a machine can have pwsh installed for unrelated
    # reasons without that meaning pwsh should be what runs the hooks.
    if os_name == "Windows":
        # --- PowerShell availability check (Windows only: hooks require PS7+) ---
        pwsh_path = shutil.which("pwsh")
        ps5_path  = shutil.which("powershell")

        if pwsh_path is not None:
            _log(f"pwsh (PS7+) found at: {pwsh_path}")
            normalise_pwsh_path()
            ensure_local_default_shell("powershell")
        elif ps5_path is not None:
            _log(
                f"Windows PowerShell 5.x found at: {ps5_path}\n"
                "  PowerShell 7+ (pwsh) is not installed.\n"
                "  Note: settings.json hooks use 'pwsh' and require PS7+ to run."
            )
            answer = input(
                "Install PowerShell 7+ (pwsh) for full hook support? [y/N]: "
            ).strip().lower()
            if answer in ("y", "yes"):
                install_pwsh(os_name)
                if shutil.which("pwsh") is not None:
                    _log("pwsh (PS7+) is now available.")
                    normalise_pwsh_path()
                    ensure_local_default_shell("powershell")
                else:
                    _log(
                        "pwsh still not found after install attempt.\n"
                        "  Hooks using 'pwsh' will not function until PS7+ is installed manually."
                    )
            else:
                _log(
                    "User declined pwsh install.\n"
                    "  Warning: settings.json hooks use 'pwsh' and will not run under PS5.x."
                )
        else:
            _log("No PowerShell found on PATH.")
            answer = input("Install PowerShell 7+ (pwsh)? [y/N]: ").strip().lower()
            if answer in ("y", "yes"):
                install_pwsh(os_name)
                if shutil.which("pwsh") is not None:
                    _log("pwsh is now available.")
                    normalise_pwsh_path()
                    ensure_local_default_shell("powershell")
                else:
                    _log(
                        "pwsh still not found after install attempt.\n"
                        "  Interactive '!' commands will use bash instead (settings.json's\n"
                        "  hooks are unaffected — they run via 'uv run', not pwsh/bash)."
                    )
                    ensure_local_default_shell("bash")
            else:
                _log(
                    "User declined pwsh install.\n"
                    "  Interactive '!' commands will use bash instead (settings.json's\n"
                    "  hooks are unaffected — they run via 'uv run', not pwsh/bash)."
                )
                ensure_local_default_shell("bash")
    else:
        # macOS / Linux / WSL: bash is the interactive shell per CLAUDE.md §1.
        # settings.json itself needs no per-OS variant or copy step since Phase 3 —
        # every hook already runs via the OS-agnostic "uv run <path>.py".
        _log(f"OS is {'WSL' if is_wsl else os_name} — interactive shell is bash.")
        ensure_local_default_shell("bash")
        if shutil.which("pwsh") is not None:
            _log(
                "  Note: pwsh is also installed on this machine, but bash remains\n"
                "  the default interactive shell on macOS/Linux/WSL."
            )

    # --- uv availability check (required by .mcp.json's "uv run" MCP servers) ---
    uv_path = shutil.which("uv")
    if uv_path is not None:
        _log(f"uv found at: {uv_path}")
        prime_mcp_venvs()
    else:
        _log(
            "uv not found on PATH.\n"
            "  .mcp.json launches the workspace-knowledge/agent-memory MCP servers via\n"
            "  'uv run', which requires uv (https://docs.astral.sh/uv/)."
        )
        answer = input("Install uv now? [y/N]: ").strip().lower()
        if answer in ("y", "yes"):
            install_uv(os_name)
            if shutil.which("uv") is not None:
                _log("uv is now available.")
                prime_mcp_venvs()
            else:
                _log(
                    "uv still not found after install attempt.\n"
                    "  The workspace-knowledge/agent-memory MCP servers will not launch\n"
                    "  until uv is installed manually."
                )
        else:
            _log(
                "User declined uv install.\n"
                "  Warning: the workspace-knowledge/agent-memory MCP servers require uv\n"
                "  and will not launch until it's installed."
            )

    # --- Always patch statusLine ---
    patch_statusline()

    # --- Write sentinel ---
    _write_sentinel()

    _log("Initialization complete.")


if __name__ == "__main__":
    main()
