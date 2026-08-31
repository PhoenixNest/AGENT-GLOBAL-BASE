# RAG Edge Cases and Handling Guide

## Comprehensive Reference for Production RAG Edge Cases

This guide addresses common edge cases, failure modes, and their mitigation strategies in production RAG systems.

---

## Quick Reference: Edge Case Matrix

| Category               | Edge Case                              | Severity | Mitigation Strategy                                        | Implementation Priority |
| ---------------------- | -------------------------------------- | -------- | ---------------------------------------------------------- | ----------------------- |
| **Retrieval Quality**  | Out-of-scope query (topic not covered) | Medium   | Guardrail response; clarify limitations                    | High                    |
|                        | Ambiguous query intent                 | Medium   | Ask clarifying question OR return multiple interpretations | Medium                  |
|                        | Contradictory sources in context       | High     | Weight by recency; present all views with citations        | High                    |
|                        | Very short single-chunk relevant info  | Low      | Use smaller chunks for specific lookups                    | Medium                  |
|                        | Very long multi-document topics        | Medium   | Context compression + hierarchical summarization           | High                    |
| **Generation Quality** | LLM hallucination (unsupported claims) | Critical | Fact-checking pipeline; citation enforcement               | Critical                |
|                        | Token budget overflow                  | Medium   | Truncate least-relevant chunks first                       | High                    |
|                        | Repetitive responses                   | Medium   | Add diversity penalty in prompt engineering                | Medium                  |
|                        | Code generation errors                 | High     | Validate code syntax; add unit tests                       | High                    |
| **System Performance** | Query cache poisoning                  | Low-High | Content-addressed caching + TTL rotation                   | Medium                  |
|                        | Embedding service OOM                  | Critical | Graceful degradation to cached responses                   | High                    |
|                        | Vector DB connection loss              | High     | Circuit breaker + automatic reconnection                   | High                    |
|                        | Rate limit exceeded (LLM provider)     | Medium   | Retry with exponential backoff                             | Medium                  |
| **Security**           | Prompt injection attack                | Critical | Input sanitization; output filtering                       | Critical                |
|                        | Unauthorized document access           | Critical | Pre-filter ACL; immutable audit logs                       | Critical                |
|                        | PII leakage in response                | Critical | Masking layer at both ingestion and retrieval              | Critical                |
| **Data Quality**       | Corrupted/invalid embeddings           | Medium   | Fallback to cached result or skip generation               | Medium                  |
|                        | Duplicate document chunks              | Low      | Deduplication on ingestion; fingerprint-based filtering    | Low                     |
|                        | Outdated documentation                 | Medium   | Timestamp-aware retrieval; versioned indexing              | High                    |

---

## 1. Out-of-Scope Query Handling

### Problem

User asks about a topic not covered in your documentation (e.g., personal topics when system is corporate knowledge base).

### Detection Strategies

```python
from typing import Optional, Dict, Any


def detect_out_of_scope(query: str, context: list[str]) -> Dict[str, Any]:
    """Detect if query is out of scope based on retrieved context."""

    # Strategy 1: Check retrieval confidence score
    avg_confidence = sum(c.get("confidence_score", 0.5) for c in context) / len(context)
    low_confidence = avg_confidence < 0.4

    # Strategy 2: Analyze retrieved document domains
    domains = set()
    for chunk in context:
        doc_source = chunk.get("source", "")
        if "harness-engineering" in doc_source or "prompt-engineering" in doc_source:
            domains.add("technical")
        elif "docs.public" in doc_source:
            domains.add("public-facing")

    is_technical_domain = len(domains & {"technical"}) > 0

    # Strategy 3: Check for topic keywords
    technical_keywords = [
        "RAG", "vector database", "embedding", "chunking", "retrieval",
        "orchestrator", "inference", "LLM", "API", "endpoint"
    ]

    query_lower = query.lower()
    has_technical_terms = any(kw in query_lower for kw in technical_keywords)

    return {
        "is_out_of_scope": not (low_confidence and is_technical_domain and has_technical_terms),
        "confidence_score": avg_confidence,
        "reasoning": _generate_reasoning(avg_confidence, domains, query_lower),
    }


def _generate_reasoning(confidence: float, domains: set, query: str) -> str:
    if confidence < 0.4 and len(domains) < 2:
        return "Low confidence retrieval with narrow domain scope"
    return "Confident retrieval across relevant domains"
```

