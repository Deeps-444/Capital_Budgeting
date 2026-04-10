from fastapi import FastAPI
from services.predictor import predict_drivers
from services.cashflow_engine import calculate_cashflows
from monte_carlo import monte_carlo_simulation
from services.financial_metrics import calculate_npv, calculate_irr
import math
app = FastAPI()

def clean_value(x):
    if x is None:
        return 0.0
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return 0.0
    return float(x)

@app.get("/")
def home():
    return {"message": "ML Service Running (DSS Mode)"}


@app.post("/predict")
def predict(data: dict):
    data["revenueGrowthRate"] = data["revenueGrowthRate"] 
    data["discountRate"] = data["discountRate"]/100 

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

    npv = calculate_npv(
      cashflows,
      data["initialInvestment"],
      data["discountRate"]
    )

    irr = calculate_irr(
      cashflows,
      data["initialInvestment"]
   )
    print("----- DEBUG -----")
    print("Cashflows:", cashflows)
    print("Initial Investment:", data["initialInvestment"])
    print("Discount Rate:", data["discountRate"])
    print("npv:", npv)
    print("irr:", irr)
    print("-----------------")
   
   # This should match ML response DTO in backend
    return {
        "predictedDrivers": drivers,
        "cashflows": cashflow_results,
        "monteCarlo": {
            "meanNPV": clean_value(mc_result.get("meanNPV")),
            "stdNPV": clean_value(mc_result.get("stdNPV")),
            "riskProbability": clean_value(mc_result.get("riskProbability")),
            "percentiles": {
               "p10": clean_value(mc_result.get("percentiles", {}).get("p10")),
               "p50": clean_value(mc_result.get("percentiles", {}).get("p50")),
               "p90": clean_value(mc_result.get("percentiles", {}).get("p90"))
            }
        },  
        "npv": clean_value(npv),
        "irr": clean_value(irr)
    }