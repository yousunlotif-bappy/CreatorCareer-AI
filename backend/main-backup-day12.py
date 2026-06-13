import json
import uuid
from datetime import datetime
from html import escape
from pathlib import Path
from typing import List

from services.database import get_recent_records, insert_record

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# Main FastAPI app for CreatorCareer AI.
app = FastAPI(
    title="CreatorCareer AI Backend",
    description=(
        "Backend API for creator profile analysis, content packages, market analysis, "
        "product validation, affiliate roadmap, ethical monetization, 7-agent dashboard, "
        "database testing, and PDF business reports."
    ),
    version="0.1.0",
)

# Allow the Next.js frontend to connect with this FastAPI backend.
# Frontend local URL: http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Folder where generated PDF reports will be saved.
reports_dir = Path(__file__).parent / "reports"
reports_dir.mkdir(exist_ok=True)

# This makes generated PDFs downloadable from:
# http://localhost:8000/reports/<file-name>.pdf
app.mount("/reports", StaticFiles(directory=str(reports_dir)), name="reports")


class CreatorProfileRequest(BaseModel):
    """
    Request model for creator profile analysis.

    The frontend sends creator profile information to this model.
    The backend uses the data to calculate a simple creator readiness score
    and generate an AI-style business summary.
    """

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


def calculate_readiness_score(profile: CreatorProfileRequest) -> int:
    """
    Calculate a simple creator business readiness score.

    This is MVP scoring logic for the contest demo.
    Later, this can be upgraded with IBM Granite / watsonx
    for deeper AI-based scoring.
    """

    score = 40

    # Audience size gives basic creator strength.
    if profile.followers >= 1000:
        score += 10

    if profile.followers >= 10000:
        score += 10

    if profile.followers >= 50000:
        score += 5

    # Multi-platform creators usually have better distribution.
    if len(profile.platforms) >= 2:
        score += 10

    if len(profile.platforms) >= 4:
        score += 5

    # Business intent matters for creator-to-entrepreneur transition.
    interest = profile.business_interest.lower()

    if "affiliate" in interest:
        score += 8

    if "digital" in interest:
        score += 8

    if "product" in interest:
        score += 7

    if "dropshipping" in interest:
        score += 5

    # Clear skill description means stronger creator positioning.
    if len(profile.skills) > 20:
        score += 7

    return min(score, 100)


def get_creator_stage(followers: int) -> str:
    """
    Determine creator stage based on follower count.
    """

    if followers < 1000:
        return "Early-stage Creator"

    if followers < 10000:
        return "Growing Creator"

    if followers < 50000:
        return "Monetization-ready Creator"

    return "Established Creator"


@app.get("/")
def health_check():
    """
    Health check endpoint.

    This confirms that the backend server is running successfully.
    """

    return {
        "status": "ok",
        "message": "CreatorCareer AI backend is running",
    }


@app.post("/profile/analyze")
def analyze_creator_profile(profile: CreatorProfileRequest):
    """
    Analyze a creator profile and return an AI-style business report.

    For the MVP, this uses simple rule-based logic.
    Later, this endpoint can call IBM Granite / watsonx.
    """

    readiness_score = calculate_readiness_score(profile)
    creator_stage = get_creator_stage(profile.followers)
    platform_text = ", ".join(profile.platforms)

    return {
        "creator_summary": (
            f"You are a {creator_stage.lower()} in the {profile.niche} niche, "
            f"creating content for {profile.audience} across {platform_text}."
        ),
        "creator_stage": creator_stage,
        "niche_positioning": (
            f"Your strongest positioning is to become a trusted creator in {profile.niche}. "
            f"Your content should focus on practical, useful, and audience-friendly solutions "
            f"for people in {profile.region}."
        ),
        "audience_opportunity": (
            "Your audience has potential for educational, problem-solving, and product-driven content. "
            "This can support digital products, affiliate recommendations, dropshipping ideas, "
            "or creator-led services when trust is built properly."
        ),
        "business_opportunity": (
            f"Based on your interest in {profile.business_interest}, your best path is to connect "
            "your content with useful offers, simple products, transparent monetization, and a clear "
            "content-to-commerce roadmap."
        ),
        "business_readiness_score": readiness_score,
        "recommended_next_modules": [
            "AI Content Package Generator",
            "AI Market Analysis",
            "Product Validation Score",
            "Affiliate & Dropshipping Roadmap",
            "Ethical Monetization Checker",
            "7-Agent Creator Business Dashboard",
            "PDF Business Report Generator",
        ],
        "next_best_action": (
            "Create 5 content ideas around your audience's biggest problem. Then validate one product "
            "idea using comments, polls, short-form video engagement, and audience questions."
        ),
    }


class ContentPackageRequest(BaseModel):
    """
    Request model for AI content package generation.

    This also collects story/video reference input so the system can
    prepare a video generation plan for future AI video tools.
    """

    topic: str = Field(..., min_length=2)
    platform: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    tone: str = Field(..., min_length=2)
    duration: str = Field(..., min_length=1)
    language: str = Field(..., min_length=2)
    content_goal: str = Field(..., min_length=2)

    # Video/story import workflow fields.
    story_or_video_reference: str = Field(..., min_length=2)
    video_style: str = Field(..., min_length=2)


def build_hashtags(topic: str, platform: str) -> List[str]:
    """
    Build simple hashtags from topic and platform.

    This is MVP logic.
    Later, this can be improved with IBM Granite / watsonx.
    """

    clean_words = [
        word.strip("#,.!?").lower()
        for word in topic.split()
        if len(word.strip("#,.!?")) > 3
    ]

    base_tags = ["#CreatorTips", "#ContentCreator", "#DigitalBusiness"]

    platform_lower = platform.lower()

    if "tiktok" in platform_lower:
        base_tags.append("#TikTokTips")

    if "instagram" in platform_lower:
        base_tags.append("#InstagramReels")

    if "youtube" in platform_lower:
        base_tags.append("#YouTubeShorts")

    if "facebook" in platform_lower:
        base_tags.append("#FacebookReels")

    topic_tags = [f"#{word.title().replace('-', '')}" for word in clean_words[:4]]

    # dict.fromkeys removes duplicates while keeping order.
    return list(dict.fromkeys(base_tags + topic_tags))


