from typing import Any

from fastapi import APIRouter

from models.schemas import CreatorProfileRequest
from routes.utils import attach_database_result, save_record_safely
from services.proof import add_proof_fields


router = APIRouter(prefix="/profile", tags=["Profile"])


def extract_database_record_id(db_result: Any) -> str:
    """
    Safely extract database record id from common Supabase response shapes.
    """

    try:
        if not db_result:
            return ""

        if isinstance(db_result, dict):
            if db_result.get("id"):
                return str(db_result["id"])

            data = db_result.get("data")

            if isinstance(data, list) and len(data) > 0:
                first_item = data[0]

                if isinstance(first_item, dict) and first_item.get("id"):
                    return str(first_item["id"])

            if isinstance(data, dict) and data.get("id"):
                return str(data["id"])

            record = db_result.get("record")

            if isinstance(record, dict) and record.get("id"):
                return str(record["id"])

        data = getattr(db_result, "data", None)

        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]

            if isinstance(first_item, dict) and first_item.get("id"):
                return str(first_item["id"])

        if isinstance(data, dict) and data.get("id"):
            return str(data["id"])

        record_id = getattr(db_result, "id", None)

        if record_id:
            return str(record_id)

        return ""

    except Exception:
        return ""


def check_database_saved(db_result: Any, database_record_id: str) -> bool:
    """
    Check whether database save was successful.
    """

    if database_record_id:
        return True

    if not db_result:
        return False

    if isinstance(db_result, dict):
        if db_result.get("success") is True:
            return True

        if db_result.get("saved") is True:
            return True

        if db_result.get("error"):
            return False

        if db_result.get("data"):
            return True

    data = getattr(db_result, "data", None)

    if data:
        return True

    return False


def calculate_readiness_score(profile: CreatorProfileRequest) -> int:
    """
    Calculate a simple creator business readiness score.
    """

    score = 40

    if profile.followers >= 1000:
        score += 10

    if profile.followers >= 10000:
        score += 10

    if profile.followers >= 50000:
        score += 5

    if len(profile.platforms) >= 2:
        score += 10

    if len(profile.platforms) >= 4:
        score += 5

    business_interest = profile.business_interest.lower()

    if "affiliate" in business_interest:
        score += 8

    if "digital" in business_interest:
        score += 8

    if "product" in business_interest:
        score += 7

    if "dropshipping" in business_interest:
        score += 5

    if len(profile.skills) > 20:
        score += 7

    return min(score, 100)


def get_creator_stage(followers: int) -> str:
    """
    Convert follower count into a creator stage label.
    """

    if followers < 1000:
        return "Early-stage Creator"

    if followers < 10000:
        return "Growing Creator"

    if followers < 50000:
        return "Monetization-ready Creator"

    return "Established Creator"


@router.post("/analyze")
def analyze_creator_profile(profile: CreatorProfileRequest):
    """
    Analyze a creator profile, save it to the creators table,
    and return proof fields for the frontend AiProofCard.
    """

    readiness_score = calculate_readiness_score(profile)
    creator_stage = get_creator_stage(profile.followers)
    platform_text = ", ".join(profile.platforms)

    result = {
        "creator_summary": (
            f"You are a {creator_stage.lower()} in the {profile.niche} niche, "
            f"creating content for {profile.audience} across {platform_text}."
        ),
        "creator_stage": creator_stage,
        "niche_positioning": (
            f"Your strongest positioning is to become a trusted creator in {profile.niche}. "
            f"Your content should focus on practical, useful, and audience-friendly solutions "
            f"for people in {profile.region}."
        ),
        "audience_opportunity": (
            "Your audience has potential for educational, problem-solving, and product-driven content. "
            "This can support digital products, affiliate recommendations, dropshipping ideas, "
            "or creator-led services when trust is built properly."
        ),
        "business_opportunity": (
            f"Based on your interest in {profile.business_interest}, your best path is to connect "
            "your content with useful offers, simple products, transparent monetization, and a clear "
            "content-to-commerce roadmap."
        ),
        "business_readiness_score": readiness_score,
        "recommended_next_modules": [
            "AI Content Package Generator",
            "AI Market Analysis",
            "Product Validation Score",
            "Affiliate & Dropshipping Roadmap",
            "Ethical Monetization Checker",
            "7-Agent Creator Business Dashboard",
            "PDF Business Report Generator",
        ],
        "next_best_action": (
            "Create 5 content ideas around your audience's biggest problem. Then validate one product "
            "idea using comments, polls, short-form video engagement, and audience questions."
        ),
    }

    database_payload = {
        "name": profile.name,
        "niche": profile.niche,
        "platforms": profile.platforms,
        "followers": profile.followers,
        "audience": profile.audience,
        "region": profile.region,
        "skills": profile.skills,
        "business_interest": profile.business_interest,
        "income_goal": profile.income_goal,
        "available_time": profile.available_time,
        "current_challenge": profile.current_challenge,
        "readiness_score": readiness_score,
        "creator_stage": creator_stage,
    }

    db_result = save_record_safely("creators", database_payload)

    database_record_id = extract_database_record_id(db_result)
    database_saved = check_database_saved(db_result, database_record_id)

    response_payload = attach_database_result(result, db_result)

    return add_proof_fields(
        payload=response_payload,
        database_saved=database_saved,
        database_record_id=database_record_id,
        granite_used=False,
    )



