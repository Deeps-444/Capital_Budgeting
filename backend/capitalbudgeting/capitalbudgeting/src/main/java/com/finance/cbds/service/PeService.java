package com.finance.cbds.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.stereotype.Service;

import com.finance.cbds.dto.CashflowDto;
import com.finance.cbds.dto.MLResponseDto;
import com.finance.cbds.dto.PredictedDriversDto;
import com.finance.cbds.dto.ProjectInputDto;
import com.finance.cbds.dto.ProjectResultDto;
import com.finance.cbds.entity.Cashflow;
import com.finance.cbds.entity.PredictedDrivers;
import com.finance.cbds.entity.ProjectEvaluation;
import com.finance.cbds.entity.RiskAnalysis;
import com.finance.cbds.entity.User;
import com.finance.cbds.repository.CashflowRepo;
import com.finance.cbds.repository.PeRepo;
import com.finance.cbds.repository.PredictedDriversRepo;
import com.finance.cbds.repository.RiskAnalysisRepo;
import com.finance.cbds.repository.UserRepository;

import jakarta.transaction.Transactional;


@Service
public class PeService {
	
	@Autowired
	private PredictedDriversRepo driversRepo;

	@Autowired
	private CashflowRepo cashflowRepo;

	@Autowired
	private RiskAnalysisRepo riskRepo;
	
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
	
	// MAPPING TO DTO
	private ProjectResultDto mapToResultDto(ProjectEvaluation project, MLResponseDto mlResponse) {

	    ProjectResultDto result = new ProjectResultDto();
	    result.setProjectId(project.getId());
	    result.setProjectName(project.getProjectName());
	    result.setInitialInvestment(project.getInitialInvestment());

	    result.setPredictedDrivers(mlResponse.getPredictedDrivers());
	    result.setCashflows(mlResponse.getCashflows());

	    result.setMeanNPV(mlResponse.getMonteCarlo().getMeanNPV());
	    result.setRiskProbability(mlResponse.getMonteCarlo().getRiskProbability());
	    result.setStdNPV(mlResponse.getMonteCarlo().getStdNPV());

	    result.setP10(mlResponse.getMonteCarlo().getPercentiles().getP10());
	    result.setP50(mlResponse.getMonteCarlo().getPercentiles().getP50());
	    result.setP90(mlResponse.getMonteCarlo().getPercentiles().getP90());
	    result.setNPV(mlResponse.getNpv());
	    result.setIRR(mlResponse.getIrr());

	    return result;
	}
	
	// CONEVRTING TO DTO
	private ProjectResultDto convertToDto(ProjectEvaluation project) {

	    ProjectResultDto dto = new ProjectResultDto();
	    
	    dto.setProjectId(project.getId());
	    dto.setProjectName(project.getProjectName());
	    dto.setInitialInvestment(project.getInitialInvestment());
	    dto.setNPV(project.getNpv());
	    dto.setIRR(project.getIrr());

	    // Drivers
	    PredictedDrivers drivers = driversRepo.findByProject(project);
	    PredictedDriversDto driversDto = new PredictedDriversDto();
	    driversDto.setOperatingCostRatio(drivers.getOperatingCostRatio());
	    driversDto.setWorkingCapitalRatio(drivers.getWorkingCapitalRatio());
	    driversDto.setCapexRatio(drivers.getCapexRatio());

	    dto.setPredictedDrivers(driversDto);
	    
	    // Cashflows
	    List<Cashflow> cashflows = cashflowRepo.findByProject(project);
	    List<CashflowDto> cfDtos = cashflows.stream().map(cf -> {
	        CashflowDto c = new CashflowDto();
	        c.setYear(cf.getYear());
	        c.setRevenue(cf.getRevenue());
	        c.setCost(cf.getCost());
	        c.setDeltaWC(cf.getDeltaWC());
	        c.setCapex(cf.getCapex());
	        c.setCashflow(cf.getCashflow());
	        return c;
	    }).toList();

	    dto.setCashflows(cfDtos);

	    // Risk
	    RiskAnalysis risk = riskRepo.findByProject(project);

	    dto.setMeanNPV(risk.getMeanNPV());
	    dto.setStdNPV(risk.getStdNPV());
	    dto.setRiskProbability(risk.getRiskProbability());
	    dto.setP10(risk.getP10());
	    dto.setP50(risk.getP50());
	    dto.setP90(risk.getP90());

	    return dto;
	}
	
	// SAVING PROJECT

