"""
CreatorCareer AI - AI Service Layer

This layer tries IBM Granite locally through Ollama + LangChain first.
If Granite/Ollama is unavailable, it safely falls back to explainable
local AI-style summaries so the demo remains stable.
"""

import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

from services.local_llm_service import check_ollama_server, generate_with_granite


BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


def is_ai_enabled() -> bool:
    """
    Check whether the AI layer is enabled.
    """

    return os.getenv("AI_ENABLED", "true").strip().lower() in {
        "true",
        "1",
        "yes",
        "on",
    }


def get_ai_provider_name() -> str:
    """
    Return the configured AI provider label.
    """

    return os.getenv(
        "AI_PROVIDER",
        "IBM Granite Local + CreatorCareer Fallback Engine",
    )


def get_ai_engine_name() -> str:
    """
    Return the configured AI engine label.
    """

    return os.getenv("AI_ENGINE", "granite_ollama")


def get_ai_config_status() -> Dict[str, Any]:
    """
    Return safe AI configuration status for /ai/health.
    """

    return {
        "ai_enabled": is_ai_enabled(),
        "ai_engine": get_ai_engine_name(),
        "ai_provider": get_ai_provider_name(),
        "requires_external_api_key": False,
        "requires_billing": False,
        "mode": "granite_ollama_with_safe_fallback",
        "watsonx_enabled": False,
        "env_file": str(ENV_PATH),
        "local_llm": check_ollama_server(),
    }


def build_content_prompt_template(payload: dict) -> str:
    return f"""
You are CreatorCareer AI, a creator business assistant.

Task:
Give a short AI reasoning summary for this content package.

Input:
Topic: {payload.get("topic")}
Platform: {payload.get("platform")}
Audience: {payload.get("audience")}
Tone: {payload.get("tone")}
Duration: {payload.get("duration")}
Language: {payload.get("language")}
Content Goal: {payload.get("content_goal")}

Rules:
- Do not promise guaranteed views, followers, income, or sales.
- Focus on ethical creator strategy.
- Keep the answer short and practical.
"""


def build_market_prompt_template(payload: dict) -> str:
    return f"""
You are CreatorCareer AI, a creator business market assistant.

Task:
Give a short market reasoning summary.

Input:
Niche: {payload.get("niche")}
Audience: {payload.get("audience")}
Region: {payload.get("region")}
Platforms: {payload.get("platforms")}
Business Type: {payload.get("business_type")}
Budget: {payload.get("budget")}
Product Interest: {payload.get("product_interest")}

Rules:
- Use validation-first wording.
- Do not guarantee income or sales.
- Keep the answer practical.
"""


def build_product_prompt_template(payload: dict) -> str:
    return f"""
You are CreatorCareer AI, a product validation assistant.

Task:
Give a short product validation reasoning summary.

Input:
Product: {payload.get("product_name")}
Niche: {payload.get("niche")}
Audience: {payload.get("audience")}
Platform: {payload.get("platform")}
Business Model: {payload.get("business_model")}
Budget: {payload.get("budget")}
Product Type: {payload.get("product_type")}
Promotion Style: {payload.get("promotion_style")}

Rules:
- Explain validation logic.
- Mention risk.
- Do not guarantee sales or success.
"""


def build_affiliate_prompt_template(payload: dict) -> str:
    return f"""
You are CreatorCareer AI, an affiliate and dropshipping roadmap assistant.

Task:
Give a short reasoning summary for this creator monetization roadmap.

Input:
Niche: {payload.get("niche")}
Audience: {payload.get("audience")}
Region: {payload.get("region")}
Platforms: {payload.get("platforms")}
Business Type: {payload.get("business_type")}
Budget: {payload.get("budget")}
Product Category: {payload.get("product_category")}
Content Style: {payload.get("content_style")}

Rules:
- Recommend validation-first monetization.
- Mention transparency and affiliate disclosure.
- Do not guarantee sales or income.
"""


def build_ethical_prompt_template(payload: dict) -> str:
    return f"""
You are CreatorCareer AI, an ethical monetization checker.

Task:
Give a short ethical monetization reasoning summary.

Input:
Content Text: {payload.get("content_text")}
Platform: {payload.get("platform")}
Promotion Type: {payload.get("promotion_type")}
Has Affiliate Link: {payload.get("has_affiliate_link")}
Product Claim: {payload.get("product_claim")}
Target Audience: {payload.get("target_audience")}

Rules:
- Focus on disclosure, transparency, and realistic wording.
- Avoid fake urgency and guaranteed claims.
"""


def build_agent_prompt_template(payload: dict) -> str:
    return f"""
You are CreatorCareer AI, a 7-agent creator business intelligence system.

Task:
Give a short executive AI reasoning summary.

Input:
Creator Niche: {payload.get("creator_niche")}
Audience: {payload.get("audience")}
Region: {payload.get("region")}
Platforms: {payload.get("platforms")}
Followers: {payload.get("followers")}
Product Idea: {payload.get("product_idea")}
Business Model: {payload.get("business_model")}
Income Goal: {payload.get("income_goal")}
Available Time: {payload.get("available_time")}

Agents:
1. Creator Business Readiness
2. Niche-to-Product Fit
3. Audience-to-Market Matching
4. Content-to-Commerce Roadmap
5. Ethical Monetization Checker
6. Product Validation Checklist
7. 6-Month Roadmap

Rules:
- Give practical business guidance.
- Do not guarantee income, views, followers, or sales.
"""


