#!/usr/bin/env python
"""
monitoring-sla-check.py
SessionStart → SLA Metrics Monitoring
============================================================================
Trigger: When SLA health check is requested.

Validates 6 SLA metrics against thresholds:
  1. Assessment processing time (< 48 hours)
  2. Scoring anomaly rate (< 5%)
  3. Candidate drop-off rate (< 15% per stage)
  4. Sourcing channel yield (> 1% pass rate)
  5. Background check failure rate (< 10%)
  6. R0/R1 defect count (0)

Exit: 0 = all metrics healthy, 2 = critical threshold breach
============================================================================
"""

import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


SLA_THRESHOLDS = {
    "assessment_processing_hours": 48,
    "scoring_anomaly_rate": 5,
    "candidate_dropoff_rate": 15,
    "sourcing_channel_min_yield": 1,
    "background_check_failure_rate": 10,
    "r0_defect_count": 0,
    "r1_defect_count": 0,
}


def check_sla(raw: dict, ctx) -> tuple:
    """Returns (is_healthy, alerts, warnings)."""
    alerts = []
    warnings = []

    metrics = raw.get("metrics", {})

    # 1. Assessment processing time
    apt = metrics.get("assessment_processing_hours", 0)
    try:
        if float(apt) > SLA_THRESHOLDS["assessment_processing_hours"]:
            alerts.append(f"Assessment processing time: {apt}h (threshold: {SLA_THRESHOLDS['assessment_processing_hours']}h)")
    except (TypeError, ValueError):
        alerts.append(f"Assessment processing time has invalid type: {apt}")

    # 2. Scoring anomaly rate
    sar = metrics.get("scoring_anomaly_rate", 0)
    try:
        if float(sar) > SLA_THRESHOLDS["scoring_anomaly_rate"]:
            alerts.append(f"Scoring anomaly rate: {sar}% (threshold: {SLA_THRESHOLDS['scoring_anomaly_rate']}%)")
    except (TypeError, ValueError):
        alerts.append(f"Scoring anomaly rate has invalid type: {sar}")

    # 3. Candidate drop-off rate
    dropoff = metrics.get("candidate_dropoff_rate", {})
    if isinstance(dropoff, dict):
        for stage_name, rate in dropoff.items():
            try:
                if float(rate) > SLA_THRESHOLDS["candidate_dropoff_rate"]:
                    alerts.append(f"Candidate drop-off at {stage_name}: {rate}% (threshold: {SLA_THRESHOLDS['candidate_dropoff_rate']}%)")
            except (TypeError, ValueError):
                alerts.append(f"Candidate drop-off rate at {stage_name} has invalid type: {rate}")
    elif isinstance(dropoff, (int, float)):
        try:
            if float(dropoff) > SLA_THRESHOLDS["candidate_dropoff_rate"]:
                alerts.append(f"Candidate drop-off rate: {dropoff}% (threshold: {SLA_THRESHOLDS['candidate_dropoff_rate']}%)")
        except (TypeError, ValueError):
            pass

    # 4. Sourcing channel yield
    channels = metrics.get("sourcing_channel_yield", {})
    if isinstance(channels, dict):
        for channel, yield_pct in channels.items():
            try:
                if float(yield_pct) < SLA_THRESHOLDS["sourcing_channel_min_yield"]:
                    warnings.append(f"Sourcing channel '{channel}' yield: {yield_pct}% (below {SLA_THRESHOLDS['sourcing_channel_min_yield']}%)")
            except (TypeError, ValueError):
                pass

    # 5. Background check failure rate
    bg_fail = metrics.get("background_check_failure_rate", 0)
    try:
        if float(bg_fail) > SLA_THRESHOLDS["background_check_failure_rate"]:
            alerts.append(f"Background check failure rate: {bg_fail}% (threshold: {SLA_THRESHOLDS['background_check_failure_rate']}%)")
    except (TypeError, ValueError):
        alerts.append(f"Background check failure rate has invalid type: {bg_fail}")

    # 6. R0/R1 defect count
    r0 = metrics.get("r0_defect_count", 0)
    r1 = metrics.get("r1_defect_count", 0)
    try:
        if int(r0) > SLA_THRESHOLDS["r0_defect_count"]:
            alerts.append(f"R0 defects: {r0} (threshold: 0)")
    except (TypeError, ValueError):
        pass
    try:
        if int(r1) > SLA_THRESHOLDS["r1_defect_count"]:
            alerts.append(f"R1 defects: {r1} (threshold: 0)")
    except (TypeError, ValueError):
        pass

    is_healthy = len(alerts) == 0
    return is_healthy, alerts, warnings


def main():
    raw = {}
    try:
        if not sys.stdin.isatty():
            c = sys.stdin.read().strip()
            if c:
                raw = json.loads(c)
    except json.JSONDecodeError:
        print("❌ Invalid JSON input", file=sys.stderr)
        sys.exit(2)

    ctx = resolve_entity(raw)
    is_healthy, alerts, warnings = check_sla(raw, ctx)

    audit_data = {
        "event_type": "sla_health_check",
        "is_healthy": is_healthy,
        "alert_count": len(alerts),
        "warning_count": len(warnings),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_healthy:
        print(f"✅ SLA: HEALTHY (all metrics within threshold)", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"🚨 SLA: UNHEALTHY — {len(alerts)} alert(s):", file=sys.stderr)
        for a in alerts:
            print(f"   ALERT: {a}", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
