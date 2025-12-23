from typing import Dict, Any
from ..state import DealSourcingState

MAX_ITERATIONS = 3
MIN_TOP_SCORE = 0.65


def analyst_review(state: DealSourcingState) -> Dict[str, Any]:
    # This node simulates an analyst review and decides whether to refine or stop.
    trace = list(state["trace"])
    iteration = state["iteration"]

    # Hard stop to prevent infinite refinement loops.
    if iteration >= MAX_ITERATIONS:
        trace.append("[analyst_review] max iterations reached -> ending")
        return {"analyst_feedback": "", "trace": trace}

    if not state["candidate_companies"]:
        if iteration == 0 and state["criteria"].get("geography"):
            trace.append("[analyst_review] no candidates -> suggest removing geography constraint")
            return {"analyst_feedback": "remove geography constraint", "trace": trace}
        if state["criteria"].get("industry"):
            trace.append("[analyst_review] still no candidates -> suggest removing industry constraint")
            return {"analyst_feedback": "remove industry constraint", "trace": trace}

        trace.append("[analyst_review] no candidates even after broadening -> ending")
        return {"analyst_feedback": "", "trace": trace}

    if state["analyzed_companies"] and all(x["disqualified"] for x in state["analyzed_companies"]):
        trace.append("[analyst_review] no suitable targets -> suggest expanding revenue range")
        return {"analyst_feedback": "expand revenue up to 60m", "trace": trace}

    shortlist = state["shortlist"]
    if not shortlist:
        trace.append("[analyst_review] no shortlist -> suggest expanding revenue range")
        return {"analyst_feedback": "expand revenue up to 60m", "trace": trace}

    top = shortlist[0]["overall_score"]
    if top >= MIN_TOP_SCORE:
        trace.append(f"[analyst_review] satisfied (top_score={top:.2f})")
        return {"analyst_feedback": "", "trace": trace}

    trace.append(f"[analyst_review] not satisfied (top_score={top:.2f}) -> broaden criteria")
    return {"analyst_feedback": "expand revenue up to 60m", "trace": trace}
