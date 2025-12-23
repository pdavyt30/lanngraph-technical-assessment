from typing import Dict, Any, List

from ..state import DealSourcingState, Company
from ..tools.company_search import mock_company_search


def search_targets(state: DealSourcingState) -> Dict[str, Any]:
    """
    Node:
    - Uses current criteria to retrieve candidate companies from the mock search tool
    - Resets downstream state to avoid stale results across iterations
    """
    criteria = state["criteria"]
    companies: List[Company] = mock_company_search(criteria)

    trace = list(state["trace"])
    trace.append(f"[search_targets] found {len(companies)} companies")

    return {
        "candidate_companies": companies,
        "analyzed_companies": [],
        "fit_scores": {},
        "shortlist": [],
        "trace": trace,
    }
