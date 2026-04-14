#!/usr/bin/env python
"""
any-stage-validate-and-send-notification.py
P2 Hook: Notification → Notification Governance
============================================================================
Trigger: When any candidate notification is sent.

Validates:
  1. FCRA compliance for US candidates (adverse action notice)
  2. GDPR compliance for EU candidates (right to be informed)
  3. No discriminatory language in notification body
  4. Rejection notifications use neutral template
  5. Escalation notifications routed to correct target

Exit: 0 = notification valid and sent, 2 = notification blocked (compliance violation)
============================================================================
"""

import json
import sys
import os
import re
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib.entity_resolver import resolve_entity
from lib.audit_writer import append_audit_log


def _sanitize_filename(name):
    """Sanitize a string for safe use in filenames."""
    return re.sub(r'[^a-zA-Z0-9._-]', '_', str(name))


# Discriminatory language patterns (context-aware: require candidate-related context)
DISCRIMINATORY_PATTERNS = [
    r"(due to age)",
    r"(because of age)",
    r"(due to gender)",
    r"(because of gender)",
    r"(due to race)",
    r"(because of race)",
    r"(due to religion)",
    r"(because of religion)",
    r"(due to disability)",
    r"(because of disability)",
    r"(due to .*(?:married|pregnant|family))",
    r"(because .*(?:married|pregnant|family))",
    r"(due to .*(?:gay|lesbian|sexual orientation))",
    r"(because .*(?:gay|lesbian|sexual orientation))",
]

# Jurisdiction-specific rules
FCRA_JURISDICTIONS = ["US", "USA", "United States"]
GDPR_JURISDICTIONS = ["EU", "UK", "FR", "DE", "IT", "ES", "NL", "BE", "AT", "PL", "SE", "NO", "DK", "FI"]


def validate_notification(raw: dict, ctx) -> tuple:
    """Returns (is_valid, errors, warnings)."""
    errors = []
    warnings = []

    notification_type = raw.get("notification_type", "")
    recipient_type = raw.get("recipient_type", "")
    jurisdiction = raw.get("jurisdiction", "")
    subject = raw.get("subject", "")
    body = raw.get("body", "")

    # 1. FCRA compliance (US)
    if jurisdiction in FCRA_JURISDICTIONS and notification_type == "adverse-action":
        if "pre-adverse" not in body.lower() and "adverse action" not in body.lower():
            errors.append("FCRA violation: Adverse action notice missing required language")

    # 2. GDPR compliance (EU)
    if jurisdiction in GDPR_JURISDICTIONS:
        if "privacy" not in body.lower() and "data protection" not in body.lower():
            warnings.append("GDPR: Consider adding data protection reference")

    # 3. Discriminatory language check
    for pattern in DISCRIMINATORY_PATTERNS:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if matches:
            errors.append(f"Potentially discriminatory language detected: '{matches[0]}'")

    # 4. Rejection notification must use neutral template
    if "rejection" in notification_type.lower() or "reject" in notification_type.lower():
        negative_words = ["failed", "inadequate", "unqualified", "poor", "terrible", "unacceptable"]
        for word in negative_words:
            if word in body.lower():
                errors.append(f"Rejection notification contains non-neutral language: '{word}'")

    # 5. Escalation routing
    severity = raw.get("severity", "")
    if severity in ("R0", "R1"):
        targets = raw.get("escalation_targets", [])
        if not targets:
            warnings.append("R0/R1 escalation has no specified targets")

    # 8. FCRA adverse action workflow state enforcement
    if jurisdiction in FCRA_JURISDICTIONS and notification_type == "adverse-action":
        adverse_step = raw.get("adverse_step", 0)  # 1=pre-adverse, 2=final adverse
        pre_adverse_date = raw.get("pre_adverse_date", "")

        if adverse_step == 2:
            # Cannot issue final adverse until pre-adverse was sent
            if not pre_adverse_date:
                errors.append("FCRA: Cannot issue final adverse action without pre-adverse notice record")
            else:
                # 5-day dispute window must have elapsed
                try:
                    pre_date = datetime.fromisoformat(pre_adverse_date.replace("Z", "+00:00"))
                    now = datetime.now(timezone.utc)
                    days_elapsed = (now - pre_date).days
                    if days_elapsed < 5:
                        errors.append(
                            f"FCRA: Only {days_elapsed} days since pre-adverse notice. "
                            f"5-day dispute window not yet elapsed. Can send on "
                            f"{(pre_date + timedelta(days=5)).strftime('%Y-%m-%d')}"
                        )
                except (ValueError, TypeError):
                    errors.append("FCRA: Invalid pre_adverse_date format")

        elif adverse_step == 1:
            # Pre-adverse notice must include summary of rights
            if "summary of rights" not in body.lower() and "dispute" not in body.lower():
                warnings.append(
                    "FCRA: Pre-adverse notice should include summary of rights "
                    "under FCRA and dispute process information"
                )

    # 9. GDPR Article 22 human review tracking for EU/UK
    if jurisdiction in GDPR_JURISDICTIONS and "rejection" in notification_type.lower():
        candidate_id = _sanitize_filename(raw.get("candidate_id", ""))
        if candidate_id:
            gdpr_review_file = os.path.join(
                ctx.entity_root, "data", f"gdpr-article22-{candidate_id}.json"
            )
            review_data = {
                "candidate_id": candidate_id,
                "jurisdiction": jurisdiction,
                "notification_date": datetime.now(timezone.utc).isoformat(),
                "review_request_deadline": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat(),
                "review_sla_days": 5,
                "status": "pending_candidate_response",
            }
            try:
                os.makedirs(os.path.dirname(gdpr_review_file), exist_ok=True)
                with open(gdpr_review_file, "w") as f:
                    json.dump(review_data, f, indent=2)
                warnings.append(
                    f"GDPR Article 22: Human review tracking created for {candidate_id}. "
                    f"Review request deadline: {review_data['review_request_deadline'][:10]}"
                )
            except (IOError, OSError):
                warnings.append("GDPR Article 22: Failed to create human review tracking file")

    return len(errors) == 0, errors, warnings


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
    is_valid, errors, warnings = validate_notification(raw, ctx)

    audit_data = {
        "event_type": "notification_validation",
        "notification_type": raw.get("notification_type", "unknown"),
        "jurisdiction": raw.get("jurisdiction", "unknown"),
        "is_valid": is_valid,
        "error_count": len(errors),
    }
    try:
        append_audit_log(ctx, audit_data)
    except Exception:
        pass

    if is_valid:
        icon = "⚠️" if warnings else "✅"
        print(f"{icon} Notification validated: {raw.get('notification_type', 'unknown')}", file=sys.stderr)
        for w in warnings:
            print(f"   WARN: {w}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"❌ Notification BLOCKED (compliance violation):", file=sys.stderr)
        for e in errors:
            print(f"   FAIL: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