def build_scene_breakdown(request: ContentPackageRequest) -> List[str]:
    """
    Create a simple AI video scene plan.

    This is not real video rendering yet.
    It prepares a structure that can later be sent to IBM Granite/watsonx,
    Runway, Pika, Kling, or another AI video tool.
    """

    return [
        f"Scene 1: Start with a fast visual hook about {request.topic}. Show the problem clearly in the first 3 seconds.",
        f"Scene 2: Show the creator explaining why this matters for {request.audience}.",
        f"Scene 3: Add 2-3 quick examples from the story/video reference: {request.story_or_video_reference}.",
        f"Scene 4: Show the simple solution using a {request.tone.lower()} tone.",
        f"Scene 5: End with a clear CTA and a strong visual that matches {request.platform}.",
    ]


@app.post("/content/package")
def generate_content_package(request: ContentPackageRequest):
    """
    Generate a complete AI-style content package.

    For the MVP, this uses structured rule-based generation.
    Later, this endpoint can call IBM Granite / watsonx.
    """

    titles = [
        f"{request.topic}: What Most Creators Miss",
        f"How to Use {request.topic} to Grow Smarter",
        f"{request.topic} Explained for {request.audience}",
        f"Stop Ignoring This: {request.topic}",
    ]

    hook = (
        f"If you are creating content for {request.audience}, "
        f"this idea about {request.topic} can help you create smarter and move faster."
    )

    voiceover_script = (
        f"Many creators talk about {request.topic}, but very few turn it into a clear strategy. "
        f"In this {request.duration} {request.platform} video, start with the problem, "
        f"explain the simple solution, and end with one action your audience can take today. "
        f"Use a {request.tone.lower()} tone and keep the message practical."
    )

    caption = (
        f"{request.topic} can become more than just content. "
        f"It can help creators educate, build trust, and move toward a real digital business. "
        f"Save this idea if you want to create with purpose."
    )

    thumbnail_text = [
        "Stop Posting Randomly",
        "Turn Content Into Business",
        "Creator Growth Roadmap",
        "Create Smarter",
    ]

    content_goal_lower = request.content_goal.lower()

    if "sell" in content_goal_lower or "conversion" in content_goal_lower:
        cta = "Comment your niche and start building your creator business roadmap."
    elif "awareness" in content_goal_lower:
        cta = "Save this and use it for your next content plan."
    else:
        cta = "Follow for more creator growth and digital business ideas."

    platform_notes = (
        f"For {request.platform}, keep the opening fast, use short lines, "
        f"add subtitles, and place the strongest idea in the first 3 seconds."
    )

    video_generation_prompt = (
        f"Create a {request.duration} {request.video_style} vertical video for {request.platform}. "
        f"The video topic is: {request.topic}. "
        f"Target audience: {request.audience}. "
        f"Use a {request.tone.lower()} tone. "
        f"Story/video reference: {request.story_or_video_reference}. "
        f"Start with a strong visual hook, use fast pacing, add subtitle-friendly scenes, "
        f"and end with a clear call to action."
    )

    b_roll_ideas = [
        "Close-up creator talking to camera",
        "Text overlay showing the main mistake/problem",
        "Screen recording or simple visual example",
        "Before vs after comparison",
        "Final CTA screen with bold thumbnail-style text",
    ]

    editing_notes = [
        "Use vertical 9:16 format",
        "Keep first 3 seconds visually strong",
        "Add large readable subtitles",
        "Use quick cuts every 2-3 seconds",
        "End with CTA text on screen",
    ]

    return {
        "titles": titles,
        "hook": hook,
        "voiceover_script": voiceover_script,
        "caption": caption,
        "hashtags": build_hashtags(request.topic, request.platform),
        "thumbnail_text": thumbnail_text,
        "cta": cta,
        "platform_notes": platform_notes,
        "scene_breakdown": build_scene_breakdown(request),
        "video_generation_prompt": video_generation_prompt,
        "b_roll_ideas": b_roll_ideas,
        "editing_notes": editing_notes,
        "status": (
            "MVP generated output. Ready for IBM Granite/watsonx "
            "and AI video generation integration."
        ),
    }


class MarketAnalysisRequest(BaseModel):
    """
    Request model for AI Market Analysis.

    This collects creator market context.
    The backend uses this data to match the creator niche with
    sample market signal data.
    """

    niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platforms: List[str]
    business_type: str = Field(..., min_length=2)
    budget: str = Field(..., min_length=1)
    product_interest: str = Field(..., min_length=2)


