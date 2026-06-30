"""
Prompt Evaluation Harness — Cross-Tier Stability Testing

Tests prompt patterns across three model tiers (Haiku/Sonnet/Opus) to identify
stable vs. brittle prompt patterns. Based on BrittleBench methodology (arXiv:2603.13285).

Usage:
    python prompt_eval_harness.py
"""
import hashlib
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

MODEL_TIERS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-8",
}

class StabilityClass(Enum):
    STABLE = "stable"
    TIER_SENSITIVE = "tier_sensitive"
    BRITTLE = "brittle"

@dataclass
class PromptVariant:
    prompt_id: str
    category: str
    base_prompt: str
    perturbations: List[str] = field(default_factory=list)

@dataclass
class EvalResult:
    prompt_id: str
    tier: str
    variant_id: int
    output_hash: str
    latency_ms: float
    stability_class: StabilityClass = StabilityClass.TIER_SENSITIVE

BENCHMARK_PROMPTS = [
    # schema_constrained (3)
    PromptVariant("SC-01", "schema_constrained",
        'Return JSON: {"name": "...", "age": 0}. Name: Alice, Age: 30.',
        ['Return JSON {"name":"...","age":0}. Name=Alice, Age=30.',
         'Output as JSON with name and age fields. Alice is 30 years old.']),
    PromptVariant("SC-02", "schema_constrained",
        'Output {"status":"ok","code":200} for a successful request.',
        ['Respond with JSON status ok and code 200.',
         'Return {"status":"ok","code":200} always.']),
    PromptVariant("SC-03", "schema_constrained",
        'List 3 items as JSON array: ["item1","item2","item3"].',
        ['Return JSON array with three items.',
         'Give me 3 things as a JSON list.']),
    # chain_of_thought (3)
    PromptVariant("COT-01", "chain_of_thought",
        'Think step by step. What is 17 × 24?',
        ['Solve 17 × 24 step by step.',
         'Calculate 17 times 24, showing your reasoning.']),
    PromptVariant("COT-02", "chain_of_thought",
        'Think step by step. If A > B and B > C, is A > C?',
        ['Step by step: A>B and B>C, does A>C follow?',
         'Using logical reasoning, solve: A>B, B>C implies A>C?']),
    PromptVariant("COT-03", "chain_of_thought",
        'Think through this: A train travels 60 mph for 2 hours. Distance?',
        ['Step by step: speed=60mph, time=2h, what is distance?',
         'Calculate distance: 60 mph for 2 hours, show work.']),
    # zero_shot (3)
    PromptVariant("ZS-01", "zero_shot",
        'What is the capital of France?',
        ['Name the capital city of France.',
         'France capital city?']),
    PromptVariant("ZS-02", "zero_shot",
        'Summarize in one sentence: The sky is blue because of Rayleigh scattering.',
        ['One sentence summary: sky is blue due to Rayleigh scattering.',
         'In a single sentence, explain why the sky appears blue.']),
    PromptVariant("ZS-03", "zero_shot",
        'What programming language is known for its use in data science?',
        ['Name a programming language popular in data science.',
         'Which language dominates data science work?']),
    # few_shot (3)
    PromptVariant("FS-01", "few_shot",
        'Translate to French. English: Hello -> French: Bonjour. English: Cat -> French: ',
        ['English to French: Hello=Bonjour. Cat=?',
         'French translation practice. Hello is Bonjour. Cat is?']),
    PromptVariant("FS-02", "few_shot",
        'Sentiment: "Great product!" -> positive. "Terrible service" -> negative. "It was ok" -> ',
        ['Classify sentiment: Great=positive, Terrible=negative. "It was ok"?',
         'Sentiment analysis examples given. Classify: "It was ok".']),
    PromptVariant("FS-03", "few_shot",
        'Rhymes: cat->hat, dog->log. What rhymes with "sun"?',
        ['cat rhymes with hat, dog with log. sun rhymes with?',
         'Find a rhyme for sun. Examples: cat/hat, dog/log.']),
    # persona (3)
    PromptVariant("PE-01", "persona",
        'You are a helpful assistant. Explain what an API is in simple terms.',
        ['As a helpful assistant, what is an API? Keep it simple.',
         'Explain API simply. You are a friendly helper.']),
    PromptVariant("PE-02", "persona",
        'You are an expert chef. What herb goes best with tomatoes?',
        ['As an expert chef, which herb pairs with tomatoes?',
         'Chef persona: best herb for tomatoes?']),
    PromptVariant("PE-03", "persona",
        'You are a historian. In one sentence, why did Rome fall?',
        ['As a historian: why did Rome fall? One sentence.',
         'Historian perspective: cause of Roman fall, brief.']),
]

