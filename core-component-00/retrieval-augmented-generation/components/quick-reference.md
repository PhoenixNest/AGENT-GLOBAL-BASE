# RAG Components Quick Reference

## Essential Component Specifications and Integration Patterns

This reference provides quick access to key component specifications, integration patterns, and implementation examples for building an enterprise RAG system.

---

## Component Selection Matrix

| Requirement         | Recommended Component        | Alternative Options                         | Trade-offs                                            |
| ------------------- | ---------------------------- | ------------------------------------------- | ----------------------------------------------------- |
| **Embedding Model** | `all-MiniLM-L6-v2` (384 dim) | `bge-small-en-v1.5`, `E5-small-v2`          | Smaller = faster, larger = better accuracy            |
| **Vector Database** | Qdrant (local), Weaviate     | Pinecone (cloud), pgvector                  | Local = no vendor lock-in, Cloud = managed ops        |
| **Reranking Model** | `bge-reranker-large`         | `cross-encoder/ms-marco`, Cohere Rerank API | Cross-encoders more accurate, slower than bi-encoders |
| **LLM Inference**   | vLLM + local GPU             | Ollama (simple), TextGenWebUI               | vLLM = best throughput, Simple = easier setup         |
| **Cache Backend**   | Redis                        | Memcached, DynamoDB                         | Redis = rich features, Memcached = simpler            |

---

## Embedding Service Quick Start

### Installation

```bash
pip install sentence-transformers accelerate torch
```

### Basic Usage

```python
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

class EmbeddingService:
    """Simple embedding service for RAG system."""

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = SentenceTransformer(model_name, device="cuda" if torch.cuda.is_available() else "cpu")

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        tokens = self.tokenizer(batch_encode_add_texts=texts, padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**tokens.to(self.model.device))
            embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        return embeddings.tolist()

# Usage example
embedding = EmbeddingService()
vectors = embedding.embed(["What is RAG?", "How does retrieval work?"])
print(f"Generated {len(vectors)} vectors of shape {len(vectors[0])}")  # 512-dim
```

### Performance Characteristics

| Metric           | Value (all-MiniLM-L6-v2)    | Notes                           |
| ---------------- | --------------------------- | ------------------------------- |
| Input limit      | ~8k tokens per batch        | Longer inputs may be truncated  |
| Batch size       | 32 (recommended)            | Adjust based on GPU memory      |
| Latency (p50)    | ~40ms/batch on A10G         | With batching, ~1.3ms/query avg |
| Memory footprint | 450MB (INT8) / 900MB (FP16) | Quantize for production         |

### Deployment Options

```yaml
# Docker deployment example
services:
  embedding-service:
    image: sentence-transformers/all-MiniLM-L6-v2:latest
    ports:
      - "8001:8001"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

## Vector Database Setup (Qdrant Example)

### Docker Compose Quick Start

```yaml
version: "3.8"
services:
  qdrant:
    image: qdrant/qdrant:v1.7.0
    ports:
      - "6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      QDRANT_ALLOW_CREATE_DEFAULT_COLLECTION: "true"

volumes:
  qdrant_storage:
```

### Python Client Setup

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, CollectionStatus

client = QdrantClient("http://localhost:6333")

# Create collection
client.create_collection(
    collection_name="rag-knowledge-base",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# Upsert points (documents)
points = [
    qdrant_client.models.PointStruct(
        id=f"doc_{i}",
        payload={"text": text, "metadata": {"source": "docs.md"}},
        vector=embedding_vector,
    )
    for i, (text, embedding_vector) in enumerate(zip(documents, embeddings))
]

client.upsert(collection_name="rag-knowledge-base", points=points)

# Query with metadata filter
query = client.retrieve(
    collection_name="rag-knowledge-base",
    query_vector=query_embedding,
    limit=5,
    with_payload=True,
    with_vectors=False,
    score_threshold=0.8,  # Optional minimum relevance threshold
)
```

