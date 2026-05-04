import yaml


class PromptfooConfigGenerator:
    def generate(self, models: list[str], prompts: list[str], output_path: str):
        config = {
            "providers": models,
            "prompts": prompts,
        }
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
