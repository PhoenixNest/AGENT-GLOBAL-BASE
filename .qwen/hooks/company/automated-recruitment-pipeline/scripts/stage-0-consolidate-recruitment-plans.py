#!/usr/bin/env python
"""
stage-0-consolidate-recruitment-plans.py
P2 Hook: SubagentStart → Plan Consolidation (Stage 0)
============================================================================
Trigger: When CHRO consolidates department recruitment plans.

Behavior:
  1. Aggregates all department plans from stdin
  2. Detects conflicts (competing skills, budget overruns)
  3. Auto-ranks by priority (P0 > P1 > P2)
  4. Produces company-wide recruitment plan
  5. Validates against company budget capacity
  6. Writes consolidated plan to entity_root/data/

Exit: 0 = consolidation complete, 2 = conflict unresolvable
============================================================================
"""

import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


def consolidate_plans(raw: dict, ctx) -> tuple:
    """Returns (is_valid, consolidated_plan, errors, warnings)."""
    errors = []
    warnings = []

    department_plans = raw.get("department_plans", [])
    company_budget = raw.get("company_budget", {})
    total_budget = company_budget.get("recruitment", {}).get("quarterly_allocation", 0)

    if not department_plans:
        errors.append("No department plans provided for consolidation")
        return False, None, errors, warnings

    # Aggregate all roles
    all_roles = []
    total_headcount = 0
    total_estimated_cost = 0

    for plan in department_plans:
        dept = plan.get("department", "unknown")
        roles = plan.get("roles", [])
        for role in roles:
            role["_source_department"] = dept
            all_roles.append(role)
            count = role.get("count", 0)
            total_headcount += count

    # Budget check
    budget_impact = raw.get("budget_impact", {})
    estimated_total = budget_impact.get("estimated_total", 0)
    if total_budget > 0 and estimated_total > total_budget:
        errors.append(f"Total estimated cost ${estimated_total:,} exceeds budget ${total_budget:,}")

    # Priority ranking
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    all_roles.sort(key=lambda r: priority_order.get(r.get("priority", "P2"), 2))

    # Conflict detection
    role_keys = {}
    cross_dept_conflicts = []
    for role in all_roles:
        key = f"{role.get('title', '').lower()}|{role.get('seniority', '').lower()}"
        if key in role_keys:
            existing = role_keys[key]
            if existing.get("_source_department") != role.get("_source_department"):
                conflict = {
                    "role": role.get("title"),
                    "seniority": role.get("seniority"),
                    "departments": [existing.get("_source_department"), role.get("_source_department")],
                    "resolution": "auto-ranked-by-priority",
                }
                cross_dept_conflicts.append(conflict)
                warnings.append(f"Cross-department role conflict: '{role.get('title')}' at {role.get('seniority')} "
                                f"requested by {existing.get('_source_department')} and {role.get('_source_department')}")
        role_keys[key] = role

    # Build consolidated plan
    consolidated = {
        "quarter": raw.get("quarter", "unknown"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_headcount": total_headcount,
        "total_estimated_cost": estimated_total,
        "budget_capacity": total_budget,
        "budget_remaining": max(0, total_budget - estimated_total),
        "roles": [{k: v for k, v in r.items() if not k.startswith("_")} for r in all_roles],
        "conflicts": cross_dept_conflicts,
        "status": "approved" if not errors else "rejected",
    }

    # Write consolidated plan
    if not errors:
        data_dir = os.path.join(ctx.entity_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        plan_path = os.path.join(data_dir, f"recruitment-plan-{raw.get('quarter', 'unknown')}.json")
        with open(plan_path, "w") as f:
            json.dump(consolidated, f, indent=2)

    return len(errors) == 0, consolidated, errors, warnings


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
    is_valid, plan, errors, warnings = consolidate_plans(raw, ctx)

    audit_data = {
        "event_type": "stage_0_plan_consolidation",
        "quarter": raw.get("quarter", "unknown"),
        "is_valid": is_valid,
        "total_headcount": plan.get("total_headcount", 0) if plan else 0,
        "error_count": len(errors),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        print(f"✅ Plan consolidation complete: {plan['total_headcount']} roles, "
              f"${plan['total_estimated_cost']:,} / ${plan['budget_capacity']:,} budget", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        print(json.dumps({"is_valid": True, "plan_summary": {
            "total_headcount": plan["total_headcount"],
            "total_cost": plan["total_estimated_cost"],
            "budget_remaining": plan["budget_remaining"],
        }}), file=sys.stdout)
        sys.exit(0)
    else:
        print(f"❌ Plan consolidation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
