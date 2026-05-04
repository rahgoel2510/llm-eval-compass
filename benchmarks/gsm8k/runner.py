"""GSM8K math reasoning benchmark runner."""

import re


class GSM8KRunner:
    """Runs grade-school math problems and checks numeric answers."""

    PROBLEMS = [
        {"question": "If a train travels 60 miles in 1.5 hours, what is its speed in mph?", "answer": 40},
        {"question": "A store sells 3 apples for $2. How much do 12 apples cost?", "answer": 8},
        {"question": "If 5 workers can build a wall in 10 days, how many days for 10 workers?", "answer": 5},
    ]

    def run(self, model_fn) -> dict:
        correct = 0
        for p in self.PROBLEMS:
            response = model_fn(p["question"] + "\nGive only the final numeric answer:")
            numbers = re.findall(r"[\d.]+", response)
            if numbers and float(numbers[-1]) == p["answer"]:
                correct += 1

        return {"total": len(self.PROBLEMS), "correct": correct, "accuracy": correct / len(self.PROBLEMS)}
