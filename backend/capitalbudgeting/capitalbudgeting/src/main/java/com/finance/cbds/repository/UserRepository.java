package com.finance.cbds.repository;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
// gives crud automatically

import com.finance.cbds.entity.User;


public interface UserRepository extends JpaRepository<User, Long>{
	Optional<User> findByEmail(String email);
}
