# LLM Evaluation Scorecard — Bedrock Enterprise Deployment

**Use Case Profile:** regulated_industry
**Test Set:** 100 domain queries | **Date:** 2026-04-28

| Dimension | Weight | Claude on Bedrock | Llama 3 on Bedrock | Titan Text |
|---|---|---|---|---|
| Quality | 25% | 87 | 80 | 68 |
| Performance | 3% | 76 | 82 | 91 |
| Cost | 10% | 65 | 78 | 93 |
| Safety | 25% | 91 | 82 | 76 |
| Compliance | 35% | 92 | 84 | 95 |
| Operational | 2% | 88 | 85 | 92 |
| **Weighted Score** | | **86.3** | **81.5** | **81.0** |

## Key Metrics

| Metric | Claude on Bedrock | Llama 3 on Bedrock | Titan Text |
|---|---|---|---|
| Task Accuracy | 87.6% | 79.8% | 68.4% |
| Hallucination Rate | 2.4% | 6.1% | 14.3% |
| Faithfulness (RAG) | 0.90 | 0.82 | 0.64 |
| Latency p95 (ms) | 1,950 | 1,600 | 890 |
| Cost/1K queries | $0.52 | $0.28 | $0.08 |
| Data Residency | AWS us-east-1 | AWS us-east-1 | AWS us-east-1 |

## Recommendation

**Selected:** Claude on Bedrock
**Rationale:** Highest weighted score in a regulated-industry profile where compliance (35%) and safety (25%) dominate. Claude leads on quality and safety while meeting all compliance requirements via Bedrock's data residency guarantees. Llama 3's hallucination rate (6.1%) exceeds the 5% threshold. Titan eliminated on quality.
**Fallback:** Llama 3 on Bedrock (with guardrails for hallucination mitigation)
**Review Date:** 2026-07-28
