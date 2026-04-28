# RAG System Templates Quick Reference

## Deployment Configuration Templates

This quick reference provides reusable templates for deploying an enterprise RAG system.

---

## 1. Minimal Deployment Template (Development)

### Single-Node Local Development Setup

```yaml
# rag-dev.yaml - Minimal deployment for development
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-local-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rag-system
  template:
    metadata:
      labels:
        app: rag-system
    spec:
      containers:
        - name: embedding-service
          image: sentence-transformers/all-MiniLM-L6-v2:latest
          ports:
            - containerPort: 8001
          env:
            - name: MODEL_NAME
              value: "sentence-transformers/all-MiniLM-L6-v2"
        - name: reranking-service
          image: reranking-base:latest
          ports:
            - containerPort: 8002
        - name: ollama-inference
          image: ollama/ollama:latest
          ports:
            - containerPort: 11434
          volumeMounts:
            - name: ollama-models
              mountPath: /root/.ollama
      volumes:
        - name: ollama-models
          emptyDir: {}

---
# rag-pvc.yaml - Persistent storage for local dev
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ollama-models-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
```

### Docker Compose Minimal Setup

```yaml
# docker-compose-dev.yml - Local development environment
version: "3.8"

services:
  qdrant:
    image: qdrant/qdrant:v1.7.0
    ports:
      - "6333:6333"
    volumes:
      - ./volumes/qdrant:/qdrant/storage

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - ./volumes/redis:/data

  embedding-service:
    build:
      context: .
      dockerfile: Dockerfile.embedding
    ports:
      - "8001:8001"
    environment:
      - MODEL_NAME=all-MiniLM-L6-v2
    depends_on:
      - qdrant

  reranking-service:
    build:
      context: .
      dockerfile: Dockerfile.reranker
    ports:
      - "8002:8002"
    depends_on:
      - qdrant

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./volumes/ollama:/root/.ollama
    command: serve --model=qwen2.5:7b

  rag-orchestrator:
    build:
      context: .
      dockerfile: Dockerfile.orchestrator
    ports:
      - "8000:8000"
    environment:
      - EMBEDDING_SERVICE_URL=http://embedding-service:8001
      - RERANKING_SERVICE_URL=http://reranking-service:8002
      - VECTOR_DB_URL=qdrant://qdrant:6333
      - REDIS_URL=redis://redis:6379
    depends_on:
      - embedding-service
      - reranking-service
      - qdrant
      - redis

  # Web interface for local development
  web-ui:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "3000:3000"
    depends_on:
      - rag-orchestrator
```

---

## 2. Production Deployment Template (Kubernetes)

### Full Production Configuration

