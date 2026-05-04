"""Google Gemini connector."""

import google.generativeai as genai

from connectors.base import BaseConnector, ModelResponse


class GoogleConnector(BaseConnector):
    """Connector for Google Gemini API."""

    @property
    def provider(self) -> str:
        return "Google"

    def _call(self, prompt: str, **kwargs) -> ModelResponse:
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model_id)
        resp = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=kwargs.get("max_tokens", 1024),
                temperature=kwargs.get("temperature", 0),
            ),
        )
        usage = resp.usage_metadata
        return ModelResponse(
            text=resp.text or "",
            model_id=self.model_id,
            input_tokens=getattr(usage, "prompt_token_count", 0),
            output_tokens=getattr(usage, "candidates_token_count", 0),
            raw={"text": resp.text},
        )
