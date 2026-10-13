
"""
V2 Capital Budgeting DSS API
----------------------------

This API exposes the V2 forecasting pipeline through FastAPI.

Flow:
    Project Input
        -> Project Assessment
        -> CBR + LSTM Forecast
        -> BBN Probability Estimates
        -> Monte Carlo Financial Risk Analysis
        -> Structured JSON Response

The existing app.py remains unchanged.

IMPORTANT:
- Rates are supplied as decimals (0.05 means 5%).
- The current project_pipeline.py implements CBR_LSTM.
- Direct LSTM integration must be completed in the pipeline separately.
"""

import math
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.project_pipeline import forecast_project
import os
import tempfile
from pathlib import Path

from fastapi import UploadFile, File, HTTPException

app = FastAPI(
    title="Capital Budgeting DSS API - V2",
    description=(
        "Project cash-flow forecasting, "
        "Bayesian risk estimation and Monte Carlo NPV analysis."
    ),
    version="2.0.0"
)

from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/extract-document")
async def extract_document(file: UploadFile = File(...)):
    """
    Extract explicitly stated project details from a PDF, DOCX, or TXT.
    This endpoint does not run forecasting.
    """
    allowed_extensions = {".pdf", ".docx", ".txt"}
    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Upload a PDF, DOCX, or TXT file."
        )

    temp_path = None

    try:
        # Limit uploads to 10 MB.
        content = await file.read(10 * 1024 * 1024 + 1)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="File size must not exceed 10 MB."
            )

        # Import here so a missing Gemini configuration does not
        # prevent the entire API from starting.
        from document_extraction.parser import parse_document
        from document_extraction.extractor import extract_project_details

        with tempfile.NamedTemporaryFile(
            suffix=extension, delete=False
        ) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        text = parse_document(temp_path)

        if not text or not text.strip():
            raise HTTPException(
                status_code=422,
                detail=(
                    "No readable text was found. "
                    "Scanned PDFs may require OCR."
                )
            )

        details = extract_project_details(text)

        return {
            "message": "Project details extracted successfully.",
            "extractedDetails": details.model_dump(mode="json"),
            "reviewRequired": True,
            "forecastingPerformed": False
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document extraction failed: {str(exc)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()


# ------------------------------------------------------------------
# REQUEST MODELS
# ------------------------------------------------------------------
# These models define the JSON structure accepted by the API.
# They also provide basic input validation before running the pipeline.
# ------------------------------------------------------------------
class ResearchRequest(BaseModel):
    project: Dict[str, Any]

@app.post("/research-assumptions")
def research_assumptions(request: ResearchRequest):
    """
    Retrieve web evidence for inflation and market-growth assumptions.
    This endpoint does not approve or generate annual forecast rates.
    """
    from services.project_pipeline import (
        prepare_future_assumption_candidates
    )
    from services.future_assumptions_research import ResearchServiceError

    try:
        return prepare_future_assumption_candidates(
            project=request.project,
            run_research=True,
            max_results_per_topic=5,
        )

    except ResearchServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
class ProjectInput(BaseModel):
    project_type: str
    project_scale: str
    project_duration_years: int = Field(gt=0)
    initial_investment: float = Field(gt=0)
    tax_rate: float = Field(ge=0, le=1)
    discount_rate: float = Field(ge=0, le=1)


class FutureAssumptionsInput(BaseModel):
    inflation: list[float] = Field(min_length=1)
    market_growth: list[float] = Field(min_length=1)


class PredictionRequest(BaseModel):
    project: ProjectInput
    risks: list[dict]
    historical_cash_flows: Optional[list[float]] = None
    future_assumptions: FutureAssumptionsInput
    


# ------------------------------------------------------------------
# JSON SERIALIZATION
# ------------------------------------------------------------------
# Convert non-finite numbers to null so the API never emits NaN or Infinity.
# Recursively handle dictionaries and lists returned by model services.
# ------------------------------------------------------------------

def clean_for_json(value):
    if isinstance(value, dict):
        return {
            str(key): clean_for_json(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [clean_for_json(item) for item in value]

    if hasattr(value, "item"):
        value = value.item()

    if isinstance(value, float):
        if not math.isfinite(value):
            return None

    return value


# ------------------------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Capital Budgeting DSS V2 API is running",
        "version": "2.0.0"
    }


# ------------------------------------------------------------------
# MAIN PREDICTION ENDPOINT
# ------------------------------------------------------------------

@app.post("/predict")
def predict(request: PredictionRequest):

    # --------------------------------------------------------------
    # STEP 1: Prepare the project and assumption data.
    #
    # Pydantic validates the basic fields. Rates remain decimals;
    # unlike the old API, we do not divide discount_rate by 100.
    # --------------------------------------------------------------

    project = request.project.model_dump()

    risks = request.risks

    historical_cash_flows = request.historical_cash_flows

    future_assumptions = request.future_assumptions.model_dump()

    # --------------------------------------------------------------
    # STEP 2: Validate the forecast horizon.
    #
    # The current CBR + LSTM predictor defaults to a five-year horizon.
    # Both assumption lists must match that horizon.
    # --------------------------------------------------------------

    inflation = future_assumptions["inflation"]
    market_growth = future_assumptions["market_growth"]

    if len(inflation) != len(market_growth):
        raise HTTPException(
            status_code=422,
            detail=(
                "Inflation and market_growth must contain "
                "the same number of yearly values."
            )
        )

    if len(inflation) != 5:
        raise HTTPException(
            status_code=422,
            detail=(
                "The current CBR + LSTM pipeline expects five "
                "future inflation values and five market-growth values."
            )
        )

    # --------------------------------------------------------------
    # STEP 3: Execute the V2 pipeline.
    #
    # This runs complexity and risk assessment, chooses a forecasting
    # method, generates forecasts, performs BBN inference and runs
    # Monte Carlo financial analysis.
    # --------------------------------------------------------------

    try:
        result = forecast_project(
            project=project,
            risks=risks,
            historical_cash_flows=historical_cash_flows,
            future_assumptions=future_assumptions
        )

    except NotImplementedError as exc:
        raise HTTPException(
            status_code=501,
            detail=str(exc)
        ) from exc

    except (ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc

    # --------------------------------------------------------------
    # STEP 4: Prepare a compact, frontend-friendly response.
    #
    # Do not return the complete Monte Carlo NPV distribution here:
    # 10,000 individual outcomes are unnecessary for the initial API.
    # Summary metrics and percentiles are enough for the dashboard.
    # --------------------------------------------------------------

    forecast = result.get("forecast", {})
    monte_carlo = result.get("monte_carlo", {})
    bbn = result.get("bbn", {})
    percentiles = monte_carlo.get("percentiles", {})

    comparable_projects = []

    for item in result.get("comparable_projects", []):
        comparable_projects.append({
            "project_id": item.get("project_id"),
            "distance": item.get("distance"),
            "similarity": item.get(
                "similarity",
                item.get("similarity_score")
            )
        })

    # --------------------------------------------------------------
    # STEP 5: Provide explainability information.
    #
    # These are explanations based on actual pipeline outputs:
    # comparable projects explain the CBR context, BBN probabilities
    # explain cash-flow deviation states, and financial metrics explain
    # the simulated NPV outcomes.
    #
    # SHAP-based LSTM explanations are not invoked in this first version.
    # --------------------------------------------------------------

    yearly_bbn_explanations = []

    for prediction in bbn.get("yearly_predictions", []):
        probabilities = prediction.get("probabilities", {})

        most_likely_state = (
            max(probabilities, key=probabilities.get)
            if probabilities
            else None
        )

        yearly_bbn_explanations.append({
            "year": prediction.get("year"),
            "probabilities": probabilities,
            "most_likely_state": most_likely_state,
            "interpretation": (
                f"Cash-flow deviation is most likely to be "
                f"{most_likely_state}."
                if most_likely_state
                else "No BBN probabilities were returned."
            )
        })

    mean_npv = monte_carlo.get("mean_npv")
    negative_npv_probability = monte_carlo.get(
        "probability_npv_negative"
    )

    financial_explanation = {
        "expected_npv": mean_npv,
        "expected_npv_interpretation": (
            "The mean simulated NPV is negative under the supplied "
            "assumptions."
            if mean_npv is not None and mean_npv < 0
            else (
                "The mean simulated NPV is non-negative under the "
                "supplied assumptions."
                if mean_npv is not None
                else "Mean NPV was not returned by the simulation."
            )
        ),
        "downside_risk_interpretation": (
            f"{negative_npv_probability:.1%} of simulated outcomes "
            "have negative NPV."
            if negative_npv_probability is not None
            else "Negative-NPV probability was not returned."
        ),
        "scope_note": (
            "Financial results cover the forecast horizon only and "
            "depend on the supplied assumptions and simulation model."
        )
    }

    response = {
        "project": result.get("project"),
        "complexity": result.get("complexity"),
        "risk": result.get("risk"),
        "forecastingMethod": result.get("forecasting_method"),

        "forecast": {
            "method": forecast.get("method"),
            "predictedCashFlows": forecast.get(
                "predicted_cash_flows", []
            ),
            "horizonYears": len(
                forecast.get("predicted_cash_flows", [])
            )
        },

        "cbr": {
            "summary": (
                "Comparable historical projects were retrieved "
                "to construct the LSTM context."
            ),
            "comparables": comparable_projects,
            "constructedContext": result.get("cbr_context")
        },

        "bbn": {
            "yearlyPredictions": yearly_bbn_explanations
        },

        "monteCarlo": {
            "simulations": monte_carlo.get("simulations"),
            "meanNPV": mean_npv,
            "medianNPV": monte_carlo.get("median_npv"),
            "stdNPV": monte_carlo.get("std_npv"),
            "probabilityNPVNegative": negative_npv_probability,
            "percentiles": {
                "p10": percentiles.get("p10"),
                "p25": percentiles.get("p25"),
                "p75": percentiles.get("p75"),
                "p90": percentiles.get("p90")
            }
        },

        "explainability": {
            "financial": financial_explanation,
            "notes": [
                "BBN probabilities describe cash-flow deviation states, "
                "not the probability of a positive NPV.",
                "Financial results apply only to the forecast horizon.",
                "SHAP-based LSTM explanations are not yet included."
            ]
        },

        "futureAssumptions": future_assumptions
    }

    return clean_for_json(response)