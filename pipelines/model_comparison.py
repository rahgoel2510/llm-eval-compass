"""Head-to-head comparison of multiple LLMs."""

import argparse
import json
import os
import time

from rich.console import Console
from rich.table import Table

from pipelines.single_model_eval import run_eval


def compute_weighted_score(dimensions: dict, weights: dict) -> float:
    """Compute a 0-100 weighted score from dimension results."""
    score = 0.0
    for dim, weight in weights.items():
        dim_data = dimensions.get(dim, {})
        # Extract a representative 0-1 value from each dimension
        if dim == "quality":
            acc = dim_data.get("accuracy", {})
            val = acc.get("task_accuracy", 0.0) if isinstance(acc, dict) else 0.0
        elif dim == "performance":
            # Lower latency is better; normalize against 5000ms ceiling
            p95 = dim_data.get("latency_p95_ms", 5000)
            val = max(0, 1 - p95 / 5000)
        elif dim == "cost":
            # Lower cost is better; normalize against $1 per query ceiling
            cpq = dim_data.get("cost_per_query", 1.0)
            val = max(0, 1 - cpq)
        else:
            val = 0.0
        score += val * weight * 100
    return round(score, 1)


def generate_markdown(all_results: list[dict], use_case: str) -> str:
    lines = [
        f"# LLM Evaluation Scorecard",
        f"**Use Case:** {use_case}  ",
        f"**Date:** {time.strftime('%Y-%m-%d')}  ",
        f"**Models:** {len(all_results)}",
        "",
        "| Model | Quality | Performance | Cost | Weighted Score |",
        "|---|---|---|---|---|",
    ]
    for r in all_results:
        d = r["dimensions"]
        acc = d.get("quality", {}).get("accuracy", {}).get("task_accuracy", "N/A")
        p95 = d.get("performance", {}).get("latency_p95_ms", "N/A")
        cpq = d.get("cost", {}).get("cost_per_query", "N/A")
        ws = r.get("weighted_score", "N/A")
        lines.append(f"| {r['model']} | {acc} | {p95} ms | ${cpq} | {ws} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Compare multiple LLMs head-to-head")
    parser.add_argument("--models", required=True, help="Comma-separated model names")
    parser.add_argument("--test-set", required=True, help="Path to JSON test set")
    parser.add_argument("--use-case", required=True, help="Weight profile name")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    model_names = [m.strip() for m in args.models.split(",")]
    all_results = []

    for name in model_names:
        result = run_eval(name, args.test_set, args.use_case)
        result["weighted_score"] = compute_weighted_score(result["dimensions"], result["weights"])
        all_results.append(result)

    all_results.sort(key=lambda r: r["weighted_score"], reverse=True)

    # Print rich table
    console = Console()
    table = Table(title=f"LLM Comparison — {args.use_case}")
    table.add_column("Model", style="bold")
    table.add_column("Quality (Acc)")
    table.add_column("Perf (p95 ms)")
    table.add_column("Cost/Query")
    table.add_column("Weighted Score", style="bold green")

    for r in all_results:
        d = r["dimensions"]
        acc = str(d.get("quality", {}).get("accuracy", {}).get("task_accuracy", "N/A"))
        p95 = str(d.get("performance", {}).get("latency_p95_ms", "N/A"))
        cpq = str(d.get("cost", {}).get("cost_per_query", "N/A"))
        table.add_row(r["model"], acc, p95, f"${cpq}", str(r["weighted_score"]))

    console.print(table)

    # Save outputs
    os.makedirs(args.output, exist_ok=True)

    json_path = os.path.join(args.output, "comparison_results.json")
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=2)

    md_path = os.path.join(args.output, "scorecard.md")
    with open(md_path, "w") as f:
        f.write(generate_markdown(all_results, args.use_case))

    print(f"\nResults: {json_path}")
    print(f"Scorecard: {md_path}")


if __name__ == "__main__":
    main()
