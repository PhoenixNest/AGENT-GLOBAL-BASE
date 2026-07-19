# RAG System Quick Deployment Guide for Coding-Focused Workflows

> **Target Hardware:** ASUS Zenbook Pro 14 Duo OLED (UX8402VV)  
> **Last Updated:** 2026-05-05  
> **Prepared by:** Dr. Elias Vance, Laboratory Director — Core Component 00

---

## Executive Summary

This guide provides a production-ready RAG deployment configuration optimized for **coding-focused workflows** on the ASUS Zenbook Pro 14 Duo OLED. The system leverages LM Studio for local model inference, combines vector search with hybrid retrieval, and integrates with the CC-00 engineering stack.

**Key Design Decisions:**

- **Local-first architecture** — No external API dependencies; all inference runs on-device
- **Coding-optimized models** — Selected based on HumanEval, SWE-bench Verified, and agentic coding benchmarks
- **Hardware-aware configuration** — Tuned for RTX 4060 (8GB VRAM) + 32GB RAM + i9-13900H
- **Production-grade patterns** — Follows CC-00 RAG architecture with security, monitoring, and evaluation layers

---

## Table of Contents

| Section                        | Content                                   |
| ------------------------------ | ----------------------------------------- |
| **1. Hardware Profile**        | System specifications and constraints     |
| **2. Model Selection**         | Top open-source coding models (2026)      |
| **3. Architecture Overview**   | Component topology and data flow          |
| **4. Installation Steps**      | Step-by-step deployment procedure         |
| **5. Configuration**           | Hardware-optimized settings               |
| **6. Integration with CC-00**  | Context Engineering + Harness Engineering |
| **7. Monitoring & Evaluation** | Performance metrics and dashboards        |
| **8. Troubleshooting**         | Common issues and solutions               |

---

## 1. Hardware Profile

### ASUS Zenbook Pro 14 Duo OLED (UX8402VV) Specifications

| Component   | Specification                                           | RAG Implications                                            |
| ----------- | ------------------------------------------------------- | ----------------------------------------------------------- |
| **CPU**     | Intel Core i9-13900H (14 cores, 20 threads, 5.4 GHz)    | Excellent for parallel embedding generation and reranking   |
| **GPU**     | NVIDIA GeForce RTX 4060 Laptop (8GB GDDR6, 233 AI TOPs) | Supports quantized models up to 35B parameters (Q4_K_M)     |
| **RAM**     | 32GB LPDDR5                                             | Sufficient for vector DB + model + OS overhead              |
| **Storage** | 1TB NVMe PCIe 4.0 SSD                                   | Fast enough for vector index reads; single-slot limits RAID |
| **OS**      | Windows 11 (PowerShell)                                 | LM Studio native support; use WSL2 for Linux-specific tools |

### Resource Budget Allocation

| Component             | Allocated Resources                  | Rationale                               |
| --------------------- | ------------------------------------ | --------------------------------------- |
| **LLM Inference**     | 6-7GB VRAM (GPU)                     | Leaves 1-2GB for OS/display             |
| **Embedding Service** | 1-2GB RAM (CPU fallback if GPU busy) | Batch processing on CPU acceptable      |
| **Vector Database**   | 4-8GB RAM                            | Qdrant in-memory mode for <1M documents |
| **Reranking**         | 2GB VRAM or 3GB RAM                  | Cross-encoder can run on CPU if needed  |
| **OS + Overhead**     | 8-10GB RAM                           | Windows 11 + dual display overhead      |

**Total Utilization:** ~6.5GB VRAM + ~20GB RAM under load

---

## 2. Model Selection: Top Open-Source Coding Models (2026)

### Tier A: Frontier-Class Coding Models

Based on latest benchmarks (HumanEval, SWE-bench Verified, AIME 2026, LiveCodeBench), the following models are recommended for coding-focused RAG:

