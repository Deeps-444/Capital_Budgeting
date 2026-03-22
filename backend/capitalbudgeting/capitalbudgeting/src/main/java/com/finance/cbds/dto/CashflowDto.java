package com.finance.cbds.dto;

public class CashflowDto {
	private int year;
    private double revenue;
    private double cost;
    private double deltaWC;
    private double capex;
    private double cashflow;
	public int getYear() {
		return year;
	}
	public void setYear(int year) {
		this.year = year;
	}
	public double getRevenue() {
		return revenue;
	}
	public void setRevenue(double revenue) {
		this.revenue = revenue;
	}
	public double getCost() {
		return cost;
	}
	public void setCost(double cost) {
		this.cost = cost;
	}
	public double getDeltaWC() {
		return deltaWC;
	}
	public void setDeltaWC(double deltaWC) {
		this.deltaWC = deltaWC;
	}
	public double getCapex() {
		return capex;
	}
	public void setCapex(double capex) {
		this.capex = capex;
	}
	public double getCashflow() {
		return cashflow;
	}
	public void setCashflow(double cashflow) {
		this.cashflow = cashflow;
	}
    
}
