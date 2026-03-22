def calculate_cashflows(inputs, cost_ratio, wc_ratio, capex_ratio):
    """
    Calculate 5-year cashflows using financial logic
    """

    results = []

    initial_investment = inputs["initialInvestment"]
    growth_rate = inputs["revenueGrowthRate"]
    market_index = inputs["marketGrowthIndex"]

    # Step 1: Base revenue (same as dataset logic)
    base_revenue = initial_investment * 0.5
    revenue_base = base_revenue * market_index

    wc_previous = 0

    for year in range(1, 6):

        # Revenue growth
        revenue = revenue_base * (1 + growth_rate) ** year

        # Operating cost
        cost = revenue * cost_ratio

        # Working capital
        wc_current = revenue * wc_ratio
        delta_wc = wc_current - wc_previous

        # Capex
        capex = initial_investment * capex_ratio

        # Cashflow
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