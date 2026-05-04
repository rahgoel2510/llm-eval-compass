"""Context precision evaluator using RAGAS."""

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_precision

from evaluators.base_evaluator import BaseEvaluator


class ContextPrecisionEvaluator(BaseEvaluator):
    """Measures precision of retrieved context chunks."""

    @property
    def name(self) -> str:
        return "context_precision"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate context precision. Each input needs: question, answer, contexts, ground_truth."""
        dataset = Dataset.from_list([
            {
                "question": item["question"],
                "answer": item["answer"],
                "contexts": item["contexts"],
                "ground_truth": item["ground_truth"],
            }
            for item in inputs
        ])
        result = evaluate(dataset, metrics=[context_precision])
        return {"context_precision": float(result["context_precision"])}
