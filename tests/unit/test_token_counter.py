from evaluators.cost.token_counter import TokenCounter


def test_token_count_approximation():
    counter = TokenCounter()
    text = "a" * 100
    assert counter.count_tokens(text, "claude-sonnet-4-6") == 100 // 4
