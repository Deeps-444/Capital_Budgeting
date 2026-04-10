import numpy as np

def monte_carlo_simulation(cashflows, investment, discount_rate, simulations=3000):
    # helps to analyse investement risk under uncertainity
    cashflows = np.array(cashflows)
    results = []

    for _ in range(simulations):

        simulated_cf = []

        for cf in cashflows:
            
            variation = np.random.normal(0, 0.1) # -0.05, 0.4
            variation = np.clip(variation, -0.3, 0.3)

            
            adjusted_cf = cf * (1 + variation)
            simulated_cf.append(adjusted_cf)

        
        sim_discount = np.random.normal(discount_rate, 0.02)
        sim_discount = max(0.01, sim_discount)

        
        sim_investment = np.random.normal(investment, investment * 0.02)

        # NPV calculation
        npv = -sim_investment

        for t, cf in enumerate(simulated_cf):
            npv += cf / (1 + sim_discount) ** (t + 1)

        results.append(npv)

    results = np.array(results)

    # Metrics
    mean_npv = np.mean(results)
    std_npv = np.std(results)

    
    risk_probability = np.mean(results < 0)

    # Percentiles 
    p10 = np.percentile(results, 10)
    p50 = np.percentile(results, 50)
    p90 = np.percentile(results, 90)

    return {
        "meanNPV": float(mean_npv), # expected
        "stdNPV": float(std_npv), # valatility
        "riskProbability": float(risk_probability), # chance of  loss
        "percentiles": { # worst and best case 
            "p10": float(p10),
            "p50": float(p50),
            "p90": float(p90)
        }
    }