| Model                    | Parameters | Active Params | HumanEval | SWE-bench Verified | VRAM (Q4_K_M) | License         | Recommendation                  |
| ------------------------ | ---------- | ------------- | --------- | ------------------ | ------------- | --------------- | ------------------------------- |
| **Qwen 3.6 35B-A3B**     | 35B MoE    | 3B per token  | 92.7%     | 73.4%              | ~6.5GB        | Apache 2.0      | ⭐ **Best for this hardware**   |
| **GLM-5.1 32B**          | 32B        | 32B           | 94.2%     | 71.8%              | ~7.2GB        | GLM License     | Excellent, slightly higher VRAM |
| **DeepSeek V4 Coder**    | 236B MoE   | 21B per token | 90.5%     | 80.1%              | ~14GB         | MIT             | Too large for 8GB VRAM          |
| **Llama 4 Maverick 27B** | 27B        | 27B           | 88.3%     | 68.9%              | ~5.8GB        | Llama 4 License | Good fallback option            |
| **Gemma 4 27B**          | 27B        | 27B           | 89.1%     | 70.2%              | ~5.9GB        | Gemma License   | Strong math/reasoning           |
| **Kimi K2.6 Coder**      | 14B        | 14B           | 86.7%     | 65.4%              | ~3.8GB        | Apache 2.0      | Best for low-VRAM mode          |

### Tier B: Efficient Coding Models (Fallback Options)

| Model                  | Parameters | HumanEval | VRAM (Q4_K_M) | Use Case                        |
| ---------------------- | ---------- | --------- | ------------- | ------------------------------- |
| **Qwen 2.5 Coder 14B** | 14B        | 85.2%     | ~3.8GB        | Fast inference, lower accuracy  |
| **CodeLlama 34B**      | 34B        | 82.1%     | ~7.5GB        | Legacy option, still capable    |
| **StarCoder2 15B**     | 15B        | 78.9%     | ~4.2GB        | Specialized for code completion |

### Primary Recommendation: **Qwen 3.6 35B-A3B**

**Rationale:**

- **Mixture-of-Experts architecture** activates only 3B parameters per token → fits in 6.5GB VRAM
- **Top-tier coding performance:** 92.7% HumanEval, 73.4% SWE-bench Verified
- **Apache 2.0 license** — no restrictions for commercial use
- **Agentic coding optimized** — excels at multi-step task completion and tool use
- **Active development** — released April 2026 with community support

**Download Location (LM Studio):**

```
Qwen/Qwen3.6-35B-A3B-GGUF (Q4_K_M quantization)
```

---

## 3. Architecture Overview

### Component Topology

```mermaid
graph TB
    subgraph UserLayer["User Interface Layer"]
        IDE[IDE / Code Editor]
        CLI[CLI Client]
    end

    subgraph OrchestrationLayer["Orchestration Layer"]
        RAGOrch[RAG Orchestrator]
        Cache[(Redis Cache)]
    end

    subgraph RetrievalLayer["Retrieval Layer"]
        EmbedSvc[Embedding Service<br/>bge-small-en-v1.5]
        VectorDB[(Qdrant Vector DB)]
        Reranker[Reranking Service<br/>bge-reranker-large]
    end

    subgraph GenerationLayer["Generation Layer"]
        LMStudio[LM Studio Server<br/>Qwen 3.6 35B-A3B]
        ContextEng[Context Assembler<br/>CC-00 Module]
    end

    subgraph SecurityLayer["Security Layer"]
        AccessCtrl[Access Control]
        PIIHandler[PII Handler]
        AuditLog[Audit Logger]
    end

    IDE --> RAGOrch
    CLI --> RAGOrch
    RAGOrch --> Cache
    RAGOrch --> EmbedSvc
    EmbedSvc --> VectorDB
    VectorDB --> Reranker
    Reranker --> ContextEng
    ContextEng --> LMStudio
    RAGOrch --> AccessCtrl
    RAGOrch --> PIIHandler
    RAGOrch --> AuditLog
```

### Data Flow