### Recommended Response Patterns

| Scenario                   | Response Pattern Example                                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Genuinely out-of-scope** | "I don't have information on [topic] in my knowledge base. I specialize in technical documentation about [my domain]. Can I help you with something related?" |
| **Partially covered**      | "I found some relevant information, but it's incomplete: [partial answer]. For more details, please check [specific document]."                               |
| **Wrong source selected**  | "That information appears to be from a different source. My knowledge covers [correct domain]. Let me search the right documentation."                        |

### Implementation with Guardrails

```python
from typing import Dict, Any


async def generate_with_guards(query: str, context: list[str]) -> Dict[str, Any]:
    """Generate response with out-of-scope detection."""

    # Detect out of scope
    scope_check = detect_out_of_scope(query, context)

    if scope_check["is_out_of_scope"]:
        return {
            "response": _generate_guardrail_response(query),
            "metadata": {
                "status": "out_of_scope",
                "confidence_score": scope_check["confidence_score"],
                "suggested_domains": [d for d in ["engineering", "tech"] if "engineering" not in query.lower()]
            }
        }

    # Normal generation
    return await _generate_normal_response(query, context)


def _generate_guardrail_response(query: str) -> str:
    """Generate appropriate response for out-of-scope queries."""
    patterns = [
        "I don't have information on that topic in my knowledge base.",
        "That falls outside the scope of documentation I can access.",
        "My knowledge is limited to technical and engineering content.",
    ]

    return f"{patterns[0]}. Can you ask something related to [engineering/technical topics]?"
```

---

## 2. Ambiguous Query Intent Handling

### Problem

User's query has multiple possible interpretations.

### Detection Strategies

```python
from typing import List, Dict


def analyze_query_ambiguity(query: str) -> Dict[str, Any]:
    """Analyze whether a query is ambiguous."""

    # Pattern 1: Multiple keywords with equal weight
    ambiguous_patterns = [
        r"(\w+)\s+(\w+)",  # Two nouns without clear relationship
        r"how\s+(to\s+)?\w+",  # "How to X" where X could be many things
        r"what\s+(do\s+does|is)\s+\w+",  # "What is X/What do X"
    ]

    import re

    has_pattern_match = any(re.match(p, query, re.IGNORECASE) for p in ambiguous_patterns)

    # Pattern 2: Generic nouns without modifiers
    generic_nouns = ["component", "function", "file", "config", "api"]
    query_words = query.lower().split()
    word_counts = [query.count(word) for word in generic_nouns if len(word) > 3]

    has_generic_terms = sum(word_counts) > 1

    # Pattern 3: No clear entity (no specific names, numbers, etc.)
    specific_tokens = r"(\d+|[A-Za-z0-9_-]+)"  # Numbers or alphanumeric IDs
    token_match = re.search(specific_tokens, query)

    is_specific = token_match is not None

    return {
        "is_ambiguous": has_pattern_match and (has_generic_terms or not is_specific),
        "ambiguity_type": _classify_ambiguity(query),
        "confidence": 0.6 if has_pattern_match else 0.9,
    }


def _classify_ambiguity(query: str) -> str:
    """Classify the type of ambiguity."""
    lower = query.lower()

    if any(x in lower for x in ["api", "endpoint", "interface"]):
        return "entity_specificity"  # Which API/endpoint?
    elif any(x in lower for x in ["config", "setting", "option"]):
        return "property_specificity"  # Which configuration?
    else:
        return "general_vagueness"
```

### Response Strategies

