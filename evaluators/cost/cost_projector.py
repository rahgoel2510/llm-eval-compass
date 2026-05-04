"""Cost projector for daily/monthly/annual estimates."""

from evaluators.cost.cost_calculator import CostCalculator


class CostProjector:
    """Projects costs at scale given usage patterns."""

    def __init__(self, calculator: CostCalculator) -> None:
        self.calculator = calculator

    def project(
        self, model_id: str, queries_per_day: int, avg_input_tokens: int, avg_output_tokens: int
    ) -> dict[str, float]:
        """Project costs over time periods."""
        cost_per_query = self.calculator.cost_per_query(avg_input_tokens, avg_output_tokens, model_id)
        daily = cost_per_query * queries_per_day
        return {
            "cost_per_query": cost_per_query,
            "daily": daily,
            "monthly": daily * 30,
            "annual": daily * 365,
        }
