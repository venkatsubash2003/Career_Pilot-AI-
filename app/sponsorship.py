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

    raise ValueError("No valid JSON found in model response.")


def classify_sponsorship_with_llm(job_description: str, company_name: str = "") -> dict:
    llm = get_llm()

    prompt = f"""
You are a strict JSON classifier.

Task:
Classify whether this job is suitable for an international student in the U.S.

Company Name:
{company_name}

Job Description:
{job_description}

Choose exactly one category:
- H1B_SPONSORSHIP_EXPLICIT
- US_CITIZEN_OR_GREEN_CARD_ONLY
- NO_H1B_SPONSORSHIP
- SPONSORSHIP_NOT_MENTIONED

Rules:
- If the job requires U.S. citizenship, green card, permanent residency, or security clearance, use US_CITIZEN_OR_GREEN_CARD_ONLY.
- If the job says visa/H1B sponsorship is available, use H1B_SPONSORSHIP_EXPLICIT.
- If the job says sponsorship is unavailable now or in the future, use NO_H1B_SPONSORSHIP.
- If sponsorship is unclear or not mentioned, use SPONSORSHIP_NOT_MENTIONED.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations outside JSON.

JSON format:
{{
  "category": "ONE_OF_THE_FOUR_CATEGORIES",
  "international_student_friendly": true,
  "continue_resume_analysis": true,
  "confidence_score": 90,
  "reason": "short reason",
  "evidence_from_jd": "short evidence"
}}
"""

    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    try:
        return extract_json(raw_output)
    except Exception:
        return {
            "category": "PARSING_ERROR",
            "international_student_friendly": False,
            "continue_resume_analysis": False,
            "confidence_score": 0,
            "reason": "The model response could not be parsed as valid JSON.",
            "evidence_from_jd": raw_output
        }