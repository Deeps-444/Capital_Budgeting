package com.finance.cbds.finance;

public class NPVCalculator {
	
	public static double calculateNPV(double initialInvestement, double[] cashflows, double discountRate) {
		double npv = -initialInvestement;
		
		for (int t = 0; t < cashflows.length; t++) {
            npv += cashflows[t] / Math.pow(1 + discountRate, t + 1);
        }
		return npv;
	}
}
