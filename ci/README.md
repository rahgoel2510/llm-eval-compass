# CI Pipelines

- **eval_on_pr.yml** — Runs regression evals on every pull request. Blocks merge if quality drops >5%.
- **nightly_eval.yml** — Nightly full benchmark run against all models in `config/models.yaml`.
- **production_alert.yml** — Runs every 6 hours, monitors production model metrics and alerts on failure.