def load_market_data() -> dict:
    """
    Load sample market data from backend/data/sample_market_data.json.

    This keeps the MVP simple and contest-demo friendly.
    Later, this can be replaced with live APIs like Google Trends,
    affiliate marketplaces, e-commerce data, and social trend APIs.
    """

    data_path = Path(__file__).parent / "data" / "sample_market_data.json"

    with open(data_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_market_category(niche: str, market_data: dict):
    """
    Match a creator niche to the closest sample market category.

    This is simple MVP matching logic.
    Later, IBM Granite / watsonx can make this matching smarter.
    """

    niche_lower = niche.lower().strip()

    # Direct match check.
    for category in market_data:
        if category in niche_lower or niche_lower in category:
            return category, market_data[category]

    # Helpful fallback rules for common creator niches.
    if any(keyword in niche_lower for keyword in ["money", "budget", "finance", "saving"]):
        return "personal finance", market_data["personal finance"]

    if any(keyword in niche_lower for keyword in ["fitness", "workout", "health", "gym"]):
        return "home fitness", market_data["home fitness"]

    if any(keyword in niche_lower for keyword in ["creator", "content", "youtube", "social media"]):
        return "creator education", market_data["creator education"]

    if any(keyword in niche_lower for keyword in ["beauty", "skin", "skincare", "makeup"]):
        return "beauty skincare", market_data["beauty skincare"]

    # Safe default fallback.
    return "creator education", market_data["creator education"]


@app.post("/market/analyze")
def analyze_market_opportunity(request: MarketAnalysisRequest):
    """
    Analyze market opportunity for a creator niche.

    Important:
    This endpoint does not claim guaranteed profit.
    It returns estimated market signals and recommended opportunities.
    """

    market_data = load_market_data()

    matched_category, category_data = find_market_category(
        request.niche,
        market_data,
    )

    platform_text = ", ".join(request.platforms)

    market_summary = (
        f"Based on the {matched_category} market signal, your audience segment "
        f"({request.audience}) has estimated potential for content-led product opportunities. "
        f"Your selected platforms ({platform_text}) can be used to test demand before launching "
        f"a full product in {request.region}."
    )

    business_type_note = (
        f"Your selected business type is {request.business_type}. "
        f"With a {request.budget.lower()} budget, start with validation-first content before "
        f"spending on inventory, ads, or paid tools."
    )

    next_best_action = (
        "Start with one low-cost product idea. Create 5 short-form videos around the audience problem, "
        "run one poll, and measure saves, comments, clicks, and direct messages before launching."
    )

    return {
        "matched_category": matched_category,
        "market_summary": market_summary,
        "demand_level": category_data["demand_level"],
        "competition_level": category_data["competition_level"],
        "recommended_products": category_data["recommended_products"],
        "digital_product_ideas": category_data["digital_product_ideas"],
        "affiliate_product_ideas": category_data["affiliate_product_ideas"],
        "dropshipping_product_ideas": category_data["dropshipping_product_ideas"],
        "best_platforms": category_data["best_platforms"],
        "risk_level": category_data["risk_level"],
        "opportunity_score": category_data["opportunity_score"],
        "business_type_note": business_type_note,
        "next_best_action": next_best_action,
        "data_note": (
            "MVP uses sample market signal data with API-ready architecture. "
            "Future versions can connect live Google Trends, affiliate marketplace, "
            "e-commerce, and social trend APIs."
        ),
    }


class ProductValidationRequest(BaseModel):
    """
    Request model for product validation.

    This collects the creator's product idea and business context.
    The backend uses rule-based MVP scoring now.
    Later, this can be improved with IBM Granite / watsonx.
    """

    product_name: str = Field(..., min_length=2)
    niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platform: str = Field(..., min_length=2)
    business_model: str = Field(..., min_length=2)
    budget: str = Field(..., min_length=1)
    product_type: str = Field(..., min_length=2)
    promotion_style: str = Field(..., min_length=2)


def calculate_product_validation_scores(request: ProductValidationRequest) -> dict:
    """
    MVP product validation scoring engine.

    The score is an estimated validation signal, not a profit guarantee.
    """

    niche = request.niche.lower()
    product = request.product_name.lower()
    business_model = request.business_model.lower()
    product_type = request.product_type.lower()
    budget = request.budget.lower()
    platform = request.platform.lower()
    promotion_style = request.promotion_style.lower()

    # Base scores keep the MVP realistic.
    audience_fit = 14
    market_demand = 11
    competition = 9
    content_promotion_fit = 12
    profit_potential = 6
    ease_of_starting = 6

    # Audience fit logic.
    niche_words = [word for word in niche.split() if len(word) > 3]

    if any(word in product for word in niche_words):
        audience_fit += 5

    if any(item in product for item in ["template", "planner", "guide", "tracker", "workbook"]):
        audience_fit += 4

    if any(item in product for item in ["course", "toolkit", "membership"]):
        audience_fit += 3

    # Market demand logic.
    high_demand_niches = [
        "finance",
        "fitness",
        "beauty",
        "creator",
        "ai",
        "productivity",
        "skincare",
        "business",
    ]

    if any(item in niche for item in high_demand_niches):
        market_demand += 5

    if "digital" in business_model or "affiliate" in business_model:
        market_demand += 3

    if "template" in product_type or "course" in product_type:
        market_demand += 1

    # Higher competition score means competition is manageable.
    if "low" in budget and any(item in product_type for item in ["digital", "template", "guide"]):
        competition += 3

    if "dropshipping" in business_model:
        competition -= 2

    if "high" in budget:
        competition += 1

    # Content promotion fit logic.
    if any(item in platform for item in ["tiktok", "instagram", "youtube", "shorts", "reels"]):
        content_promotion_fit += 4

    if any(item in product for item in ["planner", "template", "guide", "toolkit", "checklist"]):
        content_promotion_fit += 4

    if any(item in promotion_style for item in ["educational", "short-form", "tutorial", "story"]):
        content_promotion_fit += 2

    # Profit potential logic.
    if "digital" in business_model:
        profit_potential += 2

    if "affiliate" in business_model:
        profit_potential += 1

    if any(item in product for item in ["course", "toolkit", "template"]):
        profit_potential += 1

    # Ease of starting logic.
    if "low" in budget:
        ease_of_starting += 2

    if any(item in product_type for item in ["digital", "template", "guide", "workbook"]):
        ease_of_starting += 2

    if "dropshipping" in business_model:
        ease_of_starting -= 1

    # Cap each score by its maximum.
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
    Convert total validation score into a human-friendly product status.
    """

    if score >= 85:
        return "Strong Launch-Test Opportunity"

    if score >= 70:
        return "Good Opportunity — Validate First"

    if score >= 55:
        return "Moderate Opportunity — Needs More Research"

    return "Risky Idea — Improve Before Testing"


@app.post("/product/validate")
def validate_product(request: ProductValidationRequest):
    """
    Validate a product idea and return score breakdown.

    This endpoint does not guarantee sales or profit.
    It gives a practical MVP validation signal.
    """

    scores = calculate_product_validation_scores(request)
    total_score = scores["total_score"]
    status = get_validation_status(total_score)

    if total_score >= 85:
        recommendation = (
            "This product idea has strong validation potential. Start with a small MVP, "
            "test it through short-form content, and collect audience feedback before scaling."
        )
    elif total_score >= 70:
        recommendation = (
            "This product idea looks promising, but it should be validated first. "
            "Use polls, comments, waitlists, and 5-10 content tests before building the full product."
        )
    elif total_score >= 55:
        recommendation = (
            "This idea may work, but the positioning needs improvement. Refine the product promise, "
            "target audience, or promotion strategy before testing."
        )
    else:
        recommendation = (
            "This idea is currently risky. Improve audience fit, simplify the offer, or choose a product "
            "that connects more naturally with your content niche."
        )

    return {
        "product_name": request.product_name,
        "status": status,
        "total_score": total_score,
        "score_breakdown": scores,
        "recommendation": recommendation,
        "strengths": [
            "Product can be tested through content before major spending.",
            "Creator audience can be used for early validation.",
            "Short-form platforms can help test demand quickly.",
        ],
        "risks": [
            "Score is an estimate, not a guarantee of sales.",
            "Audience interest should be validated before launch.",
            "Competition and pricing should be checked before investing.",
        ],
        "validation_checklist": [
            "Define the exact audience problem this product solves.",
            "Create 5 content posts around the problem before launch.",
            "Run one poll or comment-based validation test.",
            "Check competitor pricing and product positioning.",
            "Prepare ethical disclosure if affiliate links are used.",
            "Start with a small MVP before building the full product.",
        ],
        "next_best_action": (
            f"Create 5 short-form videos about the problem behind '{request.product_name}', "
            "then measure saves, comments, clicks, and direct messages to validate demand."
        ),
        "data_note": (
            "This MVP score uses rule-based validation logic. Future versions can combine "
            "IBM Granite / watsonx reasoning with live market, affiliate, and e-commerce APIs."
        ),
    }


class AffiliateRoadmapRequest(BaseModel):
    """
    Request model for Affiliate & Dropshipping Roadmap.

    This collects creator business context.
    The backend uses MVP recommendation logic now.
    Later, this can be improved with IBM Granite / watsonx and live product APIs.
    """

    niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platforms: List[str]
    business_type: str = Field(..., min_length=2)
    budget: str = Field(..., min_length=1)
    product_category: str = Field(..., min_length=2)
    content_style: str = Field(..., min_length=2)


def get_affiliate_dropshipping_ideas(niche: str) -> dict:
    """
    Select affiliate and dropshipping ideas based on creator niche.

    This is simple MVP logic.
    It does not guarantee sales or income.
    """

    niche_lower = niche.lower()

    if any(keyword in niche_lower for keyword in ["finance", "money", "budget", "saving"]):
        return {
            "affiliate": [
                "Budgeting apps",
                "Credit monitoring tools",
                "Personal finance books",
                "Investment education platforms",
                "Notion finance templates marketplace",
            ],
            "dropshipping": [
                "Budget binders",
                "Cash envelope wallets",
                "Desk planners",
                "Financial goal trackers",
                "Minimal office organizers",
            ],
            "best_fit": (
                "Digital products and affiliate offers are stronger than dropshipping for this niche, "
                "because finance audiences usually trust education, tools, and templates more than random physical products."
            ),
        }

    if any(keyword in niche_lower for keyword in ["fitness", "workout", "health", "gym"]):
        return {
            "affiliate": [
                "Fitness trackers",
                "Workout apps",
                "Resistance bands",
                "Meal planning apps",
                "Protein shaker bottles",
            ],
            "dropshipping": [
                "Yoga mats",
                "Foam rollers",
                "Workout gloves",
                "Posture correctors",
                "Water bottles",
            ],
            "best_fit": (
                "Affiliate and dropshipping can both fit this niche. Start with affiliate tests first, "
                "then only test dropshipping products that solve clear workout problems."
            ),
        }

    if any(keyword in niche_lower for keyword in ["creator", "content", "youtube", "social media", "ai"]):
        return {
            "affiliate": [
                "AI writing tools",
                "Video editing software",
                "Email marketing platforms",
                "Website builders",
                "Creator analytics tools",
            ],
            "dropshipping": [
                "Phone tripods",
                "Microphones",
                "Desk lights",
                "Creator desk accessories",
                "Portable ring lights",
            ],
            "best_fit": (
                "Affiliate offers and digital toolkits are strong because creators naturally buy tools that improve workflow, "
                "content quality, and monetization systems."
            ),
        }

    if any(keyword in niche_lower for keyword in ["beauty", "skin", "skincare", "makeup"]):
        return {
            "affiliate": [
                "Skincare products",
                "Beauty tools",
                "Makeup organizers",
                "Ingredient education products",
                "Dermatologist-recommended product lines",
            ],
            "dropshipping": [
                "Makeup organizers",
                "Beauty mirrors",
                "Travel cosmetic bags",
                "Facial rollers",
                "Skincare mini fridges",
            ],
            "best_fit": (
                "Affiliate can be strong, but product safety, honest wording, and ethical claims are very important. "
                "Avoid exaggerated skincare or health promises."
            ),
        }

    return {
        "affiliate": [
            "AI tools",
            "Productivity apps",
            "Digital templates",
            "Creator software",
            "Online learning platforms",
        ],
        "dropshipping": [
            "Desk accessories",
            "Phone stands",
            "Digital creator gear",
            "Lifestyle accessories",
            "Home office tools",
        ],
        "best_fit": (
            "Start with affiliate products and digital offers before testing dropshipping products. "
            "This keeps risk lower while you validate audience interest."
        ),
    }


@app.post("/affiliate/roadmap")
def generate_affiliate_roadmap(request: AffiliateRoadmapRequest):
    """
    Generate a validation-first affiliate and dropshipping roadmap.

    Important:
    This endpoint does not promise guaranteed income.
    """

    product_ideas = get_affiliate_dropshipping_ideas(request.niche)
    platform_text = ", ".join(request.platforms)

    roadmap_summary = (
        f"For your {request.niche} niche and audience ({request.audience}), "
        f"the safest starting path is to validate product interest through content on {platform_text}. "
        f"Because your budget is {request.budget.lower()}, start with low-cost affiliate tests or simple digital offers "
        f"before moving into dropshipping, paid ads, or inventory-heavy setup in {request.region}."
    )

    return {
        "roadmap_summary": roadmap_summary,
        "affiliate_product_ideas": product_ideas["affiliate"],
        "dropshipping_product_ideas": product_ideas["dropshipping"],
        "best_product_fit": product_ideas["best_fit"],
        "content_promotion_plan": [
            "Create problem-aware content that explains the audience pain point.",
            "Create comparison or review content around 2-3 product options.",
            "Use short-form videos to test saves, comments, clicks, and direct messages.",
            "Add a clear CTA such as: 'Check the resource link in the description.'",
            "Use transparent affiliate disclosure when promoting affiliate links.",
            "Double down only on products that get engagement and clear audience interest.",
        ],
        "supplier_research_checklist": [
            "Check product reviews and customer complaints before choosing a supplier.",
            "Compare at least 3 suppliers or affiliate programs.",
            "Check shipping time, refund policy, and product quality signals.",
            "Avoid products with unclear claims, risky health promises, or poor reviews.",
            "Test the product or review trusted customer feedback before promotion.",
            "Make sure the product naturally fits your content niche and audience problem.",
        ],
        "thirty_day_roadmap": [
            "Week 1: Choose 2 product categories and create audience problem content.",
            "Week 2: Publish 5 short videos testing product-related angles.",
            "Week 3: Add affiliate disclosure, CTA, and track clicks, comments, saves, and DMs.",
            "Week 4: Review performance, keep the best product, and create a simple content-to-commerce funnel.",
        ],
        "risk_analysis": [
            "Affiliate or dropshipping success is not guaranteed; validate demand first.",
            "Dropshipping has more risk because of supplier quality, shipping time, and refunds.",
            "Affiliate content needs clear disclosure and honest product language.",
            "Do not overpromise results or use misleading claims.",
            "Start small before spending on ads, inventory, or complex store setup.",
        ],
        "ethical_disclosure": (
            "This content may contain affiliate links. If you buy through my link, "
            "I may earn a small commission at no extra cost to you."
        ),
        "next_best_action": (
            f"Pick one product from the {request.product_category} category, create 3 short-form videos around the audience problem, "
            "and measure saves, comments, clicks, and direct messages before building a full sales funnel."
        ),
        "data_note": (
            "MVP uses rule-based product recommendation logic with sample market signals. "
            "Future versions can connect live affiliate marketplace, e-commerce, Google Trends, and social trend APIs."
        ),
    }


class EthicalCheckRequest(BaseModel):
    """
    Request model for Ethical Monetization Checker.

    This collects promotional content and product claim context.
    The backend checks for common monetization risk signals.
    This is not legal advice. It is a responsible AI-style content safety helper.
    """

    content_text: str = Field(..., min_length=5)
    platform: str = Field(..., min_length=2)
    promotion_type: str = Field(..., min_length=2)
    has_affiliate_link: bool
    product_claim: str = Field(..., min_length=2)
    target_audience: str = Field(..., min_length=2)


def analyze_ethical_risks(request: EthicalCheckRequest) -> dict:
    """
    Analyze promotional content for ethical monetization risks.

    The MVP checks:
    - Missing affiliate disclosure
    - Overpromising language
    - Fake urgency
    - Clickbait wording
    - Risky income claims
    - Absolute product claims
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
        "secret hack",
    ]

    fake_urgency_words = [
        "buy now or regret",
        "only today",
        "last chance",
        "limited time",
        "act now",
        "don't miss this or",
    ]

    clickbait_words = [
        "shocking",
        "you won't believe",
        "must watch",
        "insane",
        "secret nobody tells",
        "this changed my life",
    ]

    risky_income_words = [
        "make money fast",
        "passive income guaranteed",
        "earn thousands overnight",
        "rich fast",
        "financial freedom guaranteed",
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
        issues.append("The content may need more balanced wording instead of absolute claims.")
        score -= 8

    score = max(score, 0)

    if score >= 85:
        risk_level = "Low Risk"
    elif score >= 65:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    disclosure_status = "Disclosure found" if has_disclosure else "Disclosure missing or unclear"

    return {
        "score": score,
        "risk_level": risk_level,
        "issues": issues if issues else ["No major ethical monetization issue detected in this MVP check."],
        "disclosure_status": disclosure_status,
    }


def build_safer_version(request: EthicalCheckRequest) -> str:
    """
    Build a safer, more transparent rewrite.

    This keeps the creator's original idea but reduces risky claims,
    pressure language, and guaranteed result wording.
    """

    safer_intro = "Here is a more transparent and platform-friendly version:\n\n"

    safer_body = (
        request.content_text
        .replace("will make you rich fast", "may help you organize your workflow or finances")
        .replace("guaranteed", "designed to help")
        .replace("100%", "potentially")
        .replace("instant results", "better results over time")
        .replace("Buy now", "Check if this fits your needs")
        .replace("buy now", "check if this fits your needs")
    )

    if request.has_affiliate_link:
        safer_body += (
            "\n\nDisclosure: This content may contain affiliate links. "
            "If you buy through my link, I may earn a small commission at no extra cost to you."
        )

    safer_body += "\n\nReminder: Results can vary based on your situation, effort, and product fit."

    return safer_intro + safer_body


@app.post("/ethical/check")
def check_ethical_monetization(request: EthicalCheckRequest):
    """
    Check promotional content for ethical monetization risks.

    Important:
    This endpoint gives creator-friendly risk guidance.
    It does not provide legal advice.
    """

    analysis = analyze_ethical_risks(request)

    return {
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
            f"For {request.platform}, keep promotional language transparent, clear, and audience-friendly."
        ),
        "data_note": (
            "This MVP uses rule-based ethical risk detection. Future versions can combine "
            "IBM Granite / watsonx reasoning with platform-specific policy guidance."
        ),
    }


