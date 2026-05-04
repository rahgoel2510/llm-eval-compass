# LLM Selection Decision — 2026-05-01

## Context
Selecting a model for our RAG-based customer support system. The system retrieves knowledge base articles and generates answers for ~500K queries/month. Must handle multi-turn conversations and cite sources accurately.

## Requirements
- Task type: RAG Q&A with citation
- Acceptable latency (p95): < 3,000ms
- Budget: < $0.01/query ($5,000/month cap)
- Data residency: US or EU
- Compliance: SOC 2, no PII in logs

## Candidates Evaluated
1. **Claude Sonnet 4.6** — Strong faithfulness scores, competitive pricing
2. **GPT-4o** — High accuracy, widely adopted, slightly higher cost
3. **Mistral Large** — Cost-effective, good multilingual support
4. **Titan Text** — Lowest cost, native Bedrock integration

## Evaluation Results
Scorecard: `reports/examples/2026-05-01_rag_customer_support.html`

| Metric | Claude Sonnet | GPT-4o | Mistral Large | Titan Text |
|---|---|---|---|---|
| Faithfulness | 0.91 | 0.88 | 0.83 | 0.64 |
| Hallucination Rate | 2.1% | 3.4% | 5.8% | 14.3% |
| Latency p95 | 1,840ms | 2,100ms | 1,420ms | 890ms |
| Cost/1K queries | $0.47 | $0.61 | $0.19 | $0.08 |
| Weighted Score | 84.2 | 81.7 | 74.1 | 52.3 |

## Decision
**Selected: Claude Sonnet 4.6**

Claude Sonnet scored highest on faithfulness (0.91) and lowest on hallucination rate (2.1%), which are the most critical metrics for customer-facing RAG. The cost difference vs GPT-4o is ~$70/month at our volume — acceptable given the 2.7% quality advantage. Titan Text was eliminated due to hallucination rate (14.3%) exceeding our 5% threshold. Mistral Large was viable on cost but fell short on faithfulness.

## Risks and Mitigations
- **Risk**: Anthropic API outage → **Mitigation**: GPT-4o configured as automatic fallback
- **Risk**: Pricing increase → **Mitigation**: Mistral Large validated as cost-optimized alternative
- **Risk**: Context window limits on long conversations → **Mitigation**: Conversation summarization at 80K tokens

## Review Date
2026-08-01 (quarterly) or sooner if Anthropic releases a new Sonnet version.
