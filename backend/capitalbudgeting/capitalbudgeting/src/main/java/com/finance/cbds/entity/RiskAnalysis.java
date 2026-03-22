package com.finance.cbds.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "risk_analysis")
public class RiskAnalysis {
	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Double meanNPV;
    private Double stdNPV;
    private Double riskProbability;

    private Double p10;
    private Double p50;
    private Double p90;

    @ManyToOne
    @JoinColumn(name = "project_id")
    private ProjectEvaluation project;

    //geter and setter
	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
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

	public ProjectEvaluation getProject() {
		return project;
	}

	public void setProject(ProjectEvaluation project) {
		this.project = project;
	}
    
   
    
    
}
