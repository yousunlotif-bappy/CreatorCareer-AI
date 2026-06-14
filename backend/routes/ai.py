"""
AI Service Routes

Checks the IBM Granite local AI layer through Ollama + LangChain.
This route also returns proof fields so the frontend can show meaningful
AI system evidence.
"""

from fastapi import APIRouter

from services.ai_service import get_ai_config_status
from services.proof import add_proof_fields


router = APIRouter(prefix="/ai", tags=["AI Service"])


@router.get("/health")
def ai_health_check():
    """
    Check local Granite/LangChain AI configuration.
    """

    config_status = get_ai_config_status()

    result = {
        "status": "ok",
        "message": "CreatorCareer AI local Granite/LangChain AI layer is available.",
        "config": config_status,
        "contest_note": (
            "CreatorCareer AI uses IBM Granite open-source model locally through Ollama "
            "with LangChain integration. This does not require watsonx billing or external API keys. "
            "watsonx is kept as a future-ready deployment path."
        ),
    }

    return add_proof_fields(
        payload=result,
        database_saved=False,
        database_record_id="",
        granite_used=True,
    )