def build_report_prompt_template(payload: dict) -> str:
    return f"""
You are CreatorCareer AI, a creator business report assistant.

Task:
Give a short summary explaining what this PDF report helps the creator understand.

Input:
Creator Name: {payload.get("creator_name")}
Creator Niche: {payload.get("creator_niche")}
Audience: {payload.get("audience")}
Region: {payload.get("region")}
Product Idea: {payload.get("product_idea")}
Business Model: {payload.get("business_model")}
Income Goal: {payload.get("income_goal")}

Rules:
- Explain the report value.
- Do not guarantee income or business success.
"""


def build_prompt(module_name: str, payload: dict) -> str:
    """
    Select the best prompt template for each module.
    """

    if module_name == "content":
        return build_content_prompt_template(payload)

    if module_name == "market":
        return build_market_prompt_template(payload)

    if module_name == "product":
        return build_product_prompt_template(payload)

    if module_name == "affiliate":
        return build_affiliate_prompt_template(payload)

    if module_name == "ethical":
        return build_ethical_prompt_template(payload)

    if module_name == "agents":
        return build_agent_prompt_template(payload)

    if module_name == "report":
        return build_report_prompt_template(payload)

    return "Give a short practical CreatorCareer AI business reasoning summary."


def build_fallback_summary(module_name: str, payload: dict) -> str:
    """
    Safe fallback summary when Granite/Ollama is unavailable.
    """

    if module_name == "content":
        return (
            f"CreatorCareer AI analyzed '{payload.get('topic')}' for "
            f"{payload.get('platform')} and the audience '{payload.get('audience')}'. "
            "The content package focuses on trust, practical value, and ethical creator strategy."
        )

    if module_name == "market":
        return (
            f"CreatorCareer AI reviewed the '{payload.get('niche')}' niche using local market reasoning. "
            "The safest next step is to validate demand with low-cost content experiments before spending heavily."
        )

    if module_name == "product":
        return (
            f"CreatorCareer AI reviewed the product idea '{payload.get('product_name')}'. "
            "The score supports decision-making, but it is not a guarantee of sales or business success."
        )

    if module_name == "affiliate":
        return (
            f"CreatorCareer AI reviewed affiliate and dropshipping opportunities for '{payload.get('niche')}'. "
            "The safest path is to validate product interest before investing in inventory, ads, or complex funnels."
        )

    if module_name == "ethical":
        return (
            "CreatorCareer AI checked the monetization copy for disclosure, overpromising, fake urgency, "
            "and risky income claims. Transparent disclosure and realistic wording are recommended."
        )

    if module_name == "agents":
        return (
            f"CreatorCareer AI ran a 7-agent business analysis for '{payload.get('creator_niche')}' "
            f"and product idea '{payload.get('product_idea')}'. The output supports validation-first planning."
        )

    if module_name == "report":
        return (
            f"CreatorCareer AI generated a PDF report for '{payload.get('creator_name')}' to summarize "
            "creator positioning, product validation, ethical monetization guidance, and roadmap planning."
        )

    return "CreatorCareer AI generated structured business guidance using the local fallback engine."


def generate_local_ai_response(module_name: str, payload: dict) -> Dict[str, Any]:
    """
    Main AI response function used by backend routes.

    It tries IBM Granite locally first.
    If Granite/Ollama fails, it returns a safe fallback response.
    """

    prompt_template = build_prompt(module_name, payload)
    fallback_summary = build_fallback_summary(module_name, payload)

    if not is_ai_enabled():
        return {
            "ai_provider": get_ai_provider_name(),
            "ai_engine": get_ai_engine_name(),
            "ai_used": False,
            "requires_external_api_key": False,
            "requires_billing": False,
            "ai_summary": "AI layer is disabled by AI_ENABLED=false.",
            "ai_note": "Enable AI_ENABLED=true in backend/.env.",
            "ai_prompt_template": prompt_template.strip(),
            "granite_used": False,
            "llm_model": None,
            "llm_error": None,
        }

    granite_result = generate_with_granite(prompt_template)

    if granite_result["success"]:
        return {
            "ai_provider": granite_result["provider"],
            "ai_engine": get_ai_engine_name(),
            "ai_used": True,
            "requires_external_api_key": False,
            "requires_billing": False,
            "ai_summary": granite_result["text"],
            "ai_note": (
                "This response was enhanced using IBM Granite open-source model locally through "
                "Ollama with LangChain. No watsonx billing or external API key is required."
            ),
            "ai_prompt_template": prompt_template.strip(),
            "granite_used": True,
            "llm_model": granite_result["model"],
            "llm_error": None,
        }

    return {
        "ai_provider": "CreatorCareer Local Fallback Engine",
        "ai_engine": get_ai_engine_name(),
        "ai_used": True,
        "requires_external_api_key": False,
        "requires_billing": False,
        "ai_summary": fallback_summary,
        "ai_note": (
            "Granite/Ollama was unavailable, so CreatorCareer AI used the safe local fallback engine. "
            "The app remains stable for demo."
        ),
        "ai_prompt_template": prompt_template.strip(),
        "granite_used": False,
        "llm_model": granite_result["model"],
        "llm_error": granite_result["error"],
    }



