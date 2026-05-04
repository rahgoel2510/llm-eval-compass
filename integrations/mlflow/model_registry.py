import mlflow


class ModelRegistry:
    def register(self, model_name: str, model_id: str, scores: dict):
        mlflow.set_experiment(model_name)
        with mlflow.start_run():
            mlflow.log_params({"model_id": model_id})
            mlflow.log_metrics(scores)
            mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", model_name)
