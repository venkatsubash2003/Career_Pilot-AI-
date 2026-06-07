import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.sponsorship import classify_sponsorship_with_llm
import streamlit as st
from app.config import get_llm
from app.parser import extract_resume_text
from app.chains import analyze_resume_job_match

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🌍",
    layout="wide"
)

st.title("CareerPilot AI")
st.subheader("Agentic Career Intelligence Platform for International Students")

resume_file = st.file_uploader("Upload your resume", type=["pdf", "txt"])
company_name = st.text_input(
    "Company Name",
    placeholder="e.g. Microsoft"
)

job_description = st.text_area(
    "Paste Job Description",
    height=350,
    placeholder="Copy and paste the complete job description here..."
)

if st.button("Analyze Job Fit"):
    if not job_description:
        st.warning("Please paste a job description.")
    else:
        sponsorship_result = classify_sponsorship_with_llm(job_description,company_name)

        st.header("Visa & Sponsorship Check")

        if sponsorship_result["international_student_friendly"] is False:
            st.error(sponsorship_result["category"])
            st.write(sponsorship_result["reason"])
            st.stop()

        elif sponsorship_result["international_student_friendly"] is True:
            st.success(sponsorship_result["category"])
            st.write(sponsorship_result["reason"])

        elif sponsorship_result["international_student_friendly"] == "warning":
            st.warning(sponsorship_result["category"])
            st.write(sponsorship_result["reason"])

            st.info(
                "Next step: check whether this company has a strong H1B sponsorship history."
            )

        else:
            st.info(sponsorship_result["category"])
            st.write(sponsorship_result["reason"])

        if not resume_file:
            st.warning("Please upload your resume to continue resume analysis.")
        else:
            with st.spinner("Analyzing resume and job description with Llama 3.1..."):
                llm = get_llm()

                response = llm.invoke(
                    f"""
                    You are CareerPilot AI.

                    Analyze this job description for an international student job seeker.

                    Company:
                    {company_name}

                    Sponsorship Result:
                    {sponsorship_result}

                    Analyze:
                    1. Required skills
                    2. Preferred skills
                    3. Resume tailoring suggestions
                    4. Projects the candidate should highlight
                    5. ATS keywords to include

                    Job Description:
                    {job_description}
                    """
                )

                st.header("Resume & Job Match Analysis")
                resume_text = extract_resume_text(resume_file)
                if not resume_text:
                    st.error("Could not extract text from resume")
                    st.stop()
                
                # st.write(response)
                st.subheader("Extracted Resume Preview")
                st.text_area("Resume Text", resume_text[:2000], height=250)
                analysis_result = analyze_resume_job_match(
                resume_text=resume_text,
                job_description=job_description,
                company_name=company_name,
                sponsorship_result=sponsorship_result
                )
                st.metric(
    label="ATS Match Score",
    value=f"{analysis_result['ats_match_score']}%"
    )

                st.subheader("Match Summary")
                st.write(analysis_result["match_summary"])

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Matching Skills")
                    st.write(analysis_result["matching_skills"])

                    st.subheader("Strong Resume Points")
                    st.write(analysis_result["strong_resume_points"])

                with col2:
                    st.subheader("Missing Skills")
                    st.write(analysis_result["missing_skills"])

                    st.subheader("Weak Resume Points")
                    st.write(analysis_result["weak_resume_points"])

                st.subheader("Recommended Resume Changes")
                st.write(analysis_result["recommended_resume_changes"])

                st.subheader("Projects to Highlight")
                st.write(analysis_result["projects_to_highlight"])

                st.subheader("Keywords to Add")
                st.write(analysis_result["keywords_to_add"])

                st.subheader("Final Recommendation")
                st.success(analysis_result["final_recommendation"])