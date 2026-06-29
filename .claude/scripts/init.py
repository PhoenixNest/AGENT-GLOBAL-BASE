#!/usr/bin/env python3
"""
init.py — Cross-Platform Workspace Initialization Script
.claude/scripts/init.py

Phases 4a/4b of the cross-platform compatibility hardening plan.
Run once to configure the Claude Code workspace for the current OS.

Usage:
    python .claude/scripts/init.py           # normal run (skips if already initialized)
    python .claude/scripts/init.py --force   # re-run even if sentinel exists

Branches:
    Branch A — pwsh is (or becomes) available: normalizes settings.json paths.
    Branch B — user declines pwsh install: copies settings.branch-b.json as fallback.

Both branches conclude with patch_statusline() and sentinel file creation.
"""

from __future__ import annotations

import argparse
import json
import platform
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
_BRANCH_B   = _CLAUDE_DIR / "settings.branch-b.json"
_SENTINEL   = _CLAUDE_DIR / ".workspace-initialized"

# The hardcoded Windows path that Branch A normalises away.
_HARDCODED_PWSH = "C:/PROGRA~1/PowerShell/7/pwsh.exe"
_PORTABLE_PWSH  = "pwsh"

# The hardcoded statusline path that patch_statusline() normalises.
_HARDCODED_STATUSLINE = "python -u C:/Users/ASUS/.claude/statusline.py"
_PORTABLE_STATUSLINE  = "python -u ~/.claude/statusline.py"


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


def _replace_in_json_str(raw: str, old: str, new: str) -> tuple[str, int]:
    """String-level replacement across the whole JSON blob.

    Returns the (possibly modified) string and the replacement count.
    Operates on the raw text so it handles all nested locations uniformly.
    """
    count = raw.count(old)
    return raw.replace(old, new), count


# ---------------------------------------------------------------------------
# Branch A — normalise hardcoded pwsh path
# ---------------------------------------------------------------------------

def apply_branch_a() -> None:
    """Replace C:/PROGRA~1/... occurrences with plain 'pwsh' in settings.json."""
    _log("Branch A: normalising settings.json pwsh paths...")

    with _SETTINGS.open(encoding="utf-8") as fh:
        raw = fh.read()

    updated, count = _replace_in_json_str(raw, _HARDCODED_PWSH, _PORTABLE_PWSH)

    if count == 0:
        _log("  settings.json is already clean — no pwsh path substitution needed.")
        return

    # Validate that the result is still valid JSON before writing.
    try:
        json.loads(updated)
    except json.JSONDecodeError as exc:
        _log(f"  ERROR: post-substitution JSON is invalid ({exc}). Aborting Branch A.")
        sys.exit(1)

    with _SETTINGS.open("w", encoding="utf-8") as fh:
        fh.write(updated)

    _log(f"  Replaced {count} occurrence(s) of hardcoded pwsh path with '{_PORTABLE_PWSH}'.")


# ---------------------------------------------------------------------------
# Branch B — copy fallback settings
# ---------------------------------------------------------------------------

def apply_branch_b(os_name: str) -> None:
    """Copy settings.branch-b.json over settings.json (with backup)."""
    _log(f"Branch B: applying bash-compatible settings for OS '{os_name}'...")

    if not _BRANCH_B.exists():
        _log(
            f"  WARNING: {_BRANCH_B} does not exist yet.\n"
            "  Branch B cannot be applied until that file is created.\n"
            "  Skipping Branch B — settings.json left unchanged.\n"
            "  Create '.claude/settings.branch-b.json' with a bash-compatible hook\n"
            "  configuration and re-run init.py to complete Branch B setup."
        )
        return

    backup = _SETTINGS.with_suffix(".json.bak")
    shutil.copy2(_SETTINGS, backup)
    _log(f"  Backed up settings.json -> {backup.name}")

    shutil.copy2(_BRANCH_B, _SETTINGS)
    _log(f"  Copied settings.branch-b.json -> settings.json")


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
    """Replace the hardcoded ASUS statusline path with the portable ~ form."""
    with _SETTINGS.open(encoding="utf-8") as fh:
        raw = fh.read()

    updated, count = _replace_in_json_str(raw, _HARDCODED_STATUSLINE, _PORTABLE_STATUSLINE)

    if count == 0:
        _log("patch_statusline: statusLine path already portable — no change needed.")
        return

    try:
        json.loads(updated)
    except json.JSONDecodeError as exc:
        _log(f"patch_statusline: ERROR — post-patch JSON invalid ({exc}). Skipping.")
        return

    with _SETTINGS.open("w", encoding="utf-8") as fh:
        fh.write(updated)

    _log(f"patch_statusline: updated {count} occurrence(s) to portable path.")


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

    # --- pwsh availability check ---
    pwsh_path = shutil.which("pwsh")

    if pwsh_path is not None:
        _log(f"pwsh found at: {pwsh_path}")
        apply_branch_a()
    else:
        _log("pwsh not found on PATH.")
        answer = input("Install PowerShell (pwsh)? [y/N]: ").strip().lower()
        if answer in ("y", "yes"):
            install_pwsh(os_name)
            # Re-check after install attempt.
            if shutil.which("pwsh") is not None:
                _log("pwsh is now available.")
                apply_branch_a()
            else:
                _log(
                    "pwsh still not found after install attempt — "
                    "falling back to Branch B."
                )
                apply_branch_b(os_name)
        else:
            _log("User declined pwsh install.")
            apply_branch_b(os_name)

    # --- Always patch statusLine ---
    patch_statusline()

    # --- Write sentinel ---
    _write_sentinel()

    _log("Initialization complete.")


if __name__ == "__main__":
    main()