### Weaviate Alternative

```python
import weaviate

client = weaviate.connect_to_local()

# Create class (collection)
client.schema.create_class(
    "RagDocument",
    vectorizer_config=weaviate.config.Vectorizers.TEXT2VEC_CONTEXTIONNER,
    properties=[
        weaviate.config.Property(name="text", data_type=weaviate.config.DataType.TEXT),
        weaviate.config.Property(name="source", data_type=weaviate.config.DataType.TEXT),
        weaviate.config.Property(name="chunk_index", data_type=weaviate.config.DataType.INT),
    ],
)

# Add document
client.data_handler.delete_all("RagDocument")  # Clear for demo
client.data_handler.create(
    "RagDocument",
    {
        "text": "What is RAG?",
        "source": "docs.md",
        "chunk_index": 0,
    },
    vector=[0.1] * 384,  # Placeholder embedding
)
```

---

## Reranking Service Implementation

### Using BGE Reranker

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import CohereRerank, LlamaRerank

class RerankingService:
    """Reranking service for improving retrieval quality."""

    def __init__(self, model_name="BAAI/bge-reranker-large"):
        # Using Cohere API reranker
        self.reranker = CohereRerank(
            top_k=5,  # Number of results to return after reranking
            model="rerank-english-v2.0",
            api_key="${COHERE_API_KEY}"  # Or use local model
        )

    def rerank(self, query: str, docs: list[Dict], top_k: int = 5) -> list[Dict]:
        """Rerank documents for a query."""
        docs_for_reranking = [
            {
                "document": {"text": doc["text"]},
                "score_field": "relevance_score",
            }
            for doc in docs[:20]  # Top 20 candidates
        ]

        reranked_results = self.reranker.get_relevance_scores(
            query=query,
            documents=docs_for_reranking,
        )

        return [doc for _, doc in sorted(reranked_results, key=lambda x: x[0], reverse=True)[:top_k]]

# Alternative: Local reranking with LangChain
from langchain_community.document_compressors import LLMChainCompressor

compressor = LLMChainCompressor()  # Or use a cross-encoder model
```

### Performance Comparison

| Reranker Model             | Latency (p95) | Memory | Quality Improvement |
| -------------------------- | ------------- | ------ | ------------------- |
| `bge-reranker-base`        | ~150ms        | 2.5GB  | +0.25 MRR           |
| `bge-reranker-large`       | ~300ms        | 4GB    | +0.35 MRR           |
| Cohere rerank-english-v2.0 | ~200ms (API)  | N/A    | +0.30 MRR           |

---

## Hybrid Search Implementation

### RAGFuse Hybrid Search Pattern

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import qdrant_client

class HybridSearch:
    """Implements hybrid search combining vector + keyword retrieval."""

    def __init__(self, vector_db_client, embedding_model):
        self.vector_db = vector_db_client
        self.embedding = embedding_model

    def search_hybrid(self, query: str, top_k_vector: int = 10,
                      top_k_keyword: int = 5) -> list[Dict]:
        """Perform hybrid search combining vector and keyword search."""

        # Vector search results
        vector_results = self.vector_db.search_vectors(
            collection="rag-knowledge-base",
            query_vector=self.embedding(query),
            limit=top_k_vector,
            score_threshold=0.3,
        )

        # Keyword (BM25-style) search - using metadata filters
        keyword_results = self._keyword_search(query, top_k=top_k_keyword)

        # Merge results with weighted scoring
        merged = self._merge_results(vector_results, keyword_results)

        return merged[:10]  # Return top 10

    def _keyword_search(self, query: str, top_k: int) -> list[Dict]:
        """Perform BM25-style keyword search using Qdrant text filter."""
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        tokens = query.split()[:3]  # Take first 3 tokens for keyword matching
        keywords_filter = Filter(must=[
            FieldCondition(
                field="text",
                match=MatchValue(text=query)
            )
        ])

        return self.vector_db.search_vectors(
            collection="rag-knowledge-base",
            query_vector=None,  # No vector search for keyword only
            filter=keywords_filter,
            limit=top_k,
        )

    def _merge_results(self, vector_results: list, keyword_results: list) -> list[Dict]:
        """Merge vector and keyword results with configurable weights."""
        LAMBDA_VEC = 0.7
        LAMBDA_KEYWORD = 0.3

        all_ids = set()
        merged = []

        for result in vector_results:
            doc_id = str(result.id)
            if doc_id not in all_ids:
                all_ids.add(doc_id)
                merged.append({
                    **result,
                    "final_score": LAMBDA_VEC * (result.score or 0) + LAMBDA_KEYWORD * self._keyword_score(result.payload.get("text", ""))
                })

        return sorted(merged, key=lambda x: x["final_score"], reverse=True)[:len(vector_results)]

    def _keyword_score(self, text: str) -> float:
        """Simple keyword scoring (replace with BM25 if available)."""
        query_lower = self._normalize(query).lower()
        text_lower = self._normalize(text).lower()

        # Count matching terms
        matches = sum(1 for term in query_lower.split() if term in text_lower)
        return min(matches * 0.5, 1.0)  # Normalize to [0, 1]
```

