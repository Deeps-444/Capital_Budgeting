"""
Project Complexity Assessment
-----------------------------

Purpose
-------
Calculate a deterministic Project Complexity Index (PCI) for both:

1. Historical projects in the V2 dataset.
2. New projects entering the Capital Budgeting DSS.

The same calculation framework is used for both cases so that the
complexity score is comparable during CBR retrieval.

Complexity is estimated from three observable project characteristics:

    - Project scale
    - Project duration
    - Initial investment

The score is normalized to the range [0, 1].

Important
---------
The original synthetic dataset contained a randomly generated
complexity_index. We deliberately do NOT use that value here because
it was not derived from observable project characteristics.

Instead, this module creates a reproducible complexity measure that
can also be calculated for a completely new project.
"""

import os

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Locate the historical V2 project dataset
# ---------------------------------------------------------------------------
# The historical dataset provides the reference population against which
# duration and investment of new projects are normalized.
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw_dataset.csv"
)


# ---------------------------------------------------------------------------
# 2. Complexity component weights
# ---------------------------------------------------------------------------
# Scale is given the largest contribution because it is the most direct
# categorical representation of project magnitude.
#
# Duration and investment contribute equally.
#
# The weights are explicit design assumptions rather than parameters
# learned from the synthetic complexity_index.
# ---------------------------------------------------------------------------

SCALE_WEIGHT = 0.40
DURATION_WEIGHT = 0.30
INVESTMENT_WEIGHT = 0.30


# ---------------------------------------------------------------------------
# 3. Scale mapping
# ---------------------------------------------------------------------------
# Convert the categorical project scale into an ordinal numerical score.
#
# This does NOT claim that "Large" projects are intrinsically complex.
# It represents increasing project magnitude as one component of the
# overall complexity assessment.
# ---------------------------------------------------------------------------

SCALE_SCORES = {
    "Small": 0.0,
    "Medium": 0.5,
    "Large": 1.0
}


# ---------------------------------------------------------------------------
# 4. Load historical project data
# ---------------------------------------------------------------------------

def load_project_data():
    """
    Load the V2 historical project-year dataset.

    Returns
    -------
    pandas.DataFrame
        Historical project-year records.
    """

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Historical dataset not found at: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "project_id",
        "year",
        "project_scale",
        "project_duration_years",
        "initial_investment"
    ]

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
# 5. Create one record per project
# ---------------------------------------------------------------------------
# The raw dataset contains one row per project-year.
#
# Complexity is a project-level characteristic, so we first reduce the
# dataset to one row per project.
# ---------------------------------------------------------------------------

def create_project_level_data(df):
    """
    Convert project-year data into one row per project.

    Returns
    -------
    pandas.DataFrame
        One row per project.
    """

    project_df = (
        df.sort_values(["project_id", "year"])
        .groupby("project_id", as_index=False)
        .first()
    )

    return project_df


# ---------------------------------------------------------------------------
# 6. Calculate percentile scores
# ---------------------------------------------------------------------------
# Percentile normalization is used instead of min-max normalization.
#
# Example:
#
# If a project's investment is greater than approximately 80% of the
# historical projects, its investment percentile will be approximately 0.80.
#
# This makes the score robust to the very large investment range observed
# in the historical dataset.
# ---------------------------------------------------------------------------

def percentile_score(value, reference_values):
    """
    Calculate the percentile position of a value within a reference
    population.

    Parameters
    ----------
    value : float
        Value whose percentile is required.

    reference_values : array-like
        Historical reference values.

    Returns
    -------
    float
        Percentile score in [0, 1].
    """

    reference_values = np.asarray(reference_values, dtype=float)

    reference_values = reference_values[
        np.isfinite(reference_values)
    ]

    if len(reference_values) == 0:
        raise ValueError(
            "Reference population contains no valid numerical values."
        )

    # Fraction of historical observations less than or equal to the
    # proposed value.
    percentile = np.mean(reference_values <= value)

    return float(np.clip(percentile, 0.0, 1.0))


# ---------------------------------------------------------------------------
# 7. Build the historical reference population
# ---------------------------------------------------------------------------
# These reference values are learned ONCE from the historical dataset.
#
# The same reference population must be reused when assessing new projects.
# Otherwise, the meaning of a complexity score would change between
# different project evaluations.
# ---------------------------------------------------------------------------

