import os
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import joblib

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "..", "data", "raw_data", "projects_dataset.csv")
MODEL_DIR = os.path.join(BASE, "..", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

# 1) Generate dataset if missing
if not os.path.exists(RAW):
    print("Generating dataset...")
    np.random.seed(42)
    n = 6000
    data = pd.DataFrame({
        "initialInvestment": np.random.uniform(500000, 5000000, n),
        "revenueGrowthRate": np.random.uniform(0.05, 0.20, n),
        "inflationRate": np.random.uniform(0.02, 0.06, n),
        "marketGrowthIndex": np.random.uniform(0.8, 1.3, n),
        "sectorRiskIndex": np.random.uniform(0.1, 0.4, n),
        "discountRate": np.random.uniform(0.08, 0.15, n),
    })
    data["operatingCostRatio"] = np.clip(
        0.4 + 0.25 * data["sectorRiskIndex"] + 0.2 * data["inflationRate"]
        - 0.2 * data["marketGrowthIndex"] + 0.1 * (data["revenueGrowthRate"] ** 2)
        + np.random.normal(0, 0.01, n),
        0.2, 0.9,
    )
    data["workingCapitalRatio"] = np.clip(
        0.08 + 0.3 * data["revenueGrowthRate"] + 0.15 * data["inflationRate"]
        + 0.1 * data["sectorRiskIndex"] + np.random.normal(0, 0.008, n),
        0.05, 0.4,
    )
    data["capexRatio"] = np.clip(
        0.04 + 0.25 * data["sectorRiskIndex"] + 0.15 * data["marketGrowthIndex"]
        + 0.1 * (data["initialInvestment"] / 5000000) + np.random.normal(0, 0.008, n),
        0.03, 0.5,
    )
    os.makedirs(os.path.dirname(RAW), exist_ok=True)
    data.to_csv(RAW, index=False)
    print("Dataset saved:", RAW)
else:
    data = pd.read_csv(RAW)
    print("Loaded existing dataset:", data.shape)

FEATURES = [
    "initialInvestment",
    "revenueGrowthRate",
    "inflationRate",
    "marketGrowthIndex",
    "sectorRiskIndex",
    "discountRate",
]
X = data[FEATURES]

targets = {
    "cost_model.pkl": "operatingCostRatio",
    "wc_model.pkl": "workingCapitalRatio",
    "capex_model.pkl": "capexRatio",
}

for filename, target in targets.items():
    print(f"Training {filename}...")
    y = data[target]
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X, y)
    path = os.path.join(MODEL_DIR, filename)
    joblib.dump(model, path)
    print("  saved →", path)

print("\nDone. Models are ready.")