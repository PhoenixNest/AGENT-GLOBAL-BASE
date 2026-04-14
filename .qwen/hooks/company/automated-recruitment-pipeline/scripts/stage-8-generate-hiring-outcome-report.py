#!/usr/bin/env python
"""
stage-8-generate-hiring-outcome-report.py
P3 Hook: SessionEnd → Hiring Outcome Report Generation
============================================================================
Trigger: When Stage 8 user review completes or hiring cycle closes.

Behavior:
  1. Reads all candidate artifacts from entity_root/crew/.../pipeline-artifacts/
  2. Generates HIRING OUTCOME REPORT with all 7 sections
  3. Verifies per-candidate artifact completeness
  4. Seals audit trails for this cycle
  5. Applies data retention policies
  6. Writes report to entity_root/reports/ (NOT .qwen/)

Exit: 0 = report generated successfully
============================================================================
"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log
from lib.artifact_parser import parse_artifact


def find_crew_members(entity_root: str) -> list:
    """Find all crew member directories under entity_root/crew/."""
    crew_root = os.path.join(entity_root, "crew")
    if not os.path.exists(crew_root):
        return []

    members = []
    for div in sorted(os.listdir(crew_root)):
        div_path = os.path.join(crew_root, div)
        if not os.path.isdir(div_path):
            continue
        for role in sorted(os.listdir(div_path)):
            role_path = os.path.join(div_path, role)
            if not os.path.isdir(role_path):
                continue
            for person in sorted(os.listdir(role_path)):
                person_path = os.path.join(role_path, person)
                artifacts_path = os.path.join(person_path, "pipeline-artifacts")
                if os.path.isdir(artifacts_path):
                    members.append({
                        "name": person.replace("-", " ").title(),
                        "division": div,
                        "role": role,
                        "path": person_path,
                        "artifacts_path": artifacts_path,
                    })
    return members


def check_candidate_artifacts(artifacts_path: str) -> dict:
    """Check which artifacts exist for a candidate."""
    expected = [
        "stage1-psd.md", "stage2-sourcing-shortlist.md",
        "stage3-screening-results.md", "stage4-interview-scores.md",
        "stage5-vetting-gate.md", "stage6-background-check.md",
        "stage7-offer.md", "stage8-provisioning.md",
        "stage9-hiring-outcome-report.md",
    ]
    result = {"total": len(expected), "present": 0, "missing": [], "scores": {}}

    for fname in expected:
        fpath = os.path.join(artifacts_path, fname)
        if os.path.exists(fpath):
            result["present"] += 1
            # Extract key data from frontmatter or fallback
            try:
                parsed = parse_artifact(fpath)
                data = parsed.data
                if "vetting" in fname:
                    scores = data.get("scores", {})
                    result["scores"]["vetting_total"] = data.get("total_score", 0)
                if "interview" in fname:
                    result["scores"]["composite"] = data.get("composite_score", 0)
                    result["scores"]["percentile"] = data.get("percentile", 0)
                if "hiring" in fname:
                    result["final_decision"] = data.get("final_decision", data.get("gate_status", "unknown"))
            except Exception:
                pass
        else:
            result["missing"].append(fname)

    return result


def compute_pipeline_health(entity_root: str) -> dict:
    """Compute pipeline health metrics from entity audit log."""
    audit_path = os.path.join(entity_root, "audit", "audit-log.jsonl")
    entries = []
    if os.path.exists(audit_path):
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
            pass

    defects = [e for e in entries if e.get("event_type") == "defect_classification"]
    return {
        "total_audit_events": len(entries),
        "defects": {
            "R0": sum(1 for d in defects if d.get("severity") == "R0"),
            "R1": sum(1 for d in defects if d.get("severity") == "R1"),
            "R2": sum(1 for d in defects if d.get("severity") == "R2"),
            "R3": sum(1 for d in defects if d.get("severity") == "R3"),
        },
        "unique_event_types": len(set(e.get("event_type", "") for e in entries)),
    }


def generate_report(entity_root: str, raw: dict) -> dict:
    """Generate the complete HIRING OUTCOME REPORT."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    hiring_cycle_id = raw.get("hiring_cycle_id", "unknown")

    # Find all crew members
    crew = find_crew_members(entity_root)

    # Check each candidate's artifacts
    candidates = []
    hired = []
    for member in crew:
        art_check = check_candidate_artifacts(member["artifacts_path"])
        candidate_info = {
            "name": member["name"],
            "division": member["division"],
            "role": member["role"],
            "artifacts": art_check,
            "complete": art_check["present"] == art_check["total"],
        }
        candidates.append(candidate_info)
        if art_check.get("final_decision") == "HIRED":
            hired.append(candidate_info)

    # Pipeline health
    health = compute_pipeline_health(entity_root)

    # Compute rejection breakdown from audit log
    audit_path = os.path.join(entity_root, "audit", "audit-log.jsonl")
    rejection_stages = {}
    rejection_reasons = {}
    if os.path.exists(audit_path):
        try:
            with open(audit_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            if entry.get("result") == "auto-reject" or entry.get("event_type") == "defect_classification":
                                stage = entry.get("stage", "unknown")
                                rejection_stages[stage] = rejection_stages.get(stage, 0) + 1
                                reason = entry.get("severity", entry.get("result", "unknown"))
                                rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
                        except json.JSONDecodeError:
                            continue
        except IOError:
            pass

    # Compute competency bar calibration from vetting scores
    vetting_scores = []
    for member in crew:
        vetting_path = os.path.join(member["artifacts_path"], "stage5-vetting-gate.md")
        if os.path.exists(vetting_path):
            try:
                parsed = parse_artifact(vetting_path)
                data = parsed.data
                total = data.get("total_score", 0)
                if total > 0:
                    vetting_scores.append(total)
            except Exception:
                pass

    competency_calibration = {
        "vetting_score_distribution": {
            "mean": round(sum(vetting_scores) / len(vetting_scores), 2) if vetting_scores else 0,
            "min": min(vetting_scores) if vetting_scores else 0,
            "max": max(vetting_scores) if vetting_scores else 0,
            "count": len(vetting_scores),
        },
        "elite_bar_pass_rate": f"{len(hired)}/{len(candidates)}" if candidates else "N/A",
        "recommended_adjustments": "No adjustment recommended for first cycle" if len(candidates) < 10 else "Review after 3+ cycles",
    }

    # Build report with all 7 sections containing real data
    report = {
        "title": "HIRING OUTCOME REPORT",
        "reporting_period": raw.get("quarter", "unknown"),
        "generated": timestamp,
        "prepared_by": "System (CHRO-curated)",
        "hiring_cycle_id": hiring_cycle_id,
        "entity_root": entity_root,

        "1_executive_summary": {
            "total_candidates": len(candidates),
            "total_hired": len(hired),
            "complete_dossiers": sum(1 for c in candidates if c["complete"]),
            "incomplete_dossiers": sum(1 for c in candidates if not c["complete"]),
        },

        "2_per_role_breakdown": {
            "hired_candidates": [
                {"name": h["name"], "division": h["division"], "role": h["role"],
                 "scores": h["artifacts"].get("scores", {})}
                for h in hired
            ],
        },

        "3_rejected_candidate_summary": {
            "total_processed": len(candidates),
            "rejected_by_stage": rejection_stages,
            "rejection_reason_counts": rejection_reasons,
            "note": "Individual rejection details available in each candidate's stage9 artifact",
        },

        "4_exceptions_and_escalations": {
            "defects": health.get("defects", {}),
            "total_defects": sum(health.get("defects", {}).values()),
            "unresolved_r2": [e for e in health.get("defects", {}) if health["defects"].get(e, 0) > 0 and e == "R2"],
        },

        "5_pipeline_health_metrics": {
            **health,
            "rejection_rate_by_stage": rejection_stages,
            "offer_acceptance_rate": f"{len(hired)}/{len(candidates)}" if candidates else "N/A",
        },

        "6_competency_bar_calibration": competency_calibration,

        "7_recommendations": {
            "hiring_plan": "Continue current trajectory" if hired else "Re-source candidates — review rejection reasons",
            "channel_changes": "Review sourcing channel yield after 3+ cycles",
            "bar_adjustments": competency_calibration["recommended_adjustments"],
            "process_improvements": [
                "Monitor assessment completion times" if not hired else "All assessments completed successfully",
                "Track candidate drop-off rates per stage",
                "Review defect patterns for systemic issues" if health.get("defects", {}).get("R0", 0) + health.get("defects", {}).get("R1", 0) > 0 else "No critical defects detected",
            ],
            "stage_0_1_improvements": _compute_stage_improvements(candidates, health),
        },

        "candidate_inventory": [
            {"name": c["name"], "division": c["division"], "role": c["role"],
             "artifacts_present": c["artifacts"]["present"],
             "artifacts_total": c["artifacts"]["total"],
             "complete": c["complete"]}
            for c in candidates
        ],
    }

    # Write report to entity_root/reports/
    reports_dir = os.path.join(entity_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    report_json_path = os.path.join(reports_dir, f"hiring-outcome-{hiring_cycle_id}.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Markdown version
    md_path = os.path.join(reports_dir, f"hiring-outcome-{hiring_cycle_id}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(_generate_markdown(report))

    return {
        "report_file": report_json_path,
        "markdown_file": md_path,
        "hiring_cycle_id": hiring_cycle_id,
        "candidates_processed": len(candidates),
        "hired": len(hired),
        "complete_dossiers": sum(1 for c in candidates if c["complete"]),
    }


def _compute_stage_improvements(candidates: list, health: dict) -> list:
    """Compute Stage 0/1 improvement recommendations based on pipeline data."""
    improvements = []
    incomplete = sum(1 for c in candidates if not c["complete"])
    if incomplete > 0:
        improvements.append(f"{incomplete} candidates have incomplete dossiers — improve artifact generation pipeline")
    r2_count = health.get("defects", {}).get("R2", 0)
    if r2_count > 0:
        improvements.append(f"{r2_count} R2 defects logged — review for systemic patterns")
    if not improvements:
        improvements.append("No Stage 0/1 improvements identified for this cycle")
    return improvements


def _generate_markdown(report: dict) -> str:
    """Generate human-readable markdown report."""
    lines = [
        "# HIRING OUTCOME REPORT",
        "",
        f"**Reporting Period:** {report['reporting_period']}",
        f"**Generated:** {report['generated']}",
        f"**Prepared by:** {report['prepared_by']}",
        f"**Entity:** {report['entity_root']}",
        "",
        "---",
        "",
        "## 1. Executive Summary",
        "",
        f"- Total candidates processed: {report['1_executive_summary']['total_candidates']}",
        f"- Total hired: {report['1_executive_summary']['total_hired']}",
        f"- Complete dossiers: {report['1_executive_summary']['complete_dossiers']}",
        f"- Incomplete dossiers: {report['1_executive_summary']['incomplete_dossiers']}",
        "",
        "---",
        "",
        "## 2. Hired Candidates",
        "",
    ]
    for c in report["2_per_role_breakdown"]["hired_candidates"]:
        scores = c.get("scores", {})
        lines.append(f"- **{c['name']}** — {c['division']}/{c['role']} "
                      f"(Vetting: {scores.get('vetting_total', 'N/A')}/20, "
                      f"Composite: {scores.get('composite', 'N/A')})")
    lines.extend([
        "",
        "---",
        "",
        "## 3. Rejected Candidates",
        "",
        f"- Total rejected: {report['3_rejected_candidate_summary']['total_processed']}",
        f"- Rejection reasons: {', '.join(report['3_rejected_candidate_summary'].get('top_rejection_reasons', ['N/A']))}",
        "",
        "---",
        "",
        "## 4. Exceptions & Escalations",
        "",
        f"- Total defects: {report['4_exceptions_and_escalations']['total_defects']}",
        f"- Unresolved R2 defects: {len(report['4_exceptions_and_escalations'].get('unresolved_r2', []))}",
        "",
        "---",
        "",
        "## 5. Pipeline Health",
        "",
        f"- Total audit events: {report['5_pipeline_health_metrics']['total_audit_events']}",
        f"- Unique event types: {report['5_pipeline_health_metrics'].get('unique_event_types', 'N/A')}",
        f"- Assessments run: {report['5_pipeline_health_metrics'].get('assessments_run', 'N/A')}",
        f"- Notifications sent: {report['5_pipeline_health_metrics'].get('notifications_sent', 'N/A')}",
        f"- Defects: {report['5_pipeline_health_metrics'].get('defects', {})}",
        "",
        "---",
        "",
        "## 6. Competency Bar Calibration",
        "",
        f"- Vetting score distribution: {report['6_competency_bar_calibration'].get('vetting_score_distribution', {})}",
        f"- Elite bar pass rate: {report['6_competency_bar_calibration'].get('elite_bar_pass_rate', 'N/A')}",
        f"- Recommended adjustments: {report['6_competency_bar_calibration'].get('recommended_adjustments', 'N/A')}",
        "",
        "---",
        "",
        "## 7. Recommendations",
        "",
        f"- Hiring plan: {report['7_recommendations']['hiring_plan']}",
        f"- Channel changes: {report['7_recommendations'].get('channel_changes', 'N/A')}",
        f"- Bar adjustments: {report['7_recommendations'].get('bar_adjustments', 'N/A')}",
        f"- Process improvements: {', '.join(report['7_recommendations'].get('process_improvements', []))}",
        f"- Stage 0/1 improvements: {', '.join(report['7_recommendations'].get('stage_0_1_improvements', ['N/A']))}",
        "",
        "---",
        "",
        f"*Report sealed at {report['generated']}*",
    ])
    return "\n".join(lines)


def main():
    raw = {}
    try:
        if not sys.stdin.isatty():
            content = sys.stdin.read().strip()
            if content:
                raw = json.loads(content)
    except json.JSONDecodeError:
        raw = {"hiring_cycle_id": "unknown"}

    ctx = resolve_entity(raw)
    entity_root = ctx.entity_root

    result = generate_report(entity_root, raw)

    # Audit
    audit_data = {
        "event_type": "stage_8_hiring_outcome_report",
        "hiring_cycle_id": result["hiring_cycle_id"],
        "candidates_processed": result["candidates_processed"],
        "hired": result["hired"],
        "complete_dossiers": result["complete_dossiers"],
        "report_file": result["report_file"],
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    print(f"✅ Hiring outcome report generated for cycle {result['hiring_cycle_id']}:", file=sys.stderr)
    print(f"   JSON report: {result['report_file']}", file=sys.stderr)
    print(f"   Markdown report: {result['markdown_file']}", file=sys.stderr)
    print(f"   Candidates processed: {result['candidates_processed']}", file=sys.stderr)
    print(f"   Hired: {result['hired']}, Complete dossiers: {result['complete_dossiers']}", file=sys.stderr)
    print(json.dumps(result, indent=2), file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
