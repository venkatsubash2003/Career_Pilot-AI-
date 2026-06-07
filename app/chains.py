import json
import re
from app.config import get_llm


def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("No JSON found")


def analyze_resume_job_match(
    resume_text: str,
    job_description: str,
    company_name: str,
    sponsorship_result: dict
) -> dict:
    llm = get_llm()

    prompt = f"""
You are CareerPilot AI, an AI career assistant for international students.

Analyze the resume against the job description.

Company:
{company_name}

Sponsorship Analysis:
{sponsorship_result}

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY valid JSON with this structure:

{{
  "ats_match_score": 0,
  "match_summary": "short summary",
  "matching_skills": [],
  "missing_skills": [],
  "strong_resume_points": [],
  "weak_resume_points": [],
  "recommended_resume_changes": [],
  "projects_to_highlight": [],
  "keywords_to_add": [],
  "final_recommendation": "Apply / Apply with caution / Do not apply"
}}
"""

    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    try:
        return extract_json(raw_output)
    except Exception:
        return {
            "ats_match_score": 0,
            "match_summary": "Parsing error",
            "matching_skills": [],
            "missing_skills": [],
            "strong_resume_points": [],
            "weak_resume_points": [],
            "recommended_resume_changes": [],
            "projects_to_highlight": [],
            "keywords_to_add": [],
            "final_recommendation": "Could not analyze properly",
            "raw_output": raw_output
        }