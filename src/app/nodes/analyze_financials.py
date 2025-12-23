from typing import Dict, Any, List

from ..state import DealSourcingState, AnalyzedCompany
from ..tools.financial_analysis import mock_financial_analysis
from ..tools.market_research import mock_market_research


def analyze_financials(state: DealSourcingState) -> Dict[str, Any]:
    """
    Node:
    - Runs financial screening for each candidate company
    - Runs mock market research and stores it for later scoring
    """
    analyzed: List[AnalyzedCompany] = []
    trace = list(state["trace"])

    for c in state["candidate_companies"]:
        screening = mock_financial_analysis(c)
        research = mock_market_research(c["company_name"], c["industry"])

        disqualified = not screening["passes"]

        analyzed.append(
            {
                "company": c,
                "financial_screening": screening,
                "market_research": research,
                "disqualified": disqualified,
            }
        )

        if disqualified:
            trace.append(
                f"[analyze_financials] DISQUALIFIED {c['company_name']} "
                f"reasons={screening['disqualification_reasons']}"
            )
        else:
            trace.append(f"[analyze_financials] QUALIFIED {c['company_name']}")

    return {
        "analyzed_companies": analyzed,
        "trace": trace,
    }
