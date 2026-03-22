package com.finance.cbds.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.finance.cbds.entity.Cashflow;
import com.finance.cbds.entity.ProjectEvaluation;

public interface CashflowRepo extends JpaRepository<Cashflow, Long>{

	List<Cashflow> findByProject(ProjectEvaluation project);
	

}
