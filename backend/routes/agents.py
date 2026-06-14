from typing import Any

from fastapi import APIRouter

from models.schemas import SevenAgentRequest
from routes.utils import attach_database_result, clean_optional_uuid, save_record_safely
from services.ai_service import generate_local_ai_response
from services.proof import add_proof_fields


router = APIRouter(prefix="/agents", tags=["7-Agent Dashboard"])


def clamp_score(score: int) -> int:
    return max(0, min(score, 100))


def get_agent_status(score: int) -> str:
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Strong"
    if score >= 55:
        return "Moderate"
    return "Needs Improvement"


def build_agent_result(
    agent_name: str,
    score: int,
    reason: str,
    recommendation: str,
    next_action: str,
    extra_output: dict | None = None,
) -> dict:
    safe_score = clamp_score(score)

    result = {
        "agent_name": agent_name,
        "score": safe_score,
        "status": get_agent_status(safe_score),
        "reason": reason,
        "recommendation": recommendation,
        "next_action": next_action,
    }

    if extra_output:
        result.update(extra_output)

    return result


def extract_database_record_id(db_result: Any) -> str:
    """
    Safely extract database record id from common Supabase response shapes.
    This prevents undefined record_id errors.
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


def business_readiness_agent(request: SevenAgentRequest) -> dict:
    score = 45

    if request.followers >= 1000:
        score += 10
    if request.followers >= 10000:
        score += 10
    if len(request.platforms) >= 2:
        score += 10
    if "digital" in request.business_model.lower():
        score += 8
    if "affiliate" in request.business_model.lower():
        score += 7
    if "hour" in request.available_time.lower():
        score += 5

    return build_agent_result(
        "Creator Business Readiness",
        score,
        "This score estimates how ready the creator is to move from content creation into a structured digital business.",
        "Focus on one clear offer and validate demand before building a complex product.",
        "Create a simple creator business profile and choose one product idea to test this week.",
    )


def niche_product_fit_agent(request: SevenAgentRequest) -> dict:
    score = 60
    niche = request.creator_niche.lower()
    product = request.product_idea.lower()

    for word in niche.split():
        if len(word) > 3 and word in product:
            score += 12

    if any(
        item in product
        for item in ["template", "planner", "guide", "toolkit", "course"]
    ):
        score += 12

    if "digital" in request.business_model.lower():
        score += 8

    return build_agent_result(
        "Niche-to-Product Fit",
        score,
        "This score checks whether the product idea naturally connects with the creator niche.",
        "Choose products that solve a clear audience problem and can be promoted through educational content.",
        "Write one sentence explaining exactly why your audience needs this product.",
    )


def audience_market_match_agent(request: SevenAgentRequest) -> dict:
    score = 58
    niche = request.creator_niche.lower()
    product = request.product_idea.lower()
    audience = request.audience.lower()
    region = request.region.lower()

    if any(
        item in niche
        for item in [
            "finance",
            "fitness",
            "beauty",
            "creator",
            "ai",
            "productivity",
            "marketing",
            "business",
        ]
    ):
        score += 15

    if any(
        item in product
        for item in ["planner", "template", "tool", "guide", "kit", "course"]
    ):
        score += 10

    if "usa" in audience or "united states" in region:
        score += 8

    if len(request.platforms) >= 3:
        score += 5

    return build_agent_result(
        "Audience-to-Market Matching",
        score,
        "This score estimates how well the audience, region, product idea, and platform mix match a market opportunity.",
        "Use content to test buying interest before spending on ads, inventory, or complex funnels.",
        "Run one audience poll and publish 3 product-related short videos to measure interest.",
    )


def content_commerce_roadmap_agent(request: SevenAgentRequest) -> dict:
    roadmap_steps = [
        "Step 1: Identify the audience problem behind the product.",
        "Step 2: Create awareness content that explains the problem.",
        "Step 3: Build trust with educational short-form content.",
        "Step 4: Introduce the product as one possible solution.",
        "Step 5: Add transparent disclosure and a simple CTA.",
        "Step 6: Track saves, comments, clicks, and direct messages.",
    ]

    return build_agent_result(
        "Content-to-Commerce Roadmap",
        82,
        "The content-to-commerce path is strong when the creator can educate the audience, build trust, and track response.",
        "Build a simple funnel: awareness content, trust content, product mention, ethical CTA, and validation tracking.",
        "Create 5 short-form videos: 2 problem-aware, 2 educational, and 1 soft product introduction.",
        {"roadmap_steps": roadmap_steps},
    )


def ethical_monetization_agent(request: SevenAgentRequest) -> dict:
    text = request.promotion_copy.lower()
    business_model = request.business_model.lower()
    score = 100
    issues = []

    has_disclosure = any(
        keyword in text
        for keyword in [
            "affiliate",
            "commission",
            "sponsored",
            "paid partnership",
            "ad",
        ]
    )

    if "affiliate" in business_model and not has_disclosure:
        score -= 20
        issues.append("Affiliate or sponsorship disclosure may be missing.")

    if any(
        phrase in text
        for phrase in [
            "guaranteed",
            "make you rich",
            "instant results",
            "100%",
            "no risk",
            "rich fast",
        ]
    ):
        score -= 25
        issues.append("Promotion copy may contain overpromising or risky claim language.")

    if any(
        phrase in text
        for phrase in ["buy now or regret", "last chance", "only today", "act now"]
    ):
        score -= 10
        issues.append("Promotion copy may contain pressure-based urgency.")

    if not issues:
        issues.append("No major ethical risk detected in this MVP check.")

    return build_agent_result(
        "Ethical Monetization Checker",
        score,
        "This agent checks whether promotional content is transparent and avoids overpromising.",
        "Use clear affiliate disclosure, avoid guaranteed results, and explain limitations honestly.",
        "Rewrite the promotion copy using safer, clearer claims.",
        {
            "issues_found": issues,
            "recommended_disclosure": (
                "This content may contain affiliate links. If you buy through my link, "
                "I may earn a small commission at no extra cost to you."
            ),
        },
    )


def product_validation_checklist_agent(request: SevenAgentRequest) -> dict:
    score = 78
    product = request.product_idea.lower()

    if "template" in product or "planner" in product:
        score += 8

    if "digital" in request.business_model.lower():
        score += 4

    checklist = [
        "Audience problem is clearly defined.",
        "Product solves one specific problem.",
        "Product can be explained in short-form content.",
        "Low-cost test is possible.",
        "Audience poll or comment test is planned.",
        "Competitor pricing is checked.",
        "Ethical disclosure is ready if affiliate links are used.",
    ]

    return build_agent_result(
        "Product Validation Checklist",
        score,
        "This agent checks whether the product can be validated before full launch.",
        "Validate demand before building the full product. Start with a small MVP or simple offer.",
        "Create a validation checklist and complete it before launch.",
        {"checklist": checklist},
    )


def six_month_roadmap_agent(request: SevenAgentRequest) -> dict:
    roadmap = [
        "Month 1: Clarify niche, audience problem, and content pillars.",
        "Month 2: Publish 20-30 short-form videos and test product-related topics.",
        "Month 3: Validate one product idea using comments, polls, and a waitlist.",
        "Month 4: Launch a small MVP product, affiliate offer, or digital template.",
        "Month 5: Improve offer based on real audience response and conversion data.",
        "Month 6: Scale through collaborations, email list, partnerships, and better content funnels.",
    ]

    return build_agent_result(
        "6-Month Creator-to-Business Roadmap",
        84,
        "A six-month roadmap helps the creator move from random content creation into a structured business-building process.",
        "Follow a validation-first roadmap: clarify niche, test content, validate product, launch small, improve, then scale.",
        "Start Month 1 by defining content pillars and testing audience pain points.",
        {"roadmap": roadmap},
    )


@router.post("/run")
def run_seven_agent_dashboard(request: SevenAgentRequest):
    """
    Run all seven creator business agents, add local AI reasoning,
    save the unified report, and return proof fields for the frontend.
    """

    agent_results = [
        business_readiness_agent(request),
        niche_product_fit_agent(request),
        audience_market_match_agent(request),
        content_commerce_roadmap_agent(request),
        ethical_monetization_agent(request),
        product_validation_checklist_agent(request),
        six_month_roadmap_agent(request),
    ]

    overall_score = round(
        agent_results[0]["score"] * 0.20
        + agent_results[1]["score"] * 0.20
        + agent_results[2]["score"] * 0.20
        + agent_results[3]["score"] * 0.15
        + agent_results[5]["score"] * 0.15
        + agent_results[4]["score"] * 0.10
    )

    result = {
        "overall_business_opportunity_score": overall_score,
        "executive_summary": (
            f"CreatorCareer AI analyzed your {request.creator_niche} creator business idea for "
            f"{request.audience}. Your product idea, '{request.product_idea}', shows an estimated "
            f"overall business opportunity score of {overall_score}/100."
        ),
        "agent_results": agent_results,
        "next_7_days_plan": [
            "Day 1: Define the exact audience problem your product solves.",
            "Day 2: Create 3 short-form content hooks around that problem.",
            "Day 3: Publish one educational video and ask for audience feedback.",
            "Day 4: Run a poll or comment-based validation test.",
            "Day 5: Draft the first MVP version of the product or affiliate offer.",
            "Day 6: Add clear disclosure and prepare a simple CTA.",
            "Day 7: Review engagement signals and decide whether to continue, adjust, or pause.",
        ],
        "score_weights": {
            "business_readiness": "20%",
            "niche_product_fit": "20%",
            "audience_market_match": "20%",
            "content_to_commerce": "15%",
            "product_validation": "15%",
            "ethical_safety": "10%",
        },
        "data_note": "MVP uses rule-based agent logic and sample market signals.",
    }

    ai_result = generate_local_ai_response(
        module_name="agents",
        payload={
            "creator_niche": request.creator_niche,
            "audience": request.audience,
            "region": request.region,
            "platforms": request.platforms,
            "followers": request.followers,
            "product_idea": request.product_idea,
            "business_model": request.business_model,
            "income_goal": request.income_goal,
            "available_time": request.available_time,
            "promotion_copy": request.promotion_copy,
        },
    )

    result.update(ai_result)

    database_payload = {
        "creator_id": clean_optional_uuid(request.creator_id),
        "creator_niche": request.creator_niche,
        "audience": request.audience,
        "region": request.region,
        "platforms": request.platforms,
        "followers": request.followers,
        "product_idea": request.product_idea,
        "business_model": request.business_model,
        "income_goal": request.income_goal,
        "available_time": request.available_time,
        "promotion_copy": request.promotion_copy,
        "overall_business_opportunity_score": result[
            "overall_business_opportunity_score"
        ],
        "executive_summary": result["executive_summary"],
        "agent_results": result["agent_results"],
        "next_7_days_plan": result["next_7_days_plan"],
        "score_weights": result["score_weights"],
        "data_note": result["data_note"],
    }

    db_result = save_record_safely("seven_agent_reports", database_payload)

    database_record_id = extract_database_record_id(db_result)
    database_saved = check_database_saved(db_result, database_record_id)

    response_payload = attach_database_result(result, db_result)

    return add_proof_fields(
        payload=response_payload,
        database_saved=database_saved,
        database_record_id=database_record_id,
        granite_used=True,
    )

