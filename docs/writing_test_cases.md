# Writing Test Cases

1. Copy `benchmarks/custom/template.json` into a new domain folder under `benchmarks/custom/`.
2. Each test case requires: `test_case_id`, `input`, `expected_output`, `category`, `difficulty`.
3. Write at least 50 test cases for statistical significance.
4. Mix difficulty levels: ~30% easy, ~50% medium, ~20% hard.
5. Use real-world inputs from your domain — synthetic data produces misleading scores.
6. Run with: `python pipelines/single_model_eval.py --test-set benchmarks/custom/your_domain/your_test.json`

See `benchmarks/custom/tpm_domain/` for examples.
