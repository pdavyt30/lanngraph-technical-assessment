# lanngraph-technical-assessment
This repository has been specifically created for this Junior AI Developer - Technical Assessment

# LangGraph Deal Sourcing Workflow (Mock)

This repo implements a deal-sourcing workflow using **LangGraph** with:
- deterministic mock tools (no external APIs)
- deterministic mock LLM logic (rule-based)
- conditional routing + refinement loop

# What this does
Given an analyst request like:
> "Find SaaS in Germany 20-40M"

the workflow:
1. Extracts investment criteria
2. Searches a mock company dataset
3. Screens candidates financially (red flags + pass/fail)
4. Scores qualified candidates (strategic/financial/market) and produces a shortlist
5. Simulates an analyst review and refines criteria until satisfied or iteration limit reached

# Architecture (LangGraph)
```mermaid 
flowchart TD
  A[collect_criteria] --> B[search_targets]

  B -->|candidates found| C[analyze_financials]
  B -->|none found| F[analyst_review]

  C -->|>=1 qualified| D[score_strategic_fit]
  C -->|none qualified| F[analyst_review]

  D --> E[generate_shortlist]
  E --> F[analyst_review]

  F -->|feedback present| G[refine_criteria]
  F -->|no feedback / stop| H((END))

  G --> B
  ```

# Setup (Windows PowerShell)

```
powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
