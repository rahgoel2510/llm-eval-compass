"""Context window evaluator testing quality degradation at different lengths."""

from typing import Callable

from evaluators.base_evaluator import BaseEvaluator


class ContextWindowEvaluator(BaseEvaluator):
    """Tests quality degradation as context length increases."""

    @property
    def name(self) -> str:
        return "context_window"

    def evaluate(self, inputs: list[dict]) -> dict:
        """Evaluate context window degradation.

        Each input needs: prompt, context, expected.
        Config needs: call_fn(prompt) -> str, context_sizes (list[int] of token counts).
        """
        call_fn: Callable = self.config["call_fn"]
        sizes = self.config.get("context_sizes", [1000, 4000, 8000, 16000, 32000])
        results: dict[str, float] = {}

        for item in inputs:
            for size in sizes:
                truncated_ctx = item["context"][:size]
                prompt = f"Context: {truncated_ctx}\n\nQuestion: {item['prompt']}"
                output = call_fn(prompt)
                # TODO: use a proper similarity metric instead of simple containment
                score = 1.0 if item["expected"].lower() in output.lower() else 0.0
                key = f"accuracy_at_{size}_tokens"
                results[key] = results.get(key, 0.0) + score

        n = len(inputs) or 1
        return {k: v / n for k, v in results.items()}
