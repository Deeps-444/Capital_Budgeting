"""
Risk-Aware Monte Carlo Simulation
---------------------------------

This module converts the LSTM + BBN forecast into a probabilistic
financial assessment.

For every Monte Carlo simulation:

    1. For each forecast year, obtain the BBN probability distribution.
    2. Sample one cash-flow state:
           Better
           Near Expected
           Worse
    3. Sample an empirical LSTM prediction deviation belonging to
       that state.
    4. Apply the sampled deviation to the LSTM baseline cash flow.
    5. Calculate the NPV of the resulting cash-flow path.

The deviation distributions were learned from historical LSTM
prediction errors. Therefore, this module does not introduce arbitrary
risk adjustments such as "high risk = -20%".

The output is an NPV distribution from which the DSS can calculate:

    - Expected NPV
    - Median NPV
    - NPV standard deviation
    - Percentiles
    - Probability(NPV < 0)
"""


from pathlib import Path

import joblib
import numpy as np


# ---------------------------------------------------------------------------
# MODEL ARTIFACT
# ---------------------------------------------------------------------------
# The deviation distributions were learned during the research stage and
# saved for reuse during inference.
#
# Each distribution contains historical LSTM prediction deviations
# associated with one BBN cash-flow state.
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

DEVIATION_DISTRIBUTIONS_PATH = (
    MODEL_DIR / "deviation_distributions.pkl"
)

deviation_distributions = joblib.load(
    DEVIATION_DISTRIBUTIONS_PATH
)


# ---------------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------------

VALID_STATES = {
    "Better",
    "Near Expected",
    "Worse"
}


def _validate_deviation_distributions():
    """
    Verify that all BBN states required by the Monte Carlo simulation
    have empirical deviation observations available.
    """

    missing_states = [
        state
        for state in VALID_STATES
        if state not in deviation_distributions
    ]

    if missing_states:
        raise ValueError(
            "Deviation distributions are missing states: "
            f"{missing_states}"
        )

    for state in VALID_STATES:

        values = np.asarray(
            deviation_distributions[state],
            dtype=float
        )

        if len(values) == 0:
            raise ValueError(
                f"No empirical deviations available for state '{state}'."
            )


_validate_deviation_distributions()


def _sample_state(probabilities):
    """
    Sample one cash-flow deviation state from the BBN probability
    distribution.

    Parameters
    ----------
    probabilities : dict
        Example:

        {
            "Better": 0.43,
            "Near Expected": 0.43,
            "Worse": 0.14
        }

    Returns
    -------
    str
        One of Better, Near Expected, Worse.
    """

    missing_states = [
        state
        for state in VALID_STATES
        if state not in probabilities
    ]

    if missing_states:
        raise ValueError(
            f"BBN probabilities are missing states: {missing_states}"
        )

    states = [
        "Better",
        "Near Expected",
        "Worse"
    ]

    probabilities_array = np.array(
        [probabilities[state] for state in states],
        dtype=float
    )

    if np.any(probabilities_array < 0):
        raise ValueError(
            "BBN probabilities cannot contain negative values."
        )

    probability_sum = probabilities_array.sum()

    if probability_sum <= 0:
        raise ValueError(
            "BBN probabilities must have a positive sum."
        )

    # Numerical normalization protects against tiny floating-point
    # differences while preserving the relative BBN probabilities.
    probabilities_array = (
        probabilities_array / probability_sum
    )

    return np.random.choice(
        states,
        p=probabilities_array
    )


def _sample_deviation(state):
    """
    Sample one historical LSTM prediction deviation from the empirical
    distribution associated with the selected BBN state.
    """

    values = np.asarray(
        deviation_distributions[state],
        dtype=float
    )

    return float(
        np.random.choice(values)
    )


