import os
from typing import List
from ..state import Company, InvestmentCriteria

# Base mock dataset used by mock_company_search.
DATASET_DEFAULT: List[Company] = [
    {
        "company_name": "TechCorp GmbH",
        "industry": "SaaS",
        "geography": "Germany",
        "revenue_eur": 25_000_000,
        "revenue_growth_3yr": 0.35,
        "ebitda_margin": 0.22,
        "employee_count": 150,
        "founded_year": 2015,
        "debt_to_equity": 0.30,
        "market_position": "Regional leader in HR tech",
    },
    {
        "company_name": "CloudWorks AG",
        "industry": "SaaS",
        "geography": "Germany",
        "revenue_eur": 55_000_000,
        "revenue_growth_3yr": 0.08,
        "ebitda_margin": 0.14,
        "employee_count": 320,
        "founded_year": 2012,
        "debt_to_equity": 1.10,
        "market_position": "Mature ERP cloud suite for mid-market",
    },
    {
        "company_name": "FinPulse Ltd",
        "industry": "Fintech",
        "geography": "UK",
        "revenue_eur": 18_000_000,
        "revenue_growth_3yr": 0.42,
        "ebitda_margin": 0.19,
        "employee_count": 120,
        "founded_year": 2018,
        "debt_to_equity": 0.25,
        "market_position": "Fast-growing payments platform",
    },
    {
        "company_name": "RetailStack GmbH",
        "industry": "Retail",
        "geography": "Germany",
        "revenue_eur": 30_000_000,
        "revenue_growth_3yr": -0.05,
        "ebitda_margin": 0.07,
        "employee_count": 220,
        "founded_year": 2010,
        "debt_to_equity": 0.85,
        "market_position": "Niche POS provider under price pressure",
    },
]

# ------------------------------------------------------------
# DATASET 1: SaaS Germany 20–50M
# Goal for query: "Find SaaS in Germany 20 50"
# Expected:
# - Candidates found: 5
# - Qualified (passes screening): 3
# - Disqualified: 2
# Disqualified rules (financial tool):
# - revenue_growth_3yr < 0  => disq
# - ebitda_margin < 0.10    => disq
# - debt_to_equity > 1.00   => disq
# ------------------------------------------------------------
DATASET_1_SAAS_DE_20_50: List[Company] = [
    # PASS (growth>=0, margin>=0.10, debt<=1.00)
    {
        "company_name": "NordHR Cloud GmbH",
        "industry": "SaaS",
        "geography": "Germany",
        "revenue_eur": 22_000_000,
        "revenue_growth_3yr": 0.18,
        "ebitda_margin": 0.16,
        "employee_count": 95,
        "founded_year": 2017,
        "debt_to_equity": 0.40,
        "market_position": "Strong HR workflow automation in the DACH mid-market",
    },
    # PASS
    {
        "company_name": "BavariaOps SaaS GmbH",
        "industry": "SaaS",
        "geography": "Germany",
        "revenue_eur": 35_000_000,
        "revenue_growth_3yr": 0.28,
        "ebitda_margin": 0.12,
        "employee_count": 180,
        "founded_year": 2014,
        "debt_to_equity": 0.90,
        "market_position": "Operations platform with strong retention in manufacturing SMBs",
    },
    # PASS
    {
        "company_name": "RhineMetrics GmbH",
        "industry": "SaaS",
        "geography": "Germany",
        "revenue_eur": 48_000_000,
        "revenue_growth_3yr": 0.10,
        "ebitda_margin": 0.20,
        "employee_count": 260,
        "founded_year": 2013,
        "debt_to_equity": 0.60,
        "market_position": "Analytics suite for regulated industries with sticky customers",
    },
    # DISQUALIFIED (negative growth)
    {
        "company_name": "LegacySuite DE GmbH",
        "industry": "SaaS",
        "geography": "Germany",
        "revenue_eur": 40_000_000,
        "revenue_growth_3yr": -0.02,
        "ebitda_margin": 0.18,
        "employee_count": 310,
        "founded_year": 2009,
        "debt_to_equity": 0.55,
        "market_position": "Legacy ERP vendor facing SaaS-native competition",
    },
    # DISQUALIFIED (low margin)
    {
        "company_name": "ScaleBurner GmbH",
        "industry": "SaaS",
        "geography": "Germany",
        "revenue_eur": 28_000_000,
        "revenue_growth_3yr": 0.30,
        "ebitda_margin": 0.08,
        "employee_count": 210,
        "founded_year": 2016,
        "debt_to_equity": 0.70,
        "market_position": "High-growth GTM tool with heavy discounting pressure",
    },
]

