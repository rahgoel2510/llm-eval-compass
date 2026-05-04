import pytest


@pytest.mark.integration
def test_rag_eval_pipeline_imports():
    from pipelines import rag_eval_pipeline  # noqa: F401
