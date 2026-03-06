package com.finance.cbds.dto;

public class ProjectResultDto {
	private String projectName;

    private Double initialInvestment;
    private Double revenueGrowthRate;
    private Double operatingCostRatio;
    private Double inflationRate;
    private Double debtRatio;
    private Double marketGrowthIndex;
    private Double sectorRiskIndex;
    private Double discountRate;
	public String getProjectName() {
		return projectName;
	}
	public Double getInitialInvestment() {
		return initialInvestment;
	}
	public Double getRevenueGrowthRate() {
		return revenueGrowthRate;
	}
	public Double getOperatingCostRatio() {
		return operatingCostRatio;
	}
	public Double getInflationRate() {
		return inflationRate;
	}
	public Double getDebtRatio() {
		return debtRatio;
	}
	public Double getMarketGrowthIndex() {
		return marketGrowthIndex;
	}
	public Double getSectorRiskIndex() {
		return sectorRiskIndex;
	}
	public Double getDiscountRate() {
		return discountRate;
	}
	public void setProjectName(String projectName) {
		this.projectName = projectName;
	}
	public void setInitialInvestment(Double initialInvestment) {
		this.initialInvestment = initialInvestment;
	}
	public void setRevenueGrowthRate(Double revenueGrowthRate) {
		this.revenueGrowthRate = revenueGrowthRate;
	}
	public void setOperatingCostRatio(Double operatingCostRatio) {
		this.operatingCostRatio = operatingCostRatio;
	}
	public void setInflationRate(Double inflationRate) {
		this.inflationRate = inflationRate;
	}
	public void setDebtRatio(Double debtRatio) {
		this.debtRatio = debtRatio;
	}
	public void setMarketGrowthIndex(Double marketGrowthIndex) {
		this.marketGrowthIndex = marketGrowthIndex;
	}
	public void setSectorRiskIndex(Double sectorRiskIndex) {
		this.sectorRiskIndex = sectorRiskIndex;
	}
	public void setDiscountRate(Double discountRate) {
		this.discountRate = discountRate;
	}
    
    
}
