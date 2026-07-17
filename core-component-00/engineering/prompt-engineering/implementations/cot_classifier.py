"""
CoT Classifier — Classifier-Selective Chain-of-Thought Suppression

Suppresses CoT prompting for fine-tuned model variants and BRITTLE prompts.

Background: arXiv:2505.11423 found 13/14 fine-tuned models degraded on CoT tasks.
Llama3-8B-Instruct: 75.2% -> 59.0% accuracy post fine-tuning (attention diversion).
"""
from dataclasses import dataclass
from enum import Enum

class ModelVariant(Enum):
    BASE = "base"
    FINE_TUNED = "fine_tuned"

FINE_TUNING_MARKERS = ("-ft-", ":ft:", "finetuned", "fine-tuned", "-rl-", "-sft-")

@dataclass
class CoTDecision:
    use_cot: bool
    reason: str
    model_variant: ModelVariant
    stability_class: str

    def __str__(self):
        status = "ENABLED" if self.use_cot else "SUPPRESSED"
        return f"CoT {status}: {self.reason}"

class CoTClassifier:
    COT_INSTRUCTION = "Think through this step by step before answering."

    def classify_model(self, model_id: str) -> ModelVariant:
        model_lower = model_id.lower()
        if any(m in model_lower for m in FINE_TUNING_MARKERS):
            return ModelVariant.FINE_TUNED
        return ModelVariant.BASE

    def should_use_cot(
        self,
        model_id: str,
        stability_class: str = "TIER_SENSITIVE",
        prompt_type: str = "general",
    ) -> CoTDecision:
        variant = self.classify_model(model_id)
        if variant == ModelVariant.FINE_TUNED:
            return CoTDecision(use_cot=False, reason="fine-tuned model: CoT degrades accuracy (arXiv:2505.11423)",
                               model_variant=variant, stability_class=stability_class)
        if stability_class == "BRITTLE":
            return CoTDecision(use_cot=False, reason="BRITTLE prompt: CoT injection causes output variance",
                               model_variant=variant, stability_class=stability_class)
        return CoTDecision(use_cot=True, reason="base model with stable prompt: CoT enabled",
                           model_variant=variant, stability_class=stability_class)

    def inject_cot(self, prompt: str, decision: CoTDecision) -> str:
        if not decision.use_cot:
            return prompt
        return f"{self.COT_INSTRUCTION}\n\n{prompt}"

if __name__ == "__main__":
    clf = CoTClassifier()
    test_cases = [
        ("claude-opus-4-8", "TIER_SENSITIVE"),
        ("claude-opus-4-8-ft-v1", "TIER_SENSITIVE"),
        ("claude-sonnet-4-6", "BRITTLE"),
        ("claude-haiku-4-5-20251001", "STABLE"),
    ]
    print(f"{'Model':<35} {'Stability':<16} {'Decision'}")
    print("-" * 75)
    for model_id, sc in test_cases:
        d = clf.should_use_cot(model_id, stability_class=sc)
        print(f"{model_id:<35} {sc:<16} {d}")
