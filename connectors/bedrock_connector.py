"""AWS Bedrock connector (Titan, Claude on Bedrock, Llama on Bedrock)."""

import json

import boto3

from connectors.base import BaseConnector, ModelResponse


class BedrockConnector(BaseConnector):
    """Connector for AWS Bedrock invoke_model API."""

    @property
    def provider(self) -> str:
        return "AWS Bedrock"

    def _call(self, prompt: str, **kwargs) -> ModelResponse:
        region = self.extra.get("region", "us-east-1")
        client = boto3.client(
            "bedrock-runtime",
            region_name=region,
            aws_access_key_id=self.extra.get("aws_access_key_id"),
            aws_secret_access_key=self.extra.get("aws_secret_access_key"),
        )
        body = self._build_body(prompt, **kwargs)
        resp = client.invoke_model(modelId=self.model_id, body=json.dumps(body))
        result = json.loads(resp["body"].read())
        text, in_tok, out_tok = self._parse_response(result)
        return ModelResponse(
            text=text,
            model_id=self.model_id,
            input_tokens=in_tok,
            output_tokens=out_tok,
            raw=result,
        )

    def _build_body(self, prompt: str, **kwargs) -> dict:
        max_tokens = kwargs.get("max_tokens", 1024)
        # Titan
        if "titan" in self.model_id.lower():
            return {"inputText": prompt, "textGenerationConfig": {"maxTokenCount": max_tokens, "temperature": 0}}
        # Claude on Bedrock
        if "claude" in self.model_id.lower() or "anthropic" in self.model_id.lower():
            return {"anthropic_version": "bedrock-2023-05-31", "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}
        # Llama on Bedrock
        return {"prompt": prompt, "max_gen_len": max_tokens, "temperature": 0}

    def _parse_response(self, result: dict) -> tuple[str, int, int]:
        # Titan
        if "results" in result:
            r = result["results"][0]
            return r.get("outputText", ""), result.get("inputTextTokenCount", 0), r.get("tokenCount", 0)
        # Claude on Bedrock
        if "content" in result:
            text = result["content"][0]["text"] if result["content"] else ""
            u = result.get("usage", {})
            return text, u.get("input_tokens", 0), u.get("output_tokens", 0)
        # Llama on Bedrock
        return result.get("generation", ""), 0, 0
