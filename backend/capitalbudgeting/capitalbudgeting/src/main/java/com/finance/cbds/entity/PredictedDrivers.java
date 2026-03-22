package com.finance.cbds.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "predicted_drivers")
public class PredictedDrivers {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	private Double operatingCostRatio;
    private Double workingCapitalRatio;
    private Double capexRatio;
    
    @ManyToOne
    @JoinColumn(name = "project_id")
    private ProjectEvaluation project;

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Double getOperatingCostRatio() {
		return operatingCostRatio;
	}

	public void setOperatingCostRatio(Double operatingCostRatio) {
		this.operatingCostRatio = operatingCostRatio;
	}

	public Double getWorkingCapitalRatio() {
		return workingCapitalRatio;
	}

	public void setWorkingCapitalRatio(Double workingCapitalRatio) {
		this.workingCapitalRatio = workingCapitalRatio;
	}

	public Double getCapexRatio() {
		return capexRatio;
	}

	public void setCapexRatio(Double capexRatio) {
		this.capexRatio = capexRatio;
	}

	public ProjectEvaluation getProject() {
		return project;
	}

	public void setProject(ProjectEvaluation project) {
		this.project = project;
	}
    
    
	
}
