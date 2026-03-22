package com.finance.cbds.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "cashflow")
public class Cashflow {
	
	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Integer year;
    private Double revenue;
    private Double cost;
    private Double deltaWC;
    private Double capex;
    private Double cashflow;

    @ManyToOne
    @JoinColumn(name = "project_id")
    private ProjectEvaluation project;
    
    //getter seter

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Integer getYear() {
		return year;
	}

	public void setYear(Integer year) {
		this.year = year;
	}

	public Double getRevenue() {
		return revenue;
	}

	public void setRevenue(Double revenue) {
		this.revenue = revenue;
	}

	public Double getCost() {
		return cost;
	}

	public void setCost(Double cost) {
		this.cost = cost;
	}

	public Double getDeltaWC() {
		return deltaWC;
	}

	public void setDeltaWC(Double deltaWC) {
		this.deltaWC = deltaWC;
	}

	public Double getCapex() {
		return capex;
	}

	public void setCapex(Double capex) {
		this.capex = capex;
	}

	public Double getCashflow() {
		return cashflow;
	}

	public void setCashflow(Double cashflow) {
		this.cashflow = cashflow;
	}

	public ProjectEvaluation getProject() {
		return project;
	}

	public void setProject(ProjectEvaluation project) {
		this.project = project;
	}
    
   
    
    

}
