import numpy as np

def monte_carlo_simulation(cashflows, investment, discount_rate, simulations=3000):
    
    cashflows = np.array(cashflows)
    results = []

    for _ in range(simulations):

        simulated_cf = []

        for cf in cashflows:
            # 🔥 Stronger variation for mix of outcomes
            variation = np.random.normal(0, 0.35)

            # Prevent unrealistic negative cashflows
            adjusted_cf = max(cf * (1 + variation), 0)
            simulated_cf.append(adjusted_cf)

        # 🔥 Add variation in discount rate
        sim_discount = np.random.normal(discount_rate, 0.03)

        # 🔥 Slight variation in investment
        sim_investment = np.random.normal(investment, investment * 0.05)

        # NPV calculation
        npv = -sim_investment

        for t, cf in enumerate(simulated_cf):
            npv += cf / (1 + sim_discount) ** (t + 1)

        results.append(npv)

    results = np.array(results)

    # Metrics
    mean_npv = np.mean(results)
    std_npv = np.std(results)

    # 🔥 This will now be fractional (NOT 0 or 1)
    risk_probability = np.mean(results < 0)

    # Percentiles 
    p10 = np.percentile(results, 10)
    p50 = np.percentile(results, 50)
    p90 = np.percentile(results, 90)

    return {
        "meanNPV": float(mean_npv),
        "stdNPV": float(std_npv),
        "riskProbability": float(risk_probability),
        "percentiles": {
            "p10": float(p10),
            "p50": float(p50),
            "p90": float(p90)
        }
    }