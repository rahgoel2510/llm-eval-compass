# llm-eval-compass

> A production-grade, reusable framework for evaluating, comparing, and selecting Large Language Models across quality, cost, latency, safety, and domain-specific criteria.

Built for teams who need a structured, repeatable process for LLM evaluation — not just a one-time benchmark comparison.

---

## Why This Repo Exists

Most LLM evaluation approaches fail in one of three ways:

1. They run generic benchmarks (MMLU, HumanEval) and assume the highest score wins
2. They evaluate once at selection time and never monitor in production
3. They have no documentation of *why* a model was chosen — making future decisions harder

`llm-eval-compass` solves all three. It gives you a structured framework to evaluate models at development time, validate before release, monitor in production, and document every decision.

---

## Repo Name

```
llm-eval-compass
```

Suggested GitHub URL: `https://github.com/[your-username]/llm-eval-compass`

---

## Supported Models (out of the box)

| Provider | Models |
|---|---|
| Anthropic | Claude Haiku, Sonnet 4.6, Opus 4.6 |
| OpenAI | GPT-4o, GPT-4o-mini, GPT-4.1 |
| Google | Gemini 2.5 Pro, Gemini Flash |
| AWS Bedrock | Titan Text, Claude on Bedrock, Llama 3 on Bedrock |
| Mistral AI | Mistral Large, Mistral Small, Mistral 7B |
| Meta (via Bedrock/HuggingFace) | Llama 3 8B, 70B |
| Moonshot AI | Kimi K2.5 |
| Open Source (self-hosted) | Any model via Ollama or vLLM |

---

## Folder Structure

