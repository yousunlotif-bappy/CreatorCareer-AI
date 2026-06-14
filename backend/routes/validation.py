from fastapi import APIRouter

from models.schemas import ProductValidationRequest
from routes.utils import (
    attach_database_result,
    clean_optional_uuid,
    get_database_proof_values,
    save_record_safely,
)
from services.ai_service import generate_local_ai_response
from services.proof import add_proof_fields


router = APIRouter(prefix="/product", tags=["Product Validation"])


def calculate_product_validation_scores(request: ProductValidationRequest) -> dict:
    """
    Calculate product validation score for the MVP.
    """

    niche = request.niche.lower()
    product = request.product_name.lower()
    business_model = request.business_model.lower()
    product_type = request.product_type.lower()
    budget = request.budget.lower()
    platform = request.platform.lower()
    promotion_style = request.promotion_style.lower()

    audience_fit = 14
    market_demand = 11
    competition = 9
    content_promotion_fit = 12
    profit_potential = 6
    ease_of_starting = 6

    if any(word in product for word in niche.split() if len(word) > 3):
        audience_fit += 5

    if any(
        item in product
        for item in ["template", "planner", "guide", "tracker", "workbook"]
    ):
        audience_fit += 4

    if any(item in product for item in ["course", "toolkit", "membership"]):
        audience_fit += 3

    if any(
        item in niche
        for item in [
            "finance",
            "fitness",
            "beauty",
            "creator",
            "ai",
            "productivity",
            "skincare",
            "business",
        ]
    ):
        market_demand += 5

    if "digital" in business_model or "affiliate" in business_model:
        market_demand += 3

    if "template" in product_type or "course" in product_type:
        market_demand += 1

    if "low" in budget and any(
        item in product_type for item in ["digital", "template", "guide"]
    ):
        competition += 3

    if "dropshipping" in business_model:
        competition -= 2

    if "high" in budget:
        competition += 1

    if any(
        item in platform
        for item in ["tiktok", "instagram", "youtube", "shorts", "reels"]
    ):
        content_promotion_fit += 4

    if any(
        item in product
        for item in ["planner", "template", "guide", "toolkit", "checklist"]
    ):
        content_promotion_fit += 4

    if any(
        item in promotion_style
        for item in ["educational", "short-form", "tutorial", "story"]
    ):
        content_promotion_fit += 2

    if "digital" in business_model:
        profit_potential += 2

    if "affiliate" in business_model:
        profit_potential += 1

    if any(item in product for item in ["course", "toolkit", "template"]):
        profit_potential += 1

    if "low" in budget:
        ease_of_starting += 2

    if any(
        item in product_type
        for item in ["digital", "template", "guide", "workbook"]
    ):
        ease_of_starting += 2

    if "dropshipping" in business_model:
        ease_of_starting -= 1

    audience_fit = min(audience_fit, 25)
    market_demand = min(market_demand, 20)
    competition = max(0, min(competition, 15))
    content_promotion_fit = min(content_promotion_fit, 20)
    profit_potential = min(profit_potential, 10)
    ease_of_starting = max(0, min(ease_of_starting, 10))

    total = (
        audience_fit
        + market_demand
        + competition
        + content_promotion_fit
        + profit_potential
        + ease_of_starting
    )

    return {
        "audience_fit_score": audience_fit,
        "market_demand_score": market_demand,
        "competition_score": competition,
        "content_promotion_fit_score": content_promotion_fit,
        "profit_potential_score": profit_potential,
        "ease_of_starting_score": ease_of_starting,
        "total_score": total,
    }


def get_validation_status(score: int) -> str:
    """
    Convert total validation score into a human-readable status.
    """

    if score >= 85:
        return "Strong Launch-Test Opportunity"

    if score >= 70:
        return "Good Opportunity - Validate First"

    if score >= 55:
        return "Moderate Opportunity - Needs More Research"

    return "Risky Idea - Improve Before Testing"


@router.post("/validate")
def validate_product(request: ProductValidationRequest):
    """
    Validate a product idea, add local AI reasoning, save the result,
    and return proof fields for the frontend AiProofCard.
    """

    scores = calculate_product_validation_scores(request)
    total_score = scores["total_score"]
    status = get_validation_status(total_score)

    if total_score >= 85:
        recommendation = (
            "This product idea has strong validation potential. Start with a small MVP "
            "and test it through short-form content."
        )
    elif total_score >= 70:
        recommendation = (
            "This product idea looks promising, but it should be validated first using "
            "polls, comments, waitlists, and content tests."
        )
    elif total_score >= 55:
        recommendation = (
            "This idea may work, but the positioning needs improvement before testing."
        )
    else:
        recommendation = (
            "This idea is currently risky. Improve audience fit, simplify the offer, "
            "or choose a product that fits your niche better."
        )

    strengths = [
        "Product can be tested through content before major spending.",
        "Creator audience can be used for early validation.",
        "Short-form platforms can help test demand quickly.",
    ]

    risks = [
        "Score is an estimate, not a guarantee of sales.",
        "Audience interest should be validated before launch.",
        "Competition and pricing should be checked before investing.",
    ]

    validation_checklist = [
        "Define the exact audience problem this product solves.",
        "Create 5 content posts around the problem before launch.",
        "Run one poll or comment-based validation test.",
        "Check competitor pricing and product positioning.",
        "Prepare ethical disclosure if affiliate links are used.",
        "Start with a small MVP before building the full product.",
    ]

    result = {
        "product_name": request.product_name,
        "status": status,
        "total_score": total_score,
        "score_breakdown": scores,
        "recommendation": recommendation,
        "strengths": strengths,
        "risks": risks,
        "validation_checklist": validation_checklist,
        "next_best_action": (
            f"Create 5 short-form videos about the problem behind '{request.product_name}', "
            "then measure saves, comments, clicks, and direct messages to validate demand."
        ),
        "data_note": (
            "This MVP score uses rule-based validation logic and can later connect to live APIs."
        ),
    }

    ai_result = generate_local_ai_response(
        module_name="product",
        payload={
            "product_name": request.product_name,
            "niche": request.niche,
            "audience": request.audience,
            "region": request.region,
            "platform": request.platform,
            "business_model": request.business_model,
            "budget": request.budget,
            "product_type": request.product_type,
            "promotion_style": request.promotion_style,
        },
    )

    result.update(ai_result)

    database_payload = {
        "creator_id": clean_optional_uuid(request.creator_id),
        "product_name": request.product_name,
        "niche": request.niche,
        "audience": request.audience,
        "region": request.region,
        "platform": request.platform,
        "business_model": request.business_model,
        "budget": request.budget,
        "product_type": request.product_type,
        "promotion_style": request.promotion_style,
        "audience_fit_score": scores["audience_fit_score"],
        "market_demand_score": scores["market_demand_score"],
        "competition_score": scores["competition_score"],
        "content_promotion_fit_score": scores["content_promotion_fit_score"],
        "profit_potential_score": scores["profit_potential_score"],
        "ease_of_starting_score": scores["ease_of_starting_score"],
        "total_score": total_score,
        "status": status,
        "recommendation": recommendation,
        "strengths": strengths,
        "risks": risks,
        "validation_checklist": validation_checklist,
        "next_best_action": result["next_best_action"],
        "data_note": result["data_note"],
    }

    db_result = save_record_safely("product_scores", database_payload)

    response_payload = attach_database_result(result, db_result)
    proof_values = get_database_proof_values(db_result)

    return add_proof_fields(
        payload=response_payload,
        database_saved=proof_values["database_saved"],
        database_record_id=proof_values["database_record_id"],
        granite_used=True,
    )



