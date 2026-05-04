# LLM Selection Decision — 2026-04-15

## Context
Upgrading the production chatbot model from GPT-4o-mini to GPT-4o. User satisfaction scores dropped 12% over the past month, with complaints about shallow answers and missed nuance in complex queries. The chatbot handles internal employee HR and IT support (~200K queries/month).

## Requirements
- Task type: Multi-turn conversational Q&A
- Acceptable latency (p95): < 2,500ms
- Budget: < $0.015/query ($3,000/month cap)
- Data residency: US
- Compliance: Internal data only, no external logging

## Candidates Evaluated
1. **GPT-4o** — Direct upgrade path, higher capability
2. **Claude Sonnet 4.6** — Strong reasoning, competitive pricing
3. **GPT-4o-mini (current)** — Baseline for comparison

## Evaluation Results
Scorecard: `reports/examples/2026-04-15_chatbot_upgrade.html`

| Metric | GPT-4o | Claude Sonnet | GPT-4o-mini (current) |
|---|---|---|---|
| Task Accuracy | 87.1% | 88.4% | 74.2% |
| User Satisfaction (test panel) | 4.2/5 | 4.3/5 | 3.4/5 |
| Latency p95 | 2,100ms | 1,840ms | 980ms |
| Cost/1K queries | $0.61 | $0.47 | $0.12 |
| Weighted Score | 81.7 | 83.1 | 68.4 |

## Decision
**Selected: GPT-4o**

Despite Claude Sonnet scoring slightly higher overall, we chose GPT-4o to minimize migration risk. The chatbot's prompt library (47 prompts) was optimized for OpenAI's API format. Switching providers would require prompt re-engineering and integration changes estimated at 2 weeks. GPT-4o delivers a 12.9% accuracy improvement over GPT-4o-mini at an additional $0.49/1K queries (~$98/month increase), well within budget.

## Risks and Mitigations
- **Risk**: 2x latency increase (980ms → 2,100ms) → **Mitigation**: Acceptable for internal tool; streaming enabled to improve perceived speed
- **Risk**: Cost increase from $24/month to $122/month → **Mitigation**: Within $3K cap; monitor monthly
- **Risk**: Quality regression on edge cases → **Mitigation**: Regression pipeline runs nightly against 200-case test set

## Review Date
2026-07-15 (quarterly). Will re-evaluate Claude Sonnet if prompt migration becomes feasible.
