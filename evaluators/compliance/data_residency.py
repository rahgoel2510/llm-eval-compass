"""Data residency checker using models.yaml."""

from pathlib import Path

import yaml


class DataResidencyChecker:
    """Maps models to their data processing regions."""

    def __init__(self, config_path: str | None = None) -> None:
        path = Path(config_path or "config/models.yaml")
        with open(path) as f:
            self.models = yaml.safe_load(f) or {}

    def check(self, model_id: str) -> dict:
        """Return data residency info for a model."""
        model = self.models.get(model_id, {})
        return {
            "model_id": model_id,
            "provider": model.get("provider", "unknown"),
            "regions": model.get("data_residency", {}).get("regions", []),
            "data_processing_location": model.get("data_residency", {}).get("location", "unknown"),
        }
