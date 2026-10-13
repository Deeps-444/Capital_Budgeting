
"""
BBN Explainability Service
--------------------------

Explains how observable project conditions are converted into
BBN evidence states and how those states lead to cash-flow
deviation probabilities.

This module reuses the existing BBN predictor. It does not
retrain the network or change its inference logic.
"""

from services.bbn_predictor import (
    _to_bbn_state,
    infer_cash_flow_state
)


def explain_bbn_prediction(
    complexity,
    inflation,
    market_growth
):
    """
    Explain a BBN prediction using the same discretization
    boundaries and inference function as the existing predictor.
    """

    # Step 1: Convert continuous inputs into the trained BBN states.
    evidence_states = {
        "complexity_state": _to_bbn_state(
            complexity,
            "complexity_index"
        ),
        "inflation_state": _to_bbn_state(
            inflation,
            "inflation_rate"
        ),
        "market_growth_state": _to_bbn_state(
            market_growth,
            "market_growth_rate"
        )
    }

    # Step 2: Obtain probabilities from the existing BBN.
    probabilities = infer_cash_flow_state(
        complexity=complexity,
        inflation=inflation,
        market_growth=market_growth
    )

    # Step 3: Sort outcomes by probability for readability.
    most_likely_state = max(
        probabilities,
        key=probabilities.get
    )

    # Step 4: Build a human-readable explanation.
    outcome_descriptions = {
        "Better": "Cash flow performs better than expected.",
        "Near Expected": "Cash flow remains near the expected level.",
        "Worse": "Cash flow performs worse than expected."
    }

    return {
        "method": "Bayesian Belief Network",
        "input_evidence": {
            "complexity": complexity,
            "inflation": inflation,
            "market_growth": market_growth
        },
        "discretized_evidence": evidence_states,
        "probabilities": probabilities,
        "most_likely_state": most_likely_state,
        "interpretation": outcome_descriptions.get(
            most_likely_state,
            "The BBN returned an unrecognized outcome state."
        ),
        "important_note": (
            "These probabilities describe cash-flow deviation "
            "states, not the probability that the project will "
            "be profitable or have a positive NPV."
        )
    }