class SevenAgentRequest(BaseModel):
    """
    Request model for the 7-Agent Creator Business Dashboard.

    This model collects the core creator business context.
    The backend will run seven AI-style business agents using this data.
    """

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


def clamp_score(score: int) -> int:
    """
    Keep every score safely between 0 and 100.
    """

    return max(0, min(score, 100))


def get_agent_status(score: int) -> str:
    """
    Convert a numeric score into a human-friendly status.
    """

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Strong"

    if score >= 55:
        return "Moderate"

    return "Needs Improvement"


def business_readiness_agent(request: SevenAgentRequest) -> dict:
    """
    Agent 1:
    Checks whether the creator is ready to move from content creation
    into a structured digital business.
    """

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

    score = clamp_score(score)

    return {
        "agent_name": "Creator Business Readiness",
        "score": score,
        "status": get_agent_status(score),
        "reason": (
            "This score estimates how ready the creator is to move from content creation "
            "into a structured digital business based on audience size, platform presence, "
            "business interest, and available execution time."
        ),
        "recommendation": (
            "Focus on one clear offer and validate demand before building a complex product."
        ),
        "next_action": (
            "Create a simple creator business profile and choose one product idea to test this week."
        ),
    }


def niche_product_fit_agent(request: SevenAgentRequest) -> dict:
    """
    Agent 2:
    Checks whether the product idea naturally fits the creator niche.
    """

    niche = request.creator_niche.lower()
    product = request.product_idea.lower()

    score = 60

    for word in niche.split():
        if len(word) > 3 and word in product:
            score += 12

    if any(item in product for item in ["template", "planner", "guide", "toolkit", "course"]):
        score += 12

    if "digital" in request.business_model.lower():
        score += 8

    score = clamp_score(score)

    return {
        "agent_name": "Niche-to-Product Fit",
        "score": score,
        "status": get_agent_status(score),
        "reason": (
            "This score checks whether the product idea naturally connects with the creator niche "
            "and whether it can be explained through content."
        ),
        "recommendation": (
            "Choose products that solve a clear audience problem and can be promoted naturally through educational content."
        ),
        "next_action": (
            "Write one sentence explaining exactly why your audience needs this product."
        ),
    }


