import mlflow


class ExperimentTracker:
    def log_eval_run(self, experiment_name: str, model_id: str, metrics: dict, params: dict):
        mlflow.set_experiment(experiment_name)
        with mlflow.start_run():
            mlflow.log_params({"model_id": model_id, **params})
            mlflow.log_metrics(metrics)
