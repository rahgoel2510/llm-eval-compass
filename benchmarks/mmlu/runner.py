"""MMLU benchmark runner."""

import json


class MMLURunner:
    """Runs MMLU multiple-choice questions and scores accuracy."""

    def run(self, model_fn, questions_path: str = "benchmarks/mmlu/sample_questions.json") -> dict:
        with open(questions_path) as f:
            questions = json.load(f)

        correct = 0
        for q in questions:
            prompt = f"Subject: {q['subject']}\nQuestion: {q['question']}\n"
            prompt += "\n".join(f"{k}) {v}" for k, v in q["choices"].items())
            prompt += "\nAnswer with just the letter:"

            response = model_fn(prompt).strip().upper()
            if response and response[0] == q["answer"]:
                correct += 1

        return {"total": len(questions), "correct": correct, "accuracy": correct / len(questions) if questions else 0}
