"""Task accuracy evaluator using exact and fuzzy matching."""

from difflib import SequenceMatcher

from evaluators.base_evaluator import BaseEvaluator


class TaskAccuracyEvaluator(BaseEvaluator):
    """Compares model output to expected output."""

    @property
    def name(self) -> str:
        return "task_accuracy"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate accuracy. Each input needs: output, expected."""
        exact = 0
        fuzzy_scores: list[float] = []
        for item in inputs:
            output = item["output"].strip()
            expected = item["expected"].strip()
            if output == expected:
                exact += 1
            fuzzy_scores.append(SequenceMatcher(None, output, expected).ratio())
        n = len(inputs) or 1
        return {
            "exact_match": exact / n,
            "fuzzy_match": sum(fuzzy_scores) / n,
        }
