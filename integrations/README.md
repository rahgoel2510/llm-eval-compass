# Integrations

## ragas
RAG evaluation using the RAGAS framework. Provides faithfulness, answer relevancy, context precision, and context recall metrics.
Wraps `ragas.evaluate()` for easy use with dataset dicts.

## bedrock
AWS Bedrock model invocation and evaluation helpers.
Supports invoking any Bedrock foundation model and running test case batches for comparison.

## deepeval
LLM output unit testing via DeepEval.
Runs hallucination, toxicity, and bias checks using pytest-style test cases.

## langsmith
LangSmith tracing and evaluation integration for LangChain-based pipelines.
Sets up tracing env vars and runs evaluations against LangSmith datasets.

## mlflow
MLflow experiment tracking and model registry integration.
Logs eval runs as experiments and registers models with their scores.

## wandb
Weights & Biases logging for eval metrics.
Logs model evaluation results to W&B projects for dashboarding.

## promptfoo
Promptfoo YAML config generation for CLI-based prompt testing.
Generates config files for model comparison and CI/CD integration.
