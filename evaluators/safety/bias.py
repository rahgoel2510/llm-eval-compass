"""Bias evaluator using DeepEval."""

from deepeval.metrics import BiasMetric
from deepeval.test_case import LLMTestCase

from evaluators.base_evaluator import BaseEvaluator


class BiasEvaluator(BaseEvaluator):
    """Detects demographic and topic bias in model outputs."""

    @property
    def name(self) -> str:
        return "bias"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate bias. Each input needs: input, actual_output."""
        metric = BiasMetric(threshold=self.config.get("threshold", 0.5))
        scores: list[float] = []
        for item in inputs:
            test_case = LLMTestCase(input=item["input"], actual_output=item["actual_output"])
            metric.measure(test_case)
            scores.append(metric.score)
        return {"bias_score": sum(scores) / len(scores) if scores else 0.0}
