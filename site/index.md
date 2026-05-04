---
layout: default
title: LLM Eval Compass — Evaluate, Compare, and Select LLMs with Confidence
---

## The Problem

Your team is choosing an LLM. You run a few prompts, compare vibes, and pick one. Six months later, costs spike, hallucinations surface in production, and nobody remembers *why* that model was chosen.

**Sound familiar?**

Most LLM evaluation approaches fail because they:
- Run generic benchmarks and assume the highest score wins
- Evaluate once and never monitor in production
- Leave no documentation trail for future decisions

LLM Eval Compass fixes all three.

---

## What You Get

<div class="card-grid">
  <div class="card">
    <div class="icon">🎯</div>
    <h3>Multi-Dimensional Scoring</h3>
    <p>Every model scored across 6 dimensions — quality, performance, cost, safety, compliance, and operational — with configurable weights per use case.</p>
  </div>
  <div class="card">
    <div class="icon">🔌</div>
    <h3>Plug In Any Model</h3>
    <p>Unified connector layer for OpenAI, Anthropic, Google, Mistral, and AWS Bedrock. One interface, every provider. Add your own in minutes.</p>
  </div>
  <div class="card">
    <div class="icon">📊</div>
    <h3>Interactive Dashboard</h3>
    <p>Streamlit-powered UI with demo mode. Run evaluations, compare models head-to-head, project costs, and scan for PII — no API keys needed to try.</p>
  </div>
  <div class="card">
    <div class="icon">🧪</div>
    <h3>Domain-Specific Testing</h3>
    <p>Bring your own test sets or use built-in benchmarks (MMLU, HumanEval, GSM8K). Evaluate on what matters to your business, not generic leaderboards.</p>
  </div>
  <div class="card">
    <div class="icon">🔒</div>
    <h3>Safety & Compliance</h3>
    <p>Built-in evaluators for toxicity, PII leakage, bias detection, prompt injection resistance, GDPR compliance, and EU AI Act risk classification.</p>
  </div>
  <div class="card">
    <div class="icon">🔄</div>
    <h3>CI/CD Eval Gates</h3>
    <p>Block merges if prompt changes or model upgrades degrade quality. Nightly benchmarks. Production monitoring with alerting.</p>
  </div>
</div>

---

## Supported Models

| Provider | Models |
|---|---|
| **Anthropic** | Claude Haiku 3.5, Sonnet 4.6, Opus 4.6 |
| **OpenAI** | GPT-4o, GPT-4o-mini, GPT-4.1 |
| **Google** | Gemini 2.5 Pro, Gemini 2.5 Flash |
| **AWS Bedrock** | Titan Text, Claude on Bedrock, Llama 3 (8B, 70B) |
| **Mistral AI** | Mistral Large, Mistral Small |
| **Self-hosted** | Any model via Ollama or vLLM |

---

## The Six Evaluation Dimensions

| Dimension | What It Measures | Default Weight |
|---|---|---|
| **Quality** | Faithfulness, answer relevancy, hallucination rate, task accuracy | 30% |
| **Performance** | Time to first token, throughput, context window degradation | 20% |
| **Cost** | Cost per query, cost at scale, token efficiency | 20% |
| **Safety** | Toxicity, PII leakage, bias, prompt injection resistance | 15% |
| **Compliance** | Data residency, GDPR fit, EU AI Act risk classification | 10% |
| **Operational** | API uptime, rate limits, vendor lock-in risk | 5% |

Weights are fully configurable. Pre-built profiles for **customer-facing chat**, **internal tools**, **high-volume batch**, and **regulated industries**.

---

## Example: Model Comparison Output

