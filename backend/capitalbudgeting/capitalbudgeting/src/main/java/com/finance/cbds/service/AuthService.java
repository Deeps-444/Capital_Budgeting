package com.finance.cbds.service;

import org.springframework.stereotype.Service;

import com.finance.cbds.dto.LoginRequest;
import com.finance.cbds.dto.LoginResponse;
import com.finance.cbds.entity.User;
import com.finance.cbds.repository.UserRepository;

@Service
public class AuthService {
	private final UserRepository userRepository;
	
	public AuthService(UserRepository userRepository) {
		this.userRepository = userRepository;
	}
	
	public LoginResponse login(LoginRequest request) {
		User user = userRepository.findByEmail(request.getEmail())
				.orElseThrow(() -> new RuntimeException("User not found"));
		
		if(!user.getPassword().equals(request.getPassword())) {
			throw new RuntimeException("Invalid passsword");
		}
		
		return new LoginResponse(user.getId(), user.getName(), user.getRole());
	}
}
