"""
Database Routes

Handles Supabase database health, test insert, latest saved records,
and history overview for CreatorCareer AI.
"""

from typing import Any

from fastapi import APIRouter

from services.database import get_recent_records, insert_record
from services.proof import add_proof_fields


router = APIRouter(prefix="/db", tags=["Database"])


def get_latest_records(table_name: str, limit: int = 5):
    """
    Local wrapper to keep route code readable.
    """

    return get_recent_records(table_name, limit=limit)


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


def success_response(message: str, data: Any = None):
    """
    Standard success response with proof fields.
    """

    result = {
        "status": "ok",
        "message": message,
        "data": data,
        "database_connected": True,
    }

    return add_proof_fields(
        payload=result,
        database_saved=False,
        database_record_id="",
        granite_used=False,
    )


def error_response(message: str, error: Exception):
    """
    Standard error response with proof fields.
    """

    result = {
        "status": "error",
        "message": message,
        "detail": str(error),
        "database_connected": False,
    }

    return add_proof_fields(
        payload=result,
        database_saved=False,
        database_record_id="",
        granite_used=False,
    )


@router.get("/health")
def database_health_check():
    """
    Test Supabase database connection by reading recent creators.
    """

    try:
        creators = get_recent_records("creators", limit=3)

        result = {
            "status": "ok",
            "message": "Supabase database connection is working.",
            "recent_creators": creators,
            "database_connected": True,
        }

        return add_proof_fields(
            payload=result,
            database_saved=False,
            database_record_id="",
            granite_used=False,
        )

    except Exception as error:
        result = {
            "status": "error",
            "message": "Supabase database connection failed.",
            "detail": str(error),
            "database_connected": False,
        }

        return add_proof_fields(
            payload=result,
            database_saved=False,
            database_record_id="",
            granite_used=False,
        )


@router.post("/test-creator")
def create_test_creator():
    """
    Insert one test creator into Supabase.
    """

    try:
        test_creator = {
            "name": "Alex Morgan",
            "niche": "Personal finance",
            "platforms": ["TikTok", "Instagram Reels", "YouTube Shorts"],
            "followers": 25000,
            "audience": "USA young professionals, age 22-35",
            "region": "United States",
            "skills": "Budgeting tips, short-form video storytelling",
            "business_interest": "Digital products + affiliate marketing",
            "income_goal": "$2,000/month in 6 months",
            "available_time": "2 hours/day",
            "current_challenge": "Needs clear roadmap to turn audience into business",
            "readiness_score": 82,
            "creator_stage": "Monetization-ready Creator",
        }

        saved_creator = insert_record("creators", test_creator)
        database_record_id = extract_database_record_id(saved_creator)

        result = {
            "status": "success",
            "message": "Test creator inserted successfully.",
            "data": saved_creator,
            "database_connected": True,
        }

        return add_proof_fields(
            payload=result,
            database_saved=True,
            database_record_id=database_record_id,
            granite_used=False,
        )

    except Exception as error:
        result = {
            "status": "error",
            "message": "Failed to insert test creator.",
            "detail": str(error),
            "database_connected": False,
        }

        return add_proof_fields(
            payload=result,
            database_saved=False,
            database_record_id="",
            granite_used=False,
        )


@router.get("/latest-creators")
def latest_creators():
    try:
        return success_response(
            message="Latest creator profiles loaded successfully.",
            data=get_latest_records("creators", limit=5),
        )
    except Exception as error:
        return error_response("Failed to load latest creator profiles.", error)


@router.get("/latest-content")
def latest_content_outputs():
    try:
        return success_response(
            message="Latest content outputs loaded successfully.",
            data=get_latest_records("content_outputs", limit=5),
        )
    except Exception as error:
        return error_response("Failed to load latest content outputs.", error)


@router.get("/latest-market-analysis")
def latest_market_analysis():
    try:
        return success_response(
            message="Latest market analysis records loaded successfully.",
            data=get_latest_records("market_analysis_results", limit=5),
        )
    except Exception as error:
        return error_response("Failed to load latest market analysis records.", error)


@router.get("/latest-product-scores")
def latest_product_scores():
    try:
        return success_response(
            message="Latest product scores loaded successfully.",
            data=get_latest_records("product_scores", limit=5),
        )
    except Exception as error:
        return error_response("Failed to load latest product scores.", error)


@router.get("/latest-affiliate-roadmaps")
def latest_affiliate_roadmaps():
    try:
        return success_response(
            message="Latest affiliate roadmaps loaded successfully.",
            data=get_latest_records("affiliate_roadmaps", limit=5),
        )
    except Exception as error:
        return error_response("Failed to load latest affiliate roadmaps.", error)


@router.get("/latest-ethical-checks")
def latest_ethical_checks():
    try:
        return success_response(
            message="Latest ethical checks loaded successfully.",
            data=get_latest_records("ethical_check_results", limit=5),
        )
    except Exception as error:
        return error_response("Failed to load latest ethical checks.", error)


@router.get("/latest-seven-agent-reports")
def latest_seven_agent_reports():
    try:
        return success_response(
            message="Latest 7-agent reports loaded successfully.",
            data=get_latest_records("seven_agent_reports", limit=5),
        )
    except Exception as error:
        return error_response("Failed to load latest 7-agent reports.", error)


@router.get("/latest-reports")
def latest_reports():
    try:
        return success_response(
            message="Latest PDF reports loaded successfully.",
            data=get_latest_records("reports", limit=5),
        )
    except Exception as error:
        return error_response("Failed to load latest PDF reports.", error)


@router.get("/overview")
def database_overview():
    """
    Return latest saved records for the history dashboard.
    """

    try:
        result = {
            "status": "ok",
            "message": "Database overview loaded successfully.",
            "database_connected": True,
            "creators": get_latest_records("creators", limit=3),
            "content_outputs": get_latest_records("content_outputs", limit=3),
            "product_scores": get_latest_records("product_scores", limit=3),
            "market_analysis": get_latest_records("market_analysis_results", limit=3),
            "affiliate_roadmaps": get_latest_records("affiliate_roadmaps", limit=3),
            "ethical_checks": get_latest_records("ethical_check_results", limit=3),
            "seven_agent_reports": get_latest_records("seven_agent_reports", limit=3),
            "reports": get_latest_records("reports", limit=3),
        }

        return add_proof_fields(
            payload=result,
            database_saved=False,
            database_record_id="",
            granite_used=False,
        )

    except Exception as error:
        result = {
            "status": "error",
            "message": "Failed to load database overview.",
            "detail": str(error),
            "database_connected": False,
        }

        return add_proof_fields(
            payload=result,
            database_saved=False,
            database_record_id="",
            granite_used=False,
        )
    


