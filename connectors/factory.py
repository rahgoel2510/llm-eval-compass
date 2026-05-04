"""Factory to create the right connector from a model ID or provider name."""

from __future__ import annotations

from pathlib import Path

import yaml

from connectors.base import BaseConnector

# Provider -> (module_path, class_name)
_REGISTRY: dict[str, tuple[str, str]] = {
    "OpenAI": ("connectors.openai_connector", "OpenAIConnector"),
    "Anthropic": ("connectors.anthropic_connector", "AnthropicConnector"),
    "Google": ("connectors.google_connector", "GoogleConnector"),
    "Mistral": ("connectors.mistral_connector", "MistralConnector"),
    "AWS Bedrock": ("connectors.bedrock_connector", "BedrockConnector"),
}


def _load_model_config(model_key: str) -> dict | None:
    path = Path(__file__).resolve().parent.parent / "config" / "models.yaml"
    if not path.exists():
        return None
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return data.get("models", {}).get(model_key)


def create_connector(
    model_key: str,
    api_key: str | None = None,
    provider: str | None = None,
    **kwargs,
) -> BaseConnector:
    """Create a connector for the given model.

    Args:
        model_key: Key from models.yaml (e.g. 'gpt-4o') or a raw model ID.
        api_key: API key for the provider.
        provider: Override provider detection (e.g. 'OpenAI').
        **kwargs: Extra args passed to the connector (region, aws keys, etc.).

    Returns:
        A configured BaseConnector instance.
    """
    cfg = _load_model_config(model_key)
    if cfg:
        resolved_provider = provider or cfg["provider"]
        model_id = cfg.get("model_id", model_key)
    else:
        resolved_provider = provider or _guess_provider(model_key)
        model_id = model_key

    if resolved_provider not in _REGISTRY:
        raise ValueError(f"Unknown provider '{resolved_provider}'. Supported: {list(_REGISTRY.keys())}")

    module_path, class_name = _REGISTRY[resolved_provider]
    import importlib
    mod = importlib.import_module(module_path)
    cls = getattr(mod, class_name)
    return cls(model_id=model_id, api_key=api_key, **kwargs)


def _guess_provider(model_id: str) -> str:
    mid = model_id.lower()
    if "gpt" in mid or "o1" in mid or "o3" in mid:
        return "OpenAI"
    if "claude" in mid:
        return "Anthropic"
    if "gemini" in mid:
        return "Google"
    if "mistral" in mid:
        return "Mistral"
    if "titan" in mid or "llama" in mid:
        return "AWS Bedrock"
    raise ValueError(f"Cannot guess provider for '{model_id}'. Pass provider= explicitly.")
