import numpy as np
import pandas as pd

np.random.seed(42)

n_projects = 6000
data = pd.DataFrame()

# 1. Generate Driver Features
data["initialInvestment"] = np.random.uniform(500000, 5000000, n_projects)
data["revenueGrowthRate"] = np.random.uniform(0.05, 0.20, n_projects)
data["inflationRate"] = np.random.uniform(0.02, 0.06, n_projects)
data["marketGrowthIndex"] = np.random.uniform(0.8, 1.3, n_projects)
data["sectorRiskIndex"] = np.random.uniform(0.1, 0.4, n_projects)
data["discountRate"] = np.random.uniform(0.08, 0.15, n_projects)

# Operating Cost Ratio
data["operatingCostRatio"] = (
    0.4
    + 0.25 * data["sectorRiskIndex"]
    + 0.2 * data["inflationRate"]
    - 0.2 * data["marketGrowthIndex"]
    + 0.1 * (data["revenueGrowthRate"] ** 2)
    + np.random.normal(0, 0.01, n_projects)
)

# High risk spikes
high_risk = data["sectorRiskIndex"] > 0.3
data.loc[high_risk, "operatingCostRatio"] += np.random.uniform(0.05, 0.15, high_risk.sum())

# Clamp ratios (IMPORTANT)
data["operatingCostRatio"] = np.clip(data["operatingCostRatio"], 0.2, 0.9)

# Working Capital
data["workingCapitalRatio"] = (
    0.08
    + 0.3 * data["revenueGrowthRate"]
    + 0.15 * data["inflationRate"]
    + 0.1 * data["sectorRiskIndex"]
    + np.random.normal(0, 0.008, n_projects)
)
data["workingCapitalRatio"] = np.clip(data["workingCapitalRatio"], 0.05, 0.4)

# Capex Ratio
data["capexRatio"] = (
    0.04
    + 0.25 * data["sectorRiskIndex"]
    + 0.15 * data["marketGrowthIndex"]
    + 0.1 * (data["initialInvestment"] / 5000000)
    + np.random.normal(0, 0.008, n_projects)
)
data["capexRatio"] = np.clip(data["capexRatio"], 0.03, 0.5)

# Base Revenue
base_revenue = data["initialInvestment"] * np.random.uniform(0.4, 0.7, n_projects)
data["revenue_base"] = base_revenue * data["marketGrowthIndex"]

# Project-specific economic sensitivity
project_sensitivity = np.random.uniform(0.8, 1.2, n_projects)

# Failure mask (project-level)
failure_mask = np.random.rand(n_projects) < 0.1

# Cashflow generation
wc_previous = np.zeros(n_projects)

for year in range(1, 6):

    # Revenue
    revenue = data["revenue_base"] * (1 + data["revenueGrowthRate"])**year

    # Economic shock (project-specific)
    shock = np.random.choice(
        ["boom", "normal", "recession"],
        size=n_projects,
        p=[0.2, 0.6, 0.2]
    )

    boom_mask = shock == "boom"
    recession_mask = shock == "recession"

    revenue[boom_mask] *= np.random.uniform(1.05, 1.2, boom_mask.sum())
    revenue[recession_mask] *= np.random.uniform(0.6, 0.9, recession_mask.sum())

    revenue *= project_sensitivity

    # Costs
    cost = revenue * data["operatingCostRatio"]
    cost *= np.random.uniform(0.9, 1.15, n_projects)

    # Working capital
    wc_current = revenue * data["workingCapitalRatio"]
    delta_wc = wc_current - wc_previous

    # Capex (decreasing)
    capex = data["initialInvestment"] * data["capexRatio"] / year

    # Cashflow
    cashflow = revenue - cost - delta_wc - capex

    # Noise (scaled)
    noise = revenue * np.random.normal(0, 0.08, n_projects)
    cashflow += noise

    # Apply failure EACH YEAR (FIXED)
    cashflow[failure_mask] *= np.random.uniform(0.2, 0.5, failure_mask.sum())

    # Allow negative but bounded
    cashflow = np.clip(cashflow, -data["initialInvestment"] * 0.5, None)

    data[f"cf{year}"] = cashflow

    wc_previous = wc_current

# Remove temp column
data = data.drop(columns=["revenue_base"])

# Save
data.to_csv("../data/raw_data/projects_dataset.csv", index=False)

print("Dataset generated successfully")
print("Shape:", data.shape)