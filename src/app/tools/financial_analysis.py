from typing import List
from ..state import Company, FinancialScreening

MIN_GROWTH_3YR = 0.00
MIN_EBITDA_MARGIN = 0.10
MAX_DEBT_TO_EQUITY = 1.00


def mock_financial_analysis(company_data: Company) -> FinancialScreening:
    """
    Simple financial screening based on already-provided company metrics.
    Produces red flags, pass/fail, and disqualification reasons.
    """
    red_flags: List[str] = []
    disq: List[str] = []
 
    growth = company_data["revenue_growth_3yr"]
    margin = company_data["ebitda_margin"]
    debt = company_data["debt_to_equity"]

    if growth < 0:
        red_flags.append("declining_revenue")
        disq.append("Negative 3-year revenue growth")

    if margin < MIN_EBITDA_MARGIN:
        red_flags.append("low_profitability")
        disq.append(f"EBITDA margin below {MIN_EBITDA_MARGIN:.0%}")

    if debt > MAX_DEBT_TO_EQUITY:
        red_flags.append("high_leverage")
        disq.append(f"Debt-to-equity above {MAX_DEBT_TO_EQUITY:.2f}")

    passes = len(disq) == 0

    return {
        "passes": passes,
        "red_flags": red_flags,
        "disqualification_reasons": disq,
    }
