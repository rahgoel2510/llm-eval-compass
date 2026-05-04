"""Throughput evaluator measuring tokens per second."""

import time
from typing import Callable

from evaluators.base_evaluator import BaseEvaluator


class ThroughputEvaluator(BaseEvaluator):
    """Measures tokens per second throughput."""

    @property
    def name(self) -> str:
        return "throughput"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate throughput. Each input needs: prompt. Config needs: call_fn(prompt) -> list[str]."""
        call_fn: Callable = self.config["call_fn"]
        total_tokens = 0
        total_time = 0.0

        for item in inputs:
            start = time.perf_counter()
            tokens = list(call_fn(item["prompt"]))
            elapsed = time.perf_counter() - start
            total_tokens += len(tokens)
            total_time += elapsed

        return {
            "tokens_per_second": total_tokens / total_time if total_time > 0 else 0.0,
            "total_tokens": total_tokens,
        }
