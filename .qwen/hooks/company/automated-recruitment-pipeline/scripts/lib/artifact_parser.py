"""
artifact_parser.py — Parse YAML frontmatter + markdown body from pipeline artifacts.

Supports two modes:
  1. Frontmatter mode: YAML between --- delimiters, parsed with safe_load
  2. Fallback mode: regex extraction from markdown body (for legacy artifacts)

Usage:
    from lib.artifact_parser import parse_artifact

    result = parse_artifact("/path/to/stage5-vetting-gate.md")
    # result.frontmatter → dict (parsed YAML)
    # result.body        → str  (markdown text after frontmatter)
    # result.has_frontmatter → bool
    # result.fallback    → dict (regex-extracted fields, if no frontmatter)
"""

import re
import os


class ParseResult:
    """Result of parsing a markdown artifact."""

    def __init__(self, filepath: str, frontmatter: dict = None,
                 body: str = "", has_frontmatter: bool = False,
                 fallback: dict = None):
        self.filepath = filepath
        self.frontmatter = frontmatter or {}
        self.body = body
        self.has_frontmatter = has_frontmatter
        self.fallback = fallback or {}

    @property
    def data(self) -> dict:
        """Return frontmatter if present, else fallback data."""
        return self.frontmatter if self.has_frontmatter else self.fallback

    def get(self, key: str, default=None):
        """Get a field from frontmatter or fallback."""
        if self.has_frontmatter and key in self.frontmatter:
            return self.frontmatter[key]
        return self.fallback.get(key, default)

    def __repr__(self):
        status = "frontmatter" if self.has_frontmatter else "fallback"
        return f"ParseResult({self.filepath}, mode={status})"


def parse_artifact(filepath: str) -> ParseResult:
    """
    Parse a markdown artifact file.

    Tries YAML frontmatter first. Falls back to regex extraction.
    """
    if not os.path.exists(filepath):
        return ParseResult(filepath)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return ParseResult(filepath)

    # Try frontmatter parsing
    fm = extract_frontmatter(content)
    if fm:
        # Split body
        body_match = re.match(r"^---\n.*?\n---\n(.*)", content, re.DOTALL)
        body = body_match.group(1).strip() if body_match else ""
        return ParseResult(filepath, frontmatter=fm, body=body, has_frontmatter=True)

    # Fallback: regex extraction based on file pattern
    fallback = parse_markdown_fallback(filepath, content)
    return ParseResult(filepath, fallback=fallback)


def extract_frontmatter(content: str) -> dict:
    """
    Extract YAML frontmatter from markdown content.

    Returns dict if frontmatter found, None otherwise.
    """
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        return None

    fm_text = match.group(1)
    return _parse_simple_yaml(fm_text)


def _parse_simple_yaml(text: str) -> dict:
    """
    Minimal YAML parser for flat/nested frontmatter.
    Handles: scalars, lists, simple nested dicts.
    Not a full YAML parser — good enough for our frontmatter schema.
    """
    try:
        import yaml
        return yaml.safe_load(text) or {}
    except ImportError:
        # yaml not available — use fallback parser
        return _parse_yaml_fallback(text)
    except Exception:
        return _parse_yaml_fallback(text)


def _parse_yaml_fallback(text: str) -> dict:
    """Fallback YAML parser (line-by-line). Handles nested dicts and lists."""
    result = {}
    current_key = None
    current_dict = None
    list_key = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        # Reset context when indent returns to top level
        if indent == 0:
            current_dict = None
            list_key = None

        # List item under a key (dict items like "  - name: value")
        m = re.match(r"^\s+-\s+(\w+):\s+(.*)", line)
        if m and list_key:
            key, val = m.groups()
            item = {_yaml_convert(key): _yaml_convert_val(val)}
            if not isinstance(result.get(list_key), list):
                result[list_key] = []
            result[list_key].append(item)
            continue

        # Simple list item (like "  - engineering")
        m = re.match(r"^\s+-\s+(.*)", line)
        if m and list_key:
            val = m.group(1).strip()
            if not isinstance(result.get(list_key), list):
                result[list_key] = []
            result[list_key].append(_yaml_convert_val(val))
            continue

        # Nested dict key (indent > 0, no value after colon)
        m = re.match(r"^(\s+)(\w[\w_-]*):\s*$", line)
        if m and indent > 0 and current_key:
            key = _yaml_convert(m.group(2))
            if not isinstance(result.get(current_key), dict):
                result[current_key] = {}
            result[current_key][key] = {}
            current_dict = result[current_key][key]
            continue

        # Nested dict value (indent > 0, has value)
        m = re.match(r"^(\s+)(\w[\w_-]*):\s*(.*)", line)
        if m and indent > 0:
            key = _yaml_convert(m.group(2))
            val = m.group(3).strip()
            if current_key and isinstance(result.get(current_key), dict):
                result[current_key][key] = _yaml_convert_val(val)
            elif current_dict is not None:
                current_dict[key] = _yaml_convert_val(val)
            list_key = None
            continue

        # Top-level key with value
        m = re.match(r"^(\w[\w_-]*):\s*(.*)", line)
        if m:
            key, val = m.groups()
            key = _yaml_convert(key)
            val = val.strip()

            # Reset nested context on new top-level key
            current_dict = None
            list_key = None

            if not val:
                # Start of nested dict or list
                list_key = key
                current_key = key
                current_dict = None
                result[key] = {}  # Will be populated by subsequent indented items
                continue
            else:
                list_key = None
                current_dict = None
                result[key] = _yaml_convert_val(val)
                current_key = key

    return result


