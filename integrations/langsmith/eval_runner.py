from langsmith import Client


class LangSmithEvalRunner:
    def __init__(self):
        self.client = Client()

    def run(self, dataset_name: str, model_fn: callable) -> dict:
        results = self.client.run_on_dataset(dataset_name=dataset_name, llm_or_chain_factory=model_fn)
        return results
