# Benchmarks

## When to Use Which Benchmark

| Benchmark | Tests | Use When |
|---|---|---|
| **MMLU** | Knowledge across 57 subjects | Comparing general knowledge and reasoning |
| **HumanEval** | Code generation accuracy | Evaluating coding assistants or code-gen features |
| **GSM8K** | Grade-school math reasoning | Testing multi-step reasoning and arithmetic |
| **Custom** | Domain-specific tasks | Evaluating for your actual use case (recommended) |
| **Chatbot Arena** | Community ELO rankings | Quick reference for overall model standing |

## Guidance

- Always run **custom domain benchmarks** in addition to generic ones — generic scores don't predict domain performance.
- Use `benchmarks/custom/template.json` to create your own test sets.
- Benchmark scores are one input to the scorecard, not the final decision. See `scorecards/` for weighted evaluation.
