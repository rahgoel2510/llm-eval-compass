"""Markdown table report generator."""


class MarkdownReportGenerator:
    """Generate a markdown comparison report from evaluation results."""

    def generate(self, results: dict, output_path: str) -> str:
        models = results.get("models", [])
        title = results.get("title", "LLM Evaluation Report")
        lines = [
            f"# {title}",
            "",
            f"**Date:** {results.get('date', '')} | **Use Case:** {results.get('use_case', '')}",
            "",
        ]

        if not models:
            lines.append("No model results available.")
        else:
            metrics = [k for k in models[0].get("scores", {})]
            header = "| Metric | " + " | ".join(m["name"] for m in models) + " |"
            sep = "|---|" + "|".join("---" for _ in models) + "|"
            lines.extend([header, sep])
            for metric in metrics:
                row = f"| {metric} | " + " | ".join(
                    str(m["scores"].get(metric, "N/A")) for m in models
                ) + " |"
                lines.append(row)

        if results.get("recommendation"):
            lines.extend(["", f"**Recommendation:** {results['recommendation']}"])

        content = "\n".join(lines) + "\n"
        with open(output_path, "w") as f:
            f.write(content)

        return output_path
