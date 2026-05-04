"""Evaluation engine — runs a model against a test set and scores the results.

Usage:
    from connectors import create_connector
    from engine import EvaluationEngine

    conn = create_connector("gpt-4o", api_key="sk-...")
    engine = EvaluationEngine(conn)
    results = engine.run("benchmarks/custom/tpm_domain/meeting_summarization.json")
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from connectors.base import BaseConnector, ModelResponse
from evaluators.cost.token_counter import TokenCounter
from evaluators.quality.task_accuracy import TaskAccuracyEvaluator
from evaluators.safety.pii_leakage import PIILeakageEvaluator

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config"


@dataclass
class TestCaseResult:
    """Result for a single test case."""

    test_case_id: str
    input: str
    expected: str
    output: str
    latency_ms: float
    input_tokens: int
    output_tokens: int


@dataclass
class EvaluationResult:
    """Full evaluation result for one model against one test set."""

    model_id: str
    provider: str
    test_set: str
    timestamp: str = ""
    test_case_results: list[TestCaseResult] = field(default_factory=list)
    scores: dict = field(default_factory=dict)
    cost: dict = field(default_factory=dict)
    latency: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "model_id": self.model_id,
            "provider": self.provider,
            "test_set": self.test_set,
            "timestamp": self.timestamp,
            "num_test_cases": len(self.test_case_results),
            "num_errors": len(self.errors),
            "scores": self.scores,
            "cost": self.cost,
            "latency": self.latency,
            "errors": self.errors,
        }


def _load_model_pricing(model_key: str) -> dict:
    path = CONFIG / "models.yaml"
    if not path.exists():
        return {}
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    models = data.get("models", {})
    # Try exact key match, then match by model_id field
    if model_key in models:
        return models[model_key]
    for m in models.values():
        if m.get("model_id") == model_key:
            return m
    return {}


class EvaluationEngine:
    """Runs a model connector against a test set and evaluates the outputs."""

    def __init__(self, connector: BaseConnector) -> None:
        self.connector = connector
        self.token_counter = TokenCounter()

    def run(
        self,
        test_set_path: str,
        *,
        progress_callback: callable | None = None,
    ) -> EvaluationResult:
        """Run evaluation end-to-end.

        Args:
            test_set_path: Path to a JSON test set file. Each item needs
                           'input' and 'expected_output' fields.
            progress_callback: Optional fn(current, total, test_case_id) called per test case.

        Returns:
            EvaluationResult with scores, cost, latency, and per-case details.
        """
        test_cases = self._load_test_set(test_set_path)
        result = EvaluationResult(
            model_id=self.connector.model_id,
            provider=self.connector.provider,
            test_set=Path(test_set_path).stem,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
        )

        # Phase 1: Run each test case through the model
        for i, tc in enumerate(test_cases):
            tc_id = tc.get("test_case_id", f"tc-{i}")
            prompt = tc["input"]
            expected = tc.get("expected_output", "")

            if progress_callback:
                progress_callback(i, len(test_cases), tc_id)

            try:
                resp: ModelResponse = self.connector.generate(prompt)
                result.test_case_results.append(TestCaseResult(
                    test_case_id=tc_id,
                    input=prompt,
                    expected=expected,
                    output=resp.text,
                    latency_ms=resp.latency_ms,
                    input_tokens=resp.input_tokens,
                    output_tokens=resp.output_tokens,
                ))
            except Exception as e:
                result.errors.append(f"{tc_id}: {e}")

        if progress_callback:
            progress_callback(len(test_cases), len(test_cases), "done")

        # Phase 2: Score the results
        self._score(result)
        return result

    def _score(self, result: EvaluationResult) -> None:
        """Run evaluators on collected results."""
        cases = result.test_case_results
        if not cases:
            return

        # Task accuracy
        accuracy_inputs = [{"output": c.output, "expected": c.expected} for c in cases if c.expected]
        if accuracy_inputs:
            acc = TaskAccuracyEvaluator(self.connector.model_id)
            result.scores["task_accuracy"] = acc.evaluate(accuracy_inputs)

        # PII leakage
        pii_inputs = [{"output": c.output} for c in cases]
        pii = PIILeakageEvaluator(self.connector.model_id)
        result.scores["pii_leakage"] = pii.evaluate(pii_inputs)

        # Latency stats
        latencies = [c.latency_ms for c in cases]
        latencies.sort()
        n = len(latencies)
        result.latency = {
            "mean_ms": round(sum(latencies) / n, 1),
            "min_ms": round(latencies[0], 1),
            "max_ms": round(latencies[-1], 1),
            "p50_ms": round(latencies[n // 2], 1),
            "p95_ms": round(latencies[int(n * 0.95)], 1) if n >= 2 else round(latencies[-1], 1),
        }

        # Cost
        total_in = sum(c.input_tokens for c in cases)
        total_out = sum(c.output_tokens for c in cases)
        pricing = _load_model_pricing(self.connector.model_id)
        in_price = pricing.get("input_cost_per_1k_tokens", 0)
        out_price = pricing.get("output_cost_per_1k_tokens", 0)
        total_cost = (total_in * in_price + total_out * out_price) / 1000
        result.cost = {
            "total_input_tokens": total_in,
            "total_output_tokens": total_out,
            "total_cost_usd": round(total_cost, 6),
            "avg_cost_per_query_usd": round(total_cost / n, 6),
        }

    @staticmethod
    def _load_test_set(path: str) -> list[dict]:
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        raise ValueError(f"Test set must be a JSON array, got {type(data).__name__}")
