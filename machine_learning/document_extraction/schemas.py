from pydantic import BaseModel
from typing import Optional

class ProjectDetails(BaseModel):
    projectName: Optional[str] = None
    initialInvestment: Optional[float] = None
    revenueGrowthRate: Optional[float] = None
    inflationRate: Optional[float] = None
    discountRate: Optional[float] = None