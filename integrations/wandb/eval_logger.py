import wandb


class WandbEvalLogger:
    def log(self, project: str, model_id: str, metrics: dict):
        wandb.init(project=project, config={"model_id": model_id})
        wandb.log(metrics)
        wandb.finish()
