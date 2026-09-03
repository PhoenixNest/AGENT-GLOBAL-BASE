#!/usr/bin/env python3
"""
DR-backup scheduling registration for the daily agent-memory JSONL log
snapshot, on Linux/macOS. Cross-platform counterpart to
register_backup_task.ps1 (Windows Task Scheduler).

STATUS: implemented, INACTIVE by default. The "systemd" mechanism is verified
on Linux (WSL2): registering, enabling, and manually firing it produces a
correct backup snapshot. The "cron" mechanism and macOS support (cron subject
to TCC restrictions; no launchd implementation) remain unverified -- do not
treat either as DR-ready until run for real and confirmed to fire. A
registered "systemd" timer also does not survive a full logout/reboot unless
`loginctl enable-linger` has been run separately for the account -- this
script does not enable lingering for you.

Running this script with no flags performs a DRY RUN only — it prints the
unit/crontab definition it would register and registers nothing. Pass
--activate to actually register it. This mirrors register_backup_task.ps1's
same split exactly: CEO approval to write scheduling automation is not the
same approval as activating it — do not pass --activate without a fresh,
explicit authorization to activate, on either script.

Mechanism selection (--mechanism, default "auto"):
  systemd  Linux only. Writes a systemd --user service + timer unit to
           ~/.config/systemd/user/, then (on --activate) runs
           `systemctl --user daemon-reload` and
           `systemctl --user enable --now <name>.timer`. Requires a running
           user systemd session (loginctl linger, or an active graphical/SSH
           session) — a headless cron-only server has no user systemd
           session unless lingering is enabled; this script does not enable
           lingering for you.
  cron     Linux or macOS. Installs a line into the current user's crontab
           via `crontab -l` / `crontab -`. On modern macOS, cron itself is
           subject to Full Disk Access / TCC restrictions in System
           Settings > Privacy & Security — launchd is Apple's recommended
           replacement for cron, but a launchd LaunchAgent implementation is
           NOT included here; that is a further gap, not silently covered by
           this "cron" mechanism. Track it as its own follow-up if macOS
           support is actually needed, rather than assuming this script
           covers macOS just because it runs there.
  auto     Picks "systemd" if `systemctl` is on PATH and a user session is
           detected (`systemctl --user status` succeeds), else "cron".

Usage:
    python register_backup_task.py                          # dry run
    python register_backup_task.py --activate                # register for real
    python register_backup_task.py --mechanism cron --time 03:00
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AGENT_MEMORY_DIR = SCRIPT_DIR.parent
BACKUP_SCRIPT = SCRIPT_DIR / "backup_memory_log.py"
PYTHON_EXE = AGENT_MEMORY_DIR / ".venv" / "bin" / "python"

DEFAULT_TASK_NAME = "cc00-agent-memory-daily-backup"
DEFAULT_TIME = "03:00"

CRON_MARKER = "# cc00-agent-memory-daily-backup (register_backup_task.py)"


def _parse_time(time_str: str) -> tuple:
    try:
        hour_str, minute_str = time_str.split(":", 1)
        hour, minute = int(hour_str), int(minute_str)
    except (ValueError, IndexError):
        raise SystemExit(f"--time must be HH:MM 24-hour format, got {time_str!r}")
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise SystemExit(f"--time out of range: {time_str!r}")
    return hour, minute


def _detect_mechanism() -> str:
    if shutil.which("systemctl") is None:
        return "cron"
    try:
        result = subprocess.run(
            ["systemctl", "--user", "status"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return "cron"
    return "systemd" if result.returncode in (0, 3) else "cron"


def _systemd_units(task_name: str, hour: int, minute: int) -> tuple:
    service_unit = (
        f"[Unit]\n"
        f"Description=CC-00 agent-memory JSONL log daily snapshot (DR backup)\n"
        f"\n"
        f"[Service]\n"
        f"Type=oneshot\n"
        f'ExecStart="{PYTHON_EXE}" "{BACKUP_SCRIPT}"\n'
    )
    timer_unit = (
        f"[Unit]\n"
        f"Description=Daily timer for {task_name}\n"
        f"\n"
        f"[Timer]\n"
        f"OnCalendar=*-*-* {hour:02d}:{minute:02d}:00\n"
        f"Persistent=true\n"
        f"\n"
        f"[Install]\n"
        f"WantedBy=timers.target\n"
    )
    return service_unit, timer_unit


def _register_systemd(task_name: str, hour: int, minute: int, activate: bool) -> None:
    service_unit, timer_unit = _systemd_units(task_name, hour, minute)
    unit_dir = Path.home() / ".config" / "systemd" / "user"
    service_path = unit_dir / f"{task_name}.service"
    timer_path = unit_dir / f"{task_name}.timer"

    print(f"Mechanism:    systemd --user timer")
    print(f"Task name:    {task_name}")
    print(f"Trigger:      Daily at {hour:02d}:{minute:02d}")
    print(f"Action:       \"{PYTHON_EXE}\" \"{BACKUP_SCRIPT}\"")
    print(f"Unit dir:     {unit_dir}")
    print()
    print(f"--- {service_path.name} ---")
    print(service_unit)
    print(f"--- {timer_path.name} ---")
    print(timer_unit)

    if not activate:
        print("DRY RUN — no unit files were written. Pass --activate to register for real.")
        return

    unit_dir.mkdir(parents=True, exist_ok=True)
    service_path.write_text(service_unit, encoding="utf-8")
    timer_path.write_text(timer_unit, encoding="utf-8")
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "--user", "enable", "--now", f"{task_name}.timer"], check=True)
    print(f"Registered and started systemd user timer '{task_name}.timer'.")


def _register_cron(hour: int, minute: int, activate: bool) -> None:
    cron_line = f'{minute} {hour} * * * "{PYTHON_EXE}" "{BACKUP_SCRIPT}"  {CRON_MARKER}'

    print(f"Mechanism:    cron (current user crontab)")
    print(f"Trigger:      Daily at {hour:02d}:{minute:02d}")
    print(f"Crontab line: {cron_line}")
    print()

    if not activate:
        print("DRY RUN — crontab was not modified. Pass --activate to register for real.")
        return

    try:
        existing = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, timeout=10
        )
        current_lines = existing.stdout.splitlines() if existing.returncode == 0 else []
    except FileNotFoundError:
        raise SystemExit("crontab command not found — cannot register via cron on this system.")

    kept_lines = [line for line in current_lines if CRON_MARKER not in line]
    new_crontab = "\n".join(kept_lines + [cron_line]) + "\n"

    proc = subprocess.run(["crontab", "-"], input=new_crontab, text=True, timeout=10)
    if proc.returncode != 0:
        raise SystemExit("Failed to install crontab entry — see crontab's own error output above.")
    print("Installed daily crontab entry.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--activate", action="store_true", help="Actually register. Omit to dry-run only.")
    parser.add_argument("--task-name", default=DEFAULT_TASK_NAME, help=f"Task/timer name. Default: {DEFAULT_TASK_NAME!r}")
    parser.add_argument("--time", default=DEFAULT_TIME, help=f'Daily run time, HH:MM 24h. Default: "{DEFAULT_TIME}"')
    parser.add_argument("--mechanism", choices=["auto", "systemd", "cron"], default="auto", help="Scheduling mechanism. Default: auto-detect.")
    args = parser.parse_args()

    if sys.platform == "win32":
        raise SystemExit(
            "This script targets Linux/macOS. On Windows, use register_backup_task.ps1 instead."
        )

    hour, minute = _parse_time(args.time)
    mechanism = args.mechanism if args.mechanism != "auto" else _detect_mechanism()

    print("*** UNVERIFIED SCRIPT — written without a non-Windows machine to test against. ***")
    print("*** Confirm the resulting timer/cron entry actually fires before relying on it. ***")
    print()

    if mechanism == "systemd":
        _register_systemd(args.task_name, hour, minute, args.activate)
    else:
        _register_cron(hour, minute, args.activate)
    return 0


if __name__ == "__main__":
    sys.exit(main())
