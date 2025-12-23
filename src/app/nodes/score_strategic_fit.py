from typing import Dict, Any

from ..state import DealSourcingState, FitScore
from ..llm.mock_llm import mock_llm_call


def score_strategic_fit(state: DealSourcingState) -> Dict[str, Any]:
    """
    Node:
    - Skips disqualified companies
    - Computes fit scores (strategic, financial, market) and an overall score
    """
    fit_scores: Dict[str, FitScore] = {}
    trace = list(state["trace"])

    for item in state["analyzed_companies"]:
        company = item["company"]

        # skip strategic scoring for disqualified companies.
        if item["disqualified"]:
            trace.append(f"[score_strategic_fit] SKIP {company['company_name']} (disqualified)")
            continue

        state_for_mock_llm = dict(state)
        state_for_mock_llm["current_company"] = company

        strategic = mock_llm_call(state_for_mock_llm, "strategic_assessment")
        strategic_fit = float(strategic.get("strategic_fit", 0.5))
        reasoning = str(strategic.get("reasoning", "Rule-based mock assessment."))

        growth = company["revenue_growth_3yr"]
        margin = company["ebitda_margin"]
        debt = company["debt_to_equity"]

        financial_fit = 0.0
        financial_fit += max(0.0, min(1.0, growth / 0.40))
        financial_fit += max(0.0, min(1.0, margin / 0.30))
        financial_fit += max(0.0, min(1.0, 1.0 - (debt / 1.50)))
        financial_fit = financial_fit / 3.0

        market_share = item["market_research"]["market_share"]
        market_fit = max(0.0, min(1.0, market_share / 0.10))

        overall = (0.45 * strategic_fit) + (0.40 * financial_fit) + (0.15 * market_fit)

        fit_scores[company["company_name"]] = {
            "overall": round(overall, 3),
            "strategic_fit": round(strategic_fit, 3),
            "financial_fit": round(financial_fit, 3),
            "market_fit": round(market_fit, 3),
            "reasoning": reasoning,
        }

        trace.append(f"[score_strategic_fit] SCORED {company['company_name']} overall={overall:.3f}")

    return {"fit_scores": fit_scores, "trace": trace}
