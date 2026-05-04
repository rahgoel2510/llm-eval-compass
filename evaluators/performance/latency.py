"""Latency evaluator measuring TTFT and percentile latencies."""

import time
from typing import Callable

import numpy as np

from evaluators.base_evaluator import BaseEvaluator


class LatencyEvaluator(BaseEvaluator):
    """Measures TTFT, p50, p95, p99 latency for a model endpoint."""

    @property
    def name(self) -> str:
        return "latency"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate latency. Each input needs: prompt. Config needs: call_fn(prompt) -> iterator."""
        call_fn: Callable = self.config["call_fn"]
        ttfts: list[float] = []
        totals: list[float] = []

        for item in inputs:
            start = time.perf_counter()
            first_token_time = None
            for _token in call_fn(item["prompt"]):
                if first_token_time is None:
                    first_token_time = time.perf_counter() - start
            total = time.perf_counter() - start
            if first_token_time is not None:
                ttfts.append(first_token_time * 1000)
            totals.append(total * 1000)

        return {
            "ttft_ms": float(np.mean(ttfts)) if ttfts else 0.0,
            "latency_p50_ms": float(np.percentile(totals, 50)) if totals else 0.0,
            "latency_p95_ms": float(np.percentile(totals, 95)) if totals else 0.0,
            "latency_p99_ms": float(np.percentile(totals, 99)) if totals else 0.0,
        }