def audience_market_match_agent(request: SevenAgentRequest) -> dict:
    """
    Agent 3:
    Estimates audience-to-market match using niche, audience, region,
    product idea, and platform mix.
    """

    niche = request.creator_niche.lower()
    product = request.product_idea.lower()
    audience = request.audience.lower()
    region = request.region.lower()

    score = 58

    high_signal_niches = [
        "finance",
        "fitness",
        "beauty",
        "creator",
        "ai",
        "productivity",
        "marketing",
        "business",
    ]

    if any(item in niche for item in high_signal_niches):
        score += 15

    if any(item in product for item in ["planner", "template", "tool", "guide", "kit", "course"]):
        score += 10

    if "usa" in audience or "united states" in region:
        score += 8

    if len(request.platforms) >= 3:
        score += 5

    score = clamp_score(score)

    return {
        "agent_name": "Audience-to-Market Matching",
        "score": score,
        "status": get_agent_status(score),
        "reason": (
            "This score estimates how well the target audience, region, product idea, and platform mix "
            "match a realistic market opportunity."
        ),
        "recommendation": (
            "Use content to test buying interest before spending on ads, inventory, or complex funnels."
        ),
        "next_action": (
            "Run one audience poll and publish 3 product-related short videos to measure interest."
        ),
    }


