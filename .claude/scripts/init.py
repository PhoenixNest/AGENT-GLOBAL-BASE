#!/usr/bin/env python3
"""
init.py — Cross-Platform Workspace Initialization Script
.claude/scripts/init.py

Phases 4a/4b of the cross-platform compatibility hardening plan.
Run once to configure the Claude Code workspace for the current OS.

Usage:
    python .claude/scripts/init.py           # normal run (skips if already initialized)
    python .claude/scripts/init.py --force   # re-run even if sentinel exists

Setup paths:
    pwsh path  — pwsh is (or becomes) available: normalizes settings.json paths.
    bash path  — user declines pwsh install: copies platform-settings/settings.bash.json as fallback.

Both paths conclude with patch_statusline() and sentinel file creation.

PowerShell detection order on Windows:
    1. pwsh       — PowerShell 7+ cross-platform edition (must be installed separately)
    2. powershell — Windows PowerShell 5.x (built-in; always present on Windows)
    Settings.json hooks require pwsh; PS 5.x alone is insufficient.
"""

from __future__ import annotations

import argparse
import json
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
_BASH_SETTINGS = _CLAUDE_DIR / "platform-settings" / "settings.bash.json"
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


# ---------------------------------------------------------------------------
# bash path — copy bash-compatible settings
# ---------------------------------------------------------------------------

def apply_bash_config(os_name: str) -> None:
    """Copy platform-settings/settings.bash.json over settings.json (with backup)."""
    _log(f"Bash path: applying bash-compatible settings for OS '{os_name}'...")

    if not _BASH_SETTINGS.exists():
        _log(
            f"  WARNING: {_BASH_SETTINGS} does not exist yet.\n"
            "  Bash config cannot be applied until that file is created.\n"
            "  Skipping bash path — settings.json left unchanged.\n"
            "  Create '.claude/platform-settings/settings.bash.json' with a bash-compatible hook\n"
            "  configuration and re-run init.py to complete bash path setup."
        )
        return

    backup = _SETTINGS.with_suffix(".json.bak")
    shutil.copy2(_SETTINGS, backup)
    _log(f"  Backed up settings.json -> {backup.name}")

    shutil.copy2(_BASH_SETTINGS, _SETTINGS)
    _log(f"  Copied platform-settings/settings.bash.json -> settings.json")


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
    _log(f"Detected OS: {os_name}")

    # --- PowerShell availability check ---
    # pwsh   = PowerShell 7+ (must be installed separately on all OSes)
    # ps5    = Windows PowerShell 5.x (built-in on Windows; not available on macOS/Linux)
    pwsh_path = shutil.which("pwsh")
    ps5_path  = shutil.which("powershell")

    if pwsh_path is not None:
        _log(f"pwsh (PS7+) found at: {pwsh_path}")
        normalise_pwsh_path()
    elif ps5_path is not None and os_name == "Windows":
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
            else:
                _log("pwsh still not found after install attempt — falling back to bash config.")
                apply_bash_config(os_name)
        else:
            _log("User declined pwsh install.")
            apply_bash_config(os_name)

    # --- Always patch statusLine ---
    patch_statusline()

    # --- Write sentinel ---
    _write_sentinel()

    _log("Initialization complete.")


if __name__ == "__main__":
    main()
