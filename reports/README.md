# Reports

Generated evaluation reports in three formats:

- **HTML** (`generators/html_report.py`) — Styled comparison report viewable in any browser. Uses Jinja2 templating.
- **Markdown** (`generators/markdown_report.py`) — Table-based report suitable for GitHub PRs and documentation.
- **PDF** (`generators/pdf_report.py`) — Generates markdown first; PDF conversion requires `weasyprint` as an optional dependency.

## Usage

```python
from reports.generators.html_report import HTMLReportGenerator

generator = HTMLReportGenerator()
generator.generate(results=eval_results, output_path="reports/examples/report.html")
```

All generators accept a `results` dict with keys: `title`, `date`, `use_case`, and `models` (list of dicts with `name` and metric scores).

## Output

Generated reports are saved to `reports/examples/`.
