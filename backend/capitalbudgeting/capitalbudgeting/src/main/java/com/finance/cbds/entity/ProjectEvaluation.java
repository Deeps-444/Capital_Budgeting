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
    private Double inflationRate;
    private Double debtRatio;
    private Double marketGrowthIndex;
    private Double sectorRiskIndex;
    private Double discountRate;

    
    //user
    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
    
    private Double npv;
    private Double irr;
    
	public Double getNpv() {
		return npv;
	}
	public void setNpv(Double npv) {
		this.npv = npv;
	}
	public Double getIrr() {
		return irr;
	}
	public void setIrr(Double irr) {
		this.irr = irr;
	}
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
