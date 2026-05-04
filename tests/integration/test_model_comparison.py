import pytest


@pytest.mark.integration
def test_model_comparison_imports():
    from pipelines import model_comparison  # noqa: F401