```python
from typing import List, Dict


async def handle_ambiguous_query(query: str) -> Dict[str, Any]:
    """Handle ambiguous queries with clarification or multi-path retrieval."""

    analysis = analyze_query_ambiguity(query)

    if analysis["is_ambiguous"]:
        ambiguity_type = analysis["ambiguity_type"]

        # Strategy 1: Multi-path retrieval (retrieve for each interpretation)
        if ambiguity_type == "entity_specificity":
            interpretations = await _get_interpretations(query)

            return {
                "response": _generate_multi_path_response(interpretations),
                "metadata": {
                    "strategy": "multi_path",
                    "interpretations_found": len(interpretations),
                }
            }

        # Strategy 2: Ask clarifying question
        elif ambiguity_type in ["property_specificity", "general_vagueness"]:
            return {
                "response": _generate_clarification_request(query),
                "metadata": {
                    "strategy": "clarification_requested",
                }
            }

    return await _handle_clear_query(query)


def _get_interpretations(query: str) -> List[str]:
    """Generate possible interpretations of ambiguous query."""
    # Simple heuristic: generate variations
    variations = [
        f"information about {query}",
        f"How to use {query}",
        f"What is {query}",
    ]
    return list(set(variations))


def _generate_multi_path_response(interpretations: List[str]) -> str:
    """Generate response covering multiple interpretations."""
    if len(interpretations) == 1:
        return f"Regarding '{interpretations[0]}': {retrieved_answer}"

    # Cover top 2-3 interpretations
    top = interpretations[:3]
    responses = [
        retrieval.get_answer(interpretation)
        for interpretation in top
    ]

    return (
        "Based on your question, here are the most relevant answers:\n\n" +
        "\\n\\n".join(f"{i+1}. {resp}" for i, resp in enumerate(responses))
    )


def _generate_clarification_request(query: str) -> str:
    """Generate clarification request."""
    clarifications = []

    # Extract key entities from query
    entities = re.findall(r'\b(?:api|endpoint|config|file|function)\b', query, re.I)

    if not entities:
        return (
            "Your question could have multiple interpretations. "
            "Could you please provide more details or specify what you're looking for?"
        )

    return (
        f"I want to make sure I give you the right information. "
        f"Do you mean {entities[0]} or something else? "
        f"Here are some options that might help:\n\n" +
        "\\n".join(f"- {i}. General overview of {entities[i] if i < len(entities) else 'the topic'}"
                   for i in range(min(3, len(entities))))
    )


def _handle_clear_query(query: str) -> Dict[str, Any]:
    """Handle queries with clear intent."""
    # Normal retrieval and generation flow
    return {
        "response": retrieved_answer,
        "metadata": {"strategy": "direct_retrieval"},
    }
```

---

## 3. Contradictory Sources Handling

### Problem

Different retrieved documents contain conflicting information.

### Detection Strategies

```python
from typing import List, Dict


def detect_contradictions(context: List[Dict]) -> List[Dict]:
    """Detect contradictions among retrieved context."""

    contradictions = []

    for i in range(len(context)):
        for j in range(i + 1, len(context)):
            chunk_a = context[i]
            chunk_b = context[j]

            # Extract key claims from each chunk
            claims_a = _extract_claims(chunk_a.get("text", ""))
            claims_b = _extract_claims(chunk_b.get("text", ""))

            for claim_a in claims_a:
                for claim_b in claims_b:
                    if not _claims_compatible(claim_a, claim_b):
                        contradictions.append({
                            "chunk_ids": [chunk_a.get("id"), chunk_b.get("id")],
                            "claim_a": claim_a,
                            "claim_b": claim_b,
                            "confidence": _compute_contradiction_confidence(
                                chunk_a, chunk_b
                            ),
                        })

    return contradictions


def _extract_claims(text: str) -> List[str]:
    """Extract factual claims from text."""
    # Simple pattern matching for factual statements
    claims = []

    patterns = [
        r"(\w+(?:\s+\w+){0,5})\s*(?:is|are|was|were|should|must|can)\s*(\S+)",
        r"(\d+)\s*(?:percent|million|billion)?",  # Numeric claims
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.I)
        for match in matches:
            if isinstance(match, tuple):
                claims.append(" ".join(filter(None, match)))
            else:
                claims.append(match)

    return list(set(claims))


def _claims_compatible(claim_a: str, claim_b: str) -> bool:
    """Check if two claims are compatible (not directly contradictory)."""

    # Direct contradiction patterns
    contradiction_patterns = [
        (r"\b(most|all)\b.*\b(not|never)\b", r"\b(not|never).*\b(most|all)\b"),  # Quantifier negation
        (r"should\s+(?:not\s+)?(\S+)", r"(?:must|shall)\s+\1"),  # Must vs should
    ]

    for pattern_a, pattern_b in contradiction_patterns:
        if re.search(pattern_a, claim_a) and re.search(pattern_b, claim_b):
            return False

    # Similarity-based check
    from difflib import SequenceMatcher
    similarity = SequenceMatcher(None, claim_a.lower(), claim_b.lower()).ratio()

    return similarity > 0.5 or len(claim_a) != len(claim_b)


def _compute_contradiction_confidence(chunk_a: Dict, chunk_b: Dict) -> float:
    """Compute confidence in contradiction detection."""
    # Weight by source credibility (if available)
    score_a = chunk_a.get("metadata", {}).get("source_credibility", 0.5)
    score_b = chunk_b.get("metadata", {}).get("source_credibility", 0.5)

    avg_credibility = (score_a + score_b) / 2

    # Lower confidence source reduces contradiction confidence
    return min(0.9, avg_credibility)
```

