from typing import List, Optional

from pydantic import BaseModel, Field


class CreatorProfileRequest(BaseModel):
    """
    Request body for creator profile analysis.
    """

    name: Optional[str] = "Alex Morgan"
    niche: str = Field(..., min_length=2)
    platforms: List[str]
    followers: int = Field(..., ge=0)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    skills: str = Field(..., min_length=2)
    business_interest: str = Field(..., min_length=2)
    income_goal: str = Field(..., min_length=1)
    available_time: str = Field(..., min_length=1)
    current_challenge: str = Field(..., min_length=2)


class ContentPackageRequest(BaseModel):
    """
    Request body for AI content package generation.

    story_or_video_reference and video_style are optional so older frontend
    forms will not break if those fields are not sent.
    """

    creator_id: Optional[str] = None
    topic: str = Field(..., min_length=2)
    platform: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    tone: str = Field(..., min_length=2)
    duration: str = Field(..., min_length=1)
    language: str = Field(..., min_length=2)
    content_goal: str = Field(..., min_length=2)
    story_or_video_reference: Optional[str] = None
    video_style: Optional[str] = None


class MarketAnalysisRequest(BaseModel):
    """
    Request body for market analysis.
    """

    creator_id: Optional[str] = None
    niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platforms: List[str]
    business_type: str = Field(..., min_length=2)
    budget: str = Field(..., min_length=1)
    product_interest: str = Field(..., min_length=2)


class ProductValidationRequest(BaseModel):
    """
    Request body for product validation scoring.
    """

    creator_id: Optional[str] = None
    product_name: str = Field(..., min_length=2)
    niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platform: str = Field(..., min_length=2)
    business_model: str = Field(..., min_length=2)
    budget: str = Field(..., min_length=1)
    product_type: str = Field(..., min_length=2)
    promotion_style: str = Field(..., min_length=2)


class AffiliateRoadmapRequest(BaseModel):
    """
    Request body for affiliate and dropshipping roadmap.
    """

    creator_id: Optional[str] = None
    niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platforms: List[str]
    business_type: str = Field(..., min_length=2)
    budget: str = Field(..., min_length=1)
    product_category: str = Field(..., min_length=2)
    content_style: str = Field(..., min_length=2)


class EthicalCheckRequest(BaseModel):
    """
    Request body for ethical monetization checker.
    """

    creator_id: Optional[str] = None
    content_text: str = Field(..., min_length=5)
    platform: str = Field(..., min_length=2)
    promotion_type: str = Field(..., min_length=2)
    has_affiliate_link: bool
    product_claim: str = Field(..., min_length=2)
    target_audience: str = Field(..., min_length=2)


class SevenAgentRequest(BaseModel):
    """
    Request body for the 7-agent creator business dashboard.
    """

    creator_id: Optional[str] = None
    creator_niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platforms: List[str]
    followers: int = Field(..., ge=0)
    product_idea: str = Field(..., min_length=2)
    business_model: str = Field(..., min_length=2)
    income_goal: str = Field(..., min_length=1)
    available_time: str = Field(..., min_length=1)
    promotion_copy: str = Field(..., min_length=2)


class ReportGenerateRequest(BaseModel):
    """
    Request body for PDF report generation.
    """

    creator_id: Optional[str] = None
    creator_name: str = Field(..., min_length=2)
    creator_niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platforms: List[str]
    product_idea: str = Field(..., min_length=2)
    business_model: str = Field(..., min_length=2)
    income_goal: str = Field(..., min_length=1)