```yaml
# rag-production.yaml - Complete production deployment
apiVersion: v1
kind: ConfigMap
metadata:
  name: rag-production-config
data:
  SYSTEM_NAME: "enterprise-rag-knowledge-base"
  EMBEDDING_MODEL: "sentence-transformers/all-MiniLM-L6-v2"
  RERANKING_MODEL: "BAAI/bge-reranker-large"
  LLM_MODEL: "qwen2.5:7b"
  CHUNK_SIZE_TOKENS: "512"
  OVERLAP_TOKENS: "128"

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: qdrant-vector-db
spec:
  serviceName: qdrant-headless
  replicas: 1
  selector:
    matchLabels:
      app: qdrant
  template:
    metadata:
      labels:
        app: qdrant
    spec:
      containers:
        - name: qdrant
          image: qdrant/qdrant:v1.7.0
          ports:
            - containerPort: 6333
              name: grpc
            - containerPort: 6334
              name: http
          env:
            - name: QDRANT_ALLOW_CREATE_DEFAULT_COLLECTION
              value: "true"
          volumeMounts:
            - name: storage
              mountPath: /qdrant/storage
          resources:
            requests:
              memory: "2Gi"
              cpu: "500m"
            limits:
              memory: "8Gi"
              cpu: "2000m"
      volumes:
        - name: storage
          persistentVolumeClaim:
            claimName: qdrant-pvc

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: qdrant-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: standard-io1

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: embedding-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: embedding-service
  template:
    metadata:
      labels:
        app: embedding-service
    spec:
      containers:
        - name: embedding-model
          image: sentence-transformers/all-MiniLM-L6-v2:latest
          ports:
            - containerPort: 8001
          resources:
            requests:
              memory: "4Gi"
              cpu: "2000m"
            limits:
              memory: "8Gi"
              cpu: "4000m"
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: embedding-service
                topologyKey: kubernetes.io/hostname

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reranking-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: reranking-service
  template:
    metadata:
      labels:
        app: reranking-service
    spec:
      containers:
        - name: reranker
          image: reranking-large:latest
          ports:
            - containerPort: 8002
          resources:
            requests:
              memory: "4Gi"
              cpu: "1000m"
            limits:
              memory: "8Gi"
              cpu: "3000m"
          env:
            - name: MODEL_PATH
              value: "/models/bge-reranker-large"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama-inference
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ollama-inference
  template:
    metadata:
      labels:
        app: ollama-inference
    spec:
      containers:
        - name: ollama
          image: ollama/ollama:latest
          ports:
            - containerPort: 11434
          resources:
            requests:
              memory: "8Gi"
              cpu: "2000m"
            limits:
              memory: "16Gi"
              cpu: "8000m"
              nvidia.com/gpu: 1
          volumeMounts:
            - name: model-storage
              mountPath: /root/.ollama
      volumes:
        - name: model-storage
          emptyDir: {}

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-orchestrator
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rag-orchestrator
  template:
    metadata:
      labels:
        app: rag-orchestrator
    spec:
      containers:
        - name: orchestrator
          image: rag-system-orchestrator:v1.0.0
          ports:
            - containerPort: 8000
          env:
            - name: EMBEDDING_SERVICE_URL
              value: "http://embedding-service:8001"
            - name: RERANKING_SERVICE_URL
              value: "http://reranking-service:8002"
            - name: VECTOR_DB_URL
              value: "qdrant://qdrant:6333"
            - name: REDIS_URL
              value: "redis://redis:6379"
          resources:
            requests:
              memory: "4Gi"
              cpu: "2000m"

---
apiVersion: v1
kind: Service
metadata:
  name: rag-api-service
spec:
  type: ClusterIP
  ports:
    - port: 8000
      targetPort: 8000
      protocol: TCP
  selector:
    app: rag-orchestrator

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rag-ingress
spec:
  rules:
    - host: rag.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: rag-api-service
                port:
                  number: 8000
```

---

## 3. Security-Hardened Deployment Template

### ACL and PII Configuration

```yaml
# rag-security-config.yaml - Security-focused deployment

apiVersion: apps/v1
kind: Deployment
metadata:
  name: acl-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: acl-service
  template:
    metadata:
      labels:
        app: acl-service
    spec:
      containers:
        - name: acl-store
          image: redis:alpine
          ports:
            - containerPort: 6379
          command: ["/bin/sh", "-c", "redis-server --save '' --appendonly no"]
          resources:
            requests:
              memory: "1Gi"
              cpu: "500m"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pii-handler-service
spec:
  replicas: 2
  selector:
    matchLabels:
    app: pii-handler-service
  template:
    metadata:
      labels:
        app: pii-handler-service
    spec:
      containers:
        - name: pii-detector
          image: security/pii-detector:v1.0.0
          ports:
            - containerPort: 8003
          env:
            - name: DETECTION_MODE
              value: "mask-with-tag"
            - name: REDACTION_FORMAT
              value: "[[PII:{TYPE}]]"
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: rag-acl-reader
spec:
  rules:
    - apiGroups: [""]
      resources: ["secrets"]
      verbs: ["get", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rag-acl-binding
subjects:
  - kind: ServiceAccount
    name: acl-service
    namespace: rag-production
roleRef:
  kind: Role
  name: rag-acl-reader
  apiGroup: rbac.authorization.k8s.io

---
# Rate limiting configuration
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: rag-rate-limiter
spec:
  hosts:
    - rag.example.com
  route:
    - destination:
        host: rag-api-service
        port:
          number: 8000
      headers:
        request:
          remove: ["X-Original-User-Agent"]
      corsPolicy:
        - allowOrigin: ["https://example.com"]
      timeout: 10s

---
# Audit logging to immutable storage
apiVersion: v1
kind: ConfigMap
metadata:
  name: audit-config
data:
  STORAGE_TYPE: "s3-worm"
  BUCKET_NAME: "rag-audit-logs"
  RETENTION_DAYS: "365"
  ENCRYPTION: "AES256"
```

