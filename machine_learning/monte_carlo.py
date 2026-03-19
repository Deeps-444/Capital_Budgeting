import numpy as np

def monte_carlo_simulation(cashflows, investment, discount_rate, simulations=5000):
    cashflows = np.array(cashflows)
    results = []

    for i in range(simulations):

        # add random noise to cashflows
        noise = np.random.normal(0, 0.1, len(cashflows))
        simulated_cf = cashflows * (1 + noise)

        #initialize
        npv = -investment

        for t, cf in enumerate(simulated_cf):
            npv += cf / (1 + discount_rate) ** (t + 1)

        results.append(npv)

    results = np.array(results)

    mean_npv = np.mean(results)

    risk_probability = np.mean(results < 0)

    return {
    "predictedCashflows": cashflows.tolist(),
    "npvDistribution": results.tolist(),   
    "meanNPV": float(mean_npv),
    "riskProbability": float(risk_probability)
}