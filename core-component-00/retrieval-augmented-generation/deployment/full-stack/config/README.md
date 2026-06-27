# Configuration Templates

> **Core Component 00 — RAG Deployment Configuration**  
> **Last Updated:** 2026-05-05

---

## Overview

This directory contains production-ready configuration templates for deploying the RAG system on ASUS Zenbook Pro 14 Duo OLED hardware.

## Available Templates

| File                      | Purpose                              | Format | Usage                                |
| ------------------------- | ------------------------------------ | ------ | ------------------------------------ |
| **lm-studio-config.json** | LM Studio server configuration       | JSON   | Import into LM Studio settings       |
| **rag-config.yaml**       | Complete RAG system configuration    | YAML   | Load via Python configuration loader |
| **.env.example**          | Environment variables for deployment | ENV    | Copy to `.env` and customize         |

---

## Quick Start

### 1. LM Studio Configuration

**Option A: Manual Configuration (Recommended)**

1. Open LM Studio
2. Go to **Settings** → **Model**
3. Apply settings from `lm-studio-config.json`:
   - Context Length: `16384`
   - Max Tokens: `4096`
   - Temperature: `0.2`
   - GPU Layers: `-1` (all)
   - CPU Threads: `10`
   - Batch Size: `512`

**Option B: Import Configuration (if supported)**

```powershell
# Copy configuration to LM Studio config directory
Copy-Item lm-studio-config.json $env:APPDATA\LMStudio\config\
```

### 2. RAG System Configuration

```powershell
# Copy to your project root
Copy-Item rag-config.yaml ..\..\rag-config.yaml

# Or reference directly in Python
python -c "import yaml; config = yaml.safe_load(open('config/rag-config.yaml'))"
```

### 3. Environment Variables

```powershell
# Copy template to .env
Copy-Item .env.example ..\..\..\.env

# Edit with your values
notepad ..\..\..\.env
```

---

## Configuration Details

### LM Studio Configuration (`lm-studio-config.json`)

**Key Settings:**

| Setting                  | Value | Rationale                                |
| ------------------------ | ----- | ---------------------------------------- |
| `context_length`         | 16384 | Optimal for thermal management (75-80°C) |
| `max_tokens`             | 4096  | Sufficient for complete implementations  |
| `temperature`            | 0.2   | Low for deterministic code generation    |
| `gpu.layers`             | -1    | Offload all layers to GPU                |
| `cpu.threads`            | 10    | Leaves 4 threads for OS                  |
| `cpu.batch_size`         | 512   | Optimal for RTX 4060                     |
| `thermal.max_concurrent` | 3     | Conservative thermal limit               |

**Thermal Management:**

- `max_concurrent_requests: 3` — Prevents GPU from sustained 100% utilization
- `request_timeout: 180` — 3 minutes per request
- `idle_timeout: 300` — Unload model after 5 minutes idle (optional)

### RAG System Configuration (`rag-config.yaml`)

**Architecture:**

```
User Query → Cache Check → Embedding → Vector DB → Reranking → Context Assembly → LLM → Response
```

**Key Components:**

1. **LLM (LM Studio)**
   - Model: Qwen 3.6 35B-A3B (Q4_K_M)
   - Context: 16384 tokens
   - Temperature: 0.2 (coding-optimized)

2. **Embedding Service**
   - Model: BAAI/bge-small-en-v1.5
   - Device: CUDA (GPU)
   - Dimension: 384

3. **Vector Database (Qdrant)**
   - Collection: `coding_knowledge_base`
   - Index: HNSW (m=16, ef_construct=200)
   - Quantization: Scalar (reduces memory)

4. **Reranking**
   - Model: BAAI/bge-reranker-large
   - Device: CPU (preserves GPU for LLM)
   - Top-K: 5 (from 50 candidates)

5. **Cache (Redis)**
   - TTL: 300s (5 minutes)
   - Max Memory: 2GB
   - Eviction: LRU

**CC-00 Integration:**

- **Context Engineering**: 4-slot assembly (System, Retrieved, History, Tools)
- **Harness Engineering**: Error boundaries, retry logic, timeout protection
- **Security**: PII masking, audit logging

### Environment Variables (`.env.example`)

**Required Variables:**

```bash
# Minimum required for basic operation
LM_STUDIO_BASE_URL=http://localhost:1234/v1
QDRANT_HOST=localhost
REDIS_HOST=localhost
```

