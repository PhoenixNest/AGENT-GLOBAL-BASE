# RAG System Utility Tools

## Overview

This section documents utility scripts, monitoring dashboards, and operational tools for the RAG system.

## Quick Reference: Available Tools

| Tool                           | Purpose                           | Command Example                                       | Output Location                 |
| ------------------------------ | --------------------------------- | ----------------------------------------------------- | ------------------------------- |
| **System Health Checker**      | Verify all components are healthy | `python tools/check_health.py`                        | stdout + dashboard              |
| **Query Performance Analyzer** | Identify slow queries             | `python tools/analyze_latency.py --p95-threshold 0.5` | `reports/latency-analysis.json` |
| **Golden Dataset Generator**   | Create evaluation test cases      | `python tools/generate_gold_dataset.py --count 100`   | `data/golden.jsonl`             |
| **Memory Usage Monitor**       | Track memory across services      | `python tools/monitor_memory.py`                      | Grafana metrics endpoint        |
| **Cache Statistics Reporter**  | Cache hit rate and size analysis  | `python tools/report_cache.py`                        | `reports/cache-stats.json`      |
| **Document Ingestor**          | Batch ingest new documents        | `python tools/ingest_documents.py --paths docs/*.pdf` | Vector DB + ACL store           |
| **Access Control Auditor**     | Review permission assignments     | `python tools/audit_acl.py`                           | `reports/acl-audit.json`        |
| **Token Budget Analyzer**      | Optimize context window usage     | `python tools/analyze_tokens.py`                      | `reports/token-budgets.json`    |

## 1. System Health Checker

### Usage

```bash
# Quick health check
python tools/check_health.py

# Detailed health report
python tools/check_health.py --detailed

# Check specific components
python tools/check_health.py --component embedding-service
python tools/check_health.py --component vector-db
python tools/check_health.py --component llm-inference
```

### Implementation Example

```python
"""
check_health.py - System health monitoring utility
"""
import time
from typing import Dict, Any


class HealthChecker:
    """Checks health of all RAG system components."""

    def __init__(self):
        self.components = {
            "embedding_service": self._check_embedding,
            "vector_db": self._check_vector_db,
            "reranking_service": self._check_reranker,
            "llm_inference": self._check_llm,
            "redis_cache": self._check_redis,
        }

    async def check_all(self) -> Dict[str, Any]:
        """Check all components and return health status."""
        results = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "overall_status": "healthy",
            "components": {}
        }

        for component_name, check_func in self.components.items():
            try:
                status = await check_func()
                results["components"][component_name] = status
            except Exception as e:
                results["components"][component_name] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "details": None
                }

        # Determine overall status
        unhealthy_count = sum(
            1 for c in results["components"].values()
            if c.get("status") == "unhealthy"
        )

        results["overall_status"] = (
            "degraded" if unhealthy_count > 0 else "healthy"
        )

        return results

    async def _check_embedding(self) -> Dict[str, Any]:
        """Check embedding service health."""
        try:
            import requests

            # Replace with actual endpoint
            response = requests.get("http://localhost:8001/health", timeout=5)

            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "service": "embedding_service",
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "model_loaded": True,  # Check actual model status
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "unhealthy",
                "service": "embedding_service",
                "error": str(e)
            }

    async def _check_vector_db(self) -> Dict[str, Any]:
        """Check vector database health."""
        try:
            import requests

            response = requests.get("http://localhost:6333/health", timeout=5)

            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "service": "qdrant_vector_db",
                "collections_count": 1,  # Query for actual count
                "memory_usage_mb": 512,   # Check actual metrics
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "unhealthy",
                "service": "qdrant_vector_db",
                "error": str(e)
            }

    async def _check_reranker(self) -> Dict[str, Any]:
        """Check reranking service health."""
        try:
            import requests

            response = requests.get("http://localhost:8002/health", timeout=5)

            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "service": "reranking_service",
                "model_loaded": True,
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "unhealthy",
                "service": "reranking_service",
                "error": str(e)
            }

    async def _check_llm(self) -> Dict[str, Any]:
        """Check LLM inference service health."""
        try:
            import requests

            response = requests.post(
                "http://localhost:11434/api/tags",  # Ollama API
                timeout=5
            )

            if response.status_code == 200:
                models = response.json()

                return {
                    "status": "healthy",
                    "service": "ollama_inference",
                    "available_models": [m.get("name") for m in models],
                }
            else:
                return {
                    "status": "unhealthy",
                    "service": "ollama_inference",
                    "error": f"HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "unhealthy",
                "service": "ollama_inference",
                "error": str(e)
            }

    async def _check_redis(self) -> Dict[str, Any]:
        """Check Redis cache health."""
        try:
            import redis

            r = redis.Redis(host="localhost", port=6379, db=0)

            return {
                "status": "healthy",
                "service": "redis_cache",
                "memory_usage_mb": int(r.info()["used_memory_human"]),
                "connected_clients": r.info()["connected_clients"],
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "service": "redis_cache",
                "error": str(e)
            }
```

