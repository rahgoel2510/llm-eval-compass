"""Abstract base class for all evaluators."""

from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    """Base class all evaluators inherit from."""

    def __init__(self, model_id: str, config: dict | None = None) -> None:
        self.model_id = model_id
        self.config = config or {}

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the evaluator name."""

    @abstractmethod
    def evaluate(self, inputs: list[dict]) -> dict:
        """Run evaluation and return {metric_name: score}."""

    def passes_threshold(self, results: dict, thresholds: dict) -> dict[str, bool]:
        """Check each metric against its threshold."""
        return {
            metric: score >= thresholds[metric]
            for metric, score in results.items()
            if metric in thresholds
        }