**Optional Variables:**

```bash
# Thermal management (recommended)
THERMAL_WARNING_THRESHOLD=80
THERMAL_CRITICAL_THRESHOLD=85

# Performance tuning
MAX_CONCURRENT_REQUESTS=3
REQUEST_TIMEOUT=180

# Security (for production)
ENABLE_PII_MASKING=true
ENABLE_AUDIT_LOGGING=true
```

---

## Customization Guide

### Adjusting Context Length

**For different thermal profiles:**

| Scenario                 | Context Length | GPU Temp | Latency | Coverage |
| ------------------------ | -------------- | -------- | ------- | -------- |
| **Production (default)** | 16384          | 75-80°C  | 600ms   | 95%      |
| Long document analysis   | 24576          | 80-85°C  | 1000ms  | 99%      |
| Interactive development  | 8192           | 70-75°C  | 350ms   | 80%      |
| Emergency low-power      | 4096           | 65-70°C  | 200ms   | 60%      |

**Update in both files:**

1. `lm-studio-config.json`: `model.context_length`
2. `rag-config.yaml`: `llm.context_length`

### Switching Models

**To use Kimi K2.6 14B (fallback model):**

```json
{
  "model": {
    "name": "Kimi-K2.6-14B-Q4_K_M",
    "context_length": 32768,
    "max_tokens": 4096
  }
}
```

**Note:** Kimi supports 128K native context length.

```yaml
# rag-config.yaml
llm:
  model: "Kimi-K2.6-14B-Q4_K_M"
  context_length: 32768
```

### Adjusting Concurrent Requests

**Based on thermal monitoring:**

| GPU Temp Range | Recommended Concurrent Requests |
| -------------- | ------------------------------- |
| <75°C          | 4-5                             |
| 75-80°C        | 3 (default)                     |
| 80-85°C        | 2                               |
| >85°C          | 1 (emergency mode)              |

---

## Validation

### Test LM Studio Configuration

```powershell
# Test endpoint
curl http://localhost:1234/v1/models

# Test inference
curl http://localhost:1234/v1/chat/completions -Method POST -Body '{"model":"local-model","messages":[{"role":"user","content":"Hello"}]}' -ContentType "application/json"
```

### Test RAG Configuration

```python
import yaml

# Load configuration
with open('config/rag-config.yaml') as f:
    config = yaml.safe_load(f)

# Validate structure
assert config['llm']['context_length'] == 16384
assert config['vector_db']['provider'] == 'qdrant'
assert config['cache']['enabled'] == True

print("✅ Configuration valid")
```

### Test Environment Variables

```powershell
# Load .env file
Get-Content ..\..\..\.env

# Verify required variables
$required = @('LM_STUDIO_BASE_URL', 'QDRANT_HOST', 'REDIS_HOST')
foreach ($var in $required) {
    if (-not (Test-Path env:$var)) {
        Write-Host "❌ Missing: $var"
    } else {
        Write-Host "✅ Found: $var"
    }
}
```

---

## Troubleshooting

### Configuration Not Loading

**Issue:** LM Studio doesn't reflect configuration changes

**Solution:**

1. Restart LM Studio completely
2. Verify configuration file location
3. Check for JSON syntax errors: `python -m json.tool lm-studio-config.json`

### YAML Parse Errors

**Issue:** `yaml.scanner.ScannerError`

**Solution:**

1. Validate YAML syntax: `python -c "import yaml; yaml.safe_load(open('rag-config.yaml'))"`
2. Check indentation (use spaces, not tabs)
3. Ensure no special characters in string values

### Environment Variables Not Loading

**Issue:** Variables not accessible in application

**Solution:**

1. Verify `.env` file location (should be in project root)
2. Use `python-dotenv` to load: `from dotenv import load_dotenv; load_dotenv()`
3. Check for typos in variable names

---

## References

| Resource                         | Location                                    |
| -------------------------------- | ------------------------------------------- |
| **LM Studio Optimization Guide** | `../guides/lm-studio-optimization-guide.md` |
| **Quick Start Guide**            | `../guides/quick-start-guide.md`            |
| **Quick Reference**              | `../reference/QUICK-REFERENCE.md`           |

---

**Maintained by:** Core Component 00 Laboratory  
**Laboratory Director:** Dr. Elias Vance
