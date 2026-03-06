package com.finance.cbds.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.finance.cbds.entity.ProjectEvaluation;

public interface PeRepo extends JpaRepository<ProjectEvaluation, Long>{

}
