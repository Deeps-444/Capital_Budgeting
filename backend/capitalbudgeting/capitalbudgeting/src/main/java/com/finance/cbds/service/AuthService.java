package com.finance.cbds.service;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.finance.cbds.dto.LoginRequest;
import com.finance.cbds.dto.LoginResponse;
import com.finance.cbds.dto.RegisterDto;
import com.finance.cbds.entity.User;
import com.finance.cbds.repository.UserRepository;

@Service
public class AuthService {
	private final UserRepository userRepository;
	private final BCryptPasswordEncoder passwordEncoder;
	
	public AuthService(UserRepository userRepository, BCryptPasswordEncoder passwordEncoder) {
		this.userRepository = userRepository;
		this.passwordEncoder = passwordEncoder;
	}
	
	// FUNCTION FOR LOGIN
	public LoginResponse login(LoginRequest request) {
		User user = userRepository.findByEmail(request.getEmail())
				.orElseThrow(() -> new RuntimeException("User not found"));
		
		if(!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
			throw new RuntimeException("Invalid passsword");
		}
		System.out.println("RAW PASSWORD: " + request.getPassword());
		System.out.println("DB PASSWORD: " + user.getPassword());
		System.out.println("MATCHES: " + passwordEncoder.matches(request.getPassword(), user.getPassword()));
		
		return new LoginResponse(user.getUserId(), user.getName(), user.getRole());
	}
	
	// FUNCTION FOR REGISTER
	public String register(RegisterDto request) {

	    // check if user exists
	    if (userRepository.findByEmail(request.getEmail()).isPresent()) {
	        throw new RuntimeException("User already exists");
	    }

	    User user = new User();
	    user.setName(request.getName());
	    user.setEmail(request.getEmail());

	    
	    user.setPassword(passwordEncoder.encode(request.getPassword()));

	    user.setRole("USER");

	    userRepository.save(user);

	    return "User registered successfully";
	}
}
