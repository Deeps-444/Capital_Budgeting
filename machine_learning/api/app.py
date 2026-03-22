from fastapi import FastAPI
from services.predictor import predict_drivers
from services.cashflow_engine import calculate_cashflows
from monte_carlo import monte_carlo_simulation

app = FastAPI()


@app.get("/")
def home():
    return {"message": "ML Service Running (DSS Mode)"}


@app.post("/predict")
def predict(data: dict):

    # Predict drivers
    drivers = predict_drivers(data)

    #  Calculate cashflows
    cashflow_results = calculate_cashflows(
        data,
        drivers["operatingCostRatio"],
        drivers["workingCapitalRatio"],
        drivers["capexRatio"]
    )

    # Extract only CF values for Monte Carlo
    cashflows = [year["cashflow"] for year in cashflow_results]

    # Monte Carlo
    mc_result = monte_carlo_simulation(
        cashflows,
        data["initialInvestment"],
        data["discountRate"]
    )

   

    return {
        "predictedDrivers": drivers,
        "cashflows": cashflow_results,
        "monteCarlo": mc_result,    
    }