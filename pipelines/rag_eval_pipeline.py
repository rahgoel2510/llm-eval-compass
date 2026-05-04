"""RAG-specific evaluation pipeline using RAGAS metrics."""

import argparse
import json
import os
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

RAGAS_METRICS = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]


def load_model_config(model_name: str) -> dict:
    with open(ROOT / "config" / "models.yaml") as f:
        models = yaml.safe_load(f)
    return models.get("models", {}).get(model_name, {})


def load_test_set(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)


def run_metric(metric_name: str, model_cfg: dict, test_cases: list[dict]) -> dict:
    """Dynamically import and run a RAGAS evaluator."""
    try:
        mod = __import__(f"evaluators.quality.{metric_name}", fromlist=[metric_name])
        # Convention: class name is CamelCase of metric, e.g. faithfulness -> FaithfulnessEvaluator
        class_name = metric_name.title().replace("_", "") + "Evaluator"
        evaluator_cls = getattr(mod, class_name)
        return evaluator_cls(model_cfg).evaluate(test_cases)
    except (ImportError, AttributeError) as e:
        return {"score": 0.0, "note": f"evaluator not yet implemented ({e})"}


def main():
    parser = argparse.ArgumentParser(description="RAG evaluation with RAGAS metrics")
    parser.add_argument("--model", required=True, help="Model name from config/models.yaml")
    parser.add_argument("--test-set", required=True, help="Path to JSON test set (query/context/answer triples)")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    model_cfg = load_model_config(args.model)
    if not model_cfg:
        print(f"Error: model '{args.model}' not found in config/models.yaml")
        return

    test_cases = load_test_set(args.test_set)

    results = {
        "model": args.model,
        "test_set": args.test_set,
        "num_cases": len(test_cases),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "metrics": {},
    }

    for metric in RAGAS_METRICS:
        print(f"Running {metric}...")
        results["metrics"][metric] = run_metric(metric, model_cfg, test_cases)

    os.makedirs(args.output, exist_ok=True)
    out_path = os.path.join(args.output, f"{args.model}_rag_eval.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nRAG evaluation results written to {out_path}")
    for metric, data in results["metrics"].items():
        score = data.get("score", "N/A")
        print(f"  {metric}: {score}")


if __name__ == "__main__":
    main()