### Response Strategies for Contradictions

```python
from typing import Dict


async def handle_contradictory_context(
    query: str,
    context: List[Dict],
    contradictions: List[Dict]
) -> Dict[str, Any]:
    """Generate response handling contradictory information."""

    if not contradictions:
        return await _generate_normal_response(query, context)

    # Strategy 1: Weighted consensus (most credible source wins)
    consensus = await _compute_weighted_consensus(contradictions, context)

    if len(consensus) >= 2:
        # Present all views with citations
        return {
            "response": _generate_multi_view_response(consensus),
            "metadata": {
                "status": "multiple_perspectives",
                "perspective_count": len(consensus),
                "primary_view": consensus[0]["view"],  # Most credible
            },
        }

    # Strategy 2: Present as ongoing discussion (single perspective)
    return {
        "response": _generate_single_view_response(consensus[0]),
        "metadata": {
            "status": "unresolved",
            "recommendation": "For final decision, consult the most recent documentation.",
            "primary_source": consensus[0]["source"],
        },
    }


def _compute_weighted_consensus(
    contradictions: List[Dict],
    context: List[Dict]
) -> List[Dict]:
    """Compute weighted view based on source credibility and recency."""

    # Assign weights to each chunk
    weights = {}
    for chunk in context:
        weight = 0.5  # Base weight

        # Boost recent sources
        timestamp = chunk.get("metadata", {}).get("timestamp")
        if timestamp:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                age_hours = (datetime.utcnow() - dt).total_seconds() / 3600
                weight += min(0.2, max(-0.2, 100 - age_hours) / 500)
            except:
                pass

        # Boost high-confidence embeddings
        confidence = chunk.get("confidence_score", 0.5)
        weight += (confidence - 0.5) * 0.3

        weights[chunk["id"]] = max(0, min(1.5, weight))

    # Filter out chunks with low consensus support
    total_weight = sum(weights.values())
    filtered_context = []

    for chunk in context:
        if weights[chunk["id"]] > (total_weight / len(context) * 0.5):  # Top 50% by weight
            filtered_context.append(chunk)

    return filtered_context


def _generate_multi_view_response(views: List[Dict]) -> str:
    """Generate response presenting multiple perspectives."""
    views_text = []

    for i, view in enumerate(views[:3]):  # Show top 3 views
        views_text.append(
            f"""View {i+1} ({view['source']}, {view.get('timestamp', 'unknown')}):
{view['view']}

Source: {[p['doc_id'] for p in view.get('citations', [])]}"""
        )

    return "\\n\\n".join(views_text)


def _generate_single_view_response(view: Dict) -> str:
    """Generate response presenting single authoritative view."""
    citations = view.get("citations", [])

    text = f"Based on the most relevant and recent documentation ({view['source']}):\n\n"

    if citations:
        text += "\\n".join(
            f"{p['doc_id']}: {p['span_text'][:100]}..."
            for p in citations[:3]
        )
    else:
        text += view.get("view", "Information not available.")

    return text
```

---

## 4. Context Window Overflow Handling

### Problem

Retrieved context exceeds model's token budget.

### Detection Strategies

