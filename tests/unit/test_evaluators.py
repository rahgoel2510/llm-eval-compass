import pytest
from evaluators.base_evaluator import BaseEvaluator
from evaluators.quality.task_accuracy import TaskAccuracyEvaluator
from evaluators.safety.pii_leakage import PIILeakageEvaluator


def test_base_evaluator_is_abstract():
    with pytest.raises(TypeError):
        BaseEvaluator("test-model")


def test_task_accuracy_exact_match():
    evaluator = TaskAccuracyEvaluator("test-model")
    result = evaluator.evaluate([{"output": "hello world", "expected": "hello world"}])
    assert result["exact_match"] == 1.0


def test_pii_leakage_detects_email():
    evaluator = PIILeakageEvaluator("test-model")
    result = evaluator.evaluate([{"output": "Contact me at user@example.com"}])
    assert result["detections"]["email"] == 1
    assert result["pii_leakage_rate"] > 0
