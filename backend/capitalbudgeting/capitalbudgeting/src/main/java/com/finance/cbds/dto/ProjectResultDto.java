package com.finance.cbds.dto;

import java.util.List;

public class ProjectResultDto {
	private String projectName;
	private Double initialInvestment;
	//drivers
	private PredictedDriversDto predictedDrivers;

    // Cashflows
    private List<CashflowDto> cashflows;

    // Risk Metrics
    private Double meanNPV;
    private Double stdNPV;
    private Double riskProbability;

    private Double p10;
    private Double p50;
    private Double p90;
    
  //getters and setters------------------
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
	public PredictedDriversDto getPredictedDrivers() {
		return predictedDrivers;
	}
	public void setPredictedDrivers(PredictedDriversDto predictedDrivers) {
		this.predictedDrivers = predictedDrivers;
	}
	public List<CashflowDto> getCashflows() {
		return cashflows;
	}
	public void setCashflows(List<CashflowDto> cashflows) {
		this.cashflows = cashflows;
	}
	public Double getMeanNPV() {
		return meanNPV;
	}
	public void setMeanNPV(Double meanNPV) {
		this.meanNPV = meanNPV;
	}
	public Double getStdNPV() {
		return stdNPV;
	}
	public void setStdNPV(Double stdNPV) {
		this.stdNPV = stdNPV;
	}
	public Double getRiskProbability() {
		return riskProbability;
	}
	public void setRiskProbability(Double riskProbability) {
		this.riskProbability = riskProbability;
	}
	public Double getP10() {
		return p10;
	}
	public void setP10(Double p10) {
		this.p10 = p10;
	}
	public Double getP50() {
		return p50;
	}
	public void setP50(Double p50) {
		this.p50 = p50;
	}
	public Double getP90() {
		return p90;
	}
	public void setP90(Double p90) {
		this.p90 = p90;
	}
    
   
	
    
    
    
    
}