```
llm-eval-compass/
│
├── README.md                        ← You are here
├── CONTRIBUTING.md                  ← How to add new models, metrics, or test cases
├── LICENSE
├── .env.example                     ← API key template (never commit real keys)
├── requirements.txt
├── pyproject.toml
│
├── config/
│   ├── models.yaml                  ← Model registry: endpoints, pricing, context windows
│   ├── eval_weights.yaml            ← Scoring weights per use case (RAG, chat, coding, etc.)
│   └── thresholds.yaml              ← Pass/fail thresholds for each metric
│
├── evaluators/
│   ├── __init__.py
│   ├── base_evaluator.py            ← Abstract base class all evaluators inherit from
│   ├── quality/
│   │   ├── faithfulness.py          ← RAGAS faithfulness metric
│   │   ├── answer_relevancy.py      ← RAGAS answer relevancy
│   │   ├── hallucination.py         ← Hallucination detection (DeepEval + LLM-as-Judge)
│   │   ├── context_precision.py     ← RAG context precision
│   │   ├── context_recall.py        ← RAG context recall
│   │   └── task_accuracy.py         ← Domain-specific accuracy scoring
│   ├── performance/
│   │   ├── latency.py               ← TTFT, p50, p95, p99 latency measurement
│   │   ├── throughput.py            ← Tokens per second under load
│   │   └── context_window.py        ← Context degradation tests at different lengths
│   ├── cost/
│   │   ├── token_counter.py         ← Input/output token counting per model
│   │   ├── cost_calculator.py       ← Cost per query, daily cost at scale
│   │   └── cost_projector.py        ← Monthly/annual cost projection at given volume
│   ├── safety/
│   │   ├── toxicity.py              ← Toxicity and harmful content detection
│   │   ├── pii_leakage.py           ← PII detection in outputs
│   │   ├── bias.py                  ← Demographic and topic bias detection
│   │   └── prompt_injection.py      ← Prompt injection resistance testing
│   └── compliance/
│       ├── data_residency.py        ← Maps model to data processing region
│       ├── gdpr_checker.py          ← GDPR Article 25 compliance flags
│       └── ai_act_classifier.py     ← EU AI Act risk category classifier
│
├── benchmarks/
│   ├── README.md                    ← When to use which benchmark and what scores mean
│   ├── mmlu/
│   │   ├── runner.py                ← Run MMLU subset on any model
│   │   └── sample_questions.json    ← 100-question sample set
│   ├── humaneval/
│   │   ├── runner.py                ← Code generation benchmark runner
│   │   └── problems.json
│   ├── gsm8k/
│   │   └── runner.py                ← Math reasoning benchmark
│   ├── custom/
│   │   ├── README.md                ← How to write domain-specific test sets
│   │   ├── tpm_domain/
│   │   │   ├── meeting_summarization.json    ← 50 test cases: meeting → action items
│   │   │   ├── risk_extraction.json          ← 50 test cases: doc → risk flags
│   │   │   └── status_update_generation.json ← 50 test cases: data → exec update
│   │   └── template.json            ← Template for adding new domain test sets
│   └── chatbot_arena/
│       └── scraper.py               ← Pull latest Chatbot Arena ELO scores
│
├── pipelines/
│   ├── README.md
│   ├── single_model_eval.py         ← Evaluate one model against your test set
│   ├── model_comparison.py          ← Head-to-head comparison of N models
│   ├── rag_eval_pipeline.py         ← Full RAG pipeline evaluation with RAGAS
│   ├── ab_test_pipeline.py          ← A/B test two models on live traffic (shadow mode)
│   ├── regression_pipeline.py       ← Run before every model version upgrade
│   └── production_monitor.py        ← Continuous monitoring of deployed model
│
├── scorecards/
│   ├── README.md                    ← How to use and interpret scorecards
│   ├── templates/
│   │   ├── model_selection.xlsx     ← Weighted scorecard template (Excel)
│   │   ├── model_selection.md       ← Markdown version of the scorecard
│   │   └── rag_evaluation.md        ← RAG-specific scorecard
│   └── examples/
│       ├── gpt4o_vs_claude_sonnet_customer_support.md   ← Real example decision
│       ├── titan_vs_claude_haiku_internal_tool.md
│       └── bedrock_model_selection_enterprise.md
│
├── integrations/
│   ├── README.md
│   ├── langsmith/
│   │   ├── tracer.py                ← LangSmith tracing setup
│   │   └── eval_runner.py           ← Run evals through LangSmith datasets
│   ├── ragas/
│   │   ├── rag_evaluator.py         ← RAGAS integration wrapper
│   │   └── metrics_config.py        ← Configure which RAGAS metrics to run
│   ├── mlflow/
│   │   ├── experiment_tracker.py    ← Log eval runs as MLflow experiments
│   │   └── model_registry.py        ← Register evaluated models with scores
│   ├── wandb/
│   │   └── eval_logger.py           ← Log results to W&B for dashboards
│   ├── deepeval/
│   │   └── test_suite.py            ← DeepEval test suite integration
│   ├── promptfoo/
│   │   └── config_generator.py      ← Generate Promptfoo YAML configs
│   └── bedrock/
│       ├── bedrock_client.py        ← AWS Bedrock model caller
│       └── bedrock_eval.py          ← Bedrock-specific evaluation helpers
│
├── reports/
│   ├── README.md                    ← How reports are generated and structured
│   ├── generators/
│   │   ├── html_report.py           ← Generate HTML comparison report
│   │   ├── pdf_report.py            ← PDF version for stakeholders
│   │   └── markdown_report.py       ← Markdown report for GitHub PRs
│   └── examples/
│       ├── model_selection_report_example.html
│       └── weekly_production_report_example.md
│
├── decisions/
│   ├── README.md                    ← Why documenting LLM decisions matters
│   ├── template.md                  ← Decision doc template (ADR-style)
│   └── examples/
│       ├── 2026-05-01_rag_model_selection.md
│       └── 2026-04-15_production_model_upgrade.md
│
├── notebooks/
│   ├── 01_quickstart.ipynb          ← Run your first eval in 10 minutes
│   ├── 02_rag_evaluation.ipynb      ← End-to-end RAG eval with RAGAS
│   ├── 03_model_comparison.ipynb    ← Compare 3 models head-to-head
│   ├── 04_cost_modeling.ipynb       ← Build a cost projection for your use case
│   ├── 05_safety_audit.ipynb        ← Run safety and PII checks
│   └── 06_production_monitoring.ipynb ← Set up continuous monitoring
│
├── tests/
│   ├── unit/
│   │   ├── test_evaluators.py
│   │   ├── test_cost_calculator.py
│   │   └── test_token_counter.py
│   └── integration/
│       ├── test_rag_pipeline.py
│       └── test_model_comparison.py
│
├── ci/
│   ├── README.md
│   ├── .github/
│   │   └── workflows/
│   │       ├── eval_on_pr.yml       ← Run regression evals on every PR
│   │       ├── nightly_eval.yml     ← Nightly full benchmark run
│   │       └── production_alert.yml ← Alert if production metrics degrade
│   └── scripts/
│       ├── run_ci_evals.sh
│       └── compare_to_baseline.py
│
└── docs/
    ├── getting_started.md
    ├── adding_a_new_model.md
    ├── writing_test_cases.md
    ├── scorecard_guide.md
    ├── production_monitoring.md
    └── glossary.md                  ← MMLU, RAGAS, TTFT, faithfulness, etc. defined
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/[your-username]/llm-eval-compass.git
cd llm-eval-compass

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up API keys
cp .env.example .env
# Edit .env with your keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.

# 4. Run your first evaluation
python pipelines/model_comparison.py \
  --models claude-sonnet-4-6,gpt-4o,mistral-large \
  --test-set benchmarks/custom/tpm_domain/meeting_summarization.json \
  --use-case chat \
  --output reports/examples/
```

