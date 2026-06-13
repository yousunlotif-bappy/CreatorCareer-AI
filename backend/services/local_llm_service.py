"""
Local LLM Service

This service connects CreatorCareer AI with IBM Granite running locally
through Ollama and LangChain.

Important:
- No watsonx billing is required.
- No IBM Cloud API key is required.
- If Ollama or LangChain is unavailable, the app safely falls back.
"""

import json
import os
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


def is_ollama_enabled() -> bool:
    """
    Check whether local Ollama integration is enabled.
    """

    return os.getenv("OLLAMA_ENABLED", "true").strip().lower() in {
        "true",
        "1",
        "yes",
        "on",
    }


def get_ollama_base_url() -> str:
    """
    Return the local Ollama API base URL.
    """

    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")


def get_ollama_model() -> str:
    """
    Return the selected local IBM Granite model name.
    """

    return os.getenv("OLLAMA_MODEL", "granite3.3:2b")


def _extract_model_names(raw_payload: str) -> List[str]:
    """
    Extract installed model names from Ollama /api/tags response.
    """

    try:
        parsed = json.loads(raw_payload)
        return [item.get("name", "") for item in parsed.get("models", []) if item.get("name")]
    except Exception:
        return []


def check_ollama_server() -> Dict[str, Any]:
    """
    Check if Ollama local server is running and whether the selected model exists.
    """

    base_url = get_ollama_base_url()
    model_name = get_ollama_model()
    tags_url = f"{base_url}/api/tags"

    if not is_ollama_enabled():
        return {
            "ollama_enabled": False,
            "ollama_running": False,
            "ollama_model": model_name,
            "model_available": False,
            "available_models": [],
            "error": "OLLAMA_ENABLED=false",
        }

    try:
        with urllib.request.urlopen(tags_url, timeout=5) as response:
            raw_data = response.read().decode("utf-8")

        available_models = _extract_model_names(raw_data)

        return {
            "ollama_enabled": True,
            "ollama_running": True,
            "ollama_model": model_name,
            "model_available": model_name in available_models,
            "available_models": available_models,
            "error": None,
        }

    except Exception as error:
        return {
            "ollama_enabled": True,
            "ollama_running": False,
            "ollama_model": model_name,
            "model_available": False,
            "available_models": [],
            "error": str(error),
        }


def generate_with_granite(prompt: str) -> Dict[str, Any]:
    """
    Generate a response using IBM Granite local model through LangChain + Ollama.

    This function never raises route-breaking errors.
    Any failure returns success=False so the caller can use fallback logic.
    """

    model_name = get_ollama_model()

    if not is_ollama_enabled():
        return {
            "success": False,
            "text": "",
            "provider": "CreatorCareer Local Fallback Engine",
            "model": model_name,
            "error": "OLLAMA_ENABLED=false",
        }

    try:
        from langchain_ollama import ChatOllama

        llm = ChatOllama(
            model=model_name,
            base_url=get_ollama_base_url(),
            temperature=0.2,
        )

        response = llm.invoke(prompt)

        return {
            "success": True,
            "text": response.content,
            "provider": "IBM Granite via Ollama + LangChain",
            "model": model_name,
            "error": None,
        }

    except Exception as error:
        return {
            "success": False,
            "text": "",
            "provider": "CreatorCareer Local Fallback Engine",
            "model": model_name,
            "error": str(error),
        }