	@Transactional
	public ProjectResultDto saveProject(ProjectInputDto input) {

	    
	    // GET USER
	    User user = userRepository.findById(input.getUserId())
	            .orElseThrow(() -> new RuntimeException("User Not found"));
	    
	    // taking the scenario as string and converting into double
	    
	    double marketIndex;
	    double riskIndex;

	   // Market mapping
	    switch (input.getMarketGrowthIndex()) {
	        case "LOW": marketIndex = 0.8; break;
	        case "MEDIUM": marketIndex = 1.0; break;
	        case "HIGH": marketIndex = 1.2; break;
	        default: marketIndex = 1.0;
	    }

	   // Risk mapping
	    switch (input.getSectorRiskIndex()) {
	       case "LOW": riskIndex = 0.8; break;
	       case "MEDIUM": riskIndex = 1.0; break;
	       case "HIGH": riskIndex = 1.3; break;
	       default: riskIndex = 1.0;
	    }
	    
	    //  CREATE + SAVE PROJECT
	    
	    ProjectEvaluation project = new ProjectEvaluation();

	    project.setProjectName(input.getProjectName());
	    project.setInitialInvestment(input.getInitialInvestment());
	    project.setRevenueGrowthRate(input.getRevenueGrowthRate());
	    project.setInflationRate(input.getInflationRate());
	    project.setMarketGrowthIndex(marketIndex);
	    project.setSectorRiskIndex(riskIndex);
	    project.setDiscountRate(input.getDiscountRate());
	    project.setUser(user);

	    project = repo.save(project); 
	    
	    // for ml to receive values not string
	    input.setMarketGrowthIndex(String.valueOf(marketIndex));
	    input.setSectorRiskIndex(String.valueOf(riskIndex));
	    
	    //  call ml service
	    MLResponseDto mlResponse = mlServiceClient.getPrediction(input, marketIndex, riskIndex);

	    if (mlResponse == null) {
	        throw new RuntimeException("ML service failed");
	    }

	    
	    // new update !!!
	    project.setNpv(mlResponse.getNpv());
	    project.setIrr(mlResponse.getIrr());

	    repo.save(project); // update db

	    
	    //  SAVE PREDICTED DRIVERS
	    
	    PredictedDrivers drivers = new PredictedDrivers();

	    drivers.setProject(project);
	    drivers.setOperatingCostRatio(
	            mlResponse.getPredictedDrivers().getOperatingCostRatio()
	    );
	    drivers.setWorkingCapitalRatio(
	            mlResponse.getPredictedDrivers().getWorkingCapitalRatio()
	    );
	    drivers.setCapexRatio(
	            mlResponse.getPredictedDrivers().getCapexRatio()
	    );

	    driversRepo.save(drivers);

	    
	    // SAVE CASHFLOWS
	    for (CashflowDto cfDto : mlResponse.getCashflows()) {

	        Cashflow cf = new Cashflow();

	        cf.setProject(project);
	        cf.setYear(cfDto.getYear());
	        cf.setRevenue(cfDto.getRevenue());

	        // ⚠️ CHECK THIS MAPPING
	        cf.setCost(cfDto.getCost());
	        cf.setDeltaWC(cfDto.getDeltaWC());

	        cf.setCapex(cfDto.getCapex());
	        cf.setCashflow(cfDto.getCashflow());

	        cashflowRepo.save(cf);
	    }

	    // SAVE RISK ANALYSIS
	    
	    if (mlResponse.getMonteCarlo() == null) {
	        throw new RuntimeException("Monte Carlo missing");
	    }

	    RiskAnalysis risk = new RiskAnalysis();

	    risk.setProject(project);
	    risk.setMeanNPV(mlResponse.getMonteCarlo().getMeanNPV());
	    risk.setStdNPV(mlResponse.getMonteCarlo().getStdNPV());
	    risk.setRiskProbability(mlResponse.getMonteCarlo().getRiskProbability());

	    risk.setP10(mlResponse.getMonteCarlo().getPercentiles().getP10());
	    risk.setP50(mlResponse.getMonteCarlo().getPercentiles().getP50());
	    risk.setP90(mlResponse.getMonteCarlo().getPercentiles().getP90());

	    riskRepo.save(risk);

	   
	    // RETURN RESULT	    
	    return mapToResultDto(project, mlResponse);
	}
	
	
	public List<ProjectResultDto> getProjectsByUser(Long userId) {
	    return repo.findByUser_UserId(userId)
	            .stream()
	            .map(this::convertToDto)
	            .toList();
	}

	public ProjectResultDto getProjectById(Long projectId) {
	    ProjectEvaluation project = repo.findById(projectId).orElseThrow();
	    return convertToDto(project);
	}
	
	public List<ProjectEvaluation> getAllProjects() {
		return repo.findAll();
	}
}
