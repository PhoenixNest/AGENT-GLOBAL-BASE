"""
Latency Benchmark — CC-00 Harness Engineering

Instruments per-tier model call latency (p50/p95/p99) using a mock client.
Deterministic (fixed random seed) for CI use.

Usage:
    python latency_benchmark.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import random
import statistics
from dataclasses import dataclass
from implementations.error_boundary import get_timeout_for_model, MODEL_TIER_TIMEOUTS

random.seed(42)

BENCHMARK_TIERS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-8",
}

TIER_LATENCY_PARAMS = {
    "haiku": {"mean": 900, "std": 150},
    "sonnet": {"mean": 1700, "std": 300},
    "opus": {"mean": 3800, "std": 600},
}


@dataclass
class BenchmarkResult:
    tier: str
    model_id: str
    p50_ms: float
    p95_ms: float
    p99_ms: float
    timeout_threshold_ms: float
    sample_count: int


def run_benchmark(tier: str, model_id: str, n: int = 100) -> BenchmarkResult:
    params = TIER_LATENCY_PARAMS[tier]
    samples = [max(50, random.gauss(params["mean"], params["std"])) for _ in range(n)]
    samples.sort()
    p50 = samples[int(n * 0.50)]
    p95 = samples[int(n * 0.95)]
    p99 = samples[min(int(n * 0.99), n - 1)]
    timeout_ms = get_timeout_for_model(model_id) * 1000
    return BenchmarkResult(
        tier=tier,
        model_id=model_id,
        p50_ms=round(p50, 1),
        p95_ms=round(p95, 1),
        p99_ms=round(p99, 1),
        timeout_threshold_ms=timeout_ms,
        sample_count=n,
    )


def main():
    print(
        f"{'Tier':<10} {'Model':<35} {'p50 ms':>8} {'p95 ms':>8} {'p99 ms':>8} {'Timeout':>10} {'N':>5}"
    )
    print("-" * 90)
    for tier, model_id in BENCHMARK_TIERS.items():
        r = run_benchmark(tier, model_id)
        print(
            f"{r.tier:<10} {r.model_id:<35} {r.p50_ms:>8.0f} {r.p95_ms:>8.0f} {r.p99_ms:>8.0f} {r.timeout_threshold_ms:>9.0f}ms {r.sample_count:>5}"
        )


if __name__ == "__main__":
    main()
