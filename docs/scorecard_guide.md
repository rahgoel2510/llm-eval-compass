# Scorecard Guide

## Reading a Scorecard
- Each model is scored across 6 dimensions: Quality, Performance, Cost, Safety, Compliance, Operational.
- The **Weighted Score** combines all dimensions using weights from `config/eval_weights.yaml`.
- Models below thresholds in `config/thresholds.yaml` are marked with ✗ and eliminated.

## Customizing Weights
Edit `config/eval_weights.yaml` to adjust dimension weights for your use case. Pre-built profiles exist for `customer_facing_chat`, `internal_enterprise_tool`, `high_volume_batch`, and `regulated_industry`.

## Generating Scorecards
```bash
python pipelines/model_comparison.py --models model1,model2 --test-set your_test.json --use-case chat --output reports/
```

See `scorecards/examples/` for real scorecard outputs.
