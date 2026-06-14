from typing import Any

from fastapi import APIRouter

from models.schemas import EthicalCheckRequest
from routes.utils import attach_database_result, clean_optional_uuid, save_record_safely
from services.ai_service import generate_local_ai_response
from services.proof import add_proof_fields


router = APIRouter(prefix="/ethical", tags=["Ethical Checker"])


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


def analyze_ethical_risks(request: EthicalCheckRequest) -> dict:
    """
    Analyze promotional content for common monetization risk signals.
    """

    text = request.content_text.lower()
    claim = request.product_claim.lower()

    issues = []
    score = 100

    disclosure_keywords = [
        "affiliate",
        "commission",
        "sponsored",
        "paid partnership",
        "ad",
        "at no extra cost",
    ]

    risky_guarantee_words = [
        "guaranteed",
        "100%",
        "always works",
        "instant results",
        "make you rich",
        "get rich",
        "no risk",
        "never fail",
    ]

    fake_urgency_words = [
        "buy now or regret",
        "only today",
        "last chance",
        "limited time",
        "act now",
    ]

    clickbait_words = [
        "shocking",
        "you won't believe",
        "must watch",
        "insane",
        "secret nobody tells",
    ]

    risky_income_words = [
        "make money fast",
        "passive income guaranteed",
        "earn thousands overnight",
        "rich fast",
    ]

    has_disclosure = any(keyword in text for keyword in disclosure_keywords)

    if request.has_affiliate_link and not has_disclosure:
        issues.append("Affiliate disclosure appears to be missing.")
        score -= 25

    if any(word in text or word in claim for word in risky_guarantee_words):
        issues.append("Content may contain guaranteed or overpromising language.")
        score -= 20

    if any(word in text for word in fake_urgency_words):
        issues.append("Content may contain fake urgency or pressure-based selling.")
        score -= 12

    if any(word in text for word in clickbait_words):
        issues.append("Content may contain clickbait-style wording.")
        score -= 10

    if any(word in text or word in claim for word in risky_income_words):
        issues.append("Content may contain risky income or financial promise.")
        score -= 18

    if "best product" in text or "best tool" in text:
        issues.append(
            "The content may need more balanced wording instead of absolute claims."
        )
        score -= 8

    score = max(score, 0)

    if score >= 85:
        risk_level = "Low Risk"
    elif score >= 65:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    return {
        "score": score,
        "risk_level": risk_level,
        "issues": issues
        if issues
        else ["No major ethical monetization issue detected in this MVP check."],
        "disclosure_status": "Disclosure found"
        if has_disclosure
        else "Disclosure missing or unclear",
    }


def build_safer_version(request: EthicalCheckRequest) -> str:
    """
    Build a safer and more transparent rewrite.
    """

    safer_body = (
        request.content_text.replace(
            "will make you rich fast",
            "may help you organize your workflow or finances",
        )
        .replace("guaranteed", "designed to help")
        .replace("100%", "potentially")
        .replace("instant results", "better results over time")
        .replace("Buy now", "Check if this fits your needs")
        .replace("buy now", "check if this fits your needs")
    )

    if request.has_affiliate_link:
        safer_body += (
            "\n\nDisclosure: This content may contain affiliate links. "
            "If you buy through my link, I may earn a small commission "
            "at no extra cost to you."
        )

    safer_body += (
        "\n\nReminder: Results can vary based on your situation, effort, "
        "and product fit."
    )

    return "Here is a more transparent and platform-friendly version:\n\n" + safer_body


@router.post("/check")
def check_ethical_monetization(request: EthicalCheckRequest):
    """
    Check promotional content, add local AI reasoning, save the result,
    and return proof fields for the frontend AiProofCard.
    """

    analysis = analyze_ethical_risks(request)

    result = {
        "ethical_score": analysis["score"],
        "risk_level": analysis["risk_level"],
        "issues_found": analysis["issues"],
        "disclosure_status": analysis["disclosure_status"],
        "safer_version": build_safer_version(request),
        "recommended_disclosure": (
            "This content may contain affiliate links. If you buy through my link, "
            "I may earn a small commission at no extra cost to you."
        ),
        "next_best_action": (
            "Before publishing, add a clear disclosure, remove guaranteed outcome language, "
            "avoid pressure-based wording, and explain the product honestly with limitations."
        ),
        "platform_note": (
            f"For {request.platform}, keep promotional language transparent, "
            "clear, and audience-friendly."
        ),
        "data_note": "This MVP uses rule-based ethical risk detection.",
    }

    ai_result = generate_local_ai_response(
        module_name="ethical",
        payload={
            "content_text": request.content_text,
            "platform": request.platform,
            "promotion_type": request.promotion_type,
            "has_affiliate_link": request.has_affiliate_link,
            "product_claim": request.product_claim,
            "target_audience": request.target_audience,
        },
    )

    result.update(ai_result)

    database_payload = {
        "creator_id": clean_optional_uuid(request.creator_id),
        "content_text": request.content_text,
        "platform": request.platform,
        "promotion_type": request.promotion_type,
        "has_affiliate_link": request.has_affiliate_link,
        "product_claim": request.product_claim,
        "target_audience": request.target_audience,
        "ethical_score": result["ethical_score"],
        "risk_level": result["risk_level"],
        "issues_found": result["issues_found"],
        "disclosure_status": result["disclosure_status"],
        "safer_version": result["safer_version"],
        "recommended_disclosure": result["recommended_disclosure"],
        "next_best_action": result["next_best_action"],
        "platform_note": result["platform_note"],
        "data_note": result["data_note"],
    }

    db_result = save_record_safely("ethical_check_results", database_payload)

    database_record_id = extract_database_record_id(db_result)
    database_saved = check_database_saved(db_result, database_record_id)

    response_payload = attach_database_result(result, db_result)

    return add_proof_fields(
        payload=response_payload,
        database_saved=database_saved,
        database_record_id=database_record_id,
        granite_used=True,
    )



