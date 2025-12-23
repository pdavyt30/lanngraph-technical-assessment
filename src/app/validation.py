from typing import List, Tuple, Optional
from .state import InvestmentCriteria

ALLOWED_INDUSTRIES = {"SaaS", "Fintech", "Retail"}
ALLOWED_GEOGRAPHIES = {"Germany", "UK"}

MIN_REVENUE_EUR = 0
MAX_REVENUE_EUR = 500_000_000  # techo razonable para mock/demo


def validate_and_normalize_criteria(criteria: InvestmentCriteria) -> Tuple[InvestmentCriteria, List[str]]:
    """
    Valida y normaliza criteria para evitar estados inválidos y loops innecesarios.

    Devuelve:
      (normalized_criteria, warnings)
    """
    normalized: InvestmentCriteria = dict(criteria)
    warnings: List[str] = []

    # ---- industry ----
    industry = normalized.get("industry")
    if industry is not None and industry not in ALLOWED_INDUSTRIES:
        warnings.append(f"Invalid industry '{industry}' removed (allowed={sorted(ALLOWED_INDUSTRIES)})")
        normalized.pop("industry", None)

    # ---- geography ----
    geography = normalized.get("geography")
    if geography is not None and geography not in ALLOWED_GEOGRAPHIES:
        warnings.append(f"Invalid geography '{geography}' removed (allowed={sorted(ALLOWED_GEOGRAPHIES)})")
        normalized.pop("geography", None)

    # ---- revenue_range_eur ----
    rr = normalized.get("revenue_range_eur")
    if rr is not None:
        try:
            lo, hi = int(rr[0]), int(rr[1])
        except Exception:
            warnings.append("Invalid revenue_range_eur format removed")
            normalized.pop("revenue_range_eur", None)
        else:
            # swap si vinieron invertidos
            if lo > hi:
                warnings.append("Revenue range swapped (min > max)")
                lo, hi = hi, lo

            # clamp a límites razonables
            if lo < MIN_REVENUE_EUR:
                warnings.append("Revenue min clamped to 0")
                lo = MIN_REVENUE_EUR

            if hi > MAX_REVENUE_EUR:
                warnings.append(f"Revenue max clamped to {MAX_REVENUE_EUR}")
                hi = MAX_REVENUE_EUR

            # si queda rango inválido, lo removemos
            if hi <= lo:
                warnings.append("Revenue range removed (max <= min after normalization)")
                normalized.pop("revenue_range_eur", None)
            else:
                normalized["revenue_range_eur"] = (lo, hi)

    # ---- strategic_fit ----
    sf = normalized.get("strategic_fit")
    if sf is not None and not str(sf).strip():
        warnings.append("Empty strategic_fit removed")
        normalized.pop("strategic_fit", None)

    return normalized, warnings
