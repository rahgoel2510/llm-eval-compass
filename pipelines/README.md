# Pipelines

## single_model_eval.py
Evaluate a single model against a JSON test set. Loads model config and eval weight
profiles from `config/`, runs quality, performance, and cost evaluators, and writes
results as JSON to the specified output directory.

## model_comparison.py
Head-to-head comparison of multiple models. Runs `single_model_eval` for each model,
computes weighted scores using the selected use-case profile, prints a rich table to
the terminal, and saves both a JSON results file and a markdown scorecard.

## rag_eval_pipeline.py
RAG-specific evaluation pipeline. Runs RAGAS metrics (faithfulness, answer relevancy,
context precision, context recall) against a test set of query/context/answer triples
and outputs results as JSON.