---

## Core Concepts

### Evaluation Layers

This framework evaluates across three layers:

```
Layer 1: Model Evaluation
  → Benchmark scores (MMLU, HumanEval, GSM8K)
  → Out-of-the-box capability comparison

Layer 2: System Evaluation
  → Domain-specific test sets
  → RAG pipeline evaluation (RAGAS)
  → Prompt + retrieval + model together

Layer 3: Production Monitoring
  → Continuous quality tracking on live traffic
  → Cost and latency alerting
  → Drift detection over time
```

### The Six Evaluation Dimensions

Every model is scored across six dimensions. Weights are configurable in `config/eval_weights.yaml`.

| Dimension | Key Metrics | Default Weight |
|---|---|---|
| Quality | Faithfulness, Answer Relevancy, Hallucination Rate, Task Accuracy | 30% |
| Performance | TTFT, Throughput, Context Window Degradation | 20% |
| Cost | Cost/Query, Cost at Scale (1M/10M queries), Token Efficiency | 20% |
| Safety | Toxicity Rate, PII Leakage, Bias Score, Injection Resistance | 15% |
| Compliance | Data Residency, GDPR Fit, EU AI Act Risk Class | 10% |
| Operational | API Uptime, Rate Limits, Vendor Lock-in Score | 5% |

### Use Case Profiles

Pre-configured weight profiles for common use cases:

```yaml
# config/eval_weights.yaml

profiles:
  customer_facing_chat:
    quality: 0.35
    safety: 0.25
    performance: 0.20
    cost: 0.10
    compliance: 0.05
    operational: 0.05

  internal_enterprise_tool:
    cost: 0.30
    quality: 0.25
    compliance: 0.20
    performance: 0.15
    safety: 0.05
    operational: 0.05

  high_volume_batch:
    cost: 0.40
    performance: 0.30
    quality: 0.20
    safety: 0.05
    compliance: 0.03
    operational: 0.02

  regulated_industry:        # healthcare, finance, legal
    compliance: 0.35
    safety: 0.25
    quality: 0.25
    cost: 0.10
    performance: 0.03
    operational: 0.02
```

---

## Example: Model Comparison Output

Running `pipelines/model_comparison.py` produces a scorecard like this:

```
═══════════════════════════════════════════════════════════════════
LLM EVALUATION SCORECARD — Customer Support Bot
Use Case Profile: customer_facing_chat
Test Set: 100 domain queries | Date: 2026-05-03
═══════════════════════════════════════════════════════════════════

DIMENSION           │ Claude Sonnet │ GPT-4o   │ Mistral Large │ Titan Text
────────────────────┼───────────────┼──────────┼───────────────┼───────────
Task Accuracy       │ 88.4%         │ 87.1%    │ 82.3%         │ 71.2%
Hallucination Rate  │ 2.1%          │ 3.4%     │ 5.8%          │ 14.3%
Faithfulness (RAG)  │ 0.91          │ 0.88     │ 0.83          │ 0.64
Latency p95 (ms)    │ 1,840         │ 2,100    │ 1,420         │ 890
Cost/1K queries     │ $0.47         │ $0.61    │ $0.19         │ $0.08
Toxicity Rate       │ 0.3%          │ 0.4%     │ 0.8%          │ 1.2%
────────────────────┼───────────────┼──────────┼───────────────┼───────────
WEIGHTED SCORE      │ 84.2 ✓        │ 81.7 ✓   │ 74.1          │ 52.3 ✗
────────────────────┼───────────────┼──────────┼───────────────┼───────────
RECOMMENDATION      │ ★ SELECTED    │ Backup   │ Cost-opt alt  │ Not suitable
═══════════════════════════════════════════════════════════════════

Decision rationale: Claude Sonnet scores highest on quality and safety
(weighted 60% combined). At expected volume of 500K queries/month,
cost difference vs GPT-4o is $70/month — acceptable given 2.7% quality
gap. Titan eliminated on hallucination rate (14.3% exceeds 5% threshold).
```

---

## Decision Documentation

Every model selection should be documented. Use the template in `decisions/template.md`:

```markdown
# LLM Selection Decision — [Date]

## Context
What system is this for? What is the use case? What constraints exist?

## Requirements
- Task type:
- Acceptable latency (p95):
- Budget (cost/query or monthly cap):
- Data residency requirement:
- Compliance constraints:

## Candidates Evaluated
List 3–4 models considered and why each was shortlisted.

## Evaluation Results
Link to scorecard output file.

## Decision
Selected model + version. Why it won. What was traded off.

## Risks and Mitigations
What could go wrong? What is the fallback model?

## Review Date
When will this decision be revisited? (Recommend: quarterly)
```

---

## Integrations

