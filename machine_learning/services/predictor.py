import joblib
import numpy as np
import os
import pandas as pd

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
    features = pd.DataFrame([input_data])[
    ["initialInvestment","revenueGrowthRate","inflationRate",
     "marketGrowthIndex","sectorRiskIndex","discountRate"]
    ]
    features["revenueGrowthRate"] /= 100
    features["inflationRate"] /= 100
    # features["marketGrowthIndex"] /= 100   # if frontend sends %
    # features["sectorRiskIndex"] /= 100     # if %
    features["discountRate"] /= 100
    

    pred_cost = cost_model.predict(features)[0]
    pred_wc = wc_model.predict(features)[0]
    pred_capex = capex_model.predict(features)[0]

    pred_cost = np.clip(pred_cost, 0.2, 0.9)
    pred_wc = np.clip(pred_wc, 0.05, 0.4)
    pred_capex = np.clip(pred_capex, 0.03, 0.5)

    return {
        "operatingCostRatio": float(pred_cost),
        "workingCapitalRatio": float(pred_wc),
        "capexRatio": float(pred_capex)
    }