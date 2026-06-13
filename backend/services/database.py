import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from supabase import Client, create_client


# Load environment variables from backend/.env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


def get_supabase_client() -> Client:
    """
    Create and return a Supabase client.

    Priority:
    1. SUPABASE_SERVICE_ROLE_KEY
    2. SUPABASE_ANON_KEY

    This keeps the backend flexible for both local demo and hosted use.
    """

    if not SUPABASE_URL:
        raise RuntimeError("SUPABASE_URL is missing from backend/.env")

    supabase_key = SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY

    if not supabase_key:
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY is missing from backend/.env"
        )

    return create_client(SUPABASE_URL, supabase_key)


def insert_record(table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert one record into a Supabase table.
    """

    supabase = get_supabase_client()
    response = supabase.table(table_name).insert(data).execute()

    return {
        "status": "success",
        "table": table_name,
        "data": response.data or [],
    }


def get_recent_records(
    table_name: str,
    limit: int = 10,
    order_by: str = "created_at",
) -> List[Dict[str, Any]]:
    """
    Get recent records from a Supabase table.

    The function returns a list directly.
    """

    supabase = get_supabase_client()

    response = (
        supabase
        .table(table_name)
        .select("*")
        .order(order_by, desc=True)
        .limit(limit)
        .execute()
    )

    return response.data or []


def get_record_by_id(
    table_name: str,
    record_id: str,
    id_column: str = "id",
) -> Optional[Dict[str, Any]]:
    """
    Get one record by ID.
    """

    supabase = get_supabase_client()

    response = (
        supabase
        .table(table_name)
        .select("*")
        .eq(id_column, record_id)
        .limit(1)
        .execute()
    )

    rows = response.data or []

    if not rows:
        return None

    return rows[0]



