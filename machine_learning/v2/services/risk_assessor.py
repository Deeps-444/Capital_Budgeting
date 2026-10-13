"""
Risk Assessment Service
-----------------------

Calculates a deterministic project-level risk index from a structured
project risk register.

The service does NOT invent risks or probabilities.

Risk information must come from documented project information, explicit
user input, or another approved upstream source.

Each risk contains:

    category
    probability
    impact

Both probability and impact are normalized to [0, 1].

For each risk:

    risk_exposure = probability × impact

The project-level risk index is the mean exposure across the supplied
risks and therefore remains in the range [0, 1].

This risk index is used as a compact project-level feature for CBR.
The richer individual risk information can later be used by the BBN and
the DSS interface.
"""


# ---------------------------------------------------------------------------
# Validate a single risk item
# ---------------------------------------------------------------------------

def validate_risk(risk):
    """
    Validate the structure and values of one project risk.

    Parameters
    ----------
    risk : dict
        Expected fields:
            category
            probability
            impact

    Raises
    ------
    ValueError
        If required information is missing or outside [0, 1].
    """

    required_fields = [
        "category",
        "probability",
        "impact"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in risk or risk[field] is None
    ]

    if missing_fields:
        raise ValueError(
            f"Risk is missing required fields: {missing_fields}"
        )

    probability = float(risk["probability"])
    impact = float(risk["impact"])

    if not 0 <= probability <= 1:
        raise ValueError(
            "Risk probability must be between 0 and 1."
        )

    if not 0 <= impact <= 1:
        raise ValueError(
            "Risk impact must be between 0 and 1."
        )


# ---------------------------------------------------------------------------
# Calculate exposure for one risk
# ---------------------------------------------------------------------------

def calculate_risk_exposure(risk):
    """
    Calculate probability × impact for one risk.

    Returns
    -------
    float
        Risk exposure in [0, 1].
    """

    validate_risk(risk)

    probability = float(risk["probability"])
    impact = float(risk["impact"])

    return probability * impact


# ---------------------------------------------------------------------------
# Calculate project-level risk
# ---------------------------------------------------------------------------

def calculate_risk_index(risks):
    """
    Calculate a project-level risk index from a risk register.

    The project-level index is the mean exposure across all supplied risks.

    Parameters
    ----------
    risks : list of dict
        Structured project risks.

    Returns
    -------
    dict
        Contains the overall risk index and detailed risk exposures.

    Raises
    ------
    ValueError
        If no risks are supplied.
    """

    if not risks:
        raise ValueError(
            "At least one explicit project risk is required "
            "to calculate the risk index."
        )

    risk_results = []

    for risk in risks:
        exposure = calculate_risk_exposure(risk)

        risk_results.append({
            "category": risk["category"],
            "probability": float(risk["probability"]),
            "impact": float(risk["impact"]),
            "exposure": float(exposure)
        })

    risk_index = sum(
        risk["exposure"]
        for risk in risk_results
    ) / len(risk_results)

    return {
        "risk_index": float(risk_index),
        "risks": risk_results
    }