import numpy as np
def calculate_cashflows(inputs, cost_ratio, wc_ratio, capex_ratio):

    results = []

    initial_investment = inputs["initialInvestment"]
    growth_rate = inputs["revenueGrowthRate"] / 100
    market_index = inputs["marketGrowthIndex"] 

    # Match dataset (stable version)
    base_revenue = initial_investment * 0.55
    revenue_base = base_revenue * market_index

    wc_previous = 0

    for year in range(1, 5):

        revenue = revenue_base * (1 + growth_rate) ** year

        # ADD SMALL NOISE (IMPORTANT)
        revenue *= np.random.uniform(0.95, 1.05)

        cost = revenue * cost_ratio
        cost *= np.random.uniform(0.95, 1.05)

        wc_current = revenue * wc_ratio
        delta_wc = wc_current - wc_previous

        # FIXED CAPEX
        capex = initial_investment * capex_ratio / year

        cashflow = revenue - cost - delta_wc - capex

        results.append({
            "year": year,
            "revenue": float(revenue),
            "cost": float(cost),
            "deltaWC": float(delta_wc),
            "capex": float(capex),
            "cashflow": float(cashflow)
        })

        wc_previous = wc_current

    return results