```python
from typing import Dict


def check_token_budget(
    system_prompt_tokens: int = 100,
    context_chunks: list[str] = None,
    max_input_tokens: int = 4096,
) -> Dict[str, Any]:
    """Check if context exceeds token budget."""

    from transformers import PreTrainedTokenizerFast

    # Initialize tokenizer (use your model's tokenizer)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(
        "microsoft/phi-2",  # Example
        # Or use model-specific tokenizer
    )

    system_tokens = len(tokenizer.encode(system_prompt))
    total_context_tokens = sum(len(tokenizer.encode(chunk)) for chunk in context_chunks)
    total_input = system_tokens + total_context_tokens

    return {
        "within_budget": total_input <= max_input_tokens,
        "system_prompt_tokens": system_tokens,
        "context_tokens": total_context_tokens,
        "total_input_tokens": total_input,
        "max_input_tokens": max_input_tokens,
        "overflow_tokens": max(0, total_input - max_input_tokens),
    }


def optimize_context_for_budget(
    query: str,
    context_chunks: list[str],
    max_input_tokens: int = 4096,
) -> Dict[str, Any]:
    """Optimize context selection to fit within budget."""

    # Sort chunks by relevance score (descending)
    sorted_chunks = sorted(
        context_chunks,
        key=lambda c: c.get("relevance_score", 0),
        reverse=True
    )

    # Greedy selection with token counting
    selected_chunks = []
    current_tokens = len(tokenizer.encode(query)) + 100  # Query + system prompt

    for chunk in sorted_chunks:
        chunk_tokens = len(tokenizer.encode(chunk))

        if current_tokens + chunk_tokens <= max_input_tokens * 0.8:  # Leave 20% margin
            selected_chunks.append(chunk)
            current_tokens += chunk_tokens

    return {
        "selected_count": len(selected_chunks),
        "selected_chunks": selected_chunks,
        "total_tokens": current_tokens,
        "remaining_budget": max_input_tokens - current_tokens,
    }
```

### Context Compression Strategies

```python
from typing import List


class ContextCompressor:
    """Compress context while preserving key information."""

    def __init__(self):
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/phi-2",  # Use your model's tokenizer
        )
        self.summarizer = HuggingFacePipeline.from_model_id(
            "sshleifer/p50-summarization",
            config=None,
            tokenizer=self.tokenizer,
            feature_extractor=None,
            max_length=256,
            truncation=True,
        )

    def compress_context(self, chunks: List[Dict], target_tokens: int = 3500) -> Dict[str, Any]:
        """Compress context while preserving key information."""

        # Sort by relevance
        sorted_chunks = sorted(
            chunks,
            key=lambda c: c.get("relevance_score", 0),
            reverse=True
        )

        # Strategy: Hybrid approach - keep high-relevance chunks, summarize low ones
        compressed_text = ""
        chunk_count = 0

        for chunk in sorted_chunks:
            tokens_needed = len(self.tokenizer.encode(chunk.get("text", ""))) + 50

            if chunk_count == 0:
                # Always include the most relevant chunk fully
                compressed_text += chunk["text"] + "\\n\\n"
                chunk_count += 1

            elif chunk_count < 3:
                # Keep top 3 chunks fully (they may have important details)
                compressed_text += chunk["text"] + "\\n\\n"
                chunk_count += 1

            else:
                # Compress remaining chunks
                if tokens_needed > target_tokens - len(self.tokenizer.encode(compressed_text)):
                    # Budget exceeded, summarize this chunk
                    summary = self.summarizer(chunk["text"])
                    compressed_text += f"[Summarized from {chunk.get('source', 'doc')}] {summary}..." + "\\n\\n"
                else:
                    compressed_text += chunk["text"][:target_tokens - len(compressed_text)] + "..." + "\\n\\n"

        return {
            "compressed_text": compressed_text,
            "chunk_count": chunk_count,
            "token_count": len(self.tokenizer.encode(compressed_text)),
        }
```

---

## 5. Security Edge Cases

### Prompt Injection Detection

````python
import re


def detect_prompt_injection(query: str) -> Dict[str, Any]:
    """Detect potential prompt injection attacks."""

    dangerous_patterns = {
        "ignore_previous": [
            r"\b(ignore|stop|forget|do not consider|pretend|act as)\b.*?(instructions?|context|memory|history|previous)",
            r"```.*?```",  # Code block injection
            r"<\s*?\w+[^>]*>",  # HTML tag injection
            r"(system|user|assistant):\s*(.*?)(",
        ],
        "data_exfiltration": [
            r"who\s+(are|is)\s+(admin|owner|developer)",
            r"your\s+(name|model|company|database|server)",
            r"ip\s+address",
            r"datacenter\s+location",
        ],
        "authority_manipulation": [
            r"\b(admin|moderator|owner)\b.*?(you|system|bot)",
            r"You\smust",
            r"You\sshould",
        ],
    }

    detected_attacks = []

    for attack_type, patterns in dangerous_patterns.items():
        for pattern in patterns:
            if re.search(pattern, query, re.I):
                detected_attacks.append({
                    "type": attack_type,
                    "pattern_matched": pattern,
                    "severity": "high" if "exfiltration" in attack_type else "medium",
                })

    return {
        "is_safe": len(detected_attacks) == 0,
        "detected_attacks": detected_attacks,
        "query_hash": hash(query[:100]),  # For logging (not actual query)
    }
