"""Evaluate a single model against a test set."""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_config():
    with open(ROOT / "config" / "models.yaml") as f:
        models = yaml.safe_load(f)
    with open(ROOT / "config" / "eval_weights.yaml") as f:
        weights = yaml.safe_load(f)
    return models, weights


def load_test_set(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)


def evaluate_quality(model_cfg: dict, test_cases: list[dict]) -> dict:
    """Run quality evaluators. Returns metric scores."""
    try:
        from evaluators.quality.task_accuracy import TaskAccuracyEvaluator
        evaluator = TaskAccuracyEvaluator(model_cfg)
        accuracy = evaluator.evaluate(test_cases)
    except ImportError:
        accuracy = {"task_accuracy": 0.0, "note": "evaluator not yet implemented"}

    try:
        from evaluators.quality.hallucination import HallucinationEvaluator
        evaluator = HallucinationEvaluator(model_cfg)
        hallucination = evaluator.evaluate(test_cases)
    except ImportError:
        hallucination = {"hallucination_rate": 0.0, "note": "evaluator not yet implemented"}

    return {"accuracy": accuracy, "hallucination": hallucination}


def evaluate_performance(model_cfg: dict, test_cases: list[dict]) -> dict:
    """Run performance evaluators. Returns latency/throughput metrics."""
    try:
        from evaluators.performance.latency import LatencyEvaluator
        evaluator = LatencyEvaluator(model_cfg)
        return evaluator.evaluate(test_cases)
    except ImportError:
        return {"latency_p50_ms": 0, "latency_p95_ms": 0, "ttft_ms": 0, "note": "evaluator not yet implemented"}


def evaluate_cost(model_cfg: dict, test_cases: list[dict]) -> dict:
    """Run cost evaluators. Returns cost metrics."""
    try:
        from evaluators.cost.cost_calculator import CostCalculator
        calc = CostCalculator(model_cfg)
        return calc.evaluate(test_cases)
    except ImportError:
        return {"cost_per_query": 0.0, "cost_per_1k": 0.0, "note": "evaluator not yet implemented"}


def run_eval(model_name: str, test_set_path: str, use_case: str) -> dict:
    models_cfg, weights_cfg = load_config()

    model_cfg = models_cfg.get("models", {}).get(model_name)
    if not model_cfg:
        print(f"Error: model '{model_name}' not found in config/models.yaml", file=sys.stderr)
        sys.exit(1)

    profile = weights_cfg.get("profiles", {}).get(use_case)
    if not profile:
        print(f"Error: use-case '{use_case}' not found in config/eval_weights.yaml", file=sys.stderr)
        sys.exit(1)

    test_cases = load_test_set(test_set_path)

    results = {
        "model": model_name,
        "use_case": use_case,
        "test_set": test_set_path,
        "num_cases": len(test_cases),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "dimensions": {
            "quality": evaluate_quality(model_cfg, test_cases),
            "performance": evaluate_performance(model_cfg, test_cases),
            "cost": evaluate_cost(model_cfg, test_cases),
        },
        "weights": profile,
    }
    return results


def main():
    parser = argparse.ArgumentParser(description="Evaluate a single LLM against a test set")
    parser.add_argument("--model", required=True, help="Model name from config/models.yaml")
    parser.add_argument("--test-set", required=True, help="Path to JSON test set")
    parser.add_argument("--use-case", required=True, help="Weight profile name from eval_weights.yaml")
    parser.add_argument("--output", required=True, help="Output directory for results")
    args = parser.parse_args()

    results = run_eval(args.model, args.test_set, args.use_case)

    os.makedirs(args.output, exist_ok=True)
    out_path = os.path.join(args.output, f"{args.model}_eval.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results written to {out_path}")


if __name__ == "__main__":
    main()
