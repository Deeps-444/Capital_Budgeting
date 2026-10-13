
from services.future_assumptions_research import (
    search_future_assumption_sources
)
from services.future_assumption_proposer import (
    propose_future_assumption_candidates
)

# Research context for testing.
project = {
    "project_type": "Energy",
    "project_scale": "Large",
    "project_duration_years": 5,
    "location": "India",
}

# Step 1: Retrieve sources using the working Tavily service.
research_result = search_future_assumption_sources(project)



# TEMPORARY DEBUG: inspect sources using the actual result structure.

import re

percent_pattern = re.compile(
    r"(?P<value>-?\d+(?:\.\d+)?)\s*(?:%|per\s*cent|percent)",
    re.IGNORECASE,
)

forecast_pattern = re.compile(
    r"\b(forecast|forecasted|projected|projection|outlook|expected|"
    r"estimate|estimated|expects|will reach|is set to|is likely to|"
    r"cagr|by\s+20\d{2}|over the next|next\s+(?:\d+\s+)?years?)\b",
    re.IGNORECASE,
)

historical_pattern = re.compile(
    r"\b(historical|previously|previous year|last year|actual|"
    r"recorded|rose to|increased to|declined to|fell to|stood at|"
    r"was\s+\d)\b",
    re.IGNORECASE,
)

for category in ("inflation", "market_growth"):
    sources = research_result.get("sources", {}).get(category, [])

    print(f"\n--- DEBUG: {category} ---")
    print("Source count:", len(sources))

    for source in sources[:3]:
        title = str(source.get("title", ""))
        snippet = str(
            source.get("snippet", source.get("content", ""))
        )

        print("\nTITLE:", title)
        print("SNIPPET:", snippet[:600])

        for match in percent_pattern.finditer(snippet):
            start = max(0, match.start() - 150)
            end = min(len(snippet), match.end() + 150)
            context = snippet[start:end]

            print("RATE:", match.group("value"))
            print(
                "FORECAST MATCH:",
                bool(forecast_pattern.search(context)),
            )
            print(
                "HISTORICAL MATCH:",
                bool(historical_pattern.search(context)),
            )
            print("RATE CONTEXT:", context)
# Step 2: Extract percentage candidates for review.
proposal_result = propose_future_assumption_candidates(
    research_result
)

print("Status:", proposal_result["status"])
print(
    "Inflation candidates:",
    len(proposal_result["inflation_candidates"])
)
print(
    "Market-growth candidates:",
    len(proposal_result["market_growth_candidates"])
)

# Display a few candidates with their sources.
for topic in ("inflation_candidates", "market_growth_candidates"):
    print(f"\n{topic.replace('_', ' ').title()}")

    for candidate in proposal_result[topic][:3]:
        print(
            candidate["rate_percent"],
            "|",
            candidate["context_classification"],
            "|",
            candidate["source_title"],
            "|",
            candidate["source_url"],
        )

print(
    "\nAnnual assumptions generated:",
    proposal_result["annual_assumptions"]
)
print(
    "Approval required:",
    proposal_result["approval_required"]
)