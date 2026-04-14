#!/usr/bin/env python
"""
stage-2-aggregate-sourcing-results.py
P3 Hook: SubagentStop → Sourcing Result Aggregation (Stage 2)
============================================================================
Trigger: When sourcing agents complete their scan.

Behavior:
  1. Deduplicates candidates by email
  2. Applies channel-weighted scoring
  3. Generates top-50 shortlist
  4. Writes sourcing results to entity data directory

Exit: 0 = aggregation complete
============================================================================
"""

import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


def aggregate_sourcing(raw: dict, ctx) -> dict:
    """Deduplicate, score, and shortlist candidates."""
    candidates = raw.get("candidates", [])
    role_id = raw.get("role_id", ctx.role_id or "unknown")
    quarter = raw.get("quarter", "unknown")

    if not candidates:
        return {"error": "No candidates provided"}

    # Deduplicate by email
    seen_emails = {}
    no_email = []
    for c in candidates:
        email = c.get("email", "").lower()
        if email and email in seen_emails:
            # Merge: take the higher-scored entry
            existing = seen_emails[email]
            if c.get("experience_years", 0) > existing.get("experience_years", 0):
                seen_emails[email] = c
        elif email:
            seen_emails[email] = c
        else:
            no_email.append(c)  # Keep candidates without email separately

    unique = list(seen_emails.values()) + no_email

    # Score candidates
    for c in unique:
        score = 0.0
        exp = c.get("experience_years", 0)
        score += min(exp * 3, 30)  # Up to 30 points for experience

        skills = c.get("skills", [])
        score += min(len(skills) * 5, 25)  # Up to 25 points for skills

        channels = c.get("source_channels", [])
        channel_bonus = len(channels) * 2
        score += min(channel_bonus, 15)  # Up to 15 points for channel diversity

        github_stars = c.get("github_stars", 0)
        score += min(github_stars / 100, 10)  # Up to 10 points for GitHub

        tenure = c.get("avg_tenure_months", 0)
        score += min(tenure / 6, 10)  # Up to 10 points for tenure

        publications = c.get("publications", 0)
        score += min(publications * 2, 10)  # Up to 10 points for publications

        c["sourcing_score"] = round(score, 1)

    # Rank and shortlist
    unique.sort(key=lambda c: c.get("sourcing_score", 0), reverse=True)
    shortlist = unique[:50]

    # Write results
    data_dir = os.path.join(ctx.entity_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    result = {
        "role_id": role_id,
        "quarter": quarter,
        "total_raw": len(candidates),
        "unique_after_dedup": len(unique),
        "shortlist_count": len(shortlist),
        "shortlist": [{"candidate_id": f"CAND-{i+1:03d}", **c} for i, c in enumerate(shortlist)],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    result_path = os.path.join(data_dir, f"sourcing-results-{role_id}.json")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


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
    result = aggregate_sourcing(raw, ctx)

    if "error" in result:
        print(f"❌ Sourcing aggregation failed: {result['error']}", file=sys.stderr)
        sys.exit(2)

    # Audit
    audit_data = {
        "event_type": "stage_2_sourcing_aggregation",
        "role_id": result.get("role_id", "unknown"),
        "total_raw": result.get("total_raw", 0),
        "unique_after_dedup": result.get("unique_after_dedup", 0),
        "shortlist_count": result.get("shortlist_count", 0),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    print(f"✅ Sourcing aggregation: {result['total_raw']} raw → {result['unique_after_dedup']} unique → "
          f"{result['shortlist_count']} shortlisted", file=sys.stderr)
    print(json.dumps(result, indent=2), file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