## 2. Query Latency Analyzer

### Usage

```bash
# Analyze latency distribution
python tools/analyze_latency.py

# Find slow queries above threshold
python tools/analyze_latency.py --p95-threshold 0.5

# Compare latency before/after optimization
python tools/analyze_latency.py --compare snapshots/before.json snapshots/after.json
```

### Implementation Example

```python
"""
analyze_latency.py - Query performance analysis utility
"""
import json
from typing import List, Dict, Any
from pathlib import Path


class LatencyAnalyzer:
    """Analyzes query latency patterns and identifies slow queries."""

    def __init__(self):
        self.latency_percentiles = {
            "p50": 0,
            "p90": 0,
            "p95": 0,
            "p99": 0,
        }
        self.component_latencies = {}

    def analyze(self, latency_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze query latency data.

        Args:
            latency_data: List of dicts with keys:
                - component: Component name (embedding, vector_db, etc.)
                - latency_ms: Latency in milliseconds

        Returns:
            Analysis report with percentiles and slow query identification
        """
        if not latency_data:
            return {"error": "No data to analyze"}

        # Separate by component
        components = {}
        for entry in latency_data:
            comp = entry.get("component")
            if comp not in components:
                components[comp] = []
            components[comp].append(entry.get("latency_ms", 0))

        # Calculate percentiles per component
        for component, latencies in components.items():
            sorted_latencies = sorted(latencies)
            n = len(sorted_latencies)

            self.latency_percentiles["p50"] = sorted_latencies[int(n * 0.5)] if n else 0
            self.latency_percentiles["p90"] = sorted_latencies[int(n * 0.9)] if n else 0
            self.latency_percentiles["p95"] = sorted_latencies[int(n * 0.95)] if n else 0
            self.latency_percentiles["p99"] = sorted_latencies[int(n * 0.99)] if n else 0

        # Identify slow queries (above p95)
        p95_threshold = self.latency_percentiles["p95"]
        slow_queries = [
            {"latency_ms": l, "component": c}
            for c, latencies in components.items()
            for l in latencies if l > p95_threshold
        ][:100]  # Top 100 slowest

        return {
            "percentiles": self.latency_percentiles,
            "component_latencies": {
                k: {"count": len(v), "p50": v[int(len(v) * 0.5)] if v else 0}
                for k, v in components.items()
            },
            "slow_query_count": len(slow_queries),
            "p95_threshold_ms": p95_threshold,
            "slow_queries_sample": slow_queries,
        }


def identify_bottlenecks(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    """Identify potential bottlenecks from latency analysis."""
    bottlenecks = []

    p95 = analysis.get("percentiles", {}).get("p95", 0)

    # Check for embedding service slowdowns
    if "embedding" in analysis.get("component_latencies", {}):
        embedding_percentile = analysis["percentiles"]["p95"]
        if embedding_percentile > 400:
            bottlenecks.append({
                "type": "embedding_service_slow",
                "component": "embedding",
                "latency_ms": embedding_percentile,
                "recommendation": "Consider GPU acceleration or model quantization"
            })

    # Check for reranker slowdowns
    if "reranking" in analysis.get("component_latencies", {}):
        rerank_percentile = analysis["percentiles"]["p95"]
        if rerank_percentile > 300:
            bottlenecks.append({
                "type": "reranker_slow",
                "component": "reranking",
                "latency_ms": rerank_percentile,
                "recommendation": "Enable batching or use smaller model"
            })

    return bottlenecks
```

