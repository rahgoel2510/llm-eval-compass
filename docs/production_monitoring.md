# Production Monitoring

## Setup
1. Configure your deployed model in `pipelines/production_monitor.py`.
2. Set alert thresholds for faithfulness, latency, and cost.
3. Schedule the monitor to run on a cron job or AWS Lambda.

## How It Works
- Samples a configurable percentage of live traffic (default 5%).
- Scores sampled queries on quality, cost, and latency metrics.
- Alerts via Slack or PagerDuty if any metric breaches its threshold.

## Example
```bash
python pipelines/production_monitor.py --model claude-sonnet-4-6 --sample-rate 0.05
```

See `notebooks/06_production_monitoring.ipynb` for interactive setup.