def _yaml_convert(key: str) -> str:
    """Convert YAML key to Python-friendly name."""
    return key.strip().strip('"').strip("'")


def _yaml_convert_val(val: str):
    """Convert YAML value to appropriate Python type."""
    val = val.strip().strip('"').strip("'")
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.lower() in ("null", "~"):
        return None
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


def parse_markdown_fallback(filepath: str, content: str) -> dict:
    """
    Extract structured data from markdown via regex patterns.

    Used when YAML frontmatter is not present (legacy artifacts).
    """
    data = {}
    filename = os.path.basename(filepath)

    # Document ID
    m = re.search(r"\*\*Document ID:\*\*\s*(\S+)", content)
    if m:
        data["document_id"] = m.group(1)

    # Generated/Date
    m = re.search(r"\*\*(?:Generated|Date):\*\*\s*(\S+)", content)
    if m:
        data["generated_at"] = m.group(1)

    # Gate Status
    m = re.search(r"\*\*Gate Status:\*\*\s*(.*)", content)
    if m:
        data["gate_status"] = m.group(1).strip()

    # Candidate name from title
    m = re.search(r"#\s+(?:VETTING GATE|HIRING OUTCOME REPORT|Offer Document|"
                  r"Provisioning Record|Background Check Report|"
                  r"Interview Scores|Screening Results|"
                  r"Sourcing Shortlist|Position Specification Document|"
                  r"Hiring Outcome Report)\s*[-–—]?\s*(.+)", content)
    if m:
        name_part = m.group(1).strip()
        # Extract name from "Anya Petrova (G24)" or just "Anya Petrova"
        name_m = re.match(r"([A-Za-z\s'-]+?)(?:\s*\((\w+)\))?", name_part)
        if name_m:
            data["candidate_name"] = name_m.group(1).strip()
            if name_m.group(2):
                data["candidate_id"] = name_m.group(2)

    # Stage-specific extractions
    if "vetting" in filename.lower() or "stage5" in filename.lower():
        data.update(_parse_vetting_fallback(content))
    elif "interview" in filename.lower() or "stage4" in filename.lower():
        data.update(_parse_interview_fallback(content))
    elif "offer" in filename.lower() or "stage7" in filename.lower():
        data.update(_parse_offer_fallback(content))
    elif "background" in filename.lower() or "stage6" in filename.lower():
        data.update(_parse_background_fallback(content))
    elif "hiring" in filename.lower() or "stage9" in filename.lower():
        data.update(_parse_hiring_outcome_fallback(content))
    elif "provisioning" in filename.lower() or "stage8" in filename.lower():
        data.update(_parse_provisioning_fallback(content))
    elif "screening" in filename.lower() or "stage3" in filename.lower():
        data.update(_parse_screening_fallback(content))
    elif "sourcing" in filename.lower() or "stage2" in filename.lower():
        data.update(_parse_sourcing_fallback(content))
    elif "psd" in filename.lower() or "stage1" in filename.lower():
        data.update(_parse_psd_fallback(content))

    return data


