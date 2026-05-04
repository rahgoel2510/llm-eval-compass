from .bedrock_client import BedrockClient


class BedrockEvalHelper:
    def __init__(self, client: BedrockClient):
        self.client = client

    def evaluate_model(self, model_id: str, test_cases: list[dict]) -> dict:
        results = []
        for tc in test_cases:
            resp = self.client.invoke(model_id, tc["prompt"])
            results.append({"input": tc["prompt"], "expected": tc.get("expected"), "output": resp})
        return {"model_id": model_id, "results": results}
