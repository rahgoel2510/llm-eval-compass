# Scorecards

Scorecards provide a structured, weighted comparison of LLM candidates across the six evaluation dimensions:

| Dimension | What It Measures |
|---|---|
| Quality | Faithfulness, answer relevancy, hallucination rate, task accuracy |
| Performance | TTFT, throughput, context window degradation |
| Cost | Cost per query, cost at scale, token efficiency |
| Safety | Toxicity, PII leakage, bias, prompt injection resistance |
| Compliance | Data residency, GDPR fit, EU AI Act risk class |
| Operational | API uptime, rate limits, vendor lock-in |

## How to Use

1. Pick a use-case profile from `config/eval_weights.yaml` (e.g., `customer_facing_chat`, `internal_enterprise_tool`).
2. Run an evaluation pipeline to produce a `results` dict.
3. Fill in the scorecard template from `templates/model_selection.md` or `templates/rag_evaluation.md`.
4. Record the decision in `decisions/`.

## Interpreting Scores

- Each dimension is scored 0–100 and multiplied by its weight.
- **Weighted Score** = sum of (dimension score × weight). Higher is better.
- Models below thresholds in `config/thresholds.yaml` are automatically flagged.

## Templates

- `templates/model_selection.md` — General model comparison scorecard.
- `templates/rag_evaluation.md` — RAG-specific scorecard with RAGAS metrics.

## Examples

See `examples/` for filled-in scorecards from real evaluations.