---

## Prompt Template Engine Examples

### Reasoning Sandwich Pattern (Recommended for Complex Queries)

```python
from jinja2 import Template

class PromptTemplateEngine:
    """Manages dynamic prompt construction for RAG generation."""

    def __init__(self):
        self.templates = {
            "reasoning_sandwich": Template(self._get_reasoning_sandwich_template()),
            "simple_qa": Template(self._get_simple_qa_template()),
            "citations_required": Template(self._get_citations_template()),
        }

    def get_reasoning_sandwich_prompt(
        self,
        query: str,
        context: list[str],
        task_type: str = "answer"
    ) -> dict:
        """Generate reasoning sandwich prompt for complex QA."""

        # System message (task definition)
        system_msg = f"""You are an expert AI assistant. Your task is {task_type}.
Follow these instructions carefully:
1. Analyze the user's question thoroughly
2. Consider all provided context documents
3. Only use information from the context to answer
4. If the answer cannot be found in context, say so clearly
5. Cite relevant sections when making specific claims"""

        # Context assembly (chunk consolidation)
        consolidated_context = self._consolidate_context(context)

        # User message
        user_msg = f"""User Question: {query}

Relevant Context Documents:
---------------------------
{consolidated_context}

---------------------------

Based on the context above, please answer the question. Be helpful and accurate."""

        return {
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ]
        }

    def _consolidate_context(self, chunks: list[str]) -> str:
        """Consolidate multiple context chunks."""
        if not chunks:
            return "No relevant information found."

        # Sort by relevance score (if available) or order
        sorted_chunks = sorted(enumerate(chunks), key=lambda x: len(x[1]), reverse=True)[:5]

        formatted = []
        for idx, chunk in sorted_chunks:
            chunk_text = chunk.replace("\n", " ").strip()
            formatted.append(f"[Context Chunk {idx + 1}]\n{chunk_text}")

        return "\\n\\n".join(formatted)

# Usage
template_engine = PromptTemplateEngine()
prompt_data = template_engine.get_reasoning_sandwich_prompt(
    query="How do I implement error boundaries?",
    context=["Error boundaries wrap components...", "Use class Component with render method..."]
)
```

---

## Evaluation Framework Integration

### Quick Start with RAGAS

```python
from ragas import evaluate
from ragas.metrics import answer_relevance, faithfulness, contextual_precision
from datasets import Dataset
from sentence_transformers import SentenceTransformer

# Setup embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Prepare evaluation dataset
evaluation_data = Dataset.from_dict({
    "question": ["What is RAG?", "How to implement error boundaries?"],
    "contexts": [
        ["RAG stands for Retrieval Augmented Generation..."],
        ["Error boundaries allow components to recover..."]
    ],
    "answers": ["RAG combines retrieval with generative models...", "..."]
})

# Evaluate RAG pipeline
ragas_metrics = [answer_relevance, faithfulness]

results = evaluate(
    evaluation_data,
    metrics=ragas_metrics,
    embedding_model=embedding_model
)

print(f"Answer Relevance: {results['answer_relevance']}")
print(f"Faithfulness: {results['faithfulness']}")
```

