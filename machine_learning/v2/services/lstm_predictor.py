"""
LSTM-based project cash-flow forecasting.

This module loads the trained LSTM model and its scalers, then performs
recursive multi-step forecasting for a project.

Expected input:
    - 3 historical cash flows
    - 3 historical inflation values
    - 3 historical market-growth values
    - future inflation assumptions
    - future market-growth assumptions

The LSTM predicts one future cash flow at a time. Each prediction is then
fed back into the next input sequence, allowing us to forecast multiple
future years.
"""

import os
import joblib
import numpy as np
from tensorflow.keras.models import load_model


# ---------------------------------------------------------------------------
# 1. Locate the trained model artifacts
# ---------------------------------------------------------------------------
# __file__ points to:
# machine_learning/v2/services/lstm_predictor.py
#
# Therefore:
#   dirname(__file__)          -> services/
#   dirname(dirname(__file__)) -> v2/
#
# The trained model artifacts are stored inside:
# machine_learning/v2/model/
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")


LSTM_MODEL_PATH = os.path.join(MODEL_DIR, "lstm_model.keras")
X_SCALER_PATH = os.path.join(MODEL_DIR, "X_scaler.pkl")
Y_SCALER_PATH = os.path.join(MODEL_DIR, "y_scaler.pkl")


# ---------------------------------------------------------------------------
# 2. Load the trained artifacts once
# ---------------------------------------------------------------------------
# We load these when the module starts rather than loading them every time
# the API receives a prediction request.
#
# This is important for an API because repeatedly loading a neural-network
# model from disk would add unnecessary overhead.
# ---------------------------------------------------------------------------

model = load_model(LSTM_MODEL_PATH)

X_scaler = joblib.load(X_SCALER_PATH)
y_scaler = joblib.load(Y_SCALER_PATH)


# ---------------------------------------------------------------------------
# 3. Model configuration
# ---------------------------------------------------------------------------
# The LSTM was trained using:
#
#   cash_flow
#   inflation_rate
#   market_growth_rate
#
# and a sequence length of 3 years.
# ---------------------------------------------------------------------------

SEQUENCE_LENGTH = 3
NUMBER_OF_FEATURES = 3


# ---------------------------------------------------------------------------
# 4. Recursive multi-step forecasting
# ---------------------------------------------------------------------------

def predict_cashflows(
    historical_cash_flows,
    historical_inflation,
    historical_market_growth,
    forecast_inflation,
    forecast_market_growth
):
    """
    Predict future project cash flows using the trained LSTM.

    Parameters
    ----------
    historical_cash_flows : list
        Cash flows from the most recent 3 historical years.

    historical_inflation : list
        Inflation values corresponding to the same 3 historical years.

    historical_market_growth : list
        Market-growth values corresponding to the same 3 historical years.

    forecast_inflation : list
        Future inflation assumptions, one value for each forecast year.

    forecast_market_growth : list
        Future market-growth assumptions, one value for each forecast year.

    Returns
    -------
    list
        Predicted cash flow for each future year.
    """

    # -----------------------------------------------------------------------
    # Validate the historical sequence.
    # The LSTM was trained with exactly 3 consecutive years as input.
    # -----------------------------------------------------------------------

    if len(historical_cash_flows) != SEQUENCE_LENGTH:
        raise ValueError(
            f"Expected {SEQUENCE_LENGTH} historical cash flows, "
            f"got {len(historical_cash_flows)}."
        )

    if len(historical_inflation) != SEQUENCE_LENGTH:
        raise ValueError(
            f"Expected {SEQUENCE_LENGTH} historical inflation values, "
            f"got {len(historical_inflation)}."
        )

    if len(historical_market_growth) != SEQUENCE_LENGTH:
        raise ValueError(
            f"Expected {SEQUENCE_LENGTH} historical market-growth values, "
            f"got {len(historical_market_growth)}."
        )

    # -----------------------------------------------------------------------
    # Validate the future assumptions.
    #
    # We need one inflation and one market-growth assumption for every
    # future year that we want to predict.
    # -----------------------------------------------------------------------

    if len(forecast_inflation) != len(forecast_market_growth):
        raise ValueError(
            "forecast_inflation and forecast_market_growth "
            "must contain the same number of values."
        )

    if len(forecast_inflation) == 0:
        raise ValueError(
            "At least one future year must be provided for forecasting."
        )

    # -----------------------------------------------------------------------
    # Construct the initial 3-year sequence.
    #
    # Each row represents:
    #
    #     [cash_flow, inflation_rate, market_growth_rate]
    #
    # Example:
    #
    #     Year 1 -> [CF1, inflation1, growth1]
    #     Year 2 -> [CF2, inflation2, growth2]
    #     Year 3 -> [CF3, inflation3, growth3]
    # -----------------------------------------------------------------------

    history = np.column_stack([
        historical_cash_flows,
        historical_inflation,
        historical_market_growth
    ]).astype(float)

    predictions = []

    # -----------------------------------------------------------------------
    # Recursively forecast each future year.
    #
    # For every year:
    #
    #   1. Scale the current 3-year sequence.
    #   2. Give it to the LSTM.
    #   3. Convert the scaled prediction back to actual cash-flow units.
    #   4. Add the prediction to our results.
    #   5. Shift the sequence forward by one year.
    #   6. Use the predicted cash flow as part of the next sequence.
    #
    # This allows the model to forecast more than one year into the future.
    # -----------------------------------------------------------------------

    for step in range(len(forecast_inflation)):

        # Scale the input using the SAME scaler used during training.
        scaled_history = X_scaler.transform(history)

        # Keras expects:
        # (number_of_samples, sequence_length, number_of_features)
        X_input = scaled_history.reshape(
            1,
            SEQUENCE_LENGTH,
            NUMBER_OF_FEATURES
        )

        # Predict the next year's scaled cash flow.
        predicted_cash_flow_scaled = model.predict(
            X_input,
            verbose=0
        )[0, 0]

        # Convert the prediction from scaled space back to actual
        # cash-flow units (e.g. ₹).
        predicted_cash_flow = y_scaler.inverse_transform(
            [[predicted_cash_flow_scaled]]
        )[0, 0]

        predictions.append(float(predicted_cash_flow))

        # -------------------------------------------------------------------
        # Prepare the next sequence.
        #
        # The predicted cash flow becomes the cash-flow value for the newly
        # forecasted year. Inflation and market growth are supplied externally
        # as future assumptions.
        # -------------------------------------------------------------------

        new_row = np.array([
            predicted_cash_flow,
            forecast_inflation[step],
            forecast_market_growth[step]
        ])

        # Remove the oldest year and append the newly predicted year.
        history = np.vstack([
            history[1:],
            new_row
        ])

    return predictions

