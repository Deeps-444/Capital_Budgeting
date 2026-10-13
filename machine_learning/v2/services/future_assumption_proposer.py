"""
Future Assumption Proposal Layer
================================
Extract percentage evidence from already-retrieved Tavily results for human review.
This module makes NO API calls and never generates annual assumptions automatically.
A market CAGR is not automatically a project's annual cash-flow growth rate.
"""
import re
from typing import Any, Dict, List, Tuple

_PERCENT_PATTERN = re.compile(r"(?P<value>-?\d+(?:\.\d+)?)\s*(?:%|per\s*cent\b|percent\b)", re.I)
_FORECAST_TERMS = re.compile(r"\b(forecast(?:ed)?|project(?:ed|ion)?|outlook|expected|estimate(?:d|s)?|expects|will reach|is set to|is likely to|cagr|by\s+20\d{2}|over the next|next\s+(?:\d+\s+)?years?|during\s+20\d{2}|forecast period|anticipated to grow|estimated to grow|projected to grow|is projected|is estimated)\b", re.I)
_HISTORICAL_TERMS = re.compile(r"\b(historically|historical|previously|previous year|last year|actual|recorded|rose to|increased to|declined to|fell to|stood at|grew by|growth was|from\s+(?:19|20)\d{2}\s+to\s+(?:19|20)\d{2}|during\s+(?:19|20)\d{2})\b", re.I)
_INFLATION_TERMS = re.compile(r"\b(inflation|consumer price index|cpi|retail prices?|price rise|headline inflation|food inflation)\b", re.I)
_MARKET_TERMS = re.compile(r"\b(market growth|market is expected|market is projected|market is forecast|market size|market value|industry growth|sector growth|cagr|compound annual growth|renewable energy|solar energy|wind energy|power market|electricity market|energy capacity|industry forecast)\b", re.I)
_SHARE_TARGET_TERMS = re.compile(r"\b(market share|share of|share in|share accounted|accounted for|capacity share|market segment|leading segment|tolerance band|target of|target range|within the target)\b", re.I)

# Extract explicit forecast periods such as 2025-30, 2026-2034,
# or "by 2030". These are evidence from the source, not assumptions
# about the project's own cash flows.

_YEAR_RANGE_PATTERN = re.compile(
    r"\b(20\d{2})\s*[-–—]\s*(\d{2}|20\d{2})\b"
)

_BY_YEAR_PATTERN = re.compile(
    r"\bby\s+(20\d{2})\b",
    re.IGNORECASE,
)


def _extract_forecast_period(context):
    """Extract an explicit year range or end year when available."""

    range_match = _YEAR_RANGE_PATTERN.search(context)

    if range_match:
        start_year = int(range_match.group(1))
        end_text = range_match.group(2)

        if len(end_text) == 2:
            end_year = (start_year // 100) * 100 + int(end_text)

            # Handle a century boundary, if encountered.
            if end_year < start_year:
                end_year += 100
        else:
            end_year = int(end_text)

        return {
            "start_year": start_year,
            "end_year": end_year,
            "period_text": range_match.group(0),
        }

    by_match = _BY_YEAR_PATTERN.search(context)

    if by_match:
        return {
            "start_year": None,
            "end_year": int(by_match.group(1)),
            "period_text": by_match.group(0),
        }

    return {
        "start_year": None,
        "end_year": None,
        "period_text": None,
    }

def _source_text(source: Dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value = source.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return default


def _split_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text or "").strip()
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()] if text else []


def _topic_relevant(text: str, topic: str) -> bool:
    if topic == "inflation":
        return bool(_INFLATION_TERMS.search(text))
    if topic == "market_growth":
        return bool(_MARKET_TERMS.search(text))
    return False


def _classify_sentence(context: str, topic: str) -> Tuple[str, bool, List[str]]:
    reasons: List[str] = []
    relevant = _topic_relevant(context, topic)
    forecast = bool(_FORECAST_TERMS.search(context))
    historical = bool(_HISTORICAL_TERMS.search(context))
    share_or_target = bool(_SHARE_TARGET_TERMS.search(context))
    if not relevant:
        reasons.append("The percentage's local context does not clearly identify the requested topic.")
    if not forecast:
        reasons.append("No explicit forecast/projection wording appears in the local context.")
    if historical:
        reasons.append("Historical/current-period wording appears in the local context.")
    if share_or_target:
        reasons.append("The percentage may describe a share or target rather than an inflation/growth rate.")
    if share_or_target:
        label = "share_or_target"
    elif forecast and historical:
        label = "mixed_context"
    elif historical:
        label = "historical_context"
    elif forecast and relevant:
        label = "forecast_context"
    else:
        label = "unclear_context"
    eligible = relevant and forecast and not historical and not share_or_target
    return label, eligible, reasons


