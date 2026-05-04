"""EU AI Act risk classifier."""

_HIGH_RISK_KEYWORDS = {"medical", "healthcare", "legal", "hiring", "recruitment", "credit", "law enforcement", "biometric"}
_UNACCEPTABLE_KEYWORDS = {"social scoring", "mass surveillance", "subliminal manipulation"}
_LIMITED_KEYWORDS = {"chatbot", "deepfake", "emotion recognition"}


class AIActClassifier:
    """Classifies use cases by EU AI Act risk level."""

    def classify(self, use_case: str) -> dict:
        """Classify a use case into EU AI Act risk categories."""
        lower = use_case.lower()
        if any(kw in lower for kw in _UNACCEPTABLE_KEYWORDS):
            level = "unacceptable"
        elif any(kw in lower for kw in _HIGH_RISK_KEYWORDS):
            level = "high"
        elif any(kw in lower for kw in _LIMITED_KEYWORDS):
            level = "limited"
        else:
            level = "minimal"
        return {"use_case": use_case, "risk_level": level}