def content_commerce_roadmap_agent(request: SevenAgentRequest) -> dict:
    """
    Agent 4:
    Builds a content-to-commerce roadmap.
    """

    score = 82

    return {
        "agent_name": "Content-to-Commerce Roadmap",
        "score": score,
        "status": get_agent_status(score),
        "reason": (
            "The content-to-commerce path is strong when the creator can educate the audience, "
            "build trust, introduce the product naturally, and track response."
        ),
        "recommendation": (
            "Build a simple funnel: awareness content → trust content → product mention → ethical CTA → validation tracking."
        ),
        "next_action": (
            "Create 5 short-form videos: 2 problem-aware, 2 educational, and 1 soft product introduction."
        ),
        "roadmap_steps": [
            "Step 1: Identify the audience problem behind the product.",
            "Step 2: Create awareness content that explains the problem.",
            "Step 3: Build trust with educational short-form content.",
            "Step 4: Introduce the product as one possible solution.",
            "Step 5: Add transparent disclosure and a simple CTA.",
            "Step 6: Track saves, comments, clicks, and direct messages.",
        ],
    }


def ethical_monetization_agent(request: SevenAgentRequest) -> dict:
    """
    Agent 5:
    Checks promotion copy for basic ethical monetization risk.
    """

    text = request.promotion_copy.lower()

    score = 100
    issues = []

    if "affiliate" not in text and "commission" not in text and "sponsored" not in text:
        score -= 20
        issues.append("Affiliate or sponsorship disclosure may be missing.")

    risky_phrases = [
        "guaranteed",
        "make you rich",
        "instant results",
        "100%",
        "no risk",
        "rich fast",
        "earn thousands overnight",
    ]

    if any(phrase in text for phrase in risky_phrases):
        score -= 25
        issues.append("Promotion copy may contain overpromising or risky claim language.")

    if "buy now or regret" in text or "last chance" in text:
        score -= 10
        issues.append("Promotion copy may contain pressure-based urgency.")

    score = clamp_score(score)

    if not issues:
        issues.append("No major ethical risk detected in this MVP check.")

    return {
        "agent_name": "Ethical Monetization Checker",
        "score": score,
        "status": get_agent_status(score),
        "reason": (
            "This agent checks whether promotional content is transparent, avoids overpromising, "
            "and includes disclosure when monetization links are used."
        ),
        "recommendation": (
            "Use clear affiliate disclosure, avoid guaranteed results, and explain limitations honestly."
        ),
        "next_action": "Add a disclosure line before publishing promotional content.",
        "issues_found": issues,
        "recommended_disclosure": (
            "This content may contain affiliate links. If you buy through my link, "
            "I may earn a small commission at no extra cost to you."
        ),
    }


