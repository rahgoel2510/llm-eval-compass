import json
import boto3


class BedrockClient:
    def __init__(self, region: str = "us-east-1"):
        self.runtime = boto3.client("bedrock-runtime", region_name=region)
        self.bedrock = boto3.client("bedrock", region_name=region)

    def invoke(self, model_id: str, prompt: str, **kwargs) -> dict:
        body = json.dumps({"prompt": prompt, **kwargs})
        resp = self.runtime.invoke_model(modelId=model_id, body=body)
        return json.loads(resp["body"].read())

    def list_models(self) -> list:
        resp = self.bedrock.list_foundation_models()
        return resp["modelSummaries"]
