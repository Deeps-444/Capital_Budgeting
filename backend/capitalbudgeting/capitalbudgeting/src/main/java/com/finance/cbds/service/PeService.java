package com.finance.cbds.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.finance.cbds.dto.ProjectInputDto;
import com.finance.cbds.entity.ProjectEvaluation;
import com.finance.cbds.repository.PeRepo;


@Service
public class PeService {
	
	@Autowired
	private PeRepo repo;
	
	public ProjectEvaluation saveProject(ProjectInputDto input) {

	    ProjectEvaluation project = new ProjectEvaluation();

	    project.setProjectName(input.getProjectName());
	    project.setInitialInvestment(input.getInitialInvestment());
	    project.setRevenueGrowthRate(input.getRevenueGrowthRate());
	    project.setOperatingCostRatio(input.getOperatingCostRatio());
	    project.setInflationRate(input.getInflationRate());
	    project.setDebtRatio(input.getDebtRatio());
	    project.setMarketGrowthIndex(input.getMarketGrowthIndex());
	    project.setSectorRiskIndex(input.getSectorRiskIndex());
	    project.setDiscountRate(input.getDiscountRate());

	    return repo.save(project);
	}
	
	public List<ProjectEvaluation> getAllProjects() {
		return repo.findAll();
	}
}