def product_validation_checklist_agent(request: SevenAgentRequest) -> dict:
    """
    Agent 6:
    Creates a product validation checklist and validation score.
    """

    score = 78
    product = request.product_idea.lower()

    if "template" in product or "planner" in product:
        score += 8

    if "digital" in request.business_model.lower():
        score += 5

    score = clamp_score(score)

    return {
        "agent_name": "Product Validation Checklist",
        "score": score,
        "status": get_agent_status(score),
        "reason": (
            "This agent checks whether the product can be validated before full launch using audience signals and content tests."
        ),
        "recommendation": (
            "Validate demand before building the full product. Start with a small MVP or simple offer."
        ),
        "next_action": "Create a validation checklist and complete it before launch.",
        "checklist": [
            "Audience problem is clearly defined.",
            "Product solves one specific problem.",
            "Product can be explained in short-form content.",
            "Low-cost test is possible.",
            "Audience poll or comment test is planned.",
            "Competitor pricing is checked.",
            "Ethical disclosure is ready if affiliate links are used.",
        ],
    }


def six_month_roadmap_agent(request: SevenAgentRequest) -> dict:
    """
    Agent 7:
    Creates a six-month creator-to-business roadmap.
    """

    score = 84

    return {
        "agent_name": "6-Month Creator-to-Business Roadmap",
        "score": score,
        "status": get_agent_status(score),
        "reason": (
            "A six-month roadmap helps the creator move from random content creation into a structured business-building process."
        ),
        "recommendation": (
            "Follow a validation-first roadmap: clarify niche, test content, validate product, launch small, improve, then scale."
        ),
        "next_action": (
            "Start Month 1 by defining content pillars and testing audience pain points."
        ),
        "roadmap": [
            "Month 1: Clarify niche, audience problem, and content pillars.",
            "Month 2: Publish 20-30 short-form videos and test product-related topics.",
            "Month 3: Validate one product idea using comments, polls, and a waitlist.",
            "Month 4: Launch a small MVP product, affiliate offer, or digital template.",
            "Month 5: Improve offer based on real audience response and conversion data.",
            "Month 6: Scale through collaborations, email list, partnerships, and better content funnels.",
        ],
    }


