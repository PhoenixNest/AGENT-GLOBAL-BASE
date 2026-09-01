"""
CoT Classifier — Constraint-Aware Chain-of-Thought Suppression

Suppresses CoT prompting for high-constraint / structured-output tasks and for prompts
already known to be output-unstable.

Background: arXiv:2505.11423 ("When Thinking Fails: The Pitfalls of Reasoning for
Instruction-Following in LLMs") evaluated 15 models on IFEval (simple, rule-verifiable
constraints) and ComplexBench (complex, compositional constraints) and found that CoT
prompting consistently degrades instruction-following: 13 of 14 models regress on IFEval and
all models regress on ComplexBench when CoT is applied. Llama3-8B-Instruct drops from 75.2%
to 59.0% accuracy — an Original-vs-CoT comparison on the *same* model, not a
base-vs-fine-tuned comparison. The paper's own proposed mitigation is "classifier-selective
reasoning": an external classifier predicts whether CoT will help a given instance, keyed on
the instance's task/constraints — not on the model's fine-tuning status.

An earlier version of this module suppressed CoT based on a `-ft-`-style substring match in
the model ID string. That is not a distinction this paper draws, measures, or supports, and
no independent source was found documenting fine-tuning status as a CoT-routing signal in
practice. That routing key has been removed; suppression now keys on the query's own
task/constraint content (the axis the paper's benchmarks and mitigation actually use) plus
the existing prompt-stability signal. Corrected 2026-08-24 — see
core-component-00/platform/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/
items I2 and I3.
"""
from dataclasses import dataclass
from enum import Enum

class TaskType(Enum):
    STRUCTURED_OUTPUT = "structured_output"
    HIGH_CONSTRAINT = "high_constraint"
    GENERAL = "general"

# Markers indicating the prompt asks for machine-parseable output — the IFEval-style
# "simple, rule-verifiable constraints" case the cited paper measures degradation on.
STRUCTURED_OUTPUT_MARKERS = ("json", "schema", "xml", "yaml", "return only", "format:")

# Markers indicating compositional/multi-constraint instruction-following — the
# ComplexBench-style case the cited paper also measures degradation on.
CONSTRAINT_MARKERS = (
    "must ", "must not", "only ", "do not", "don't", "never ", "always ",
    "no more than", "at least", "exactly ", "strictly",
)
HIGH_CONSTRAINT_THRESHOLD = 2

@dataclass
class CoTDecision:
    use_cot: bool
    reason: str
    task_type: TaskType
    stability_class: str

    def __str__(self):
        status = "ENABLED" if self.use_cot else "SUPPRESSED"
        return f"CoT {status}: {self.reason}"

class CoTClassifier:
    COT_INSTRUCTION = "Think through this step by step before answering."

    def count_constraints(self, prompt_text: str) -> int:
        text_lower = prompt_text.lower()
        return sum(text_lower.count(marker) for marker in CONSTRAINT_MARKERS)

    def classify_task(self, prompt_text: str) -> TaskType:
        text_lower = prompt_text.lower()
        if any(marker in text_lower for marker in STRUCTURED_OUTPUT_MARKERS):
            return TaskType.STRUCTURED_OUTPUT
        if self.count_constraints(prompt_text) >= HIGH_CONSTRAINT_THRESHOLD:
            return TaskType.HIGH_CONSTRAINT
        return TaskType.GENERAL

    def should_use_cot(
        self,
        prompt_text: str,
        stability_class: str = "TIER_SENSITIVE",
    ) -> CoTDecision:
        task_type = self.classify_task(prompt_text)
        if task_type in (TaskType.STRUCTURED_OUTPUT, TaskType.HIGH_CONSTRAINT):
            return CoTDecision(
                use_cot=False,
                reason=f"{task_type.value} task: CoT degrades instruction-following (arXiv:2505.11423)",
                task_type=task_type, stability_class=stability_class,
            )
        if stability_class == "BRITTLE":
            return CoTDecision(
                use_cot=False, reason="BRITTLE prompt: CoT injection causes output variance",
                task_type=task_type, stability_class=stability_class,
            )
        return CoTDecision(
            use_cot=True, reason="low-constraint task with stable prompt: CoT enabled",
            task_type=task_type, stability_class=stability_class,
        )

    def inject_cot(self, prompt: str, decision: CoTDecision) -> str:
        if not decision.use_cot:
            return prompt
        return f"{self.COT_INSTRUCTION}\n\n{prompt}"

if __name__ == "__main__":
    clf = CoTClassifier()
    # Same model throughout — every case below varies only in query content, demonstrating
    # that routing no longer depends on any model-identity signal.
    test_cases = [
        ("What is the capital of France?", "TIER_SENSITIVE"),
        ('Return JSON: {"name": "...", "age": 0}. Name: Alice.', "TIER_SENSITIVE"),
        ("You must not use analogies. You must not exceed 50 words. Explain gravity.", "TIER_SENSITIVE"),
        ("Summarize this document in one paragraph.", "BRITTLE"),
        ("Explain quantum entanglement simply.", "STABLE"),
    ]
    print(f"{'Prompt':<60} {'Stability':<14} {'Decision'}")
    print("-" * 110)
    for prompt_text, sc in test_cases:
        d = clf.should_use_cot(prompt_text, stability_class=sc)
        print(f"{prompt_text[:58]:<60} {sc:<14} {d}")
