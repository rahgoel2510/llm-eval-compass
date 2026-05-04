# LLM Evaluation Scorecard — Internal Enterprise Tool

**Use Case Profile:** internal_enterprise_tool
**Test Set:** 75 domain queries | **Date:** 2026-05-01

| Dimension | Weight | Claude Haiku | Titan Text |
|---|---|---|---|
| Quality | 25% | 81 | 68 |
| Performance | 15% | 88 | 92 |
| Cost | 30% | 85 | 94 |
| Safety | 5% | 90 | 78 |
| Compliance | 20% | 87 | 91 |
| Operational | 5% | 86 | 90 |
| **Weighted Score** | | **85.0** | **84.8** |

## Key Metrics

| Metric | Claude Haiku | Titan Text |
|---|---|---|
| Task Accuracy | 81.2% | 71.2% |
| Hallucination Rate | 3.8% | 14.3% |
| Latency p95 (ms) | 620 | 890 |
| Cost/1K queries | $0.12 | $0.08 |
| Toxicity Rate | 0.2% | 1.2% |

## Recommendation

**Selected:** Claude Haiku
**Rationale:** Near-identical weighted scores, but Titan's 14.3% hallucination rate exceeds the 5% threshold. Claude Haiku offers significantly better quality at a marginal cost increase ($0.04/1K queries).
**Fallback:** Titan Text (acceptable for low-risk summarization tasks only)
**Review Date:** 2026-08-01