def _parse_vetting_fallback(content: str) -> dict:
    """Extract vetting scores from markdown body."""
    data = {}
    scores = {}

    m = re.search(r"Impact at Scale:\s*(\d+)/5", content)
    if m: scores["impact_at_scale"] = int(m.group(1))

    m = re.search(r"Craft Depth:\s*(\d+)/5", content)
    if m: scores["craft_depth"] = int(m.group(1))

    m = re.search(r"Leadership Signal:\s*(\d+)/5", content)
    if m: scores["leadership_signal"] = int(m.group(1))

    m = re.search(r"Standards Signal:\s*(\d+)/5", content)
    if m: scores["standards_signal"] = int(m.group(1))

    m = re.search(r"Red Flag Scan:\s*(PASS|FAIL)", content)
    if m: scores["red_flag_scan"] = m.group(1)

    if scores:
        data["scores"] = scores

    m = re.search(r"Total:\s*(\d+)/20", content)
    if m: data["total_score"] = int(m.group(1))

    m = re.search(r"VETTING RESULT:\s*(PASS|FAIL)", content, re.IGNORECASE)
    if m: data["result"] = m.group(1).upper()

    return data


def _parse_interview_fallback(content: str) -> dict:
    """Extract interview scores from markdown table."""
    data = {}
    assessments = []

    for m in re.finditer(r"\|\s*(.+?)\s*\|\s*([\d.]+)\s*\|\s*(\d+)%\s*\|\s*([\d.]+)\s*\|", content):
        component, score, weight, weighted = m.groups()
        component = component.strip()
        if component in ("Composite", ""):
            continue
        assessments.append({
            "component": component,
            "score": float(score),
            "weight": int(weight) / 100.0,
            "weighted_score": float(weighted),
        })

    if assessments:
        data["assessments"] = assessments

    m = re.search(r"\*\*Composite\*\*.*?\*\*([\d.]+)\*\*", content, re.DOTALL)
    if m: data["composite_score"] = float(m.group(1))

    m = re.search(r"(\d+)st|\b(\d+)th\b|(\d+)nd", content)
    if m: data["percentile"] = int(m.group(1) or m.group(2) or m.group(3))

    m = re.search(r"Bar Raiser:\s*(\w+\s*\w*)", content)
    if m: data["bar_raiser"] = m.group(1).strip()

    return data


def _parse_offer_fallback(content: str) -> dict:
    """Extract offer details from markdown body."""
    data = {}
    offer = {}

    m = re.search(r"Base\s*\$?([\d,]+)", content)
    if m: offer["base_salary"] = int(m.group(1).replace(",", ""))

    m = re.search(r"Bonus\s*(\d+)%", content)
    if m: offer["bonus_percent"] = float(m.group(1))

    m = re.search(r"Equity\s*([\d.]+)%", content)
    if m: offer["equity_percent"] = float(m.group(1))

    m = re.search(r"Signing\s*\$?([\d,]+)", content)
    if m: offer["signing_bonus"] = int(m.group(1).replace(",", ""))

    m = re.search(r"Start:\s*([\d-]+)", content)
    if m: offer["start_date"] = m.group(1)

    if offer:
        data["offer"] = offer

    m = re.search(r"\*\*Status:\*\*\s*(accepted|declined|extended|negotiating)", content, re.IGNORECASE)
    if m:
        data["status"] = m.group(1).lower()
    elif re.search(r"accepted", content, re.IGNORECASE):
        data["status"] = "accepted"

    return data


def _parse_background_fallback(content: str) -> dict:
    """Extract background check results from markdown body."""
    data = {}
    checks = {}

    if "Employment" in content:
        checks["employment_verification"] = "CLEAR" if "✅" in content.split("Employment")[1].split("\n")[0] else "FLAGGED"

    if "Education" in content:
        checks["education_verification"] = "CLEAR" if "✅" in content.split("Education")[1].split("\n")[0] else "FLAGGED"

    if "Criminal" in content:
        checks["criminal_background"] = "CLEAR" if "Clear" in content.split("Criminal")[1].split("\n")[0] else "FLAGGED"

    if "References" in content:
        checks["reference_checks"] = "CLEAR" if "✅" in content.split("References")[1].split("\n")[0] else "FLAGGED"

    if "COI" in content:
        checks["conflict_of_interest"] = "CLEAR" if "Clear" in content.split("COI")[1].split("\n")[0] else "FLAGGED"

    if checks:
        data["checks"] = checks

    m = re.search(r"\*\*Overall:\*\*\s*(?:✅\s*)?(CLEAR|FLAGGED|FAIL)", content)
    if m: data["overall_status"] = m.group(1)

    return data


