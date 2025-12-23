from typing import TypedDict, List, Dict, Tuple


class InvestmentCriteria(TypedDict, total=False):
    industry: str
    revenue_range_eur: Tuple[int, int]
    geography: str
    strategic_fit: str

class Company(TypedDict):
    company_name: str
    industry: str
    geography: str
    revenue_eur: int
    revenue_growth_3yr: float
    ebitda_margin: float
    employee_count: int
    founded_year: int
    debt_to_equity: float
    market_position: str

class FinancialScreening(TypedDict):
    passes: bool
    red_flags: List[str]
    disqualification_reasons: List[str]

class MarketResearch(TypedDict):
    market_share: float
    competitive_positioning: str
    notes: str

class AnalyzedCompany(TypedDict):
    company: Company
    financial_screening: FinancialScreening
    market_research: MarketResearch
    disqualified: bool

class FitScore(TypedDict):
    overall: float
    strategic_fit: float
    financial_fit: float
    market_fit: float
    reasoning: str


class ShortlistItem(TypedDict):
    company_name: str
    overall_score: float
    key_reasons: List[str]
    risks: List[str]

class DealSourcingState(TypedDict):
    raw_request: str
    criteria: InvestmentCriteria
    candidate_companies: List[Company]
    analyzed_companies: List[AnalyzedCompany]
    fit_scores: Dict[str, FitScore]
    shortlist: List[ShortlistItem]
    analyst_feedback: str
    iteration: int
    trace: List[str]

def initial_state() -> DealSourcingState:
    # Initializes the state with empty defaults.
    return {
        "raw_request": "",
        "criteria": {},
        "candidate_companies": [],
        "analyzed_companies": [],
        "fit_scores": {},
        "shortlist": [],
        "analyst_feedback": "",
        "iteration": 0,
        "trace": [],
    }