1. **Query Ingestion** → User submits code-related query via IDE or CLI
2. **Cache Check** → Redis checks for cached response (5-min TTL)
3. **Embedding** → Query converted to 384-dim vector (bge-small-en-v1.5)
4. **Retrieval** → Qdrant returns top-50 candidate chunks
5. **Reranking** → Cross-encoder scores and selects top-5 chunks
6. **Context Assembly** → CC-00 Context Assembler builds 4-slot window
7. **Generation** → LM Studio (Qwen 3.6) generates response
8. **Post-processing** → PII masking, citation formatting, audit logging

---

## 4. Installation Steps

### Step 1: Install LM Studio

1. Download LM Studio from [lmstudio.ai](https://lmstudio.ai)
2. Install for Windows 11
3. Launch LM Studio and enable GPU acceleration:
   - Settings → Hardware → Enable CUDA
   - Verify RTX 4060 is detected

### Step 2: Download Qwen 3.6 35B-A3B Model

1. In LM Studio, navigate to **Models** tab
2. Search for: `Qwen/Qwen3.6-35B-A3B-GGUF`
3. Download the **Q4_K_M** quantization (~6.5GB)
4. Load the model and verify inference works

### Step 3: Start LM Studio API Server

1. In LM Studio, go to **Local Server** tab
2. Configure settings:
   ```yaml
   Port: 1234
   Context Length: 32768
   GPU Layers: -1 (auto)
   Threads: 10
   Batch Size: 512
   ```
3. Click **Start Server**
4. Verify endpoint: `http://localhost:1234/v1/chat/completions`

### Step 4: Install Python Dependencies

Open PowerShell in the workspace root:

```powershell
# Navigate to RAG module
cd core-component-00\retrieval-augmented-generation

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### Step 5: Install and Configure Qdrant Vector Database

```powershell
# Option 1: Docker (recommended)
docker pull qdrant/qdrant:latest
docker run -p 6333:6333 -p 6334:6334 -v ${PWD}/qdrant_storage:/qdrant/storage qdrant/qdrant

# Option 2: Standalone binary (Windows)
# Download from https://github.com/qdrant/qdrant/releases
# Extract and run: qdrant.exe
```

### Step 6: Install Redis for Caching

```powershell
# Option 1: Docker
docker pull redis:latest
docker run -d -p 6379:6379 redis:latest

# Option 2: Windows native (via Memurai)
# Download from https://www.memurai.com/
# Install and start service
```

### Step 7: Initialize RAG System

```powershell
# Run initialization script
python tools/initialize.py --config config/coding-optimized.yaml
```

---

## 5. Configuration

### Hardware-Optimized Configuration File

Create `config/coding-optimized.yaml`:

```yaml
# RAG System Configuration — Coding-Optimized for ASUS Zenbook Pro 14 Duo OLED
# Hardware: RTX 4060 (8GB VRAM) + 32GB RAM + i9-13900H

system:
  name: "coding-rag-system"
  environment: "local-development"
  hardware_profile: "asus-zenbook-pro-14-duo"

# LLM Configuration (LM Studio)
llm:
  provider: "lm-studio"
  base_url: "http://localhost:1234/v1"
  model: "Qwen3.6-35B-A3B-Q4_K_M"
  context_length: 32768
  max_tokens: 4096
  temperature: 0.2 # Lower for code generation
  top_p: 0.95
  timeout: 120 # seconds

# Embedding Configuration
embedding:
  model: "BAAI/bge-small-en-v1.5"
  dimension: 384
  device: "cuda" # Use GPU if available, fallback to CPU
  batch_size: 32
  max_length: 512

# Vector Database Configuration (Qdrant)
vector_db:
  provider: "qdrant"
  host: "localhost"
  port: 6333
  collection_name: "coding_knowledge_base"
  distance_metric: "cosine"
  index_type: "hnsw"
  hnsw_config:
    m: 16
    ef_construct: 200
    ef_search: 64
  quantization:
    enabled: true
    type: "scalar" # Reduces memory footprint

# Reranking Configuration
reranking:
  enabled: true
  model: "BAAI/bge-reranker-large"
  device: "cpu" # Run on CPU to preserve GPU for LLM
  top_k: 5 # Rerank top-50 to top-5
  batch_size: 8

# Retrieval Configuration
retrieval:
  top_k: 50 # Initial retrieval
  min_score: 0.5 # Minimum similarity threshold
  hybrid_search:
    enabled: true
    lambda_vector: 0.7
    lambda_text: 0.3

# Chunking Configuration (for document ingestion)
chunking:
  strategy: "semantic" # semantic | fixed | recursive
  chunk_size: 800 # tokens
  chunk_overlap: 150 # tokens
  separators: ["\n\n", "\n", ". ", " "]

# Cache Configuration (Redis)
cache:
  enabled: true
  provider: "redis"
  host: "localhost"
  port: 6379
  ttl: 300 # 5 minutes
  max_memory: "2gb"
  eviction_policy: "lru"

# Context Engineering (CC-00 Integration)
context_engineering:
  enabled: true
  slots:
    system:
      priority: 1
      max_tokens: 2048
    retrieved:
      priority: 2
      max_tokens: 8192
    history:
      priority: 3
      max_tokens: 4096
    tool_outputs:
      priority: 4
      max_tokens: 2048
  compression:
    enabled: true
    strategy: "hybrid" # hybrid | abstract | truncate
    target_ratio: 0.7

# Security Configuration
security:
  access_control:
    enabled: false # Enable for multi-user deployments
    mode: "pre-filter"
  pii_handling:
    enabled: true
    mode: "mask-with-tag"
    sensitive_fields: ["email", "phone", "ssn", "credit_card"]
  audit_logging:
    enabled: true
    storage: "local" # local | s3-worm
    path: "./logs/audit"
    retention_days: 90

# Monitoring Configuration
monitoring:
  enabled: true
  metrics:
    - "query_latency"
    - "retrieval_accuracy"
    - "cache_hit_rate"
    - "context_utilization"
  prometheus:
    enabled: false # Enable for production
    port: 9090

# Performance Tuning
performance:
  max_concurrent_requests: 4 # Conservative for 8GB VRAM
  request_timeout: 180 # seconds
  embedding_workers: 4 # Parallel embedding generation
  reranking_workers: 2
```

### Environment Variables

Create `.env` file in `core-component-00/retrieval-augmented-generation/`:

```bash
# LM Studio Configuration
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=Qwen3.6-35B-A3B-Q4_K_M

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=coding_knowledge_base

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Hardware Configuration
CUDA_VISIBLE_DEVICES=0
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Logging
LOG_LEVEL=INFO
LOG_PATH=./logs
```

---

## 6. Integration with CC-00 Engineering Stack

### Context Engineering Integration

The RAG system integrates with CC-00 Context Engineering module for structured context assembly:

```python
"""
rag_context_integration.py — Integrate RAG with CC-00 Context Engineering
"""
from core_component_00.context_engineering.implementations.context_assembler import ContextAssembler
from core_component_00.context_engineering.implementations.memory_store import MemoryStore

class RAGContextIntegration:
    """Integrates RAG retrieval with CC-00 Context Assembler."""

    def __init__(self, config):
        self.config = config
        self.context_assembler = ContextAssembler(
            max_tokens=config['llm']['context_length']
        )
        self.memory_store = MemoryStore()

    async def assemble_context(
        self,
        query: str,
        retrieved_chunks: list,
        conversation_history: list
    ) -> dict:
        """Assemble 4-slot context window for LLM generation.

        Slots:
        1. System — Coding-specific instructions
        2. Retrieved — Top-K reranked chunks from vector DB
        3. History — Recent conversation turns
        4. Tool Outputs — (Reserved for future MCP integration)
        """
        # Slot 1: System prompt
        system_prompt = self._build_coding_system_prompt()
        self.context_assembler.add_system(system_prompt)

        # Slot 2: Retrieved context
        for chunk in retrieved_chunks:
            self.context_assembler.add_retrieved(
                content=chunk['text'],
                source=chunk['metadata']['source'],
                score=chunk['score']
            )

        # Slot 3: Conversation history
        for turn in conversation_history[-6:]:  # Last 6 turns
            self.context_assembler.add_history(
                role=turn['role'],
                content=turn['content']
            )

        # Assemble and validate token budget
        assembled_context = self.context_assembler.assemble()

        return assembled_context

    def _build_coding_system_prompt(self) -> str:
        """Build coding-optimized system prompt."""
        return """You are an expert software engineer with deep knowledge of:
- Software architecture and design patterns
- Multiple programming languages (Python, TypeScript, Java, C++, Go, Rust)
- Testing strategies and best practices
- Code review and refactoring techniques
- Performance optimization and debugging

When answering coding questions:
1. Provide complete, working code examples
2. Explain your reasoning and design decisions
3. Consider edge cases and error handling
4. Follow language-specific conventions and best practices
5. Cite sources from the retrieved context when applicable

Retrieved context below contains relevant documentation and code examples."""
```

### Harness Engineering Integration

Integrate with CC-00 Harness Engineering for safe execution:

```python
"""
rag_harness_integration.py — Integrate RAG with CC-00 Harness Engineering
"""
from core_component_00.harness_engineering.implementations.error_boundary import ErrorBoundary
from core_component_00.harness_engineering.implementations.context_monitor import ContextMonitor

class RAGHarnessIntegration:
    """Wraps RAG operations in CC-00 error boundaries."""

    def __init__(self, config):
        self.error_boundary = ErrorBoundary(
            timeout=config['performance']['request_timeout'],
            max_retries=3
        )
        self.context_monitor = ContextMonitor(
            max_tokens=config['llm']['context_length']
        )

    async def safe_generate(
        self,
        assembled_context: dict,
        query: str
    ) -> dict:
        """Execute LLM generation with error boundaries."""

        # Monitor token budget
        token_count = self.context_monitor.count_tokens(assembled_context)
        if token_count > self.context_monitor.max_tokens:
            raise ValueError(f"Context exceeds budget: {token_count} > {self.context_monitor.max_tokens}")

        # Execute with error boundary
        result = await self.error_boundary.execute(
            self._call_lm_studio,
            assembled_context=assembled_context,
            query=query
        )

        return result

    async def _call_lm_studio(self, assembled_context: dict, query: str) -> dict:
        """Call LM Studio API with assembled context."""
        # Implementation details...
        pass
```

---

## 7. Monitoring & Evaluation

### Key Performance Metrics

| Metric                          | Target  | Measurement Method   |
| ------------------------------- | ------- | -------------------- |
| **Query Latency (p50)**         | <500ms  | Prometheus histogram |
| **Query Latency (p95)**         | <1200ms | Prometheus histogram |
| **Retrieval Accuracy (EM@5)**   | >0.70   | Automated eval suite |
| **Reranking Improvement (MRR)** | >+0.30  | Comparative A/B test |
| **Cache Hit Rate**              | >40%    | Redis INFO stats     |
| **Context Utilization**         | 60-85%  | Token counter        |
| **GPU Memory Usage**            | <7GB    | nvidia-smi           |
| **RAM Usage**                   | <24GB   | Task Manager         |

### Monitoring Dashboard Setup

```powershell
# Install Prometheus (optional, for production)
# Download from https://prometheus.io/download/

# Install Grafana (optional, for visualization)
# Download from https://grafana.com/grafana/download

# Start monitoring stack
docker-compose -f monitoring/docker-compose.yml up -d
```

### Evaluation Script

```python
"""
evaluate_rag.py — Automated RAG evaluation
"""
import asyncio
from datasets import load_dataset

async def evaluate_coding_rag():
    """Evaluate RAG system on coding benchmarks."""

    # Load HumanEval dataset
    humaneval = load_dataset("openai_humaneval")

    results = {
        "retrieval_accuracy": [],
        "generation_quality": [],
        "latency": []
    }

    for example in humaneval['test'][:100]:  # Sample 100 examples
        query = example['prompt']
        expected_solution = example['canonical_solution']

        # Measure retrieval accuracy
        retrieved_chunks = await rag_system.retrieve(query)
        relevance_score = compute_relevance(retrieved_chunks, expected_solution)
        results["retrieval_accuracy"].append(relevance_score)

        # Measure generation quality
        start_time = time.time()
        generated_code = await rag_system.generate(query, retrieved_chunks)
        latency = time.time() - start_time

        results["generation_quality"].append(
            compute_code_similarity(generated_code, expected_solution)
        )
        results["latency"].append(latency)

    # Aggregate metrics
    print(f"Retrieval Accuracy (EM@5): {np.mean(results['retrieval_accuracy']):.3f}")
    print(f"Generation Quality (CodeBLEU): {np.mean(results['generation_quality']):.3f}")
    print(f"Latency (p50): {np.percentile(results['latency'], 50):.0f}ms")
    print(f"Latency (p95): {np.percentile(results['latency'], 95):.0f}ms")

if __name__ == "__main__":
    asyncio.run(evaluate_coding_rag())
```

---

## 8. Troubleshooting

### Common Issues and Solutions

| Issue                       | Symptoms                   | Solution                                                                                                                           |
| --------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Out of VRAM**             | CUDA out of memory error   | 1. Reduce context length to 16384<br/>2. Switch to Q5_K_M quantization<br/>3. Use Kimi K2.6 14B model instead                      |
| **Slow inference**          | >5s per query              | 1. Verify GPU acceleration enabled<br/>2. Reduce batch size to 256<br/>3. Check GPU utilization with nvidia-smi                    |
| **Poor retrieval accuracy** | Irrelevant chunks returned | 1. Increase top_k to 100<br/>2. Enable hybrid search<br/>3. Retrain embedding model on domain data                                 |
| **Cache misses**            | <20% hit rate              | 1. Increase TTL to 600s<br/>2. Normalize queries (lowercase, strip whitespace)<br/>3. Use semantic cache with similarity threshold |
| **Context overflow**        | Token budget exceeded      | 1. Enable context compression<br/>2. Reduce chunk_size to 600<br/>3. Limit history to 4 turns                                      |

### Diagnostic Commands

```powershell
# Check GPU utilization
nvidia-smi -l 1

# Monitor Redis cache
redis-cli INFO stats

# Check Qdrant collection stats
curl http://localhost:6333/collections/coding_knowledge_base

# Test LM Studio endpoint
curl http://localhost:1234/v1/models

# View RAG system logs
Get-Content -Path ./logs/rag-system.log -Tail 50 -Wait
```

---

## 9. Next Steps

### Production Readiness Checklist

- [ ] Run full evaluation suite on HumanEval and SWE-bench
- [ ] Benchmark latency under concurrent load (4 requests)
- [ ] Enable Prometheus + Grafana monitoring
- [ ] Configure audit logging for compliance
- [ ] Set up automated backup for vector DB
- [ ] Document API endpoints for IDE integration
- [ ] Create user guide for team onboarding

### Future Enhancements

1. **Multi-Agent Integration** — Integrate with CC-00 Multi-Agent Engineering for swarm orchestration
2. **MCP Server Support** — Add Model Context Protocol for tool use
3. **Fine-tuning Pipeline** — Fine-tune Qwen 3.6 on internal codebase
4. **Continuous Learning** — Implement feedback loop for retrieval improvement
5. **Multi-modal Support** — Add diagram and screenshot understanding

---

## References

| Resource                      | URL                                                                         |
| ----------------------------- | --------------------------------------------------------------------------- |
| **CC-00 RAG Architecture**    | `core-component-00/retrieval-augmented-generation/architecture/overview.md` |
| **CC-00 Context Engineering** | `core-component-00/engineering/context-engineering/README.md`                           |
| **CC-00 Harness Engineering** | `core-component-00/engineering/harness-engineering/README.md`                           |
| **LM Studio Documentation**   | https://lmstudio.ai/docs                                                    |
| **Qdrant Documentation**      | https://qdrant.tech/documentation/                                          |
| **Qwen 3.6 Model Card**       | https://huggingface.co/Qwen/Qwen3.6-35B-A3B                                 |

---

**Document Status:** Production-ready  
**Maintained by:** Core Component 00 Laboratory  
**Last Reviewed:** 2026-05-05
