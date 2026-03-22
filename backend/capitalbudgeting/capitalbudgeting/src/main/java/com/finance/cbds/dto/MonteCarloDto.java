package com.finance.cbds.dto;

public class MonteCarloDto {
	private double meanNPV;
    private double stdNPV;
    private double riskProbability;
    private PercentilesDto percentiles;
	public double getMeanNPV() {
		return meanNPV;
	}
	public void setMeanNPV(double meanNPV) {
		this.meanNPV = meanNPV;
	}
	public double getStdNPV() {
		return stdNPV;
	}
	public void setStdNPV(double stdNPV) {
		this.stdNPV = stdNPV;
	}
	public double getRiskProbability() {
		return riskProbability;
	}
	public void setRiskProbability(double riskProbability) {
		this.riskProbability = riskProbability;
	}
	public PercentilesDto getPercentiles() {
		return percentiles;
	}
	public void setPercentiles(PercentilesDto percentiles) {
		this.percentiles = percentiles;
	}
    
    //getters and setters
    
}
