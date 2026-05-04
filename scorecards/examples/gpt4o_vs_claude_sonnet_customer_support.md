# LLM Evaluation Scorecard — Customer Support Bot

**Use Case Profile:** customer_facing_chat
**Test Set:** 100 domain queries | **Date:** 2026-05-03

| Dimension | Weight | Claude Sonnet | GPT-4o |
|---|---|---|---|
| Quality | 35% | 88 | 85 |
| Performance | 20% | 78 | 74 |
| Cost | 10% | 72 | 64 |
| Safety | 25% | 92 | 90 |
| Compliance | 5% | 85 | 83 |
| Operational | 5% | 88 | 90 |
| **Weighted Score** | | **84.2** | **81.7** |

## Key Metrics

| Metric | Claude Sonnet | GPT-4o |
|---|---|---|
| Task Accuracy | 88.4% | 87.1% |
| Hallucination Rate | 2.1% | 3.4% |
| Faithfulness (RAG) | 0.91 | 0.88 |
| Latency p95 (ms) | 1,840 | 2,100 |
| Cost/1K queries | $0.47 | $0.61 |
| Toxicity Rate | 0.3% | 0.4% |

## Recommendation

**Selected:** Claude Sonnet
**Rationale:** Highest weighted score driven by quality and safety (60% combined weight). At 500K queries/month, cost difference vs GPT-4o is ~$70/month — acceptable given the 2.7% quality gap.
**Fallback:** GPT-4o
**Review Date:** 2026-08-01
