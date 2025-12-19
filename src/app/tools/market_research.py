from ..state import MarketResearch


def mock_market_research(company_name: str, industry: str) -> MarketResearch:
    """
    Mock determinístico de research:
    devuelve insights simples sin API externa.
    """
    # Reglas simples para variar un poco el texto
    if industry == "SaaS":
        positioning = "Strong recurring revenue dynamics; competitive but scalable market."
        market_share = 0.07
        notes = "SaaS comps show healthy multiples; watch churn and CAC."
    elif industry == "Fintech":
        positioning = "High-growth space with regulatory risk and platform dependencies."
        market_share = 0.05
        notes = "Key risk: compliance changes; opportunity: cross-sell to SMEs."
    else:
        positioning = "Stable demand but margin pressure and fragmented competition."
        market_share = 0.03
        notes = "Focus on defensibility and supply chain dynamics."

    return {
        "market_share": market_share,
        "competitive_positioning": f"{company_name}: {positioning}",
        "notes": notes,
    }