---

## 4. Evaluation Pipeline Template

### Automated Evaluation Setup

```python
# evaluation_pipeline.py - Automated evaluation framework
"""
RAG System Evaluation Pipeline

Usage:
    python evaluation_pipeline.py --dataset golden_questions.jsonl \
        --output results/evaluation-report.json \
        --metrics retrieval_em faithfulness hallucination_rate
"""
import argparse
import json
from pathlib import Path


def run_evaluation(
    queries_file: str,
    results_dir: str = "evaluation_results",
    batch_size: int = 32
) -> dict:
    """Run full evaluation suite on RAG system."""

    # Load test dataset
    with open(queries_file, 'r') as f:
        queries = [json.loads(line) for line in f]

    print(f"Loaded {len(queries)} queries for evaluation")

    # Configuration
    metrics_to_track = [
        "exact_match_at_k",
        "f1_score_at_k",
        "bertscore",
        "faithfulness",
        "hallucination_rate",
        "context_utilization",
    ]

    results = {
        "queries_evaluated": 0,
        "metrics": {metric: [] for metric in metrics_to_track},
        "slowest_queries": [],
        "errors": [],
    }

    # Process queries (in production, parallelize this)
    for i, query in enumerate(queries):
        try:
            print(f"Processing query {i+1}/{len(queries)}: {query['query'][:50]}...")

            # Retrieve context
            retrieved_docs = retrieve_documents(query["query"])

            # Generate response
            response = generate_response(query["query"], retrieved_docs)

            # Evaluate against ground truth
            evaluation_result = evaluate_single_query(
                query=query,
                retrieved_docs=retrieved_docs,
                generated_response=response
            )

            # Store results
            for metric in metrics_to_track:
                results["metrics"][metric].append(evaluation_result.get(metric))

            results["queries_evaluated"] += 1

        except Exception as e:
            print(f"Error evaluating query {i+1}: {e}")
            results["errors"].append({
                "query_id": query.get("id"),
                "error": str(e),
            })

    # Calculate averages
    avg_metrics = {}
    for metric, values in results["metrics"].items():
        if values:
            avg_metrics[metric] = sum(values) / len(values)
        else:
            avg_metrics[metric] = None

    results["averaged_metrics"] = avg_metrics

    # Save results
    output_path = Path(results_dir) / "evaluation-report.json"
    Path(results_dir).mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nEvaluation complete!")
    print(f"Results saved to: {output_path}")
    print(f"\nAveraged metrics:")
    for metric, value in avg_metrics.items():
        print(f"  {metric}: {value:.4f}" if value else f"  {metric}: N/A")

    return results


def evaluate_single_query(query: dict, retrieved_docs: list, response: str) -> dict:
    """Evaluate a single query-response pair."""

    # Placeholder for actual evaluation logic
    # In production, use libraries like RAGAS, Trulens, or custom implementations

    return {
        "exact_match_at_k": 0.8,
        "f1_score_at_k": 0.75,
        "bertscore": 0.72,
        "faithfulness": 0.85,
        "hallucination_rate": 0.05,
        "context_utilization": 0.65,
    }


# Command-line entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG System Evaluation Pipeline")
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to JSONL file with golden QA dataset"
    )
    parser.add_argument(
        "--results-dir",
        default="evaluation_results",
        help="Output directory for results"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for processing"
    )

    args = parser.parse_args()
    run_evaluation(args.dataset, args.results_dir, args.batch_size)
```

---

## 5. Ingestion Pipeline Template

### Automated Document Ingestion Script