def run_monte_carlo(
    predicted_cash_flows,
    bbn_predictions,
    initial_investment,
    discount_rate,
    simulations=10000
):
    """
    Run the risk-aware Monte Carlo financial simulation.

    Parameters
    ----------
    predicted_cash_flows : list[float]
        Baseline future cash-flow predictions produced by the LSTM.

    bbn_predictions : list[dict]
        Year-specific BBN results produced by project_pipeline.py.

        Each element must contain:

            {
                "year": 1,
                "baseline_cash_flow": ...,
                "probabilities": {
                    "Better": ...,
                    "Near Expected": ...,
                    "Worse": ...
                }
            }

    initial_investment : float
        Initial project investment.

    discount_rate : float
        Discount rate used for NPV calculation.

    simulations : int
        Number of Monte Carlo paths.

    Returns
    -------
    dict
        Financial risk distribution and summary statistics.
    """

    if len(predicted_cash_flows) == 0:
        raise ValueError(
            "At least one predicted cash flow is required."
        )

    if len(predicted_cash_flows) != len(bbn_predictions):
        raise ValueError(
            "The number of predicted cash flows must match the "
            "number of BBN predictions."
        )

    if initial_investment <= 0:
        raise ValueError(
            "Initial investment must be greater than zero."
        )

    if discount_rate < 0:
        raise ValueError(
            "Discount rate cannot be negative."
        )

    if simulations <= 0:
        raise ValueError(
            "Number of simulations must be greater than zero."
        )

    # ------------------------------------------------------------------
    # Store simulated NPV outcomes.
    # ------------------------------------------------------------------

    npv_results = np.empty(
        simulations,
        dtype=float
    )

    # ------------------------------------------------------------------
    # Store one simulated cash-flow path for each simulation only while
    # calculating the NPV. We do not need to retain all paths because
    # the DSS primarily needs the NPV distribution.
    # ------------------------------------------------------------------

    for simulation in range(simulations):

        simulated_cash_flows = []

        for year_index, baseline_cash_flow in enumerate(
            predicted_cash_flows
        ):

            # ----------------------------------------------------------
            # STEP 1:
            # Sample a cash-flow state according to the BBN posterior.
            # ----------------------------------------------------------

            probabilities = (
                bbn_predictions[year_index]["probabilities"]
            )

            state = _sample_state(probabilities)

            # ----------------------------------------------------------
            # STEP 2:
            # Sample an empirical LSTM prediction deviation belonging
            # to that BBN state.
            # ----------------------------------------------------------

            deviation = _sample_deviation(state)

            # ----------------------------------------------------------
            # STEP 3:
            # Apply the historically observed deviation to the LSTM
            # baseline forecast.
            #
            # Example:
            #
            # baseline CF = ₹30M
            # deviation   = -0.20
            #
            # simulated CF = ₹30M × (1 - 0.20)
            #              = ₹24M
            # ----------------------------------------------------------

            simulated_cash_flow = (
                baseline_cash_flow *
                (1.0 + deviation)
            )

            simulated_cash_flows.append(
                simulated_cash_flow
            )

        # --------------------------------------------------------------
        # STEP 4:
        # Calculate NPV for the simulated future cash-flow path.
        #
        # Initial investment occurs at time 0, therefore it is not
        # discounted.
        # --------------------------------------------------------------

        npv = -float(initial_investment)

        for year, cash_flow in enumerate(
            simulated_cash_flows,
            start=1
        ):
            npv += (
                cash_flow /
                ((1.0 + discount_rate) ** year)
            )

        npv_results[simulation] = npv

    # ------------------------------------------------------------------
    # FINANCIAL DISTRIBUTION SUMMARY
    # ------------------------------------------------------------------

    mean_npv = np.mean(npv_results)
    median_npv = np.median(npv_results)
    std_npv = np.std(npv_results)

    p10 = np.percentile(npv_results, 10)
    p25 = np.percentile(npv_results, 25)
    p75 = np.percentile(npv_results, 75)
    p90 = np.percentile(npv_results, 90)

    probability_negative_npv = np.mean(
        npv_results < 0
    )

    return {
        "simulations": int(simulations),

        "mean_npv": float(mean_npv),

        "median_npv": float(median_npv),

        "std_npv": float(std_npv),

        "probability_npv_negative": float(
            probability_negative_npv
        ),

        "percentiles": {
            "p10": float(p10),
            "p25": float(p25),
            "p75": float(p75),
            "p90": float(p90)
        },

        # Retained so the frontend can later construct an NPV
        # distribution visualization.
        "npv_distribution": npv_results.tolist()
    }