# ------------------------------------------------------------
# DATASET 2: Fintech UK 30–60M
# Goal for query: "Find Fintech in UK 30 60 m"
# Expected:
# - Candidates found: 4
# - Qualified: 2
# - Disqualified: 2
# ------------------------------------------------------------
DATASET_2_FINTECH_UK_30_60: List[Company] = [
    # PASS
    {
        "company_name": "RegPay UK Ltd",
        "industry": "Fintech",
        "geography": "UK",
        "revenue_eur": 32_000_000,
        "revenue_growth_3yr": 0.20,
        "ebitda_margin": 0.18,
        "employee_count": 140,
        "founded_year": 2015,
        "debt_to_equity": 0.60,
        "market_position": "Compliance-first payments platform for SMEs",
    },
    # PASS
    {
        "company_name": "LedgerFlow Ltd",
        "industry": "Fintech",
        "geography": "UK",
        "revenue_eur": 58_000_000,
        "revenue_growth_3yr": 0.15,
        "ebitda_margin": 0.12,
        "employee_count": 280,
        "founded_year": 2012,
        "debt_to_equity": 0.90,
        "market_position": "Embedded finance ledger infrastructure with stable enterprise contracts",
    },
    # DISQUALIFIED (low margin)
    {
        "company_name": "CreditBurst PLC",
        "industry": "Fintech",
        "geography": "UK",
        "revenue_eur": 45_000_000,
        "revenue_growth_3yr": 0.25,
        "ebitda_margin": 0.07,
        "employee_count": 230,
        "founded_year": 2016,
        "debt_to_equity": 0.55,
        "market_position": "Consumer credit platform with aggressive acquisition costs",
    },
    # DISQUALIFIED (high leverage)
    {
        "company_name": "RiskyCapital UK Ltd",
        "industry": "Fintech",
        "geography": "UK",
        "revenue_eur": 60_000_000,
        "revenue_growth_3yr": 0.05,
        "ebitda_margin": 0.14,
        "employee_count": 310,
        "founded_year": 2011,
        "debt_to_equity": 1.25,
        "market_position": "Brokerage platform with heavy balance-sheet financing",
    },
]

# Dataset registry (selectable via environment variable).

MOCK_DATASETS = {
    "default": DATASET_DEFAULT,
    "set1": DATASET_1_SAAS_DE_20_50,
    "set2": DATASET_2_FINTECH_UK_30_60,
}

def _active_dataset() -> List[Company]:
    dataset_name = os.environ.get("MOCK_DATASET", "default").strip().lower()
    return MOCK_DATASETS.get(dataset_name, DATASET_DEFAULT)


def mock_company_search(criteria: InvestmentCriteria) -> List[Company]:
    """
    Filters the active dataset by:
    - industry: exact match (if provided)
    - geography: exact match (if provided)
    - revenue_range_eur: inclusive range filter (if provided)
    """
    companies = _active_dataset()

    industry = criteria.get("industry")
    geography = criteria.get("geography")
    rev_range = criteria.get("revenue_range_eur")

    results: List[Company] = []
    for c in companies:
        if industry and c["industry"] != industry:
            continue
        if geography and c["geography"] != geography:
            continue
        if rev_range:
            rmin, rmax = rev_range
            if not (rmin <= c["revenue_eur"] <= rmax):
                continue
        results.append(c)

    return results
