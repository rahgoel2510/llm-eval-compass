# Glossary

| Term | Definition |
|---|---|
| MMLU | Massive Multitask Language Understanding. Tests knowledge across 57 subjects. |
| HumanEval | OpenAI benchmark for code generation accuracy. |
| RAGAS | RAG Assessment. Open-source framework for evaluating RAG pipelines. |
| Faithfulness | Whether model output is grounded in retrieved context (0–1 score). |
| Hallucination | Model confidently stating something that is factually wrong or not in context. |
| TTFT | Time to First Token. Latency before user sees first word of response. |
| LLM-as-Judge | Using a strong LLM (e.g. GPT-4o) to evaluate outputs from another LLM. |
| p95 Latency | 95th percentile latency — 95% of requests complete within this time. |
| Token | The unit LLMs process. ~0.75 words per token. Pricing is per token. |
| Context Window | Maximum tokens a model processes at once. Larger = handles longer docs. |
| DeepEval | Open-source LLM unit testing framework, pytest-style. |
| Promptfoo | CLI tool for prompt testing and model comparison with CI/CD integration. |
| Bedrock | AWS managed service that hosts multiple LLMs (Claude, Titan, Llama, etc.). |
| LoRA / QLoRA | Parameter-efficient fine-tuning techniques for adapting LLMs to domains. |
