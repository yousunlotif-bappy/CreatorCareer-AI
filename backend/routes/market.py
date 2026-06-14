from typing import Any

from fastapi import APIRouter

from models.schemas import MarketAnalysisRequest
from routes.utils import attach_database_result, clean_optional_uuid, save_record_safely
from services.ai_service import generate_local_ai_response
from services.market_data import find_market_category, load_market_data
from services.proof import add_proof_fields


router = APIRouter(prefix="/market", tags=["Market Analysis"])


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


@router.post("/analyze")
def analyze_market_opportunity(request: MarketAnalysisRequest):
    """
    Analyze market opportunity for a creator niche, save the result,
    and return proof fields for the frontend AiProofCard.
    """

    market_data = load_market_data()
    matched_category, category_data = find_market_category(request.niche, market_data)
    platform_text = ", ".join(request.platforms)

    result = {
        "matched_category": matched_category,
        "market_summary": (
            f"Based on the {matched_category} market signal, your audience segment "
            f"({request.audience}) has estimated potential for content-led product opportunities. "
            f"Your selected platforms ({platform_text}) can be used to test demand before launching "
            f"a full product in {request.region}."
        ),
        "demand_level": category_data["demand_level"],
        "competition_level": category_data["competition_level"],
        "recommended_products": category_data["recommended_products"],
        "digital_product_ideas": category_data["digital_product_ideas"],
        "affiliate_product_ideas": category_data["affiliate_product_ideas"],
        "dropshipping_product_ideas": category_data["dropshipping_product_ideas"],
        "best_platforms": category_data["best_platforms"],
        "risk_level": category_data["risk_level"],
        "opportunity_score": category_data["opportunity_score"],
        "business_type_note": (
            f"Your selected business type is {request.business_type}. "
            f"With a {request.budget.lower()} budget, start with validation-first content before "
            f"spending on inventory, ads, or paid tools."
        ),
        "next_best_action": (
            "Start with one low-cost product idea. Create 5 short-form videos around the audience problem, "
            "run one poll, and measure saves, comments, clicks, and direct messages before launching."
        ),
        "data_note": (
            "MVP uses sample market signal data with API-ready architecture. "
            "Future versions can connect live market and social trend APIs."
        ),
    }

    ai_result = generate_local_ai_response(
        module_name="market",
        payload={
            "niche": request.niche,
            "audience": request.audience,
            "region": request.region,
            "platforms": request.platforms,
            "business_type": request.business_type,
            "budget": request.budget,
            "product_interest": request.product_interest,
        },
    )

    result.update(ai_result)

    database_payload = {
        "creator_id": clean_optional_uuid(request.creator_id),
        "niche": request.niche,
        "audience": request.audience,
        "region": request.region,
        "platforms": request.platforms,
        "business_type": request.business_type,
        "budget": request.budget,
        "product_interest": request.product_interest,
        "matched_category": result["matched_category"],
        "market_summary": result["market_summary"],
        "demand_level": result["demand_level"],
        "competition_level": result["competition_level"],
        "recommended_products": result["recommended_products"],
        "digital_product_ideas": result["digital_product_ideas"],
        "affiliate_product_ideas": result["affiliate_product_ideas"],
        "dropshipping_product_ideas": result["dropshipping_product_ideas"],
        "best_platforms": result["best_platforms"],
        "risk_level": result["risk_level"],
        "opportunity_score": result["opportunity_score"],
        "business_type_note": result["business_type_note"],
        "next_best_action": result["next_best_action"],
        "data_note": result["data_note"],
    }

    db_result = save_record_safely("market_analysis_results", database_payload)

    database_record_id = extract_database_record_id(db_result)
    database_saved = check_database_saved(db_result, database_record_id)

    response_payload = attach_database_result(result, db_result)

    return add_proof_fields(
        payload=response_payload,
        database_saved=database_saved,
        database_record_id=database_record_id,
        granite_used=True,
    )



