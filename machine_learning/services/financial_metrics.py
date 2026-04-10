import numpy as np

def calculate_npv(cashflows, initial_investment, discount_rate):
    """
    NPV calculation
    """
    discount_rate = max(0.01, discount_rate)
    npv = -initial_investment

    for t, cf in enumerate(cashflows, start=1):
        npv += cf / ((1 + discount_rate) ** t)

    return float(npv)

import numpy_financial as npf

def calculate_irr(cashflows, initial_investment):
    try:
        full_cashflows = [-initial_investment] + cashflows
        irr = npf.irr(full_cashflows)

        if irr is None or np.isnan(irr) or np.isinf(irr):
            return 0.0

        return float(irr)
    except Exception as e:
        print("IRR Error:", e)
        return 0.0