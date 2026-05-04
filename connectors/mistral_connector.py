"""Mistral AI connector."""

from mistralai import Mistral

from connectors.base import BaseConnector, ModelResponse


class MistralConnector(BaseConnector):
    """Connector for Mistral chat API."""

    @property
    def provider(self) -> str:
        return "Mistral"

    def _call(self, prompt: str, **kwargs) -> ModelResponse:
        client = Mistral(api_key=self.api_key)
        resp = client.chat.complete(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 1024),
            temperature=kwargs.get("temperature", 0),
        )
        choice = resp.choices[0]
        usage = resp.usage
        return ModelResponse(
            text=choice.message.content or "",
            model_id=self.model_id,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            raw=resp.model_dump() if hasattr(resp, "model_dump") else {},
        )
