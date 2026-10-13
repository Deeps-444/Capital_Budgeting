"""
LSTM Explainability Service
---------------------------

This module explains an individual LSTM cash-flow prediction using SHAP.

The trained LSTM receives a 3-year sequence containing:

    [cash_flow, inflation_rate, market_growth_rate]

for each historical year.

The explainer therefore produces a SHAP contribution for every
year-feature combination, allowing us to answer:

    "Which historical values contributed to this forecast,
     and in which direction?"

The explainer is kept separate from lstm_predictor.py so that
forecasting and explainability remain independent services.
"""

import os
import numpy as np
import shap

from ..lstm_predictor import model, X_scaler, y_scaler


# ---------------------------------------------------------------------------
# 1. Model configuration
# ---------------------------------------------------------------------------
#
# These values must remain consistent with the trained LSTM.
#
# Input shape:
#     3 historical years × 3 features
#
# Feature order:
#     cash_flow
#     inflation_rate
#     market_growth_rate
# ---------------------------------------------------------------------------

SEQUENCE_LENGTH = 3

FEATURE_NAMES = [
    "cash_flow",
    "inflation_rate",
    "market_growth_rate"
]


# ---------------------------------------------------------------------------
# 2. Build a SHAP explainer
# ---------------------------------------------------------------------------
#
# The LSTM is a neural-network model, so we use SHAP's DeepExplainer
# rather than TreeExplainer, which is intended for tree-based models.
#
# The background dataset represents a neutral reference input.
#
# IMPORTANT:
# This first implementation explains the first forecast year only.
# The recursive later-year predictions will be handled separately
# if required.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Load the representative training sequences used as SHAP's reference.
# These sequences must already be scaled exactly as the LSTM expects.
# ---------------------------------------------------------------------------

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BACKGROUND_PATH = PROJECT_ROOT / "model" / "shap_background.npy"


# ------------------------------------------------------------
# LOAD AND SCALE SHAP BACKGROUND DATA
#
# The LSTM was trained on inputs transformed using X_scaler.
# SHAP background sequences must use the same scaled feature
# space as the sequences passed to the trained model.
# ------------------------------------------------------------


background_data = np.load(BACKGROUND_PATH).astype(np.float32)

background_shape = background_data.shape

background_data = X_scaler.transform(
    background_data.reshape(-1, len(FEATURE_NAMES))
).reshape(background_shape).astype(np.float32)

print(
    "EXPLAINER BACKGROUND AFTER SCALING:",
    background_data.shape,
    float(background_data.min()),
    float(background_data.max())
)

def _build_explainer():
    """
    Create a prediction-based SHAP explainer.

    The model receives a 3-year sequence with 3 features per year.
    We flatten that sequence to 9 values for SHAP, then reshape
    each perturbed sample back to (3, 3) before prediction.

    This avoids relying on TensorFlow's gradient implementation.
    """

    def predict_flattened(flat_inputs):
        flat_inputs = np.asarray(flat_inputs)

        # Restore the LSTM input shape:
        # (samples, 9) -> (samples, 3 years, 3 features)
        sequence_inputs = flat_inputs.reshape(
            -1,
            SEQUENCE_LENGTH,
            len(FEATURE_NAMES)
        )

        # The LSTM expects scaled inputs and produces scaled outputs.
        scaled_predictions = model.predict(
            sequence_inputs,
            verbose=0
        )

        # Explain predictions in original cash-flow units.
        return y_scaler.inverse_transform(
            scaled_predictions
        ).reshape(-1)

    background_flat = background_data.reshape(
        len(background_data),
        -1
    )

    masker = shap.maskers.Independent(background_flat)

    return shap.PermutationExplainer(
        predict_flattened,
        masker
    )


# ---------------------------------------------------------------------------
# 3. Explain one forecast
# ---------------------------------------------------------------------------