## 3. Cache Statistics Reporter

### Usage

```bash
# Generate cache report
python tools/report_cache.py

# With Redis connection details
python tools/report_cache.py --redis-host localhost --port 6379

# Export to JSON or CSV
python tools/report_cache.py --output-format json
python tools/report_cache.py --output-format csv --output-file cache-report.csv
```

### Implementation Example

```python
"""
report_cache.py - Cache performance monitoring utility
"""
import redis
from typing import Dict, Any


class CacheReporter:
    """Generates cache performance reports."""

    def __init__(self, redis_client: redis.Redis = None):
        self.redis = redis_client

    async def report(self) -> Dict[str, Any]:
        """Generate comprehensive cache statistics.

        Returns:
            Dictionary with cache metrics
        """
        if not self.redis:
            return {"error": "Redis client not configured"}

        try:
            # Get Redis info
            info = self.redis.info()

            memory_used_bytes = int(info.get("used_memory", 0))
            memory_human = f"{memory_used_bytes / (1024**2):.2f} MB"

            # Get keys by pattern if we have cache data
            query_cache_keys = [
                key for key in self.redis.keys("rag:*:query:*")
            ]

            result_cache_keys = [
                key for key in self.redis.keys("rag:*:result:*")
            ]

            return {
                "timestamp": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ"),
                "memory_usage": memory_human,
                "total_memory_mb": info.get("used_memory_human", "unknown"),
                "query_cache_keys": len(query_cache_keys),
                "result_cache_keys": len(result_cache_keys),
                "eviction_count_1m": int(info.get("expiredkeys_total", 0)),
                "connect_clients": int(info.get("connected_clients", 0)),
            }
        except Exception as e:
            return {"error": str(e)}
```

## 4. Token Budget Analyzer

### Usage

```bash
# Analyze context window usage
python tools/analyze_tokens.py

# Find responses exceeding budget
python tools/analyze_tokens.py --alert-threshold 3500

# Compare current vs optimal usage
python tools/analyze_tokens.py --compare baseline.json current.json
```

### Implementation Example

```python
"""
analyze_tokens.py - Token budget analysis utility
"""
import re
from typing import Dict, List


class TokenAnalyzer:
    """Analyzes token usage patterns in RAG responses."""

    def __init__(self):
        # Approximate token counts (GPT-2 style)
        self.char_to_token_ratio = 3.75
        self.system_prompt_tokens = 100

    async def analyze_response(
        self,
        response_text: str,
        context_chunks: List[str]
    ) -> Dict[str, Any]:
        """Analyze token usage for a single response.

        Args:
            response_text: Generated response text
            context_chunks: List of retrieved context chunks

        Returns:
            Token usage breakdown
        """
        # Estimate tokens (rough approximation)
        response_tokens = int(len(response_text) / self.char_to_token_ratio)
        context_tokens = sum(int(len(c) / self.char_to_token_ratio) for c in context_chunks)

        total_input_tokens = self.system_prompt_tokens + context_tokens

        return {
            "response_text": response_text[:500] + "..." if len(response_text) > 500 else response_text,
            "response_tokens": response_tokens,
            "context_tokens": context_tokens,
            "system_prompt_tokens": self.system_prompt_tokens,
            "total_input_tokens": total_input_tokens,
            "output_tokens": response_tokens,
        }

    async def analyze_usage_across_responses(
        self,
        responses: List[tuple]
    ) -> Dict[str, Any]:
        """Analyze token usage across multiple responses.

        Args:
            responses: List of (context_chunks, response_text) tuples

        Returns:
            Aggregated token usage statistics
        """
        usages = [
            await self.analyze_response(resp, context)
            for context, resp in responses
        ]

        return {
            "total_responses": len(usages),
            "avg_input_tokens": sum(u["total_input_tokens"] for u in usages) / len(usages) if usages else 0,
            "max_input_tokens": max(u["total_input_tokens"] for u in usages) if usages else 0,
            "avg_context_utilization": (
                sum(u["response_tokens"] for u in usages) /
                sum(u["context_tokens"] for u in usages) * 100
            ) if any(u["context_tokens"] > 0 for u in usages) else 0,
            "responses_over_budget": [
                {"tokens": u["total_input_tokens"], "response": u["response_text"]}
                for u in usages
                if u["total_input_tokens"] > 3500  # Example budget
            ],
        }
```

