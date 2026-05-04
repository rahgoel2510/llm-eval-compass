# Writing Domain-Specific Test Sets

1. Copy `template.json` and fill in your test cases.
2. Each test case needs: `test_case_id`, `input`, `expected_output`, `category`, `difficulty`.
3. Aim for 50+ test cases per domain task for statistical significance.
4. Include a mix of easy, medium, and hard cases.
5. Store test sets in a subfolder named after your domain (e.g., `tpm_domain/`).
6. Run with: `python pipelines/single_model_eval.py --test-set benchmarks/custom/your_domain/your_test.json`

See `tpm_domain/` for examples.