<div class="scorecard-preview">
═══════════════════════════════════════════════════════════════<br>
&nbsp;LLM EVALUATION SCORECARD — Customer Support Bot<br>
═══════════════════════════════════════════════════════════════<br>
<br>
&nbsp;DIMENSION &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; │ Claude Sonnet │ GPT-4o &nbsp; │ Mistral Large<br>
&nbsp;───────────────────┼───────────────┼──────────┼──────────────<br>
&nbsp;Task Accuracy &nbsp; &nbsp; &nbsp;│ 88.4% &nbsp; &nbsp; &nbsp; &nbsp; │ 87.1% &nbsp; &nbsp;│ 82.3%<br>
&nbsp;Hallucination Rate │ <span class="pass">2.1%</span> &nbsp; &nbsp; &nbsp; &nbsp; │ <span class="pass">3.4%</span> &nbsp; &nbsp;│ <span class="fail">5.8%</span><br>
&nbsp;Faithfulness (RAG) │ 0.91 &nbsp; &nbsp; &nbsp; &nbsp; │ 0.88 &nbsp; &nbsp; │ 0.83<br>
&nbsp;Latency p95 (ms) &nbsp; │ 1,840 &nbsp; &nbsp; &nbsp; &nbsp; │ 2,100 &nbsp; &nbsp;│ 1,420<br>
&nbsp;Cost/1K queries &nbsp; &nbsp;│ $0.47 &nbsp; &nbsp; &nbsp; &nbsp; │ $0.61 &nbsp; &nbsp;│ $0.19<br>
&nbsp;───────────────────┼───────────────┼──────────┼──────────────<br>
&nbsp;WEIGHTED SCORE &nbsp; &nbsp; &nbsp;│ <span class="highlight">84.2 ✓</span> &nbsp; &nbsp; &nbsp; │ <span class="pass">81.7 ✓</span> &nbsp;│ 74.1<br>
&nbsp;RECOMMENDATION &nbsp; &nbsp; │ <span class="highlight">★ SELECTED</span> &nbsp; &nbsp;│ Backup &nbsp; │ Cost-opt alt<br>
═══════════════════════════════════════════════════════════════
</div>

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/rahgoel2510/llm-eval-compass.git
cd llm-eval-compass
pip install -r requirements.txt

# Launch the interactive dashboard (demo mode — no API keys needed)
streamlit run app.py

# Or run from the CLI
python pipelines/model_comparison.py \
  --models claude-sonnet-4-6,gpt-4o,mistral-large \
  --test-set benchmarks/custom/tpm_domain/meeting_summarization.json \
  --use-case customer_facing_chat \
  --output reports/examples/
```

---

## Integrations

<div class="card-grid">
  <div class="card">
    <h3>🔬 RAGAS</h3>
    <p>RAG pipeline evaluation — faithfulness, answer relevancy, context precision and recall.</p>
  </div>
  <div class="card">
    <h3>🧪 DeepEval</h3>
    <p>Pytest-style unit testing for LLM outputs — hallucination, toxicity, bias metrics.</p>
  </div>
  <div class="card">
    <h3>🔗 LangSmith</h3>
    <p>Tracing and evaluation for LangChain-based applications.</p>
  </div>
  <div class="card">
    <h3>📈 MLflow</h3>
    <p>Experiment tracking — log eval runs, compare across versions, register models.</p>
  </div>
  <div class="card">
    <h3>📊 Weights & Biases</h3>
    <p>Dashboards and logging for evaluation results across teams.</p>
  </div>
  <div class="card">
    <h3>⚡ Promptfoo</h3>
    <p>CLI-based prompt testing with CI/CD integration and YAML configs.</p>
  </div>
</div>

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit Dashboard                 │
│   Connect Model → Select Test Set → Run → Compare   │
└──────────────────────┬──────────────────────────────┘
                       │
              ┌────────▼────────┐
              │  Eval Engine    │  Orchestrates the full pipeline
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │Connectors│  │Evaluators│  │ Reports  │
   │ OpenAI   │  │ Quality  │  │ HTML     │
   │ Anthropic│  │ Safety   │  │ Markdown │
   │ Google   │  │ Cost     │  │ PDF      │
   │ Mistral  │  │ Perf     │  │ JSON     │
   │ Bedrock  │  │ Comply   │  └──────────┘
   │ Mock/Demo│  └──────────┘
   └──────────┘
```

---

## Documentation

| Guide | Description |
|---|---|
| [Getting Started](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/getting_started.md) | Install, configure, run your first eval |
| [Adding a New Model](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/adding_a_new_model.md) | Register models in the YAML config |
| [Writing Test Cases](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/writing_test_cases.md) | Create domain-specific evaluation sets |
| [Scorecard Guide](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/scorecard_guide.md) | Interpret and customize scorecards |
| [Production Monitoring](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/production_monitoring.md) | Continuous quality tracking |
| [Glossary](https://github.com/rahgoel2510/llm-eval-compass/blob/main/docs/glossary.md) | MMLU, RAGAS, TTFT, faithfulness, etc. |

---

## Contributing

We welcome contributions — new models, evaluation metrics, domain test sets, and scorecard examples. See the [Contributing Guide](https://github.com/rahgoel2510/llm-eval-compass/blob/main/CONTRIBUTING.md).

```bash
git clone https://github.com/rahgoel2510/llm-eval-compass.git
cd llm-eval-compass
pip install -e ".[dev]"
pytest
```
