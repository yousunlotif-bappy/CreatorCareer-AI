import json
from pathlib import Path
from typing import Any, Dict, Tuple


def load_market_data() -> Dict[str, Any]:
    """
    Load sample market signal data for the MVP.

    The file must exist here:
    backend/data/sample_market_data.json
    """

    data_path = Path(__file__).resolve().parents[1] / "data" / "sample_market_data.json"

    if not data_path.exists():
        raise FileNotFoundError(
            "sample_market_data.json was not found. "
            "Expected path: backend/data/sample_market_data.json"
        )

    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_market_category(niche: str, market_data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Match a creator niche with the closest sample market category.
    """

    niche_lower = niche.lower().strip()

    for category in market_data:
        category_lower = category.lower().strip()

        if category_lower in niche_lower or niche_lower in category_lower:
            return category, market_data[category]

    if any(keyword in niche_lower for keyword in ["money", "budget", "finance", "saving"]):
        return "personal finance", market_data["personal finance"]

    if any(keyword in niche_lower for keyword in ["fitness", "workout", "health", "gym"]):
        return "home fitness", market_data["home fitness"]

    if any(keyword in niche_lower for keyword in ["creator", "content", "youtube", "social media", "ai"]):
        return "creator education", market_data["creator education"]

    if any(keyword in niche_lower for keyword in ["beauty", "skin", "skincare", "makeup"]):
        return "beauty skincare", market_data["beauty skincare"]

    return "creator education", market_data["creator education"]



