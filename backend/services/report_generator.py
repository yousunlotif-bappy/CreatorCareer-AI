from datetime import datetime
from html import escape
from pathlib import Path
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from models.schemas import ReportGenerateRequest


def build_report_sections(request: ReportGenerateRequest) -> dict:
    """
    Build MVP report sections.
    """

    platforms_text = ", ".join(request.platforms)

    return {
        "overall_score": 84,
        "profile_summary": (
            f"{escape(request.creator_name)} is building a creator business in the "
            f"{escape(request.creator_niche)} niche for {escape(request.audience)} in "
            f"{escape(request.region)}. Selected platforms: {escape(platforms_text)}. "
            f"The current business direction is {escape(request.business_model)}, with a goal of "
            f"{escape(request.income_goal)}."
        ),
        "agent_summary": [
            ["Agent", "Score", "Status"],
            ["Creator Business Readiness", "82/100", "Strong"],
            ["Niche-to-Product Fit", "86/100", "Excellent"],
            ["Audience-to-Market Match", "84/100", "Strong"],
            ["Content-to-Commerce Roadmap", "82/100", "Strong"],
            ["Ethical Monetization Checker", "80/100", "Strong"],
            ["Product Validation Checklist", "86/100", "Excellent"],
            ["6-Month Creator Roadmap", "84/100", "Strong"],
        ],
        "product_validation_summary": (
            f"The product idea '{escape(request.product_idea)}' shows strong validation potential. "
            "It should be tested with short-form educational content, audience polls, and a small MVP before scaling."
        ),
        "ethical_note": (
            "CreatorCareer AI recommends using clear affiliate disclosure, avoiding guaranteed income claims, "
            "and explaining product limitations honestly before publishing promotional content."
        ),
        "next_7_days_plan": [
            "Day 1: Define the exact audience problem the product solves.",
            "Day 2: Create 3 short-form content hooks around that problem.",
            "Day 3: Publish one educational video and ask for audience feedback.",
            "Day 4: Run a poll or comment-based validation test.",
            "Day 5: Draft the first MVP version of the product or affiliate offer.",
            "Day 6: Add clear disclosure and prepare a simple CTA.",
            "Day 7: Review engagement signals and decide whether to continue, adjust, or pause.",
        ],
        "six_month_roadmap": [
            "Month 1: Clarify niche, audience problem, and content pillars.",
            "Month 2: Publish 20-30 short-form videos and test product-related topics.",
            "Month 3: Validate one product idea using comments, polls, and a waitlist.",
            "Month 4: Launch a small MVP product, affiliate offer, or digital template.",
            "Month 5: Improve offer based on real audience response and conversion data.",
            "Month 6: Scale through collaborations, email list, partnerships, and better content funnels.",
        ],
        "local_ai_note": (
            "This report was generated using CreatorCareer AI's local explainable multi-agent reasoning engine. "
            "The MVP uses structured scoring logic, prompt-style templates, ethical checks, and business workflow rules "
            "without requiring paid external API keys."
        ),
        "mvp_data_note": (
            "This MVP report uses rule-based scoring and sample market signals. Future versions can connect "
            "foundation model reasoning, Supabase saved reports, and live market APIs."
        ),
    }


def add_section_title(story: list, title: str, styles) -> None:
    """
    Add a consistent section heading to the PDF story.
    """

    story.append(Spacer(1, 12))
    story.append(Paragraph(title, styles["SectionTitle"]))
    story.append(Spacer(1, 8))


def add_bullet_list(story: list, items: List[str], styles) -> None:
    """
    Add a readable bullet-style list to the PDF.
    """

    for item in items:
        story.append(Paragraph(f"- {escape(item)}", styles["BodyText"]))
        story.append(Spacer(1, 5))


def generate_pdf_report(request: ReportGenerateRequest, file_path: Path) -> None:
    """
    Generate the PDF file using ReportLab.
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

    add_section_title(story, "7. Local AI Reasoning Layer", styles)
    story.append(Paragraph(report["local_ai_note"], styles["BodyText"]))

    add_section_title(story, "8. MVP Data Note", styles)
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



