package com.finance.cbds.controller;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.finance.cbds.dto.LoginRequest;
import com.finance.cbds.dto.LoginResponse;
import com.finance.cbds.service.AuthService;

@RestController // Api controller
@RequestMapping("/") // bae url 
@CrossOrigin(origins = "http://localhost:3000") // alllows react to call origin
public class AuthController {
	private final AuthService authService;

	public AuthController(AuthService authService) {
//		super();
		this.authService = authService;
	}
	
	@PostMapping("/login")
	public LoginResponse login(@RequestBody LoginRequest request) {
		return authService.login(request); // json to java object
	}
	
}
