"""HTML comparison report generator."""

from jinja2 import Template

HTML_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{ title }}</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
  h1 { border-bottom: 2px solid #2563eb; padding-bottom: 0.5rem; }
  .meta { color: #666; margin-bottom: 1.5rem; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
  th, td { padding: 0.5rem 0.75rem; text-align: left; border: 1px solid #d1d5db; }
  th { background: #2563eb; color: white; }
  tr:nth-child(even) { background: #f3f4f6; }
  .recommendation { margin-top: 1.5rem; padding: 1rem; background: #ecfdf5; border-left: 4px solid #10b981; }
</style>
</head>
<body>
<h1>{{ title }}</h1>
<p class="meta">Date: {{ date }} | Use Case: {{ use_case }}</p>
<table>
<tr><th>Metric</th>{% for m in models %}<th>{{ m.name }}</th>{% endfor %}</tr>
{% for metric in metrics %}
<tr><td>{{ metric }}</td>{% for m in models %}<td>{{ m.scores.get(metric, 'N/A') }}</td>{% endfor %}</tr>
{% endfor %}
<tr style="font-weight:bold"><td>Weighted Score</td>{% for m in models %}<td>{{ m.scores.get('weighted_score', 'N/A') }}</td>{% endfor %}</tr>
</table>
{% if recommendation %}
<div class="recommendation"><strong>Recommendation:</strong> {{ recommendation }}</div>
{% endif %}
</body>
</html>""")


class HTMLReportGenerator:
    """Generate an HTML comparison report from evaluation results."""

    def generate(self, results: dict, output_path: str) -> str:
        models = results.get("models", [])
        metrics = []
        if models:
            metrics = [k for k in models[0].get("scores", {}) if k != "weighted_score"]

        html = HTML_TEMPLATE.render(
            title=results.get("title", "LLM Evaluation Report"),
            date=results.get("date", ""),
            use_case=results.get("use_case", ""),
            models=models,
            metrics=metrics,
            recommendation=results.get("recommendation", ""),
        )

        with open(output_path, "w") as f:
            f.write(html)

        return output_path
