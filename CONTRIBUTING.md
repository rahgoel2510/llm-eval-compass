# Contributing to llm-eval-compass

Thanks for your interest in contributing! Here's how to get involved.

## Development Setup

```bash
git clone https://github.com/[your-username]/llm-eval-compass.git
cd llm-eval-compass
pip install -r requirements.txt
pip install -e '.[dev]'
pytest
```

## How to Add a New Model

1. Add the model entry to `config/models.yaml` with endpoint, pricing, and context window info.
2. If the model requires a custom API client, create an evaluator under `evaluators/` or add support in an existing integration under `integrations/`.
3. Run the test suite to verify: `pytest tests/`

## How to Write a Domain-Specific Test Set

1. Copy `benchmarks/custom/template.json` to a new file under `benchmarks/custom/your_domain/`.
2. Each test case needs an `input`, `expected_output`, and optional `context` field.
3. Include at least 50 test cases for statistical significance.
4. Add a brief description in your test set's JSON metadata.

## How to Add a New Evaluation Metric

1. Create a new file under the appropriate `evaluators/` subdirectory.
2. Extend `BaseEvaluator` from `evaluators/base_evaluator.py`.
3. Implement the `evaluate()` method returning a score between 0 and 1.
4. Add unit tests in `tests/unit/`.

## How to Submit a Scorecard Example

1. Run a comparison using `pipelines/model_comparison.py`.
2. Save the output as a Markdown file under `scorecards/examples/`.
3. Use the naming convention: `modelA_vs_modelB_usecase.md`.

## Code Style

- Format with **black** and lint with **ruff**.
- Type hints are required on all public functions.
- Run `ruff check .` and `black --check .` before submitting.

## PR Process

1. Create a feature branch: `git checkout -b feat/your-change`
2. Make your changes and add tests.
3. Run the full test suite: `pytest`
4. Submit a pull request with a clear description of what changed and why.
5. PRs require one approving review before merge.
