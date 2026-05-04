from deepeval import evaluate
from deepeval.metrics import HallucinationMetric, ToxicityMetric, BiasMetric
from deepeval.test_case import LLMTestCase

METRICS_MAP = {
    "hallucination": HallucinationMetric,
    "toxicity": ToxicityMetric,
    "bias": BiasMetric,
}

DEFAULT_METRICS = ["hallucination", "toxicity", "bias"]


class DeepEvalTestSuite:
    def __init__(self, metrics: list[str] | None = None):
        self.metrics = [METRICS_MAP[m]() for m in (metrics or DEFAULT_METRICS)]

    def run(self, test_cases: list[dict]) -> dict:
        cases = [LLMTestCase(input=tc["input"], actual_output=tc["actual_output"],
                             context=tc.get("context")) for tc in test_cases]
        results = evaluate(cases, self.metrics)
        return {"results": results}
