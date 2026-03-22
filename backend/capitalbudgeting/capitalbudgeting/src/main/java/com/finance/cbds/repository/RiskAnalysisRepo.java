package com.finance.cbds.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.finance.cbds.entity.ProjectEvaluation;
import com.finance.cbds.entity.RiskAnalysis;

public interface RiskAnalysisRepo extends JpaRepository<RiskAnalysis, Long> {

	RiskAnalysis findByProject(ProjectEvaluation project);
	

}
