"""Thin wrapper around the RAG backend REST API.

The backend URL is read from the environment (frontend/.env) — it is never
hard-coded in the app.
"""
import os
from pathlib import Path
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Load frontend/.env regardless of the current working directory
load_dotenv(Path(__file__).resolve().parent / ".env")

API_BASE_URL = os.getenv("API_BASE_URL")

HEALTH_TIMEOUT = 3   # seconds
QUERY_TIMEOUT = 60   # seconds — LLM generation can take a while


class ConfigurationError(RuntimeError):
    """API_BASE_URL is not set in the environment / .env."""


class BackendError(Exception):
    """The backend answered with a non-200 status code."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Backend returned HTTP {status_code}: {detail}")


class BackendUnavailableError(Exception):
    """Could not connect to the backend at all."""


class BackendTimeoutError(Exception):
    """The backend took too long to respond."""


def _base_url() -> str:
    if not API_BASE_URL:
        raise ConfigurationError(
            "API_BASE_URL is not set. Copy frontend/.env.example to frontend/.env "
            "and set API_BASE_URL=http://localhost:8000"
        )
    return API_BASE_URL.rstrip("/")


def check_backend_health() -> bool:
    """Return True when GET /health responds 200."""
    try:
        response = requests.get(f"{_base_url()}/health", timeout=HEALTH_TIMEOUT)
        return response.status_code == 200
    except (requests.RequestException, ConfigurationError):
        return False


def ask_question(question: str) -> Dict[str, Any]:
    """POST /query and return {'answer': str, 'sources': list[str]}."""
    try:
        response = requests.post(
            f"{_base_url()}/query",
            json={"question": question},
            timeout=QUERY_TIMEOUT,
        )
    except requests.exceptions.ConnectionError as exc:
        raise BackendUnavailableError(str(exc)) from exc
    except requests.exceptions.Timeout as exc:
        raise BackendTimeoutError(str(exc)) from exc

    if response.status_code == 200:
        return response.json()

    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    raise BackendError(response.status_code, detail)