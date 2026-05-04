"""HumanEval code generation benchmark runner."""

import json


class HumanEvalRunner:
    """Runs HumanEval code generation problems and checks correctness."""

    def run(self, model_fn, problems_path: str = "benchmarks/humaneval/problems.json") -> dict:
        with open(problems_path) as f:
            problems = json.load(f)

        passed = 0
        for p in problems:
            code = model_fn(p["prompt"])
            try:
                exec(code + "\n" + p["test"], {})
                passed += 1
            except Exception:
                pass

        return {"total": len(problems), "passed": passed, "pass_rate": passed / len(problems) if problems else 0}
