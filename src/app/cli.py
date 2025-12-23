from .state import initial_state
from .graph import build_graph
from .llm.mock_llm import mock_llm_call


def main():
    # CLI for demo: runs the full graph and displays the result.
    g = build_graph()
    s = initial_state()

    raw = input("Describe what you want to source (e.g. 'Find SaaS in Germany 10-50M'): ").strip()
    s["raw_request"] = raw

    out = g.invoke(s)

    print("\n - FINAL CRITERIA -")
    print(out["criteria"])

    print("\n - SHORTLIST -")
    if not out["shortlist"]:
        print("(empty)")
    else:
        for i, item in enumerate(out["shortlist"], start=1):
            print(f"{i}. {item['company_name']} | score={item['overall_score']:.3f}")
            print("   reasons:", "; ".join(item["key_reasons"]))
            print("   risks:  ", "; ".join(item["risks"]))

    memo = mock_llm_call(out, "generate_memo")
    print("\n - MEMO -")
    print(memo)

    show_trace = input("\nShow trace? (y/n): ").strip().lower() == "y"
    if show_trace:
        print("\n - TRACE -")
        for line in out["trace"]:
            print(line)


if __name__ == "__main__":
    main()
