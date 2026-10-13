"""
Project Pipeline
================

Coordinates assessment, source research/proposal preparation, and forecasting.

Important separation:
- Research retrieves external source evidence only when explicitly requested.
- The proposal layer extracts reviewable percentage candidates from already
  retrieved results; it does not make API calls.
- Candidate percentages are NOT annual project assumptions.
- Forecasting continues to require explicit annual inflation and market-growth
  arrays supplied by the user/application after review.
"""
from typing import Optional, Dict, Any

from .complexity_assessor import calculate_complexity
from .risk_assessor import calculate_risk_index
from .model_router import select_forecasting_method
from .cbr_retriever import find_similar_projects, build_lstm_context
from .lstm_predictor import predict_from_cbr_context
from .future_assumptions import validate_future_assumptions
from .bbn_predictor import infer_cash_flow_state
from monte_carlo import run_monte_carlo


def determine_forecasting_method(
    project,
    historical_cash_flows: Optional[list[float]] = None,
) -> dict:
    """Assess complexity and select a forecasting path deterministically."""
    complexity_result = calculate_complexity(project)
    forecasting_method = select_forecasting_method(historical_cash_flows)
    return {
        "complexity_index": complexity_result["complexity_index"],
        "complexity_details": complexity_result,
        "forecasting_method": forecasting_method,
    }


def assess_project(
    project,
    risks: list[dict],
    historical_cash_flows: Optional[list[float]] = None,
) -> dict:
    """Calculate complexity/risk and select the forecasting method."""
    complexity_result = calculate_complexity(project)
    risk_result = calculate_risk_index(risks)
    forecasting_method = select_forecasting_method(historical_cash_flows)
    return {
        "project": project,
        "complexity": complexity_result,
        "risk": risk_result,
        "forecasting_method": forecasting_method,
    }


def prepare_future_assumption_candidates(
    project: Dict[str, Any],
    research_result: Optional[Dict[str, Any]] = None,
    *,
    run_research: bool = False,
    max_results_per_topic: int = 5,
) -> dict:
    """
    Prepare reviewable evidence candidates for inflation and market growth.

    If `research_result` is provided, it is reused and no network request is
    made. A Tavily search is made only when `run_research=True` and no existing
    result is supplied. This keeps offline tests and ordinary forecasts from
    consuming search credits.
    """
    if not isinstance(project, dict):
        raise ValueError("project must be a dictionary.")

    if research_result is None:
        if not run_research:
            return {
                "status": "research_not_run",
                "message": (
                    "No cached research result was supplied. Set run_research=True "
                    "to retrieve source evidence, or pass existing research_result."
                ),
                "research": None,
                "proposals": None,
                "approval_required": True,
            }

        from .future_assumptions_research import search_future_assumption_sources
        research_result = search_future_assumption_sources(
            project,
            max_results_per_topic=max_results_per_topic,
        )

    # This import is deliberately local so forecasting-only usage does not
    # require the proposal layer until this helper is called.
    from .future_assumption_proposer import propose_future_assumption_candidates
    proposals = propose_future_assumption_candidates(research_result)

    return {
        "status": "candidates_ready_for_human_review",
        "research": research_result,
        "proposals": proposals,
        "approval_required": True,
        "annual_assumptions": None,
        "message": (
            "Review the original source and choose/edit annual values for the "
            "project horizon. Candidate percentages are evidence only and are "
            "not automatically converted into annual assumptions."
        ),
    }


def forecast_project(
    project,
    risks,
    historical_cash_flows,
    future_assumptions,
):
    """
    Execute CBR+LSTM forecasting, BBN state inference and Monte Carlo NPV.

    `future_assumptions` must contain explicit annual `inflation` and
    `market_growth` decimal-rate arrays of equal length. Research/proposal
    candidates alone are intentionally insufficient to run a forecast.
    """
    if not isinstance(future_assumptions, dict):
        raise ValueError("future_assumptions must be a dictionary.")
    validate_future_assumptions(
        future_assumptions.get("inflation"),
        future_assumptions.get("market_growth"),
    )

    assessment = assess_project(
        project=project,
        risks=risks,
        historical_cash_flows=historical_cash_flows,
    )

    enriched_project = {
        **project,
        "complexity_index": assessment["complexity"]["complexity_index"],
        "risk_index": assessment["risk"]["risk_index"],
    }
    method = assessment["forecasting_method"]["method"]

    if method == "CBR_LSTM":
        similar_projects = find_similar_projects(enriched_project)
        cbr_context = build_lstm_context(project, similar_projects)
        predicted_cash_flows = predict_from_cbr_context(
            cbr_context=cbr_context,
            future_inflation=future_assumptions["inflation"],
            future_market_growth=future_assumptions["market_growth"],
        )

        bbn_predictions = []
        for year in range(len(predicted_cash_flows)):
            bbn_result = infer_cash_flow_state(
                complexity=assessment["complexity"]["complexity_index"],
                inflation=future_assumptions["inflation"][year],
                market_growth=future_assumptions["market_growth"][year],
            )
            bbn_predictions.append({
                "year": year + 1,
                "baseline_cash_flow": float(predicted_cash_flows[year]),
                "probabilities": bbn_result,
            })

        discount_rate = project.get("discount_rate")
        if discount_rate is None:
            raise ValueError("A discount_rate is required for Monte Carlo NPV calculation.")

        monte_carlo_result = run_monte_carlo(
            predicted_cash_flows=predicted_cash_flows,
            bbn_predictions=bbn_predictions,
            initial_investment=project["initial_investment"],
            discount_rate=discount_rate,
            simulations=10000,
        )

        return {
            **assessment,
            "forecast": {
                "method": "CBR_LSTM",
                "predicted_cash_flows": predicted_cash_flows,
            },
            "bbn": {"yearly_predictions": bbn_predictions},
            "monte_carlo": monte_carlo_result,
            "comparable_projects": similar_projects,
            "cbr_context": cbr_context,
            "future_assumptions": future_assumptions,
        }

    if method == "LSTM":
        raise NotImplementedError(
            "Direct historical-data LSTM integration is not implemented in this pipeline yet."
        )

    raise ValueError(f"Unsupported forecasting method: {method}")
