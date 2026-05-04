"""Unified model connector layer.

Usage:
    from connectors import create_connector
    conn = create_connector("gpt-4o", api_key="sk-...")
    response = conn.generate("Summarize this meeting.")
"""

from connectors.base import BaseConnector, ModelResponse
from connectors.factory import create_connector

__all__ = ["BaseConnector", "ModelResponse", "create_connector"]
