
def generate_recommendations(missing_skills, matched_skills):
    recommendations = []

    if missing_skills:
        recommendations.append(
            "Review these job-description skills that "
            "were not detected in your resume: "
            + ", ".join(missing_skills)
            + ". Add them only if they accurately reflect "
            "your skills or experience."
        )
    else:
        recommendations.append(
            "No missing skills were detected from the "
            "recognized skill dictionary. Review the job "
            "requirements manually for completeness."
        )

    if matched_skills:
        recommendations.append(
            "Highlight your matching skills in your "
            "professional summary and relevant project "
            "descriptions, using concrete examples."
        )
    else:
        recommendations.append(
            "Review your projects and work experience to "
            "identify relevant skills supported by evidence."
        )

    recommendations.append(
        "Add measurable project outcomes where possible, "
        "such as processing time reduced, model accuracy "
        "measured, or users supported. Use only truthful "
        "results you can substantiate."
    )

    return recommendations