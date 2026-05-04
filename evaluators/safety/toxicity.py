"""Toxicity evaluator using DeepEval."""

from deepeval.metrics import ToxicityMetric
from deepeval.test_case import LLMTestCase

from evaluators.base_evaluator import BaseEvaluator


class ToxicityEvaluator(BaseEvaluator):
    """Detects toxic and harmful content in model outputs."""

    @property
    def name(self) -> str:
        return "toxicity"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate toxicity. Each input needs: input, actual_output."""
        metric = ToxicityMetric(threshold=self.config.get("threshold", 0.5))
        scores: list[float] = []
        for item in inputs:
            test_case = LLMTestCase(input=item["input"], actual_output=item["actual_output"])
            metric.measure(test_case)
            scores.append(metric.score)
        return {"toxicity_rate": sum(scores) / len(scores) if scores else 0.0}
