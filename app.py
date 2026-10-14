
import streamlit as st

from resume_parser import extract_resume_text
from matcher import compare_skills
from semantic_matcher import calculate_semantic_similarity
from recommendations import generate_recommendations
from report_generator import generate_pdf_report
from ai_recommender import generate_ai_recommendations


# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# --------------------------------------------------
# 2. Application Header
# --------------------------------------------------

st.title("📄 AI Resume Analyzer")

st.markdown(
    """
    ### Your resume. Your next opportunity.

    Analyze your resume against a job description using AI.
    Discover matching skills, potential skill gaps, and
    personalized suggestions to improve your application.
    """
)

st.caption(
    "🔒 Privacy note: This version uses a local Ollama model "
    "for AI recommendations. Your resume text is sent to the "
    "local Ollama service running on your computer."
)

st.divider()


# --------------------------------------------------
# 3. Resume Upload
# --------------------------------------------------

st.subheader("📄 1. Upload Your Resume")

resume_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"]
)


# --------------------------------------------------
# 4. Job Description
# --------------------------------------------------

st.subheader("💼 2. Job Description")

job_description = st.text_area(
    "Paste the job description here",
    placeholder=(
        "Enter the job title, required skills, "
        "qualifications, and responsibilities..."
    ),
    height=200
)


# --------------------------------------------------
# 5. Analyze Resume
# --------------------------------------------------

if st.button("🚀 Analyze Resume", type="primary"):

    if resume_file is None:
        st.warning("Please upload your resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            # ------------------------------------------
            # 6. Extract Resume Text
            # ------------------------------------------

            with st.spinner("Reading your resume..."):
                resume_text = extract_resume_text(resume_file)

            if not resume_text or not resume_text.strip():
                st.warning(
                    "No readable text found in the resume. "
                    "If it is a scanned PDF, OCR may be required."
                )
                st.stop()

            st.success("Resume text extracted successfully!")

            with st.expander("View Extracted Resume Text"):
                st.text_area(
                    "Resume contents",
                    value=resume_text,
                    height=300
                )

            # ------------------------------------------
            # 7. Skill Matching
            # ------------------------------------------

            with st.spinner("Matching resume skills..."):
                result = compare_skills(
                    resume_text,
                    job_description
                )

            matched_skills = sorted(
                set(result["matched_skills"])
            )

            missing_skills = sorted(
                set(result["missing_skills"])
            )

            skill_score = result["match_percentage"]

            # ------------------------------------------
            # 8. Semantic AI Matching
            # ------------------------------------------

            with st.spinner(
                "Comparing resume and job description..."
            ):
                semantic_score = calculate_semantic_similarity(
                    resume_text,
                    job_description
                )

            # ------------------------------------------
            # 9. Overall Match Score
            # ------------------------------------------

            overall_score = None

            if skill_score is not None:
                overall_score = round(
                    0.6 * skill_score
                    + 0.4 * semantic_score,
                    2
                )

            # ------------------------------------------
            # 10. Display Dashboard
            # ------------------------------------------

            st.divider()
            st.header("📊 Resume Analysis Dashboard")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🎯 Overall Match",
                    (
                        f"{overall_score:.1f}%"
                        if overall_score is not None
                        else "N/A"
                    )
                )

            with col2:
                st.metric(
                    "🧩 Skill Coverage",
                    (
                        f"{skill_score:.1f}%"
                        if skill_score is not None
                        else "N/A"
                    )
                )

            with col3:
                st.metric(
                    "🤖 Semantic Similarity",
                    f"{semantic_score:.1f}%"
                )

            if overall_score is not None:
                st.progress(
                    max(0.0, min(1.0, overall_score / 100)),
                    text="Experimental overall match score"
                )

            st.caption(
                "These are prototype text-matching metrics, "
                "not a probability of getting a job or a "
                "validated measure of candidate suitability."
            )

            # ------------------------------------------
            # 11. Matched Skills
            # ------------------------------------------

            st.divider()
            st.subheader("✅ Matched Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.write(f"✅ {skill}")
            else:
                st.info("No recognized matching skills found.")

            # ------------------------------------------
            # 12. Potential Skill Gaps
            # ------------------------------------------

            st.subheader("⚠️ Potential Skill Gaps")

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"⚠️ {skill}")
            else:
                st.success(
                    "No missing skills from the recognized "
                    "skill dictionary were detected."
                )

            # ------------------------------------------
            # 13. All Detected Skills
            # ------------------------------------------

            with st.expander("🔎 View All Detected Skills"):

                st.write("**Skills found in the resume:**")

                st.write(
                    ", ".join(result["resume_skills"])
                    or "No recognized skills found."
                )

                st.write("**Skills found in the job description:**")

                st.write(
                    ", ".join(result["job_skills"])
                    or "No recognized skills found."
                )

            # ------------------------------------------
            # 14. Rule-Based Recommendations
            # ------------------------------------------

            st.divider()
            st.subheader("💡 Skill-Based Recommendations")

            recommendations = generate_recommendations(
                missing_skills=missing_skills,
                matched_skills=matched_skills
            )

            if recommendations:
                for recommendation in recommendations:
                    st.markdown(f"- {recommendation}")
            else:
                st.info("No additional rule-based suggestions.")

            # ------------------------------------------
            # 15. Ollama AI Recommendations
            # ------------------------------------------

            st.divider()
            st.subheader("🤖 Personalized AI Recommendations")

            with st.spinner(
                "Ollama is analyzing your resume and job description..."
            ):
                ai_recommendations = generate_ai_recommendations(
                    resume_text=resume_text,
                    job_description=job_description
                )

            st.markdown(ai_recommendations)

            st.caption(
                "AI-generated suggestions may contain errors. "
                "Verify recommendations before editing your resume, "
                "and never add skills or achievements you do not have."
            )

            # ------------------------------------------
            # 16. Download PDF Report
            # ------------------------------------------

            st.divider()
            st.subheader("📥 Download Your Report")

            report_pdf = generate_pdf_report(
                skill_score=skill_score,
                semantic_score=semantic_score,
                overall_score=overall_score,
                matched_skills=matched_skills,
                missing_skills=missing_skills,
                recommendations=recommendations
            )

            st.download_button(
                label="📄 Download Analysis Report (PDF)",
                data=report_pdf,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )

        except Exception as error:
            st.error(f"Analysis failed: {error}")
            st.info(
                "Check that all project modules are present, "
                "your Python dependencies are installed, and "
                "the Ollama model is available."
            )