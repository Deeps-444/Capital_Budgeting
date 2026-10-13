"""
Future Assumptions Research Service
===================================

Retrieves source evidence for future inflation and market-growth assumptions
through the Tavily Web Search API.

This is a new, standalone module. It does not modify future_assumptions.py,
app_v2.py, or the existing forecasting pipeline. It returns source evidence,
not approved numerical forecasts.

Setup:
    pip install requests

PowerShell:
    $env:TAVILY_API_KEY="your_tavily_api_key"

Example:
    from services.future_assumptions_research import search_future_assumption_sources

    result = search_future_assumption_sources({
        "project_type": "Energy",
        "project_scale": "Large",
        "project_duration_years": 5,
        "location": "India"
    })
"""

import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import requests

TAVILY_SEARCH_URL = "https://api.tavily.com/search"
DEFAULT_COUNTRY = "India"
REQUEST_TIMEOUT_SECONDS = 30
# Load environment variables from the V2 project's .env file.

from pathlib import Path
import os
from dotenv import load_dotenv

# test_future_research.py is inside services/,
# so go up one directory to reach machine_learning/v2/.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH, override=True)

api_key = os.getenv("TAVILY_API_KEY")

print("Environment file:", ENV_PATH)
print("Environment file exists:", ENV_PATH.is_file())
print("API key loaded:", bool(api_key))
print("API key length:", len(api_key) if api_key else 0)
class ResearchServiceError(RuntimeError):
    """Raised when source research cannot be completed safely."""


def _search_tavily(
    query: str,
    api_key: str,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """Run one search and normalize results without inventing forecast values."""
    payload = {
        "api_key": api_key,
        "query": query,
        "topic": "general",
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False
    }

    try:
        response = requests.post(
            TAVILY_SEARCH_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        body = response.json()
    except requests.Timeout as exc:
        raise ResearchServiceError(
            "Tavily search timed out. Please try again."
        ) from exc
    
    except requests.HTTPError as exc:
        # Show Tavily's HTTP status and error response without exposing the API key.
        status_code = (
            exc.response.status_code
            if exc.response is not None
            else "unknown"
        )
        error_body = (
            exc.response.text[:500]
            if exc.response is not None
            else str(exc)
        )

        raise ResearchServiceError(
            f"Tavily HTTP error {status_code}: {error_body}"
        ) from exc

    except requests.RequestException as exc:
        raise ResearchServiceError(
            f"Tavily network/request error: {type(exc).__name__}: {exc}"
        ) from exc
    except ValueError as exc:
        raise ResearchServiceError(
            "Tavily returned a response that was not valid JSON."
        ) from exc

    results = []
    for item in body.get("results", []):
        url = item.get("url")
        domain = None
        if url:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc

        results.append({
            "title": item.get("title"),
            "url": url,
            "source_domain": domain,
            "published_date": item.get("published_date"),
            "relevance_score": item.get("score"),
            "snippet": item.get("content"),
            "research_query": query
        })

    return results


def _build_queries(project: Dict[str, Any]) -> Dict[str, str]:
    """Create separate searches for inflation and project-sector growth."""
    project_type = str(project.get("project_type") or "project").strip()
    location = str(
        project.get("location")
        or project.get("country")
        or DEFAULT_COUNTRY
    ).strip()
    horizon = project.get("project_duration_years", 5)

    return {
        "inflation": (
            f"{location} official inflation forecast outlook next {horizon} "
            "years central bank government statistics inflation projections"
        ),
        "market_growth": (
            f"{location} {project_type} sector market growth outlook forecast "
            f"next {horizon} years government regulator industry report"
        )
    }


def search_future_assumption_sources(
    project: Dict[str, Any],
    api_key: Optional[str] = None,
    max_results_per_topic: int = 5
) -> Dict[str, Any]:
    """
    Retrieve source evidence for inflation and market-growth assumptions.

    Numerical values are intentionally not inferred from search snippets.
    A later extraction/review step must determine which evidence supports
    proposed assumptions, and the user must approve them before forecasting.
    """
    if not isinstance(project, dict):
        raise ValueError("project must be a dictionary.")

    if (
        not isinstance(max_results_per_topic, int)
        or not 1 <= max_results_per_topic <= 10
    ):
        raise ValueError("max_results_per_topic must be between 1 and 10.")

    resolved_key = api_key or os.getenv("TAVILY_API_KEY")
    if not resolved_key:
        raise ResearchServiceError(
            "TAVILY_API_KEY is not configured. Set it as an environment "
            "variable before calling the research service."
        )

    queries = _build_queries(project)
    sources = {}

    for topic, query in queries.items():
        sources[topic] = _search_tavily(
            query=query,
            api_key=resolved_key,
            max_results=max_results_per_topic
        )

    return {
        "status": "evidence_retrieved_not_forecast",
        "message": (
            "Sources were retrieved. Numerical assumptions have not been "
            "generated or approved; review source quality and extract "
            "supported values before forecasting."
        ),
        "project_context": {
            "project_type": project.get("project_type"),
            "location": (
                project.get("location")
                or project.get("country")
                or DEFAULT_COUNTRY
            ),
            "project_duration_years": project.get(
                "project_duration_years", 5
            )
        },
        "queries": queries,
        "sources": sources,
        "assumptions": None,
        "approval_required": True
    }