````

### PII Leakage Prevention

```python
import re


def sanitize_response_for_pii(response: str) -> Dict[str, Any]:
    """Mask PII in generated response."""

    pii_patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone_us": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        "ssn": r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b",
        "credit_card": r"\b(?:\d[ -]*?){16}\b",
        "ip_address": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
    }

    sanitized = response

    for pii_type, pattern in pii_patterns.items():
        matches = re.findall(pattern, sanitized)
        if matches:
            mask_str = "***REDACTED***"
            sanitized = re.sub(pattern, mask_str, sanitized, count=10)  # Limit masking
            detected_count = len(matches)

    return {
        "sanitized_response": sanitized,
        "pii_detected": any(
            len(re.findall(pattern, response)) > 0
            for pattern in pii_patterns.values()
        ),
        "pii_types_detected": [
            type for type, _ in pii_patterns.items()
            if len(re.findall(pii_patterns[type], response)) > 0
        ],
    }
```

---

## Monitoring and Alerting Setup

### Health Check with Edge Case Detection

```python
from typing import Dict


class RAGEdgeCaseMonitor:
    """Monitors for edge cases that need intervention."""

    def __init__(self):
        self.alert_thresholds = {
            "low_retrieval_confidence": 0.4,
            "high_hallucination_rate": 0.1,
            "prompt_injection_attempts": 0,
            "pii_leakage_count": 0,
        }

    async def check_health(self) -> Dict[str, Any]:
        """Run edge case health checks."""

        results = {
            "timestamp": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ"),
            "overall_status": "healthy",
            "checks": {},
        }

        # Check 1: Retrieval confidence distribution
        recent_confidences = self._get_recent_metric("retrieval_confidence")[:100]
        avg_confidence = sum(recent_confidences) / len(recent_confidences) if recent_confidences else 0.5

        if avg_confidence < self.alert_thresholds["low_retrieval_confidence"]:
            results["checks"]["retrieval_confidence"] = {
                "status": "warning",
                "value": avg_confidence,
                "threshold": self.alert_thresholds["low_retrieval_confidence"],
                "recommendation": "Review embedding model or add more documentation coverage."
            }
            results["overall_status"] = "degraded"

        # Check 2: Prompt injection attempts (should be 0)
        injection_count = self._get_recent_metric("prompt_injection_attempts")[-1] if self._get_recent_metric("prompt_injection_attempts") else 0

        if injection_count > 0:
            results["checks"]["prompt_injection"] = {
                "status": "critical",
                "count": injection_count,
                "recommendation": "Review input sanitization and block offending IPs/users."
            }
            results["overall_status"] = "degraded"

        return results

    def _get_recent_metric(self, metric_name: str) -> list[float]:
        """Placeholder for fetching recent metrics from monitoring system."""
        # In production, use Prometheus, Datadog, or custom metrics store
        return []
```

---

## Summary Table: Edge Case Handling Priorities

| Edge Case             | Mitigation Complexity              | Testing Requirement                   | Production Readiness       |
| --------------------- | ---------------------------------- | ------------------------------------- | -------------------------- |
| Out-of-scope queries  | Medium (guardrail responses)       | Golden dataset for out-of-scope tests | Ready with proper training |
| Ambiguous queries     | High (requires multi-path logic)   | Adversarial query testing             | Needs fine-tuning          |
| Contradictory sources | Medium (requires weighted ranking) | Source credibility evaluation         | Recommended pattern        |
| Context overflow      | Low (chunk selection heuristics)   | Token budget testing                  | Standard implementation    |
| Prompt injection      | Critical (must block all attacks)  | Security penetration testing          | Essential for enterprise   |
| PII leakage           | Critical (compliance requirement)  | Privacy impact assessment             | Mandatory with masking     |