## 5. Document Ingestor Script

### Usage

```bash
# Ingest markdown files
python tools/ingest_documents.py --path ./docs/markdown --recursive

# Ingest PDF documents
python tools/ingest_documents.py --path ./docs/pdf --format pdf

# Dry run (validate paths without processing)
python tools/ingest_documents.py --dry-run

# Specify chunking parameters
python tools/ingest_documents.py --chunk-size 512 --overlap 128
```

### Implementation Example

```python
"""
ingest_documents.py - Batch document ingestion utility
"""
import os
from pathlib import Path
from typing import List, Dict, Any


class DocumentIngestor:
    """Handles batch ingestion of documents into RAG system."""

    def __init__(self, vector_db_client, embedding_model):
        self.vector_db = vector_db_client
        self.embedding = embedding_model

    async _ingest_files(
        self,
        directory_path: str,
        recursive: bool = True,
        chunk_size: int = 512,
        overlap: int = 128
    ) -> Dict[str, Any]:
        """Ingest all documents in a directory.

        Args:
            directory_path: Path to directory with documents
            recursive: Whether to recurse into subdirectories
            chunk_size: Tokens per chunk (default 512)
            overlap: Token overlap between chunks (default 128)

        Returns:
            Ingestion statistics
        """
        stats = {
            "processed": 0,
            "chunks_created": 0,
            "errors": []
        }

        # Find all markdown files
        if recursive:
            patterns = ["**/*.md", "**/*.txt"]
        else:
            patterns = ["*.md", "*.txt"]

        files = list(Path(directory_path).glob("".join(patterns)))

        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")

                # Chunk the content
                chunks = self._split_into_chunks(
                    content, chunk_size=chunk_size, overlap=overlap
                )

                for i, chunk in enumerate(chunks):
                    embedding = await self.embedding(chunk["text"])

                    vector_id = f"{file_path.stem}_chunk_{i}"

                    await self.vector_db.upsert(
                        id=vector_id,
                        embedding=embedding,
                        metadata={
                            "source": str(file_path),
                            "chunk_index": i,
                            **chunk.get("metadata", {})
                        }
                    )

                    stats["chunks_created"] += 1
                    stats["processed"] += 1

            except Exception as e:
                stats["errors"].append({
                    "file": str(file_path),
                    "error": str(e)
                })

        return stats

    def _split_into_chunks(
        self,
        content: str,
        chunk_size: int = 512,
        overlap: int = 128
    ) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks."""
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len,
            separators=["\\n\\n", "\\n", ".", ",", ""]
        )

        chunks = text_splitter.split_text(content)

        return [
            {
                "text": chunk,
                "metadata": {"source": str(self.source_path)}
            } for chunk in chunks
        ]


async def dry_run_check(paths: List[str]) -> Dict[str, Any]:
    """Check what would be ingested without processing."""
    results = {
        "files_to_process": [],
        "estimated_chunks": 0
    }

    for path in paths:
        p = Path(path)

        if not p.exists():
            continue

        files = list(p.glob("*.md")) if p.is_dir() else [p]

        results["files_to_process"].extend([str(f) for f in files])

    return results
```

## 6. Access Control Auditor

### Usage

```bash
# Audit current ACL permissions
python tools/audit_acl.py

# Export ACL to CSV
python tools/audit_acl.py --export csv --output acl-permissions.csv

# Find orphaned documents (not accessed by anyone)
python tools/audit_acl.py --find-orphaned
```

