"""
thermal_guardian.py — Automated thermal management for LM Studio

Monitors GPU temperature and provides warnings when thermal thresholds are exceeded.
Part of the CC-00 RAG deployment toolkit for ASUS Zenbook Pro 14 Duo OLED.

Usage:
    python thermal_guardian.py

Author: Core Component 00 Laboratory
Laboratory Director: Dr. Elias Vance
Last Updated: 2026-05-05
"""

import subprocess
import time
import sys
from datetime import datetime
from typing import Optional


class ThermalGuardian:
    """Monitors GPU temperature and provides thermal management guidance."""

    def __init__(
        self,
        check_interval: int = 30,
        temp_threshold_warning: int = 80,
        temp_threshold_critical: int = 85,
    ):
        """
        Initialize thermal guardian.

        Args:
            check_interval: Seconds between temperature checks
            temp_threshold_warning: Temperature (°C) for warning alerts
            temp_threshold_critical: Temperature (°C) for critical alerts
        """
        self.check_interval = check_interval
        self.temp_warning = temp_threshold_warning
        self.temp_critical = temp_threshold_critical
        self.current_mode = "normal"
        self.max_temp_seen = 0

    def get_gpu_temperature(self) -> Optional[int]:
        """Query GPU temperature via nvidia-smi."""
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=temperature.gpu",
                    "--format=csv,noheader",
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            return int(result.stdout.strip())
        except subprocess.TimeoutExpired:
            print("⚠️  Warning: nvidia-smi timeout")
            return None
        except subprocess.CalledProcessError:
            print("❌ Error: nvidia-smi failed (is NVIDIA driver installed?)")
            return None
        except ValueError:
            print("❌ Error: Could not parse GPU temperature")
            return None
        except FileNotFoundError:
            print("❌ Error: nvidia-smi not found (is NVIDIA driver installed?)")
            sys.exit(1)

    def get_gpu_utilization(self) -> Optional[int]:
        """Query GPU utilization percentage."""
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu",
                    "--format=csv,noheader",
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            return int(result.stdout.strip().replace("%", "").strip())
        except Exception:
            return None

    def get_gpu_memory_used(self) -> Optional[int]:
        """Query GPU memory usage in MB."""
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=memory.used",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            return int(result.stdout.strip())
        except Exception:
            return None

    def adjust_for_temperature(self, temp: int):
        """Provide guidance based on temperature."""
        if temp >= self.temp_critical and self.current_mode != "emergency":
            print(f"\n🚨 CRITICAL: GPU at {temp}°C — IMMEDIATE ACTION REQUIRED")
            print("   Recommended actions:")
            print("   1. Reduce context length to 12288 or 8192")
            print("   2. Switch to Kimi K2.6 14B model (3.8GB VRAM)")
            print("   3. Reduce max concurrent requests to 1")
            print("   4. Check laptop cooling (vents clear, on hard surface)")
            print("   5. Consider stopping LM Studio if temperature continues rising")
            self.current_mode = "emergency"

        elif temp >= self.temp_warning and self.current_mode == "normal":
            print(f"\n⚠️  WARNING: GPU at {temp}°C — Elevated temperature detected")
            print("   Recommended actions:")
            print("   1. Reduce context length from 16384 to 12288")
            print("   2. Reduce max concurrent requests from 3 to 2")
            print("   3. Ensure laptop is on hard surface with good airflow")
            print("   4. Consider using laptop stand or cooling pad")
            self.current_mode = "reduced"

        elif temp < (self.temp_warning - 5) and self.current_mode != "normal":
            print(
                f"\n✅ Temperature normalized at {temp}°C — Safe to restore normal operation"
            )
            self.current_mode = "normal"

    def print_status(self, temp: int, util: Optional[int], vram: Optional[int]):
        """Print current status line."""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Update max temperature
        self.max_temp_seen = max(self.max_temp_seen, temp)

        # Build status line
        status_parts = [f"[{timestamp}]", f"GPU: {temp}°C"]

        if util is not None:
            status_parts.append(f"Util: {util}%")

        if vram is not None:
            status_parts.append(f"VRAM: {vram}MB")

        status_parts.append(f"Max: {self.max_temp_seen}°C")
        status_parts.append(f"Mode: {self.current_mode}")

        # Color code based on temperature
        if temp >= self.temp_critical:
            prefix = "🔴"
        elif temp >= self.temp_warning:
            prefix = "🟡"
        else:
            prefix = "🟢"

        print(f"{prefix} {' | '.join(status_parts)}")

    def monitor(self):
        """Main monitoring loop."""
        print("=" * 70)
        print("🔍 Thermal Guardian — GPU Temperature Monitor")
        print("=" * 70)
        print(f"   Target Hardware: ASUS Zenbook Pro 14 Duo OLED (RTX 4060)")
        print(f"   Warning Threshold: {self.temp_warning}°C")
        print(f"   Critical Threshold: {self.temp_critical}°C")
        print(f"   Check Interval: {self.check_interval}s")
        print()
        print("Legend:")
        print("   🟢 Normal (<80°C) | 🟡 Warning (80-84°C) | 🔴 Critical (≥85°C)")
        print()
        print("Press Ctrl+C to stop monitoring")
        print("=" * 70)
        print()

        try:
            while True:
                temp = self.get_gpu_temperature()

                if temp is None:
                    print("⚠️  Could not read GPU temperature, retrying...")
                    time.sleep(self.check_interval)
                    continue

                util = self.get_gpu_utilization()
                vram = self.get_gpu_memory_used()

                self.print_status(temp, util, vram)
                self.adjust_for_temperature(temp)

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print("\n")
            print("=" * 70)
            print("🛑 Thermal Guardian stopped")
            print("=" * 70)
            print(f"   Session Summary:")
            print(f"   ├─ Maximum Temperature: {self.max_temp_seen}°C")
            print(
                f"   ├─ Final Mode: {self.current_mode}"
            )
            if self.max_temp_seen >= self.temp_critical:
                print(
                    f"   └─ Status: ⚠️  Critical temperature reached — review configuration"
                )
            elif self.max_temp_seen >= self.temp_warning:
                print(
                    f"   └─ Status: ⚠️  Elevated temperature — consider optimization"
                )
            else:
                print(f"   └─ Status: ✅ Normal operation")
            print("=" * 70)


def main():
    """Entry point for thermal guardian."""
    guardian = ThermalGuardian(
        temp_threshold_warning=80, temp_threshold_critical=85, check_interval=30
    )
    guardian.monitor()


if __name__ == "__main__":
    main()