```python
# ingest_documents.py - Batch document ingestion utility
"""
RAG System Document Ingestion Pipeline

Usage:
    python ingest_documents.py --paths ./docs/markdown --recursive \
        --chunk-size 512 --overlap 128 --embedding-model all-MiniLM-L6-v2
"""
import argparse
import asyncio
from pathlib import Path
from typing import List, Dict


async def ingest_documents(
    paths: List[str],
    recursive: bool = True,
    chunk_size: int = 512,
    overlap: int = 128,
    embedding_model: str = "all-MiniLM-L6-v2"
) -> dict:
    """Ingest documents from specified paths."""

    print(f"Ingesting documents from {paths}")

    stats = {
        "total_files": 0,
        "chunks_created": 0,
        "errors": [],
    }

    for path in paths:
        p = Path(path)

        if not p.exists():
            print(f"Path not found: {p}")
            continue

        # Find files
        if recursive:
            patterns = ["**/*.md", "**/*.txt", "**/*.pdf"]
        else:
            patterns = ["*.md", "*.txt", "*.pdf"]

        files = []
        for pattern in patterns:
            files.extend(p.glob(pattern))

        stats["total_files"] += len(files)

        # Process each file
        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")

                # Chunk the content
                chunks = split_into_chunks(content, chunk_size, overlap)

                # Generate embeddings and store in vector DB
                for i, chunk in enumerate(chunks):
                    embedding_vector = generate_embedding(chunk["text"])

                    await store_in_vector_db(
                        id=f"{file_path.stem}_{i}",
                        embedding=embedding_vector,
                        metadata={
                            "source": str(file_path),
                            "chunk_index": i,
                            **chunk.get("metadata", {}),
                        }
                    )

                    stats["chunks_created"] += 1

            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                stats["errors"].append({
                    "file": str(file_path),
                    "error": str(e),
                })

    # Print summary
    print(f"\nIngestion complete!")
    print(f"  Total files processed: {stats['total_files']}")
    print(f"  Chunks created: {stats['chunks_created']}")
    if stats["errors"]:
        print(f"  Errors encountered: {len(stats['errors'])}")

    return stats


async def split_into_chunks(
    content: str,
    chunk_size: int = 512,
    overlap: int = 128
) -> List[Dict[str, any]]:
    """Split text into overlapping chunks."""
    # Implementation using RecursiveCharacterTextSplitter or similar
    return []


async def generate_embedding(text: str) -> List[float]:
    """Generate embedding vector for text."""
    # Implementation using sentence-transformers or similar
    return [0.0] * 384  # Placeholder


async def store_in_vector_db(
    id: str,
    embedding: List[float],
    metadata: Dict[str, any]
) -> None:
    """Store document chunk in vector database."""
    # Implementation using Qdrant client
    pass


# Command-line entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Document Ingestion Pipeline")
    parser.add_argument(
        "--paths",
        nargs="+",
        required=True,
        help="Paths to directories containing documents"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        default=True,
        help="Recurse into subdirectories"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=512,
        help="Number of tokens per chunk (default: 512)"
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=128,
        help="Token overlap between chunks (default: 128)"
    )
    parser.add_argument(
        "--embedding-model",
        default="all-MiniLM-L6-v2",
        help="Name of embedding model to use"
    )

    args = parser.parse_args()
    asyncio.run(ingest_documents(args.paths, args.recursive,
                                   args.chunk_size, args.overlap,
                                   args.embedding_model))
```

---

## Quick Reference Summary Table

| Template File              | Purpose                         | Recommended For         | Location      |
| -------------------------- | ------------------------------- | ----------------------- | ------------- |
| `deployment-template.yaml` | Full production K8s deployment  | Enterprise deployments  | ./templates/  |
| `docker-compose-dev.yml`   | Local development setup         | Development teams       | ./templates/  |
| `security-config.yaml`     | Security-hardened configuration | Compliance requirements | ./security/   |
| `evaluation-pipeline.py`   | Automated evaluation scripts    | ML ops teams            | ./evaluation/ |
| `ingest-documents.py`      | Batch document ingestion        | Data engineering        | ./tools/      |

All templates are formatted with Prettier and follow the project's style guidelines.
