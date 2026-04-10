package com.finance.cbds.dto;

public class ProjectInputDto {
	private Long userId;
	private String projectName;
	
	private double initialInvestment;
	private double revenueGrowthRate;
	private double inflationRate;
	private String marketGrowthIndex; //changed
	private String sectorRiskIndex; // changed
	private double discountRate;
	
	//getter and setter
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
	public double getInitialInvestment() {
		return initialInvestment;
	}
	public void setInitialInvestment(double initialInvestment) {
		this.initialInvestment = initialInvestment;
	}
	public double getRevenueGrowthRate() {
		return revenueGrowthRate;
	}
	public void setRevenueGrowthRate(double revenueGrowthRate) {
		this.revenueGrowthRate = revenueGrowthRate;
	}
	public double getInflationRate() {
		return inflationRate;
	}
	public void setInflationRate(double inflationRate) {
		this.inflationRate = inflationRate;
	}
	
	public String getMarketGrowthIndex() {
		return marketGrowthIndex;
	}
	public void setMarketGrowthIndex(String marketGrowthIndex) {
		this.marketGrowthIndex = marketGrowthIndex;
	}
	public String getSectorRiskIndex() {
		return sectorRiskIndex;
	}
	public void setSectorRiskIndex(String sectorRiskIndex) {
		this.sectorRiskIndex = sectorRiskIndex;
	}
	public double getDiscountRate() {
		return discountRate;
	}
	public void setDiscountRate(double discountRate) {
		this.discountRate = discountRate;
	}
	
	
	
}
