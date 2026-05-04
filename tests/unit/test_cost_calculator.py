import pytest
from evaluators.cost.cost_calculator import CostCalculator
from evaluators.cost.cost_projector import CostProjector


def test_cost_calculation(tmp_path):
    config = tmp_path / "models.yaml"
    config.write_text(
        "test-model:\n"
        "  pricing:\n"
        "    input_per_1k_tokens: 0.01\n"
        "    output_per_1k_tokens: 0.03\n"
    )
    calc = CostCalculator(config_path=str(config))
    cost = calc.cost_per_query(1000, 500, "test-model")
    assert cost == pytest.approx(0.01 + 0.015)


def test_cost_projection(tmp_path):
    config = tmp_path / "models.yaml"
    config.write_text(
        "test-model:\n"
        "  pricing:\n"
        "    input_per_1k_tokens: 0.001\n"
        "    output_per_1k_tokens: 0.002\n"
    )
    calc = CostCalculator(config_path=str(config))
    projector = CostProjector(calculator=calc)
    result = projector.project("test-model", queries_per_day=1000, avg_input_tokens=100, avg_output_tokens=100)
    assert result["monthly"] == pytest.approx(result["daily"] * 30)