| Tool | Purpose | Setup Guide |
|---|---|---|
| [RAGAS](https://docs.ragas.io) | RAG-specific evaluation | `docs/integrations/ragas.md` |
| [LangSmith](https://smith.langchain.com) | Tracing + eval for LangChain | `docs/integrations/langsmith.md` |
| [MLflow](https://mlflow.org) | Experiment tracking | `docs/integrations/mlflow.md` |
| [Weights & Biases](https://wandb.ai) | Dashboard and logging | `docs/integrations/wandb.md` |
| [DeepEval](https://github.com/confident-ai/deepeval) | Unit testing LLM outputs | `docs/integrations/deepeval.md` |
| [Promptfoo](https://promptfoo.dev) | CLI prompt testing, CI/CD | `docs/integrations/promptfoo.md` |
| [AWS Bedrock](https://aws.amazon.com/bedrock) | Bedrock model access | `docs/integrations/bedrock.md` |

---

## CI/CD Integration

Add LLM eval gates to your pipeline:

```yaml
# .github/workflows/eval_on_pr.yml

name: LLM Eval Gate
on: [pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run regression evals
        run: python pipelines/regression_pipeline.py --baseline main --compare ${{ github.sha }}
      - name: Fail if quality drops > 5%
        run: python ci/scripts/compare_to_baseline.py --threshold 0.05
```

This blocks merges if your prompt changes, config updates, or model version upgrades cause quality to drop beyond your threshold.

---

## Production Monitoring

The `pipelines/production_monitor.py` script samples live traffic and runs continuous evaluation:

```python
# Runs on a schedule (cron or Lambda)
# Samples 5% of production queries
# Scores on quality, cost, latency
# Alerts via Slack/PagerDuty if thresholds breached

monitor = ProductionMonitor(
    model="claude-sonnet-4-6",
    sample_rate=0.05,
    metrics=["faithfulness", "latency_p95", "cost_per_query"],
    alert_thresholds={
        "faithfulness": 0.80,      # Alert if drops below 0.80
        "latency_p95_ms": 3000,    # Alert if p95 exceeds 3s
        "cost_per_query_usd": 0.01 # Alert if cost per query spikes
    }
)
```

---

## Glossary

| Term | Definition |
|---|---|
| MMLU | Massive Multitask Language Understanding. Tests knowledge across 57 subjects. |
| HumanEval | OpenAI benchmark for code generation accuracy. |
| RAGAS | RAG Assessment. Open-source framework for evaluating RAG pipelines. |
| Faithfulness | Whether model output is grounded in retrieved context (0–1 score). |
| Hallucination | Model confidently stating something that is factually wrong or not in context. |
| TTFT | Time to First Token. Latency before user sees first word of response. |
| LLM-as-Judge | Using a strong LLM (e.g. GPT-4o) to evaluate outputs from another LLM. |
| p95 Latency | 95th percentile latency — 95% of requests complete within this time. |
| Token | The unit LLMs process. ~0.75 words per token. Pricing is per token. |
| Context Window | Maximum tokens a model processes at once. Larger = handles longer docs. |
| DeepEval | Open-source LLM unit testing framework, pytest-style. |
| Promptfoo | CLI tool for prompt testing and model comparison with CI/CD integration. |
| Bedrock | AWS managed service that hosts multiple LLMs (Claude, Titan, Llama, etc.). |
| LoRA / QLoRA | Parameter-efficient fine-tuning techniques for adapting LLMs to domains. |

---

## Roadmap

- [ ] Add Gemini 2.5 Pro and Flash evaluators
- [ ] Multimodal evaluation support (image + text inputs)
- [ ] Automated red teaming module
- [ ] Cost optimization recommender (suggests when to downgrade model)
- [ ] EU AI Act risk classification automation
- [ ] Streamlit dashboard for non-technical stakeholders

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to:
- Add a new model to the registry
- Write a new domain-specific test set
- Add a new evaluation metric
- Submit a scorecard example

---

## References

- [RAGAS Documentation](https://docs.ragas.io)
- [DeepEval GitHub](https://github.com/confident-ai/deepeval)
- [Promptfoo GitHub](https://github.com/promptfoo/promptfoo)
- [OpenAI Evals](https://github.com/openai/evals)
- [LLM Stats Leaderboard](https://llm-stats.com)
- [Artificial Analysis Leaderboard](https://artificialanalysis.ai/leaderboards/models)
- [LLM Evaluation Frameworks 2026 — MLAI Digital](https://www.mlaidigital.com/blogs/llm-evaluation-frameworks-2026)
- [Evaluating RAG with LangSmith — LangChain Blog](https://blog.langchain.com/evaluating-rag-pipelines-with-ragas-langsmith/)

---

*Built by Rahul Goel — Principal TPM | GenAI/LLMOps*
*Contributions welcome. Star the repo if it helps your team.*
