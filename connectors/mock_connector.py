"""Mock connector for demo mode — no API keys needed."""

from __future__ import annotations

import random
import time

from connectors.base import BaseConnector, ModelResponse

# Simulated responses keyed by partial input match.
# Falls back to a generic paraphrase if no match found.
_CANNED: dict[str, str] = {
    "API migration": (
        "Action items: 1) John: Complete API migration by Friday. "
        "2) Sarah: Resolve auth integration blocker with DevOps support. "
        "3) Mike: Deliver staging environment by Wednesday."
    ),
    "Q3 budget": (
        "Summary: Q3 budget discussion — no final decision. Lisa proposed 20% ML platform "
        "cut to fund hiring. Tom opposed, citing model training needs. "
        "Next step: Revisit after cost analysis next week."
    ),
    "Sprint retro": (
        "Retro summary — Positive: Deployment pipeline cut release time from 4hrs to 45min. "
        "Negative: 3 P1 incidents from missing integration tests. "
        "Actions: 1) QA lead: Add integration test gate to CI next sprint. "
        "2) PM: Schedule incident review Thursday."
    ),
    "risk": (
        "Risks identified: 1) Vendor lock-in with single cloud provider — medium severity. "
        "2) Data pipeline SLA breach risk due to growing volume — high severity. "
        "Mitigation: Evaluate multi-cloud strategy; add autoscaling to pipeline."
    ),
    "status update": (
        "Executive Summary: Project is on track for Q3 delivery. Backend API at 80% completion. "
        "Frontend redesign started this sprint. Key risk: third-party auth integration delayed. "
        "Budget utilization: 62% of allocated spend."
    ),
}

# Per-model personality: (quality_factor, speed_factor_ms, token_overhead)
_MODEL_PROFILES: dict[str, tuple[float, float, float]] = {
    "demo-claude-sonnet":  (0.95, 800, 1.0),
    "demo-gpt-4o":         (0.92, 950, 1.1),
    "demo-gemini-flash":   (0.85, 400, 0.9),
    "demo-mistral-large":  (0.88, 600, 1.0),
}


def _find_canned(prompt: str) -> str | None:
    for key, response in _CANNED.items():
        if key.lower() in prompt.lower():
            return response
    return None


def _generic_response(prompt: str) -> str:
    words = prompt.split()
    n = min(len(words), 40)
    return "Based on the input: " + " ".join(words[:n]) + "... [summarized output]"


class MockConnector(BaseConnector):
    """Simulates a model with realistic latency, token counts, and varied quality."""

    @property
    def provider(self) -> str:
        return "Demo"

    def _call(self, prompt: str, **kwargs) -> ModelResponse:
        quality, base_latency, tok_factor = _MODEL_PROFILES.get(
            self.model_id, (0.90, 700, 1.0)
        )

        # Pick response
        canned = _find_canned(prompt)
        if canned and random.random() < quality:
            text = canned
        elif canned:
            # Slightly degrade the canned response to simulate lower quality
            words = canned.split()
            drop = max(1, int(len(words) * (1 - quality) * 2))
            text = " ".join(words[:-drop]) + "..."
        else:
            text = _generic_response(prompt)

        # Simulate latency
        jitter = random.uniform(0.7, 1.4)
        sleep_s = (base_latency * jitter) / 1000
        time.sleep(sleep_s)

        # Simulate token counts
        input_tokens = int(len(prompt.split()) * 1.3)
        output_tokens = int(len(text.split()) * 1.3 * tok_factor)

        return ModelResponse(
            text=text,
            model_id=self.model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    def test_connection(self) -> bool:
        return True


# The demo models available
DEMO_MODELS: dict[str, dict] = {
    "demo-claude-sonnet": {
        "provider": "Demo",
        "model_id": "demo-claude-sonnet",
        "display_name": "🎭 Demo: Claude Sonnet",
        "context_window": 200_000,
        "input_cost_per_1k_tokens": 0.003,
        "output_cost_per_1k_tokens": 0.015,
        "endpoint_type": "demo",
    },
    "demo-gpt-4o": {
        "provider": "Demo",
        "model_id": "demo-gpt-4o",
        "display_name": "🎭 Demo: GPT-4o",
        "context_window": 128_000,
        "input_cost_per_1k_tokens": 0.0025,
        "output_cost_per_1k_tokens": 0.01,
        "endpoint_type": "demo",
    },
    "demo-gemini-flash": {
        "provider": "Demo",
        "model_id": "demo-gemini-flash",
        "display_name": "🎭 Demo: Gemini Flash",
        "context_window": 1_000_000,
        "input_cost_per_1k_tokens": 0.00015,
        "output_cost_per_1k_tokens": 0.0035,
        "endpoint_type": "demo",
    },
    "demo-mistral-large": {
        "provider": "Demo",
        "model_id": "demo-mistral-large",
        "display_name": "🎭 Demo: Mistral Large",
        "context_window": 128_000,
        "input_cost_per_1k_tokens": 0.002,
        "output_cost_per_1k_tokens": 0.006,
        "endpoint_type": "demo",
    },
}
