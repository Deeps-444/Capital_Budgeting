"""
BBN Predictor Service
---------------------

Loads the trained Bayesian Belief Network and its training-derived
discretization boundaries.

The BBN receives observable project/economic conditions:

    - Project complexity
    - Future inflation
    - Future market growth

These continuous values are converted into the same Low / Medium / High
states used when training the BBN.

The BBN then returns:

    P(Worse)
    P(Near Expected)
    P(Better)

Important:
- The BBN does NOT receive the LSTM prediction.
- The BBN does NOT directly modify the cash flow.
- The probabilities produced here will later be used by Monte Carlo
  together with the empirical LSTM deviation distributions.
"""

from pathlib import Path
import joblib


import pandas as pd
from pgmpy.inference import VariableElimination


# ---------------------------------------------------------------------------
# MODEL PATHS
# ---------------------------------------------------------------------------
# The trained BBN and its discretization boundaries were copied into the
# V2 model directory during the model-integration stage.
#
# Using paths relative to this file keeps the service independent of the
# directory from which test.py or the API is executed.
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "model"

BBN_MODEL_PATH = MODEL_DIR / "bbn_model.pkl"
BBN_BINS_PATH = MODEL_DIR / "bbn_bins.pkl"


# ---------------------------------------------------------------------------
# LOAD TRAINED BBN
# ---------------------------------------------------------------------------
# The BBN was trained in the research notebook and serialized for reuse.
# We load the trained network rather than retraining it every time the
# application starts.
# ---------------------------------------------------------------------------

bbn_model = joblib.load(BBN_MODEL_PATH)


# ---------------------------------------------------------------------------
# LOAD TRAINING-DERIVED DISCRETIZATION BOUNDARIES
# ---------------------------------------------------------------------------
# These boundaries must remain fixed during inference.
#
# They were learned from the training data and are therefore reused for
# new projects instead of calculating new quantiles from the incoming
# project or the complete dataset.
# ---------------------------------------------------------------------------

bbn_bins = joblib.load(BBN_BINS_PATH)


# ---------------------------------------------------------------------------
# CREATE BAYESIAN INFERENCE ENGINE
# ---------------------------------------------------------------------------
# VariableElimination performs probabilistic inference on the trained BBN.
# ---------------------------------------------------------------------------

bbn_inference = VariableElimination(bbn_model)


def _to_bbn_state(value, column):
    """
    Convert a continuous value into the Low / Medium / High state used
    by the trained BBN.

    The important point is that the boundaries come from bbn_bins,
    which were learned during training.

    Parameters
    ----------
    value:
        Continuous input value.

    column:
        Name of the original continuous variable whose boundaries
        should be used.

    Returns
    -------
    str
        One of:
            Low
            Medium
            High
    """

    if column not in bbn_bins:
        raise ValueError(
            f"No trained BBN discretization boundaries found "
            f"for '{column}'."
        )

    state = pd.cut(
        [value],
        bins=bbn_bins[column],
        labels=["Low", "Medium", "High"],
        include_lowest=True
    )[0]

    if pd.isna(state):
        raise ValueError(
            f"Value {value} could not be mapped to a BBN state "
            f"for '{column}'."
        )

    return str(state)


def infer_cash_flow_state(
    complexity,
    inflation,
    market_growth
):
    """
    Infer the probability distribution of future cash-flow deviation
    states for a proposed project.

    Parameters
    ----------
    complexity:
        Project complexity index.

    inflation:
        Inflation assumption for the forecast period.

    market_growth:
        Market-growth assumption for the forecast period.

    Returns
    -------
    dict
        Probability distribution over:

            Better
            Near Expected
            Worse

    Example
    -------
    {
        "Better": 0.326,
        "Near Expected": 0.293,
        "Worse": 0.380
    }
    """

    # ------------------------------------------------------------------
    # Convert continuous inputs into the categorical states expected by
    # the trained BBN.
    # ------------------------------------------------------------------

    evidence = {
        "complexity_state": _to_bbn_state(
            complexity,
            "complexity_index"
        ),

        "inflation_state": _to_bbn_state(
            inflation,
            "inflation_rate"
        ),

        "market_growth_state": _to_bbn_state(
            market_growth,
            "market_growth_rate"
        )
    }

    # ------------------------------------------------------------------
    # Perform Bayesian inference.
    #
    # The BBN estimates the probability distribution of the
    # cash_flow_evidence node conditioned on the observable evidence.
    # ------------------------------------------------------------------

    result = bbn_inference.query(
        variables=["cash_flow_evidence"],
        evidence=evidence,
        show_progress=False
    )

    # ------------------------------------------------------------------
    # Extract the state names and their corresponding probabilities.
    # ------------------------------------------------------------------

    state_names = result.state_names["cash_flow_evidence"]
    probabilities = result.values

    return {
        state: float(probabilities[index])
        for index, state in enumerate(state_names)
    }