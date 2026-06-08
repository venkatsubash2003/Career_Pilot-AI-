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
from app.scoring import calculate_keyword_match,calculate_final_ats_score
from app.scoring import normalize_llm_score
from app.generators import generate_resume_improvements
from app.application_writer import generate_cover_letter, generate_recruiter_email
from app.sponsorship_history import check_company_sponsorship_history
from app.database import init_db, save_application_analysis, get_all_applications
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "company_name" not in st.session_state:
    st.session_state.company_name = ""

if "job_title" not in st.session_state:
    st.session_state.job_title = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "sponsorship_result" not in st.session_state:
    st.session_state.sponsorship_result = None

if "history_result" not in st.session_state:
    st.session_state.history_result = None

if "final_ats_score" not in st.session_state:
    st.session_state.final_ats_score = None

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

if "recruiter_email" not in st.session_state:
    st.session_state.recruiter_email = ""

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🌍",
    layout="wide"
)
init_db()

st.title("CareerPilot AI")
st.subheader("Agentic Career Intelligence Platform for International Students")

resume_file = st.file_uploader("Upload your resume", type=["pdf", "txt"])
company_name = st.text_input(
    "Company Name",
    key="company_name"
)

# job_title = st.text_input(
#     "Job Title",
#     key="job_title"
# )

job_description = st.text_area(
    "Paste Job Description",
    height=300,
    key="job_description"
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
        history_result = check_company_sponsorship_history(company_name)

        st.header("Company Sponsorship History")

        rating = history_result["h1b_history_rating"]

        if rating == "VERY_STRONG":
            st.success("H1B History: VERY STRONG")
        elif rating == "STRONG":
            st.success("H1B History: STRONG")
        elif rating == "MODERATE":
            st.warning("H1B History: MODERATE")
        elif rating == "LOW":
            st.warning("H1B History: LOW")
        else:
            st.info("H1B History: UNKNOWN")

        col_h1b_1, col_h1b_2 = st.columns(2)

        with col_h1b_1:
            st.metric("Sponsorship Confidence", f"{history_result['confidence_score']}%")

        with col_h1b_2:
            st.metric(
                "Database Rank",
                history_result["database_rank"] if history_result["database_rank"] else "N/A"
            )

        if history_result["matched_company"]:
            st.write("Matched Company:", history_result["matched_company"])

        st.write(history_result["recommendation"])
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
                
                keyword_result = calculate_keyword_match(
                    resume_text=resume_text,
                    job_description=job_description,
                    extracted_skills=analysis_result.get("keywords_to_add", []) + analysis_result.get("matching_skills", [])
                )
                normalized_llm_score = normalize_llm_score(
                    analysis_result.get("ats_match_score",0)
                )

                final_ats_score = calculate_final_ats_score(
                    llm_score=normalized_llm_score,
                    keyword_score=keyword_result["keyword_match_score"],
                    sponsorship_category=sponsorship_result.get("category", "")
                )
                st.session_state.resume_text = resume_text
                st.session_state.sponsorship_result = sponsorship_result
                st.session_state.history_result = history_result
                st.session_state.analysis_result = analysis_result
                st.session_state.final_ats_score = final_ats_score
                st.metric(
                    label="Final ATS Match Score",
                    value=f"{final_ats_score}%"
                )
                job_title = st.text_input(
                    "Job Title",
                    placeholder="e.g. Machine Learning Engineer"
                )

                col_score1, col_score2 = st.columns(2)

                with col_score1:
                    st.metric(
                        label="LLM Resume Match Score",
                        value=f"{normalized_llm_score}%"
                    )

                with col_score2:
                    st.metric(
                        label="Keyword Match Score",
                        value=f"{keyword_result['keyword_match_score']}%"
                    )
                st.subheader("Matched Keywords")
                st.write(keyword_result["matched_keywords"])

                st.subheader("Missing Keywords")
                st.write(keyword_result["missing_keywords"])
                improvement_result = generate_resume_improvements(
                resume_text=resume_text,
                job_description=job_description,
                company_name=company_name,
                analysis_result=analysis_result
                )
                st.header("Resume Improvement Plan")

                st.subheader("Professional Summary Rewrite")
                st.write(improvement_result["summary_rewrite"])

                st.subheader("Skills to Add")
                st.write(improvement_result["skills_to_add"])

                st.subheader("Experience Bullets to Improve")
                st.write(improvement_result["experience_bullets_to_improve"])

                st.subheader("Project Bullets to Improve")
                st.write(improvement_result["project_bullets_to_improve"])

                st.subheader("New Project Suggestions")
                st.write(improvement_result["new_project_suggestions"])

                st.subheader("Priority Changes")
                st.write(improvement_result["priority_changes"])
                st.header("Application Materials")
                if st.button("Save Application Analysis"):
                    save_application_analysis(
                        company_name=company_name,
                        job_title=job_title,
                        sponsorship_category=sponsorship_result.get("category", ""),
                        h1b_history_rating=history_result.get("h1b_history_rating", ""),
                        final_ats_score=final_ats_score,
                        recommendation=analysis_result.get("final_recommendation", "")
                    )

                    st.success("Application analysis saved successfully.")

                if st.session_state.analysis_result:

                    st.header("Application Materials")

                    if st.button("Generate Cover Letter"):
                        with st.spinner("Generating cover letter..."):
                            st.session_state.cover_letter = generate_cover_letter(
                                resume_text=st.session_state.resume_text,
                                job_description=st.session_state.job_description,
                                company_name=st.session_state.company_name,
                                analysis_result=st.session_state.analysis_result
                            )

                    if st.session_state.cover_letter:
                        st.subheader("Cover Letter")
                        st.text_area(
                            "Generated Cover Letter",
                            st.session_state.cover_letter,
                            height=350
                        )

                    if st.button("Generate Recruiter Email"):
                        with st.spinner("Generating recruiter email..."):
                            st.session_state.recruiter_email = generate_recruiter_email(
                                resume_text=st.session_state.resume_text,
                                job_description=st.session_state.job_description,
                                company_name=st.session_state.company_name,
                                analysis_result=st.session_state.analysis_result
                            )

                    if st.session_state.recruiter_email:
                        st.subheader("Recruiter Email")
                        st.text_area(
                            "Generated Recruiter Email",
                            st.session_state.recruiter_email,
                            height=250
                        )
                st.header("Saved Application Analyses")

                applications = get_all_applications()

                if applications:
                    st.dataframe(
                        applications,
                        column_config={
                            0: "ID",
                            1: "Company",
                            2: "Job Title",
                            3: "Sponsorship Category",
                            4: "H1B History",
                            5: "ATS Score",
                            6: "Recommendation",
                            7: "Date"
                        },
                        use_container_width=True
                    )
                else:
                    st.info("No saved applications yet.")