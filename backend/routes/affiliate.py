from fastapi import APIRouter

from models.schemas import AffiliateRoadmapRequest
from routes.utils import attach_database_result, clean_optional_uuid, save_record_safely
from services.ai_service import generate_local_ai_response
from services.proof import add_proof_fields


router = APIRouter(prefix="/affiliate", tags=["Affiliate Roadmap"])


def get_affiliate_dropshipping_ideas(niche: str) -> dict:
    """
    Return MVP affiliate and dropshipping ideas based on creator niche.
    """

    niche_lower = niche.lower()

    if any(keyword in niche_lower for keyword in ["finance", "money", "budget", "saving"]):
        return {
            "affiliate": [
                "Budgeting apps",
                "Credit monitoring tools",
                "Personal finance books",
                "Investment education platforms",
            ],
            "dropshipping": [
                "Budget binders",
                "Cash envelope wallets",
                "Desk planners",
                "Financial goal trackers",
            ],
            "best_fit": "Digital products and affiliate offers are stronger than dropshipping for this niche.",
        }

    if any(keyword in niche_lower for keyword in ["fitness", "workout", "health", "gym"]):
        return {
            "affiliate": [
                "Fitness trackers",
                "Workout apps",
                "Resistance bands",
                "Meal planning apps",
            ],
            "dropshipping": [
                "Yoga mats",
                "Foam rollers",
                "Workout gloves",
                "Water bottles",
            ],
            "best_fit": "Affiliate and dropshipping can both fit this niche. Start with affiliate tests first.",
        }

    if any(keyword in niche_lower for keyword in ["creator", "content", "youtube", "social media", "ai"]):
        return {
            "affiliate": [
                "AI writing tools",
                "Video editing software",
                "Email marketing platforms",
                "Website builders",
            ],
            "dropshipping": [
                "Phone tripods",
                "Microphones",
                "Desk lights",
                "Portable ring lights",
            ],
            "best_fit": "Affiliate offers and digital toolkits are strong for creator audiences.",
        }

    if any(keyword in niche_lower for keyword in ["beauty", "skin", "skincare", "makeup"]):
        return {
            "affiliate": [
                "Skincare products",
                "Beauty tools",
                "Makeup organizers",
                "Ingredient education products",
            ],
            "dropshipping": [
                "Makeup organizers",
                "Beauty mirrors",
                "Travel cosmetic bags",
                "Facial rollers",
            ],
            "best_fit": "Affiliate can be strong, but product safety and honest wording are very important.",
        }

    return {
        "affiliate": [
            "AI tools",
            "Productivity apps",
            "Digital templates",
            "Creator software",
        ],
        "dropshipping": [
            "Desk accessories",
            "Phone stands",
            "Digital creator gear",
            "Lifestyle accessories",
        ],
        "best_fit": "Start with affiliate products and digital offers before testing dropshipping products.",
    }


def extract_database_record_id(db_result) -> str:
    """
    Safely extract database record id from different possible Supabase response shapes.
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


def check_database_saved(db_result, database_record_id: str) -> bool:
    """
    Decide whether database save worked.
    If record id exists, database_saved is true.
    Otherwise, check common success response shapes.
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


@router.post("/roadmap")
def generate_affiliate_roadmap(request: AffiliateRoadmapRequest):
    """
    Generate a validation-first affiliate and dropshipping roadmap.
    """

    product_ideas = get_affiliate_dropshipping_ideas(request.niche)
    platform_text = ", ".join(request.platforms)

    result = {
        "roadmap_summary": (
            f"For your {request.niche} niche and audience ({request.audience}), "
            f"the safest starting path is to validate product interest through content on {platform_text}. "
            f"Because your budget is {request.budget.lower()}, start with low-cost affiliate tests or simple digital offers first."
        ),
        "affiliate_product_ideas": product_ideas["affiliate"],
        "dropshipping_product_ideas": product_ideas["dropshipping"],
        "best_product_fit": product_ideas["best_fit"],
        "content_promotion_plan": [
            "Create problem-aware content that explains the audience pain point.",
            "Create comparison or review content around 2-3 product options.",
            "Use short-form videos to test saves, comments, clicks, and direct messages.",
            "Use transparent affiliate disclosure when promoting affiliate links.",
        ],
        "supplier_research_checklist": [
            "Check product reviews and customer complaints before choosing a supplier.",
            "Compare at least 3 suppliers or affiliate programs.",
            "Check shipping time, refund policy, and product quality signals.",
            "Avoid products with unclear claims, risky health promises, or poor reviews.",
        ],
        "thirty_day_roadmap": [
            "Week 1: Choose 2 product categories and create audience problem content.",
            "Week 2: Publish 5 short videos testing product-related angles.",
            "Week 3: Add affiliate disclosure, CTA, and track clicks, comments, saves, and direct messages.",
            "Week 4: Review performance and keep the best product angle.",
        ],
        "risk_analysis": [
            "Affiliate or dropshipping success is not guaranteed.",
            "Dropshipping has supplier, shipping, and refund risks.",
            "Affiliate content needs clear disclosure and honest product language.",
        ],
        "ethical_disclosure": (
            "This content may contain affiliate links. If you buy through my link, "
            "I may earn a small commission at no extra cost to you."
        ),
        "next_best_action": (
            f"Pick one product from the {request.product_category} category, create 3 short-form videos, "
            "and measure saves, comments, clicks, and direct messages before building a full funnel."
        ),
        "data_note": "MVP uses rule-based product recommendation logic with sample market signals.",
    }

    ai_result = generate_local_ai_response(
        module_name="affiliate",
        payload={
            "niche": request.niche,
            "audience": request.audience,
            "region": request.region,
            "platforms": request.platforms,
            "business_type": request.business_type,
            "budget": request.budget,
            "product_category": request.product_category,
            "content_style": request.content_style,
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
        "product_category": request.product_category,
        "content_style": request.content_style,
        "roadmap_summary": result["roadmap_summary"],
        "affiliate_product_ideas": result["affiliate_product_ideas"],
        "dropshipping_product_ideas": result["dropshipping_product_ideas"],
        "best_product_fit": result["best_product_fit"],
        "content_promotion_plan": result["content_promotion_plan"],
        "supplier_research_checklist": result["supplier_research_checklist"],
        "thirty_day_roadmap": result["thirty_day_roadmap"],
        "risk_analysis": result["risk_analysis"],
        "ethical_disclosure": result["ethical_disclosure"],
        "next_best_action": result["next_best_action"],
        "data_note": result["data_note"],
    }

    db_result = save_record_safely("affiliate_roadmaps", database_payload)

    database_record_id = extract_database_record_id(db_result)
    database_saved = check_database_saved(db_result, database_record_id)

    response_payload = attach_database_result(result, db_result)

    return add_proof_fields(
        payload=response_payload,
        database_saved=database_saved,
        database_record_id=database_record_id,
        granite_used=True,
    )



