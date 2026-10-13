"""
Case-Based Reasoning (CBR) retrieval for the V2 Capital Budgeting DSS.

Purpose
-------
When a proposed project does not have enough project-specific historical
cash-flow data, this module finds completed projects that are similar to it.

The module does NOT predict cash flow.

Instead, it:

1. Loads the historical project database.
2. Represents each completed project using project-level characteristics.
3. Compares a new project against those completed projects.
4. Returns the most similar projects.
5. Preserves the complete year-by-year history of those projects.

Those comparable projects can later be used by the forecasting pipeline
to establish a cold-start forecasting context.

Important:
-----------
The historical dataset contains one row per project-year. Therefore,
similarity must be calculated at the PROJECT level, not by treating every
project-year row as an independent case.
"""

import os
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import pairwise_distances

from services.complexity_assessor import (
    build_reference_population,
    calculate_complexity
)


# ---------------------------------------------------------------------------
# 1. Locate the V2 historical project database
# ---------------------------------------------------------------------------
# This keeps the V2 implementation independent from the Research folder.
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw_dataset.csv"
)


# ---------------------------------------------------------------------------
# 2. Features used to describe project similarity
# ---------------------------------------------------------------------------
# These are characteristics of the project itself or its environment.
#
# "cash_flow" is deliberately NOT included here.
#
# Cash flow is what we ultimately want to forecast, so using it to determine
# similarity for a new project would introduce information that the new
# project does not actually have.
# ---------------------------------------------------------------------------

CATEGORICAL_FEATURES = [
    "project_type",
    "project_scale"
]

NUMERICAL_FEATURES = [
    "project_duration_years",
    "complexity_index",
    "initial_investment",
    "tax_rate",
    "risk_index"
]


# ---------------------------------------------------------------------------
# 3. Load the historical project database
# ---------------------------------------------------------------------------

def load_project_data():
    """
    Load the historical project-year dataset.

    Returns
    -------
    pandas.DataFrame
        Historical project-year records.
    """

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Historical project database not found at: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = (
        CATEGORICAL_FEATURES
        + NUMERICAL_FEATURES
        + [
            "project_id",
            "year",
            "inflation_rate",
            "market_growth_rate",
            "cash_flow"
        ]
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Historical dataset is missing columns: {missing_columns}"
        )

    return df


# ---------------------------------------------------------------------------
# 4. Create one project-level record
# ---------------------------------------------------------------------------

def create_project_level_data(df):
    """
    Convert the project-year dataset into one row per project.

    A project appears multiple times in the raw dataset because each row
    represents one year.

    For CBR similarity, we need one representation of the project itself.

    Returns
    -------
    pandas.DataFrame
        One row per project.
    """

    # -----------------------------------------------------------------------
    # Project characteristics such as project type, scale, duration,
    # complexity, investment, tax and risk should remain project-level
    # attributes.
    #
    # We take the first recorded value for these attributes because they
    # describe the project rather than a particular year.
    # -----------------------------------------------------------------------

    project_df = (
        df.sort_values(["project_id", "year"])
        .groupby("project_id", as_index=False)
        .first()
    )

    # -----------------------------------------------------------------------
    # Calculate the new deterministic complexity index.
    # -----------------------------------------------------------------------

    reference_population = build_reference_population()

    complexity_results = []

    for _, project in project_df.iterrows():

        complexity = calculate_complexity(
            {
                "project_scale": project["project_scale"],
                "project_duration_years": project[
                    "project_duration_years"
                ],
                "initial_investment": project[
                    "initial_investment"
                ]
            },
            reference_population
        )

        complexity_results.append(
            complexity["complexity_index"]
        )

    project_df["complexity_index"] = complexity_results

    return project_df



# ---------------------------------------------------------------------------
# 5. Build the similarity representation
# ---------------------------------------------------------------------------

def build_similarity_transformer(project_data):
    """
    Create preprocessing for project similarity.

    Categorical features are one-hot encoded.

    Numerical features are standardized so that variables with large
    numerical magnitudes, such as investment, do not dominate variables
    such as risk or complexity.

    Returns
    -------
    ColumnTransformer
        Fitted preprocessing transformer.
    """

    transformer = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                CATEGORICAL_FEATURES
            ),
            (
                "numerical",
                StandardScaler(),
                NUMERICAL_FEATURES
            )
        ]
    )

    transformer.fit(
        project_data[
            CATEGORICAL_FEATURES + NUMERICAL_FEATURES
        ]
    )

    return transformer


