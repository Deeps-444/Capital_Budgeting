from fastapi import FastAPI
from monte_carlo import monte_carlo_simulation
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("model/cashflow_model.pkl")


@app.get("/")
def home():
    return {"message": "ML Service Running"}


@app.post("/predict")
def predict(data: dict):

    # 🔹 extract inputs properly
    initial_investment = data["initialInvestment"]
    discount_rate = data["discountRate"]

    # 🔹 prepare features for ML model
    features = np.array([[
        data["initialInvestment"],
        data["revenueGrowthRate"],
        data["operatingCostRatio"],
        data["workingCapitalRatio"],
        data["capexRatio"],
        data["inflationRate"],
        data["marketGrowthIndex"],
        data["sectorRiskIndex"],
        data["discountRate"]
    ]])

    # predict cashflows
    predicted = model.predict(features)

    # IMPORTANT: ensure it's a list/array of 5 values
    cashflows = np.array(predicted).flatten()

    #call Monte Carlo
    mc_result = monte_carlo_simulation(
        cashflows,
        initial_investment,
        discount_rate
    )

    return mc_result