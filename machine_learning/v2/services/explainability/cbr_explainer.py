
"""
CBR explainability for the Capital Budgeting DSS.

Explains which historical projects were retrieved, how their
distances and relative weights were calculated, and how their
histories were combined into the LSTM's three-year context.

This module explains the existing CBR process. It does not
change retrieval, forecasting, or model training.
"""

import numpy as np

from services.cbr_retriever import (
    find_similar_projects,
    build_lstm_context
)


def explain_cbr_retrieval(new_project, n_neighbors=5):
    """
    Retrieve comparable projects and return an explanation
    of how they contribute to the LSTM's historical context.

    Parameters
    ----------
    new_project : dict
        Proposed project with the fields required by the CBR retriever.

    n_neighbors : int
        Number of comparable historical projects to retrieve.

    Returns
    -------
    dict
        Comparable projects, their similarity information,
        their context weights, and the constructed LSTM context.
    """

    # ------------------------------------------------------------
    # 1. Retrieve comparable historical projects using existing CBR.
    # ------------------------------------------------------------

    similar_projects = find_similar_projects(
        new_project,
        n_neighbors=n_neighbors
    )

    if not similar_projects:
        raise ValueError("No comparable projects were found.")

    # ------------------------------------------------------------
    # 2. Calculate the same inverse-distance weights used by
    #    build_lstm_context().
    #
    #    These weights describe relative contribution to the
    #    combined context; they are NOT probabilities.
    # ------------------------------------------------------------

    distances = np.array(
        [project["distance"] for project in similar_projects],
        dtype=float
    )

    inverse_distances = 1 / np.maximum(distances, 1e-10)

    weights = inverse_distances / inverse_distances.sum()

    # ------------------------------------------------------------
    # 3. Explain each retrieved project.
    # ------------------------------------------------------------

    comparable_explanations = []

    for project, weight in zip(similar_projects, weights):

        history = project["project_history"]
        characteristics = history[0] if history else {}

        comparable_explanations.append({
            "project_id": str(project["project_id"]),

            # Smaller distance means closer in the transformed
            # project-feature space.
            "distance": float(project["distance"]),

            # This is the retriever's relative similarity score,
            # not a probability.
            "similarity_score": float(project["similarity"]),

            # This is the normalized inverse-distance weight used
            # to combine historical information.
            "context_weight_percent": round(
                float(weight * 100), 2
            ),

            "matched_characteristics": {
                "project_type": characteristics.get("project_type"),
                "project_scale": characteristics.get("project_scale"),
                "project_duration_years": characteristics.get(
                    "project_duration_years"
                ),
                "initial_investment": characteristics.get(
                    "initial_investment"
                ),
                "tax_rate": characteristics.get("tax_rate"),
                "risk_index": characteristics.get("risk_index")
            },

            # Preserve the actual historical observations so the
            # user can inspect the evidence behind the comparison.
            "historical_cash_flows": [
                {
                    "year": int(row["year"]),
                    "cash_flow": float(row["cash_flow"]),
                    "inflation_rate": float(row["inflation_rate"]),
                    "market_growth_rate": float(
                        row["market_growth_rate"]
                    )
                }
                for row in history
            ]
        })

    # ------------------------------------------------------------
    # 4. Construct the exact three-year context using the existing
    #    function that supplies the LSTM.
    # ------------------------------------------------------------

    context = build_lstm_context(
        new_project,
        similar_projects
    )

    explained_context = [
        {
            "year": index + 1,
            "cash_flow": float(values[0]),
            "inflation_rate": float(values[1]),
            "market_growth_rate": float(values[2])
        }
        for index, values in enumerate(context)
    ]

    # ------------------------------------------------------------
    # 5. Return structured explanations for the API or UI.
    # ------------------------------------------------------------

    return {
        "method": "Case-Based Reasoning (CBR)",

        "summary": (
            f"Retrieved {len(similar_projects)} comparable "
            "historical projects using project characteristics. "
            "Their histories were combined using inverse-distance "
            "weights to construct the LSTM's three-year context."
        ),

        "matching_features": [
            "project_type",
            "project_scale",
            "project_duration_years",
            "complexity_index",
            "initial_investment",
            "tax_rate",
            "risk_index"
        ],

        "weighting_method": (
            "Normalized inverse Euclidean distance. "
            "Closer projects receive larger context weights."
        ),

        "comparables": comparable_explanations,
        "constructed_lstm_context": explained_context,

        "limitations": [
            "Similarity scores are not probabilities.",
            "The constructed history is an estimate based on "
            "comparable projects, not actual history of the new project.",
            "Similarity indicates closeness in the selected feature "
            "space; it does not guarantee similar future performance."
        ]
    }