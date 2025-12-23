from typing import Dict, Any

from ..state import DealSourcingState, InvestmentCriteria
from ..llm.mock_llm import mock_llm_call
from ..validation import validate_and_normalize_criteria


def refine_criteria(state: DealSourcingState) -> Dict[str, Any]:
    """
    Node:
    - Interprets analyst feedback and applies a criteria patch
    - Increments iteration to control loops
    """
    patch = mock_llm_call(state, "interpret_feedback")

    criteria: InvestmentCriteria = dict(state["criteria"])
    for k, v in patch.items():
        if v is None:
            criteria.pop(k, None)  # remove constraint
        else:
            criteria[k] = v
            
    criteria, warnings = validate_and_normalize_criteria(criteria)
    if warnings:
        trace.append(f"[refine_criteria] validation_warnings={warnings}")

    trace = list(state["trace"])
    trace.append(f"[refine_criteria] applied patch={patch}")

    return {
        "criteria": criteria,
        "iteration": state["iteration"] + 1,
        "analyst_feedback": "",  
        "trace": trace,
    }
