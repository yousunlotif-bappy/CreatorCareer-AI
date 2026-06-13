"""
AI Service Routes

Checks the IBM Granite local AI layer through Ollama + LangChain.
"""

from fastapi import APIRouter

from services.ai_service import get_ai_config_status


router = APIRouter(prefix="/ai", tags=["AI Service"])


@router.get("/health")
def ai_health_check():
    """
    Check local Granite/LangChain AI configuration.
    """

    return {
        "status": "ok",
        "message": "CreatorCareer AI local Granite/LangChain AI layer is available.",
        "config": get_ai_config_status(),
        "contest_note": (
            "CreatorCareer AI uses IBM Granite open-source model locally through Ollama "
            "with LangChain integration. This does not require watsonx billing or external API keys. "
            "watsonx is kept as a future-ready deployment path."
        ),
    }