@app.post("/agents/run")
def run_seven_agent_dashboard(request: SevenAgentRequest):
    """
    Run all 7 creator business agents and return one unified report.

    Important:
    This does not guarantee income.
    It gives an estimated, validation-first creator business roadmap.
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

    business_readiness = agent_results[0]["score"]
    product_fit = agent_results[1]["score"]
    market_match = agent_results[2]["score"]
    content_commerce = agent_results[3]["score"]
    ethical_safety = agent_results[4]["score"]
    product_validation = agent_results[5]["score"]

    overall_score = round(
        business_readiness * 0.20
        + product_fit * 0.20
        + market_match * 0.20
        + content_commerce * 0.15
        + product_validation * 0.15
        + ethical_safety * 0.10
    )

    executive_summary = (
        f"CreatorCareer AI analyzed your {request.creator_niche} creator business idea for "
        f"{request.audience}. Your product idea, '{request.product_idea}', shows an estimated "
        f"overall business opportunity score of {overall_score}/100. This is not a guarantee of income, "
        f"but it gives a structured validation-first roadmap for turning content into a digital business."
    )

    return {
        "overall_business_opportunity_score": overall_score,
        "executive_summary": executive_summary,
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
        "data_note": (
            "MVP uses rule-based agent logic and sample market signals. Future versions can connect "
            "IBM Granite / watsonx reasoning, live market APIs, affiliate marketplace APIs, and Supabase/PostgreSQL history."
        ),
    }


class ReportGenerateRequest(BaseModel):
    """
    Request model for generating a CreatorCareer AI PDF report.

    This is the information the frontend sends to the backend.
    Later, this can be combined with saved 7-agent results from Supabase.
    """

    creator_name: str = Field(..., min_length=2)
    creator_niche: str = Field(..., min_length=2)
    audience: str = Field(..., min_length=2)
    region: str = Field(..., min_length=2)
    platforms: List[str]
    product_idea: str = Field(..., min_length=2)
    business_model: str = Field(..., min_length=2)
    income_goal: str = Field(..., min_length=1)


def clean_file_part(value: str) -> str:
    """
    Create a safe filename part from user input.

    Example:
    'Alex Morgan' -> 'alex-morgan'
    """

    safe = "".join(
        character.lower() if character.isalnum() else "-"
        for character in value.strip()
    )

    # Remove empty parts created by repeated spaces or symbols.
    safe = "-".join(part for part in safe.split("-") if part)

    return safe or "creator"


def build_report_sections(request: ReportGenerateRequest) -> dict:
    """
    Build the content sections used inside the PDF report.

    For the MVP, this uses static scoring and report sections.
    Later, these values can be pulled from the real /agents/run output
    and saved report history.
    """

    platforms_text = ", ".join(request.platforms)

    profile_summary = (
        f"{escape(request.creator_name)} is building a creator business in the "
        f"{escape(request.creator_niche)} niche for {escape(request.audience)} in "
        f"{escape(request.region)}. The selected platforms are {escape(platforms_text)}. "
        f"The current business direction is {escape(request.business_model)}, with a goal of "
        f"{escape(request.income_goal)}."
    )

    agent_summary = [
        ["Agent", "Score", "Status"],
        ["Creator Business Readiness", "82/100", "Strong"],
        ["Niche-to-Product Fit", "86/100", "Excellent"],
        ["Audience-to-Market Match", "84/100", "Strong"],
        ["Content-to-Commerce Roadmap", "82/100", "Strong"],
        ["Ethical Monetization Checker", "80/100", "Strong"],
        ["Product Validation Checklist", "86/100", "Excellent"],
        ["6-Month Creator Roadmap", "84/100", "Strong"],
    ]

    next_7_days_plan = [
        "Day 1: Define the exact audience problem the product solves.",
        "Day 2: Create 3 short-form content hooks around that problem.",
        "Day 3: Publish one educational video and ask for audience feedback.",
        "Day 4: Run a poll or comment-based validation test.",
        "Day 5: Draft the first MVP version of the product or affiliate offer.",
        "Day 6: Add clear disclosure and prepare a simple call to action.",
        "Day 7: Review engagement signals and decide whether to continue, adjust, or pause.",
    ]

    six_month_roadmap = [
        "Month 1: Clarify niche, audience problem, and content pillars.",
        "Month 2: Publish 20-30 short-form videos and test product-related topics.",
        "Month 3: Validate one product idea using comments, polls, and a waitlist.",
        "Month 4: Launch a small MVP product, affiliate offer, or digital template.",
        "Month 5: Improve the offer based on real audience response and conversion data.",
        "Month 6: Scale through collaborations, email list, partnerships, and better content funnels.",
    ]

    return {
        "overall_score": 84,
        "profile_summary": profile_summary,
        "agent_summary": agent_summary,
        "product_validation_summary": (
            f"The product idea '{escape(request.product_idea)}' shows strong validation potential. "
            "It should be tested with short-form educational content, audience polls, and a small MVP before scaling."
        ),
        "ethical_note": (
            "CreatorCareer AI recommends using clear affiliate disclosure, avoiding guaranteed income claims, "
            "and explaining product limitations honestly before publishing promotional content."
        ),
        "next_7_days_plan": next_7_days_plan,
        "six_month_roadmap": six_month_roadmap,
        "mvp_data_note": (
            "This MVP report uses rule-based scoring and sample market signals. Future versions can connect "
            "IBM Granite/watsonx reasoning, Supabase/PostgreSQL saved reports, and live market APIs."
        ),
    }


def add_section_title(story, title: str, styles) -> None:
    """
    Add a consistent section title to the PDF story.
    """

    story.append(Spacer(1, 12))
    story.append(Paragraph(title, styles["SectionTitle"]))
    story.append(Spacer(1, 8))


def add_bullet_list(story, items: List[str], styles) -> None:
    """
    Add a readable bullet-style list to the PDF.
    """

    for item in items:
        story.append(Paragraph(f"- {escape(item)}", styles["BodyText"]))
        story.append(Spacer(1, 5))


def generate_pdf_report(request: ReportGenerateRequest, file_path: Path) -> None:
    """
    Generate the actual PDF file using ReportLab.

    The PDF is saved into backend/reports.
    The frontend receives a download URL after generation.
    """

    report = build_report_sections(request)

    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=letter,
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontSize=26,
            leading=32,
            textColor=colors.HexColor("#111827"),
            spaceAfter=16,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontSize=15,
            leading=20,
            textColor=colors.HexColor("#4C1D95"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallNote",
            parent=styles["BodyText"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#4B5563"),
        )
    )

    story = []

    story.append(Paragraph("CreatorCareer AI", styles["CoverTitle"]))
    story.append(Paragraph("7-Agent Creator Business Report", styles["Heading2"]))
    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Generated for: <b>{escape(request.creator_name)}</b><br/>"
            f"Niche: <b>{escape(request.creator_niche)}</b><br/>"
            f"Product Idea: <b>{escape(request.product_idea)}</b><br/>"
            f"Generated on: {datetime.now().strftime('%B %d, %Y')}",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 18))

    score_table = Table(
        [["Overall Business Opportunity Score", f"{report['overall_score']}/100"]],
        colWidths=[330, 130],
    )

    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F3FF")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111827")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#7C3AED")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 14),
                ("ALIGN", (1, 0), (1, 0), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
            ]
        )
    )

    story.append(score_table)

    add_section_title(story, "1. Creator Profile Summary", styles)
    story.append(Paragraph(report["profile_summary"], styles["BodyText"]))

    add_section_title(story, "2. 7-Agent Analysis Summary", styles)

    agent_table = Table(report["agent_summary"], colWidths=[260, 95, 105])
    agent_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4C1D95")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FAFAFA")),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(agent_table)

    add_section_title(story, "3. Product Validation Summary", styles)
    story.append(Paragraph(report["product_validation_summary"], styles["BodyText"]))

    add_section_title(story, "4. Ethical Monetization Note", styles)
    story.append(Paragraph(report["ethical_note"], styles["BodyText"]))

    add_section_title(story, "5. Next 7 Days Action Plan", styles)
    add_bullet_list(story, report["next_7_days_plan"], styles)

    add_section_title(story, "6. 6-Month Creator-to-Business Roadmap", styles)
    add_bullet_list(story, report["six_month_roadmap"], styles)

    add_section_title(story, "7. MVP Data Note", styles)
    story.append(Paragraph(report["mvp_data_note"], styles["SmallNote"]))

    story.append(Spacer(1, 14))
    story.append(
        Paragraph(
            "Disclaimer: This report provides educational and strategic guidance only. "
            "It does not guarantee income, sales, platform growth, or business success.",
            styles["SmallNote"],
        )
    )

    doc.build(story)


@app.post("/report/generate")
def generate_report(request: ReportGenerateRequest):
    """
    Generate a CreatorCareer AI PDF report and return the download URL.
    """

    safe_name = clean_file_part(request.creator_name)
    file_name = f"creatorcareer-report-{safe_name}-{uuid.uuid4().hex[:8]}.pdf"
    file_path = reports_dir / file_name

    generate_pdf_report(request, file_path)

    return {
        "status": "success",
        "message": "PDF report generated successfully.",
        "file_name": file_name,
        "download_url": f"http://localhost:8000/reports/{file_name}",
    }


@app.get("/db/health")
def database_health_check():
    """
    Test Supabase database connection.

    This route reads latest creators from the creators table.
    If this works, backend can read from Supabase.

    Important:
    get_recent_records() returns a list.
    So we must return creators directly.
    Do not use creators["data"] here.
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


@app.post("/db/test-creator")
def create_test_creator():
    """
    Insert one test creator into Supabase.

    This confirms that the backend can write data into the creators table.

    Important:
    insert_record() returns a dictionary:
    {
      "status": "success",
      "table": "...",
      "data": [...]
    }

    So we return saved_creator directly.
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
    