# ---------------------------------------------------------------------------
# 6. Find comparable projects
# ---------------------------------------------------------------------------

from services.complexity_assessor import (
    build_reference_population,
    calculate_complexity
)

# ---------------------------------------------------------------------------
# Calculate the proposed project's complexity using the same deterministic
# framework used for historical projects.
#
# The reference population comes from the historical project database.
# This ensures that duration and investment percentiles are calculated
# consistently for both historical and new projects.
# ---------------------------------------------------------------------------

# reference_population = build_reference_population()


def find_similar_projects(
    project,
    n_neighbors=5
):
    """
    Find the most similar completed projects.

    Parameters
    ----------
    project : dict
        Proposed project information.

    n_neighbors : int
        Number of comparable projects to return.

    Expected project fields
    -----------------------
    project_type
    project_scale
    project_duration
    complexity_index
    initial_investment
    tax_rate
    risk_index

    Returns
    -------
    list of dict
        Similar projects with similarity information and historical
        trajectories.
    """

    # -----------------------------------------------------------------------
    # Load and convert the historical project-year data into project-level
    # records for similarity matching.
    # -----------------------------------------------------------------------

    historical_data = load_project_data()

    project_level_data = create_project_level_data(
        historical_data
    )

    transformer = build_similarity_transformer(
        project_level_data
    )

    # -----------------------------------------------------------------------
    # Validate the proposed project's required fields.
    # -----------------------------------------------------------------------

    required_features = (
        CATEGORICAL_FEATURES
        + NUMERICAL_FEATURES
    )

    missing_features = [
        feature
        for feature in required_features
        if feature not in project
        or project[feature] is None
    ]

    if missing_features:
        raise ValueError(
            "Cannot perform CBR because the proposed project is "
            f"missing: {missing_features}"
        )

    # -----------------------------------------------------------------------
    # Convert the new project into the same feature representation used for
    # the historical projects.
    # -----------------------------------------------------------------------

    new_project_df = pd.DataFrame(
        [project],
        columns=required_features
    )

    historical_matrix = transformer.transform(
        project_level_data[required_features]
    )

    new_project_matrix = transformer.transform(
        new_project_df
    )

    # -----------------------------------------------------------------------
    # Calculate Euclidean distance between the new project and every
    # historical project.
    #
    # Smaller distance = more similar project.
    # -----------------------------------------------------------------------

    distances = pairwise_distances(
        new_project_matrix,
        historical_matrix,
        metric="euclidean"
    )[0]

    nearest_indices = np.argsort(distances)[
        :n_neighbors
    ]

    results = []

    # -----------------------------------------------------------------------
    # Retrieve the COMPLETE historical trajectory of each comparable
    # project, not just the single row used for similarity.
    # -----------------------------------------------------------------------

    for index in nearest_indices:

        project_id = project_level_data.iloc[
            index
        ]["project_id"]

        project_history = (
            historical_data[
                historical_data["project_id"] == project_id
            ]
            .sort_values("year")
            .copy()
        )

        distance = float(
            distances[index]
        )

        # Convert distance into a simple relative similarity score.
        #
        # This is NOT a probability.
        # It is only a convenient score where larger values indicate
        # greater similarity.
        similarity = 1 / (1 + distance)

        results.append({
            "project_id": project_id,
            "distance": distance,
            "similarity": float(similarity),
            "project_history": project_history.to_dict(
                orient="records"
            )
        })

    return results


# ---------------------------------------------------------------------------
# 7. Build a cold-start LSTM context from comparable projects
# ---------------------------------------------------------------------------

