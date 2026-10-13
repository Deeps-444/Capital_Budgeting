"""
Future Assumptions Service
==========================

Validates and standardizes annual assumptions consumed by the forecasting model.
Research evidence and percentage candidates are kept separate from approved
annual project assumptions: source percentages must never be silently treated
as project cash-flow assumptions.
"""
from typing import Any, Optional


def validate_future_assumptions(future_inflation, future_market_growth):
    """Validate equal-length numeric decimal-rate series."""
    if future_inflation is None:
        raise ValueError("Future inflation assumptions are required.")
    if future_market_growth is None:
        raise ValueError("Future market-growth assumptions are required.")
    if len(future_inflation) == 0:
        raise ValueError("Future inflation assumptions cannot be empty.")
    if len(future_market_growth) == 0:
        raise ValueError("Future market-growth assumptions cannot be empty.")
    if len(future_inflation) != len(future_market_growth):
        raise ValueError(
            "Future inflation and market-growth assumptions must have the same forecast horizon."
        )

    for name, series in (
        ("inflation", future_inflation),
        ("market-growth", future_market_growth),
    ):
        for value in series:
            # bool is a subclass of int in Python, but should not be accepted as a rate.
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"Future {name} assumptions must contain numeric values.")
            if value < -1:
                raise ValueError(f"Future {name} rate cannot be below -100%.")
    return True


def build_future_assumptions(
    future_inflation,
    future_market_growth,
    sources=None,
    status="provided",
):
    """
    Standardize approved annual assumptions.

    `status` records provenance (e.g. provided, accepted, edited). This
    function validates values but does not itself decide whether a human
    has approved the evidence used to choose them.
    """
    validate_future_assumptions(future_inflation, future_market_growth)
    return {
        "inflation": [float(v) for v in future_inflation],
        "market_growth": [float(v) for v in future_market_growth],
        "sources": sources or [],
        "status": status,
    }


def approve_future_assumptions(
    future_inflation,
    future_market_growth,
    sources=None,
    decision="accepted",
):
    """
    Build the annual series after the user has reviewed the evidence.

    `decision` must be `accepted` or `edited`. The actual annual values are
    supplied explicitly by the user; candidate percentages are not auto-mapped
    into annual values.
    """
    if decision not in {"accepted", "edited"}:
        raise ValueError("decision must be 'accepted' or 'edited'.")
    return build_future_assumptions(
        future_inflation=future_inflation,
        future_market_growth=future_market_growth,
        sources=sources,
        status=decision,
    )
