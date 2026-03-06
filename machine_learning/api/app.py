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

    cashflows = model.predict(features)[0]

    npv_dist, mean_npv, risk = monte_carlo_simulation(
        cashflows,
        data["initialInvestment"],
        data["discountRate"]
    )


    return {
        "predictedCashflows": cashflows.tolist(),
        "meanNPV": float(mean_npv),
        "riskProbability": float(risk),
        "npvDistribution": npv_dist.tolist()
    }