package com.finance.cbds.dto;

import java.util.List;

public class MLResponseDto {
	private PredictedDriversDto predictedDrivers;
    private List<CashflowDto> cashflows;
    private MonteCarloDto monteCarlo;
    private double npv;
    private double irr;
    
  
	//getter and setter
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
	public MonteCarloDto getMonteCarlo() {
		return monteCarlo;
	}
	public void setMonteCarlo(MonteCarloDto monteCarlo) {
		this.monteCarlo = monteCarlo;
	}
	public double getNpv() {
		return npv;
	}
	public void setNpv(double npv) {
		this.npv = npv;
	}
	public double getIrr() {
		return irr;
	}
	public void setIrr(double irr) {
		this.irr = irr;
	}
	
	
	
	
	

	    
	
    
}
