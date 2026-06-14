"""
AI Service Routes

This module explains and exposes the AI layer used by CreatorCareer AI.

Why this route matters:
- It gives the frontend a simple AI health-check endpoint.
- It explains how IBM Granite was used during local development.
- It honestly explains why the deployed Render version may use fallback AI logic.
- It shows that the backend is prepared for a future IBM watsonx upgrade.
- It gives judges a clear technical proof point for the AI architecture.

Honest AI disclosure:
- Local development supports IBM Granite through Ollama.
- Render deployment usually cannot run a local Ollama server by default.
- When Ollama is unavailable in production, the backend uses stable,
  explainable fallback AI/scoring logic.
- The architecture is designed to be upgraded to IBM watsonx or another
  hosted AI runtime later.

IBM Bob influence:
- IBM Bob helped inspire the project planning mindset, workflow structure,
  AI-first feature organization, and judge-friendly MVP direction.
"""

import os

from fastapi import APIRouter

from services.ai_service import get_ai_config_status
from services.proof import add_proof_fields


# All AI-related endpoints are grouped under /ai.
# Example:
# GET /ai/health
router = APIRouter(prefix="/ai", tags=["AI Service"])


def _read_bool(payload: dict, keys: list[str]) -> bool:
    """
    Safely read boolean-like values from the AI configuration payload.

    This helper makes the route more reliable because the AI config service
    may return different key names depending on the environment.

    Example supported values:
    - True / False
    - "true" / "false"
    - "yes" / "no"
    - "ok"
    - "active"
    - "available"

    If none of the provided keys are found, the function returns False.
    """

    for key in keys:
        value = payload.get(key)

        # Direct boolean value, for example: True or False
        if isinstance(value, bool):
            return value

        # String-based status value, for example: "available" or "active"
        if isinstance(value, str):
            return value.strip().lower() in {
                "true",
                "yes",
                "ok",
                "active",
                "available",
            }

    return False


@router.get("/health")
def ai_health_check():
    """
    Check the AI configuration and return an honest deployment explanation.

    This endpoint is used by the frontend dashboard/settings page to show:
    - AI service status
    - IBM Granite local testing information
    - Ollama runtime availability
    - Production fallback AI mode
    - Future watsonx readiness
    - Judge-friendly AI proof details
    """

    # Read the current AI configuration from the AI service layer.
    # This keeps the route clean and separates route logic from AI config logic.
    config_status = get_ai_config_status()

    # Detect whether the Ollama server is currently reachable.
    # Multiple key names are supported to make this endpoint flexible.
    ollama_running = _read_bool(
        config_status,
        ["ollama_running", "ollama_available", "is_ollama_running"],
    )

    # Detect whether the IBM Granite model is available inside the local runtime.
    model_available = _read_bool(
        config_status,
        ["model_available", "granite_available", "is_model_available"],
    )

    # IBM Granite is considered active only when both Ollama and the model exist.
    granite_runtime_available = ollama_running and model_available

    # Decide which AI mode the project is currently using.
    # This is important for honest deployment transparency.
    production_mode = (
        "ibm_granite_via_ollama"
        if granite_runtime_available
        else "explainable_fallback_ai"
    )

    # Main response returned to the frontend.
    # The wording is intentionally clear so judges, reviewers, and users
    # can understand the AI layer without needing to inspect the source code.
    result = {
        "status": "ok",
        "message": "CreatorCareer AI AI service health check completed.",

        # Current AI engine label used by the deployed MVP.
        "ai_engine": "local_explainable_ai",

        # Raw config status from the AI service.
        # This helps with debugging and deployment verification.
        "config": config_status,

        # IBM Granite / Ollama information.
        "local_development_model": "IBM Granite granite3.3:2b via Ollama",
        "ollama_base_url": os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ),
        "ollama_model": os.getenv("OLLAMA_MODEL", "granite3.3:2b"),

        # Production AI mode selected from the runtime status.
        "production_ai_mode": production_mode,

        # Clear deployment explanation for Render.
        "render_note": (
            "Render deployment does not run local Ollama by default, so "
            "CreatorCareer AI uses explainable fallback AI logic when Ollama "
            "is unavailable."
        ),

        # Future upgrade signal.
        "watsonx_ready": True,

        # Honest AI disclosure for judges and users.
        "honest_ai_disclosure": (
            "CreatorCareer AI supports IBM Granite through Ollama in local "
            "development. In production, the deployed MVP uses explainable "
            "fallback AI logic unless an external model service such as IBM "
            "watsonx or a hosted Ollama runtime is connected."
        ),

        # IBM Bob influence explanation.
        "ibm_bob_influence": (
            "IBM Bob helped shape the project planning mindset, feature "
            "organization, MVP workflow, and AI-first creator business system "
            "direction. The result is a structured platform that moves creators "
            "from content ideas to business strategy."
        ),

        # Judge-friendly explanation of how AI is part of the product.
        "contest_note": (
            "CreatorCareer AI uses AI as a core workflow component for creator "
            "profile analysis, content package generation, market opportunity "
            "analysis, product validation, ethical monetization checking, "
            "7-agent business planning, and PDF business reporting. IBM Granite "
            "was used locally through Ollama during development, while the "
            "deployed MVP uses stable explainable fallback logic when the local "
            "model server is not available."
        ),
    }

    # Add standard proof fields used across the backend.
    # These fields help the frontend show whether Granite was actually used
    # during this specific runtime check.
    return add_proof_fields(
        payload=result,
        database_saved=False,
        database_record_id="",
        granite_used=granite_runtime_available,
    )


