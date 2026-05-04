---
layout: default
---

# LLM Eval Compass

> A production-grade, reusable framework for evaluating, comparing, and selecting Large Language Models across quality, cost, latency, safety, and domain-specific criteria.

[**View on GitHub**](https://github.com/rahgoel2510/llm-eval-compass){: .btn .btn-primary }
[**Get Started**](#quick-start){: .btn }

---

## Why This Framework?

Most LLM evaluation approaches fail in one of three ways:

1. They run generic benchmarks and assume the highest score wins
2. They evaluate once at selection time and never monitor in production
3. They have no documentation of *why* a model was chosen

**llm-eval-compass** gives you a structured, repeatable process to evaluate models at development time, validate before release, monitor in production, and document every decision.

---

## The Six Evaluation Dimensions

Every model is scored across six configurable dimensions:

| Dimension | Key Metrics | Default Weight |
|---|---|---|
| **Quality** | Faithfulness, Answer Relevancy, Hallucination Rate, Task Accuracy | 30% |
| **Performance** | TTFT, Throughput, Context Window Degradation | 20% |
| **Cost** | Cost/Query, Cost at Scale, Token Efficiency | 20% |
| **Safety** | Toxicity Rate, PII Leakage, Bias Score, Injection Resistance | 15% |
| **Compliance** | Data Residency, GDPR Fit, EU AI Act Risk Class | 10% |
| **Operational** | API Uptime, Rate Limits, Vendor Lock-in Score | 5% |

---

## Supported Models

| Provider | Models |
|---|---|
| Anthropic | Claude Haiku, Sonnet 4.6, Opus 4.6 |
| OpenAI | GPT-4o, GPT-4o-mini, GPT-4.1 |
| Google | Gemini 2.5 Pro, Gemini Flash |
| AWS Bedrock | Titan Text, Claude on Bedrock, Llama 3 on Bedrock |
| Mistral AI | Mistral Large, Mistral Small |
| Meta | Llama 3 8B, 70B (via Bedrock/HuggingFace) |

---

## Quick Start

```bash
git clone https://github.com/rahgoel2510/llm-eval-compass.git
cd llm-eval-compass
pip install -r requirements.txt
cp .env.example .env   # Add your API keys

python pipelines/model_comparison.py \
  --models claude-sonnet-4-6,gpt-4o,mistral-large \
  --test-set benchmarks/custom/tpm_domain/meeting_summarization.json \
  --use-case chat \
  --output reports/examples/
```

---

## Key Features

### Evaluation Pipelines

- **Single Model Eval** — Evaluate one model against your test set
- **Model Comparison** — Head-to-head comparison of N models with weighted scoring
- **RAG Evaluation** — Full RAG pipeline evaluation with RAGAS metrics
- **Regression Testing** — Run before every model version upgrade
- **Production Monitoring** — Continuous quality tracking on live traffic

### Integrations

| Tool | Purpose |
|---|---|
| [RAGAS](https://docs.ragas.io) | RAG-specific evaluation |
| [DeepEval](https://github.com/confident-ai/deepeval) | Unit testing LLM outputs |
| [LangSmith](https://smith.langchain.com) | Tracing + eval for LangChain |
| [MLflow](https://mlflow.org) | Experiment tracking |
| [Weights & Biases](https://wandb.ai) | Dashboard and logging |
| [Promptfoo](https://promptfoo.dev) | CLI prompt testing, CI/CD |
| [AWS Bedrock](https://aws.amazon.com/bedrock) | Bedrock model access |

### Use Case Profiles

Pre-configured weight profiles for common scenarios:

- **Customer-Facing Chat** — Quality + Safety weighted highest
- **Internal Enterprise Tool** — Cost + Compliance weighted highest
- **High-Volume Batch** — Cost + Performance weighted highest
- **Regulated Industry** — Compliance + Safety weighted highest

---

## Example Output

```
═══════════════════════════════════════════════════════════════
LLM EVALUATION SCORECARD — Customer Support Bot
═══════════════════════════════════════════════════════════════

DIMENSION           │ Claude Sonnet │ GPT-4o   │ Mistral Large
────────────────────┼───────────────┼──────────┼──────────────
Task Accuracy       │ 88.4%         │ 87.1%    │ 82.3%
Hallucination Rate  │ 2.1%          │ 3.4%     │ 5.8%
Faithfulness (RAG)  │ 0.91          │ 0.88     │ 0.83
Latency p95 (ms)    │ 1,840         │ 2,100    │ 1,420
Cost/1K queries     │ $0.47         │ $0.61    │ $0.19
────────────────────┼───────────────┼──────────┼──────────────
WEIGHTED SCORE      │ 84.2 ✓        │ 81.7 ✓   │ 74.1
RECOMMENDATION      │ ★ SELECTED    │ Backup   │ Cost-opt alt
═══════════════════════════════════════════════════════════════
```

---

## Project Structure

```
llm-eval-compass/
├── config/          # Model registry, eval weights, thresholds
├── evaluators/      # Quality, performance, cost, safety, compliance
├── pipelines/       # Single eval, comparison, RAG, regression, monitoring
├── integrations/    # RAGAS, Bedrock, DeepEval, LangSmith, MLflow, W&B
├── benchmarks/      # MMLU, HumanEval, GSM8K, custom domain tests
├── scorecards/      # Templates and examples
├── reports/         # HTML, Markdown, PDF report generators
├── decisions/       # ADR-style decision documentation
├── notebooks/       # Jupyter quickstart guides
├── tests/           # Unit and integration tests
└── ci/              # GitHub Actions workflows
```

---

## CI/CD Integration

Add LLM eval gates to your pipeline — block merges if prompt changes or model upgrades cause quality to drop:

```yaml
# .github/workflows/eval_on_pr.yml
- name: Run regression evals
  run: python pipelines/regression_pipeline.py --baseline main
- name: Fail if quality drops > 5%
  run: python ci/scripts/compare_to_baseline.py --threshold 0.05
```

---

## Documentation

- [Getting Started](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/getting_started.md)
- [Adding a New Model](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/adding_a_new_model.md)
- [Writing Test Cases](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/writing_test_cases.md)
- [Scorecard Guide](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/scorecard_guide.md)
- [Production Monitoring](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/production_monitoring.md)
- [Glossary](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/glossary.md)
- [Contributing](https://github.com/rahgoel2510/llm-eval-compass/blob/main/CONTRIBUTING.md)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](https://github.com/rahgoel2510/llm-eval-compass/blob/main/CONTRIBUTING.md) for how to add models, metrics, test sets, and scorecard examples.

---

## License

[MIT License](https://github.com/rahgoel2510/llm-eval-compass/blob/main/LICENSE) — Copyright 2026 Rahul Goel

---

*Built by Rahul Goel — Principal TPM · GenAI/LLMOps*
*Star the repo if it helps your team.*
