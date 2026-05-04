"""Answer relevancy evaluator using RAGAS."""

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy

from evaluators.base_evaluator import BaseEvaluator


class AnswerRelevancyEvaluator(BaseEvaluator):
    """Measures how relevant the answer is to the question."""

    @property
    def name(self) -> str:
        return "answer_relevancy"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate answer relevancy. Each input needs: question, answer, contexts."""
        dataset = Dataset.from_list([
            {
                "question": item["question"],
                "answer": item["answer"],
                "contexts": item["contexts"],
            }
            for item in inputs
        ])
        result = evaluate(dataset, metrics=[answer_relevancy])
        return {"answer_relevancy": float(result["answer_relevancy"])}
