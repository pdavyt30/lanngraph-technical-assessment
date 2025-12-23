from typing import Dict, Any, List

from ..state import DealSourcingState, ShortlistItem


def generate_shortlist(state: DealSourcingState) -> Dict[str, Any]:
    """
    Node:
    - Sorts companies by overall score (descending)
    - Produces a business-friendly shortlist with key reasons and risks
    """
    trace = list(state["trace"])
    shortlist: List[ShortlistItem] = []

    scored = [(name, score["overall"]) for name, score in state["fit_scores"].items()]
    scored.sort(key=lambda x: x[1], reverse=True)

    analyzed_by_name = {item["company"]["company_name"]: item for item in state["analyzed_companies"]}

    for company_name, overall in scored:
        item = analyzed_by_name[company_name]
        company = item["company"]
        screening = item["financial_screening"]
        research = item["market_research"]
        score = state["fit_scores"][company_name]

        reasons = []
        risks = []

        if company["revenue_growth_3yr"] >= 0.25:
            reasons.append("Strong 3Y revenue growth")
        if company["ebitda_margin"] >= 0.15:
            reasons.append("Healthy EBITDA margin")
        reasons.append(f"Positioning: {company['market_position']}")
        reasons.append(research["competitive_positioning"])

        if company["debt_to_equity"] >= 0.9:
            risks.append("Leverage is on the high side")
        if company["ebitda_margin"] < 0.12:
            risks.append("Profitability is relatively low")
        if screening["red_flags"]:
            risks.extend(screening["red_flags"])

        shortlist.append(
            {
                "company_name": company_name,
                "overall_score": float(overall),
                "key_reasons": reasons[:4],
                "risks": risks[:4],
            }
        )

        trace.append(
            f"[generate_shortlist] shortlisted {company_name} score={overall:.3f} "
            f"(strategic={score['strategic_fit']}, fin={score['financial_fit']}, market={score['market_fit']})"
        )

    return {"shortlist": shortlist, "trace": trace}
