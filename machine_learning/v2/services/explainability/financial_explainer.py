
"""
Financial Explainability Service
--------------------------------

Interprets existing Monte Carlo simulation results for the
Capital Budgeting Decision Support System.

Explains expected NPV, downside risk, uncertainty, and
percentile outcomes without rerunning simulations or
retraining any model.
"""


def explain_financial_results(
    simulation_results,
    initial_investment,
    discount_rate,
    forecast_years
):
    """
    Generate a human-readable explanation of Monte Carlo results.

    Parameters
    ----------
    simulation_results : dict
        Output returned by run_monte_carlo().

    initial_investment : float
        Initial project investment.

    discount_rate : float
        Discount rate used in the NPV calculation.

    forecast_years : int
        Number of years covered by the cash-flow forecast.
    """

    # STEP 1: Extract metrics using the actual Monte Carlo output keys.
    mean_npv = simulation_results["mean_npv"]
    median_npv = simulation_results["median_npv"]
    std_npv = simulation_results["std_npv"]

    loss_probability = simulation_results[
        "probability_npv_negative"
    ]

    percentiles = simulation_results["percentiles"]

    p10 = percentiles["p10"]
    p25 = percentiles["p25"]
    p75 = percentiles["p75"]
    p90 = percentiles["p90"]

    # STEP 2: Explain the expected financial outcome.
    if mean_npv > 0:
        expected_npv_explanation = (
            "The average simulated NPV is positive. Under the "
            "current assumptions, discounted cash inflows "
            "exceed the initial investment on average."
        )
    elif mean_npv < 0:
        expected_npv_explanation = (
            "The average simulated NPV is negative. Under the "
            "current assumptions, discounted future cash flows "
            "do not recover the initial investment on average."
        )
    else:
        expected_npv_explanation = (
            "The average simulated NPV is zero, indicating "
            "break-even in expected net present value."
        )

    # STEP 3: Explain the probability of negative NPV.
    loss_percentage = loss_probability * 100

    loss_explanation = (
        f"{loss_percentage:.2f}% of simulated outcomes have "
        "negative NPV. This estimates the downside risk under "
        "the current forecast, discount rate, and simulation model."
    )

    # STEP 4: Explain the spread of financial outcomes.
    uncertainty_explanation = (
        f"The NPV standard deviation is {std_npv:,.2f}. "
        "It measures the spread of simulated NPVs around "
        "their mean; a larger value indicates greater "
        "variation in the simulated outcomes."
    )

    # STEP 5: Explain percentile results.
    percentile_explanation = (
        f"P10 = {p10:,.2f}: approximately 10% of outcomes "
        "are at or below this NPV. "
        f"P25 = {p25:,.2f}: approximately 25% are at or "
        "below this NPV. "
        f"P75 = {p75:,.2f}: approximately 75% are at or "
        "below this NPV. "
        f"P90 = {p90:,.2f}: approximately 90% are at or "
        "below this NPV."
    )

    # STEP 6: Return structured explanations for the UI/API.
    return {
        "method": "Monte Carlo Financial Explainability",

        "investment_context": {
            "initial_investment": initial_investment,
            "discount_rate": discount_rate,
            "forecast_years": forecast_years
        },

        "financial_metrics": {
            "simulations": simulation_results["simulations"],
            "mean_npv": mean_npv,
            "median_npv": median_npv,
            "std_npv": std_npv,
            "probability_npv_negative": loss_probability,
            "percentiles": percentiles
        },

        "interpretations": {
            "expected_npv": expected_npv_explanation,
            "downside_risk": loss_explanation,
            "uncertainty": uncertainty_explanation,
            "percentiles": percentile_explanation
        },

        "important_note": (
            f"These results cover only the specified "
            f"{forecast_years}-year forecast horizon. They depend "
            "on the baseline cash-flow forecasts, BBN probabilities, "
            "historical deviation distributions, and discount rate. "
            "They are estimates, not guarantees of actual performance."
        )
    }