def _extract_candidates(
    topic: str,
    source_items: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Extract percentage evidence while preserving its source context.

    Candidates remain evidence for human review. This function never
    generates annual project assumptions.
    """

    all_candidates = []
    eligible_candidates = []

    # Deduplicate repeated representations of the same rate from the
    # same source and forecast period, such as prose and a summary table.
    seen = set()

    for source in source_items:
        if not isinstance(source, dict):
            continue

        title = _source_text(
            source, "title", "source_title",
            default="Untitled source",
        )
        url = _source_text(source, "url", "source_url")
        snippet = _source_text(
            source, "snippet", "content", "excerpt"
        )

        if not snippet:
            continue

        for sentence in _split_sentences(snippet):
            for match in _PERCENT_PATTERN.finditer(sentence):
                try:
                    value = float(match.group("value"))
                except (TypeError, ValueError):
                    continue

                # Keep classification local to the sentence containing
                # the percentage. The title alone cannot make a value
                # eligible as a forecast.
                left = max(0, match.start() - 160)
                right = min(len(sentence), match.end() + 160)
                context = sentence[left:right].strip()

                classification, eligible, reasons = (
                    _classify_sentence(context, topic)
                )

                # Preserve the complete sentence as evidence so the
                # reviewer can see what the percentage actually refers to.
                matched_text = sentence.strip()

                # Prefer a period found near the percentage. If there is
                # none, use an explicit period elsewhere in this source
                # as a hint, clearly marked as source-level evidence.
                period = _extract_forecast_period(context)
                period_scope = "local_context"

                if period["period_text"] is None:
                    source_period = _extract_forecast_period(snippet)
                    if source_period["period_text"] is not None:
                        period = source_period
                        period_scope = "source_level_hint"

                if topic == "inflation":
                    candidate_type = (
                        "inflation_forecast"
                        if eligible
                        else "historical_statistic"
                        if classification == "historical_context"
                        else "inflation_rate_uncertain"
                    )

                else:
                    if classification == "share_or_target":
                        candidate_type = "share_or_target"
                    elif classification == "historical_context":
                        candidate_type = "historical_statistic"
                    elif eligible and re.search(
                        r"\bCAGR\b|compound annual growth",
                        context,
                        re.IGNORECASE,
                    ):
                        candidate_type = "market_cagr"
                    elif eligible:
                        candidate_type = "market_growth_forecast"
                    else:
                        candidate_type = "market_growth_uncertain"

                # A source may repeat the same forecast in prose and a
                # table. Collapse those duplicates when source, value,
                # candidate type, and period match.
                #
                # If no period is identifiable, use the normalized
                # sentence so distinct claims are not blindly merged.
                normalized_url = url.strip().rstrip("/").lower()
                normalized_text = re.sub(
                    r"\s+", " ", matched_text
                ).strip().lower()

                if period["period_text"]:
                    context_identity = (
                        period["start_year"],
                        period["end_year"],
                    )
                else:
                    context_identity = normalized_text

                identity = (
                    topic,
                    normalized_url,
                    value,
                    candidate_type,
                    context_identity,
                )

                if identity in seen:
                    continue

                seen.add(identity)

                candidate = {
                    "topic": topic,
                    "rate_percent": value,
                    "candidate_type": candidate_type,
                    "context_classification": classification,
                    "topic_relevant": _topic_relevant(
                        context, topic
                    ),
                    "eligible_for_proposal": eligible,

                    # Provenance
                    "source_title": title,
                    "source_url": url or None,
                    "source_domain": _source_text(
                        source, "source_domain", "domain"
                    ) or None,
                    "published_date": (
                        source.get("published_date")
                        or source.get("date")
                    ),
                    "relevance_score": source.get(
                        "relevance_score", source.get("score")
                    ),
                    "research_query": (
                        source.get("research_query")
                        or source.get("query")
                    ),

                    # Evidence and period
                    "matched_text": matched_text,
                    "forecast_period": period,
                    "forecast_period_scope": period_scope,

                    # Human review
                    "review_status": "pending",
                    "review_reasons": reasons,

                    "limitations": [
                        "Heuristic classification; verify the original source.",
                        "The extracted rate may refer to the economy or market, "
                        "not the proposed project's cash flows.",
                        "A source-level period hint is not proof that this "
                        "specific percentage applies throughout that period.",
                        "No annual project assumptions have been generated.",
                    ],
                }

                all_candidates.append(candidate)

                if eligible:
                    eligible_candidates.append(candidate)

    return all_candidates, eligible_candidates

def propose_future_assumption_candidates(research_result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract reviewable evidence from existing research results without new API calls."""
    if not isinstance(research_result, dict):
        raise ValueError("research_result must be a dictionary.")
    sources = research_result.get("sources", {})
    if not isinstance(sources, dict):
        raise ValueError("research_result['sources'] must be a dictionary.")
    inflation_sources = sources.get("inflation", [])
    market_sources = sources.get("market_growth", [])
    if not isinstance(inflation_sources, list) or not isinstance(market_sources, list):
        raise ValueError("sources['inflation'] and sources['market_growth'] must be lists.")
    inf_all, inf_eligible = _extract_candidates("inflation", inflation_sources)
    market_all, market_eligible = _extract_candidates("market_growth", market_sources)
    
    result = {
        "status": "candidates_extracted_for_review",
        "message": (
            "Candidates retain source context and require human review. "
            "Eligible candidates are not approved project assumptions."
        ),
        "inflation_candidates": inf_eligible,
        "market_growth_candidates": market_eligible,
        "all_inflation_candidates": inf_all,
        "all_market_growth_candidates": market_all,
        "candidate_counts": {
            "inflation_raw": len(inf_all),
            "inflation_eligible": len(inf_eligible),
            "market_growth_raw": len(market_all),
            "market_growth_eligible": len(market_eligible),
        },
        "annual_assumptions": None,
        "approval_required": True,
        "important_note": (
            "Market-growth CAGR is not automatically project cash-flow "
            "growth. Review every proposed rate and its source."
        ),
    }

    result["annual_proposals"] = build_annual_assumption_proposals(
        result,
        horizon_years=5,
    )

    return result


def build_annual_assumption_proposals(
    candidate_result: Dict[str, Any],
    horizon_years: int = 5,
    base_year: int | None = None,
) -> Dict[str, Any]:
    """
    Build provisional annual baselines from eligible, source-backed rates.

    A selected rate is carried forward for the requested horizon.
    This is a modelling baseline, NOT a claim that the source forecasts
    every individual year. Human approval is always required.
    """
    from datetime import date

    if horizon_years <= 0:
        raise ValueError("horizon_years must be positive.")

    if base_year is None:
        base_year = date.today().year

    def select_candidate(topic: str):
        candidates = candidate_result.get(f"{topic}_candidates", [])
        candidates = [
            c for c in candidates
            if c.get("eligible_for_proposal") is True
            and isinstance(c.get("rate_percent"), (int, float))
            and c.get("source_url")
        ]

        if not candidates:
            return None

        # Prefer candidates with an explicit forecast end year.
        # Do not claim this is a comprehensive source-quality ranking.
        candidates.sort(
            key=lambda c: (
                c.get("forecast_period", {}).get("end_year") is not None,
                c.get("relevance_score") is not None,
            ),
            reverse=True,
        )
        return candidates[0]

    def make_proposals(topic: str):
        candidate = select_candidate(topic)

        if candidate is None:
            return {
                "status": "insufficient_evidence",
                "message": (
                    "No eligible source-backed rate was found. "
                    "Research more sources or enter a value manually."
                ),
                "annual_proposals": [],
            }

        rate_percent = float(candidate["rate_percent"])
        period = candidate.get("forecast_period") or {}

        annual = []
        for offset in range(horizon_years):
            year = base_year + offset
            annual.append({
                "year": year,
                "rate_percent": rate_percent,
                "rate_decimal": rate_percent / 100.0,
                "proposal_method": "constant_rate_baseline",
                "year_specific_source_forecast": False,
                "review_status": "pending",
                "source_title": candidate.get("source_title"),
                "source_url": candidate.get("source_url"),
                "evidence": candidate.get("matched_text"),
                "source_forecast_period": period,
            })

        return {
            "status": "provisional_baseline",
            "message": (
                "The source-backed rate is carried forward as a baseline "
                "for each year. Individual yearly rates were not verified "
                "by the source and require human review."
            ),
            "annual_proposals": annual,
        }

    inflation_result = make_proposals("inflation")
    market_result = make_proposals("market_growth")

    return {
        "status": "proposals_ready_for_review",
        "horizon_years": horizon_years,
        "base_year": base_year,
        "inflation": inflation_result,
        "market_growth": market_result,
        "approval_required": True,
    }

if __name__ == "__main__":
    # Offline smoke test: this makes no Tavily/API calls.
    sample = {"sources": {
        "inflation": [{"title": "Inflation forecast", "url": "https://example.com/i", "snippet": "Inflation is projected to be 4.0 percent in 2027. Actual inflation was 5.2% in 2024."}],
        "market_growth": [{"title": "Renewable energy market forecast", "url": "https://example.com/e", "snippet": "The renewable energy market is projected to grow at a CAGR of 9% by 2030. Solar energy has a 40% market share. Capacity grew by over 50% in 2024."}],
    }}
    result = propose_future_assumption_candidates(sample)
    print("Offline smoke test (no Tavily calls)")
    print("Inflation eligible:", [c["candidate_rate_percent"] for c in result["inflation_candidates"]])
    print("Market eligible:", [c["candidate_rate_percent"] for c in result["market_growth_candidates"]])
    print("Annual assumptions:", result["annual_assumptions"])
    print("Approval required:", result["approval_required"])
