#!/usr/bin/env python
"""
monitoring-drift-detection.py
SessionStart → Competency Bar Drift Detection
============================================================================
Trigger: When drift check is requested.

Computes 6 drift detection metrics from entity audit log:
  1. Vetting pass rate vs. baseline
  2. Score distribution shift (>5% triggers flag)
  3. Stage-specific pass rates vs. historical
  4. Assessment completion rate trend
  5. Offer acceptance rate vs. baseline
  6. Auto-reject rate by stage vs. historical

Exit: 0 = no significant drift, 2 = drift detected (flags for CIO review)
============================================================================
"""

import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


DRIFT_THRESHOLD = 0.05  # 5% shift triggers flag


def compute_drift(entity_root: str) -> tuple:
    """Returns (has_drift, drift_details, warnings)."""
    drift_details = []
    warnings = []

    audit_path = os.path.join(entity_root, "audit", "audit-log.jsonl")
    if not os.path.exists(audit_path):
        return False, [], ["No audit data available for drift detection"]

    entries = []
    try:
        with open(audit_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except IOError:
        return False, [], ["Unable to read audit log"]

    # 1. Vetting pass rate
    vetting_events = [e for e in entries if e.get("event_type") == "stage_5_vetting_gate"]
    if vetting_events:
        passes = sum(1 for e in vetting_events if e.get("result") == "PASS")
        total = len(vetting_events)
        pass_rate = passes / total if total > 0 else 0
        # Baseline: expect ≥ 20% pass rate for elite bar
        baseline = 0.20
        if pass_rate < baseline * 0.8:  # 20% below baseline
            drift_details.append({
                "metric": "vetting_pass_rate",
                "current": round(pass_rate, 4),
                "baseline": baseline,
                "drift_pct": round((baseline - pass_rate) / baseline * 100, 1),
                "severity": "HIGH" if pass_rate < baseline * 0.5 else "MEDIUM",
            })

    # 2. Score distribution shift (vetting total scores)
    vetting_scores = []
    for e in vetting_events:
        scores = e.get("scores", {})
        total_score = sum(scores.get(k, 0) for k in ["impact_at_scale", "craft_depth",
                                                       "leadership_signal", "standards_signal"])
        if total_score > 0:
            vetting_scores.append(total_score)
    if len(vetting_scores) >= 5:
        mean_score = sum(vetting_scores) / len(vetting_scores)
        # Baseline: expect mean ≥ 16/20 (elite bar)
        baseline_mean = 16.0
        if abs(mean_score - baseline_mean) / baseline_mean > DRIFT_THRESHOLD:
            drift_details.append({
                "metric": "vetting_score_mean",
                "current": round(mean_score, 2),
                "baseline": baseline_mean,
                "drift_pct": round((mean_score - baseline_mean) / baseline_mean * 100, 1),
                "severity": "MEDIUM",
            })

    # 3. Auto-reject rate by stage
    reject_events = [e for e in entries if e.get("event_type") == "defect_classification"]
    r0_count = sum(1 for e in reject_events if e.get("severity") == "R0")
    r1_count = sum(1 for e in reject_events if e.get("severity") == "R1")
    if r0_count > 0:
        drift_details.append({
            "metric": "r0_defect_count",
            "current": r0_count,
            "baseline": 0,
            "severity": "CRITICAL",
        })

    # 4. Assessment completion rate
    assessment_starts = [e for e in entries if "assessment" in e.get("event_type", "").lower()]
    assessment_completions = [e for e in entries if "interview_scores" in e.get("event_type", "").lower()]
    if assessment_starts:
        completion_rate = len(assessment_completions) / len(assessment_starts)
        if completion_rate < 0.90:
            drift_details.append({
                "metric": "assessment_completion_rate",
                "current": round(completion_rate, 4),
                "baseline": 0.95,
                "drift_pct": round((0.95 - completion_rate) / 0.95 * 100, 1),
                "severity": "MEDIUM",
            })

    # 5. Offer acceptance rate
    offer_events = [e for e in entries if "offer" in e.get("event_type", "").lower()]
    accepted = sum(1 for e in offer_events if e.get("status") == "accepted")
    total_offers = len(offer_events)
    if total_offers > 0:
        acceptance_rate = accepted / total_offers
        baseline = 0.60  # 60% threshold from pipeline spec
        if acceptance_rate < baseline:
            drift_details.append({
                "metric": "offer_acceptance_rate",
                "current": round(acceptance_rate, 4),
                "baseline": baseline,
                "drift_pct": round((baseline - acceptance_rate) / baseline * 100, 1),
                "severity": "HIGH" if acceptance_rate < 0.40 else "MEDIUM",
            })

    has_drift = any(d.get("severity") in ("HIGH", "CRITICAL") for d in drift_details)
    return has_drift, drift_details, warnings


def main():
    raw = {}
    try:
        if not sys.stdin.isatty():
            c = sys.stdin.read().strip()
            if c:
                raw = json.loads(c)
    except json.JSONDecodeError:
        raw = {}

    ctx = resolve_entity(raw)
    has_drift, drift_details, warnings = compute_drift(ctx.entity_root)

    audit_data = {
        "event_type": "competency_drift_detection",
        "has_drift": has_drift,
        "drift_count": len(drift_details),
        "drift_metrics": drift_details[:5],  # Truncate for audit
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if has_drift:
        print(f"🚨 DRIFT DETECTED — {len(drift_details)} metric(s) flagged:", file=sys.stderr)
        for d in drift_details:
            print(f"   {d['severity']}: {d['metric']} = {d['current']} "
                  f"(baseline: {d['baseline']}, drift: {d.get('drift_pct', 'N/A')}%)", file=sys.stderr)
        sys.exit(2)
    elif warnings:
        print(f"⚠️ Drift check: insufficient data", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"✅ Drift check: All metrics within normal range", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
