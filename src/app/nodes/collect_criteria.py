from typing import Dict, Any
from ..state import DealSourcingState, InvestmentCriteria
from ..llm.mock_llm import mock_llm_call
from ..validation import validate_and_normalize_criteria



def collect_criteria(state: DealSourcingState) -> Dict[str, Any]:
    """
    Node:
    - Extracts investment criteria from the analyst raw request using the mock LLM.
    """
    criteria: InvestmentCriteria = mock_llm_call(state, "extract_criteria")
    criteria, warnings = validate_and_normalize_criteria(criteria)
    
    trace = list(state["trace"])
    trace.append(f"[collect_criteria] extracted criteria={criteria}")
    
    if warnings:
        trace.append(f"[collect_criteria] validation_warnings={warnings}")
        
    return {
        "criteria": criteria,
        "trace": trace,
    }
