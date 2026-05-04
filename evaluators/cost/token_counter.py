"""Token counter using tiktoken for OpenAI models, approximation for others."""

try:
    import tiktoken
except ImportError:
    tiktoken = None


class TokenCounter:
    """Counts tokens for different model providers."""

    _OPENAI_MODELS = {"gpt-4o", "gpt-4o-mini", "gpt-4.1"}

    def count_tokens(self, text: str, model_id: str) -> int:
        """Count tokens in text for the given model."""
        if model_id in self._OPENAI_MODELS and tiktoken is not None:
            try:
                enc = tiktoken.encoding_for_model(model_id)
            except KeyError:
                enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        # Approximation: ~4 chars per token
        return len(text) // 4
