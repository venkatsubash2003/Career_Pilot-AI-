import re


def clean_text(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9+#. ]", " ", text.lower())

def normalize_llm_score(score) -> int:
    try:
        score = float(score)
    except (TypeError, ValueError):
        return 0

    # If LLM returns 0.8, treat it as 80%
    if 0 <= score <= 1:
        return round(score * 100)

    # If LLM returns 80, keep it as 80%
    if 1 < score <= 100:
        return round(score)

    return 0

def calculate_keyword_match(resume_text: str, job_description: str, extracted_skills: list) -> dict:
    resume_clean = clean_text(resume_text)

    matched = []
    missing = []

    for skill in extracted_skills:
        skill_clean = skill.lower().strip()
        if skill_clean and skill_clean in resume_clean:
            matched.append(skill)
        else:
            missing.append(skill)

    total = len(extracted_skills)

    if total == 0:
        score = 0
    else:
        score = round((len(matched) / total) * 100)

    return {
        "keyword_match_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing
    }


def calculate_final_ats_score(llm_score: int, keyword_score: int, sponsorship_category: str) -> int:
    llm_score = normalize_llm_score(llm_score)

    final_score = round((llm_score * 0.7) + (keyword_score * 0.3))

    if sponsorship_category == "US_CITIZEN_OR_GREEN_CARD_ONLY":
        return 0

    return final_score

