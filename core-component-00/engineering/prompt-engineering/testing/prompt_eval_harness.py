"""
Prompt Evaluation Benchmark Set — Cross-Tier Perturbation Suite

Defines a benchmark set of 15 prompts (5 categories x 3 each), each paired with two
semantics-preserving perturbations, for sweeping across three model tiers
(Haiku/Sonnet/Opus). Perturbation pairing follows the BrittleBench methodology
(arXiv:2603.13285).

This file is an UNEXECUTED benchmark-set definition. It intentionally ships no
classification logic and no model client.

A prior version of this file computed a STABLE / TIER_SENSITIVE / BRITTLE verdict via a
`MockModelClient` that returned `hashlib.md5(f"{tier}:{prompt[:50]}:{variant_id}")` in place
of a real model call. That hash is a pure function of prompt text, tier, and variant index —
it carries no model-output signal, so every run produced the same classification regardless
of what any model actually did (verified: executing the prior version classified all 15
prompts BRITTLE on every run, an arithmetic artifact of hashing 3 tiers x 2 variants, not a
finding about any model). That classification path has been removed rather than kept as a
placeholder — see
core-component-00/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/
item I1.

To actually classify prompt stability, wire a real model client and grade its outputs
directly instead of hashing them. A real client only needs to satisfy:

    class ModelClient(Protocol):
        def call(self, tier: str, prompt: str, variant_id: int) -> tuple[str, float]:
            '''Return (model_output_text, latency_ms) from an actual model call.'''

Then compare `model_output_text` across a prompt's variants (e.g. via embedding similarity,
exact match after normalization, or an LLM-judge rubric) to derive a stability verdict. Do
not reintroduce a hash-of-prompt-text substitute for that comparison.

Usage:
    from prompt_eval_harness import MODEL_TIERS, BENCHMARK_PROMPTS, PromptVariant
    # Wire a real client and grade its outputs against a rubric — not shipped here.
"""
from dataclasses import dataclass, field
from typing import List

MODEL_TIERS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-8",
}

@dataclass
class PromptVariant:
    prompt_id: str
    category: str
    base_prompt: str
    perturbations: List[str] = field(default_factory=list)

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
