package com.finance.cbds.dto;

public class ProjectInputDto {
	private Long userId;
	 private String projectName;

	 private Double initialInvestment;
	 private Double revenueGrowthRate;
	 private Double operatingCostRatio;
	 private Double workingCapitalRatio;
	 private Double capexRatio;
	 private Double inflationRate;
	 private Double debtRatio;
	 private Double marketGrowthIndex;
	 private Double sectorRiskIndex;
	 private Double discountRate;
	    
	    public void setWorkingCapitalRatio(Double workingCapitalRatio) {
			this.workingCapitalRatio = workingCapitalRatio;
		}

		public void setCapexRatio(Double capexRatio) {
			this.capexRatio = capexRatio;
		}

		public Double getWorkingCapitalRatio() {
			return workingCapitalRatio;
		}

		public Double getCapexRatio() {
			return capexRatio;
		}

		

	    public Long getUserId() {
			return userId;
		}

		public void setUserId(Long userId) {
			this.userId = userId;
		}

		public String getProjectName() {
	        return projectName;
	    }

	    public void setProjectName(String projectName) {
	        this.projectName = projectName;
	    }

	    public Double getInitialInvestment() {
	        return initialInvestment;
	    }

	    public void setInitialInvestment(Double initialInvestment) {
	        this.initialInvestment = initialInvestment;
	    }

	    public Double getRevenueGrowthRate() {
	        return revenueGrowthRate;
	    }

	    public void setRevenueGrowthRate(Double revenueGrowthRate) {
	        this.revenueGrowthRate = revenueGrowthRate;
	    }

	    public Double getOperatingCostRatio() {
	        return operatingCostRatio;
	    }

	    public void setOperatingCostRatio(Double operatingCostRatio) {
	        this.operatingCostRatio = operatingCostRatio;
	    }

	    public Double getInflationRate() {
	        return inflationRate;
	    }

	    public void setInflationRate(Double inflationRate) {
	        this.inflationRate = inflationRate;
	    }

	    public Double getDebtRatio() {
	        return debtRatio;
	    }

	    public void setDebtRatio(Double debtRatio) {
	        this.debtRatio = debtRatio;
	    }

	    public Double getMarketGrowthIndex() {
	        return marketGrowthIndex;
	    }

	    public void setMarketGrowthIndex(Double marketGrowthIndex) {
	        this.marketGrowthIndex = marketGrowthIndex;
	    }

	    public Double getSectorRiskIndex() {
	        return sectorRiskIndex;
	    }

	    public void setSectorRiskIndex(Double sectorRiskIndex) {
	        this.sectorRiskIndex = sectorRiskIndex;
	    }

	    public Double getDiscountRate() {
	        return discountRate;
	    }

	    public void setDiscountRate(Double discountRate) {
	        this.discountRate = discountRate;
	    }
}
