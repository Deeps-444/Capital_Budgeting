package com.finance.cbds.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.finance.cbds.entity.PredictedDrivers;
import com.finance.cbds.entity.ProjectEvaluation;

public interface PredictedDriversRepo extends JpaRepository<PredictedDrivers, Long> {

	PredictedDrivers findByProject(ProjectEvaluation project);
	

}
