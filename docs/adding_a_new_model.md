# Adding a New Model

1. Add the model entry to `config/models.yaml`:
   ```yaml
   my-new-model:
     provider: provider_name
     endpoint: https://api.example.com/v1/chat
     context_window: 128000
     cost_per_1k_input_tokens: 0.003
     cost_per_1k_output_tokens: 0.015
   ```
2. If the provider needs a custom client, add it under `integrations/`.
3. Set the API key in `.env`.
4. Test with: `python pipelines/single_model_eval.py --model my-new-model --test-set benchmarks/mmlu/sample_questions.json`

See `CONTRIBUTING.md` for full details.
