package com.finance.cbds.repository;

import java.util.Collection;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.finance.cbds.dto.CashflowDto;
import com.finance.cbds.entity.ProjectEvaluation;

public interface PeRepo extends JpaRepository<ProjectEvaluation, Long>{

	List<ProjectEvaluation> findByUser_UserId(Long userId);

}
