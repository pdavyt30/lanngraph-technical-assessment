from langgraph.graph import StateGraph, END

from .state import DealSourcingState
from .nodes.collect_criteria import collect_criteria
from .nodes.search_targets import search_targets
from .nodes.analyze_financials import analyze_financials
from .nodes.score_strategic_fit import score_strategic_fit
from .nodes.generate_shortlist import generate_shortlist
from .nodes.refine_criteria import refine_criteria
from .nodes.analyst_review import analyst_review

from .nodes.routes import route_after_search, route_after_financials, route_after_review


def build_graph():
    # Build and compile the LangGraph workflow.
    graph = StateGraph(DealSourcingState)

    graph.add_node("collect_criteria", collect_criteria)
    graph.add_node("search_targets", search_targets)
    graph.add_node("analyze_financials", analyze_financials)
    graph.add_node("score_strategic_fit", score_strategic_fit)
    graph.add_node("generate_shortlist", generate_shortlist)
    graph.add_node("analyst_review", analyst_review)
    graph.add_node("refine_criteria", refine_criteria)

    graph.set_entry_point("collect_criteria")
    graph.add_edge("collect_criteria", "search_targets")

    graph.add_conditional_edges(
        "search_targets",
        route_after_search,
        {
            "analyze_financials": "analyze_financials",
            "analyst_review": "analyst_review",
        },
    )

    graph.add_conditional_edges(
        "analyze_financials",
        route_after_financials,
        {
            "score_strategic_fit": "score_strategic_fit",
            "analyst_review": "analyst_review",
        },
    )

    graph.add_edge("score_strategic_fit", "generate_shortlist")
    graph.add_edge("generate_shortlist", "analyst_review")

    graph.add_conditional_edges(
        "analyst_review",
        route_after_review,
        {
            "refine_criteria": "refine_criteria",
            "end": END,
        },
    )

    graph.add_edge("refine_criteria", "search_targets")

    return graph.compile()
