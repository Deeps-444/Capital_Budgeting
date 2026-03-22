package com.finance.cbds.dto;

public class ProjectInputDto {
	private Long userId;
	private String projectName;
	
	private double initialInvestment;
	private double revenueGrowthRate;
	private double inflationRate;
	private double marketGrowthIndex;
	private double sectorRiskIndex;
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
	public double getMarketGrowthIndex() {
		return marketGrowthIndex;
	}
	public void setMarketGrowthIndex(double marketGrowthIndex) {
		this.marketGrowthIndex = marketGrowthIndex;
	}
	public double getSectorRiskIndex() {
		return sectorRiskIndex;
	}
	public void setSectorRiskIndex(double sectorRiskIndex) {
		this.sectorRiskIndex = sectorRiskIndex;
	}
	public double getDiscountRate() {
		return discountRate;
	}
	public void setDiscountRate(double discountRate) {
		this.discountRate = discountRate;
	}
	
	
	
}
