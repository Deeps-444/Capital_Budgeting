package com.finance.cbds.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.convert.DtoInstantiatingConverter;
import org.springframework.stereotype.Service;

import com.finance.cbds.dto.MLResponseDto;
import com.finance.cbds.dto.ProjectInputDto;
import com.finance.cbds.dto.ProjectResultDto;
import com.finance.cbds.entity.ProjectEvaluation;
import com.finance.cbds.entity.User;
import com.finance.cbds.repository.PeRepo;
import com.finance.cbds.repository.UserRepository;


@Service
public class PeService {
	
	@Autowired
	private PeRepo repo;
	
	private final UserRepository userRepository;
	
	private final MLServiceClient mlServiceClient;
	
	public PeService(PeRepo repo, UserRepository userRepository, MLServiceClient mlServiceClient) {
//		super();
		this.repo = repo;
		this.userRepository = userRepository;
		this.mlServiceClient = mlServiceClient;
	}

	public ProjectResultDto saveProject(ProjectInputDto input) {
		
		User user = userRepository.findById(input.getUserId())
				.orElseThrow(()-> new RuntimeException("User Not found"));

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
	    
	    project.setUser(user);
	    
	    //calling ml 
//	    System.out.println("Calling ML...");
	    MLResponseDto mlResponse = mlServiceClient.getPrediction(input);
//	    System.out.println("ML Response: " + mlResponse);
	    double[] cashflows = mlResponse.getPredictedCashflows();

	    project.setYear1Cashflow(cashflows[0]);
	    project.setYear2Cashflow(cashflows[1]);
	    project.setYear3Cashflow(cashflows[2]);
	    project.setYear4Cashflow(cashflows[3]);
	    project.setYear5Cashflow(cashflows[4]);

	    project.setMeanNPV(mlResponse.getMeanNPV());
	    project.setRiskProbability(mlResponse.getRiskProbability());
	    
	    
	    //save the project in db
	    repo.save(project);
	    
	    //create result dto
	    ProjectResultDto result = new ProjectResultDto();
	    result.setProjectName(project.getProjectName());
	    result.setInitialInvestment(project.getInitialInvestment());
	    result.setMeanNPV(mlResponse.getMeanNPV());
	    result.setRiskProbability(mlResponse.getRiskProbability());
	    result.setPredictedCashflows(mlResponse.getPredictedCashflows());
	    result.setNpvDistribution(mlResponse.getNpvDistribution());

	    return result;
	    
	}
	
	public List<ProjectEvaluation> getAllProjects() {
		return repo.findAll();
	}
}