def build_reference_population():
    """
    Build the historical reference population required for complexity
    normalization.

    Returns
    -------
    dict
        Reference duration and investment values.
    """

    df = load_project_data()
    project_df = create_project_level_data(df)

    return {
        "duration_values": project_df[
            "project_duration_years"
        ].dropna().to_numpy(),

        "investment_values": project_df[
            "initial_investment"
        ].dropna().to_numpy()
    }


# ---------------------------------------------------------------------------
# 8. Calculate complexity for one project
# ---------------------------------------------------------------------------

def calculate_complexity(
    project,
    reference_population=None
):
    """
    Calculate the Project Complexity Index for a project.

    Parameters
    ----------
    project : dict
        Project information containing:

            project_scale
            project_duration_years
            initial_investment

    reference_population : dict, optional
        Historical normalization reference.
        If omitted, it is loaded from the V2 historical dataset.

    Returns
    -------
    dict
        Individual component scores and final complexity index.
    """

    if reference_population is None:
        reference_population = build_reference_population()

    # -----------------------------------------------------------------------
    # Validate required project information.
    # -----------------------------------------------------------------------

    required_fields = [
        "project_scale",
        "project_duration_years",
        "initial_investment"
    ]

    missing_fields = [
        field
        for field in required_fields
        if project.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            f"Missing project information required for complexity "
            f"assessment: {missing_fields}"
        )

    # -----------------------------------------------------------------------
    # Scale component
    # -----------------------------------------------------------------------

    project_scale = str(
        project["project_scale"]
    ).strip().title()

    if project_scale not in SCALE_SCORES:
        raise ValueError(
            f"Unknown project_scale '{project_scale}'. "
            f"Expected one of: {list(SCALE_SCORES.keys())}"
        )

    scale_score = SCALE_SCORES[project_scale]

    # -----------------------------------------------------------------------
    # Duration component
    # -----------------------------------------------------------------------

    duration = float(
        project["project_duration_years"]
    )

    if duration <= 0:
        raise ValueError(
            "project_duration_years must be greater than zero."
        )

    duration_score = percentile_score(
        duration,
        reference_population["duration_values"]
    )

    # -----------------------------------------------------------------------
    # Investment component
    # -----------------------------------------------------------------------

    investment = float(
        project["initial_investment"]
    )

    if investment <= 0:
        raise ValueError(
            "initial_investment must be greater than zero."
        )

    investment_score = percentile_score(
        investment,
        reference_population["investment_values"]
    )

    # -----------------------------------------------------------------------
    # Combine the three components.
    #
    # The result remains within [0, 1] because every component is already
    # normalized to [0, 1] and the weights sum to 1.
    # -----------------------------------------------------------------------

    complexity_index = (
        SCALE_WEIGHT * scale_score
        + DURATION_WEIGHT * duration_score
        + INVESTMENT_WEIGHT * investment_score
    )

    return {
        "complexity_index": float(complexity_index),
        "scale_score": float(scale_score),
        "duration_score": float(duration_score),
        "investment_score": float(investment_score)
    }


# ---------------------------------------------------------------------------
# 9. Calculate complexity for every historical project
# ---------------------------------------------------------------------------
# This function allows us to replace the old synthetic complexity_index
# with the new deterministic index throughout the historical project
# population.
# ---------------------------------------------------------------------------

def calculate_historical_complexity():
    """
    Calculate the new complexity index for every historical project.

    Returns
    -------
    pandas.DataFrame
        Project-level data containing the newly calculated complexity index.
    """

    df = load_project_data()
    project_df = create_project_level_data(df)

    reference_population = {
        "duration_values": project_df[
            "project_duration_years"
        ].dropna().to_numpy(),

        "investment_values": project_df[
            "initial_investment"
        ].dropna().to_numpy()
    }

    results = []

    for _, project in project_df.iterrows():

        project_input = {
            "project_scale": project["project_scale"],
            "project_duration_years": project[
                "project_duration_years"
            ],
            "initial_investment": project[
                "initial_investment"
            ]
        }

        result = calculate_complexity(
            project_input,
            reference_population
        )

        results.append({
            "project_id": project["project_id"],
            **result
        })

    return pd.DataFrame(results)