### Implementation Example

```python
"""
audit_acl.py - Access control auditing utility
"""
import redis
from typing import Dict, Any, Set


class ACLAuditor:
    """Audits access control permissions for RAG documents."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def audit_all_permissions(self) -> Dict[str, Any]:
        """Audit all document permissions.

        Returns:
            Permission audit report
        """
        # Get all documents with permission info
        doc_perms = []

        for key in self.redis.keys("permission:*"):
            perm_data = self.redis.get(key)

            if perm_data:
                import json
                perm = json.loads(perm_data.decode())

                doc_perms.append({
                    "doc_id": key.replace("permission:", ""),
                    **perm
                })

        # Find orphaned documents (no ACL, effectively public)
        all_docs = [key for key in self.redis.keys("vector:*")]
        controlled_docs = [d["doc_id"] for d in doc_perms]
        orphaned_docs = set(all_docs) - set(controlled_docs)

        return {
            "total_documents": len(all_docs),
            "controlled_documents": len(controlled_docs),
            "public_documents": len(orphaned_docs),
            "public_document_ids": list(orphaned_docs)[:100],  # Limit output
            "permission_details": doc_perms[:50]  # First 50 for summary
        }

    async def export_acl_to_csv(self, filepath: str):
        """Export ACL permissions to CSV file."""
        import csv

        perms = await self.audit_all_permissions()

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["doc_id", "permission_level", "allowed_groups"])

            for perm in perms.get("permission_details", []):
                writer.writerow([
                    perm["doc_id"],
                    perm.get("permission_level", "public"),
                    ";".join(perm.get("allowed_groups", []))
                ])
```

## Running All Tools Together

### Health Check Script with Multiple Tools

```bash
#!/bin/bash
# run_health_check.sh - Comprehensive health check script

set -e

echo "=== RAG System Health Check ==="
echo ""

# 1. System health check
echo "[1/6] Checking system health..."
python tools/check_health.py --detailed

# 2. Cache statistics
echo ""
echo "[2/6] Cache statistics..."
python tools/report_cache.py

# 3. Token budget analysis
echo ""
echo "[3/6] Token budget analysis..."
python tools/analyze_tokens.py

# 4. Access control audit
echo ""
echo "[4/6] ACL audit..."
python tools/audit_acl.py

# 5. Latency analysis (if latency logs available)
echo ""
echo "[5/6] Latency analysis..."
if [ -f "data/query-latencies.json" ]; then
    python tools/analyze_latency.py
fi

# 6. Component status
echo ""
echo "[6/6] Summary:"
python tools/check_health.py --summary

echo ""
echo "=== Health Check Complete ==="
```

## Best Practices for Tool Usage

| Task                             | Recommended Tool      | Frequency                 |
| -------------------------------- | --------------------- | ------------------------- |
| Deployment health verification   | `check_health.py`     | On deploy + periodic cron |
| Performance regression detection | `analyze_latency.py`  | Daily automated checks    |
| Memory pressure monitoring       | `report_cache.py`     | Every 15 minutes          |
| Security permission review       | `audit_acl.py`        | Weekly                    |
| Token budget optimization        | `analyze_tokens.py`   | After major updates       |
| Batch document ingestion         | `ingest_documents.py` | As needed                 |

## Prettier Formatting Configuration

```json
{
  "parser": "markdown",
  "plugins": ["@prettier/plugin-markdown"],
  "overrides": [
    {
      "files": "*.md",
      "options": {
        "endOfLine": "lf",
        "tabWidth": 2,
        "printWidth": 120
      }
    },
    {
      "files": "*.yaml",
      "options": {
        "endOfLine": "lf",
        "tabWidth": 2,
        "printWidth": 160,
        "singleQuote": true
      }
    },
    {
      "files": "*.py",
      "options": {
        "endOfLine": "lf",
        "tabWidth": 4,
        "printWidth": 120
      }
    }
  ]
}
```

Run Prettier to format all files:

```bash
prettier --write "**/*.{py,yaml,md,json}"
```