def _parse_hiring_outcome_fallback(content: str) -> dict:
    """Extract hiring outcome from markdown body."""
    data = {}

    m = re.search(r"\*\*HIRED\*\*|\*\*NOT_HIRED\*\*|\*\*ROLLED_BACK\*\*", content)
    if m:
        data["final_decision"] = m.group(1).replace("**", "").replace("*", "")
    elif "HIRED" in content:
        data["final_decision"] = "HIRED"

    m = re.search(r"Vetting:\s*(\d+)/20", content)
    if m: data["vetting_total"] = int(m.group(1))

    m = re.search(r"Composite:\s*([\d.]+)", content)
    if m: data["composite_score"] = float(m.group(1))

    m = re.search(r"Time-to-Fill:\s*(\d+)", content)
    if m: data["time_to_fill_days"] = int(m.group(1))

    m = re.search(r"Placement:\s*`([^`]+)`", content)
    if m: data["placement_path"] = m.group(1)

    m = re.search(r"Reports To:\s*(.+?)(?:\||$)", content)
    if m: data["reports_to"] = m.group(1).strip()

    m = re.search(r"Start:\s*([\d-]+)", content)
    if m: data["start_date"] = m.group(1)

    return data


def _parse_provisioning_fallback(content: str) -> dict:
    """Extract provisioning status from markdown body."""
    data = {}
    provisioning = {}

    provisioning["accounts_created"] = "Email" in content or "Slack" in content
    provisioning["equipment_ordered"] = "Workstation" in content or "RTX" in content
    provisioning["software_licenses"] = any(x in content for x in ["Maya", "Unity", "Substance", "license"])
    provisioning["buddy_assigned"] = "Buddy:" in content
    provisioning["manager_briefing"] = True  # Assumed if provisioning exists
    provisioning["documentation_sent"] = True

    data["provisioning"] = provisioning

    m = re.search(r"(L\d)\s+Clearance", content)
    if m: data["clearance_level"] = m.group(1)

    return data


def _parse_screening_fallback(content: str) -> dict:
    """Extract screening results from markdown body."""
    data = {}

    m = re.search(r"(\d+)\s*screened", content, re.IGNORECASE)
    if m: data.setdefault("screening", {})["total_screened"] = int(m.group(1))

    m = re.search(r"(\d+)\s*passed", content, re.IGNORECASE)
    if m: data.setdefault("screening", {})["passed"] = int(m.group(1))

    m = re.search(r"(\d+)\s*reject", content, re.IGNORECASE)
    if m: data.setdefault("screening", {})["auto_rejected"] = int(m.group(1))

    # Extract candidate-specific fields
    m = re.search(r"percentile.*?(\d+)", content, re.IGNORECASE)
    if m: data.setdefault("screening", {})["candidate_percentile"] = int(m.group(1))

    m = re.search(r"(PASS|AUTO_REJECT)", content)
    if m: data.setdefault("screening", {})["candidate_result"] = m.group(1)

    return data


def _parse_sourcing_fallback(content: str) -> dict:
    """Extract sourcing results from markdown body."""
    data = {}

    m = re.search(r"Top\s*(\d+):", content)
    if m: data.setdefault("sourcing_results", {})["top_5_count"] = int(m.group(1))

    return data


def _parse_psd_fallback(content: str) -> dict:
    """Extract PSD details from markdown body."""
    data = {}

    m = re.search(r"\*\*Role:\*\*\s*(.+?)(?:\||$)", content)
    if m: data["role_title"] = m.group(1).strip()

    m = re.search(r"\*\*Family:\*\*\s*(\w+)", content)
    if m: data["role_family"] = m.group(1).strip()

    m = re.search(r"\*\*Seniority:\*\*\s*(\w+)", content)
    if m: data["seniority"] = m.group(1).strip()

    m = re.search(r"\*\*Priority:\*\*\s*(P\d)", content)
    if m: data["priority"] = m.group(1)

    m = re.search(r"\*\*Band:\*\*\s*\$?([\d,]+K?)\s*[–-]\s*\$?([\d,]+K?)", content)
    if m:
        min_s = m.group(1).replace(",", "").replace("K", "000")
        max_s = m.group(2).replace(",", "").replace("K", "000")
        data["compensation_band"] = {"min": int(min_s), "max": int(max_s)}

    m = re.search(r"\*\*Reports To:\*\*\s*(.+?)(?:\||$)", content)
    if m: data["reports_to"] = m.group(1).strip()

    return data
