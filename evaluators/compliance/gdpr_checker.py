"""GDPR compliance checker."""

from pathlib import Path

import yaml


class GDPRChecker:
    """Checks GDPR compliance flags for models."""

    def __init__(self, config_path: str | None = None) -> None:
        path = Path(config_path or "config/models.yaml")
        with open(path) as f:
            self.models = yaml.safe_load(f) or {}

    def check(self, model_id: str) -> dict:
        """Return GDPR compliance flags for a model."""
        model = self.models.get(model_id, {})
        compliance = model.get("compliance", {})
        return {
            "model_id": model_id,
            "gdpr_compliant": compliance.get("gdpr", False),
            "dpa_available": compliance.get("dpa_available", False),
            "data_retention_days": compliance.get("data_retention_days", -1),
            "eu_hosting_available": compliance.get("eu_hosting", False),
            "right_to_deletion": compliance.get("right_to_deletion", False),
        }
