import numpy as np
import pandas as pd
from pathlib import Path


# ============================================================
# 1. SETTINGS
# ============================================================

SEED = 42
N_PROJECTS = 500

rng = np.random.default_rng(SEED)

PROJECT_TYPES = [
    "Manufacturing",
    "Energy",
    "Infrastructure",
    "Technology",
    "Healthcare",
    "Real Estate"
]

PROJECT_SCALES = ["Small", "Medium", "Large"]

SCALE_PROBABILITIES = [0.35, 0.45, 0.20]


# ============================================================
# 2. PROJECT-LEVEL PARAMETERS
# ============================================================

# Typical initial investment ranges by project type (₹)
INVESTMENT_RANGES = {
    "Manufacturing": (15_000_000, 100_000_000),
    "Energy": (30_000_000, 250_000_000),
    "Infrastructure": (50_000_000, 300_000_000),
    "Technology": (5_000_000, 60_000_000),
    "Healthcare": (10_000_000, 120_000_000),
    "Real Estate": (20_000_000, 200_000_000)
}

# Revenue multiplier relative to initial investment
# Used only as a realistic starting point for generating projects.
REVENUE_MULTIPLIERS = {
    "Manufacturing": (0.35, 0.70),
    "Energy": (0.25, 0.55),
    "Infrastructure": (0.20, 0.45),
    "Technology": (0.40, 0.90),
    "Healthcare": (0.30, 0.65),
    "Real Estate": (0.25, 0.60)
}

# Typical operating cost as percentage of revenue
OPERATING_COST_RANGES = {
    "Manufacturing": (0.55, 0.75),
    "Energy": (0.40, 0.65),
    "Infrastructure": (0.45, 0.70),
    "Technology": (0.35, 0.60),
    "Healthcare": (0.50, 0.70),
    "Real Estate": (0.40, 0.65)
}


# ============================================================
# 3. GENERATE PROJECTS
# ============================================================

projects = []

for i in range(1, N_PROJECTS + 1):

    project_id = f"P{i:04d}"

    project_type = rng.choice(PROJECT_TYPES)

    project_scale = rng.choice(
        PROJECT_SCALES,
        p=SCALE_PROBABILITIES
    )

    # Project duration
    project_duration_years = int(
        rng.integers(3, 11)
    )

    # Complexity
    complexity_index = np.clip(
        rng.normal(0.55, 0.18),
        0.10,
        0.95
    )

    # Risk
    risk_index = np.clip(
        rng.normal(0.50, 0.18),
        0.10,
        0.90
    )

    # Tax rate
    tax_rate = np.clip(
        rng.normal(0.25, 0.04),
        0.15,
        0.35
    )

    # Initial investment
    low, high = INVESTMENT_RANGES[project_type]

    initial_investment = rng.uniform(low, high)

    # Adjust investment according to scale
    if project_scale == "Small":
        initial_investment *= rng.uniform(0.65, 0.85)

    elif project_scale == "Large":
        initial_investment *= rng.uniform(1.15, 1.40)

    initial_investment = round(initial_investment, 2)

    projects.append({
        "project_id": project_id,
        "project_type": project_type,
        "project_scale": project_scale,
        "project_duration_years": project_duration_years,
        "complexity_index": round(complexity_index, 3),
        "initial_investment": initial_investment,
        "tax_rate": round(tax_rate, 3),
        "risk_index": round(risk_index, 3)
    })


projects_df = pd.DataFrame(projects)


# ============================================================
# 4. GENERATE PROJECT-YEAR OBSERVATIONS
# ============================================================

rows = []