def build_lstm_context(
    new_project,
    similar_projects
):
    """
    Construct a 3-year historical context for the LSTM using comparable
    completed projects.

    This is used only when the proposed project does not have its own
    historical cash-flow data.

    The process is:

        Comparable project histories
                    ↓
        Normalize cash flow by investment
                    ↓
        Weight projects by similarity
                    ↓
        Combine the first 3 project years
                    ↓
        Scale normalized cash flow to the new project's investment
                    ↓
        Return LSTM-ready 3-year context

    Parameters
    ----------
    new_project : dict
        Proposed project information.

    similar_projects : list of dict
        Output returned by find_similar_projects().

    Returns
    -------
    list of list
        Three rows containing:

        [
            [cash_flow, inflation_rate, market_growth_rate],
            [cash_flow, inflation_rate, market_growth_rate],
            [cash_flow, inflation_rate, market_growth_rate]
        ]

    Notes
    -----
    The resulting cash flows are NOT the actual historical cash flows of
    the proposed project. They are a CBR-derived historical context based
    on comparable completed projects.
    """

    if not similar_projects:
        raise ValueError(
            "No comparable projects were found."
        )

    if "initial_investment" not in new_project:
        raise ValueError(
            "New project must contain initial_investment."
        )

    new_investment = new_project["initial_investment"]

    if new_investment is None or new_investment <= 0:
        raise ValueError(
            "New project's initial_investment must be positive."
        )

    # -----------------------------------------------------------------------
    # We need at least three years because our LSTM was trained using a
    # sequence length of three.
    # -----------------------------------------------------------------------

    required_years = 3

    # -----------------------------------------------------------------------
    # Calculate similarity weights.
    #
    # A smaller CBR distance means that a project is more similar.
    # Therefore, closer projects receive larger weights.
    #
    # We use inverse distance rather than treating the similarity value
    # from the retriever as a probability.
    # -----------------------------------------------------------------------

    distances = np.array([
        project["distance"]
        for project in similar_projects
    ], dtype=float)

    # Avoid division by zero if a proposed project happens to be identical
    # to a historical project in the feature space.
    inverse_distances = 1 / np.maximum(distances, 1e-10)

    weights = (
        inverse_distances
        / inverse_distances.sum()
    )

    # -----------------------------------------------------------------------
    # Store the weighted values for each of the first three years.
    # -----------------------------------------------------------------------

    context = []

    for year_index in range(required_years):

        weighted_normalized_cash_flow = 0.0
        weighted_inflation = 0.0
        weighted_market_growth = 0.0

        total_weight = 0.0

        for project, weight in zip(
            similar_projects,
            weights
        ):

            history = project["project_history"]

            # ---------------------------------------------------------------
            # Make sure this comparable project actually has the required
            # historical year.
            # ---------------------------------------------------------------

            if len(history) <= year_index:
                continue

            historical_year = history[year_index]

            historical_investment = historical_year[
                "initial_investment"
            ]

            historical_cash_flow = historical_year[
                "cash_flow"
            ]

            # ---------------------------------------------------------------
            # Normalize the comparable project's cash flow by its own
            # investment.
            #
            # Example:
            #
            # Project investment = ₹100M
            # Cash flow          = ₹10M
            #
            # Normalized CF = 0.10
            #
            # This allows projects of different monetary scales to be
            # compared.
            # ---------------------------------------------------------------

            if (
                historical_investment is None
                or historical_investment <= 0
            ):
                continue

            normalized_cash_flow = (
                historical_cash_flow
                / historical_investment
            )

            inflation = historical_year[
                "inflation_rate"
            ]

            market_growth = historical_year[
                "market_growth_rate"
            ]

            # ---------------------------------------------------------------
            # Accumulate similarity-weighted values.
            # ---------------------------------------------------------------

            weighted_normalized_cash_flow += (
                weight * normalized_cash_flow
            )

            weighted_inflation += (
                weight * inflation
            )

            weighted_market_growth += (
                weight * market_growth
            )

            total_weight += weight

        if total_weight == 0:
            raise ValueError(
                f"Could not construct LSTM context for year "
                f"{year_index + 1}."
            )

        # -------------------------------------------------------------------
        # Normalize the weighted values.
        # -------------------------------------------------------------------

        representative_normalized_cash_flow = (
            weighted_normalized_cash_flow
            / total_weight
        )

        representative_inflation = (
            weighted_inflation
            / total_weight
        )

        representative_market_growth = (
            weighted_market_growth
            / total_weight
        )

        # -------------------------------------------------------------------
        # Scale the representative normalized cash flow to the proposed
        # project's investment.
        #
        # This gives the LSTM a cash-flow magnitude appropriate to the
        # proposed project rather than the raw magnitude of a comparable
        # project.
        # -------------------------------------------------------------------

        representative_cash_flow = (
            representative_normalized_cash_flow
            * new_investment
        )

        context.append([
            float(representative_cash_flow),
            float(representative_inflation),
            float(representative_market_growth)
        ])

    return context