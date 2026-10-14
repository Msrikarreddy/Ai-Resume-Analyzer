
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)
from xml.sax.saxutils import escape


def generate_pdf_report(
    skill_score,
    semantic_score,
    overall_score,
    matched_skills,
    missing_skills,
    recommendations,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph("AI Resume Analyzer Report", styles["Title"])
    )
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "Resume analysis results",
            styles["Heading2"],
        )
    )
    story.append(HRFlowable(width="100%", color=colors.grey))
    story.append(Spacer(1, 12))

    if overall_score is not None:
        story.append(
            Paragraph(
                f"Overall Match Score: {overall_score:.2f}%",
                styles["Normal"],
            )
        )

    if skill_score is not None:
        story.append(
            Paragraph(
                f"Required Skill Coverage: {skill_score:.1f}%",
                styles["Normal"],
            )
        )

    story.append(
        Paragraph(
            f"Semantic Similarity: {semantic_score:.2f}%",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 16))

    story.append(
        Paragraph("Matched Skills", styles["Heading2"])
    )

    if matched_skills:
        for skill in matched_skills:
            story.append(
                Paragraph(f"- {escape(skill)}", styles["Normal"])
            )
    else:
        story.append(
            Paragraph("No recognized matching skills found.",
                      styles["Normal"])
        )

    story.append(Spacer(1, 12))
    story.append(
        Paragraph("Potential Skill Gaps", styles["Heading2"])
    )

    if missing_skills:
        for skill in missing_skills:
            story.append(
                Paragraph(f"- {escape(skill)}", styles["Normal"])
            )
    else:
        story.append(
            Paragraph("No recognized skill gaps detected.",
                      styles["Normal"])
        )

    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "Resume Improvement Suggestions",
            styles["Heading2"],
        )
    )

    for recommendation in recommendations:
        story.append(
            Paragraph(
                f"- {escape(recommendation)}",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 16))
    story.append(
        Paragraph(
            "Disclaimer: These scores are prototype text-matching "
            "metrics, not a probability of getting a job or a "
            "validated measure of candidate suitability.",
            styles["Italic"],
        )
    )

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()