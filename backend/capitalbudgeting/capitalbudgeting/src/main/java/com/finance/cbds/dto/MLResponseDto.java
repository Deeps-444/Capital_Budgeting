package com.finance.cbds.dto;

public class MLResponseDto {
	private double[] predictedCashflows;
	private Double meanNPV;
	private double[] npvDistribution;
	private Double riskProbability;
	
	//getter and setter
	
	public double[] getNpvDistribution() {
		return npvDistribution;
	}
	public void setNpvDistribution(double[] npvDistribution) {
		this.npvDistribution = npvDistribution;
	}
	public double[] getPredictedCashflows() {
		return predictedCashflows;
	}
	public void setPredictedCashflows(double[] predictedCashflows) {
		this.predictedCashflows = predictedCashflows;
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

	    
	
    
}
