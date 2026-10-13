"""
Forecasting model router for the V2 Capital Budgeting DSS.

The router does not perform machine learning itself.

Its responsibility is to inspect the structured project information and
determine which forecasting pathway should be used:

1. LSTM
   Used when sufficient project-specific historical cash-flow data exists.

2. CBR + LSTM
   Used when project-specific historical cash-flow data is unavailable.
   CBR first identifies comparable completed projects, which can then provide
   historical context for the forecasting stage.

Keeping this decision as explicit business logic makes the DSS easier to
understand, test, and explain.
"""


# ---------------------------------------------------------------------------
# Minimum historical data required by our LSTM
# ---------------------------------------------------------------------------
# Our trained LSTM expects a sequence of 3 consecutive project years.
#
# Therefore, we only consider project-specific historical cash-flow data
# sufficient when at least 3 usable historical observations are available.
# ---------------------------------------------------------------------------

MIN_HISTORICAL_YEARS = 3


def has_sufficient_historical_data(historical_cash_flows):
    """
    Check whether enough project-specific historical cash-flow data exists.

    Parameters
    ----------
    historical_cash_flows : list or None
        Historical cash-flow observations extracted from the project data.

    Returns
    -------
    bool
        True if at least 3 valid historical cash-flow observations exist.
    """

    if historical_cash_flows is None:
        return False

    # Remove missing values while preserving the actual observations.
    valid_cash_flows = [
        value
        for value in historical_cash_flows
        if value is not None
    ]

    return len(valid_cash_flows) >= MIN_HISTORICAL_YEARS


def select_forecasting_method(historical_cash_flows):
    """
    Select the appropriate forecasting pathway.

    Returns
    -------
    dict
        Contains the selected method and an explanation that can later be
        shown to the user in the DSS interface.
    """

    # -----------------------------------------------------------------------
    # Path 1:
    # Sufficient project-specific historical data exists.
    #
    # The LSTM can directly use the project's historical trajectory.
    # -----------------------------------------------------------------------

    if has_sufficient_historical_data(historical_cash_flows):

        return {
            "method": "LSTM",
            "reason": (
                "Sufficient project-specific historical cash-flow "
                "data is available."
            )
        }

    # -----------------------------------------------------------------------
    # Path 2:
    # Historical project data is unavailable or insufficient.
    #
    # We should NOT fabricate historical cash flows.
    #
    # Instead, the system will use CBR to identify comparable completed
    # projects before proceeding to the forecasting stage.
    # -----------------------------------------------------------------------

    return {
        "method": "CBR_LSTM",
        "reason": (
            "Insufficient project-specific historical cash-flow data "
            "is available. Comparable completed projects will be "
            "identified using Case-Based Reasoning."
        )
    }