for _, project in projects_df.iterrows():

    project_id = project["project_id"]
    project_type = project["project_type"]
    project_scale = project["project_scale"]

    duration = int(project["project_duration_years"])

    complexity = project["complexity_index"]
    risk = project["risk_index"]

    initial_investment = project["initial_investment"]
    tax_rate = project["tax_rate"]

    # --------------------------------------------------------
    # Project-specific characteristics
    # --------------------------------------------------------

    # Projects have their own underlying demand strength.
    demand_factor = rng.normal(1.0, 0.08)

    # Project-specific cost efficiency.
    efficiency_factor = rng.normal(1.0, 0.06)

    # Projects have their own growth potential.
    growth_factor = rng.normal(1.0, 0.08)

    # Revenue multiplier
    rev_low, rev_high = REVENUE_MULTIPLIERS[project_type]

    revenue_multiplier = rng.uniform(
        rev_low,
        rev_high
    )

    base_revenue = (
        initial_investment
        * revenue_multiplier
        * demand_factor
    )

    # Operating cost ratio
    cost_low, cost_high = OPERATING_COST_RANGES[project_type]

    base_cost_ratio = rng.uniform(
        cost_low,
        cost_high
    )

    # Initial working capital requirement
    working_capital_ratio = rng.uniform(
        0.04,
        0.12
    )

    previous_working_capital = 0

    # --------------------------------------------------------
    # Year-by-year generation
    # --------------------------------------------------------

    for year in range(1, duration + 1):

        # ====================================================
        # ECONOMIC CONDITIONS
        # ====================================================

        inflation_rate = np.clip(
            rng.normal(0.055, 0.018),
            0.015,
            0.12
        )

        market_growth_rate = np.clip(
            rng.normal(
                0.055 * growth_factor,
                0.035
            ),
            -0.08,
            0.15
        )

        # ====================================================
        # PROJECT RAMP-UP
        # ====================================================

        # Projects generally take time to reach full operation.
        if year == 1:
            ramp_factor = rng.uniform(0.45, 0.70)

        elif year == 2:
            ramp_factor = rng.uniform(0.70, 0.90)

        else:
            ramp_factor = rng.uniform(0.90, 1.05)

        # Some projects experience gradual maturity.
        maturity_factor = (
            1
            + min(year - 1, 5) * rng.uniform(0.01, 0.04)
        )

        # ====================================================
        # REVENUE
        # ====================================================

        revenue = (
            base_revenue
            * ramp_factor
            * maturity_factor
            * (1 + market_growth_rate)
            * (1 + inflation_rate * 0.35)
            * rng.normal(1.0, 0.07)
        )

        # Higher complexity can reduce operational efficiency.
        complexity_effect = 1 + (complexity - 0.5) * 0.10

        revenue *= (
            demand_factor
            * (1 / complexity_effect)
        )

        revenue = max(revenue, 0)

        # ====================================================
        # OPERATING COST
        # ====================================================

        # Inflation increases operating costs.
        cost_ratio = (
            base_cost_ratio
            * efficiency_factor
            * (1 + inflation_rate * 0.65)
        )

        # Higher complexity and risk can increase costs.
        cost_ratio *= (
            1
            + complexity * 0.08
            + risk * 0.05
        )

        operating_cost = (
            revenue
            * cost_ratio
            * rng.normal(1.0, 0.05)
        )

        operating_cost = max(
            operating_cost,
            0
        )

        # ====================================================
        # CAPEX
        # ====================================================

        if year == 1:

            # Initial setup/equipment spending.
            capex = (
                initial_investment
                * rng.uniform(0.05, 0.15)
            )

        elif year < duration:

            # Maintenance / expansion capex.
            capex = (
                initial_investment
                * rng.uniform(0.01, 0.05)
            )

            # Complex projects tend to require more reinvestment.
            capex *= (
                1 + complexity * 0.30
            )

        else:

            # Smaller final-year capital expenditure.
            capex = (
                initial_investment
                * rng.uniform(0.005, 0.025)
            )

        capex *= rng.normal(1.0, 0.10)

        capex = max(capex, 0)

        # ====================================================
        # WORKING CAPITAL
        # ====================================================

        # Working capital requirement is related to revenue.
        target_working_capital = (
            revenue
            * working_capital_ratio
            * (1 + risk * 0.15)
        )

        # Actual working capital can fluctuate.
        target_working_capital *= rng.normal(
            1.0,
            0.06
        )

        target_working_capital = max(
            target_working_capital,
            0
        )

        # The raw dataset stores the amount tied up,
        # not the yearly change.
        working_capital = target_working_capital

        change_in_working_capital = (
            working_capital
            - previous_working_capital
        )

        previous_working_capital = working_capital

        # ====================================================
        # CASH FLOW
        # ====================================================

        # Operating profit before tax
        operating_profit = (
            revenue
            - operating_cost
        )

        # Tax is paid only when there is positive operating profit.
        tax = (
            max(operating_profit, 0)
            * tax_rate
        )

        # Cash flow from operations after tax,
        # less capital expenditure and change in working capital.
        cash_flow = (
            operating_profit
            - tax
            - capex
            - change_in_working_capital
        )

        # Small unobserved factors/noise.
        cash_flow *= rng.normal(
            1.0,
            0.035
        )

        rows.append({
            "project_id": project_id,
            "project_type": project_type,
            "project_scale": project_scale,
            "project_duration_years": duration,
            "complexity_index": complexity,
            "initial_investment": initial_investment,
            "tax_rate": tax_rate,
            "risk_index": risk,
            "year": year,
            "inflation_rate": inflation_rate,
            "market_growth_rate": market_growth_rate,
            "revenue": revenue,
            "operating_cost": operating_cost,
            "capex": capex,
            "working_capital": working_capital,
            "cash_flow": cash_flow
        })


# ============================================================
# 5. CREATE FINAL DATASET
# ============================================================

df = pd.DataFrame(rows)


# ============================================================
# 6. ROUND NUMERIC VALUES
# ============================================================

numeric_columns = [
    "complexity_index",
    "initial_investment",
    "tax_rate",
    "risk_index",
    "inflation_rate",
    "market_growth_rate",
    "revenue",
    "operating_cost",
    "capex",
    "working_capital",
    "cash_flow"
]

df[numeric_columns] = df[numeric_columns].round(2)


# ============================================================
# 7. SORT DATA
# ============================================================

df = df.sort_values(
    ["project_id", "year"]
).reset_index(drop=True)


# ============================================================
# 8. VALIDATION / SANITY CHECKS
# ============================================================

print("\n" + "=" * 60)
print("DATASET GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"\nNumber of projects: {df['project_id'].nunique():,}")
print(f"Number of project-year rows: {len(df):,}")

print("\nProject duration distribution:")
print(
    df.groupby("project_id")["year"]
    .max()
    .value_counts()
    .sort_index()
)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate project-year records:")
print(
    df.duplicated(
        subset=["project_id", "year"]
    ).sum()
)

print("\nProject type distribution:")
print(df["project_type"].value_counts())

print("\nProject scale distribution:")
print(df["project_scale"].value_counts())

print("\nCash-flow statistics:")
print(df["cash_flow"].describe())

print("\nFirst 10 rows:")
print(df.head(10).to_string(index=False))


# ============================================================
# 9. SAVE DATASET
# ============================================================

output_path = Path(__file__).resolve().parent / "raw_dataset.csv"

df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 60)
print(f"Dataset saved to:")
print(output_path)
print("=" * 60)