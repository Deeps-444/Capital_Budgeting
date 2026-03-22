import joblib
import numpy as np
import os

# Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute paths
cost_model_path = os.path.abspath(os.path.join(BASE_DIR, "..", "model", "cost_model.pkl"))
wc_model_path = os.path.abspath(os.path.join(BASE_DIR, "..", "model", "wc_model.pkl"))
capex_model_path = os.path.abspath(os.path.join(BASE_DIR, "..", "model", "capex_model.pkl"))

# Load models
cost_model = joblib.load(cost_model_path)
wc_model = joblib.load(wc_model_path)
capex_model = joblib.load(capex_model_path)


def predict_drivers(input_data: dict):
    """
    input_data: dictionary from API
    returns predicted financial drivers
    """

    # Convert to array (order must match training)
    features = np.array([[
        input_data["initialInvestment"],
        input_data["revenueGrowthRate"],
        input_data["inflationRate"],
        input_data["marketGrowthIndex"],
        input_data["sectorRiskIndex"],
        input_data["discountRate"]
    ]])

    pred_cost = cost_model.predict(features)[0]
    pred_wc = wc_model.predict(features)[0]
    pred_capex = capex_model.predict(features)[0]

    return {
        "operatingCostRatio": float(pred_cost),
        "workingCapitalRatio": float(pred_wc),
        "capexRatio": float(pred_capex)
    }