### Custom Evaluation Script

```python
"""
evaluate_rag.py - Run evaluation on RAG system
"""
import json
from typing import Dict, List


def run_evaluation_suite() -> Dict[str, float]:
    """Run complete evaluation suite and return metrics."""

    # Load test dataset
    with open("evaluation/golden_questions.jsonl") as f:
        queries = [json.loads(line) for line in f]

    metrics = {
        "retrieval_em": 0.0,
        "retrieval_f1": 0.0,
        "generation_bertscore": 0.0,
        "faithfulness": 0.0,
        "context_utilization": 0.0,
    }

    for query in queries[:100]:  # Process first 100 for demo

        # Step 1: Retrieval
        retrieved_docs = retrieve_documents(query["query"])

        # Calculate EM@K (Exact Match)
        gt_ids = set(d["id"] for d in query.get("relevant_docs", []))
        pred_ids = set(d["id"] for d in retrieved_docs[:5])
        em_score = 1.0 if gt_ids == pred_ids else 0.0
        metrics["retrieval_em"] += em_score

    # Average across queries (simplified)
    num_queries = len(queries)
    return {k: v / num_queries for k, v in metrics.items()}


# Alternative: Using LangSmith for tracing and evaluation
from langsmith import traceable

@traceable(run_type="retrieval")
def evaluate_with_langsmith():
    """Run evaluation with LangSmith observability."""
    pass
```

---

## Integration Patterns Quick Reference

| Pattern                    | Use Case                      | Implementation Example                                             |
| -------------------------- | ----------------------------- | ------------------------------------------------------------------ |
| **Pre-filter ACL**         | Strict permission enforcement | Check permissions before embedding lookup using Redis bitmap       |
| **Post-filter validation** | Flexible permissions          | Validate retrieved docs after vector search, filter by ACL         |
| **Query expansion**        | Open-domain QA                | Generate 3 query variations, retrieve from each, merge top results |
| **Context compression**    | Limited token budget          | Summarize less relevant chunks, keep most relevant intact          |
| **Multi-stage reranking**  | High accuracy requirements    | Vector search → coarse rerank (top 20) → fine rerank (top 5)       |

---

## Common Issues and Solutions

| Issue                        | Symptom                             | Solution                                                                     |
| ---------------------------- | ----------------------------------- | ---------------------------------------------------------------------------- |
| **Low retrieval precision**  | Wrong docs returned, hallucinations | Add reranking step; increase context chunk overlap from 100→200              |
| **High latency**             | Queries take >1s                    | Enable query caching; use smaller embedding model (INT8 quantized)           |
| **Token budget exceeded**    | Context truncated mid-sentence      | Use `RecursiveCharacterTextSplitter` with smarter separators                 |
| **PII leakage in responses** | Sensitive data in citations         | Add PII handler in response formatter layer                                  |
| **Access denied errors**     | Legitimate queries blocked          | Pre-cache common permission checks in Redis; use post-filter hybrid approach |

---

## Best Practices Checklist

- [ ] **Always use reranking** for production retrieval quality
- [ ] **Enable query caching** with 5-15 minute TTL for frequent queries
- [ ] **Set appropriate chunk sizes** (500-800 tokens text, 250-500 code)
- [ ] **Use hybrid search** for open-domain QA tasks
- [ ] **Implement PII handling** at both ingestion and retrieval stages
- [ ] **Set up audit logging** for compliance requirements
- [ ] **Monitor context utilization** (aim for 60-80% of token budget)
- [ ] **Use session management** for multi-turn conversations
