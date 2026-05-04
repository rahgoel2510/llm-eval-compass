"""Faithfulness evaluator using RAGAS."""

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness

from evaluators.base_evaluator import BaseEvaluator


class FaithfulnessEvaluator(BaseEvaluator):
    """Measures whether model output is grounded in retrieved context."""

    @property
    def name(self) -> str:
        return "faithfulness"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate faithfulness. Each input needs: question, answer, contexts."""
        dataset = Dataset.from_list([
            {
                "question": item["question"],
                "answer": item["answer"],
                "contexts": item["contexts"],
            }
            for item in inputs
        ])
        result = evaluate(dataset, metrics=[faithfulness])
        return {"faithfulness": float(result["faithfulness"])}
