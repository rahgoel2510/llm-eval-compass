"""Cost calculator loading pricing from models.yaml."""

from pathlib import Path

import yaml


class CostCalculator:
    """Calculates cost per query based on model pricing."""

    def __init__(self, config_path: str | None = None) -> None:
        path = Path(config_path or "config/models.yaml")
        with open(path) as f:
            self.models = yaml.safe_load(f) or {}

    def cost_per_query(self, input_tokens: int, output_tokens: int, model_id: str) -> float:
        """Calculate cost for a single query in USD."""
        pricing = self.models.get(model_id, {}).get("pricing", {})
        input_cost = pricing.get("input_per_1k_tokens", 0.0)
        output_cost = pricing.get("output_per_1k_tokens", 0.0)
        return (input_tokens * input_cost + output_tokens * output_cost) / 1000
