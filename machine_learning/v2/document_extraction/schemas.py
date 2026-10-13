"""
Structured schema for project information extracted from documents.

The extractor only captures information explicitly stated in the
document. Missing information remains None.
"""

from typing import Optional

from pydantic import BaseModel


class ProjectDetails(BaseModel):
    """
    Project information extracted from an uploaded document.

    These values represent documented project facts/assumptions.
    They are not model predictions.
    """

    project_name: Optional[str] = None
    project_type: Optional[str] = None
    project_scale: Optional[str] = None
    location: Optional[str] = None

    project_duration_years: Optional[int] = None
    initial_investment: Optional[float] = None

    annual_revenue: Optional[float] = None
    annual_operating_cost: Optional[float] = None

    tax_rate: Optional[float] = None
    discount_rate: Optional[float] = None