from fastapi import APIRouter

from services.database import get_recent_records, insert_record


router = APIRouter(prefix="/db", tags=["Database"])


def get_latest_records(table_name: str, limit: int = 5):
    """
    Local wrapper to keep route code readable.
    """

    return get_recent_records(table_name, limit=limit)


@router.get("/health")
def database_health_check():
    """
    Test Supabase database connection by reading recent creators.
    """

    try:
        creators = get_recent_records("creators", limit=3)

        return {
            "status": "ok",
            "message": "Supabase database connection is working.",
            "recent_creators": creators,
        }

    except Exception as error:
        return {
            "status": "error",
            "message": "Supabase database connection failed.",
            "detail": str(error),
        }


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

        return {
            "status": "success",
            "message": "Test creator inserted successfully.",
            "data": saved_creator,
        }

    except Exception as error:
        return {
            "status": "error",
            "message": "Failed to insert test creator.",
            "detail": str(error),
        }


@router.get("/latest-creators")
def latest_creators():
    return {"status": "ok", "data": get_latest_records("creators", limit=5)}


@router.get("/latest-content")
def latest_content_outputs():
    return {"status": "ok", "data": get_latest_records("content_outputs", limit=5)}


@router.get("/latest-market-analysis")
def latest_market_analysis():
    return {"status": "ok", "data": get_latest_records("market_analysis_results", limit=5)}


@router.get("/latest-product-scores")
def latest_product_scores():
    return {"status": "ok", "data": get_latest_records("product_scores", limit=5)}


@router.get("/latest-affiliate-roadmaps")
def latest_affiliate_roadmaps():
    return {"status": "ok", "data": get_latest_records("affiliate_roadmaps", limit=5)}


@router.get("/latest-ethical-checks")
def latest_ethical_checks():
    return {"status": "ok", "data": get_latest_records("ethical_check_results", limit=5)}


@router.get("/latest-seven-agent-reports")
def latest_seven_agent_reports():
    return {"status": "ok", "data": get_latest_records("seven_agent_reports", limit=5)}


@router.get("/latest-reports")
def latest_reports():
    return {"status": "ok", "data": get_latest_records("reports", limit=5)}


@router.get("/overview")
def database_overview():
    """
    Return latest saved records for the history dashboard.
    """

    return {
        "status": "ok",
        "creators": get_latest_records("creators", limit=3),
        "content_outputs": get_latest_records("content_outputs", limit=3),
        "product_scores": get_latest_records("product_scores", limit=3),
        "market_analysis": get_latest_records("market_analysis_results", limit=3),
        "affiliate_roadmaps": get_latest_records("affiliate_roadmaps", limit=3),
        "ethical_checks": get_latest_records("ethical_check_results", limit=3),
        "seven_agent_reports": get_latest_records("seven_agent_reports", limit=3),
        "reports": get_latest_records("reports", limit=3),
    }