def explain_lstm_prediction(
    historical_cash_flows,
    historical_inflation,
    historical_market_growth
):
    """
    Explain the LSTM's next-year cash-flow prediction.

    Parameters
    ----------
    historical_cash_flows : list
        Three historical cash-flow values.

    historical_inflation : list
        Three historical inflation values.

    historical_market_growth : list
        Three historical market-growth values.

    background_data : numpy.ndarray
        Reference sequences used by SHAP.

    Returns
    -------
    dict
        Structured explanation containing:

        - predicted cash flow
        - SHAP contribution for each input feature
        - feature values
        - total contribution
    """

    # -----------------------------------------------------------------------
    # Validate the historical input.
    #
    # The trained model expects exactly three historical observations.
    # -----------------------------------------------------------------------

    if len(historical_cash_flows) != SEQUENCE_LENGTH:
        raise ValueError(
            f"Expected {SEQUENCE_LENGTH} historical cash flows."
        )

    if len(historical_inflation) != SEQUENCE_LENGTH:
        raise ValueError(
            f"Expected {SEQUENCE_LENGTH} historical inflation values."
        )

    if len(historical_market_growth) != SEQUENCE_LENGTH:
        raise ValueError(
            f"Expected {SEQUENCE_LENGTH} historical market-growth values."
        )

    # -----------------------------------------------------------------------
    # Construct the same 3 × 3 input structure used by the LSTM.
    #
    # Each row represents one historical year:
    #
    #     [cash_flow, inflation, market_growth]
    # -----------------------------------------------------------------------

    # Build the historical sequence in the original feature units.
    input_sequence = np.column_stack([
        historical_cash_flows,
        historical_inflation,
        historical_market_growth
    ]).astype(float)

    # Scale each feature using the same scaler used during LSTM training.
    scaled_sequence = X_scaler.transform(input_sequence)

    # Keras expects: (samples, timesteps, features).
    model_input = scaled_sequence.reshape(
        1,
        SEQUENCE_LENGTH,
        len(FEATURE_NAMES)
    ).astype(np.float32)

    # -----------------------------------------------------------------------
    # Create the explainer and calculate SHAP values.
    # -----------------------------------------------------------------------

    
    # Flatten the single sequence because PermutationExplainer operates
    # on tabular inputs. The prediction wrapper restores the LSTM shape.
    flat_input = model_input.reshape(1, -1)

    explainer = _build_explainer()

    # Each permutation evaluates different combinations of the nine inputs.
    # A larger number improves the approximation but takes longer.
    shap_values = explainer(
        flat_input,
        max_evals=200
    ).values

    # Expected output shape: (1, 9, 1) or (1, 9), depending on SHAP version.
    shap_values = np.asarray(shap_values).reshape(1, -1)
    shap_values = shap_values[0].reshape(
        SEQUENCE_LENGTH,
        len(FEATURE_NAMES)
    )

    shap_values = np.asarray(shap_values)

    # Remove unnecessary output dimensions if present.
    shap_values = np.squeeze(shap_values)
    

    # -----------------------------------------------------------------------
    # Obtain the actual model prediction.
    #
    # This is the same first-step prediction that the LSTM produces
    # before recursive forecasting begins.
    # -----------------------------------------------------------------------

    # The LSTM outputs a scaled cash-flow value.
    scaled_prediction = model.predict(
        model_input,
        verbose=0
    )
    

# Convert it back to the original cash-flow units.
    prediction = float(
        y_scaler.inverse_transform(scaled_prediction)[0, 0]
    )

    # -----------------------------------------------------------------------
    # Convert SHAP values into a structured format.
    #
    # This representation is much easier for the API and React frontend
    # to consume than a raw SHAP tensor.
    # -----------------------------------------------------------------------

    contributions = []

    for year_index in range(SEQUENCE_LENGTH):

        year_contributions = {}

        for feature_index, feature_name in enumerate(FEATURE_NAMES):

            contribution = float(
                shap_values[year_index, feature_index]
            )

            year_contributions[feature_name] = {
                "value": float(
                    input_sequence[year_index, feature_index]
                ),
                "shap_value": contribution
            }

        contributions.append({
            "historical_year_position": year_index + 1,
            "features": year_contributions
        })
        
        # ---------------------------------------------------------------------------
        # Validate the SHAP explanation.
        #
        # For a single-output model, the SHAP contributions should approximately
        # sum to:
        #
        #     prediction - expected_value
        #
        # The expected value is the model's average prediction over the background
        # dataset. This check helps identify shape, scaling, or attribution issues.
        # ---------------------------------------------------------------------------
    
        flat_input = model_input.reshape(1, -1)
    
        # Calculate the model's prediction on the background dataset.
        background_flat = background_data.reshape(len(background_data), -1)
    
        def predict_flattened(flat_inputs):
            sequence_inputs = np.asarray(flat_inputs).reshape(
                -1, SEQUENCE_LENGTH, len(FEATURE_NAMES)
            )
            scaled_predictions = model.predict(sequence_inputs, verbose=0)
            return y_scaler.inverse_transform(scaled_predictions).reshape(-1)
    
        background_predictions = predict_flattened(background_flat)
        expected_value = float(np.mean(background_predictions))
    
        contribution_sum = float(np.sum(shap_values))
    
        print("\n=== SHAP VALIDATION ===")
        print("Prediction (original units):", prediction)
        print("Background expected value:", expected_value)
        print("Prediction minus baseline:", prediction - expected_value)
        print("Sum of SHAP contributions:", contribution_sum)
        print(
            "Additivity difference:",
            (prediction - expected_value) - contribution_sum
        )

    return {
        "prediction": prediction,
        "contributions": contributions
    }