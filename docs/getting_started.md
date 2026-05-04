# Getting Started

## 1. Install Dependencies
```bash
git clone https://github.com/[your-username]/llm-eval-compass.git
cd llm-eval-compass
pip install -r requirements.txt
```

## 2. Configure API Keys
```bash
cp .env.example .env
# Edit .env with your keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, AWS credentials, etc.
```

## 3. Run Your First Evaluation
```bash
python pipelines/single_model_eval.py --model claude-sonnet-4-6 --test-set benchmarks/custom/tpm_domain/meeting_summarization.json
```

## 4. Compare Models
```bash
python pipelines/model_comparison.py --models claude-sonnet-4-6,gpt-4o,mistral-large --test-set benchmarks/custom/tpm_domain/meeting_summarization.json --use-case chat --output reports/examples/
```

See `notebooks/01_quickstart.ipynb` for an interactive walkthrough.