class MockModelClient:
    """Deterministic mock client for CI use. Same prompt -> same output hash."""

    def call(self, tier: str, prompt: str, variant_id: int) -> tuple:
        seed = f"{tier}:{prompt[:50]}:{variant_id}"
        h = hashlib.md5(seed.encode()).hexdigest()[:8]
        latency_map = {"haiku": 900.0, "sonnet": 1700.0, "opus": 3800.0}
        return h, latency_map.get(tier, 1700.0)

class PromptEvalHarness:
    def __init__(self, client=None):
        self.client = client or MockModelClient()

    def run_eval(self, pv: PromptVariant, tier: str, variant_id: int = 0) -> EvalResult:
        prompt = pv.base_prompt if variant_id == 0 else (pv.perturbations[variant_id - 1] if pv.perturbations else pv.base_prompt)
        output_hash, latency = self.client.call(tier, prompt, variant_id)
        return EvalResult(prompt_id=pv.prompt_id, tier=tier, variant_id=variant_id,
                          output_hash=output_hash, latency_ms=latency)

    def run_full_benchmark(self) -> List[EvalResult]:
        results = []
        for pv in BENCHMARK_PROMPTS:
            for tier in MODEL_TIERS:
                for vid in range(min(2, 1 + len(pv.perturbations))):
                    results.append(self.run_eval(pv, tier, vid))
        return results

    def compute_stability_report(self, results: List[EvalResult]) -> dict:
        from collections import defaultdict
        per_prompt = defaultdict(list)
        for r in results:
            per_prompt[r.prompt_id].append(r)
        report = {}
        stable = tier_sensitive = brittle = 0
        for pid, evals in per_prompt.items():
            hashes = set(r.output_hash for r in evals)
            if len(hashes) == 1:
                cls = StabilityClass.STABLE; stable += 1
            elif len(hashes) <= 2:
                cls = StabilityClass.TIER_SENSITIVE; tier_sensitive += 1
            else:
                cls = StabilityClass.BRITTLE; brittle += 1
            report[pid] = {"class": cls.value, "unique_outputs": len(hashes), "eval_count": len(evals)}
        report["_summary"] = {"total": len(per_prompt), "STABLE": stable,
                               "TIER_SENSITIVE": tier_sensitive, "BRITTLE": brittle}
        return report

def main():
    harness = PromptEvalHarness()
    results = harness.run_full_benchmark()
    report = harness.compute_stability_report(results)
    summary = report.pop("_summary")
    print(f"\n{'Prompt ID':<10} {'Category':<20} {'Stability Class':<18} {'Unique Outputs'}")
    print("-" * 65)
    for pid, data in sorted(report.items()):
        pv = next(p for p in BENCHMARK_PROMPTS if p.prompt_id == pid)
        print(f"{pid:<10} {pv.category:<20} {data['class']:<18} {data['unique_outputs']}")
    print(f"\nSummary: {summary['total']} prompts | STABLE={summary['STABLE']} TIER_SENSITIVE={summary['TIER_SENSITIVE']} BRITTLE={summary['BRITTLE']}")
    print(f"Total evals: {len(results)}")

if __name__ == "__main__":
    main()
