package com.finance.cbds.dto;

import java.util.List;

public class MLResponseDto {
	private PredictedDriversDto predictedDrivers;
    private List<CashflowDto> cashflows;
    private MonteCarloDto monteCarlo;
    
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
	
	
	
	
	

	    
	
    
}
