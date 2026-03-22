package com.finance.cbds.repository;
import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
// gives crud automatically

import com.finance.cbds.entity.ProjectEvaluation;
import com.finance.cbds.entity.User;


public interface UserRepository extends JpaRepository<User, Long>{
	Optional<User> findByEmail(String email);
	Optional<User> findByUserId(Long userId);
}
