from datetime import datetime, timezone
from typing import Any


def add_proof_fields(
    payload: dict[str, Any],
    database_saved: bool,
    database_record_id: str = "",
    granite_used: bool = False,
) -> dict[str, Any]:
    """
    Add proof fields to backend response so frontend AiProofCard can show
    meaningful live evidence.
    """

    payload["proof"] = {
        "ai_used": True,
        "granite_used": granite_used,
        "database_saved": database_saved,
        "database_record_id": database_record_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "CreatorCareer AI backend",
    }

    return payload