def predict_from_cbr_context(
    cbr_context,
    future_inflation,
    future_market_growth
):
    """
    Generate future cash-flow forecasts for a new project using
    a CBR-derived historical context.

    CBR supplies the three historical years required by the LSTM.
    This function converts that context into the input format expected
    by the existing predict_cashflows() function.

    Data flow:

        Comparable Projects
                ↓
        CBR-derived 3-year context
                ↓
        Split into historical CF / inflation / market growth
                ↓
        Existing LSTM forecasting function
                ↓
        Future cash-flow forecast
    """

    # -----------------------------------------------------------------------
    # Validate the CBR context.
    #
    # The LSTM was trained with a sequence length of exactly three years.
    # -----------------------------------------------------------------------

    if len(cbr_context) != SEQUENCE_LENGTH:
        raise ValueError(
            f"CBR context must contain exactly "
            f"{SEQUENCE_LENGTH} years."
        )

    # -----------------------------------------------------------------------
    # Validate that every CBR context row contains the three features
    # expected by the LSTM:
    #
    # [cash_flow, inflation_rate, market_growth_rate]
    # -----------------------------------------------------------------------

    for row in cbr_context:
        if len(row) != NUMBER_OF_FEATURES:
            raise ValueError(
                "Each CBR context row must contain exactly "
                f"{NUMBER_OF_FEATURES} values."
            )

    # -----------------------------------------------------------------------
    # Split the CBR context into the three historical input sequences
    # expected by predict_cashflows().
    # -----------------------------------------------------------------------

    historical_cash_flows = [
        row[0] for row in cbr_context
    ]

    historical_inflation = [
        row[1] for row in cbr_context
    ]

    historical_market_growth = [
        row[2] for row in cbr_context
    ]

    # -----------------------------------------------------------------------
    # Reuse the existing LSTM forecasting implementation.
    #
    # This is important because predict_cashflows() already contains:
    #   - input validation
    #   - scaling
    #   - LSTM prediction
    #   - inverse scaling
    #   - recursive sequence updating
    # -----------------------------------------------------------------------

    return predict_cashflows(
        historical_cash_flows=historical_cash_flows,
        historical_inflation=historical_inflation,
        historical_market_growth=historical_market_growth,
        forecast_inflation=future_inflation,
        forecast_market_growth=future_market_growth
    )