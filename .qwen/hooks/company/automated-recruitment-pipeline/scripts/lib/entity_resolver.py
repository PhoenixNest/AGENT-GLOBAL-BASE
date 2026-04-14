"""
entity_resolver.py — Resolve entity context from stdin JSON.

Hooks receive structured JSON via stdin. This module extracts:
  - entity_type: "studio" | "company"
  - entity_root: filesystem path root for the entity
  - candidate_path: path to the candidate's pipeline-artifacts directory
  - audit_path: computed path to entity-specific audit-log.jsonl

Usage:
    from lib.entity_resolver import resolve_entity

    ctx = resolve_entity(raw_input)
    # ctx.entity_root  → "studio/casual-games/team"
    # ctx.audit_path   → "studio/casual-games/team/audit/audit-log.jsonl"
    # ctx.candidate_path → "studio/casual-games/team/crew/art/3d-artist/anya-petrova"
"""

import os
import re


class EntityContext:
    """Resolved entity context."""

    def __init__(self, entity_type: str, entity_root: str,
                 candidate_id: str = "", candidate_name: str = "",
                 candidate_path: str = "", stage: str = "",
                 role_family: str = "", seniority: str = "",
                 hiring_cycle_id: str = "", role_id: str = ""):
        self.entity_type = entity_type
        self.entity_root = entity_root
        self.candidate_id = candidate_id
        self.candidate_name = candidate_name
        self.candidate_path = candidate_path
        self.stage = stage
        self.role_family = role_family
        self.seniority = seniority
        self.hiring_cycle_id = hiring_cycle_id
        self.role_id = role_id

    @property
    def audit_dir(self) -> str:
        """Directory for entity audit logs."""
        return os.path.join(self.entity_root, "audit")

    @property
    def audit_path(self) -> str:
        """Full path to entity audit-log.jsonl."""
        return os.path.join(self.audit_dir, "audit-log.jsonl")

    def artifact_path(self, filename: str) -> str:
        """Path to a specific artifact file within candidate's pipeline-artifacts."""
        if self.candidate_path:
            return os.path.join(self.candidate_path, "pipeline-artifacts", filename)
        return ""

    def __repr__(self):
        return (f"EntityContext(type={self.entity_type}, root={self.entity_root}, "
                f"candidate={self.candidate_id}, stage={self.stage})")


def resolve_entity(raw: dict) -> EntityContext:
    """
    Resolve entity context from raw stdin JSON.

    Priority:
    1. Explicit fields in stdin (entity_type, entity_root, candidate_path)
    2. Derive from studio/ field if present
    3. Derive from department/ field if present
    4. Fallback: try to infer from candidate_path pattern
    """
    # Normalize paths to OS-native separators
    entity_type = raw.get("entity_type", "")
    entity_root = raw.get("entity_root", "")
    if entity_root:
        entity_root = os.path.normpath(entity_root)
    candidate_path = raw.get("candidate_path", "")
    if candidate_path:
        candidate_path = os.path.normpath(candidate_path)
    candidate_id = raw.get("candidate_id", "")
    candidate_name = raw.get("candidate_name", "")
    stage = raw.get("stage", "")
    role_family = raw.get("role_family", "")
    seniority = raw.get("seniority", "")
    hiring_cycle_id = raw.get("hiring_cycle_id", "")
    role_id = raw.get("role_id", "")

    # If entity_root not explicit, try to derive
    if not entity_root:
        entity_root = _derive_entity_root(raw)

    # If entity_type not explicit, derive from root
    if not entity_type:
        # Normalize to forward slashes for consistent matching
        root_fwd = entity_root.replace("\\", "/")
        if root_fwd.startswith("studio/"):
            entity_type = "studio"
        elif root_fwd.startswith("company/departments/"):
            entity_type = "company"
        else:
            entity_type = "unknown"

    # If candidate_path not explicit, try to derive
    if not candidate_path and candidate_id:
        candidate_path = _derive_candidate_path(entity_root, raw)

    return EntityContext(
        entity_type=entity_type,
        entity_root=entity_root,
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        candidate_path=candidate_path,
        stage=stage,
        role_family=role_family,
        seniority=seniority,
        hiring_cycle_id=hiring_cycle_id,
        role_id=role_id,
    )


def _derive_entity_root(raw: dict) -> str:
    """Derive entity_root from available context fields."""
    # Studio context
    studio = raw.get("studio", "")
    if studio:
        return os.path.join("studio", studio, "team")

    # Company department context
    department = raw.get("department", "")
    if department:
        return os.path.join("company", "departments", department)

    # Try from candidate_path
    cp = raw.get("candidate_path", "")
    if cp:
        m = re.match(r"^(studio/[^/]+/team)", cp)
        if m:
            return m.group(1)
        m = re.match(r"^(company/departments/[^/]+)", cp)
        if m:
            return m.group(1)

    # Try from role_id or hiring_cycle_id pattern
    role_id = raw.get("role_id", "")
    if role_id.startswith("ROLE-"):
        # Company department pattern
        dept = raw.get("department", "engineering")
        return os.path.join("company", "departments", dept)

    # Absolute fallback — use repo root
    return os.getcwd()


def _derive_candidate_path(entity_root: str, raw: dict) -> str:
    """
    Derive candidate_path from entity_root and context.

    For studios: {entity_root}/crew/{role_family}/{slug}/
    For company: {entity_root}/{role_family}/{slug}/
    """
    candidate_id = raw.get("candidate_id", "")
    candidate_name = raw.get("candidate_name", "")
    role_family = raw.get("role_family", "")

    if not candidate_id and not candidate_name:
        return ""

    slug = _slugify(candidate_name or candidate_id)
    if not slug:
        return ""

    if entity_root.startswith("studio") or "studio" in entity_root:
        if role_family:
            return os.path.join(entity_root, "crew", role_family, slug)
        return os.path.join(entity_root, "crew", slug)
    else:
        # Company department
        if role_family:
            return os.path.join(entity_root, role_family, slug)
        return os.path.join(entity_root, slug)


def _slugify(name: str) -> str:
    """Convert a name to a filesystem-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower().strip()).strip("-")
    return slug if slug else "unknown"


def get_entity_root(raw: dict) -> str:
    """Convenience: get entity_root string from raw input."""
    return resolve_entity(raw).entity_root


def get_audit_path(raw: dict) -> str:
    """Convenience: get audit log path from raw input."""
    return resolve_entity(raw).audit_path
