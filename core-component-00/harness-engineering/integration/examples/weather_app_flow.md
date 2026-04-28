# How Harness Engineering Processes User Requests: A Deep Dive

When a user says **"Help me build a beautiful Weather App"**, the Harness Engineering system doesn't execute this directly. Instead, it orchestrates a **multi-stage decision-making process** that ensures robust, accurate results.

---

## Table of Contents

1. [Stage 1: Intent Classification](#stage-1-intent-classification)
2. [Stage 2: Information Gap Detection](#stage-2-information-gap-detection)
3. [Stage 3: Tool Selection & Boundaries](#stage-3-tool-selection--boundaries)
4. [Stage 4: Fallback Degradation Paths](#stage-4-fallback-degradation-paths)
5. [Stage 5: Error Recovery Hierarchy](#stage-5-error-recovery-hierarchy)
6. [Complete Decision Flow Diagram](#complete-decision-flow-diagram)

---

## Stage 1: Intent Classification

### Step 1.1: Parse the Request

```python
class IntentClassifier:
    """Classifies user requests into categories for appropriate handling."""

    REQUEST = "Help me build a beautiful Weather App"

    @classmethod
    def classify(cls, request) -> Dict:
        # Extract key semantic elements
        elements = cls._extract_elements(request)

        return {
            "primary_intent": "APPLICATION_CONSTRUCTION",  # Build something new
            "task_type": "CREATIVE",                      # Needs design + logic
            "domain": "WEATHER_DATA",                     # Weather domain knowledge needed
            "complexity": "HIGH",                         # Multi-step project
        }
```

### Step 1.2: Detect Task Requirements

| Element              | Extraction Method   | Value for "Weather App"           |
| -------------------- | ------------------- | --------------------------------- |
| **Domain**           | Keyword analysis    | `WEATHER_API`, `METEOROLOGICAL`   |
| **Creative needs**   | Adjective detection | `"beautiful"` → UI/UX priority    |
| **Functional scope** | NLP parsing         | Real-time data, forecasts, maps   |
| **Target platform**  | Context check       | Web/mobile? (needs clarification) |

### Step 1.3: Classify Task Complexity

```python
def assess_complexity(intent):
    """Assess how many subtasks this request implies"""

    WEATHER_APP_COMPLEXITY = {
        "frontend": ["UI design", "weather widget rendering"],
        "backend": ["API calls", "data caching"],
        "data_layer": ["forecast queries", "historical data"],
        "maps_integration": ["geolocation", "map tiles"],
    }

    return "MULTI_COMPONENT"  # Requires orchestration of multiple tools
```

---

## Stage 2: Information Gap Detection

**Critical Question:** _"Can I complete this request with the information provided?"_

### Step 2.1: Missing Information Checklist

```python
class InformationGapDetector:
    """Identifies missing information needed for accurate execution."""

    WEATHER_APP_REQUIREMENTS = [
        "target_platform",       # Web, iOS, Android?
        "design_style",          # Minimalist, colorful, dashboard?
        "weather_api",           # OpenWeatherMap, WeatherAPI, custom?
        "user_location",         # Current or manual selection?
        "data_refresh_rate",     # Every minute? Hourly? Daily?
    ]
```

### Step 2.2: Decision Matrix - Ask vs. Assume

| Missing Information Type                          | Should We Ask?           | Rationale                                   |
| ------------------------------------------------- | ------------------------ | ------------------------------------------- |
| **Critical for accuracy** (API key, location)     | ✅ YES                   | Without it, results fail or are wrong       |
| **Style preference** (color scheme, layout)       | ⚠️ PROCEED WITH DEFAULTS | Can iterate later if user prefers otherwise |
| **Optional enhancements** (maps, historical data) | ⚠️ OFFER AS OPTIONS      | Don't block main flow, but offer additions  |

### Step 2.3: Clarification Strategy

```python
async def handle_ambiguity(required_info, optional_suggestions) -> str:
    """Decides whether to ask clarifying questions or proceed with defaults."""

    # CRITICAL INFO - MUST ASK (or state our assumptions clearly)
    critical_missing = [
        item for item in required_info
        if item not in ["target_platform", "weather_api"]  # Can infer or suggest
    ]

    if critical_missing:
        return f"Need clarification on:\n" + "\n".join(critical_missing)

    # Can proceed with reasonable defaults for non-critical items
    elif optional_suggestions:
        return (
            "I'll build this with sensible defaults.\n"
            "Would you like to add these enhancements?\n" +
            "\n".join(optional_suggestions)
        )

    else:
        return "I have enough information to proceed!"
```

**For the Weather App:**

The system might respond:

```
┌─────────────────────────────────────────────────────────┐
│  ✅ I'll start building your weather app with these:     │
│                                                           │
│  - Platform: Web app (fastest to deploy)                 │
│  - API: OpenWeatherMap (free tier, easy integration)      │
│  - Design: Clean, modern dashboard style                  │
│  - Location: User's browser geolocation                   │
│                                                           │
│  Optional enhancements available:                        │
│  [ ] Real-time map visualization                          │
│  [ ] Historical weather data charts                       │
│  [ ] Forecast notifications (push to browser)             │
│                                                           │
│  Would you like me to add any of these?                  │
└─────────────────────────────────────────────────────────┘
```

---

## Stage 3: Tool Selection & Boundaries

### Step 3.1: Identify Required Tools

```python
TOOL_REGISTRY = {
    "openweather_api": {
        "description": "Fetch current weather and forecasts",
        "timeout_seconds": 15,
        "requires_approval": False,
    },
    "geolocation_service": {
        "description": "Get user's current location",
        "timeout_seconds": 10,
        "requires_approval": True,  # Privacy-sensitive operation
    },
    "ui_component_generator": {
        "description": "Create weather widget components",
        "timeout_seconds": 30,
        "requires_approval": False,
    },
}
```

### Step 3.2: Verify Tool Boundaries

| Tool                     | Max Calls     | Requires Approval | Reasoning                                      |
| ------------------------ | ------------- | ----------------- | ---------------------------------------------- |
| `openweather_api`        | 5 per session | No                | Can cache results; frequent calls not needed   |
| `geolocation_service`    | 1 per session | Yes               | Privacy-sensitive; needs explicit user consent |
| `ui_component_generator` | Unlimited     | No                | Stateless generation; no risk                  |

### Step 3.3: Execute with Error Boundaries

```python
from implementations.error_boundary import SafeModelCall, SafeToolCall

# Create safe wrappers for each tool
async def build_weather_app_workflow():
    geolocation_tool = SafeToolCall(
        lambda x: await get_user_location(),
        timeout=10,
        require_approval=True  # Critical privacy gate
    )

    api_tool = SafeToolCall(
        fetch_openweather_data,
        timeout=15
    )

    ui_tool = SafeModelCall(
        client, model="claude-3-opus", timeout=30
    )
```

---

## Stage 4: Fallback Degradation Paths

### Step 4.1: Define Fallback Tiers

| Tier                 | Approach                                         | When Used                            |
| -------------------- | ------------------------------------------------ | ------------------------------------ |
| **Tier 1 (Full)**    | Complete weather app with all features           | API works, geolocation granted       |
| **Tier 2 (Limited)** | Basic weather display without maps/maps disabled | Geolocation denied but API available |
| **Tier 3 (Static)**  | Static HTML template with placeholder data       | API unavailable or rate-limited      |

### Step 4.2: Fallback Implementation

```python
async def build_weather_app_with_fallbacks():
    """Build app with tiered degradation paths."""

    try:
        # Tier 1: Full implementation
        location = await geolocation_tool.execute({})
        weather_data = await api_tool.execute({"lat": location.lat, "lon": location.lon})
        ui_components = await ui_tool.execute(
            generate_ui_prompt(weather_data, style="modern-dashboard")
        )

        return build_complete_app(ui_components, weather_data)

    except GeolocationDeniedError:
        # Fallback to Tier 2: Manual location input
        location_input = ask_for_manual_location()
        weather_data = await api_tool.execute({"query": location_input})
        return build_limited_app(weather_data)

    except APIUnavailableError:
        # Fallback to Tier 3: Static template
        return load_static_weather_template()
```

---

## Stage 5: Error Recovery Hierarchy

### Step 5.1: Define Error Categories and Recovery Paths

| Error Type           | Cause                          | Detection                | Recovery Action                     |
| -------------------- | ------------------------------ | ------------------------ | ----------------------------------- |
| `TIMEOUT`            | API slow/unresponsive          | Response > timeout       | Retry (2s, 4s, 8s backoff)          |
| `API_ERROR`          | Invalid API key                | HTTP 401/403             | Suggest user provides valid key     |
| `RATE_LIMIT`         | Too many requests              | HTTP 429                 | Wait then retry; fallback to Tier 2 |
| `GEOLOCATION_DENIED` | Browser blocked access         | Error during geolocation | Offer manual location input         |
| `INVALID_DATA`       | API returns malformed response | Schema validation fails  | Retry with simpler request          |

### Step 5.2: Error Message Layering

```python
def format_error_for_user(error):
    """Layer error messages from technical to user-friendly."""

    if error.code == "TIMEOUT":
        return {
            "user_message": "I'm having trouble fetching the latest weather data.",
            "technical_details": f"Request timed out after {error.timeout}s",
            "suggested_action": "Please try again in a moment."
        }

    elif error.code == "API_ERROR":
        return {
            "user_message": "I need a valid weather API key to fetch data.",
            "technical_details": f"API returned {error.status_code}: {error.message}",
            "suggested_action": (
                "Sign up for a free OpenWeatherMap API key at openweathermap.org/"
                " and share it with me."
            )
        }

    else:
        return {
            "user_message": error.user_message,
            "technical_details": error.technical_details,
            "suggested_action": "Please retry the operation."
        }
```

---

## Complete Decision Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│              User Request: Weather App                    │
└─────────────────────────────────────────────────────────┘
                          ↓
          ┌───────────────────────────────────┐
          │ Stage 1: Intent Classification    │
          ├───────────────────────────────────┤
          │ - Parse: "build a beautiful app"   │
          │ - Identify domain: WEATHER         │
          │ - Assess complexity: HIGH          │
          └───────────────────────────────────┘
                          ↓
          ┌───────────────────────────────────┐
          │ Stage 2: Information Gap Analysis  │
          ├───────────────────────────────────┤
          │ - Check missing: platform, API,    │
          │   location, design style           │
          │ - Decide: Ask or assume defaults   │
          └───────────────────────────────────┘
                          ↓
          ┌───────────────────────────────────┐
          │ Stage 3: Tool Selection            │
          ├───────────────────────────────────┤
          │ - Build tool registry              │
          │ - Apply boundaries (timeout,       │
          │   call limits)                     │
          └───────────────────────────────────┘
                          ↓
          ┌───────────────────────────────────┐
          │ Stage 4: Fallback Paths Setup      │
          ├───────────────────────────────────┤
          │ - Define Tier 1 (full) → Tier 3   │
          │   (static template)                │
          └───────────────────────────────────┘
                          ↓
          ┌───────────────────────────────────┐
          │ Stage 5: Error Boundary Wrappers   │
          ├───────────────────────────────────┤
          │ - Wrap each tool call with         │
          │   specific error handlers          │
          │ - Format errors for user           │
          └───────────────────────────────────┘
                          ↓
              ┌────────────────────┐
              │ BUILD WEATHER APP  │
              ├────────────────────┤
              │ (with all safety   │
              │   layers enabled)  │
              └────────────────────┘
```

---

## Summary: Why This Multi-Stage Approach?

### Problem Without Harness Engineering

| Issue            | What Happens Without Harness Patterns                         |
| ---------------- | ------------------------------------------------------------- |
| **Ambiguity**    | LLM assumes wrong platform (iOS vs. Web) → builds wrong thing |
| **Tool Failure** | API timeout breaks entire workflow, no recovery path          |
| **Privacy Risk** | Calls geolocation without consent; violates privacy norms     |
| **Poor UX**      | Returns technical error messages directly to user             |

### Solution With Harness Engineering

| Benefit                   | How It Helps                                               |
| ------------------------- | ---------------------------------------------------------- |
| **Robustness**            | Fallback paths ensure partial success even when parts fail |
| **Privacy Safety**        | Explicit approval gates for sensitive operations           |
| **Clear Communication**   | Layered error messages from technical to user-friendly     |
| **Iterative Improvement** | Can clarify missing info mid-flow, not just at start       |

---

## Key Takeaway

**Harness Engineering turns ambiguous natural language requests into robust, production-grade workflows by:**

1. **Analyzing intent and requirements** → Understanding what the user wants vs. what they've specified
2. **Detecting information gaps** → Asking clarifying questions when accuracy requires them, assuming defaults when safe to proceed
3. **Applying safety boundaries** → Never letting tools make unbounded or unsafe calls
4. **Preparing fallback paths** → Always having a Tier 1→2→3 degradation plan
5. **Formatting errors humanly** → Never exposing technical details directly to users

---

**Last Updated:** 2026-04-24  
**Version:** 1.0  
**Maintained by:** Claude Lab Engineering Team
