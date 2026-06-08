import json
import re
from app.config import get_json_llm


def extract_json(text: str) -> dict:
    text = text.strip().replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            return json.loads(match.group())

    raise ValueError("No valid JSON found")


def generate_resume_improvements(
    resume_text: str,
    job_description: str,
    company_name: str,
    analysis_result: dict
) -> dict:
    llm = get_json_llm()

    prompt = f"""
You are an expert resume strategist.

Create specific resume improvement suggestions based on the resume and job description.

Return JSON only with these exact keys:
summary_rewrite,
skills_to_add,
experience_bullets_to_improve,
project_bullets_to_improve,
new_project_suggestions,
priority_changes.

Company:
{company_name}

Analysis Result:
{json.dumps(analysis_result)}

Resume:
{resume_text[:6000]}

Job Description:
{job_description[:6000]}
"""

    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    try:
        return extract_json(raw_output)
    except Exception:
        return {
            "summary_rewrite": "",
            "skills_to_add": [],
            "experience_bullets_to_improve": [],
            "project_bullets_to_improve": [],
            "new_project_suggestions": [],
            "priority_changes": [],
            "raw_output": raw_output
        }