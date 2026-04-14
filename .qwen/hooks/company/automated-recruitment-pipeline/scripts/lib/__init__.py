# Recruitment Pipeline Hook Library
# Shared utilities for all hook scripts.
from .entity_resolver import resolve_entity, get_entity_root, get_audit_path
from .audit_writer import append_audit_log, compute_entry_hash, get_last_hash
from .artifact_parser import parse_artifact, extract_frontmatter, parse_markdown_fallback
from .validators import (
    check_required, check_range, check_enum,
    check_nested, validate_artifact_file, has_frontmatter,
)

__all__ = [
    "resolve_entity", "get_entity_root", "get_audit_path",
    "append_audit_log", "compute_entry_hash", "get_last_hash",
    "parse_artifact", "extract_frontmatter", "parse_markdown_fallback",
    "check_required", "check_range", "check_enum",
    "check_nested", "validate_artifact_file", "has_frontmatter",
]
