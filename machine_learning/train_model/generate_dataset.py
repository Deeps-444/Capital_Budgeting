import numpy as np
import pandas as pd

np.random.seed(42)

n_projects = 6000

data = pd.DataFrame()


# 1. Generate Driver Features

data["initialInvestment"] = np.random.uniform(500000, 5000000, n_projects)

data["revenueGrowthRate"] = np.random.uniform(0.05, 0.20, n_projects)

data["operatingCostRatio"] = np.random.uniform(0.4, 0.7, n_projects)

data["workingCapitalRatio"] = np.random.uniform(0.05, 0.2, n_projects)

data["capexRatio"] = np.random.uniform(0.03, 0.1, n_projects)

data["inflationRate"] = np.random.uniform(0.02, 0.06, n_projects)

data["marketGrowthIndex"] = np.random.uniform(0.8, 1.3, n_projects)

data["sectorRiskIndex"] = np.random.uniform(0.1, 0.4, n_projects)

data["discountRate"] = np.random.uniform(0.08, 0.15, n_projects)


# 2. Generate Base Revenue


base_revenue = data["initialInvestment"] * np.random.uniform(0.4, 0.7, n_projects)

data["revenue_base"] = base_revenue * data["marketGrowthIndex"]


# 3. Generate Yearly Cashflows


wc_previous = np.zeros(n_projects)

for year in range(1,6):

    # Revenue grows each year
    revenue = data["revenue_base"] * (1 + data["revenueGrowthRate"])**year

    # Operating costs
    cost = revenue * data["operatingCostRatio"]

    # Working capital requirement
    wc_current = revenue * data["workingCapitalRatio"]

    delta_wc = wc_current - wc_previous

    # Maintenance CapEx
    capex = data["initialInvestment"] * data["capexRatio"]

    # Free Cashflow
    cashflow = revenue - cost - delta_wc - capex

    # Add economic noise
    noise = np.random.normal(0, 40000, n_projects)

    cashflow = cashflow + noise

    data[f"cf{year}"] = cashflow

    wc_previous = wc_current


# 4. Remove intermediate columns


data = data.drop(columns=["revenue_base"])


# 5. Save dataset


data.to_csv("../data/raw_data/projects_dataset.csv", index=False)

print("Dataset generated successfully")
print("Shape:", data.shape)