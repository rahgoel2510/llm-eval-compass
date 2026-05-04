"""Base connector interface and response model."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ModelResponse:
    """Standardized response from any model provider."""

    text: str
    model_id: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    raw: dict = field(default_factory=dict)


class BaseConnector(ABC):
    """Abstract base for all model connectors."""

    def __init__(self, model_id: str, api_key: str | None = None, **kwargs) -> None:
        self.model_id = model_id
        self.api_key = api_key
        self.extra = kwargs

    @abstractmethod
    def _call(self, prompt: str, **kwargs) -> ModelResponse:
        """Provider-specific API call. Subclasses implement this."""

    def generate(self, prompt: str, **kwargs) -> ModelResponse:
        """Send prompt to model and return standardized response with latency."""
        start = time.perf_counter()
        resp = self._call(prompt, **kwargs)
        resp.latency_ms = (time.perf_counter() - start) * 1000
        return resp

    @property
    @abstractmethod
    def provider(self) -> str:
        """Return provider name (e.g. 'OpenAI', 'Anthropic')."""

    def test_connection(self) -> bool:
        """Quick connectivity check."""
        try:
            resp = self.generate("Say 'ok'.", max_tokens=5)
            return bool(resp.text)
        except Exception:
            return False
