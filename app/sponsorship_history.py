from app.data_loader import load_sponsorship_companies


sponsor_companies = load_sponsorship_companies()


def get_rating_by_rank(rank: int) -> tuple[str, int]:
    if rank <= 50:
        return "VERY_STRONG", 95
    elif rank <= 150:
        return "STRONG", 85
    elif rank <= 300:
        return "MODERATE", 70
    else:
        return "LOW", 50


def get_recommendation(rating: str) -> str:
    recommendations = {
        "VERY_STRONG": "This company has a very strong H1B sponsorship history. Good option for international students.",
        "STRONG": "This company has a strong H1B sponsorship history. Proceed with application.",
        "MODERATE": "This company has some H1B sponsorship history. Sponsorship may depend on role, team, and business need.",
        "LOW": "This company appears in sponsorship records, but not as a high-volume sponsor. Apply with caution.",
        "UNKNOWN": "Company not found in the current sponsorship database."
    }

    return recommendations.get(rating, recommendations["UNKNOWN"])


def check_company_sponsorship_history(company_name: str) -> dict:
    company_clean = company_name.lower().strip()

    matched_company = None
    matched_rank = None

    for index, sponsor in enumerate(sponsor_companies, start=1):
        if company_clean in sponsor or sponsor in company_clean:
            matched_company = sponsor
            matched_rank = index
            break

    if matched_company:
        rating, confidence = get_rating_by_rank(matched_rank)

        return {
            "company_name": company_name,
            "h1b_history_rating": rating,
            "confidence_score": confidence,
            "matched_company": matched_company.title(),
            "database_rank": matched_rank,
            "recommendation": get_recommendation(rating)
        }

    return {
        "company_name": company_name,
        "h1b_history_rating": "UNKNOWN",
        "confidence_score": 0,
        "matched_company": None,
        "database_rank": None,
        "recommendation": get_recommendation("UNKNOWN")
    }