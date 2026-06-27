# LM Studio Configuration Quick Reference

> **Hardware:** ASUS Zenbook Pro 14 Duo OLED (RTX 4060 8GB + i9-13900H + 32GB RAM)  
> **Last Updated:** 2026-05-05

---

## Recommended Configuration

| Setting              | Value                     | Rationale                                   |
| -------------------- | ------------------------- | ------------------------------------------- |
| **Model**            | Qwen 3.6 35B-A3B (Q4_K_M) | Best coding performance, fits in 6.5GB VRAM |
| **Context Length**   | 16384 tokens              | Covers 95% of files, thermal-safe (75-80°C) |
| **Max Tokens**       | 4096                      | Sufficient for complete implementations     |
| **Temperature**      | 0.2                       | Low for deterministic code generation       |
| **GPU Layers**       | -1 (all)                  | Full GPU offload for maximum performance    |
| **CPU Threads**      | 10                        | Leaves 4 threads for OS                     |
| **Batch Size**       | 512                       | Optimal for RTX 4060                        |
| **Concurrent Limit** | 3                         | Conservative thermal limit                  |
| **Fallback Model**   | Kimi K2.6 14B             | For thermal throttling (3.8GB VRAM)         |

---

## Thermal Thresholds

| Temperature | Status      | Action                                     |
| ----------- | ----------- | ------------------------------------------ |
| <70°C       | ✅ Optimal  | Continue normal operation                  |
| 70-75°C     | ✅ Normal   | Monitor; acceptable for sustained use      |
| 75-80°C     | ⚠️ Elevated | Expected for production; monitor trends    |
| 80-85°C     | ⚠️ High     | Reduce context to 12288 or concurrent to 2 |
| 85-87°C     | ❌ Critical | Switch to Kimi K2.6 14B or emergency mode  |
| >87°C       | ❌ Danger   | Stop LM Studio immediately; check cooling  |

---

## Performance Targets

| Metric               | Target   | Acceptable Range |
| -------------------- | -------- | ---------------- |
| Latency (p50)        | 600ms    | 400-800ms        |
| Latency (p95)        | 1200ms   | 800-1500ms       |
| Throughput           | 25 tok/s | 20-30 tok/s      |
| GPU Temp (Sustained) | 78°C     | 75-82°C          |
| VRAM Usage           | 6.5GB    | 6.0-7.0GB        |

---

## Quick Start Commands

```powershell
# 1. Verify GPU
nvidia-smi

# 2. Start LM Studio Server
# Open LM Studio GUI → Local Server → Start Server (port 1234)

# 3. Test Endpoint
curl http://localhost:1234/v1/models

# 4. Monitor Temperature
nvidia-smi -l 1

# 5. Run Thermal Guardian
python core-component-00\retrieval-augmented-generation\tools\thermal_guardian.py
```

---

## Context Length Decision Matrix

| Use Case                    | Context | Coverage | Thermal | Latency |
| --------------------------- | ------- | -------- | ------- | ------- |
| **RAG-augmented coding** ⭐ | 16384   | 95%      | 75-80°C | 600ms   |
| Long document analysis      | 24576   | 99%      | 80-85°C | 1000ms  |
| Interactive chat (no RAG)   | 8192    | 80%      | 70-75°C | 350ms   |
| Batch code generation       | 12288   | 90%      | 75-78°C | 500ms   |
| Emergency low-power mode    | 4096    | 60%      | 65-70°C | 200ms   |

---

## Troubleshooting

| Issue                | Solution                                              |
| -------------------- | ----------------------------------------------------- |
| Out of VRAM          | Switch to Q4_K_M or use Kimi K2.6 14B                 |
| Slow inference (>2s) | Verify GPU acceleration, check temperature            |
| Thermal throttling   | Reduce context to 12288, use laptop stand/cooling pad |
| Context overflow     | Enable compression, limit retrieved chunks to 5       |

---

## Model Download

```
LM Studio → Models Tab → Search: "Qwen/Qwen3.6-35B-A3B-GGUF"
Select: bartowski/Qwen3.6-35B-A3B-GGUF (Q4_K_M)
Size: ~6.5GB
```

---

## Full Documentation

- **Complete Guide:** [lm-studio-optimization-guide.md](./lm-studio-optimization-guide.md)
- **RAG Deployment:** [quick-start-guide.md](./quick-start-guide.md)
- **Model Comparison:** [model-comparison-2026.md](./model-comparison-2026.md)

---

**Maintained by:** Core Component 00 Laboratory  
**Laboratory Director:** Dr. Elias Vance
