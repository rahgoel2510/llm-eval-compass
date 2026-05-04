from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

METRICS_MAP = {
    "faithfulness": faithfulness,
    "answer_relevancy": answer_relevancy,
    "context_precision": context_precision,
    "context_recall": context_recall,
}


def get_metrics(names: list[str]) -> list:
    return [METRICS_MAP[n] for n in names]
