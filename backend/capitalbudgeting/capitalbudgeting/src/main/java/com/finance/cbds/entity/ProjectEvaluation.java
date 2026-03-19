package com.finance.cbds.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;


@Entity
@Table(name = "project_evaluations")
public class ProjectEvaluation {
	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Project Information
    private String projectName;

    // Input Drivers
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

    // Predicted Cashflows (5 Years)
    private Double year1Cashflow;
    private Double year2Cashflow;
    private Double year3Cashflow;
    private Double year4Cashflow;
    private Double year5Cashflow;

    // Results
    private Double meanNPV;
    private Double riskProbability;
    
    //user
    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
    
	public User getUser() {
		return user;
	}
	public void setUser(User user) {
		this.user = user;
	}
	public String getProjectName() {
		return projectName;
	}
	public void setProjectName(String projectName) {
		this.projectName = projectName;
	}
	

	public Long getId() {
		return id;
	}



	public void setId(Long id) {
		this.id = id;
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



	public Double getWorkingCapitalRatio() {
		return workingCapitalRatio;
	}



	public void setWorkingCapitalRatio(Double workingCapitalRatio) {
		this.workingCapitalRatio = workingCapitalRatio;
	}



	public Double getCapexRatio() {
		return capexRatio;
	}



	public void setCapexRatio(Double maintenanceCapexRatio) {
		this.capexRatio = maintenanceCapexRatio;
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



	public Double getYear1Cashflow() {
		return year1Cashflow;
	}



	public void setYear1Cashflow(Double year1Cashflow) {
		this.year1Cashflow = year1Cashflow;
	}



	public Double getYear2Cashflow() {
		return year2Cashflow;
	}



	public void setYear2Cashflow(Double year2Cashflow) {
		this.year2Cashflow = year2Cashflow;
	}



	public Double getYear3Cashflow() {
		return year3Cashflow;
	}



	public void setYear3Cashflow(Double year3Cashflow) {
		this.year3Cashflow = year3Cashflow;
	}



	public Double getYear4Cashflow() {
		return year4Cashflow;
	}



	public void setYear4Cashflow(Double year4Cashflow) {
		this.year4Cashflow = year4Cashflow;
	}



	public Double getYear5Cashflow() {
		return year5Cashflow;
	}



	public void setYear5Cashflow(Double year5Cashflow) {
		this.year5Cashflow = year5Cashflow;
	}



	public Double getMeanNPV() {
		return meanNPV;
	}



	public void setMeanNPV(Double meanNpv) {
		this.meanNPV = meanNpv;
	}



	public Double getRiskProbability() {
		return riskProbability;
	}



	public void setRiskProbability(Double riskProbability) {
		this.riskProbability = riskProbability;
	}



	
	
	
    
    
    
    
}
