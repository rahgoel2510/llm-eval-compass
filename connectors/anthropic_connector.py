"""Anthropic connector (Claude Haiku, Sonnet, Opus)."""

from anthropic import Anthropic

from connectors.base import BaseConnector, ModelResponse


class AnthropicConnector(BaseConnector):
    """Connector for Anthropic messages API."""

    @property
    def provider(self) -> str:
        return "Anthropic"

    def _call(self, prompt: str, **kwargs) -> ModelResponse:
        client = Anthropic(api_key=self.api_key)
        resp = client.messages.create(
            model=self.model_id,
            max_tokens=kwargs.get("max_tokens", 1024),
            temperature=kwargs.get("temperature", 0),
            messages=[{"role": "user", "content": prompt}],
        )
        text = resp.content[0].text if resp.content else ""
        return ModelResponse(
            text=text,
            model_id=self.model_id,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            raw=resp.model_dump(),
        )
