from fastapi import APIRouter

from models.schemas import MarketAnalysisRequest
from routes.utils import attach_database_result, clean_optional_uuid, save_record_safely
from services.ai_service import generate_local_ai_response
from services.market_data import find_market_category, load_market_data


router = APIRouter(prefix="/market", tags=["Market Analysis"])


@router.post("/analyze")
def analyze_market_opportunity(request: MarketAnalysisRequest):
    """
    Analyze market opportunity for a creator niche.
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

    result.update(
        generate_local_ai_response(
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
    )

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

    return attach_database_result(result, db_result)
