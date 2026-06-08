from app.config import get_llm


def generate_cover_letter(resume_text, job_description, company_name, analysis_result):
    llm = get_llm()

    prompt = f"""
Write a professional cover letter for this job.

Company: {company_name}

Resume:
{resume_text[:5000]}

Job Description:
{job_description[:5000]}

Analysis:
{analysis_result}

Rules:
- Keep it under 350 words.
- Make it specific to the company and role.
- Do not mention fake experience.
- Sound natural and confident.
"""

    response = llm.invoke(prompt)
    return response.content


def generate_recruiter_email(resume_text, job_description, company_name, analysis_result):
    llm = get_llm()

    prompt = f"""
Write a short recruiter outreach email for this job.

Company: {company_name}

Resume:
{resume_text[:4000]}

Job Description:
{job_description[:4000]}

Analysis:
{analysis_result}

Rules:
- Keep it under 150 words.
- Professional and concise.
- Mention interest in the role.
- Ask if they would be open to considering the candidate.
"""

    response = llm.invoke(prompt)
    return response.content