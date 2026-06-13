from typing import List

from fastapi import APIRouter

from models.schemas import ContentPackageRequest
from routes.utils import attach_database_result, clean_optional_uuid, save_record_safely
from services.ai_service import generate_local_ai_response


router = APIRouter(prefix="/content", tags=["Content Package"])


def build_hashtags(topic: str, platform: str) -> List[str]:
    """
    Build simple hashtags from topic and platform.
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

    return list(dict.fromkeys(base_tags + topic_tags))


def build_scene_breakdown(request: ContentPackageRequest) -> List[str]:
    """
    Build a simple scene plan for AI video or short-form content.
    """

    reference = request.story_or_video_reference or "No external reference provided"
    video_style = request.video_style or "short-form educational video"

    return [
        f"Scene 1: Start with a fast visual hook about {request.topic}.",
        f"Scene 2: Show why this topic matters for {request.audience}.",
        f"Scene 3: Add a simple example based on this reference: {reference}.",
        f"Scene 4: Explain the solution in a {request.tone.lower()} tone.",
        f"Scene 5: End with a clear call to action for a {video_style}.",
    ]


@router.post("/package")
def generate_content_package(request: ContentPackageRequest):
    """
    Generate a complete AI-style content package and save it when possible.
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

    content_goal_lower = request.content_goal.lower()

    if "sell" in content_goal_lower or "conversion" in content_goal_lower:
        cta = "Comment your niche and start building your creator business roadmap."
    elif "awareness" in content_goal_lower:
        cta = "Save this and use it for your next content plan."
    else:
        cta = "Follow for more creator growth and digital business ideas."

    result = {
        "titles": titles,
        "hook": hook,
        "voiceover_script": voiceover_script,
        "caption": caption,
        "hashtags": build_hashtags(request.topic, request.platform),
        "thumbnail_text": [
            "Stop Posting Randomly",
            "Turn Content Into Business",
            "Creator Growth Roadmap",
            "Create Smarter",
        ],
        "cta": cta,
        "platform_notes": (
            f"For {request.platform}, keep the opening fast, use short lines, "
            f"add subtitles, and place the strongest idea in the first 3 seconds."
        ),
        "scene_breakdown": build_scene_breakdown(request),
        "video_generation_prompt": (
            f"Create a {request.duration} {request.video_style or 'vertical short-form'} video for {request.platform}. "
            f"Topic: {request.topic}. Audience: {request.audience}. Tone: {request.tone.lower()}."
        ),
        "b_roll_ideas": [
            "Close-up creator talking to camera",
            "Text overlay showing the main mistake or problem",
            "Screen recording or simple visual example",
            "Before vs after comparison",
            "Final CTA screen with bold thumbnail-style text",
        ],
        "editing_notes": [
            "Use vertical 9:16 format",
            "Keep the first 3 seconds visually strong",
            "Add large readable subtitles",
            "Use quick cuts every 2-3 seconds",
            "End with CTA text on screen",
        ],
        "status": "MVP generated output. Ready for future foundation model integration.",
    }

    ai_result = generate_local_ai_response(
        module_name="content",
        payload={
            "topic": request.topic,
            "platform": request.platform,
            "audience": request.audience,
            "tone": request.tone,
            "duration": request.duration,
            "language": request.language,
            "content_goal": request.content_goal,
        },
    )
    result.update(ai_result)

    database_payload = {
        "creator_id": clean_optional_uuid(request.creator_id),
        "topic": request.topic,
        "platform": request.platform,
        "audience": request.audience,
        "tone": request.tone,
        "duration": request.duration,
        "language": request.language,
        "content_goal": request.content_goal,
        "titles": result["titles"],
        "hook": result["hook"],
        "voiceover_script": result["voiceover_script"],
        "caption": result["caption"],
        "hashtags": result["hashtags"],
        "thumbnail_text": result["thumbnail_text"],
        "cta": result["cta"],
        "platform_notes": result["platform_notes"],
        "scene_breakdown": result["scene_breakdown"],
        "video_generation_prompt": result["video_generation_prompt"],
        "b_roll_ideas": result["b_roll_ideas"],
        "editing_notes": result["editing_notes"],
    }

    db_result = save_record_safely("content_outputs", database_payload)

    return attach_database_result(result, db_result)



