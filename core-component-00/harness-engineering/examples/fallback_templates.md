# Degradation Fallback Templates

This folder contains static template responses for degradation fallback paths. These are used when the primary LLM-based approach fails or is unavailable.

---

## Tier 1→2→3 Fallback Hierarchy

### Tier 1 (Best): Full Model Response

- Complete model reasoning with tool use
- Personalized, context-aware responses

### Tier 2 (Fallback): Simplified Schema Response

- Model uses simplified prompt without tools
- Returns structured but less personalized output
- Uses default assumptions for missing context

### Tier 3 (Degraded): Static Template Response

- Pre-written templates with placeholder data
- No model invocation
- Generic but functional response

---

## Template Categories

### Category 1: Information Retrieval Tasks

#### Template 1.1: General Knowledge Query

```markdown
[INFORMATION REQUESTED]

Based on my training data (cutoff {current_date}), I can provide you with:

{TOPIC_SUMMARY}

**Key Points:**

- {KEY_POINT_1}
- {KEY_POINT_2}
- {KEY_POINT_3}

**Sources Mentioned:** {SOURCE_LIST}

**Note:** For the most current information on {TOPIC}, please check official sources as my knowledge may be outdated.
```

#### Template 1.2: Time-Sensitive Query

```markdown
[TIME-SENSITIVE LIMITATION]

I cannot access real-time data beyond my training cutoff ({current_date}).

**What I can do:**

- Provide historical context about {TOPIC}
- Explain the concepts and principles involved
- Guide you to current resources

**Recommended Resources for Current Information:**

1. {RESOURCE_1_URL}: {RESOURCE_1_DESCRIPTION}
2. {RESOURCE_2_URL}: {RESOURCE_2_DESCRIPTION}

Would you like me to help structure a search query instead?
```

---

### Category 2: Tool-Dependent Tasks

#### Template 2.1: File Operations Failed

```markdown
[FILE OPERATION LIMITATION]

I attempted to access the file at path: `{file_path}`

**Result:** Access denied or file not found.

**Possible reasons:**

1. Path is incorrect or outdated
2. File has been moved/renamed
3. I don't have permission to read this file

**Suggested actions:**

- Verify the file path is correct
- Check that you've granted me access to read files in this directory
- Try providing a relative path if possible

Would you like to try a different file, or provide more specific instructions?
```

#### Template 2.2: Search Tool Unavailable

```markdown
[SEARCH FUNCTION LIMITATION]

I attempted to search for information about `{QUERY}` but the search function is currently unavailable.

**What this means:**

- I cannot access external sources for current information
- My knowledge is limited to my training cutoff ({current_date})

**Alternative approaches:**

1. I can provide general background information on related topics
2. I can help you construct search queries for your preferred tools
3. I can explain the concepts behind what you're researching

Would you like me to try one of these alternatives instead?
```

#### Template 2.3: Web Navigation Failed

```markdown
[WEB NAVIGATION LIMITATION]

I attempted to access: `{url}`

**Result:** The page is unavailable or I cannot navigate to it.

**Common causes:**

- Page moved or removed
- Requires authentication/login
- Blocked by browser policies
- Connection issues

**What I can do instead:**

- Provide information about similar accessible resources
- Help you locate alternative sources
- Explain the topic from general knowledge

Would you like me to suggest alternative resources?
```

---

### Category 3: Computation Tasks

#### Template 3.1: Complex Calculation Failed

```markdown
[COMPUTATION LIMITATION]

I attempted to perform the calculation but encountered limitations.

**Original request:** Calculate {original_expression}

**Result:** Unable to compute directly due to expression complexity.

**Alternative approaches:**

1. Break down into simpler steps if you provide them
2. Use an external calculator and provide intermediate values
3. I can help identify which part is most complex

Would you like to try a different approach?
```

#### Template 3.2: Data Analysis Requested

```markdown
[DATA ANALYSIS LIMITATION]

I cannot perform direct data analysis on the provided data without tool access.

**What I can do instead:**

1. Explain what types of analysis would be appropriate for this data
2. Suggest statistical methods or approaches to use
3. Help you write code to perform the analysis

**Recommended tools:**

- Python with pandas for tabular data analysis
- SQL for database-based queries
- Specialized tools depending on your data type

Would you like me to suggest an analysis approach instead?
```

---

### Category 4: Creative Writing Tasks

#### Template 4.1: Creative Generation Requested

