from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

from .metrics_config import get_metrics

DEFAULT_METRICS = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]


class RAGASEvaluator:
    def __init__(self, metrics: list[str] | None = None):
        self.metrics = get_metrics(metrics or DEFAULT_METRICS)

    def evaluate(self, dataset: list[dict]) -> dict:
        ds = Dataset.from_list(dataset)
        result = evaluate(ds, metrics=self.metrics)
        return result.to_pandas().to_dict()
