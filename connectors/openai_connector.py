"""OpenAI connector (GPT-4o, GPT-4o-mini, GPT-4.1, etc.)."""

from openai import OpenAI

from connectors.base import BaseConnector, ModelResponse


class OpenAIConnector(BaseConnector):
    """Connector for OpenAI chat completions API."""

    @property
    def provider(self) -> str:
        return "OpenAI"

    def _call(self, prompt: str, **kwargs) -> ModelResponse:
        client = OpenAI(api_key=self.api_key)
        resp = client.chat.completions.create(
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
            raw=resp.model_dump(),
        )
