"""Context recall evaluator using RAGAS."""

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_recall

from evaluators.base_evaluator import BaseEvaluator


class ContextRecallEvaluator(BaseEvaluator):
    """Measures recall of retrieved context against ground truth."""

    @property
    def name(self) -> str:
        return "context_recall"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate context recall. Each input needs: question, answer, contexts, ground_truth."""
        dataset = Dataset.from_list([
            {
                "question": item["question"],
                "answer": item["answer"],
                "contexts": item["contexts"],
                "ground_truth": item["ground_truth"],
            }
            for item in inputs
        ])
        result = evaluate(dataset, metrics=[context_recall])
        return {"context_recall": float(result["context_recall"])}