```markdown
[CREATIVE WRITING REQUEST]

**Topic:** {topic}

**Your requirements:** {requirements_summary}

**My approach:** I will generate a response with the structure you requested, though creative output is inherently variable.

**Template structure:**

- Opening: {expected_opening_style}
- Main content: Will follow your specified format
- Closing: {expected_closing_style}

Note: Creative outputs vary in quality. If the generated content doesn't meet expectations, please provide specific feedback so I can improve.
```

---

### Category 5: Reasoning/Analysis Tasks

#### Template 5.1: Complex Reasoning Requested

```markdown
[COMPLEX REASONING REQUEST]

**Task:** {task_description}

**My reasoning approach:**
I will break this down step by step, though please note that complex multi-step reasoning may not be perfect.

**If you notice errors or incomplete reasoning:**

- Point out specific steps that seem wrong
- Provide the correct answer if you know it
- This helps me improve my reasoning patterns

**Step 1:** {first_step_description}
...

_Note: For complex problems, consider providing intermediate checkpoints to verify progress._

Would you like me to continue with my best available reasoning?
```

---

## Implementation Guide

### How to Use These Templates

1. **In your code:** Check if model response validation failed
2. **If validation fails:** Return appropriate tier-2 fallback (simplified schema)
3. **If tier-2 also unavailable:** Return tier-3 template with placeholders filled

```python
# Example fallback logic
def get_fallback_response(task_type, error_reason):
    if task_type == "search" and error_reason == "tool_unavailable":
        return fill_template(TEMPLATE_SEARCH_FAILED, query=original_query)
    elif task_type == "file_read" and error_reason == "permission_denied":
        return fill_template(TEMPLATE_FILE_ACCESS_FAILED, path=requested_path)
    # Add more conditions for different error types
    return DEFAULT_UNAVAILABLE_RESPONSE
```

### Template Variables

Common variables used across templates:

| Variable                | Description                         | Example Value                                                  |
| ----------------------- | ----------------------------------- | -------------------------------------------------------------- |
| `{current_date}`        | Model knowledge cutoff date         | "2024-12"                                                      |
| `{QUERY}`               | Original search/query text          | "latest AI research findings"                                  |
| `{TOPIC}`               | Subject being queried               | "machine learning best practices"                              |
| `{file_path}`           | Requested file path                 | "/data/reports/2024/q1.pdf"                                    |
| `{url}`                 | Requested URL                       | "[https://example.com/api/data](https://example.com/api/data)" |
| `{original_expression}` | Mathematical/computation expression | "SUM(products.price) WHERE..."                                 |

---

## Template Customization Guidelines

### Do Customize:

- The introductory acknowledgment of limitation
- The specific error explanation for your use case
- Any suggested alternative actions relevant to your application
- Resource links pointing to your organization's preferred sources

### Don't Customize:

- The core structure of the fallback message
- The transparency about model limitations
- Suggested alternatives (they help users understand system behavior)

---

## Testing Fallback Paths

### Deterministic Test Cases for Fallbacks

```python
def test_fallback_search_unavailable():
    """Test that search unavailable returns proper template"""
    response = get_fallback_response("search", "tool_unavailable")
    assert "[SEARCH FUNCTION LIMITATION]" in response
    assert "current_date" not in response  # Should be replaced
    return response

def test_fallback_file_access_denied():
    """Test that file access denied returns proper template"""
    response = get_fallback_response("file_read", "permission_denied")
    assert "[FILE OPERATION LIMITATION]" in response
    assert "file_path" not in response  # Should be replaced
    return response
```

### Edge Cases to Cover

- Empty query string → Use generic "search unavailable" template
- Very long query (>500 chars) → Summarize and use short-version template
- Multiple tool failures → Return most relevant limitation message
- Network timeout vs. auth error → Distinguish in error classification

---

## Example Filled Template (Runtime Output)

```markdown
[SEARCH FUNCTION LIMITATION]

I cannot access external sources for current information.
My knowledge is limited to my training cutoff (2024-12).

**What I can do:**

- Provide historical context about LLM-based code generation
- Explain the concepts and principles involved
- Guide you to current resources

**Recommended Resources for Current Information:**

1. https://arxiv.org/keyword/LLM+CodeGeneration: Research papers on LLM code capabilities
2. https://github.com/topics/code-generation: GitHub repository examples

Would you like me to help structure a search query instead?
```

---

**Last Updated:** 2026-04-24  
**Version:** 1.0  
**Maintained by:** Claude Lab Engineering Team
