package com.finance.cbds.dto;

public class LoginResponse {
	private Long userId;
	private String name;
	private String role;
	public LoginResponse(Long userId, String name, String role) {
//		super();
		this.userId = userId;
		this.name = name;
		this.role = role;
	}
	public Long getUserId() {
		return userId;
	}
	public String getName() {
		return name;
	}
	public String getRole() {
		return role;
	}
	
	
}
