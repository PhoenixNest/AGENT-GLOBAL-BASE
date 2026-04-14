"""
validators.py — Common validation utilities for hook scripts.

Provides reusable check functions that all hooks can use.
"""


def check_required(data: dict, field: str, path: str = "") -> list:
    """
    Check that a required field exists and is non-empty.
    Returns list of error strings (empty if valid).
    """
    full_path = f"{path}.{field}" if path else field
    value = data.get(field)
    if value is None or (isinstance(value, str) and not value.strip()):
        return [f"{full_path} is required"]
    if isinstance(value, list) and len(value) == 0:
        return [f"{full_path} must be non-empty"]
    return []


def check_range(value, min_val, max_val, field_name: str = "") -> list:
    """
    Check that a numeric value is within [min_val, max_val].
    Returns list of error strings (empty if valid).
    """
    errors = []
    try:
        v = float(value)
        if v < min_val or v > max_val:
            label = field_name or str(value)
            errors.append(f"{label} = {value} is out of range [{min_val}, {max_val}]")
    except (TypeError, ValueError):
        errors.append(f"{field_name or 'value'} = {value} is not a valid number")
    return errors


def check_enum(value, allowed: list, field_name: str = "") -> list:
    """
    Check that a value is one of the allowed enum values.
    Returns list of error strings (empty if valid).
    """
    if value not in allowed:
        label = field_name or str(value)
        return [f"{label} = '{value}' not in allowed values: {allowed}"]
    return []


def check_sum(values: list, expected: float, tolerance: float = 0.01,
              field_name: str = "sum") -> list:
    """
    Check that the sum of values is within tolerance of expected.
    Returns list of error strings (empty if valid).
    """
    try:
        total = sum(float(v) for v in values)
        if abs(total - expected) > tolerance:
            return [f"{field_name} = {total:.4f}, expected {expected} ± {tolerance}"]
    except (TypeError, ValueError) as e:
        return [f"{field_name}: cannot sum values: {e}"]
    return []


def check_nested(data: dict, path: str) -> tuple:
    """
    Navigate a nested dict via dot-separated path.
    Returns (value, True) or (None, False).
    """
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None, False
    return current, True


def validate_artifact_file(filepath: str) -> tuple:
    """
    Check that an artifact file exists on disk.
    Returns (True, "") or (False, error_message).
    """
    import os
    if not os.path.exists(filepath):
        return False, f"Artifact file not found: {filepath}"
    if not os.path.isfile(filepath):
        return False, f"Expected file, got directory: {filepath}"
    return True, ""


def has_frontmatter(filepath: str) -> bool:
    """
    Check if a file starts with YAML frontmatter.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            return first_line == "---"
    except (IOError, UnicodeDecodeError):
        return False
