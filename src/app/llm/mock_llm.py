import re
from typing import Dict, Any, Tuple

from ..state import DealSourcingState, InvestmentCriteria, Company

def _parse_revenue_range_eur(text: str) -> Tuple[int, int] | None:
    """
    Parse revenue ranges from text:
      - "10-50M" (millions)
      - "10 to 50 million"
      - "€10-€50M"
      - "10-50m revenue"
      - "20 40" (two numbers separated by space, treated as a range)
    Returns (min_eur, max_eur) in EUR.
    """
    t = text.lower().replace(",", "").strip()

    # Support common range formats ("10-50", "10 to 50") optionally followed by M/million.
    m = re.search(r"(\d+)\s*(?:-|to)\s*(\d+)\s*(m|million)?", t)

    # Also accept "20 40" (two numbers separated by whitespace).
    if not m:
        m = re.search(r"(\d+)\s+(\d+)\s*(m|million)?", t)

    if not m:
        return None

    lo = int(m.group(1))
    hi = int(m.group(2))
    suffix = m.group(3)

    if suffix is None and hi <= 5000:
        return (lo * 1_000_000, hi * 1_000_000)

    if suffix in ("m", "million"):
        return (lo * 1_000_000, hi * 1_000_000)

    return (lo, hi)

def mock_llm_call(state: DealSourcingState, task: str) -> Any:
    """
    Deterministic, rule-based mock of an LLM call.
    It reads the shared state plus a 'task' identifier and returns task-specific outputs.
    """
    if task == "extract_criteria":
        raw = (state.get("raw_request") or "").strip()
        low = raw.lower()

        criteria: InvestmentCriteria = {}

        # Industry extraction
        if "saas" in low:
            criteria["industry"] = "SaaS"
        elif "fintech" in low:
            criteria["industry"] = "Fintech"
        elif "retail" in low:
            criteria["industry"] = "Retail"

        # Geography extraction
        if "germany" in low:
            criteria["geography"] = "Germany"
        elif "uk" in low or "united kingdom" in low:
            criteria["geography"] = "UK"
        elif "dach" in low:
            # Maping DUCH into Germany in order to simplify mock
            criteria["geography"] = "Germany"

        # Revenue range extraction
        rr = _parse_revenue_range_eur(low)
        if rr:
            criteria["revenue_range_eur"] = rr
            
        # Strategic fit
        if "platform" in low:
            criteria["strategic_fit"] = "Prioritize platform potential and scalable recurring revenue."
        elif "complement" in low or "complementar" in low:
            criteria["strategic_fit"] = "Look for complementary capabilities to the existing portfolio."


        return criteria

    if task == "interpret_feedback":
        """
        Reads state['analyst_feedback'] and returns a patch to apply over criteria.
        Examples:
        - "expand revenue up to 60M"
        - "focus only on SaaS"
        - "Germany only"
        - "remove geography constraint"
        """
        fb = (state.get("analyst_feedback") or "").strip().lower()
        patch: Dict[str, Any] = {}

        # Industry changes
        if "only saas" in fb:
            patch["industry"] = "SaaS"
        if "fintech" in fb and "only" in fb:
            patch["industry"] = "Fintech"

        # Geography changes
        if "germany" in fb:
            patch["geography"] = "Germany"
        if "uk" in fb and "only" in fb:
            patch["geography"] = "UK"

        # Expand revenue max
        m = re.search(r"up to\s*(\d+)\s*m", fb)
        if m:
            new_max = int(m.group(1)) * 1_000_000
            curr = state.get("criteria", {}).get("revenue_range_eur")
            if curr:
                patch["revenue_range_eur"] = (curr[0], new_max)

        # Explicit range in feedback
        rr = _parse_revenue_range_eur(fb)
        if rr:
            patch["revenue_range_eur"] = rr

        # Allow removing constraints when the search is too strict.
        if "remove geography" in fb:
            patch["geography"] = None
        if "remove industry" in fb:
            patch["industry"] = None

        return patch

    if task == "strategic_assessment":
        """
        Returns a strategic fit score and a short reasoning, based on simple rules.
        """
        company: Company = state.get("current_company") 
        criteria = state["criteria"]


        # This score simulates an LLM analysis
        score = 0.5
        reasons = []

        if criteria.get("industry") and company.get("industry") == criteria.get("industry"):
            score += 0.2
            reasons.append("Industry matches criteria.")

        if criteria.get("geography") and company.get("geography") == criteria.get("geography"):
            score += 0.1
            reasons.append("Geography matches criteria.")

        if company.get("revenue_growth_3yr", 0) >= 0.25:
            score += 0.1
            reasons.append("Strong 3-year revenue growth.")

        score = max(0.0, min(1.0, score))

        return {
            "strategic_fit": round(score, 2),
            "reasoning": " ".join(reasons) if reasons else "Rule-based mock assessment.",
        }

    if task == "generate_memo":
        """
        Creates a short memo based on the current shortlist.
        """
        criteria = state.get("criteria", {})
        items = state.get("shortlist", [])

        lines = []
        lines.append("=== Shortlist Memo (Mock) ===")
        lines.append(f"Criteria: {criteria}")
        lines.append("")
        if not items:
            lines.append("No shortlisted companies.")
            return "\n".join(lines)

        for idx, it in enumerate(items, start=1):
            lines.append(f"{idx}. {it['company_name']} — overall_score={it['overall_score']:.2f}")
            if it.get("key_reasons"):
                lines.append("   Reasons: " + "; ".join(it["key_reasons"]))
            if it.get("risks"):
                lines.append("   Risks: " + "; ".join(it["risks"]))
            lines.append("")

        return "\n".join(lines)

    raise ValueError(f"Unknown task: {task}")
