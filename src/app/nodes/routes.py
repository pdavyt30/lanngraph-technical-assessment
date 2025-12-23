from ..state import DealSourcingState


def route_after_search(state: DealSourcingState) -> str:
    # If candidates were found, proceed to analysis; otherwise request review/feedback.
    if state["candidate_companies"]:
        return "analyze_financials"
    return "analyst_review"


def route_after_financials(state: DealSourcingState) -> str:
    # If at least one company is qualified, proceed to scoring; otherwise request review/feedback.
    analyzed = state["analyzed_companies"]
    has_qualified = any(not item["disqualified"] for item in analyzed)
    if has_qualified:
        return "score_strategic_fit"
    return "analyst_review"


def route_after_review(state: DealSourcingState) -> str:
    MAX_ITERATIONS = 3
    if state["iteration"] >= MAX_ITERATIONS:
        return "end"
    return "refine_criteria" if state["analyst_feedback"] else "end"
