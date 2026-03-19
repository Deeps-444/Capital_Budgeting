package com.finance.cbds.dto;

public class ProjectResultDto {
	private String projectName;

    private Double initialInvestment;
    private Double meanNPV;
    private Double riskProbability;
    private double[] predictedCashflows;
    private double[] npvDistribution;
    
   
	//getters and setters
    public double[] getNpvDistribution() {
		return npvDistribution;
	}
	public void setNpvDistribution(double[] npvDistribution) {
		this.npvDistribution = npvDistribution;
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
	public Double getMeanNPV() {
		return meanNPV;
	}
	public void setMeanNPV(Double meanNPV) {
		this.meanNPV = meanNPV;
	}
	public Double getRiskProbability() {
		return riskProbability;
	}
	public void setRiskProbability(Double riskProbability) {
		this.riskProbability = riskProbability;
	}
	public double[] getPredictedCashflows() {
		return predictedCashflows;
	}
	public void setPredictedCashflows(double[] predictedCashflows) {
		this.predictedCashflows = predictedCashflows;
	}
    
    
    
}
